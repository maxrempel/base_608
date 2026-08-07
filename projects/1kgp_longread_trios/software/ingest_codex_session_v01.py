#!/usr/bin/env python3
"""ingest_codex_session_v01.py - condense a Codex rollout JSONL into a digest.

Usage:
    python ingest_codex_session_v01.py <rollout.jsonl> <digest.md> [--max-chars 4000]

The digest keeps every user prompt and every compaction summary in full,
truncates long assistant texts, and collects URLs and local file paths so a
successor session can rebuild context without re-reading megabytes of logs.
"""

import argparse
import json
import re
import sys
from collections import Counter


def text_of_content(content):
    parts = []
    if isinstance(content, list):
        for c in content:
            if not isinstance(c, dict):
                continue
            kind = c.get("type")
            if kind in ("input_text", "output_text", "text"):
                parts.append(c.get("text", ""))
            elif kind == "function_call":
                name = c.get("name", "?")
                args = c.get("arguments", "")
                if isinstance(args, str) and args:
                    parts.append(f"[call] {name}({args[:120]}{'...' if len(args) > 120 else ''})")
                else:
                    parts.append(f"[call] {name}")
            elif kind == "function_call_output":
                out = c.get("output", "") or c.get("text", "")
                if isinstance(out, str):
                    parts.append(f"[tool output] {out[:200]}{'...' if len(out) > 200 else ''}")
            elif kind == "reasoning":
                parts.append("[reasoning: summarized]")
    elif isinstance(content, str):
        parts.append(content)
    return "\n".join(parts)


URL_RE = re.compile(r"https?://[^\s\"'<>()]+")
PATH_RE = re.compile(r"(?:[A-Za-z]:\\[^\s\"'<>|]+|/mnt/[^\s\"'<>|]+|/[A-Za-z0-9_.\-/]+\.(?:md|py|tsv|json|txt|html|sh|xml|bat|ps1))")


def truncate(s, max_chars):
    if max_chars and len(s) > max_chars:
        return s[:max_chars] + f"\n... [truncated {len(s) - max_chars} chars]"
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rollout")
    ap.add_argument("digest")
    ap.add_argument("--max-chars", type=int, default=4000)
    args = ap.parse_args()

    turns = {}          # turn_id -> {"user": [...], "assistant": [...], "tools": Counter}
    order = []
    compactions = []
    event_users = []

    with open(args.rollout, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            typ = o.get("type")
            payload = o.get("payload", {})

            if typ == "compacted":
                compactions.append(payload.get("message", ""))
                continue

            if typ == "event_msg" and payload.get("type") == "user_message":
                event_users.append(payload.get("message", ""))
                continue

            if typ != "response_item":
                continue
            if payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in ("user", "assistant"):
                continue
            turn_id = payload.get("turn_id", "")
            if turn_id not in turns:
                turns[turn_id] = {"user": [], "assistant": [], "tools": Counter()}
                order.append(turn_id)
            text = text_of_content(payload.get("content", ""))
            if not text.strip():
                continue
            if role == "user":
                turns[turn_id]["user"].append(text)
            else:
                turns[turn_id]["assistant"].append(text)
                for m in re.finditer(r"\[call\] (\S+)", text):
                    turns[turn_id]["tools"][m.group(1)] += 1

    out = []
    out.append("# Q38 session digest")
    out.append("")
    out.append(f"Source: {args.rollout}")
    out.append(f"User turns: {len(order)}; event user messages: {len(event_users)}; compaction summaries: {len(compactions)}")
    out.append("")

    if event_users:
        out.append("## User messages (event log, full)")
        out.append("")
        for i, u in enumerate(event_users, 1):
            out.append(f"### Message {i}")
            out.append("")
            out.append(u)
            out.append("")
    out.append("")

    if compactions:
        out.append("## Compaction summaries (full)")
        out.append("")
        for i, c in enumerate(compactions, 1):
            out.append(f"### Compaction {i}")
            out.append("")
            out.append(c)
            out.append("")

    out.append("## Turn timeline")
    out.append("")
    for i, tid in enumerate(order, 1):
        t = turns[tid]
        out.append(f"### Turn {i} ({tid[:8]})")
        out.append("")
        for u in t["user"]:
            out.append("**User:**")
            out.append("")
            out.append(truncate(u, args.max_chars))
            out.append("")
        for a in t["assistant"]:
            out.append("**Assistant:**")
            out.append("")
            out.append(truncate(a, args.max_chars))
            out.append("")
        if t["tools"]:
            out.append("**Tools:** " + ", ".join(f"{k} x{v}" for k, v in t["tools"].most_common()))
            out.append("")

    # Deduplicated URL and path index
    all_text = "\n".join(event_users + compactions + [a for t in turns.values() for a in t["assistant"]])
    urls = sorted(set(URL_RE.findall(all_text)))
    paths = sorted(set(PATH_RE.findall(all_text)))
    out.append("## URL index")
    out.append("")
    for u in urls:
        out.append(f"- {u}")
    out.append("")
    out.append("## Local path index")
    out.append("")
    for p in paths:
        out.append(f"- {p}")
    out.append("")

    with open(args.digest, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Wrote digest: {args.digest} ({len(out)} lines)")


if __name__ == "__main__":
    sys.exit(main())
