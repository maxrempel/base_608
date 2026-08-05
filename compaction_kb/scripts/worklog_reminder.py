#!/usr/bin/env python3
"""
worklog_reminder.py - Component 6 enforcement: a GENTLE, NON-WEDGING nudge to
keep the conscious work-log fresh.

Design note (2026-06-06, after checking Claude Code hook semantics):
  A Stop hook can only surface a reminder to the MODEL by returning
  decision="block", which FORCES the session to keep running - that is exactly
  the wedge/death-spiral risk Max warns about. The SAFE injection point is
  UserPromptSubmit: its stdout is added to the model's context WITHOUT forcing
  continuation. bcast.py already uses this exact channel successfully. So this
  reminder is meant to be wired as a SECOND UserPromptSubmit hook (additive),
  not a Stop hook.

Behavior: on each user prompt, check this project's work-log
(C:\\claude_base\\worklog\\<project-key>.md). If it is MISSING or STALE (not
touched in STALE_MIN minutes), print a one-line reminder. Otherwise print
nothing (no nag when the log is fresh). EVERY session is nudged - team or not
(Max, 2026-06-09: the work-log must be auto-evoked and persistent for every
session, so any cold/fresh chat can resume the work). The log is keyed by cwd,
so each project keeps its own durable journal regardless of a bcast identity.

Fails open everywhere: a broken reminder must never wedge a session.
"""
import sys, os, json, time, hashlib, re

WORKLOG_DIR = r"C:\claude_base\worklog"
STATE_DIR = r"C:\claude_base\branch_bulletin\state"
STALE_MIN = 20  # remind if the work-log hasn't been touched in this many minutes


def _project_key(cwd):
    norm = os.path.normcase(os.path.abspath(cwd))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return f"{tail}_{h}"


def main():
    cwd = os.getcwd()
    # UserPromptSubmit passes cwd on stdin JSON
    try:
        data = json.load(sys.stdin)
        cwd = data.get("cwd") or cwd
    except Exception:
        pass

    path = os.path.join(WORKLOG_DIR, _project_key(cwd) + ".md")
    stale = True
    if os.path.isfile(path):
        age_min = (time.time() - os.path.getmtime(path)) / 60.0
        stale = age_min >= STALE_MIN

    if stale:
        print(
            "=== gentle work-log nudge ===\n"
            "Haven't jotted in the work-log for a bit. Just a friendly note to self: a "
            "quick line now lets a future session pick up right where you left off. No "
            "rush, no worry -- log whenever it feels natural:\n"
            "  python C:/claude_base/compaction_kb/scripts/worklog.py log "
            '"DID" "STATE" "NEXT"\n'
            "=== end nudge ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"worklog_reminder error (ignored): {e}\n")
        sys.exit(0)
