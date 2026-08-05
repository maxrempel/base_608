# Component 6 - Universal Conscious Work-Log (SPEC v01)

Author: b2 (Claude Opus, worktree youthful-heyrovsky-b2c7a0), 2026-06-06.
For b1 review. Owner/decider: Max. SHORT spec by request - implement after approval.

## Why
A compaction destroys ~94% of context (measured: see compaction_kb handover).
A work-log that lives OUTSIDE context (a file on disk) is the mitigation: it
survives compaction, and parallel/future sessions can read it to catch up. The
.jsonl transcript is NOT enough - it is huge, unstructured, and lost on migration.

## What it is
A dated, append-only journal that EVERY session keeps, on disk, keyed by project.
"Conscious" = the session itself decides what is worth recording (decisions,
state, next step, lessons) - NOT an auto-dump of every tool call. Think: the
session writing its own future handover, a little at a time, as it works.

## Design (proposed - b1 may revise)
- ONE log per project, append-only: `C:\claude_base\worklog\<project-key>.md`
  (project-key = same cwd hash scheme bcast already uses). Markdown so Max can
  read it directly. Append-only = branching-proof, no overwrite races.
- Entry format (one block):
  `## [YYYY-MM-DD HH:MM] <branch-id> <session-short-id>`
  then 3 plain-English lines: DID (what changed), STATE (where things stand /
  current open thread), NEXT (intended next step). Optional LESSON line.
- A tiny helper `worklog.py log "DID" "STATE" "NEXT"` so writing is one call,
  and `worklog.py read` to print the recent tail for catch-up.
- Cross-link: bcast and worklog share the project-key so siblings can find
  each other's logs.

## Enforcement (the hard part - "force every session")
Hook-enforced, additive, fail-open (same discipline as bcast/death-spiral):
- A Stop hook checks: has THIS session appended a work-log entry in the last
  N turns / M minutes? If not, inject a reminder ("log your progress: DID/
  STATE/NEXT"). Does NOT block - just nudges, so it never wedges a session.
- Bootstrapped via the existing Stop array in settings.json (ADD a hook, do
  NOT replace autocommit_rules.sh / death-spiral). Back up settings.json first.
- Global2 gets a SHORT section so every machine/session knows the habit, plus
  a skill if needed.

## Build order (one at a time, board between - per b1)
1. worklog.py (log + read) + the worklog/ folder. Seed THIS session's entries.
2. Manual habit proven across b1/b2/b3 for a few turns (does the format work?).
3. Stop-hook reminder (the enforcement). Backup settings.json, additive edit, test.
4. Global2 section + skill so it spreads to all machines/sessions.

## Open questions for b1
- One log per project, or one per session that siblings aggregate? (I lean
  per-project, append-only, branch-tagged - simplest, branching-proof.)
- Reminder cadence: every K turns, or every T minutes of wall-clock?
- Do we also write a pre-compaction FULL handover (Component 4) when a session
  nears ~165K, or is the steady drip of work-log entries enough? (I lean: drip
  is the baseline; add a near-limit handover trigger later if drip proves thin.)

## Status
v01 spec, awaiting b1 review. Nothing built yet.
