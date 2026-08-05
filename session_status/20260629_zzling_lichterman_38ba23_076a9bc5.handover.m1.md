# Scribe handover - milestone 1 (~134K tokens)
# session: 20260629_zzling_lichterman_38ba23_076a9bc5
# cwd: C:\moma\.claude\worktrees\dazzling-lichterman-38ba23
# written: 2026-06-29 16:36:38 by deepseek-v4-pro

# HANDOVER - d54 Music Cataloging Project

---

## GOAL (Max's own words)
Max wants to catalog, annotate, and map a large collection of music tracks created in Suno. The full pipeline:
1. **Download** the tracks from Suno (~30 tracks).
2. **Catalog** in a database - give each a sequential ID, rename the files, annotate/describe each track.
3. **Star-rate** tracks AND specific pieces/sections within tracks.
4. **Identify and cut out usable pieces** for use in a movie project.
5. Later: **loop-extend** some pieces using crossfade-overlap looping.

This is a new, standalone system - not directly part of the existing movie pipeline (sc10 production).

---

## DECISIONS + WHY

**No hard decisions finalized yet.** Discussion opened with:

| Topic | Claude's Proposal | Reasoning | Status |
|-------|-------------------|-----------|--------|
| **Suno download method** | Playwright (browser automation) in Max's logged-in Suno session | No official API; 3rd-party APIs are brittle, paid, and against ToS. Playwright is reliable and free. | Proposed, awaiting Max's approval |
| **Database location** | Separate, new SQLite or D1 instance - NOT inside the existing MOMA D1 | Music isn't sc10 production; clean separation prevents clutter. | Proposed, awaiting Max's choice |

---

## CURRENT STATE

- **Checked in:** d54 on branch `dazzling-lichterman-38ba23`, cwd `C:\moma\.claude\worktrees\dazzling-lichterman-38ba23`
- **Tokens used:** ~134K so far (out of ~1M window; older context summarized near ~840K)
- **Built so far:** Nothing. Pure planning stage.
- **Blocking item:** Claude is waiting on Max's decision for the two open questions before any code is written.

---

## EXACT NEXT STEP

When Max responds to the fork question (DB location), Claude should:
1. Lock in the DB design.
2. Start building the **download script** (Playwright to scrape Suno - Max logs in manually, script grabs all tracks + metadata: title, lyrics, prompt, duration).
3. Build the **catalog schema** (track table with: sequential ID, renamed filename, original Suno metadata, description, star rating).

---

## OPEN QUESTIONS (awaiting Max)

? **Q1: Database - separate or inside MOMA D1?**
- Option A: Brand-new small SQLite/D1 just for music.
- Option B: Table(s) inside the existing MOMA D1.
- Claude leans Option A (clean separation).

? **Q2: Confirm Suno download approach?**
- Claude proposed Playwright (Max clicks login in a real browser, script then scrapes).
- Awaiting Max's OK or alternative preference.

---

## KEY PATHS / IDS

| Item | Value |
|------|-------|
| **Branch** | `dazzling-lichterman-38ba23` |
| **Worktree** | `C:\moma\.claude\worktrees\dazzling-lichterman-38ba23` |
| **Bcast script** | `C:/claude_base/branch_bulletin/bcast.py` |
| **Suno tracks count** | ~30 |
| **MOMA D1** | Existing pipeline DB (sc10 production) - music should probably NOT go here |

---

## GOTCHAS & DEAD ENDS RULED OUT

- **Suno has NO official API.** Do not waste time searching for one.
- **Unofficial/third-party Suno APIs** are explicitly ruled out by Claude: paid, brittle, against Terms of Service.
- **This is a NEW system, not sc10.** Don't accidentally wire it into the movie production pipeline unless Max overrides the separation proposal.
- **Loop-extension** is a *later* phase - not to be built yet. Just noted for future design awareness.
- **No code has been written yet.** A future session starts from zero on implementation.
