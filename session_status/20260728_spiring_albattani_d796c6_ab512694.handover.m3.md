# Scribe handover - milestone 3 (~286K tokens)
# session: 20260728_spiring_albattani_d796c6_ab512694
# cwd: C:\claude_base\.claude\worktrees\inspiring-albattani-d796c6
# written: 2026-07-28 02:30:00 by deepseek-v4-pro

# HANDOVER - Telepathy Lesson 1 (h01, Reel Renderer)

---

## GOAL (in Max's words)

Produce lipsynced video reels for all ~112 spots of "Telepathy Lesson 1" - a calm woman at a night kitchen table speaking narration to camera. Everything through MoMA with no deviations or shortcuts. H42B voiced and staged the full expansion (spots 1-112) on arrangement 42 / scene 11 / tag "lesson1." h01 renders the reels using Wan 2.6 i2v-flash.

Max's most recent instruction: keep producing reels to fill gaps - only fill **junk** spots, never touch approved or held. "Do another 5 to another 5."

---

## THE LOCKED PROMPT (permanent, verbatim - do not edit)

```
A woman sits alone at a kitchen table at night in warm candlelight. She is completely alone in the room; no other people appear anywhere in the frame. She speaks very kindly, gently and warmly, her gaze resting calmly straight ahead in her original forward direction. She gestures naturally and warmly with her hands as she speaks, lifting them from the table in soft expressive movements. Gentle natural blinking and breathing. The camera slowly and gently pushes in, zooming toward her.
```

This was given by Max directly after discovering h01 had drifted the wording. It is now **locked in two enforcement layers**:
1. **Prompt lock file:** `C:\moma\sc10\combo_runner\locked_prompts\scene_locks.json` - defines mandatory substrings per scene (for lesson1: "warm candlelight", "completely alone in the room; no other people appear anywhere in the frame", "camera slowly and gently pushes in").
2. **Worker guard:** `C:\moma\sc10\combo_runner\code\prompt_lock.py` - wired into `combo_wan26au_worker.py`. The worker REFUSES to render or spend money on any lesson1 reel whose prompt is missing any mandatory clause. Scene-specific - other scenes are not affected. Marked as error, logged, job status set to `'error'`. This means a drifted prompt can never become a video.
3. **Fire script:** `fire_lesson1_reels_v09_h01_matchface.py` - `BASE` constant is set to this exact prompt; `compose()` now returns BASE verbatim (no appended per-spot text, since the locked prompt already includes camera direction and gesturing).

---

## DECISIONS MADE AND WHY

### Prompt formula defects (all confirmed, all fixed)
- **"older"** ages her face and changes the person. Removed.
- **"Anna"** (proper name in prompt) gets printed on screen as caption text by Wan. Removed.
- **"cozy" / "flickering candlelight"** over-sharpens the background and changes the lighting. The original is **"warm candlelight"** - not "lamplight," not "flickering." This is locked verbatim.
- **No zoom-out (pull).** Zooming out widens the frame and the Wan model invents extra people in the empty space. Only push-in or lateral pans. The CAM dict in v09 explicitly excludes "pull" with a hard assert.
- **Missing "completely alone" clause** is why a second person appeared. Locked as mandatory now.

### Prompt must accompany the reel (provenance fix)
The Storyboard popup was reading the editable `output_prompt` job field, which gets overwritten when a new prompt is staged. Max: "the old render should display the old prompt." Fixed in `C:\moma\sc10\shared_ui\popup.js` (~line 1210): the popup now reads `lipsync_params.prompt` (the prompt literally stamped into the render at creation time). Old renders now show their old prompt forever.

### No-overwrite guard (scripted enforcement)
Max: "Program MOMA to prohibit this idiotic behavior. There should be no possibility of idiotic claude to overwrite anything."
- Created `C:\moma\sc10\combo_runner\code\moma_safe_write.py` - `guard_output(out_path)` moves any existing file into an `archive/` subfolder renamed `obsolete_<timestamp>_<name>` before the new file is written. Counter suffix (_2, _3) if name collision.
- Wired into all four lipsync workers (`combo_wan26au_worker.py`, `combo_sync_worker.py`, `combo_lipsync_worker.py`, `combo_s2v_local_worker.py`) immediately before each write.
- Committed and pushed.

### Auto-set storyboard spine pick
When a reel finishes rendering, the worker now calls `_auto_set_as_storyboard_pick()` which sets `jobs.line_current_clip = job['id']` only if the line has no current pick yet (never clobbers an approved one). Code is committed but the worker needs a restart to pick it up - the currently running worker predates this change.

### Status discipline
Max corrected: held = keep (do NOT redo); junk = redo (fill gaps). Approved = keep. Never touch approved or held. Only fill junk gaps.

### Banned inputs
- `table_low.png` - makes Anna look shorter. Junked the still job itself (3393) and must never use it as input for any reel. The 8 held reels that pointed at it had their inputs repointed to varied good stills (free, no re-render).

### Gesture direction (accumulated rules)
- Gestures must be meaning-driven and symbolically correct.
- Slightly less head movement and face-touching than earlier batches.
- Face/temple touch only when meaningful, brief, once per reel, then hand leaves.
- No repetitive looping - the current locked prompt already handles this with "gestures naturally and warmly."
- Asymmetric preferred.
- Reserved overall - Americans over-gesture.
- Cultural variety in the gesture catalog (Indian, Russian, Jewish, Georgian, Mediterranean).
- Resting default: hands interlaced, fingertips together like holding a tennis ball, resting on the table.
- Note: the locked prompt now says "she gestures naturally and warmly with her hands as she speaks, lifting them from the table in soft expressive movements" - this IS the gesture direction. No extra per-spot motion tagging is appended.

### Terminology (committed to user dictionary)
Max's tab names: **Imager, ReelMaker, Storyboard (SB), MOMA Music Overlay, MOMA Music Player + Annotations.** The word "combo" is a dead internal code name only - never say it to Max. Recorded in `C:\claude_base\user_dictionary_tomemex.md`.

---

## CURRENT STATE

### What is done
- First 34 reels (spots 1-34) are rendered and Max has approved many.
- Spots 35-46 went through multiple bad renders (v07 gesture-pose stills froze hands; v08 had "older"/"Anna"/sharp-background prompt defects; v09 is the corrected formula). Max has manually approved the good ones from this range and junked the bad ones.
- The worker guard (prompt lock), no-overwrite guard, and SB popup fix are all committed and pushed.
- The gesture catalog (41 entries, picker, method doc) exists but may not be used directly now that the locked prompt handles gesturing natively.

### What is in flight
- The render worker (`combo_wan26au_worker.py`) was accidentally killed by h01 (a stop signal meant to reload new code), then restarted. At last check it was draining 11 queued reels, with job 3432 rendering.
- 56 more held jobs (spots 47-112) remain queued or held, waiting to be fired and rendered.
- The currently running worker is the OLD binary - it does NOT have the prompt-lock guard or the auto-pick code. A clean restart is needed when the current batch finishes.

### Data snapshot (as of last check)
- **Approved reels on disk:** spots 1-37 (some gaps where Max junked - exact approved set is whatever Max kept in the Storyboard).
- **Rendered and waiting placement:** jobs 3419, 3421, 3426, 3428, 3429, 3430, 3432, 3493 (8 gap reels). Some landed in the Storyboard already (spots ?46 auto-seed fine); spots 47+ will auto-seed as they render because those spots have no prior order.
- **Queued and rendering:** ~11 jobs (the ones the restarted worker is draining). The safety watcher flagged the pileup and h01 restarted the worker.
- **Held (not yet rendered):** ~56 jobs for spots 47-112. These are H42B's staged placeholders - correct spot?audio links, but no video yet. They need to be updated with the locked prompt + a good still, then queued.

### H42B coordination
H42B confirmed: "All 78 held on lesson1/arr42/wan26flau (ids 3486-3564). Voice trimmed." Communication channel: `python C:/claude_base/branch_bulletin/bcast.py dm H42B "message"`. This session is h01.

---

## EXACT NEXT STEP

1. **Let the current render batch finish.** The worker is draining ~11 queued reels. Wait until all are DONE. Check with:
   ```
   cd C:\moma\sc10\combo_runner\code && python -c "import moma_db; ..."
   ```
   Query jobs with `output_status='queued' AND scene_id='lesson1'` to see what's left.

2. **Restart the worker cleanly** so it picks up the new prompt-lock guard and auto-pick code. The current worker predates these changes.
   - Read current pid: `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt`
   - Stop the process: `Stop-Process -Id <pid> -Force`
   - Restart hidden: `Start-Process pythonw.exe -ArgumentList "combo_wan26au_worker.py" -WorkingDirectory "C:\moma\sc10\combo_runner\code" -WindowStyle Hidden`
   - Verify the new pid appears in the pid file.

3. **Fill remaining held jobs (spots 47-112).** For each held job that is NOT yet rendered:
   - Set `output_prompt` to the locked prompt verbatim (from `fire_lesson1_reels_v09_h01_matchface.py` BASE constant).
   - Set `source_image` / `input_file` to a good neutral still (any from `tape1select_output` EXCEPT `table_low.png`). Rotate through: `v2_front.png, cam_right.png, v2_left.png, table_profile_r.png, cam_up.png, v2_right.png, zoom_in.png, v2_high.png, cam_down.png, zoom_out.png, v2_profile_l.png, table_high.png`.
   - Set `lipsync_tool='wan26flau'`, `output_status='queued'`.
   - Fire in batches of ~5-10. After each batch, set their `line_current_clip` in `storyboard_spot_order` or let auto-seed handle it (spots 47+ have no prior order, so the Storyboard client auto-seeds them on page load).

4. **Present results** by serving the HTML gallery over HTTP:
   - Build gallery at `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\_lesson1_review.html`
   - Serve: `python -m http.server 8899` from that folder
   - Open: `http://127.0.0.1:8899/_lesson1_review.html` in Chrome
   - Vocalize when done: `pythonw C:/claude_base/tools/attention/attention.py --msg "..."`

5. **Vocalize when finishing anything** - Max's standing rule.

---

## OPEN QUESTIONS (still awaiting Max)

- None active - Max is driving the approve/junk review manually in the Storyboard.

---

## KEY PATHS AND IDS

### Database
- **D1 database** - accessed via `moma_db.connect_db()` (NOT the stale `combo_db.sqlite` snapshot).
- **Job IDs for expansion:** H42B staged 3486-3564 (78 jobs), some of which are the spots 35-46 that were re-rendered.
- **Arrangement:** 42, scene: 11, tag: "lesson1".
- **The 10 approved gesture-pose stills:** stored under scene "Tape 1Select" / arrangement 43, jobs 3482-3569, labels gest00-gest09. These have pre-raised hands - DO NOT use as input for Wan reels (Wan freezes/jitters posed hands). Use only neutral hands-at-rest stills.

### Files (all under `C:\moma\sc10\combo_runner\code\` unless noted)
- **fire_lesson1_reels_v09_h01_matchface.py** - the current fire script with locked prompt, no-zoom-out CAM, table_low ban. Update held jobs with this script's BASE and still selection.
- **combo_wan26au_worker.py** - the cloud lipsync worker. Has prompt_lock guard (import + check), auto-pick on finish, no-overwrite guard. Model: Wan 2.6 i2v-flash, 720P, 3-15s, $0.025/sec (~$0.247 avg per reel).
- **prompt_lock.py** - the guard module. `check_prompt(scene_id, prompt)` returns (ok, missing_clauses). Loads rules from `locked_prompts/scene_locks.json`.
- **moma_safe_write.py** - `guard_output(out_path)` no-overwrite guard.
- **audio_resolver.py** - `resolve_per_line_audio()` maps birth_line_hash ? per-line wav. Note: `_scene_num()` uses `re.fullmatch` (v05 fix) so "lesson1" is correctly treated as a named tag, NOT scene 1.
- **popup.js** - `C:\moma\sc10\shared_ui\popup.js` - Storyboard popup now reads `lipsync_params.prompt` for reels.
- **gesture_catalog/** - `C:\moma\sc10\combo_runner\gesture_catalog\` - 41 gestures, picker, method doc. May not be actively used now (locked prompt handles gesturing).
- **gesture_method_v01_tomemex.md** - the "how to make a lesson reel" rules doc. Contains hard camera rules, prompt rules, no-overwrite, status discipline. Keep updated.

### Still images (input folder)
`C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\`

**Good neutral stills (use these):**
v2_front.png, cam_right.png, v2_left.png, table_profile_r.png, cam_up.png, v2_right.png, zoom_in.png, v2_high.png, cam_down.png, zoom_out.png, v2_profile_l.png, table_high.png

**BANNED:**
- `table_low.png` - shortens Anna
- Any `gest*.png` (gest00-gest09) - pre-raised hands freeze/jitter in Wan

### Output lipsies
`C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\`
Naming: `lesson1_lipsie_v{job_id}_wan26flau.mp4`
Archive: `output_lipsies/archive/obsolete_<timestamp>_<name>`

### Audio
`C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\lines_20260726\`
Manifest: `manifest.json` - maps line_hash ? vocal_line, text, audio path, duration.

### Worker state
- pid file: `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt`
- log: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\wan26au_worker.log`
- launch: `Start-Process pythonw.exe -ArgumentList "combo_wan26au_worker.py" -WorkingDirectory "C:\moma\sc10\combo_runner\code" -WindowStyle Hidden`

### Storyboard
- Server: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (port 8790)
- Client v2: `storyboard_editor_v2.html` - handles position system, auto-seeds empty spots
- Client v3: `storyboard_editor_v3.html` - elegant lane
- line_current_clip picks stored in DB and auto-set by worker on finish (if committed code is live)

### Coordination
- `python C:/claude_base/branch_bulletin/bcast.py whoami h01` - register
- `python C:/claude_base/branch_bulletin/bcast.py dm H42B "message"` - message sibling

### User dictionary
`C:\claude_base\user_dictionary_tomemex.md` - contains MoMA tab name map, "combo" is dead word rule.

---

## GOTCHAS AND DEAD ENDS

### NEVER do these
- **Never** use a still with hands already raised in a
