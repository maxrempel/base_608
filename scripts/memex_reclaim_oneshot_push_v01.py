#!/usr/bin/env python3
"""One-shot catch-up push: POST every .md file under the reclaim folder
to Memex as a normal entry (source=clawy-nextcloud-sync so the reclaim
script does not re-reclaim them). Used once on migration day, right
after wiping Memex and before enabling the pusher cron.

After this, the pusher (Stream 4) will NEVER walk the reclaim folder --
that subtree is in its SKIP_SUBTREES. So direct-MCP writes from before
the migration are preserved in Memex via this one-shot, and new direct-
MCP writes after migration are preserved via reclaim's normal forward
operation.

v01 2026-04-13, Opus 4.6.

Run from Pine (or anywhere Nextcloud is mounted). Point RECLAIM_DIR at
the reclaim folder. Dry-run by default -- pass --execute to actually POST.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

MEMEX_URL  = "https://claude-memory.max-rempel2.workers.dev"
AUTH_KEY   = "claymem2026"

DEFAULT_RECLAIM_DIR = r"C:\Users\maxre\Nextcloud\00_clawy_kb\memories\reclaim_sync_from_memex"
STATE_OUT = r"C:\claude_base\memex_backups\oneshot_reclaim_push_state.json"


def memex_write(text, tags, source):
    if len(text) > 8000:
        text = text[:8000] + "\n\n[TRUNCATED]"
    payload = json.dumps({"text": text, "tags": tags, "source": source})
    # Use curl (keeps parity with prod pusher; avoids requests dep)
    import tempfile
    tf = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
    tf.write(payload)
    tf.close()
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{MEMEX_URL}/write",
             "-H", "Content-Type: application/json",
             "-H", f"X-Auth-Key: {AUTH_KEY}",
             "--data-binary", f"@{tf.name}", "--max-time", "30"],
            capture_output=True, text=True, timeout=35
        )
    finally:
        os.unlink(tf.name)
    if result.returncode != 0:
        return {"error": result.stderr}
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": result.stdout}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reclaim-dir", default=DEFAULT_RECLAIM_DIR)
    ap.add_argument("--execute", action="store_true",
                    help="Actually POST. Without this flag: dry-run.")
    args = ap.parse_args()

    files = []
    for root, _, fnames in os.walk(args.reclaim_dir):
        for fn in fnames:
            if fn.endswith(".md"):
                files.append(os.path.join(root, fn))

    print(f"Found {len(files)} .md files under {args.reclaim_dir}")
    if not args.execute:
        print("Dry-run. Re-run with --execute to POST. Sample:")
        for p in files[:3]:
            print("  " + os.path.basename(p))
        return

    state = {"pushed": []}
    ok = err = 0
    for i, path in enumerate(files):
        fname = os.path.basename(path)
        key = "nc_reclaim_sync_from_memex_" + fname
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().strip()
        except Exception as e:
            print(f"READ ERR {fname}: {e}")
            err += 1
            continue
        if len(content) < 10:
            continue

        tags = f"clawy-sync,{key.replace('.md','')}"
        result = memex_write(content, tags, "clawy-nextcloud-sync")
        mem_id = result.get("id")
        if mem_id:
            state["pushed"].append({"file": fname, "memex_id": mem_id})
            ok += 1
            print(f"[{i+1}/{len(files)}] OK {fname} -> {mem_id}")
        else:
            err += 1
            print(f"[{i+1}/{len(files)}] ERR {fname}: {result}")
        time.sleep(0.3)

    os.makedirs(os.path.dirname(STATE_OUT), exist_ok=True)
    with open(STATE_OUT, "w") as f:
        json.dump(state, f, indent=2)

    print(f"\nDone. ok={ok} err={err}. State saved to {STATE_OUT}")


if __name__ == "__main__":
    main()
