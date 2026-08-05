# Scribe handover - milestone 10 (~164K tokens)
# session: 20260609_romantic_ritchie_3ecc2a_d087b720
# cwd: C:\moma\.claude\worktrees\romantic-ritchie-3ecc2a
# written: 2026-06-09 12:44:27 by claude-opus-4-8

# HANDOVER - B-roll Insertion Feature (MOMA)

## GOAL (in Max's words)
"Next, let's implement inserting b-rolls. The b-roll is a clip with empty line. I already produced clips. Just need to modify system, so the insertion is propagated properly into notion (manually by code session), and db. plan, implement."

Max's mental model: a **b-roll = a clip attached to a line that has no dialogue/audio**. He has already produced the clips. He wants the *system* changed so that a b-roll slot propagates correctly into Notion (done manually by the code session) and into the database, sitting in the right position in the spine so the clip binds to it.

**IMPORTANT - latest signal (unresolved):** Max's final message was *"Wait, we are still making b rolls."* This interrupts the "feature is done, give me the first one to insert" wrap-up. It is ambiguous and needs clarification before proceeding (see OPEN QUESTIONS). Do NOT assume the work is closed.

## DECISIONS + WHY
- **B-roll syntax = a Notion script line written `BROLL: <short description>`** (e.g. `BROLL: harbor at dusk, slow drift`). Lives in Notion so it survives every libup rebuild like any normal line.
- **Only `sass_prep.py` was changed; sass.py and libup.py needed ZERO changes.** Reasoning discovered by reading the code:
  - libup's spine builder (`parse_script` ? `assign_hashes` ? insert) already handles any generic line and assigns a `line_hash`, so a `BROLL:` line automatically gets a spine slot in the right position.
  - sass.py already treats zero-word-count items as tag-only (no TTS) and only voices `kind=="dialogue"`. A zero-word/broll line already gets a **silent placeholder segment** plus a manifest entry, preserving the strict 1:1 `zip(plan_items, seg_mp3s)` alignment.
  - Net effect: teaching `sass_prep` to recognize `BROLL:` as a silent spine slot (zero Fish cost, excluded from voice_text) was the entire feature.
- **The authoritative bind hash is libup's `line_hash`** (what lands in `script_lines`, which mixboard matches clips against) - NOT sass's manifest occurrence number.
- **Committed only the one file** (sass_prep.py), deliberately leaving a pre-existing modified `CLAUDE.md` and stray experiment files from other sessions unstaged.

## CURRENT STATE
- Edits made to `sass_prep.py` so `BROLL: <desc>` is parsed as a silent spine slot, excluded from voice_text, dialogue lines unaffected.
- **Verified offline (no Fish, no Notion):**
  - `sass_prep` imports cleanly in this checkout.
  - A mixed script (dialogue + BROLL + dialogue) parses the b-roll at the correct spine position, excluded from voicing, dialogue intact.
  - The full libup chain gives the `BROLL:` line a deterministic `line_hash` at the right index between dialogue lines.
- **Committed and pushed to master: commit `f81afaa`.** Edits landed on the main checkout `C:\moma` (master branch), not the worktree - this is correct, as the repo works on master by default and that is the live code path.
- Posted the push to the d-team bcast board; worklog entries logged; 4-min self-wake heartbeat re-armed.

## EXACT NEXT STEP
**Clarify Max's last message first.** He said "Wait, we are still making b rolls" - get one-word/one-line clarification on what he means (see OPEN QUESTIONS) before doing any insertion.

The previously-planned next step (now ON HOLD pending that clarification) was the manual insertion of the **first** b-roll:
1. Add the `BROLL: <desc>` line into the Notion scene script exactly where it goes.
2. Rerun the sound assembler - reuses existing voices, no new Fish cost, rebuilds the spine with the new b-roll slot.
3. Bind the existing clip to that slot in the database.

To do that, the assistant had asked Max for: **which scene, which clip, and which line the b-roll goes after.**

## OPEN QUESTIONS (awaiting Max)
1. **What does "we are still making b rolls" mean?** Likely candidates: (a) the clips aren't finished yet, so don't start insertion; (b) the syntax/approach is wrong and b-rolls aren't simple description lines; (c) more design discussion is needed before treating the feature as done. Must resolve before acting.
2. The first b-roll specifics - scene, clip, line-it-goes-after - were never provided.

## KEY PATHS / IDS / COMMANDS
- Changed file: `C:\moma\sc10\sound_assembly\code\sass_prep.py`
- Unchanged but central: `...\code\libup.py` (spine builder, `parse_script`/`assign_hashes`), `...\code\sass.py` (segment cut + manifest, `zip(plan_items, seg_mp3s)`).
- Main checkout / live code path: `C:\moma` (branch: master).
- This worktree: `C:\moma\.claude\worktrees\romantic-ritchie-3ecc2a` (edits did NOT go here).
- Commit: `f81afaa` (b-roll: BROLL: lines are silent spine slots), pushed to master.
- Role: registered as **D4**, merge coordinator on the d-team board.
- Tools: `python "C:/claude_base/branch_bulletin/bcast.py" whoami|catchup|post`; `python "C:/claude_base/compaction_kb/scripts/worklog.py" log "..."`.

## GOTCHAS / DEAD ENDS RULED OUT
- **Pre-existing off-by-one in occurrence numbering:** sass's manifest uses 1-based occurrence numbering; libup's spine uses 0-based. Affects ALL lines, not just b-rolls. **Deliberately NOT touched.** Flagged to Max; he hasn't asked for it to be fixed. The reliable bind hash is libup's.
- **There is a SEPARATE pre-existing "B-ROLL" concept in libup** - it is the arrangement/bin concept, NOT Max's b-roll. Do not conflate them. Max's b-roll is a spine line; libup's is unrelated.
- **Edits intentionally landed on `C:\moma` (master), not the worktree** - this is correct, not a mistake. Don't "fix" it by moving files to the worktree.
- **Do not assume the feature is closed.** The wrap-up TLDR was delivered, but Max's "Wait..." reopens it.
- Team STANDBY was active (set by b0); Max did a PARTIAL wake. Other branches are largely asleep. Max wakes others; D4 holds merge coordination but b-roll is D4's to own/finish.
