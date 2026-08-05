# Scribe handover - milestone 9 (~687K tokens)
# session: 20260618_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-18 17:40:28 by deepseek-v4-pro

## Handover: sc10 Storyboard Pile Cleanup & Merge Traceability

### GOAL (in Max's own words)
Max wants the **storyboard pile** to show **only the Anna+Ishtab two?shots** (the two ladies in the scene style, looking at each other). Everything else - backgrounds, empty rooms, ships, window plates, solo characters - must vanish from the pile. The pile has been cluttered through twenty iterations and Max is frustrated; he said "that's what i see. Test end to end and fix. Or who should i beg? that's like 20 iterations, 2 hours , no progress."

Separately, Max wants all merge/rearrange operations fully traceable and synced everywhere (audio ? script_lines ? lipsie ? Notion), but the immediate blocker is the storyboard pile.

### DECISIONS MADE & WHY
1. **Merge prompt template (arr01-04):** After many failures (smiles ? laughing, quoting lines ? speaker swap, etc.), the approved style is:  
   - "Formal meeting of officials" atmosphere.  
   - Characters described by appearance and position (left/right) *before* the quoted lines, to stop the model from mixing up speakers.  
   - "Minimal nods, royal posture, minimal grins, eyes on each other, not the camera."  
   - No emotions words like "smile" / "warm" - they caused random laughter and penguin?nodding.  
   - The winning job: **2774** (arr01 greeting, 4 lines) on the meeting?hall two?shot.  
   - Frames from existing approved clips were used as stills for alcove and doorway beats where no standalone two?shot existed.

2. **Scene?picker dual?level:** After breaking the storyboard by making the picker scene?only, it was changed to offer both "ALL (whole scene)" and individual arrangements, so the storyboard could still filter by arrangement while the combo?gui tabs see everything at once.

3. **Lipser UI:** The dialogue lines are now shown in the lipser row (extracted from the prompt's quoted lines), and the comment boxes were moved to the buttons column.

4. **Trim audio fix:** The trim dialog now unpauses audio and stops forcing a pause on every scrub, so the video keeps sound while you drag.

5. **Merge?traceability:** A `merge_ops` ledger was created in D1; `sass.py` now uses a configurable 0.10?s silence gap between merged lines; `fire_merge_lipsie.py` is wired to stamp the ledger. The reverse Notion sync is pending (not yet built).

6. **Storyboard pile filter history:**  
   - D23 added a scene?only pile filter (`getBinImages` shows only images whose arrangement is in the scene's set).  
   - D24 then added a **background/plate filter** (commit `647761d`) that hides images whose filenames contain `bg_`, `extrap`, `iter_bg`, `station`, `window_looking`, `composite_bg`, `pair_strip`, etc.  
   - Max said after reload the pile didn't change, likely because of browser cache (hard?refresh required).  
   - His subsequent "that's what I see" after our push indicates the pile is still showing too many irrelevant things.

### CURRENT STATE
- The storyboard route is **slideshow_server on port 8790**, serving `storyboard_editor.html` (the current version, with our background?filter).
- The filter logic is at around line 644 in `storyboard_editor.html` (a `const isCharShot` check added inside `getBinImages`).
- The server reads the file fresh per request, so a hard?refresh should pick it up.
- The data comes from `http://localhost:8790/api/approved_images` - each image has `output_file`, `role`, `arrangement_id`, etc.
- Max's session is **D24** (check?in signature ???). The branch is `master`; everything is pushed.
- 143 junk lipsies, 36 errored lipsies, and 43 orphan jobs were found in sc10 earlier; 36 errored ones were junked. The remaining orphans (null arrangement) are still in the DB but not auto?junked.
- The merge?traceability effort is on hold while this pile crisis is resolved.

### EXACT NEXT STEP (what the next session must do)
1. **Hard?refresh the storyboard tab** (Ctrl+Shift+R) in Max's browser.
2. **Inspect what images are actually shown** in the pile. Open /storyboard on 8790.
3. **Check `/api/approved_images`** directly (e.g. `curl http://localhost:8790/api/approved_images?scene=10`) to see which images are returned. Cross?reference with the file we edited to confirm the filter patterns are catching everything.  
   - The filter currently excludes filenames containing `bg_`, `extrap`, `iter_bg`, `station`, `window_looking`, `composite_bg`, `pair_strip`.  
   - If non?two?shot images remain, look at their `output_file` names and add patterns to `BACKGROUND_PATTERNS`.
4. **If the filter is working but solo character images or composite shots still appear**, tighten the criteria. Max's exact words: "the only relevant images are with two ladies in this style. Everything else is irrelevant." That suggests a **two?shot filter** (maybe filenames containing `twoshot` or `two_shot`).  
   - However, the approved two?shots have names like `sc01_meet_twoshot_var01.png`, `sc05_window_twoshot.png`, `sc_B1_meet_twoshot.png`, `sc_window_twoshot_fix1.png`. So `twoshot` or `meet` could be used.  
   - Alternatively, we could add an API endpoint that returns only images with `role` indicating two characters, or we could rely on filename pattern `twoshot`.  
   - The current `getBinImages` is a client?side filter; we can make it stricter: after the background removal, keep only images whose filename matches `/twoshot/` (case insensitive).
5. **Push the refined filter immediately** (commit to master, push). Max's rule #1: always merge+push before asking him to verify.
6. **After pushing, tell Max to hard?refresh again** and confirm.
7. **If the pile still looks wrong**, we might need to examine the actual metadata in D1 (e.g., `source_still` hash) and adjust the server?side `/api/approved_images` endpoint to pre?filter. But start with the client?side pattern.

### OPEN QUESTIONS (still awaiting Max)
- Whether the existing two?shot filename pattern `twoshot` reliably catches all relevant images, or if some two?shots are named differently (e.g., `composite_bg_concourse_chars`). Max hasn't answered.
- Whether we should build a permanent "two?shot only" toggle in the storyboard UI.
- For the merge?traceability: what exact sync direction should the reverse Notion sync take? (Max said "I don't care about direction, it should be synked.") Notion writes are risky; we should probably wait for Max's explicit approval.

### KEY FILE PATHS / IDs
- **Storyboard pile HTML:** `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (lines ~640-660, `getBinImages` function, `BACKGROUND_PATTERNS` array added near line 200).
- **Slideshow server:** `slideshow_server_v01.py` (reads the same HTML). Port 8790.
- **Arrangement picker (dual?level):** `C:\moma\sc10\combo_runner\code\arrangement_picker.js`
- **Runner core (lipser UI):** `C:\moma\sc10\combo_runner\code\runner_core.js`
- **Trim dialog fix:** `C:\moma\sc10\shared_ui\popup.js`
- **Batches/comments:** `C:\moma\sc10\combo_runner\code\batches.py`, `merge_ops.py`, DB table `merge_ops`.
- **Sass merge gap:** `C:\moma\sc10\sound_assembly\code\sass.py` (line ~605-660, constant `MERGE_GAP_S`).
- **Lipser approved merge job:** 2774 (arr01 greeting).
- **Scene 10 arrangement IDs:** 2,3,4,5,6,7 (hall, corridor/window, alcove, doorway, etc.).

### GOTCHAS / DEAD ENDS RULED OUT
- **Browser caching:** The storyboard page must be hard?refreshed (Ctrl+Shift+R) every time the HTML changes. Max's "reloaded, didn't change" was likely a soft reload.
- **Smiles / emotional prompts:** Caused laughter and head?nodding chaos in wan2.6. Replaced by neutral "formal officials" wording. Do not reintroduce.
- **Bare "Left/Right" labels:** The model often ignores them; describe both characters by appearance + position first.
- **Ad?hoc merge scripts (D21's synthetic hashes):** Caused hidden surgery and must be retired. All merges should go through the canonical `[[MERGE]]` blocks in the script ? sass ? libup ? fire_merge_lipsie.
- **Storyboard editor is a shared file:** D23/D22 also edit it. Announce all edits on the d?team board before changing. Ensure `git pull --rebase` before pushing.
- **Pile filter commit `647761d`** is live; the filter correctly excludes backgrounds by pattern, but may not exclude solo character images or composites that aren't two?shots. The next step is to inspect and refine.
