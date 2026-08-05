#!/usr/bin/env python3
"""
worklog.py - Component 6: the universal CONSCIOUS work-log.

Why: a compaction destroys ~94% of a session's context (measured - see
compaction_kb/HANDOVER_AND_STATUS_v01). A dated journal that lives OUTSIDE
context (a plain file on disk) is the mitigation: it survives compaction, and
parallel/future sessions can read it to resume the exact work.

Design (b1-approved 2026-06-06):
  - ONE append-only markdown log PER PROJECT, keyed by the SAME cwd-hash scheme
    bcast uses (so the board and the work-log share project keys and siblings
    can cross-find). Path: C:\\claude_base\\worklog\\<project-key>.md
  - Every branch + session appends to the same project log; each entry is
    dated and tagged with branch-id + short session-id.
  - "Conscious": the SESSION decides what is worth recording (DID/STATE/NEXT,
    optional LESSON) - this is NOT an auto-dump of tool calls.
  - Cadence: log at each milestone AND before each self-wake.

Usage:
  python worklog.py log "DID..." "STATE..." "NEXT..." [--lesson "..."]
  python worklog.py log "DID..." "STATE..." "NEXT..." --cwd "C:\\path"
  python worklog.py read [--n 12]          print the recent tail for catch-up
  python worklog.py read --cwd "C:\\path"  read a specific project's log
  python worklog.py path                    print this project's log path

Fails open everywhere: a broken work-log must never wedge a session.
"""
import sys, os, json, glob, time, hashlib, re, subprocess

WORKLOG_DIR = r"C:\claude_base\worklog"
STATE_DIR = r"C:\claude_base\branch_bulletin\state"
PROJECTS = os.path.expanduser(r"~\.claude\projects")


def _resolve_root(cwd):
    """Normalize cwd to the git worktree/repo TOP-LEVEL so a session that cd's
    into a SUBFOLDER mid-work (e.g. into the repo root to run git) still keys to
    ONE stable log instead of a new file per folder. Falls back to cwd when not
    inside a git repo. For a session sitting at its own worktree root (the normal
    case) the top-level == cwd, so existing logs keep their key; the fix only
    changes behaviour for cd'd-into-subfolder calls. (E10 report 2026-06-18: one
    session's worklog split across 3 files because cd-ing changed the cwd key -
    the same cwd-keying flaw the bcast 'no cd' rule warns about.)"""
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5)
        top = (out.stdout or "").strip()
        if out.returncode == 0 and top:
            return os.path.normpath(top)
    except Exception:
        pass
    return cwd


def _project_key(cwd):
    """SAME scheme as bcast._safe_key so board + work-log share keys. cwd is first
    resolved to the git top-level so a subfolder cd does not split the key."""
    norm = os.path.normcase(os.path.abspath(_resolve_root(cwd)))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return f"{tail}_{h}"


def _log_path(cwd):
    return os.path.join(WORKLOG_DIR, _project_key(cwd) + ".md")


def _branch_id(cwd):
    """Read the bcast identity for this cwd, so entries are tagged b1/b2/..."""
    try:
        p = os.path.join(STATE_DIR, _project_key(cwd) + ".json")
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("id") or "?"
    except Exception:
        return "?"


def _project_name_for_cwd(cwd):
    norm = os.path.abspath(cwd)
    return "".join("-" if ch in ":\\/._" else ch for ch in norm)


def _session_id(cwd):
    """Short id from the newest transcript .jsonl for this cwd. Fails open."""
    try:
        pdir = os.path.join(PROJECTS, _project_name_for_cwd(cwd))
        cands = glob.glob(os.path.join(pdir, "*.jsonl"))
        if not cands:
            return "????????"
        newest = max(cands, key=os.path.getmtime)
        return os.path.splitext(os.path.basename(newest))[0][:8]
    except Exception:
        return "????????"


def cmd_log(cwd, did, state, nxt, lesson=None):
    os.makedirs(WORKLOG_DIR, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M")
    branch = _branch_id(cwd)
    sess = _session_id(cwd)
    block = [f"\n## [{ts}] {branch} {sess}",
             f"- DID: {did}",
             f"- STATE: {state}",
             f"- NEXT: {nxt}"]
    if lesson:
        block.append(f"- LESSON: {lesson}")
    path = _log_path(cwd)
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")
    print(f"worklog: appended entry ({branch} {sess}) -> {path}")
    return 0


def cmd_read(cwd, n=12):
    path = _log_path(cwd)
    if not os.path.isfile(path):
        print(f"worklog: no log yet for this project ({path})")
        return 0
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # split into entry blocks (each starts with '## [')
    parts = re.split(r"(?=^## \[)", text, flags=re.MULTILINE)
    parts = [p for p in parts if p.strip()]
    tail = parts[-n:] if n and len(parts) > n else parts
    print(f"=== WORK-LOG (last {len(tail)} of {len(parts)} entries) {path} ===")
    print("".join(tail).rstrip())
    return 0


def main():
    args = sys.argv[1:]
    cwd = os.getcwd()
    if "--cwd" in args:
        i = args.index("--cwd")
        cwd = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 0
    cmd = args[0]
    if cmd == "path":
        print(_log_path(cwd))
        return 0
    if cmd == "read":
        n = 12
        if "--n" in args:
            try:
                n = int(args[args.index("--n") + 1])
            except Exception:
                n = 12
        return cmd_read(cwd, n)
    if cmd == "log":
        lesson = None
        if "--lesson" in args:
            i = args.index("--lesson")
            lesson = args[i + 1]
            del args[i:i + 2]
        pos = args[1:]
        if len(pos) < 3:
            print('usage: worklog.py log "DID" "STATE" "NEXT" [--lesson "..."]')
            return 1
        return cmd_log(cwd, pos[0], pos[1], pos[2], lesson)
    print(__doc__)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"worklog.py error (ignored): {e}\n")
        sys.exit(0)
