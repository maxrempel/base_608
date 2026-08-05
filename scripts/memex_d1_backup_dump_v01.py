#!/usr/bin/env python3
"""Dump all rows from the Memex D1 memories table to a timestamped JSON
file. Used as rollback insurance before wiping Memex on migration day.

Creates: C:\\claude_base\\memex_backups\\memex_full_dump_YYYYMMDD_HHMM.json

v01 2026-04-13, Opus 4.6 on Pine.
"""
import json
import os
import urllib.request
from datetime import datetime

CF_ACCOUNT = "e4dc2224d6baa721873dca77dc6f057d"
D1_ID      = "ced548a2-e647-4547-9ae3-7606b08b6e16"
TOKEN      = "Hp0RcvNVzktIZj64vVgW7gWyseZ3wguEXfdM2cwR"
OUT_DIR    = r"C:\claude_base\memex_backups"

URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{D1_ID}/query"


def d1_query(sql):
    body = json.dumps({"sql": sql}).encode()
    req = urllib.request.Request(
        URL, data=body, method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    if not data.get("success"):
        raise RuntimeError(f"D1 query failed: {data}")
    return data["result"][0].get("results", [])


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = os.path.join(OUT_DIR, f"memex_full_dump_{ts}.json")

    # Schema discovery first
    schema = d1_query("SELECT sql FROM sqlite_master WHERE type='table' AND name='memories'")
    rows = d1_query("SELECT * FROM memories")

    payload = {
        "dumped_at": datetime.now().isoformat(),
        "row_count": len(rows),
        "schema": schema,
        "rows": rows,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Dumped {len(rows)} rows to {out_path}")
    print(f"Size: {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    main()
