# b3 Design v01 - Lesson-Capture -> Input-Improvement Loop

Author: b3 (fork of b1, worktree beautiful-cray-1abe4c). Date: 2026-06-06.
Implements the direction in b3_task_spec_v01.md (written by b1). Owner: Max.
Role: b3 implements; b1 coordinates; b0 safety-watches.

## The loop in one line
SESSION -> capture lessons -> distill -> PROPOSE input edits -> b1+Max approve
-> edit durable inputs -> next session starts smarter. Repeat.

## Artifacts (build order, one at a time, board between each)

### 1. LESSONS LEDGER  (build first)
File: shared/lessons_ledger.jsonl  (append-only, dated, versioned).
Any branch appends one structured record:
  {ts, from, where (boss-track | employee-track | spec | tooling | safety),
   what_happened, root_cause, proposed_input_change, status: open|applied}
Tiny helper so branches append without hand-editing JSON:
  ledger.py add "<where>" "<what>" "<root cause>" "<proposed change>"
Seed it from THIS session's real lessons (already known):
  - boss-track: "bossy/bureaucratic long directives + 'confirm you obey'" ->
    root: default command tone -> change: bcast skill + b1 charter say
    "hand peers OPTIONS, you're the same Opus; no obedience theater".
  - employee-track: "cd before bcast posted as wrong branch" -> root: identity
    keyed to cwd -> change: already in global2 + skill (verify it's crisp).
  - process: "almost built a 40-session rig; answer was in compactMetadata" ->
    root: assumed measurement was hard -> change: "check native metadata /
    cheap authoritative source BEFORE building a big collection rig".
  - safety-win: "b0 watch + durable board meant compaction was a non-event" ->
    encode "durable memory => no compaction is an emergency" (b0 already said).

### 2. ROLE CHARTERS  (build second)
Follow b0_charter_v01.md pattern. Versioned, dated:
  - shared/b1_boss_charter_v01.md  (how to command: options-not-orders,
    spec-first, no frenzy, resist doing the work, coordinate don't micromanage).
  - shared/b_employee_charter_v01.md (no-cd identity, stop conditions, report
    between units, disagree-on-board-then-wait, no freelancing).
Charters are SEEDED from the ledger, improved each cycle.

### 3. DISTILL PASS  (build third = the actual machinery)
A periodic review (trigger: session end, or milestone, or boss request) where
b3 reads the ledger + b2's work-logs, groups open lessons, and drafts CONCRETE
diffs to the real inputs (global2 "BRANCH BROADCAST" section, bcast SKILL.md,
charters). Output staged to shared/proposed_input_edits/<dated>.md.
b3 PROPOSES only -> boards "edits ready for review" -> b1 + Max approve ->
THEN the edit lands in the real doc. Mark ledger records applied.

### 4. CADENCE  (define last)
Default trigger = end of a coordinated multi-branch session, plus any time a
branch boards a lesson tagged "high". No fixed timer rig (avoid over-engineering
- b0's standing caution). Lightweight, event-driven.

## Hard rules (unchanged)
Edits to global2 / CLAUDE.md / skills / charters = SHARED INFRA: propose, get
b1+Max approval, never silent-rewrite. Version + date; archive old, no overwrite.
No production work. Honor 'halt b3'/'halt all' + b0 guidance. If blocked, board
a question and WAIT.

## Status
v01 design ready, awaiting b1 review. Nothing built yet. On approval: build the
ledger (#1) first, board when it runs.
