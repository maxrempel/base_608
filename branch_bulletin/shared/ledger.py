#!/usr/bin/env python3
"""
ledger.py - team lessons ledger (b3 / continuous-improvement system).

Append-only, dated record of lessons learned in real sessions, each with a
PROPOSED change to the durable "inputs" (global2.md / CLAUDE.md / bcast skill /
charters). b3 later distills these into proposed edits; b1 + Max approve before
anything lands in a real instruction doc. Pure capture here - no auto-editing.

Branch identity is auto-detected the SAME way bcast does (keyed by the chat's
working directory), so a lesson is tagged with the branch that logged it. Run by
full path, never cd first (same rule as bcast).

Commands:
  python ledger.py add <where> "<what>" "<root_cause>" "<proposed_change>" [--prio high]
       where = boss-track | employee-track | spec | tooling | safety | process
  python ledger.py list [--open]      print lessons (──open = only status=open)
  python ledger.py applied <n>        mark record #n (1-based) status=applied

Fails open: a broken ledger must never wedge a session.
"""
import sys, os, json, time, hashlib, re

BASE = r"C:\claude_base\branch_bulletin"
LEDGER = os.path.join(BASE, "shared", "lessons_ledger.jsonl")
STATE_DIR = os.path.join(BASE, "state")
WHERES = {"boss-track", "employee-track", "spec", "tooling", "safety", "process"}


def _safe_key(cwd):
    norm = os.path.normcase(os.path.abspath(cwd))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return f"{tail}_{h}"


def _whoami(cwd):
    try:
        with open(os.path.join(STATE_DIR, _safe_key(cwd) + ".json"), "r", encoding="utf-8") as f:
            return json.load(f).get("id") or "?"
    except Exception:
        return "?"


def _read():
    try:
        with open(LEDGER, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f.read().splitlines() if l.strip()]
    except Exception:
        return []


def cmd_add(cwd, args):
    if len(args) < 4:
        print('usage: ledger.py add <where> "<what>" "<root_cause>" "<proposed_change>" [--prio high]')
        return 1
    where, what, root, change = args[0], args[1], args[2], args[3]
    prio = "high" if "--prio" in args and "high" in args else "normal"
    if where not in WHERES:
        print(f"warn: unknown where '{where}' (expected one of {sorted(WHERES)}) - logging anyway")
    rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "from": _whoami(cwd),
           "where": where, "what_happened": what, "root_cause": root,
           "proposed_input_change": change, "status": "open", "prio": prio}
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")
    print(f"LESSON logged ({rec['from']}, {where}, {prio}): {what}")
    return 0


def cmd_list(args):
    recs = _read()
    only_open = "--open" in args
    n = 0
    for i, r in enumerate(recs, 1):
        if only_open and r.get("status") != "open":
            continue
        n += 1
        print(f"#{i} [{r.get('ts')}] {r.get('from')} | {r.get('where')} | {r.get('prio')} | {r.get('status')}")
        print(f"    what : {r.get('what_happened')}")
        print(f"    root : {r.get('root_cause')}")
        print(f"    fix  : {r.get('proposed_input_change')}")
    if n == 0:
        print("(no matching lessons)")
    return 0


def cmd_applied(args):
    if not args:
        print("usage: ledger.py applied <n>")
        return 1
    try:
        idx = int(args[0])
    except ValueError:
        print("n must be a number")
        return 1
    recs = _read()
    if idx < 1 or idx > len(recs):
        print(f"no record #{idx} (have {len(recs)})")
        return 1
    recs[idx - 1]["status"] = "applied"
    with open(LEDGER, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")
    print(f"#{idx} marked applied.")
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cwd = os.getcwd()
    cmd = args[0]
    if cmd == "add":
        return cmd_add(cwd, args[1:])
    if cmd == "list":
        return cmd_list(args[1:])
    if cmd == "applied":
        return cmd_applied(args[1:])
    print(__doc__)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"ledger.py error (ignored): {e}\n")
        sys.exit(0)
