# Scribe handover - milestone 2 (~166K tokens)
# session: 20260629_focused_lederberg_db400a_e6c11da4
# cwd: C:\moma\.claude\worktrees\focused-lederberg-db400a
# written: 2026-06-29 17:02:37 by deepseek-v4-pro

# HANDOVER: Notion Script Housekeeping - Duplicate Scenes Audit

## GOAL (Max's words)
Investigate the whole Notion movie script for duplications and housekeeping issues, triggered by another chat noticing two versions of Scene 10.

## DECISIONS + WHY
- **Read-only audit only - nothing changed.** Max's instruction was to investigate, and Claude explicitly held off on fixes pending approval. The reasoning: the duplicate Scene 10 situation touches the hard rule against forking/desync, so any cleanup must be deliberate.
- **Cross-referenced the sound production config (`scenes.json`) against live Notion.** This was the right move - it surfaced a second, unrelated stale pointer (scene 55) that a Notion-only search would have missed.
- **Compared the two Scene 10 pages by substance, not just title.** Dialogue is identical; the difference is merge markup. This matters because a superficial "they look the same" conclusion would miss the real hazard (lost merge registrations).

## CURRENT STATE - What is done
- Swept all scenes referenced in the production config (`scenes.json`): 9, 10, 11, 15, 20, 30, 50, 55, 60, 65, 75, 77, 80.
- Fetched the master index page ("Current Versions Kazarian movie") and confirmed it lists both Scene 10 pages as current.
- Fetched and compared both Scene 10 pages.
- Fetched and checked the scene 55 page pointer.
- **Two issues confirmed. Rest of the script is clean.**

## FINDINGS

### Issue 1 - Duplicate Scene 10
| Property | Canonical (in config) | Dead fork |
|---|---|---|
| Notion page ID | `3300316f-...` | `3890316f-...` |
| Title / date code | 10 scene Anna meets Ishtab (**20260502**) | 10 scene Anna meets Ishtab (**20260503**) |
| Last edited | 2026-06-25 | 2026-06-24 |
| Merge work | Has `[[MERGE]]` blocks + 5 registered merges | Clean copy, zero merge markup |
| In master index? | Yes | Yes (both listed as current) |

**The hazard:** the dead fork has a later date code (503 > 502). Any future session scanning for "newest" would pick the fork, edit it, and lose all merge registrations - a direct violation of the no-fork rule.

### Issue 2 - Scene 55 stale production pointer
`scenes.json` maps scene 55 to page `3140316f...fbed2`, which is actually titled **"OLD 55 Werner Garak Masterpiece"** and lives in the Archive folder. The real current scene 55 is `3480316f...cff2`. The sound pipeline would pull archived/old text.

### Clean
Scenes 9, 11, 15, 20, 30, 50, 60, 65, 75, 77, 80 - no duplicates, pointers match the index. (65 and 77 are missing from `scenes.json` but that's expected - not yet in production.)

## EXACT NEXT STEP
**Awaiting Max's "go"** to execute two reversible fixes:

1. **Scene 10 dedup:** Rename the dead fork (`3890316f...`) to something like "OBSOLETE BACKUP - 10 scene Anna meets Ishtab (20260503)", move it into the Archive folder, and remove it from the "Current Versions" master index. *Do not delete* - just quarantine.
2. **Scene 55 pointer fix:** Update `scenes.json` to point scene 55 at the real current page (`3480316f...cff2`) instead of the archived old page (`3140316f...fbed2`).

## OPEN QUESTIONS
- None raised yet. Max hasn't responded to the proposed fixes.

## KEY PATHS AND IDs

### Files in the repo
- **`C:\moma\.claude\worktrees\focused-lederberg-db400a\sc10\sound_assembly\code\config\scenes.json`** - canonical scene?Notion page mapping for the sound pipeline. This is the source of truth the production code reads.

### Notion page IDs
| Role | Page ID (short) |
|---|---|
| Scene 10 CANONICAL (with merge work) | `3300316f-3929-80dd-9e8d-e0f2c80b5ac9` |
| Scene 10 DEAD FORK (clean, no merges) | `3890316f-3929-80a9-a6b9-d2f6c1f0022d` |
| Scene 55 CURRENT (not in config) | `3480316f-3929-8060-a307-cff2...` |
| Scene 55 OLD/ARCHIVED (currently in config) | `3140316f-3929-807a-826e-fbed2...` |
| Master index page | "Current Versions Kazarian movie" (URL: `https://www.notion.so/c50b316f...`) |

### Scene date codes (from page titles)
- Scene 10 canonical: **20260502**
- Scene 10 dead fork: **20260503** ? newer-looking, trap for future sessions

## GOTCHAS
- **The dead fork has a higher date code than the canonical.** This is the trap. Any heuristic that picks "latest by date stamp in title" or "most recently created" will select the wrong page. The merge-work-bearing page must win regardless of date codes.
- **The master index itself is the source of the ambiguity** - it lists both as current. Fixing that is as important as quarantining the page.
- **Do not delete the dead fork, only quarantine it.** Someone may have linked to it, or it may serve as a reference for what the clean pre-merge text looked like. Archive + rename + de-index is sufficient.
- **`scenes.json` is a manual config file**, not auto-generated. The stale scene-55 pointer means someone moved/archived that page in Notion without updating the config. There may be a process gap to address later.
- **Scenes 65 and 77 are deliberately absent from `scenes.json`** - not yet in sound production. Don't "fix" these.
