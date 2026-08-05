# Scribe handover - milestone 10 (~752K tokens)
# session: 20260618_priceless_bhabha_01109a_feeabb00
# cwd: C:\moma\.claude\worktrees\priceless-bhabha-01109a
# written: 2026-06-18 17:09:37 by deepseek-v4-pro

# D23 Handover - sc10 Storyboard Polish & Merged-Lipsie System Integration

## GOAL (Max's words)
1. Make the new merged multi-line lipsies populate the sc10 storyboard/spine so the assembly video plays them.
2. Polish the storyboard UI: whole-scene view, grouped rows for merged lipsies, ratings as small white circles, job IDs on 2ND SPINE takes, remove "Whole Scene" toggle (make it default).
3. Fix the mixboard player so merged lipsies don't replay N times (once per pinned line).
4. Ensure approved + done (not junk) takes show in the 2ND SPINE.
5. MAX said explicitly: "the lines!!! each prompt must must must include the lines" - this is a D21 legacy that applies to all future lipsie fires.

## DECISIONS + WHY

1. **Pin merged lipsie to ALL its lines** - the renderer and player both index by line, so a merged 4-line lipsie must appear on lines 0, 1, 2, 3. The renderer already had a dedup patch (v09), but the player didn't.

2. **Collapse consecutive same-lipsie rows in storyboard** - one row per merged lipsie with speaker lines stacked (e.g. ANNA / ISHTAB / ANNA / ISHTAB shown vertically). This replaces 33 per-line rows with 11 merged rows.

3. **Kill the "Whole Scene" toggle, make it default** - Max hated the button flipping back to single-arrangement view. Now `WHOLE_SCENE = true` hard-coded, button removed, storyboard always shows all rows.

4. **Mixboard player fix** - merged lipsies advance on the **video `ended` event**, not the legacy per-line audio path. That path (`onMediaEnd`) was still using `myIdx + 1`, so a lipsie pinned across 4 lines replayed 4 times. Fixed all 6 advance paths (video end, b-roll timeout, audio, Next, Prev) to use `_nextDistinctIdx()`.

5. **No-cache headers** - added `Cache-Control: no-cache, no-store, must-revalidate` to the slideshow server's file-serving helper so page edits always surface immediately.

6. **Ratings as small white circles** - switched from gold stars (`?`) to white `?` circles, moved off the LIP badge (spine tile: bottom-left; 2ND SPINE: top-left).

7. **Retagging NOT done** - the d-team owns the `merge_hash` canonicalization system. Old takes (2761-2812) carry per-fire hashes that don't match the new `merge_hash`. D23 flagged this to the d-team board but did not execute the backfill. Also, Max junked almost all alternative takes - there are genuinely few surviving non-pick takes to show in the 2ND SPINE.

8. **2ND SPINE filter** - shows takes where `status !== 'junk'` AND `line_hash === spine_pick.line_hash`. This means `done` AND `approved` both show (not just approved). The empty 2ND SPINE is a data problem (no alternative takes surviving), not a code bug.

## CURRENT STATE

### Done & Pushed to Master:
- **Storyboard (v49):** merged-lipsie grouping, white-circle ratings, job IDs on 2ND SPINE takes, whole-scene permanent default (toggle removed), top-left alignment, darker/thicker dividers between rows. Commit `a89435e`.
- **Mixboard player (v48):** all advance paths step by distinct clip; no-cache headers active. Commit `fb377ff`.
- **Renderer (v09):** collapses same-lipsie lines into one segment. Commit `df9d5f2`.
- **Slideshow server:** serves `lip_rating` + `fit_rating` in `approved_images` endpoint; no-cache headers on HTML/JS.
- **Old sc10 spine backed up** to `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json`.
- **11 merged lipsies pinned** to all 33 lines (direct `line_current_clip` write, not via the assign API, to preserve synthetic hashes).
- **Assembly video** rendered: `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4` (2:24, draft quality).

### Still Open / Handed Off:
- **Scene-switch propagation to all tabs** - handed to a fresh/sibling D23 (posted to d-team bcast board with full technical brief).
- **merge_hash backfill** for old takes - owned by d-team.
- **Next-round production polish:** distinct still per beat, arr11 turn-to-room, arr07 warmer Anna delivery. NOT yet done.

### URGENT (from D22's WAKE CALL):
D22 reports the sc10 storyboard **image pile still shows WRONG images** (sc09, misc arr10-15) because the scene-only pile filter isn't live. D22 tagged 78 genuine-sc10 images into arr6 but can't hide the unrelated ones without the filter. The fix:
- Build `SCENE_ARR_IDS` from `/api/arrangements` where `scene_rank === SCENE`.
- In `getBinImages`, allow images only if `arr` is in `SCENE_ARR_IDS` (when no specific arrangement is selected).
- Declare `SCENE_ARR_IDS` near `let SCENE` and fetch it in `bootSb` before `loadStoryboard`.
- Note: ~10 ambiguous images (ship/station/earth-orbit) in arr6 could be sc10 or sc09 - backup at `sc10/combo_runner/code/_d2x_scratch_archive/sc10_pile_tags_backup_20260618_164336.json`.

### Note about a SECOND D23:
The git log shows another session also tagged D23 committed to `storyboard_editor.html` (v50 "fix Whole Scene persistence" and v49 "slot stars/live refresh"). There may be overlapping edits. D23 posted a heads-up to the d-team board.

## EXACT NEXT STEP

**IMMEDIATE:** Land D22's URGENT pile-filter fix in `storyboard_editor.html`. The exact steps:
1. `git pull --rebase --autostash origin master` to absorb any sibling edits cleanly.
2. Read `/api/arrangements` in `bootSb` to build `SCENE_ARR_IDS` = a Set of `arr_id` for arrangements where `scene_rank === SCENE`.
3. In `getBinImages`, the `arrOk` check: if a specific `CURRENT_ARR_ID` is set, `arr === CURRENT_ARR_ID`; otherwise `SCENE_ARR_IDS.has(arr)` (or all pass if Set is empty).
4. Announce file + line numbers before editing - there's a second D23 on this file, so coordination matters.
5. Commit + push, then verify the pile is clean in a fresh browser load.

**THEN:** Check the bcast board for the sibling D23's status on the scene-switch propagation task. If they haven't started, that task is still open.

## OPEN QUESTIONS

1. **Should D23 do the merge_hash backfill** for old takes (2761-2812), or leave it to the d-team?
2. **Does Max want the canonical-hash migration** so all takes of a combination group for star-comparison?
3. **Next-round production polish** - when to start: distinct still per beat, arr11 turn-to-room, arr07 warmer Anna delivery.
4. **The ~10 ambiguous arr6 images** (ship/station/earth-orbit) - are they sc10 or sc09? The backup file has them tagged; need Max's verdict before removing.

## KEY PATHS / IDs

- **Storyboard:** `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (v49, whole-scene default)
- **Mixboard player:** `C:\moma\sc10\sound_assembly\code\mixboard.html` (v48)
- **Renderer:** `C:\moma\sc10\sound_assembly\code\render_mixboard_video_v01.py` (v09)
- **Slideshow server:** `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (no-cache headers, `lip_rating` in endpoint)
- **MOMA DB (D1Client):** `C:\moma\sc10\combo_runner\code\moma_db.py`
- **Spine backup:** `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json`
- **Pile tags backup:** `C:\moma\sc10\combo_runner\code\_d2x_scratch_archive\sc10_pile_tags_backup_20260618_164336.json`
- **Assembly video:** `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4`
- **Scratch scripts:** `C:\moma\sc10\combo_runner\code\_d2x_scratch_archive\` (_d21_*.py, _d23_*.py)
- **Approved lipsie map (11 final jobs):** 2774 (0-3), 2775 (4-5), 2810 (6-7), 2812 (8), 2811 (9), 2805 (10-16), 2806 (17-22), 2807 (23), 2808 (24-27), 2794 (28-29), 2795 (30-32)
- **Servers:** combo_gui on 8779, slideshow_server on 8790
- **Memory files:** `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md`, `feedback_distinct_still_per_lipsie.md`, `MEMORY.md`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py`

## GOTCHAS

1. **Two D23 sessions exist** - check `git log -- sc10/sound_assembly/code/storyboard_editor.html` before editing, and coordinate via bcast board.
2. **The assign API (`/api/storyboard/assign`) overwrites `jobs.line_hash`** - never use it for merged lipsies (it would corrupt their synthetic audio hash). Write `line_current_clip` directly.
3. **Lipsies advance on video `ended`, not audio** - any player advance fix must target `onMediaEnd`, not the audio path.
4. **The "Whole Scene" toggle was removed** - storyboard now hard-defaults to whole-scene. Don't re-add it.
5. **Merge_hash system** - new takes fired via `fire_merge_lipsie.py` share a `merge_hash` and group automatically; old per-fire hashes don't match.
6. **No-cache is on the server** - page changes surface immediately, but verify with `python -c "import urllib.request; ..."` if unsure.
7. **Max's hard rule:** every lipsie prompt MUST include the actual spoken lines, labeled Left/Right. "Describe both characters + positions first, then the quoted lines." And "distinct still per lipsie" - no reusing one still across multiple arrangements.
8. **Scratch scripts are archived** - `_d21_*.py`, `_d23_*.py` moved to `_d2x_scratch_archive/`; don't look for them in the main code directory.
9. **The bcast board is the tamza-songs team** (different repo) - MOMA work is independent, but use bcast for D-team coordination if multiple sessions are on the same file.

---

**Handover written. A cold session should start by:**
1. `git pull --rebase --autostash origin master`
2. Read the bcast board (`python C:/claude_base/branch_bulletin/bcast.py read`)
3. Land D22's URGENT pile-filter fix in `storyboard_editor.html`
4. Verify no sibling D23 conflict before editing
