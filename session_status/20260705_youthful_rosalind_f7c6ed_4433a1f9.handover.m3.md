# Scribe handover - milestone 3 (~227K tokens)
# session: 20260705_youthful_rosalind_f7c6ed_4433a1f9
# cwd: C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed
# written: 2026-07-05 23:46:02 by deepseek-v4-pro

# HANDOVER - D05B: facer + facefreeze for MoMA

---

## GOAL (in Max's words)

1. **Facer**: a tool inside MoMA's image popup. Open any image (from imager or anywhere), click "facer", and with the mouse draw numbered boxes over each person's face, left to right. Up to 6 people (normally 4). Boxes auto-save to the database, per image. Just labeling - part 1 only.

2. **Facefreeze (crazy idea)**: for scene 11 spot 4 (lines L10-L15, 4 people talking in sequence - Anna/Derek/Anna/Derek/Anna/Werner), take the animated Wan clip where **everyone** flaps their mouths, and **freeze the faces of non-speakers** so only the current speaker's mouth moves. Frozen listeners = fine, ???? ? ????. Audio gives the timing of who speaks when; the facer boxes say *where* each face is. One clip, with the freeze mask switching per line.

---

## DECISIONS MADE + WHY

### facer
- **Where**: built directly into `shared_ui/popup.js` (the MoMA image/video popup) and `combo_gui.py` (the backend).
- **Storage**: new D1 table `face_boxes` in Cloudflare D1 database `moma-d1-dev`. Columns: `job_id` (text), `person` (integer 1-6), `x, y, w, h` (integers).
- **Backend**: two endpoints - `GET /api/faces/{job_id}` returns all boxes as JSON; `POST /api/faces/{job_id}` upserts a single person's box (body: `{person, x, y, w, h}`); `POST /api/faces/{job_id}/delete` removes one person's box.
- **Frontend**: pink "facer" button added to ALL popup types (plate, photo-shot, video reel). When activated, shows numbered person buttons, a "clear all" and "done" button. Clicking a person number activates box-drawing mode - mouse drag draws a coloured rectangle, auto-saves on mouseup. Overlay sits above `<img>` or `<video>`.
- **Why pink button**: so it stands out among the existing action buttons.
- **Commit**: pushed directly to master (adviser flagged - next MoMA change should use a branch).

### facefreeze
- **Approach**: Max rejected multi-pass ideas (silent clip + lipsync overlay; gaze-direction prompting). Settled on the simplest: **freeze non-speakers by overlaying a static crop from the clip's first frame onto their face box**. Speaker's face stays live from the Wan clip.
- **Why first-frame**: uses the clip's own first frame - perfect alignment, no colour mismatch, no separate still needed.
- **Feathered edge**: OpenCV seamless cloning or simple alpha-feathered blend at box boundary to hide the seam. Test frame at 6.5s (Derek speaking) showed no visible box seam.
- **Why OpenCV, not ffmpeg**: finer control over per-frame feathering and compositing.
- **Timing extraction**: used `ffmpeg silencedetect` on the Wan clip's audio track to find speech envelope, cross-referenced with per-line audio durations from the merge builder's concat logic (plain concat, no gaps - boundaries = cumulative member durations).
- **Speaker?box mapping for spot 4** (left to right): Person1 (silent, back to camera, frozen all the time), **Werner = box 2, Derek = box 3, Anna = box 4**.

---

## CURRENT STATE

### Done
- **facer**: fully working. Tested round-trip (save/load/delete) against live server on localhost:8779. Data for job 3141 (still v66) has 4 face boxes saved with correct coordinates. Button now appears on ALL popup types, including video reels. Hard refresh needed to pick up new JS.
- **facefreeze**: Python tool `facefreeze.py` built and tested. Rendered a test clip for spot 4: `sc11_spot4_facefreeze_v01.mp4` (420 frames, ~14s). QC at 6.5s frame shows clean composite - Derek green officer talking, others frozen, no visible seam. **The test clip is open on Max's screen right now for his review in motion.**
- Both files committed and pushed to master.

### In flight
- **Max is reviewing the facefreeze test clip** for two specific things:
  1. Does the freeze boundary flicker/jump at line transitions?
  2. Is the "stillness" of frozen listeners acceptable (Max said "???? ? ????, ?????? ????? ??????????" so he expects them static)?

### NOT yet done
- `face_boxes` table is NOT in the startup/schema creation code - it was created manually via D1 query. A fresh MoMA install won't have it.
- facefreeze is a standalone command-line tool - NOT integrated into the MoMA UI or the reel-building pipeline yet.
- No other spots processed with facefreeze.

---

## EXACT NEXT STEP

**Wait for Max's verdict on the test clip.** He needs to watch the full 14-second clip in motion. Two possible paths:

- **If it looks good**: apply facefreeze to other spots (Max will specify which).
- **If the freeze boundary flickers at transitions**: increase feather radius and/or adjust segment timing (add small crossfade at line boundaries).
- **If frozen listeners look too dead/unnatural**: this was exactly Max's initial concern ("stupid idea, it wouldn't work") - may need to revisit the silent-clip-with-lipsync-overlay approach, or accept the stillness as "good enough."

After verdict, next likely tasks:
1. Integrate facefreeze into the MoMA pipeline (trigger from UI, register output as a job).
2. Add `face_boxes` table to server startup.
3. Branch-based workflow for future MoMA changes.

---

## OPEN QUESTIONS

1. **Verdict on test clip**: does the facefreeze work in motion? (Max is watching it now - was interrupted at the end of the session.)
2. **Which spots next**: if the approach works, which other scene 11 spots need facefreeze?
3. **UI integration**: should facefreeze be a button in the MoMA popup (like facer), or stay a command-line/script tool?
4. **Cross-job facer data**: facer boxes are per-job_id. Still v66 (job 3141) has boxes, but the video reel job (J3279) does not. If Max draws on the video reel, those are separate boxes. Does the facefreeze tool need to auto-pull boxes from the parent still job, or will Max re-draw on each video job?

---

## KEY PATHS, IDs, COMMANDS

### Files
| File | Purpose |
|------|---------|
| `C:\moma\sc10\shared_ui\popup.js` | MoMA popup frontend (facer UI + overlay logic) |
| `C:\moma\sc10\combo_runner\code\combo_gui.py` | MoMA backend (facer API endpoints at lines ~280-330) |
| `C:\moma\sc10\combo_runner\code\facefreeze.py` | Standalone freeze compositor (OpenCV, callable from CLI) |
| `C:\moma\sc10\combo_runner\code\moma_db.py` | Database connection helper |
| `C:\moma\sc10\combo_runner\code\audio_resolver.py` | Audio assembly / per-line duration logic |

### Database (D1: `moma-d1-dev`)
- **`face_boxes`** table: `job_id TEXT, person INTEGER, x INTEGER, y INTEGER, w INTEGER, h INTEGER`
- Query via MCP tool `mcp__fee7c39e-4816-4a04-b41f-7067182da1c3__d1_database_query`

### Spot 4 IDs
| Thing | Value |
|-------|-------|
| Scene/spot | scene 11, spot 4 (lines L10-L15) |
| Merge hash | `27a57cf7b2790b` |
| Still job | 3141, still v66 (`sc11_arr02_v66.png`) |
| Wan clip job | J3279 (`sc11_arr02_lipsie_v3279_wan26flau.mp4`) |
| Clip specs | 1176?784, 30fps, ~14s (actually 12.911s audio) |
| Face boxes | job 3141: person1(552,294,136,121), person2(482,248,103,124), person3(340,244,101,124), person4(204,238,97,123) |
| Speaker order | ANNA?DEREK?ANNA?DEREK?ANNA?WERNER |
| Box?character | 1=silent background woman, 2=WERNER (green officer), 3=DEREK (light shirt man), 4=ANNA (redhead in white, far right) |
| Test output | `...\combo_runner\data\facefreeze\sc11_spot4_facefreeze_v01.mp4` |

### Render commands used
```bash
cd C:\moma\sc10\combo_runner\code
python facefreeze.py --map "WERNER=2,DEREK=3,ANNA=4"
```
(Facefreeze.py has hardcoded paths to J3279 clip, v66 boxes, and the 6-line speaker timeline - will need parameterisation for other spots.)

### MoMA server
- Running on `localhost:8779`
- Auto-reloads `combo_gui.py` on change
- JS requires manual hard refresh (Ctrl+F5) in browser

---

## GOTCHAS & DEAD ENDS

1. **Browser caching**: after any `popup.js` change, user must Ctrl+F5. Server auto-reloads .py but the browser holds old JS.
2. **facer boxes are per-job**: still job 3141 has boxes. Video job J3279 is a different job_id with no boxes (unless drawn separately). The facefreeze tool currently hardcodes the still job's boxes.
3. **facer button visibility**: boxes only appear when the "facer" button is clicked (tool activates). They are NOT permanently overlaid on the image. This confused Max - he thought markup disappeared when viewing the reel/storyboard.
4. **Commit discipline**: facer was pushed directly to master. Adviser noted this. facefreeze was also pushed to master. Branch workflow agreed but not yet enacted.
5. **face_boxes table not in startup**: created manually via D1 query (`CREATE TABLE IF NOT EXISTS face_boxes (...)`). Not in the server's auto-create schema. A fresh deploy won't have it.
6. **Dead end - silent clip + lipsync overlay**: Max briefly considered making a silent clip where everyone moves but doesn't talk, then pasting only the speaker's lipsynced face. Rejected because "they should look at the one who speaks, not just sit and breathe."
7. **Dead end - gaze-direction prompting**: using facer boxes as "look-at targets" in Wan prompts per line. Rejected by Max in favour of the simpler freeze approach.
8. **Silence detection over-splits**: `ffmpeg silencedetect` broke Derek's long line into sub-segments at internal pauses. Solution: used exact per-line audio durations from the merge builder's concat logic instead.
9. **es.exe (Everything Search) not available**: tried to use it to find audio files, fell back to Python globs.
10. **Facer data actually never disappeared**: when Max said "markup disappeared," it was because he was looking at a different job (video reel vs still) and/or hadn't clicked the facer button to activate the overlay. Data was always in the database.
