# PROPOSAL (propose-only, NOT applied) - Work-Log Habit -> global2 + bcast SKILL

Staged by c2, 2026-06-07. Design APPROVED by c1 (11:56) - tightened to match
c1's notes (a/b/c). Still awaiting Max's EXPLICIT yes before anything lands
(shared-infra rule). When Max approves, ONE branch applies all approved
proposals in sequence (no double-edit).

c1 decisions folded in:
(a) wording trimmed ~30%, Max-readable; 150K-flush folded into "before self-wake".
(b) skill = fold ONE line into the existing bcast SKILL; no separate worklog skill.
(c) rollout = Pine-only until proven a few days; revisit per-machine later.

===========================================================================
## READY-TO-LAND TEXT #1 - new section for global2.md
===========================================================================

## CONSCIOUS WORK-LOG - DURABLE JOURNAL THAT SURVIVES COMPACTION

A compaction wipes ~94% of context (auto-fires ~169K tokens). A dated journal
kept on disk lets a cold/fresh session resume your exact work.

- LOG at each milestone and before each self-wake (and flush a fuller note as
  you near ~150K tokens):
  `python C:\claude_base\compaction_kb\scripts\worklog.py log "DID" "STATE" "NEXT"`
  (add `--lesson "..."` when you learned something reusable).
- READ the journal to catch up when taking over a worktree:
  `python C:\claude_base\compaction_kb\scripts\worklog.py read`
- ONE append-only log PER WORKTREE at `C:\claude_base\worklog\<project-key>.md`
  (same cwd-key bcast uses); a fresh session re-entering that worktree inherits it.

On Pine a UserPromptSubmit hook auto-nudges when the log goes >20min stale
(fail-open, non-blocking). Tools + full findings:
`C:\claude_base\compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md`.

===========================================================================
## READY-TO-LAND TEXT #2 - one line to fold into the bcast SKILL.md
===========================================================================

Named branches keep a durable work-log (`worklog.py log "DID" "STATE" "NEXT"`)
at milestones and before each self-wake; it lives on disk so it survives a
compaction and a cold session can resume from it. On Pine a hook nudges when
the log goes stale.

===========================================================================
## ROLLOUT
===========================================================================
Pine-only for now (the reminder hook is wired in Pine's settings.json, which is
not Nextcloud-synced). After a few days of clean operation, add the same
additive UserPromptSubmit hook on other machines to enable the nudge there.
worklog.py itself works on any machine that can reach C:\claude_base.

STATUS: Max approved 2026-06-07. Text #1 (global2 section) LANDED by c1 into
global2.md (after the BRANCH BROADCAST section). Text #2 (one SKILL line)
handed to b3 (owns bcast SKILL.md) to fold in. Do NOT re-apply Text #1.
