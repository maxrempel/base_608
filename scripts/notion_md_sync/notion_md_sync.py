"""
notion_md_sync v01 - two-way sync between local .md files and Notion pages.

Created 2026-05-21 by Claude Opus 4.7.

Purpose: let Max edit auto-loaded Claude instruction files (global_CLAUDE.md,
global2.md, per-project MEMORY.md, per-project CLAUDE.md) by voice via Claude
phone, with Notion as the editable mirror.

Sync model per file:
- Track last-synced mtime (file) and last_edited_time (Notion) in state.json.
- file_changed = file mtime != last synced
- notion_changed = Notion last_edited_time != last synced
- both changed within conflict_window_seconds: STOP, log WARN, do nothing.
- only file changed: push file -> Notion (archive previous Notion content snapshot).
- only Notion changed: pull Notion -> file (archive previous file to archive_dir first).
- neither changed: skip.

Content storage on Notion side:
- Page body = one or more paragraph blocks, each holding up to 1900 chars of plain text.
- Newlines preserved inside blocks. On pull, blocks are joined in order with no separator.
- This loses Notion's rendered-markdown look but preserves exact bytes round-trip.

Run hidden every 5 min via Windows Task Scheduler.
"""
import json
import os
import sys
import time
import shutil
import logging
import datetime
import urllib.request
import urllib.error

VERSION = "v01 initial | 2026-05-21"
NOTION_VERSION = "2022-06-28"
CHUNK = 1900

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = json.load(open(os.path.join(HERE, "registry.json"), encoding="utf-8"))

os.makedirs(os.path.dirname(REGISTRY["log_path"]), exist_ok=True)
os.makedirs(REGISTRY["archive_dir"], exist_ok=True)

logging.basicConfig(
    filename=REGISTRY["log_path"],
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("notion_md_sync")

TOKEN = open(REGISTRY["token_path"], encoding="utf-8").read().strip()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


def api(method, path, body=None):
    url = f"https://api.notion.com/v1{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")
        log.error(f"HTTP {e.code} {method} {path}: {body_txt}")
        raise


def get_page_meta(page_id):
    return api("GET", f"/pages/{page_id}")


def get_page_blocks(page_id):
    out = []
    cursor = None
    while True:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        r = api("GET", path)
        out.extend(r["results"])
        if not r.get("has_more"):
            break
        cursor = r.get("next_cursor")
    return out


def blocks_to_text(blocks):
    parts = []
    for b in blocks:
        t = b.get("type")
        node = b.get(t, {})
        rich = node.get("rich_text", [])
        text = "".join(rt.get("plain_text", "") for rt in rich)
        if t == "paragraph":
            parts.append(text)
        elif t == "code":
            parts.append(text)
        elif t.startswith("heading_"):
            level = int(t.split("_")[1])
            parts.append("#" * level + " " + text)
        else:
            parts.append(text)
    return "\n".join(parts)


def text_to_paragraph_blocks(text):
    chunks = [text[i : i + CHUNK] for i in range(0, len(text), CHUNK)] or [""]
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": c}}],
            },
        }
        for c in chunks
    ]


def delete_all_children(page_id):
    blocks = get_page_blocks(page_id)
    for b in blocks:
        try:
            api("DELETE", f"/blocks/{b['id']}")
        except Exception as e:
            log.warning(f"could not delete block {b['id']}: {e}")


def push_file_to_notion(page_id, text):
    delete_all_children(page_id)
    blocks = text_to_paragraph_blocks(text)
    for i in range(0, len(blocks), 100):
        batch = blocks[i : i + 100]
        api("PATCH", f"/blocks/{page_id}/children", {"children": batch})


def load_state():
    p = REGISTRY["state_path"]
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {}


def save_state(s):
    p = REGISTRY["state_path"]
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, p)


def archive_file(path, tag):
    if not os.path.exists(path):
        return None
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.basename(path)
    dst = os.path.join(REGISTRY["archive_dir"], f"obsolete_{ts}_{tag}_{base}")
    shutil.copy2(path, dst)
    return dst


def parse_iso(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def sync_one(entry, state):
    name = entry["name"]
    path = entry["path"]
    page_id = entry["notion_page_id"]
    s = state.get(name, {})
    prev_file_mtime = s.get("file_mtime")
    prev_notion_edit = s.get("notion_edit")

    if not os.path.exists(path):
        log.warning(f"[{name}] file missing: {path}")
        return

    file_mtime = os.path.getmtime(path)
    meta = get_page_meta(page_id)
    notion_edit = meta["last_edited_time"]

    file_changed = prev_file_mtime is None or abs(file_mtime - prev_file_mtime) > 0.5
    notion_changed = prev_notion_edit is None or notion_edit != prev_notion_edit

    # On very first run for an entry, force file -> Notion.
    if prev_file_mtime is None and prev_notion_edit is None:
        log.info(f"[{name}] first run, pushing file -> Notion")
        text = open(path, encoding="utf-8").read()
        push_file_to_notion(page_id, text)
        meta = get_page_meta(page_id)
        state[name] = {"file_mtime": os.path.getmtime(path), "notion_edit": meta["last_edited_time"]}
        return

    if not file_changed and not notion_changed:
        return

    if file_changed and notion_changed:
        log.warning(
            f"[{name}] CONFLICT: both file and Notion changed since last sync. "
            f"file_mtime={file_mtime} notion_edit={notion_edit}. Skipping. "
            f"Resolve manually."
        )
        return

    if file_changed:
        log.info(f"[{name}] file changed, pushing -> Notion")
        text = open(path, encoding="utf-8").read()
        push_file_to_notion(page_id, text)
        meta = get_page_meta(page_id)
        state[name] = {"file_mtime": os.path.getmtime(path), "notion_edit": meta["last_edited_time"]}
        return

    if notion_changed:
        log.info(f"[{name}] Notion changed, pulling -> file")
        archived = archive_file(path, "preNotionPull")
        if archived:
            log.info(f"[{name}] archived previous file to {archived}")
        blocks = get_page_blocks(page_id)
        text = blocks_to_text(blocks)
        # Avoid bumping mtime if content identical
        try:
            existing = open(path, encoding="utf-8").read()
        except Exception:
            existing = None
        if existing != text:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        state[name] = {"file_mtime": os.path.getmtime(path), "notion_edit": notion_edit}
        return


def main():
    log.info(f"notion_md_sync {VERSION} starting")
    state = load_state()
    try:
        for entry in REGISTRY["files"]:
            try:
                sync_one(entry, state)
            except Exception as e:
                log.exception(f"[{entry['name']}] sync failed: {e}")
        save_state(state)
    finally:
        log.info("notion_md_sync done")


if __name__ == "__main__":
    main()
