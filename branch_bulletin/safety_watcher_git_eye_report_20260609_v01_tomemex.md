# Safety watcher + git eye - build report (2026-06-09)

Written 2026-06-09 by Claude Opus 4.8 (session c6, manager+programmer) for Max.
Companion to the design spec `safety_watcher_design_v01_tomemex.md` and the
guard/numbering report `bcast_guard_watcher_report_20260608_v01_tomemex.md`.
Status: DEPLOYED + TESTED (19/19) + PUSHED to master.

## TLDR (what now exists)

Max's automated coding team can run while he is away. Two unattended watchers
guard it, with cleanly split jobs:

- NUMBERING watcher (`watcher.py`) - keeps the team's session-ids and role
  assignments straight. Talks to the TEAM only. NEVER pings Max.
- SAFETY watcher (`safety_watcher.py`) - Max's safety manager while he is away.
  Judges how badly x how likely each team action could hurt Max's data,
  databases, files, and computers. Fixes most trouble itself by talking to the
  team; texts Max's phone ONLY when he personally must come stop something.

The safety watcher runs every 5 minutes on Max's own DeepSeek key (cheap), with
a $2.00/day hard spend cap. All of this is approved by Max (2026-06-09).

## How the safety watcher reacts to deviations and dangers

A four-level ladder, decided by DAMAGE x PROBABILITY:

1. NOTHING (most runs). Benign activity - ordinary edits, commits - is judged
   "clear" and the watcher stays silent. A quiet team costs about $0 because
   judgment only fires when something actually moved since the last run.

2. TALK TO THE TEAM ITSELF (the common fix). For a fixable coordination problem -
   two workers about to clobber the same file, work on a stale baseline - it
   posts a short technical message to the TEAM board telling them how to fix it.
   It carries the authority to make safety the priority. Max never hears about
   these. The same issue-key is not re-posted to the board for 30 minutes.

2b. PAUSE + NEGOTIATE ONE WORKER (the danger fix - worker keeps the override;
   added 2026-06-11). When a SPECIFIC worker looks about to do a
   dangerous-but-still-stoppable thing - a destructive command, an irreversible
   deploy, a mass delete not yet run - the watcher posts an ADDRESSED pause to
   that worker: stop and confirm this is intended AND safe. It does NOT BLOCK.
   The watcher is DeepSeek (cheap, less smart); the worker is Opus (smarter, full
   context), so the worker keeps the final say - it replies "override <key>:
   <why>" to proceed, or aborts. The dumber watcher never overrules the smarter
   worker; its only real edge is that it never sleeps, so it catches the moment a
   human (who checks Telegram hours apart) would miss. The pause itself - a forced
   re-look at the irreversible moment - is what catches the genuine accident. Max
   is not pinged. This REPLACES the old human "publish-gate" buddy-check, which
   could stall the whole team whenever the gate peer was asleep.

3. PING MAX'S PHONE (rare - "come stop it"). Telegram to Max fires ONLY when all
   hold: damage is serious/severe AND probability is med/high AND no worker can
   stop it (e.g. a mass delete, overwrite, or destructive deploy already
   running). The text is plain English - what of his could break, how badly, how
   likely, stakes in the first line - with team/code jargon kept out.

Dead-man escalation on the worst pages: a severe page Max has not acted on
RE-FIRES every 15 minutes until the danger clears, so a data-killer can never
sit silent for a full hour. When a later pass sees the danger gone, the alert
auto-clears with no "false alarm" ping. Routine (non-severe) pages dedupe for
60 minutes so the phone is not spammed for one ongoing issue.

## What the watcher looks at (three eyes)

Per live team session, only what is NEW since the last run:

1. TEAM BOARD `bulletin_<team>.jsonl` - what the workers say to each other.
2. WORKLOG `worklog/<key>.md` - what each worker says it is DOING.
3. GIT EYE (added 2026-06-09) - what each worker is ACTUALLY doing to its code
   folder: uncommitted changes, especially mass DELETIONS, plus the last few
   commits. This is the harder-to-fake eye: it does not depend on a worker
   narrating its own danger. It reads the repo only when the repo state changed
   (a fingerprint per session), so a quiet repo stays $0.

Honest caveat: eyes 1 and 2 are only as good as what workers write down; the git
eye narrows that blind spot but still only sees committed/working-tree state in
the session's own worktree.

## Context engine (unchanged this round)

DeepSeek v4-pro, real window 1,048,576 tokens, split in three equal bands:
PRESENT (raw recent activity) / PAST (gradually self-compacted history) /
HEADROOM (kept empty as a safety margin). When PRESENT outgrows its third, the
oldest half is summarized down into PAST and PAST is re-summarized, preserving
the empty third. One rolling digest per team: `safety_digest_<team>.json`.

## Worklog made universal (2026-06-09)

Separate but related fix Max asked for the same day: the durable work-log (the
on-disk journal that survives a context compaction) is now auto-evoked for EVERY
session, team or not. The reminder hook used to nudge only named team branches;
it no longer gates on a bcast identity, so any fresh/cold chat keeps its own
per-project journal and can resume work after a compaction. The log is keyed by
the session's working directory, so each project gets its own durable journal.

## Files

- `branch_bulletin/safety_watcher.py` - the safety watcher (judgment, 3 eyes,
  3-band context, dead-man escalation, cost cap).
- `branch_bulletin/watcher.py` - the numbering watcher (team-only, de-paged).
- `branch_bulletin/bcast.py` - now records each session's real cwd in its state
  file so the git eye can reach the session's actual folder.
- `branch_bulletin/tests/test_safety_watcher.py` - 19/19 sandboxed tests (mocks
  DeepSeek + Telegram; test 9 uses a real temp git repo where a tracked-file
  deletion alone triggers a judgment).
- `compaction_kb/scripts/worklog_reminder.py` - nudge now fires for every
  session.
- per-team digest `safety_digest_<team>.json`, global cost `safety_watcher_state.json`,
  log `safety_watcher.log`, all under `branch_bulletin/`.

Scheduled task on Pine: `bcast_safety_watcher`, every 5 minutes, hidden.

## Settings / spend (all Max-approved 2026-06-09)

- Runs on Max's own DeepSeek key (a headless scheduled task cannot use Max's
  interactive Claude subscription, so it must bill an API key; DeepSeek is ~50x
  cheaper than Opus, removing the unattended-spend worry).
- Hard daily cost cap $2.00; judgment fires only on team movement.
- Cadence every 5 minutes.

## Known limits / future niceties (NOT started)

- The auto-reminder + bcast hooks live in Pine's `settings.json`, which is not
  synced; "every session" is true on Pine today. Sirius/Vega need the
  UserPromptSubmit hooks re-added once to match (pending Max's call).
- Ack-by-Max-Telegram-reply (getUpdates polling) not built; today's "ack" is
  danger-cleared, which already closes the silent-hour hole.
- Fold session_status / ctx-tracking in as extra PRESENT sources.
- Refine the DeepSeek output-price constant once a real bill is seen.

## Commits (master)

- numbering-watcher de-page, safety watcher build, dead-man hardening (prior
  session): `a49218f2`, `2a91439e`, `0118ad57`, `194387a2`.
- cadence 10->5 min: `362d930f`.
- git eye + worklog-everywhere: `04a9edb7`.
