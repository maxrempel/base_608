# Scribe handover - milestone 3 (~286K tokens)
# session: 20260728_ecursing_mccarthy_bee782_51f9197e
# cwd: C:\claude_base\.claude\worktrees\recursing-mccarthy-bee782
# written: 2026-07-28 10:14:05 by deepseek-v4-pro

# HANDOVER: Telepathy Lesson 1 - Reel Renderer (h01)

---

## GOAL (Max's words)

Produce lipsynced video reels for Telepathy Lesson 1 - a calm woman (Anna) at a night kitchen table speaking narration to camera. Full lesson: **112 spots**. Standing rule: everything goes through MoMA; no shortcuts, no deviations.

The most recent direct order: **"Go ahead and implement. Work safely and autonomously, ignore the compaction. I expect you to fix the semantics, fix the database, and produce the next five reels, the ones which are available."**

---

## DECISIONS MADE + WHY

1. **Prompt is split into LOCKED header + VARIABLE gesture body.**
   - *Why:* Max caught that the prompt was drifting - lighting changed from "candlelight" to "lamplight," the "completely alone; no other people" clause got dropped (causing phantom people), and the name "Anna" got printed on screen as caption text. The header is now frozen verbatim and a drift-guard in the worker refuses to render any lesson1 reel missing those clauses.
   - The locked header (verbatim): *"A woman sits alone at a kitchen table at night in warm candlelight. She is completely alone in the room; no other people appear anywhere in the frame. She speaks very kindly, gently and warmly, her gaze resting calmly straight ahead in her original forward direction. She gestures naturally and warmly with her hands as she speaks, lifting them from the table in soft expressive movements. Gentle natural blinking and breathing. The camera slowly and gently pushes in, zooming toward her."*

2. **Gestures moved from keyword-lookup to semantic (meaning-based) matching.**
   - *Why:* The keyword table assigned a two-finger counting gesture to a line about dying (because the word "either" triggered it). Max caught this - "two fingers are associated with victory, not dying." The fix: build catalog v02 where every gesture is annotated with its real meaning and feeling, then choose gestures by reading the sentence and matching meaning, not surface words.

3. **Hands must start at rest - Wan 2.6 i2v FREEZES posed hands.**
   - *Why:* Discovered painfully - the gest00-gest09 gesture-pose stills caused frozen, jittering hands. Only neutral hands-on-table stills work; the gesture is scripted as MOTION from rest.

4. **table_low.png is permanently banned as an input still.**
   - *Why:* It makes Anna look shorter. Max junked it. The fire script and rules doc both enforce this.

5. **Reels go through the sanctioned pipeline path: `fire_job()` creates a fresh queued row, the worker claims it, renders it, and the storyboard auto-seeds empty spots.**
   - *Why:* The database now has a guard blocking raw hand-edits to jobs - this is Max's "use the API, don't program around it" rule, enforced in code. Hand-editing `job_type='lipsie'` rows now throws a D44 merge-guard error. The correct path is `fire_job()` with `job_type='lipsie', scene_id='lesson1', lipsync_tool='wan26flau', arrangement_id=42, birth_line_hash=<hash>`.

6. **Worker is NEVER quit to reload code - relaunch it hidden instead.**
   - *Why:* Killing the worker stranded 11 queued reels mid-render and the safety watcher flagged the pileup. The correct reload: note the pid, relaunch `pythonw.exe combo_wan26au_worker.py` hidden, and let the old one finish its current job naturally.

7. **No-overwrite guard is active on all four lipsync workers.**
   - *Why:* Max's order after a batch was overwritten in place: "Program MOMA to prohibit this idiotic behavior. It should be scripted - no possibility of idiotic Claude to overwrite anything." `moma_safe_write.guard_output()` archives any existing render before writing.

---

## CURRENT STATE

**Coverage:** ~48 of 112 spots have an approved/done reel. The rest are held placeholders (jobs with audio binding but no video yet).

**The last 10 reels (spots 57-66, jobs 3570-3579 + 3580/3581 for spot62):**
- All 10 are rendered DONE.
- Spot 62 (the "dying" line) was re-rendered as job 3581 with the palms-together-at-45? prayer gesture, replacing the two-finger victory-sign error.
- These 10 used the v01 scripted composer (keyword-based), so the gesture quality is mixed - some may still have meaning mismatches like the two-finger one. Max has NOT reviewed these yet.

**The semantic system (v02) was BUILT BUT NOT USED YET:**
- `gesture_catalog/build_catalog_v02.py` - generates catalog_v02.json (42 gestures, all annotated with real meaning, including the new palms-together-prayer-45? gesture Max described).
- `gesture_catalog/gesture_script_v02.py` - the new semantic composer. Takes a list of sentence?gesture pairs and produces the interleaved prompt.
- These two files exist and are ready but were NEVER RUN against the fire script. The fire script (`fire_lesson1_scripted_v10_h01.py`) still calls `gesture_script_v01.py` (the keyword-based version).

**The next 5 reels (spots 67-71) were NOT fired.** The sentences were loaded and analyzed, but the firing step never happened - the context cut out mid-build.

**Worker state:** Was alive and draining at last check. Needs verification on resume.

---

## EXACT NEXT STEP

This is the implementation Max ordered and expected to be done:

1. **Strip the keyword composer and replace it with the semantic v02.** Edit `fire_lesson1_scripted_v10_h01.py` so it imports and calls `gesture_script_v02.build_prompt()` instead of the v01 `build_scripted_prompt()`.

2. **Read the 5 target reels' actual sentences** (spots 67-71, from the manifest at `sound/lesson1_production/lines_20260726/manifest.json`). For each sentence in each reel, choose the semantically correct gesture from catalog v02 by matching meaning ? gesture. No keyword table.

3. **Fire the 5 reels** via the sanctioned path (fresh `fire_job()` per reel - mirror the template in `fire_lesson1_scripted_v10_h01.py`). Pick a neutral hands-at-rest still per reel (any of: `v2_front.png, cam_right.png, v2_left.png, table_profile_r.png, cam_up.png, v2_right.png, zoom_in.png, v2_high.png, cam_down.png, table_high.png, zoom_out.png` - variety, no `table_low.png`). Use the locked header + per-sentence semantic gestures.

4. **Verify:** The worker is alive (check `wan26au_worker_pid.txt`). The 5 reels are queued and the worker claims them. The storyboard (localhost:8790 ? `/sound_assembly/code/slideshow_server_v01.py`) auto-seeds each on its empty spot.

5. **Present the 5 to Max** for review. Do NOT fire beyond 5 until he blesses the semantic v02 style.

6. **Commit and push** all changes to the MoMA repo (only explicitly staged files - never `add -A`).

---

## OPEN QUESTIONS (awaiting Max)

1. **The 10 v01 reels (spots 57-66) may need re-rolling** if the keyword-chosen gestures have more meaning mismatches like the two-finger one. Max said "I'll review the new reels." He hasn't reviewed them yet. Do NOT re-render them until he explicitly junks specific ones.

2. **The palms-together-at-45? gesture:** Max described it as "two hands, two palms together, nearly a prayer position, but fingers pointed 45 degrees forward, so not up and not forward but 45 degrees." This was added to catalog v02 as a new entry. Confirm with Max whether the description reads correctly in the gesture list.

3. **The remaining ~46 held spots:** once the semantic v02 style is blessed, the cadence Max wants is ~10 at a time, autonomous firing and babysitting. Confirm the batch size.

---

## KEY PATHS AND IDs

**Scene mapping:** lesson1 = scene rank 305 (in `scenes` table) = arrangement 42.

**Manifest:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\lines_20260726\manifest.json` (112 lines; idx 0 = spot 1).

**Still images:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\` - neutral stills (v2_*, cam_*, zoom_*, table_*, only `table_low.png` banned).

**Output reels:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\`

**Worker:** `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` - pid in `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt`, log in `...\combo_runner\data\wan26au_worker.log`, state file `...\data\wan26au_worker_state.json`. Restart: `Start-Process pythonw.exe combo_wan26au_worker.py -WorkingDirectory C:\moma\sc10\combo_runner\code -WindowStyle Hidden`.

**Fire script:** `C:\moma\sc10\combo_runner\code\fire_lesson1_scripted_v10_h01.py` - the sanctioned fire path. Calls `fire_job()` from `moma_db.py`. Skip list: approved/done/queued/running lines. `BANNED_STILLS = {"table_low.png"}`.

**Semantic v02:** `C:\moma\sc10\combo_runner\gesture_catalog\gesture_script_v02.py` + `build_catalog_v02.py`. Catalog at `gesture_catalog_v02.json`.

**Drift-guard:** `C:\moma\sc10\combo_runner\code\prompt_lock.py` + `C:\moma\sc10\combo_runner\locked_prompts\scene_locks.json` - enforces "warm candlelight", "completely alone in the room; no other people appear anywhere in the frame", "camera slowly and gently pushes in" for lesson1.

**Storyboard display:** Server at `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py`, pages `storyboard_editor_v2.html` / `_v3.html`. Placement table: `storyboard_spot_order(scene=305, spot_key=<0-based manifest idx>, position=1, job_id=<...>)`. Empty spots auto-seed when the matching non-junk reel finishes rendering.

**Rules doc:** `C:\moma\sc10\combo_runner\gesture_catalog\gesture_method_v01_tomemex.md` - the canonical reel-making checklist.

**Expenses tracker:** `api_expenses` table (via `moma_db.connect_db()`). Avg reel cost ~$0.247. Avg still ~$0.017. Lifetime MoMA API spend: ~$84.60.

**Coordination:** h01 (this session, reel renderer), H42B (sibling that voiced/staged spots 35-112). Communicate via `python C:/claude_base/branch_bulletin/bcast.py dm <name> "..."`.

---

## GOTCHAS / DEAD ENDS RULED OUT

- **Never edit `output_prompt` on an existing job via raw SQL** - the D44 merge-guard blocks it, and even if it didn't, it desyncs the prompt from the actual render (the true prompt is stamped in `lipsync_params.prompt` at render time).

- **Never use gesture-pose stills** (gest00-gest09) - Wan freezes raised hands and jitters them.

- **Never say "older," "Anna," "cozy," or "flickering" in the prompt** - the model ages the face, prints the name as caption text, and over-sharpens the background.

- **Never zoom out** - widening the frame makes Wan invent extra people.

- **Never change "warm candlelight"** - that clause is locked; changing it shifts the entire lighting and Max will catch it instantly.

- **Never quit the worker mid-render** - relaunch it hidden, let the old pid finish its job, or wait for the state file command to take effect naturally.

- **Never assume `line_current_clip` puts a reel on the storyboard** - it doesn't. The v2/v3 storyboard reads `storyboard_spot_order` and auto-seeds empty spots. The worker's auto-pick writes `line_current_clip` (for playback), not the storyboard table.

- **A held job = a placeholder with NO video** - not a kept reel. "Held = keep" means don't junk it, but it still needs to be rendered.

- Shared dirty checkout: stage ONLY explicitly named files, never `git add -A` / `git add .` / `git commit -am`. Commit and push to master after working edits.
