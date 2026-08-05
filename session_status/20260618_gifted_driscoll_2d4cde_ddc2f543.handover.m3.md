# Scribe handover - milestone 3 (~262K tokens)
# session: 20260618_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-18 19:35:40 by deepseek-v4-pro

# HANDOVER - D26 Session (gifted-driscoll-2d4cde)

---

## GOAL (Max's words, two tasks)

**Task 1 (filter bug):** "Only the images with 2 ladies, in standard style, not any junk, not blank slides." The storyboard PILE filter was showing 166 items including corridors, windows, single faces, blank tiles. Three other chats (D22/D23/D24) had been fighting it in circles.

**Task 2 (spine UX):** "When a new lipsie is done, have it land right in the 1st spine, pushing the older one to the 2nd spine. It would have either done or approved status. Also I want all lipsies per merge, to have big numbers in order of their making, because it is a pain to open and rate each, and sort them. I would rather remember the last 2. Discarding older ones is not good because sometimes the new ones are worse and I have to give up. Also can you make the 2nd spine expandable, so to stretch lipsies horizontally?"

---

## DECISIONS + WHY

### Filter bug - diagnosis only, no code changed by D26
- **Root cause**: The team was filtering junk by filename regex blocklist in `storyboard_editor.html` (line ~645): patterns like `bg_|extrap|station|window_looking|...`. This is whack-a-mole - every new batch of images leaks past with different filenames.
- **Proof discovered via Playwright live inspection**: `sc05_window_twoshot` is a GOOD 2-ladies shot but contains "window"; `bg_corridor` is junk and also contains a location word. Same keywords, opposite verdicts. Filenames lie.
- **The data already has cleaner fields**: `role` (shot vs plate, 1162/894 split), `mood` (neutral vs broll). But neither field alone isolates the "2 ladies" set - corridor/window stills are also tagged `shot`+`neutral`.
- **Bonus bug found**: sc05/sc07/sc08 clips are leaking into the sc10 pile via the arrangement?scene mapping.
- **Why D26 didn't fix it**: D24 was already driving `storyboard_editor.html`. D26 handed the full root cause to D24 on the board and stayed off the file. The stable fix recommended: curate once (junk the corridors/windows/single-faces permanently so they don't return) or add a real "two-shot" data flag.
- **Why D24's swing happened**: D24 tried a filename whitelist ("real two-shots") ? got exactly 1 image ? reverted it. Then back to blacklist ? 166 with junk. The swing was inevitable given the filename approach.

### Spine UX - Phase 1 (v51): display features
- **Making-order numbers**: Used `job_id` as the signal (autoincrement = higher ID = made later). Within each merg (line_hash group), lipsies sorted by `job_id` ascending get numbered 1, 2, 3... . The newest gets the highest number. This lives on both 1st-spine tiles and 2nd-spine take tiles.
- **Expandable 2nd spine**: A `Set` tracks which mergs are expanded. The `2ND SPINE` label is clickable, toggling between `[+]` (collapsed, thumbs 64px) and `[-]` (expanded, thumbs 146px). CSS class `.expanded` on the dups-area div drives the stretch.
- **Both are pure display**: No persistence, no DB writes, no collision with D24's pile filter work.

### Spine UX - Phase 2 (v52): auto-promote fresh lipsies
- **First attempt discarded**: Designed as a load-time "always newest per line" rule. Dry-run on live data revealed all 31 existing picks were already `spine_pinned=1` (the assign flow pins everything), making the rule inert. Worse, it couldn't respect Max's deliberate reverts ("sometimes the new ones are worse"). Reverted before any push.
- **Rebuilt correctly**: Uses a `SEEN_JOB_IDS` Set captured at storyboard open time. On the 60s refresh interval, any lipsie with a `job_id` NOT in that set is "fresh" and auto-promotes to 1st spine for its merg. Lipsies that already existed when the page opened never trigger promotion - so Max's reverts to older takes are never overridden. Pinned picks still skip promotion.
- **Tested e2e**: 0 reshuffle mismatches on load (no spurious DB writes), baseline of 86 lipsies captured, simulated fresh lipsie lands on exactly its own merg.

### Naming
- Max wanted the noun for "the result of merging several spine lines into one lipsie" - settled on **"merg"**. Added to user dictionary and `moma_system_map_tomemex.md`.

---

## CURRENT STATE

- **master is at b5a4ffa** (pushed to origin). Contains v52 of `storyboard_editor.html` with all 4 spine features.
- **Live server on port 8790** serves from the main checkout (no restart needed - HTML is read fresh from disk each request via `_serve_file`).
- **Filter bug**: D24 is still working on it. D26 handed off root cause and stayed off the file. The pile still shows 166 items with junk - filename filter is the current (fragile) approach.
- **Playwright lock**: Released. No tool locks held.
- **Autonomous timer**: Armed at dynamic pacing (1200-1800s), set to run the `<<autonomous-loop-dynamic>>` sentinel check.
- **Branch bulletin board**: D26 has posted updates at each phase; D24 and D25 were coordinated.

---

## EXACT NEXT STEP

The autonomous loop just fired. The work to do:
1. Check if D24 has pushed anything new to master for the pile filter - if so, verify it doesn't conflict with D26's spine changes (same file: `storyboard_editor.html`).
2. Check for any CI status, review threads, or merge conflicts on master.
3. The one open gap D26 flagged: "a lipsie made while the storyboard is **closed** won't auto-land when you reopen (it's treated as already-there)." Max hasn't responded to whether this matters.
4. If everything is quiet, do a quick CI/board check and stop.

---

## OPEN QUESTIONS (awaiting Max)

- **"Say the word and I'll make that survive reopens too"** - D26 noted that fresh-lipsie auto-promote only works in-session. Lipsies made while the storyboard is closed won't auto-land on next open. Max hasn't responded.
- **The pile filter**: Is D24's eventual retag/curation approach acceptable, or does Max want D26 to take over and junk the bad images now?
- **Are the 4 spine features landing correctly in Max's Firefox?** D26 tested in Playwright's Chromium only.

---

## KEY PATHS / IDs / NAMES

| What | Path/Value |
|---|---|
| Storyboard editor (the modified file) | `sc10/sound_assembly/code/storyboard_editor.html` |
| Slideshow server (read-only for this work) | `sc10/sound_assembly/code/slideshow_server` (port 8790) |
| Main checkout (served by 8790) | `C:\moma` |
| D26 worktree | `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde` |
| Branch | `claude/gifted-driscoll-2d4cde` (merged to master) |
| Master commits | `3815e69` (v51 Phase 1), `b5a4ffa` (v52 Phase 2) |
| User dictionary | `C:\claude_base\user_dictionary_tomemex.md` |
| Project language map | `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde\memos\moma_system_map_tomemex.md` |
| Bulletin board script | `C:\claude_base\branch_bulletin\bcast.py` |
| API endpoint for images | `/api/approved_images` |
| Storyboard URL | `http://localhost:8790/storyboard` |
| D24 (owns pile filter) | Active on `storyboard_editor.html` when D26 joined |
| D25 (owns slideshow_server) | Idle, cleared D26 to edit |

---

## GOTCHAS

1. **`storyboard_editor.html` is a shared file** - D24 (pile filter) and D26 (spine UX) both edit it. D26 coordinated via the board and got explicit clearance before editing, but any future work on this file must check the board and rebase.

2. **No `created_at` field in lipsie data** - `job_id` (autoincrement) is the only making-order signal. This works but means the numbering relies on insertion order in the DB, not wall-clock time.

3. **Filename-based filtering is fundamentally broken** - any new approach that judges images by filename keywords will fail the same way. The data has `role` and `mood` fields but no "two-shot" flag. The only stable fix is either curation (junk bad images permanently in the DB so they never appear) or adding a real data field.

4. **All picks are `spine_pinned=1`** - the assign flow pins everything. This is why the first Phase 2 design (load-time promote) would have been completely inert. The `SEEN_JOB_IDS` approach was necessary to make auto-promote work without fighting pinning.

5. **Server serves HTML fresh from disk** - no restart needed after edits. Just merge to the main checkout and reload the browser. But the main checkout is at `C:\moma`, NOT the worktree.

6. **Playwright opens its own Chromium** - not Max's Firefox. Testing in Playwright verified the JS logic but Max's actual view may differ (browser, cached version, etc.).

7. **Empty-filename images render as blank tiles** - found 4 images with empty filenames (ids 1378-80, 1390) in the pile. These are the "blank slides" Max complained about. They're a data problem, not a filter problem.

8. **sc05/sc07/sc08 clips leak into scene-10 pile** - the arrangement?scene mapping is pulling in clips from other scenes. This is a separate bug from the filename filter.

9. **D26's worktree vs main checkout** - D26 edits in the worktree, then merges to master in the main checkout (`C:\moma`) so the live server picks it up. Don't edit files directly in the main checkout; use the worktree workflow.

10. **The autonomous loop is armed** - `ScheduleWakeup` was called with `<<autonomous-loop-dynamic>>` sentinel. The next tick will check for remaining work. If 3 consecutive ticks find nothing, scale back.
