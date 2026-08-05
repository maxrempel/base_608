# Scribe handover - milestone 8 (~605K tokens)
# session: 20260619_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-19 13:23:31 by deepseek-v4-pro

# ? D21 HANDOVER - sc10 Merged Multiline Lipsies

---

## GOAL (Max's words)

Rebuild sc10 (Anna?Ishtab two-hander, 33 lines) so each arrangement is a **single multiline merged lipsie** - ideally ~4 lines per clip - instead of the old per-line lipsies. The conversation is a continuous pingpong walking a path: greeting ? corridor ? window ? corridor ? room. The merged clips must follow this path with **distinct background stills per arrangement** (no duplicates), proper speaker assignment (Anna left, Ishtab right except at the window where Ishtab is left), no excessive smiling/laughing, and motion-primed cuts where characters walk between locations.

---

## DECISIONS MADE + WHY

1. **Merged multiline (not per-line):** Group ~4 lines into one lipsie to reduce cuts and keep the conversation flowing. The old per-line approach produced too many micro-clips.

2. **11 arrangements covering all 33 lines:** Broke the scene at natural beat boundaries, forced by the **15-second hard cap** of the wan2.6 model. Two unavoidable singles: **arr04 (line 8, ~14s)** and **arr08 (line 23, ~13s)** - these monologues already nearly fill the 15s clip alone, so nothing else can ride along. Everything else is 2-7 lines.

3. **The prompt recipe that finally worked** (after many failed iterations):
   - **Describe-both-first:** Open by naming each character and their position ("On the left: a young woman with long red hair... On the right: an older woman...") - bare "Left/Right" labels are ignored by wan2.6.
   - **Speak-ORDER:** "The red-haired woman on the left speaks first; then the elder on the right answers" - this explicit ordering kills the speaker-swap bug.
   - **No smile/grin/laugh words anywhere.** Even "minimal grins" triggers excessive smiling. Tone = calm, formal, serious, composed throughout.
   - **Eyes on each other, never the camera.** "In profile, eyes locked on each other" - frontal stills create the "weather forecast" effect where they address the lens.
   - **Neutral hand phrasing for walking shots.** Directing hands ("arms moving" or "completely still") produces either robotic frozen poses or floating. Best is to say nothing about hands and let wan animate naturally.
   - **Monologues:** "Only one speaker's lips move; the listener stays silent and still."

4. **Walking transitions use walking-pose stills:** A static standing still animated as walking produces "floating" (feet don't plant). The fix is to start from a still where characters are **already mid-stride** (like the B1 corridor walk frame or the new J483 plate `sc_walk2_c2_pan_right`).

5. **Zoom-ins/push-ins abandoned for wan2.6:** The model invents face detail from low-res input ? made-up faces. Walk-away transitions are safer. Push-in combined with walk-toward-camera only works on high-res walking-pose stills (like 2821/2822), but it's fragile.

6. **Distinct still per lipsie (non-negotiable):** Every arrangement must start from a different image. The discovered duplicate was **arr03/04/05 all on B1_corridor_walk** (the B1 triplet). Redos 2830/2831/2832 fired to break this.

7. **Silence buffer = auto 1s pads** where they fit (silence_buffer=1.0). The two long monologues are too tight for pads inside 15s.

8. **Clipper tab removed from MOMA restart/refresh** (retired/hidden). Committed to master (`de86db2`).

---

## CURRENT STATE

### The 11 arrangements (all have approved versions):

| arr | lines | location | current approved job | distinct bg status |
|-----|-------|----------|----------------------|---------------------|
| 01 | 0-3 | greeting hall | 2774 | sc01_meet_twoshot ?unique |
| 02 | 4-5 | walking corridor | 2828 (or 2775) | J483 plate ?unique |
| 03 | 6-7 | corridor | 2810 | B1_corridor_walk ??shared |
| 04 | 8 | corridor (Anna mono) | 2812 | B1_corridor_walk ??shared |
| 05 | 9 | corridor | 2811 | B1_corridor_walk ??shared |
| 06 | 10-16 | window | 2829 (or 2805) | distinct window-A frame ? |
| 07 | 17-22 | window | 2817 | distinct window-B frame ? |
| 08 | 23 | window (Ishtab mono) | 2807 | sc05_window_twoshot ?unique |
| 09 | 24-27 | alcove | 2808 | frame from spine clip ?unique |
| 10 | 28-29 | doorway | 2794 | frame door_29 ?unique |
| 11 | 30-32 | room | 2795 | frame door_32 ??same as 2794 |

### Just fired (awaiting Max's review):
- **2830** - arr03 (6-7) on distinct hall bg
- **2831** - arr04 (8) on distinct corridor-A bg
- **2832** - arr05 (9) on distinct corridor-B bg
- **2829** - arr06 (10-16) Anna relaxed/not pushy (fixing 2816's "weird emotions")
- **2828** - arr02 (4+5) from J483 plate, walking

### Old versions kept as fallback (not junked):
2810, 2811, 2812, 2775, 2805, 2816

---

## EXACT NEXT STEP

Max's last words: *"the lipsies are pretty good, but every one has troubles. Read comments and reply with a plan."*

**Action:** Read all comments across the final 11 jobs (use `batches.py comments N` for recent ones, fall back to direct D1 query for older ones lacking `commented_at`). Identify every flagged issue, then reply with a **plan** - not firing anything until Max says go. The plan should address:

1. Which specific problems remain per arrangement (bg duplicates, speaker swaps, emotional tone, hand motion, camera-facing).
2. Which arrangements truly need a redo vs which are "good enough."
3. A budget-aware redo list (one shot per redo as Max stated).
4. The arr10/arr11 same-bg issue (both on door_pan_left frame - they look identical).
5. arr11's earlier "turn toward the room" note (can't be done by frame-grab; needs a freshly generated still).

---

## OPEN QUESTIONS (awaiting Max)

1. **arr11 (2795):** Should the room-arrival beat use a different bg (door_pan_right frame) so it doesn't look identical to arr10? And does the "turn toward the room / faces to the back" note still stand (requires a new still gen, not just a frame-grab)?

2. **arr02 (2828 vs 2775):** Does the J483 corridor plate walk work better than the older 2775 standing greeting? Max hasn't commented on 2828 yet.

3. **arr06 (2829):** Does "Anna relaxed" fix the pushy tone from 2816?

4. **Motion-prime transitions:** Max started experimenting with walk-toward-camera / zoom-ins for line 3 and line 4. The zoom-in work was mixed (2819 floated, 2821 looked great but they weren't walking). Is the motion-prime approach still wanted, or is distinct stills-per-beat with clean cuts the priority?

---

## KEY PATHS / IDs

- **Project root:** `C:\moma\sc10\combo_runner\code`
- **MOMA UI:** `http://localhost:8779` (lipser, imager, storyboard tabs)
- **Database:** D1 (query via `moma_db.D1Client`)
- **Comment reader:** `python batches.py comments N` (groups by fire-batch with 180s window)
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` and `read`
- **Audio resolver:** `audio_resolver.py` - `resolve_per_line_audio()` to merge line MP3s
- **Worker:** `combo_wan26au_worker.py` - poll-loop, stamps `done`, silence_buffer param
- **Key stills:**
  - `sc01_meet_twoshot_var01.png` - greeting hall (Anna-L, Ishtab-R)
  - `B1_corridor_walk_warm_v01.png` - corridor walking (Anna-L, Ishtab-R)
  - `sc05_window_twoshot.png` - window with Earth (Ishtab-L, Anna-R)
  - `sc_walk2_c2_pan_right_v01_A_v01.png` - J483 plate, newer corridor walk
  - Frame-grabbed stills in `_d21frames/` and `_d21frames2/`
- **Memory files:**
  - `feedback_no_grin_smile_words.md` (also records zoom-in/walk-away lesson, neutral hands)
  - `feedback_distinct_still_per_lipsie.md`
  - `feedback_only_max_approves.md` (observation = discuss only, fire only on explicit command)
  - `feedback_variation_not_verbatim.md`
  - `feedback_dont_block_poll.md`
- **MOMA restart/refresh:** `sc10/moma_restart.py` and `sc10/moma_refresh.py` (clipper removed, committed to master)
- **Session register:** D21 (signature ???)
- **Sibling sessions:** D13, D15, D16 (prior D-team); D22?D24 (b-team tamza songs/timecoder - unrelated, sharing bcast board)

---

## GOTCHAS

1. **wan2.6-i2v-flash model limits:**
   - Speaker assignment ignores bare Left/Right labels ? must use speak-ORDER phrasing.
   - Camera push-ins/zooms fabricate face detail ? avoid unless input has very high face resolution.
   - Walking animation from static standing stills = "floating" ? use mid-stride walking-pose stills.
   - Hand motion during walk-and-talk is fragile (frozen vs robotic) ? neutral phrasing, don't direct hands.
   - Smile/grin/laugh words trigger random laughter grins ? omit entirely from prompts.

2. **15-second hard cap** on all lipsie clips - this, not artistic choice, is why arr04 and arr08 are singles.

3. **Only Max approves.** Never set `output_status` to `approved` - the worker only ever writes `done`.

4. **Fire only on explicit command.** Observations/diagnoses = discuss, do not fire. Max was explicit about this after I wasted ~30c on 2821.

5. **Never fire Max's verbatim prompt without asking** (saved from earlier correction).

6. **prompt_extend is OFF** on the worker - no auto-beautify of prompts.

7. **Merged audio uses synthetic line-hashes** that don't match the sc10 script line table, so the lipsies don't show in the per-line spine view. Max said wiring them in isn't clearly needed - this is a known display quirk, not a bug.

8. **The bcast board has two unrelated projects interleaved** (D-team MOMA/sc10 + B-team tamza songs). C6 was notified; don't cross-interpret B-team posts as sc10 commands.
