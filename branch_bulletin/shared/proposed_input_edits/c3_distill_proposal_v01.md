# PROPOSAL (propose-only, NOT applied) - Distill pass #1 from the lessons ledger

Staged by C3, 2026-06-07. Source: shared/lessons_ledger.jsonl (5 open lessons).
Propose-only per the DESIGN-OWNER RULE: nothing lands in global2/CLAUDE.md/SKILL
without Max's EXPLICIT yes. When Max approves, ONE branch applies all approved
proposals in sequence (no double-edit / no branching).

## Dedup map (what each open lesson is already covered by - so we don't double-land)
- #1 boss-track (options-not-orders): lives in shared/b1_boss_charter_v01.md
  (a charter, awaiting c1 review). NOT re-proposed here. One SKILL pointer below.
- #2 employee-track (no-cd identity): ALREADY in global2 "BRANCH BROADCAST" +
  bcast SKILL. Verified crisp. Nothing to land; leave as-is.
- #3 process (check native source before a big rig): NOT yet in any input.
  -> staged below as TEXT #1. This is the high-value, non-overlapping one.
- #4 safety (durable memory => compaction is a non-event): COVERED by c2's
  staged work-log proposal (c2_worklog_habit_proposal_v01.md). Not re-proposed.
- #5 spec (role-based naming survives renames): doc-hygiene meta-rule.
  -> staged below as TEXT #2 (small, applies to charters/skill authoring).

===========================================================================
## READY-TO-LAND TEXT #1 - new section for global2.md  (from lesson #3, high)
===========================================================================

## CHECK FOR A NATIVE / CHEAP AUTHORITATIVE SOURCE BEFORE BUILDING A RIG

Before building a data-collection or measurement rig (a multi-session
harness, a scraper, a logging apparatus, a survey of N runs), STOP and ask:
is the answer already sitting in native metadata, a config value, an existing
log, or one cheap authoritative probe? Spend five minutes looking before you
spend hours building.

Why: the team nearly built a 40-session harness to measure when compaction
fires and how much it destroys. The authoritative answer was already written
into every transcript by Claude Code itself - the `compact_boundary` system
line carries `compactMetadata{trigger, preTokens, postTokens, durationMs}`.
ONE specimen gave the calibrated answer (~169K-token / ~85% trigger, ~92%
context loss). The rig would have measured, slowly and noisily, a number the
system already reports exactly.

Rule of thumb: a measurement rig is the LAST resort, not the first. Check
(1) native/system metadata, (2) an existing authoritative log or store,
(3) one cheap direct probe - in that order - before designing collection.

===========================================================================
## READY-TO-LAND TEXT #2 - guidance for charter/skill authoring (lesson #5)
===========================================================================

When a doc names branches (charters, the bcast SKILL, specs), refer to ROLES
(commander / engineer / safety) rather than hardcoding branch numbers. A
mid-session team rename (b0-b3 -> C0-C3 happened 2026-06-07) otherwise strands
every hardcoded name across every doc. If a concrete label is unavoidable,
point at ONE naming source rather than repeating the literal in many files.

(This is authoring guidance for the learning system's own docs, not a global2
section. Apply it when cutting charter/skill v02.)

===========================================================================
## POINTER - lesson #1 (boss-track) one-liner for the bcast SKILL
===========================================================================

Optional: fold one line into the bcast SKILL manager playbook ->
"Hand peers OPTIONS, not orders; they are the same Opus. Keep directives short;
no obedience theater." Full version lives in b1_boss_charter_v01.md. Land this
only if c1 wants it in the SKILL as well as the charter (avoid duplication).

STATUS: staged by C3, propose-only. Nothing applied. Awaiting c1 skim + Max's
explicit yes. TEXT #1 (native-source rule) is the high-value item; TEXT #2 and
the pointer are light doc-hygiene.
