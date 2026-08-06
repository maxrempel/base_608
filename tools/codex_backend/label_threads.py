#!/usr/bin/env python3
"""Codex thread model-labeler.

Prefixes every saved Codex thread title with a short model tag so Max can see
which backend ran each session, e.g. "[Q3.8] Fix login bug".

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


def make_prefixed(name: str | None, tag: str) -> str | None:
    if name is None:
        return None
    if PREFIX_RE.match(name):
        return None
    return f"[{tag}] {name}"


def read_threads(db_path: str):
    con = sqlite3.connect(db_path, timeout=15)
    try:
        cur = con.execute("SELECT id, title, model, model_provider FROM threads")
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
    for tid, title, model, provider in threads:
        tag = tag_for(model, provider)
        if not tag:
            skipped_unknown += 1
            continue
        index_name = index_latest.get(tid)
        new_db_title = make_prefixed(title, tag)
        new_index_name = make_prefixed(index_name, tag) if index_name else None
        if new_db_title is None and new_index_name is None:
            skipped_already += 1
            continue
        plan.append(
            {
                "id": tid,
                "tag": tag,
                "old_db_title": title,
                "new_db_title": new_db_title if new_db_title else title,
                "in_index": tid in index_latest,
                "old_index_name": index_name,
                "new_index_name": new_index_name,
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
    for tid, title, model, provider in threads:
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
