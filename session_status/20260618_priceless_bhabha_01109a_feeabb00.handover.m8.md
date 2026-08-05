# Scribe handover - milestone 8 (~609K tokens)
# session: 20260618_priceless_bhabha_01109a_feeabb00
# cwd: C:\moma\.claude\worktrees\priceless-bhabha-01109a
# written: 2026-06-18 15:20:18 by deepseek-v4-pro

# D23 HANDOVER - RESUME SC10 MERGED-LIPSIE SYSTEM AFTER COMPACTION

---

## GOAL (Max's words)

"D23, you are a new branch, your task is to update the system so the new line combinations - arrangements - would match the new lipsies and populate the SB with new approved and done lipsies. Save a backup of the old spine, maybe outside of DB - specifically the sc10 spine - and update the system to place new lipsies, so I can watch the assembly video."

Then, after storyboard view was built: "I started the player and it weirdly kept playing the first lipsie at least 4 times. I kept clicking on next and finally it moved to the next. Very weird. Please fix."

---

## DECISIONS MADE + WHY

### 1. Merged lipsies pinned directly to DB (not via assign API)
**Why:** The `/api/storyboard/assign` endpoint writes `jobs.line_hash`, which would overwrite the merged lipsies' synthetic hashes and break their baked audio. So `line_current_clip` was written directly into the `storyboard_state_v2` table via SQL.

### 2. Renderer patched to collapse consecutive same-lipsie lines (v09)
**Why:** The assembly renderer originally made one segment per script line. Since a merged lipsie is pinned to all lines in its range (e.g., 2774 on lines 0,1,2,3), it would play 4?. The patch collapses consecutive lines that share the same spine pick into ONE segment, using the lipsie's own baked audio (which already contains all 4 lines). Committed + pushed to master: commit `df9d5f2`.

### 3. Storyboard grouped view (v45-47)
**Why:** Max wanted to see "one merged lipsie, lines listed under one another." Before this, each line rendered its own row, so 2774 showed 4?. The fix groups consecutive lines sharing one spine pick into a single row - MERGED badge, speaker lines stacked with separators, clip tile shown once.

### 4. "Whole Scene" toggle (v46)
**Why:** The storyboard was gated by `CURRENT_ARR_ID` (the arrangement filter), scoping the view to one beat (e.g., only lines 0-3). Max couldn't see the full scene. The toggle drops the filter so all 33 lines / 11 merged rows render.

### 5. 2ND SPINE filtered to same-combination only + stars (v48)
**Why:** Max said there were "way too many lispies per item" - the 2ND SPINE was showing old per-line lipsies (fragments) rather than only takes of the exact same line combination. Filter changed to match on `line_hash` (same sound = same combination). Stars (from `lip_rating` / `fit_rating`) displayed as gold badges on 2ND-SPINE tiles.

### 6. CSS polish (v47): top-left alignment, thicker/darker divider between lipsies
Max's stylistic request.

---

## CURRENT STATE

### What is done:
- **Old sc10 spine backed up** to `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json` (32 old per-line picks, fully restorable).
- **All 11 merged lipsies pinned** across their 33 line ranges in the DB's `storyboard_state_v2` table.
- **Assembly video rendered** (draft quality, 2:24) at `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4` - plays all 11 clips in order.
- **Renderer v09** (collapses same-lipsie lines) committed + pushed to master.
- **Storyboard v45-48** (merged grouping, Whole Scene toggle, alignment, 2ND-SPINE filter + stars) all committed + pushed to master.
- **Slideshow server** restarted clean, serving `lip_rating` and `fit_rating` fields.
- **Scratch scripts** archived to `_d2x_scratch_archive/` under `sc10/combo_runner/code/`.

### What is BROKEN (the player bug Max just reported):
The player keeps replaying the first lipsie 4 times. Root cause: the **player component** likely iterates per script line and plays whatever `line_current_clip` is pinned to each line. Since 2774 is pinned on lines 0, 1, 2, 3, the player sees 4 lines ? plays the same clip 4?. The renderer (v09) handles collapse correctly, but the **player** (which is likely the in-browser playback code in the storyboard or a separate player page) was never updated with the same collapse logic.

The "next" button finally moving past suggests a manual skip-per-line behavior - each click advances one line, not one merged arrangement.

### What was INTERRUPTED:
Max said "I meant I want to see lipsie stars right on the sb" (stars on the MAIN spine tile, not just 2ND SPINE). This was interrupted before implementation. Player bug takes priority since Max asked to fix it.

---

## EXACT NEXT STEP

**Fix the player so it plays each merged lipsie ONCE, not per-line.** This requires:

1. **Find the player component** - likely a `play_from` / `playNext` / `advanceSegment` function in `storyboard_editor.html` or a separate player JavaScript file. The player is probably iterating a flat list of script lines.
2. **Apply the same collapse logic** as the renderer v09: before playing, group consecutive lines that share the same `line_current_clip` (spine pick) into a single playback slot. The collapsed list should have 11 entries (one per merged arrangement), not 33.
3. **Verify** that "next" advances arrangement-by-arrangement and that autoplay doesn't repeat the same clip across its pinned lines.

---

## OPEN QUESTIONS AWAITING MAX

1. **Should I canonicalize the sound-hashes** so all your takes of a combination group together under one row in the 2ND SPINE? (Right now they're scattered because each D21 fire script stamped a different synthetic hash.)
2. **The next-round production polish is queued** - distinct still per arrangement, arr11 turn-to-room fix, arr07 warmer Anna delivery. When do you want to kick that off?
3. **Stars on the MAIN spine tile** (not just 2ND SPINE) - still wanted after the player fix?

---

## KEY FILE PATHS

| What | Path |
|---|---|
| Renderer (patched, v09) | `C:\moma\sc10\sound_assembly\code\render_mixboard_video_v01.py` |
| Storyboard HTML (patched, v45-48) | `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` |
| Slideshow server (patched for lip_rating) | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` |
| Spine backup | `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json` |
| Assembly video | `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4` |
| Scratch scripts archive | `C:\moma\sc10\combo_runner\code\_d2x_scratch_archive/` |
| D1 database | `C:\moma\sc10\combo_runner\code\moma_db.py` (D1Client) |
| Memory files | `C:\Users\maxre\.claude\projects\C--moma\memory\` |

---

## KEY IDs - THE 11 FINAL MERGED LIPSIES

| Arrangement | Lines | Job ID | Status |
|---|---|---|---|
| arr01 | 0-3 (greeting) | 2774 | approved |
| arr02 | 4-5 | 2775 | approved |
| arr03 | 6-7 | 2810 | approved ("excellent") |
| arr04 | 8 (Anna monologue, walking) | 2812 | approved ("perfect") |
| arr05 | 9 (walking) | 2811 | approved ("great") |
| arr06 | 10-16 (window dialogue) | 2805 | approved |
| arr07 | 17-22 (window) | 2806 | approved |
| arr08 | 23 (Ishtab monologue, window) | 2807 | approved |
| arr09 | 24-27 (alcove) | 2808 | approved |
| arr10 | 28-29 (doorway) | 2794 | approved |
| arr11 | 30-32 (room) | 2795 | approved |

---

## SERVERS / PORTS

| Server | Port | Status |
|---|---|---|
| Combo GUI (lipser viewer) | 8779 | UP |
| Slideshow server (storyboard, assembly) | 8790 | UP |
| MOMA worker (wan26au) | background | UP |

---

## GOTCHAS + DEAD ENDS

1. **"Smiles" / "grins" in prompts** ? wan2.6 produces excessive smiling, laughter, or ham acting. Final template uses NO smile/grin words. Saved to memory: `feedback_no_grin_smile_words.md`.

2. **Speaker swap in merged clips** ? wan ignores bare "Left"/"Right" labels. The fix that worked: **describe both characters + positions first, then explicit speak-ORDER** ("the red-haired woman on the left speaks first, then the elder on the right answers"). Tested on 2810 (approved "excellent").

3. **Frozen/robotic hands in walking shots** ? "completely still" froze Ishtab's hand mid-air (2803, junked). "Arms moving naturally" made robotic periodic motion (2809). **Neutral phrasing** (don't direct the hands at all) worked - 2811 approved "great."

4. **Distinct still per arrangement** - the D21 batch reused one still per location (B1 corridor-walk for all walking, sc05 for all window). Max noted every lipsie should start from a different image. Saved as rule (`feedback_distinct_still_per_lipsie.md`) but NOT yet applied to this batch.

5. **Synthetic line-hashes** - merged lipsies carry a shared synthetic hash, so they appear as spine picks but NOT in per-line candidate pools (which match on real line-hash). Expected behavior, not a bug.

6. **"Approved" status autoset** - the lipser was auto-approving on view. Max confirmed these were his genuine approvals after re-approving in a batch, no canon-forging bug.

7. **Arrangement filter hiding the scene** - the biggest dead-end of D23. I chased cosmetic markers for 30+ minutes before realizing the storyboard was gated by `CURRENT_ARR_ID` = one beat. The "Whole Scene" toggle (v46) fixed it.

8. **The player bug = same root cause as the renderer had** - per-line iteration without collapse. The renderer was patched; the player wasn't. Likely a 15-minute fix if the player code lives in the same `storyboard_editor.html` file.
