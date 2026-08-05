#!/usr/bin/env python3
"""
harvest_compactions.py - the REAL calibration harvester.

Discovery 2026-06-06: Claude Code writes a line per compaction:
  type=system, subtype=compact_boundary, with compactMetadata =
  {trigger, preTokens, postTokens, preCompactDiscoveredTools, durationMs}.
So we do NOT need byte/token estimates - the EXACT pre/post token counts are
recorded natively. This harvester walks every session transcript under
~/.claude/projects, extracts every compact_boundary's metadata, dedups by uuid,
and appends to kb/compaction_events.jsonl. Then prints summary stats: the real
auto-compact threshold (preTokens) and the severity (postTokens/preTokens).

Run anytime: `python harvest_compactions.py`  (idempotent; dedups by uuid)
"""
import json, glob, os, statistics

PROJECTS = os.path.expanduser(r"~\.claude\projects")
KB = r"C:\claude_base\compaction_kb\kb"
EVENTS = os.path.join(KB, "compaction_events.jsonl")


def _existing_uuids():
    s = set()
    try:
        with open(EVENTS, encoding="utf-8") as f:
            for line in f:
                try:
                    s.add(json.loads(line).get("uuid"))
                except Exception:
                    pass
    except Exception:
        pass
    return s


def harvest():
    os.makedirs(KB, exist_ok=True)
    seen = _existing_uuids()
    new = []
    files = glob.glob(os.path.join(PROJECTS, "**", "*.jsonl"), recursive=True)
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                for line in fh:
                    if "compact_boundary" not in line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("subtype") != "compact_boundary":
                        continue
                    u = r.get("uuid")
                    if u in seen:
                        continue
                    seen.add(u)
                    md = r.get("compactMetadata") or {}
                    new.append({
                        "uuid": u,
                        "ts": r.get("timestamp"),
                        "sessionId": r.get("sessionId"),
                        "cwd": r.get("cwd"),
                        "version": r.get("version"),
                        "trigger": md.get("trigger"),
                        "preTokens": md.get("preTokens"),
                        "postTokens": md.get("postTokens"),
                        "durationMs": md.get("durationMs"),
                        "transcript": os.path.basename(f),
                    })
        except Exception:
            continue
    if new:
        with open(EVENTS, "a", encoding="utf-8") as f:
            for ev in new:
                f.write(json.dumps(ev, ensure_ascii=True) + "\n")
    return new


def stats():
    rows = []
    try:
        with open(EVENTS, encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
    except Exception:
        pass
    pre = [r["preTokens"] for r in rows if isinstance(r.get("preTokens"), int)]
    auto = [r for r in rows if r.get("trigger") == "auto"]
    manual = [r for r in rows if r.get("trigger") == "manual"]
    print(f"TOTAL compaction events in KB: {len(rows)} (auto={len(auto)}, manual={len(manual)})")
    if pre:
        print(f"preTokens (threshold): min={min(pre)} max={max(pre)} "
              f"mean={int(statistics.mean(pre))} median={int(statistics.median(pre))} n={len(pre)}")
    ratios = [(r['postTokens']/r['preTokens']) for r in rows
              if isinstance(r.get('preTokens'), int) and isinstance(r.get('postTokens'), int) and r['preTokens']]
    if ratios:
        print(f"post/pre kept-ratio: mean={statistics.mean(ratios):.3f} "
              f"(i.e. ~{statistics.mean(ratios)*100:.1f}% of context survives a compaction)")
    # auto-trigger threshold is the key calibration number
    apre = [r["preTokens"] for r in auto if isinstance(r.get("preTokens"), int)]
    if apre:
        print(f"AUTO-compact preTokens: min={min(apre)} max={max(apre)} mean={int(statistics.mean(apre))} n={len(apre)}")


if __name__ == "__main__":
    new = harvest()
    print(f"harvested {len(new)} new compaction event(s)")
    stats()
