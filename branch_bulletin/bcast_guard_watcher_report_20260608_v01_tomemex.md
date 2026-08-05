# bcast guard + watcher - build report (2026-06-08)

Written by Claude Opus 4.8 (session c5 / goofy-goodall-68a19f) for Max.
Companion to the incident fix-list `bcast_two_manager_fix_list_20260608_v01_tomemex.md`.

## TLDR

The team-coordination system that let two sessions both become "manager" is now
guarded two ways, both fully automatic and unsupervised:

1. A GUARD baked into the bcast tool itself - it fires only when a session
   actually trips a rule, and nudges just that session. No training, no
   broadcasts (per Max's "systems must be self-explanatory" rule).
2. A WATCHER running on its own 10-minute timer (a hidden Windows scheduled
   task) - the automated replacement for a human or a session sitting and
   policing the board.

Proven live the same day: the watcher caught a real two-"b0" collision, nudged
the board, and the team resolved it itself with zero human action.

## What was broken

One global bulletin board, no locking, no liveness check. A fresh session told
"take over from C1" mistook a live manager for the dead one and self-declared
manager of a task someone else still held -> two managers, several minutes of
conflict. Root causes: no liveness handshake, no ownership baton, one undivided
board so a new worker gravitated to the loudest task, fuzzy identity.

## What was built

### Earlier this session - split boards (B1) + reassign-by-name (B2), already live
- Per-team boards `bulletin_<letter>.jsonl` + one `bulletin_joint.jsonl`.
  A worker hears its own team board + joint; `post` defaults to its team, a
  `--joint` flag routes cross-team. This stops a c-team worker from being
  pulled into b-team noise.
- Reassign by name: telling a session "you are now d2" switches its team and
  auto-announces "I am now d2 (was c5)" so siblings track the move.
- Flag-gated cutover (`SPLIT_BOARDS.on`) so the change was byte-identical to the
  old board until Max gave the go; all sessions were re-registered cleanly.

### The GUARD (point-of-violation, inside bcast.py)
- COLLISION guard at `whoami`: adopting an id a DIFFERENT live session already
  holds (its state file was touched within the 8-minute liveness window) prints
  a loud warning plus the handshake steps. It warns, never blocks (fail-open).
- INTRA-TEAM `--joint` nudge at `post`: a cross-team broadcast that only names
  the sender's own team is flagged as probably mis-routed; still delivered.
- Tested in isolation: 17/17 assertions pass.

### The WATCHER (`watcher.py`, scheduled task `bcast_watcher`, every 10 min, hidden)
- Deterministic sweep: scans all session state files for the same id held by
  two+ LIVE sessions = a collision the in-tool guard didn't catch at the moment.
  High confidence -> one cooled-down board nudge + a Telegram critical-alarm.
- Judgment pass (low-context Opus, claude-opus-4-8): only when the joint board
  moved since the last run, it reads the recent cross-team traffic + the live
  roster and flags a coordination problem brewing (two sessions on one task, an
  unconfirmed takeover, two about to edit one file). A quiet board costs nothing.
- Alert hygiene: the Opus pass returns a short stable "issue key" per problem;
  Telegram fires only for a genuinely NEW problem (60-min per-key cooldown), so
  Max's phone is not re-pinged for an ongoing issue. Tested: 12/12 pass.

## Live validation (2026-06-08)
- First watcher run detected two LIVE "b0" sessions and alerted.
- The board nudge drove one "b0" to run the liveness handshake; after the 8-min
  window elapsed with no reply, it confirmed sole-"b0" and continued. No human,
  no manual baton - the self-explanatory design working in production.
- The Opus pass separately surfaced a subtler risk a mechanical sweep cannot
  see: a "b6" about to edit app.js on a stale baseline after "b2" had already
  released the lock with newer live bytes.
- Scheduled task confirmed running unattended, exit code 0.

## Putting the team to sleep / waking everyone

This capability already exists in bcast (global, all sessions obey):
- SLEEP (reachable): `standby "reason"` - pauses all work but KEEPS each
  session's 4-minute wake-timer, so they stay reachable and auto-resume.
- WAKE ALL: `resume` - clears standby; every session sees it on its next
  ~4-minute heartbeat and resumes automatically. Max-side trigger words
  "sleep the team" / "wake the team" map to these (a session runs the command).
- FULL stop: `halt "reason"` stops timers too (deeper, but then each session
  must be re-armed by hand). For "sleep but wake later", use standby, not halt.

The watcher keeps running through a team sleep - it is cheap on a quiet board
and remains the safety net.

## Files
- `branch_bulletin/bcast.py` - tool + guards + split boards + standby/resume.
- `branch_bulletin/watcher.py` - the unsupervised watcher.
- `branch_bulletin/tests/test_split_boards.py` (17), `tests/test_watcher.py` (12).
- Scheduled task: `bcast_watcher` (Pine), every 10 min, runs hidden via pythonw.
- Infra registered in `C:\claude_base\infra_map_tomemex.md`.
