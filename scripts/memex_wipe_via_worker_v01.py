#!/usr/bin/env python3
"""Wipe Memex by DELETE /delete/:id for every id in the D1 dump.
Uses the Worker endpoint so D1 and Vectorize stay consistent.

Dry-run by default. --execute to actually delete.

v01 2026-04-13.
"""
import argparse
import json
import subprocess
import sys
import time

MEMEX_URL = "https://claude-memory.max-rempel2.workers.dev"
AUTH_KEY  = "claymem2026"


def delete_one(mid):
    r = subprocess.run(
        ["curl", "-s", "-X", "DELETE", f"{MEMEX_URL}/delete/{mid}",
         "-H", f"X-Auth-Key: {AUTH_KEY}", "--max-time", "15"],
        capture_output=True, text=True, timeout=20,
    )
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"error": r.stdout or r.stderr}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump_path")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()

    with open(args.dump_path, "r", encoding="utf-8") as f:
        dump = json.load(f)
    ids = [r["id"] for r in dump["rows"]]
    print(f"Will delete {len(ids)} entries")

    if not args.execute:
        print("DRY-RUN. Re-run with --execute to actually delete.")
        return

    ok = err = 0
    for i, mid in enumerate(ids):
        res = delete_one(mid)
        if res.get("success") or res.get("ok") or res.get("deleted"):
            ok += 1
        else:
            err += 1
            if err < 5:
                print(f"[{i+1}] ERR {mid}: {res}")
        if (i + 1) % 100 == 0:
            print(f"[{i+1}/{len(ids)}] ok={ok} err={err}")
        time.sleep(0.05)

    print(f"\nDone. ok={ok} err={err}")


if __name__ == "__main__":
    main()
