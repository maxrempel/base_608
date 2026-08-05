# Scribe handover - milestone 4 (~327K tokens)
# session: 20260706_youthful_rosalind_f7c6ed_4433a1f9
# cwd: C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed
# written: 2026-07-06 16:19:27 by deepseek-v4-pro

# Handover: Facer + Facefreeze in MoMA - Selective Frozen-Face Editing for Wan Reels

**GOAL (in Max's own words)**

> *"Document everything and implement it within MoMA so it will work inside MoMA. ... there will be a button. It should be initiated from the pop-up of the real pop-up. I play the real. I see it. And I decide that I need to silence a certain line. And a certain person of the certain line. So I label the faces and then label the line and also I need a little bit of cushion around the line, half a second before and half a second after. And then we run and I get the new copy, also registered in MoMA, it would be a new job."*

In short: a **"silence face"** tool that freezes *only one face, only during one spoken line* (with a smooth transition), and produces a new registered job - all from inside the MoMA popup.

---

## DECISIONS + WHY

1. **Start with face-labeling tool (facer)**
   - Why: The whole freeze/edit approach needs pixel?precise rectangles for each speaker's face. The user draws boxes (up to 6) on a still image, saved per?image in D1 (`face_boxes` table).
   
2. **Freeze approach, not black?box or re?animate**
   - Early ideas: black?out non?speakers, or re?animate per line. Max settled on **freezing the wrong talker's face** because Wan can't stop mouths from moving. The frozen face comes from the first frame of the clip (no separate still needed) and is blended with feathered edges to hide seams.

3. **Surgical freeze, not full?reel freeze**
   - First version froze *all* non?speakers for the entire reel. That felt too static. Second version (what we shipped) freezes **only one face, only during one line**, leaving everything else live. This is closer to Max's real need: remove one leaks (like Werner's mouth moving during Derek's "Bias.").

4. **Smooth interpolation during the frozen window**
   - Instead of a hard still?frame pop, we crossfade (morph) the frozen face from the frame *just before* the leak to the frame *just after*. Uses OpenCV (`cv2.addWeighted` with smoothstep easing). This hides the transition.

5. **UI inside the reel popup, not a separate tool**
   - A pink **"silence face"** button appears on any reel popup. Opens a small panel: dropdown for the person (box number, using the stored character?box map), dropdown for the line (from the script, auto?resolved), cushion input (?0.5?s default), and a Run button.

6. **New job registration, never overwrite original**
   - The rendered clip is copied into MoMA's `output_lipsies` folder and registered as a new job via the canonical `fire_job()` in `moma_db.py`. The original reel stays untouched; the user gets a fresh candidate.

7. **Durability**
   - DB tables auto?created on server start (`ensure_face_boxes_table`, `ensure_face_box_chars_table` in `moma_db.py`).
   - Character?to?box map (`face_box_chars`) is remembered per still, so the user only sets it once per scene.

---

## CURRENT STATE - What is done and verified

Everything is **coded, tested end?to?end, committed & pushed** to the MoMA repo (master). A clean server restart has been performed, so new endpoints are live.

### A. Database (D1, UUID `fee7c39e-4816-4a04-b41f-7067182da1c3`)
- **`face_boxes`** - per?job face rects (job_id, person_number, x, y, w, h). Used for both facer display and facefreeze.
- **`face_box_chars`** - per?still mapping from box number to character name (still_job_id, map_json). Set once, reused.

### B. Backend (`combo_gui.py`)
- **`GET /api/faces/<job_id>`** - returns face boxes for that job.
- **`POST /api/faces/<job_id>`** - saves a batch of boxes.
- **`DELETE /api/faces/<job_id>`** - deletes all boxes for that job.
- **`GET /api/facefreeze/<reel_job_id>`** - returns:
  - `lines`: list of `{idx, char, start_s, end_s, text}` for the reel.
  - `persons`: list of box numbers that have face boxes on the source still.
  - `map`: stored character?to?box mapping, if any.
- **`POST /api/facefreeze/<reel_job_id>`** - accepts `{person, line_idx, cushion}`. Calls `facefreeze.py` (surgical mode), copies result to lipsie folder, registers a new job via `fire_job`, returns `{new_job_id, output_file}`.

### C. Compositor engine (`facefreeze.py`)
- **`config_surgical_from_reel()`** - resolves reel ? still job, face boxes, script lines, audio timeline, computes the exact freeze window for the given `line_idx` ? cushion.
- **`render_surgical()`** - reads the original video frame?by?frame, applies the freeze overlay with smooth?step interpolation on the selected face box. Outputs a new MP4 (H.264, same resolution and fps as source).
- CLI still works: `python facefreeze.py --reel 3279 --freeze 2 --line 11 --cushion 0.5`.
- **`register_as_new_job()`** copies the output to `output_lipsies/`, phones `fire_job` via the DB, and returns the new job ID.

### D. Frontend (`popup.js`)
- **"silence face" button** appended to all shot?type action rows (including video/reel). Only visible when the popup is showing a lipsie reel (job_type `wan26flau` etc.).
- **Panel logic** (`_facefreeze()`):
  1. Calls `GET /api/facefreeze/<job_id>` to load lines, persons, and saved map.
  2. Shows a small overlay with three inputs: person (dropdown of box numbers, with character name if map exists), line (dropdown of line texts with speaker), cushion (number, default 0.5).
  3. On "Run", POSTs to the same endpoint.
  4. On success, fetches the new job's details from `/api/job/<id>` and opens a new popup for it (using the existing `openPlate()`).
  5. After closing, calls `onAfterAction` module?scope callback to refresh parent if needed.
- **Facer button** added earlier; works on any popup, draws boxes on image or video element, saves via `/api/faces/<job_id>` POST. Already committed.

### E. Documentation
- **`facefreeze_method_v01_tomemex.md`** - full technical architecture, schema, endpoint signatures, reasoning (searchable in Memex).
- **`facefreeze_instruction_v01_tomemex.md`** - step?by?step user instruction: how to label, set map, run silence?face.

### F. Test artifacts
- Reel **J3279** (sc11_arr02, spot4) had face boxes on still **v66** (job 3141). Character map: WERNER=2, DEREK=3, ANNA=4.
- Manual test: froze Werner during Derek's "Bias." (line index 11) ? output opened and verified.
- Automated test via POST to `/api/facefreeze/3279` with `{person:2, line_idx:11, cushion:0.5}` ? created **job 3289**, 9.5?MB, playable from MoMA.
- All endpoints tested with `curl` after server restart.

---

## EXACT NEXT STEP

**No immediate action needed - the tool is fully integrated and ready for use.** The next natural step is *using it* on more scenes:

1. For any scene/still not yet labeled, open the still in MoMA ? click **facer** ? draw boxes (1,2,3,4).
2. In the still's popup, the "silence face" button will ask for the character?to?box map once (e.g., `{"WERNER":2,"DEREK":3,"ANNA":4}`). That map is stored on the still and will be pre?filled in future reel editing for that scene.
3. Open a reel made from that still ? click **silence face** ? pick the wrong?mouth person, the offending line, adjust cushion if needed ? click Run. A new job is created and opened.

If you need to fix Derek's head turn to Werner on "Bias" (the gaze problem), that's a **separate task**: it requires modifying the Wan prompt and re?rendering the whole clip - the freeze tool can't change gaze direction. That remains an open request.

---

## OPEN QUESTIONS AWAITING MAX

1. **Derek gaze fix** - Max acknowledged that the clip shows Derek looking at Werner on "Bias." He said "I will deal with the prompt later." No action taken. This will need a new Wan render with a corrected prompt.
2. **Is the crossfade smooth enough?** - The current interpolation is a simple smoothstep blend between before? and after?frames. Max hasn't reported artifacts, but may want to tweak feather width or use a more advanced morph if seams appear on other footage.
3. **Should the cushion be different per line?** - Currently default 0.5?s each side. Could be made adjustable per line, but we left it as a single numeric input. Might need revisiting if some lines need longer lead?in.
4. **More than one face frozen per line?** -
