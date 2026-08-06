#!/usr/bin/env python3
"""Codex thread model-labeler.

Prefixes every saved Codex thread title with a short model tag so Max can see
which backend ran each session, e.g. "[Q3.8] Fix login bug".

The Codex desktop app also manages titles itself: for active sessions it
generates informative names and stamps them with its own lowercase tag
("ds Build resumable downloads system", "deepseek ...", "qw ..."). This
labeler treats those native tags as already-present and normalizes them to the
standard "[TAG] " form, so we never create "[DS] ds ..." double tags. For
threads the app left with raw dictation-style first-message titles, it derives
a short informative title from the first user message.

Tags:
  GPT   -> OpenAI / ChatGPT models (gpt-*, o1/o3/o4, chatgpt, provider=openai)
  DS    -> DeepSeek models (deepseek-*)
  Q3.8  -> Qwen 3.8 (qwen3.8*)
  Q3.7  -> Qwen 3.7 (qwen3.7*)
  Q3.5  -> Qwen 3.5 (qwen3.5*)
  Q3    -> Qwen 3 Max (qwen3-max)
  Q3C   -> Qwen3 Coder (qwen3-coder*)
  QW    -> other Qwen (provider=qwen fallback)

It reads the Codex thread database (state_5.sqlite) as the source of truth and
also updates the sidebar display index (session_index.jsonl), because the
desktop app shows thread_name from that index. Every apply:
  1. Writes a consistent SQLite backup + a copy of session_index.jsonl.
  2. Records a changes.json manifest (the undo recipe).
  3. Prefixes threads.title in the DB and appends a new session_index entry.

Undo restores both from the manifest. Labeling is idempotent: any title that
already starts with a "[TAG] " prefix is left untouched.

Usage:
  python label_threads.py preview            # show what would change
  python label_threads.py apply              # backup + label
  python label_threads.py undo               # undo most recent apply
  python label_threads.py undo --run <dir>   # undo a specific run
  python label_threads.py status             # tag distribution
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

CODEX_HOME = os.path.join(os.path.expanduser("~"), ".codex")
DEFAULT_DB = os.path.join(CODEX_HOME, "state_5.sqlite")
DEFAULT_INDEX = os.path.join(CODEX_HOME, "session_index.jsonl")
BACKUP_ROOT = os.path.join(CODEX_HOME, "backups", "thread_labels")

PREFIX_RE = re.compile(r"^\[[^\]]+\]\s")
CANON_PREFIX_RE = re.compile(r"^\[([^\]]+)\]\s*(.*)$", re.S)
BARE_PREFIX_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s+(.*)$", re.S)

# The app's native lowercase tags, mapped to our standard tags. Plain "qwen"
# is deliberately excluded so titles like "Qwen graph to 3 trackers" are not
# mistaken for a tag.
BARE_TAG_ALIASES = {
    "ds": "DS",
    "deepseek": "DS",
    "gpt": "GPT",
    "openai": "GPT",
    "chatgpt": "GPT",
    "qw": "QW",
    "q3.8": "Q3.8",
    "qwen3.8": "Q3.8",
    "q3.7": "Q3.7",
    "qwen3.7": "Q3.7",
    "q3.5": "Q3.5",
    "qwen3.5": "Q3.5",
    "q3": "Q3",
    "qwen3-max": "Q3",
    "q3c": "Q3C",
    "qwen3-coder": "Q3C",
}

# Dictation-style openers that usually precede the actual topic of a message.
FILLER_RE = re.compile(
    r"^(okay|ok|so|well|hey|hi|hello|yes|no|roger|right|great|good|thanks|"
    r"thank you|please|look|listen|also|now)[,:\s]+",
    re.I,
)
OPENER_PATTERNS = [
    r"^you are\s+",
    r"^you're\s+",
    r"^your task is to\s+",
    r"^your task[:;]?\s*",
    r"^your job is to\s+",
    r"^i need you to\s+",
    r"^we need to\s+",
    r"^i want you to\s+",
    r"^we want to\s+",
    r"^please\s+",
    r"^can you\s+",
    r"^could you\s+",
]


def tag_for(model: str | None, provider: str | None) -> str | None:
    m = (model or "").strip().lower()
    p = (provider or "").strip().lower()
    if m.startswith("qwen3.8"):
        return "Q3.8"
    if m.startswith("qwen3.7"):
        return "Q3.7"
    if m.startswith("qwen3.5"):
        return "Q3.5"
    if m.startswith("qwen3-max"):
        return "Q3"
    if m.startswith("qwen3-coder"):
        return "Q3C"
    if m.startswith("qwen"):
        return "QW"
    if m.startswith("deepseek"):
        return "DS"
    if m.startswith(("gpt", "o1", "o3", "o4", "chatgpt")):
        return "GPT"
    if p == "qwen":
        return "QW"
    if p == "deepseek":
        return "DS"
    if p == "openai":
        return "GPT"
    return None


def split_tag(name: str) -> tuple[str | None, str]:
    """Return (canonical tag, base title) for a display name.

    Handles both our "[TAG] base" form and the app's native bare form
    ("ds base", "deepseek base", "qw base"). A non-tag leading word is left
    untouched (tag=None, base=whole name).
    """
    name = (name or "").strip()
    if not name:
        return None, name
    m = CANON_PREFIX_RE.match(name)
    if m:
        return m.group(1).upper(), m.group(2).strip()
    m = BARE_PREFIX_RE.match(name)
    if m and m.group(1).lower() in BARE_TAG_ALIASES:
        return BARE_TAG_ALIASES[m.group(1).lower()], m.group(2).strip()
    return None, name


def looks_raw(base: str, first_message: str | None) -> bool:
    base = (base or "").strip()
    if not base:
        return False
    if len(base) > 45:
        return True
    if FILLER_RE.match(base):
        return True
    if first_message and len(base) > 25 and base == first_message[: len(base)]:
        return True
    return False


def clean_text(s: str) -> str:
    """Turn a raw dictation-style fragment into a short readable title."""
    s = (s or "").replace("…", " ").replace("...", " ").strip()
    prev = None
    while prev != s:
        prev = s
        s = FILLER_RE.sub("", s).strip()
    for pattern in OPENER_PATTERNS:
        s = re.sub(pattern, "", s, flags=re.I).strip()
    if not s:
        return ""
    s = s[0].upper() + s[1:]
    if len(s) <= 64:
        return s
    cut = s[:64]
    for sep in (".", "!", "?", ";", ","):
        i = cut.rfind(sep)
        if i > 20:
            cut = cut[:i]
            break
    else:
        i = cut.rfind(" ")
        if i > 20:
            cut = cut[:i]
    return cut.strip(" ,;:") + "…"


def desired_title(
    tag: str, display: str | None, first_message: str | None
) -> str | None:
    """Return the full title this thread should have, or None if unchanged."""
    display = (display or "").strip() or (first_message or "").strip()
    if not display:
        return None
    existing_tag, base = split_tag(display)
    if existing_tag is not None:
        # Peel a nested tag too, e.g. "[DS] ds ..." or "ds [DS] ...".
        inner_tag, base2 = split_tag(base) if base else (None, base)
        if inner_tag is not None:
            base = base2
        if not base:
            return None  # tag-only title; nothing to build on
        if display.startswith("[") and existing_tag == tag and inner_tag is None:
            return None  # already canonical with the right tag
        base = clean_text(base) if looks_raw(base, first_message) else base
        return f"[{tag}] {base}"
    base = clean_text(display) if looks_raw(display, first_message) else display
    return f"[{tag}] {base}"


def read_threads(db_path: str):
    con = sqlite3.connect(db_path, timeout=15)
    try:
        cur = con.execute(
            "SELECT id, title, model, model_provider, first_user_message "
            "FROM threads"
        )
        return cur.fetchall()
    finally:
        con.close()


def read_index_latest(index_path: str) -> dict:
    latest = {}
    if not os.path.exists(index_path):
        return latest
    with open(index_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            tid = entry.get("id")
            if tid:
                latest[tid] = entry.get("thread_name")
    return latest


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def build_plan(db_path: str, index_path: str):
    threads = read_threads(db_path)
    index_latest = read_index_latest(index_path)
    plan = []
    skipped_unknown = 0
    skipped_already = 0
    for tid, title, model, provider, first_message in threads:
        tag = tag_for(model, provider)
        if not tag:
            skipped_unknown += 1
            continue
        index_name = index_latest.get(tid)
        display = index_name or title
        new_title = desired_title(tag, display, first_message)
        if new_title is None:
            skipped_already += 1
            continue
        plan.append(
            {
                "id": tid,
                "tag": tag,
                "old_db_title": title,
                "new_db_title": new_title,
                "in_index": tid in index_latest,
                "old_index_name": index_name,
                "new_index_name": new_title,
            }
        )
    return plan, skipped_unknown, skipped_already


def backup_db(db_path: str, dest_path: str):
    src = sqlite3.connect(db_path, timeout=15)
    try:
        dst = sqlite3.connect(dest_path)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()


def apply_plan(db_path: str, index_path: str, plan) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = os.path.join(BACKUP_ROOT, f"run_{stamp}")
    os.makedirs(run_dir, exist_ok=True)

    backup_db(db_path, os.path.join(run_dir, "state_5.sqlite.bak"))
    if os.path.exists(index_path):
        shutil.copy2(index_path, os.path.join(run_dir, "session_index.jsonl.bak"))

    with open(os.path.join(run_dir, "changes.json"), "w", encoding="utf-8") as fh:
        json.dump(
            {"stamp": stamp, "db": db_path, "index": index_path, "changes": plan},
            fh,
            ensure_ascii=False,
            indent=2,
        )

    con = sqlite3.connect(db_path, timeout=15)
    try:
        with con:
            for change in plan:
                con.execute(
                    "UPDATE threads SET title = ? WHERE id = ?",
                    (change["new_db_title"], change["id"]),
                )
    finally:
        con.close()

    now = utc_stamp()
    appended = 0
    with open(index_path, "a", encoding="utf-8") as fh:
        for change in plan:
            new_name = change["new_index_name"]
            if not new_name:
                if not change["in_index"]:
                    new_name = change["new_db_title"]
                else:
                    continue
            fh.write(
                json.dumps(
                    {"id": change["id"], "thread_name": new_name, "updated_at": now},
                    ensure_ascii=False,
                )
                + "\n"
            )
            appended += 1
    return run_dir


def newest_run() -> str | None:
    if not os.path.isdir(BACKUP_ROOT):
        return None
    runs = sorted(d for d in os.listdir(BACKUP_ROOT) if d.startswith("run_"))
    if not runs:
        return None
    return os.path.join(BACKUP_ROOT, runs[-1])


def undo_run(run_dir: str):
    manifest_path = os.path.join(run_dir, "changes.json")
    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    db_path = manifest["db"]
    index_path = manifest["index"]
    changes = manifest["changes"]

    con = sqlite3.connect(db_path, timeout=15)
    try:
        with con:
            for change in changes:
                con.execute(
                    "UPDATE threads SET title = ? WHERE id = ?",
                    (change["old_db_title"], change["id"]),
                )
    finally:
        con.close()

    now = utc_stamp()
    with open(index_path, "a", encoding="utf-8") as fh:
        for change in changes:
            old_name = change["old_index_name"]
            if old_name is None:
                old_name = change["old_db_title"]
            fh.write(
                json.dumps(
                    {"id": change["id"], "thread_name": old_name, "updated_at": now},
                    ensure_ascii=False,
                )
                + "\n"
            )
    return len(changes)


def cmd_preview(args):
    plan, unknown, already = build_plan(args.db, args.index)
    print(f"Would label {len(plan)} threads. already-tagged={already} unknown-model={unknown}")
    by_tag = {}
    for change in plan:
        by_tag.setdefault(change["tag"], 0)
        by_tag[change["tag"]] += 1
    print("By tag:", dict(sorted(by_tag.items())))
    limit = args.limit
    for change in plan[:limit]:
        old = change["old_index_name"] or change["old_db_title"]
        print(f"  [{change['tag']}] {old[:80]}")
    if len(plan) > limit:
        print(f"  ... and {len(plan) - limit} more")


def cmd_apply(args):
    plan, unknown, already = build_plan(args.db, args.index)
    if args.log:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(os.path.dirname(args.log), exist_ok=True)
        with open(args.log, "a", encoding="utf-8") as fh:
            if not plan:
                fh.write(
                    f"{stamp} nothing to label (already-tagged={already} "
                    f"unknown-model={unknown})\n"
                )
                return
            run_dir = apply_plan(args.db, args.index, plan)
            fh.write(
                f"{stamp} labeled {len(plan)} threads "
                f"(already-tagged={already} unknown-model={unknown}); "
                f"backup={run_dir}\n"
            )
        return
    if not plan:
        print(f"Nothing to label. already-tagged={already} unknown-model={unknown}")
        return
    run_dir = apply_plan(args.db, args.index, plan)
    print(f"Labeled {len(plan)} threads. already-tagged={already} unknown-model={unknown}")
    print(f"Backup + undo manifest: {run_dir}")
    print("Undo with: python label_threads.py undo")


def cmd_undo(args):
    run_dir = args.run or newest_run()
    if not run_dir or not os.path.isdir(run_dir):
        print("No apply run found to undo.")
        return
    count = undo_run(run_dir)
    print(f"Restored {count} thread titles from {run_dir}")


def cmd_status(args):
    threads = read_threads(args.db)
    index_latest = read_index_latest(args.index)
    tag_counts = {}
    untagged = 0
    for tid, title, model, provider, _first_message in threads:
        name = index_latest.get(tid) or title or ""
        m = PREFIX_RE.match(name)
        if m:
            tag = m.group(0).strip()[1:-1]
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        else:
            untagged += 1
    print("Display-name tag distribution:")
    for tag, count in sorted(tag_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {tag}: {count}")
    print(f"  (untagged): {untagged}")
    print(f"  total threads: {len(threads)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--index", default=DEFAULT_INDEX)
    sub = parser.add_subparsers(dest="cmd")

    p_preview = sub.add_parser("preview", help="show what would change")
    p_preview.add_argument("--limit", type=int, default=20)
    p_preview.set_defaults(func=cmd_preview)

    p_apply = sub.add_parser("apply", help="backup + label")
    p_apply.add_argument(
        "--log",
        default=None,
        help="append a one-line outcome to this log file and print nothing "
        "(for hidden scheduled runs without a console)",
    )
    p_apply.set_defaults(func=cmd_apply)

    p_undo = sub.add_parser("undo", help="undo most recent apply")
    p_undo.add_argument("--run", default=None)
    p_undo.set_defaults(func=cmd_undo)

    p_status = sub.add_parser("status", help="tag distribution")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
