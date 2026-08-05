#!/usr/bin/env python3
"""Restore Memex from a D1 backup dump. For rollback after a failed
migration. Re-POSTs every row from the dump via the Worker /write
endpoint. NEW ids will differ but content (text, tags, source) is
preserved.

Usage:
  python memex_d1_restore_from_dump_v01.py PATH_TO_DUMP.json [--execute]

Dry-run by default. Lists row counts and samples. Pass --execute to POST.

v01 2026-04-13, Opus 4.6.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

MEMEX_URL = "https://claude-memory.max-rempel2.workers.dev"
AUTH_KEY  = "claymem2026"


def memex_write(text, tags, source):
    if text is None:
        return {"error": "null text"}
    if len(text) > 8000:
        text = text[:8000] + "\n\n[TRUNCATED]"
    payload = json.dumps({"text": text, "tags": tags or "", "source": source or "restore"})
    tf = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
    tf.write(payload)
    tf.close()
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{MEMEX_URL}/write",
             "-H", "Content-Type: application/json",
             "-H", f"X-Auth-Key: {AUTH_KEY}",
             "--data-binary", f"@{tf.name}", "--max-time", "30"],
            capture_output=True, text=True, timeout=35,
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
    ap.add_argument("dump_path")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()

    with open(args.dump_path, "r", encoding="utf-8") as f:
        dump = json.load(f)

    rows = dump["rows"]
    print(f"Dump has {len(rows)} rows")
    print(f"Dumped_at: {dump.get('dumped_at')}")

    if not args.execute:
        print("\nDRY-RUN. Source counts:")
        from collections import Counter
        for src, n in Counter(r.get("source", "?") for r in rows).most_common(10):
            print(f"  {n:5}  {src}")
        print("\nRe-run with --execute to actually POST.")
        return

    ok = err = 0
    out_state = []
    for i, row in enumerate(rows):
        text = row.get("text", "")
        tags = row.get("tags", "")
        source = row.get("source", "restore")
        result = memex_write(text, tags, source)
        new_id = result.get("id")
        if new_id:
            ok += 1
            out_state.append({"old_id": row["id"], "new_id": new_id})
            if (i + 1) % 50 == 0:
                print(f"[{i+1}/{len(rows)}] ok")
        else:
            err += 1
            print(f"[{i+1}/{len(rows)}] ERR: {result}")
        time.sleep(0.2)

    out_path = args.dump_path + ".restore_map.json"
    with open(out_path, "w") as f:
        json.dump(out_state, f, indent=2)
    print(f"\nDone. ok={ok} err={err}. Id remap: {out_path}")


if __name__ == "__main__":
    main()
