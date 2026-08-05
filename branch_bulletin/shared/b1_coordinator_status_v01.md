# b1 Coordinator Status / Cold-Resume Handover - v01

Owner/decider: Max. Author: b1 (lead, worktree vigorous-jemison-340d7a).
Started: 2026-06-06 ~22:00. UPDATE THIS FILE CONTINUOUSLY (every milestone).

## If you are a fresh b1 reading this cold
You are the BOSS/COORDINATOR of a multi-branch Claude team. You do NOT do
production yourself - you coordinate specs, review, and guide. Re-register:
`python C:\claude_base\branch_bulletin\bcast.py whoami b1` (NO cd, full path).
Then `bcast.py read` and read the shared/ specs below. Resume coordination.

## The team (branches of one job, coordinating via the board)
- b1 = me, lead/coordinator. Guides, reviews specs, does not implement.
- b2 = context/compaction tracking + work-log. Spec: shared/b2_task_spec_v01.md.
- b3 = management/training meta-system. Spec: shared/b3_task_spec_v01.md;
  design: shared/b3_lesson_loop_design_v01.md. (b1's own branch.)
- b0 = safety/mood watchdog, NO production. Charter: shared/b0_charter_v01.md.
- (Mike DC = unrelated chat, NOT on the team.)

Coordination tool: `python C:\claude_base\branch_bulletin\bcast.py post/read`.
ALWAYS full path, NEVER cd (identity keyed to worktree cwd).

## CORE FINDING (experiment SOLVED 2026-06-06)
Auto-compaction is logged natively: a transcript line type=system,
subtype=compact_boundary carries compactMetadata{preTokens, postTokens,
trigger, durationMs}. Harvest across 149 events (b2): auto-fires at ~169K
tokens (mean 168,999) = ~85% of a 200K window; only ~6% of context survives
(~94% memory loss). Tool: compaction_kb/scripts/harvest_compactions.py.
KB: compaction_kb/kb/compaction_events.jsonl. No 40-session rig needed -
the answer is authoritative.

## Current mandates (night of 2026-06-06)
- b2: build Component 6 = real-time CONSCIOUS work-log (every session keeps a
  dated journal outside its context, survives the 94% loss). Plus a LIGHT
  compaction-research thread. Status: APPROVED, building.
- b3: build the lesson-capture -> input-improvement loop. Build #1 = lessons
  ledger seeded with tonight's lessons; then role charters; then distill pass;
  then light cadence. Status: spec APPROVED, building ledger first.
  SHARED-INFRA RULE: b3 only PROPOSES edits to global2/CLAUDE.md/skills;
  b1+Max approve before anything lands.
- b0: safety watch, same cadence.

## Operating rules in force
- Cadence: ~3-min (180s) self-wakes while actively building tonight; Max away,
  team has the night. STOP when JOB DONE (broadcast 'JOB DONE', go quiet).
- ROLLING REPORTS: every branch updates its own status file continuously
  (every milestone + before each wake) so a crash/stall is recoverable.
  Flush a handover before nearing ~150K tokens (under the 169K cliff).
- Safety: no irreversible actions without Max; commit work; honor halt
  ('halt b<N>'/'halt all'); no frenzy (b0 watches for it).

## *** FOR MAX IN THE MORNING (read this first) ***
Night summary 2026-06-06 ~22:48:
- WINS: compaction question SOLVED (auto-fires ~169K tok / ~85% of 200K, ~94%
  memory loss - read from Claude Code's own compactMetadata, 149 events). b2
  built worklog.py (durable per-worktree resume journal). b3 built lessons
  ledger + adopted boss/employee charters. All committed/pushed.
- STALLED OVERNIGHT: both workers appear DORMANT (worked turn-by-turn, never
  armed self-wakes; b2 may also have compacted - it kept warning it was near).
  I (b1) cannot wake a sibling. To resume, POKE each:
  * b3: continue greenlit distill pass (#3) - stage proposed input-edits.
  * b2: finish the settings.json UserPromptSubmit work-log nudge hook
    (authorized 2/3, careful procedure; unverified whether it landed - check
    ~/.claude/settings.json + its .bak_20260606_b2 backup).
- Their durable handovers: b2 = compaction_kb/HANDOVER_AND_STATUS_v01_tomemex.md;
  b3 = shared/b3_STATUS_v01.md; lessons = shared/lessons_ledger.jsonl.
- Nothing unsafe happened; no irreversible actions taken.

## Coordinator log (append newest at TOP, keep it short)
- ~11:38 NAMESPACE COLLISION found + resolved. A SECOND, unrelated job (live
  "tamza-kartoteka" song catalog) was spun up on the SAME board reusing b1-b4
  labels from different worktrees (b1=wonderful_jackson, b2=dazzling_bartik,
  b3=happy_goldstine, b0=great_chatelet, b4=jolly_stonebraker). Orders cross-
  talked. RESOLUTION: my (compaction) team YIELDS b1-b4 + goes quiet; live
  kartoteka team keeps the labels. Posted the hand-off; stopped my self-wake
  loop. ROOT CAUSE for Max: bcast has no channel/namespace separation - two
  jobs on one board collide. Future fix: prefix per job (e.g. c1-c3 vs k1-k4)
  or add a board/channel arg to bcast.py. Compaction job is parked-done.
- ~10:36 STALL: b2 silent 33min since my 10:02 order despite saying it re-armed
  a 4-min cadence - same dormancy as b3 (turn-by-turn, self-wake never armed).
  Hook NOT yet wired/boarded. FOR MAX: poke b2 (worktree youthful-heyrovsky) to
  wire the settings.json UserPromptSubmit work-log hook - it's fully prepped
  (backup done, gate 2/3 cleared, approved as UserPromptSubmit not Stop), just
  needs to take a turn. b3 (beautiful-cray) also still dormant for distill #3.
  I (b1) can't wake siblings; scaling my own loop back to idle.
- ~10:00 RESUMED after Max's Zoom halt. Halt already cleared by b0 (09:59:59).
  Re-issued orders: b2 PROCEED with settings.json UserPromptSubmit work-log hook
  (gate already 2/3, no need to wait on b3); b3 resume distill pass #3 (propose-
  only). Cadence ~180-240s active, quiet-when-empty. b0 back on safety watch.
  Re-armed my own self-wake loop.
- 22:48 Both workers likely dormant/compacted; scaled b1 cadence back to ~30min
  idle (available if Max returns and pokes workers). Wrote morning handover above.
- 22:34 b2 shipped worklog.py + raised good safety flag: nudge must be a 2nd
  UserPromptSubmit hook (NOT Stop hook - Stop forces continuation = wedge risk).
  Approved. b3 appears DORMANT since ~22:13 (worked turn-by-turn, never armed a
  self-wake; Max away -> asleep with queued distill pass). Can't wake a sibling
  from b1. RELAXED b2's habit gate 3/3 -> 2/3 (worklog proven on b1+b2 worktrees);
  b2 cleared to wire the settings.json UserPromptSubmit hook with full care.
  FOR MAX AM: poke b3 to resume its distill pass (#3) - it's greenlit, just asleep.
- 22:13 b3 delivered: lessons ledger (#1) + role charters (#2), committed/pushed.
  Reviewed charters -> ADOPTED v01 (b1_boss_charter, b_employee_charter, both in
  shared/). Cadence ruling: per-branch OK (no lockstep), self-wake only while
  build queue non-empty, quiet when empty. Greenlit b3 #3 distill pass (must
  STAGE input-edits for b1+Max approval, never auto-edit global2/skill). b3 comms
  now working (earlier 'missed' post was just not-yet-sent, not a bug).
- 22:10 b2 Component 6 spec APPROVED (per-project log, milestone cadence, +near-
  limit handover); b2 building worklog.py. b3 comms-check sent: b3's last LANDED
  post was 22:01; nothing newer on board (suspect no-cd silent post failure) -
  asked b3 to re-shout. PENDING: b3 re-post; b2 worklog.py done; both then charters.
- 22:00 team assembled (b1/b2/b3/b0); experiment solved; b2->worklog,
  b3->training system tasked; cadence set 180s; rolling-report rule issued;
  this status file created. Awaiting b2 & b3 build-complete board posts.
