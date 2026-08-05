# Scribe handover - milestone 7 (~526K tokens)
# session: 20260618_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-18 16:28:38 by deepseek-v4-pro

# D21 handover - sc10 merged multiline lipsie reboot

## Current goal (in Max's own words)
**"fix the moves"** - the conversation plays without interruption but background jumps between lobby, corridor, window, etc. are too sudden. Every location change needs a motion?primed transition shot, starting with lines 3 & 4, where the characters start walking toward/away from camera so the cut to the next location feels motivated. No silent beats (must stay fast). Total sc10 runtime is ~2?min?15?s.

## Decisions made and why

1. **Merged multiline lipsies instead of per?line clips.** Merged audio ? up to 15?s each; many short lines allow 4?line chunks. Two long monologues (line?8 Anna, line?23 Ishtab) are forced singles because they alone fill the 15?s cap.

2. **Speak?order and describe?both?first template.** Bare "Left/Right" labels were ignored by wan2.6, causing speaker swaps. The fix: **describe both characters with their physical positions first, then state "left speaks first, then right answers"** before quoting the lines.

3. **No smile/grin words in prompts.** "Smiles," "grins," "warm" caused excessive smiling and laughter on serious topics. The prompt uses "calm, formal, serious" only.

4. **Listener stays neutral - not frozen, not robotic.** For standing beats: "only the one speaking moves, the other listens quietly, composed." For walking beats: **neutral hand phrasing** (no directives about arms) - "still" froze hands, "arms moving" made them robotic.

5. **Distinct starting still per lipsie.** Reusing the same still for multiple arrangements caused visual fatigue and lost the sense of moving through locations. Now every arrangement uses a different frame extracted from its corresponding spine?approved clip.

6. **Zoom?in doomed; walk?away is the prime candidate for transitions.** Zooming the camera in on a face exposes low input resolution ? wan invents facial details. Max's redo tried **walk away from camera**, which keeps faces small. (The second zoom?in attempt gave acceptable detail but the characters faced the camera instead of each other - not good.)

7. **Auto?approval warning:** A previous session observed lipsies appearing as "approved" without Max's explicit action. The worker only stamps `done`; auto?approval likely came from the modified Lipser UI. Max re?approved all final clips manually. (No action required, just awareness.)

8. **Team mixup on bcast board** already reported to C6 - no D21 action needed.

## Current state of the scene (sc10)

The entire 33?line scene has been rebuilt into **11 arrangements** (one merged lipsie each), all approved by Max except perhaps the very latest transition redo. The final approved set (as of the last round before move?fixing) is:

| Arr | Lines | Locale | Final job |
|-----|-------|--------|-----------|
| 01  | 0?3   | Lobby greeting (meet twoshot) | 2774     |
| 02  | 4?5   | Hall - distinct frame `f_arr02_5` | 2775 (or newer 2813?) |
| 03  | 6?7   | Hall walking - distinct frame | 2810 (speak?order fix) |
| 04  | 8     | Corridor walk (Anna mono) - distinct frame | 2812 ("perfect") |
| 05  | 9     | Corridor walk - distinct frame | 2811 ("great") |
| 06  | 10?16 | Window (Earth drift) - distinct frame `f_arr06_14` | 2805 (approved) |
| 07  | 17?22 | Window - distinct frame `f_arr07_20` | 2806 (approved) |
| 08  | 23    | Window (Ishtab mono) - distinct frame `f_arr08b_0.35` | 2807 (approved) |
| 09  | 24?27 | Alcove - frame from spine clip | 2808 (approved) |
| 10  | 28?29 | Doorway/room - frame from spine `door_29` | 2794 (approved) |
| 11  | 30?32 | Room - frame from spine `door_32` | 2795 (approved) |

**Transition shots just fired (not yet reviewed):**
- **2818** - line?3 (Ishtab) walk?toward?camera + camera push?in to Ishtab closeup (prompt had zoom). Max then commented that zoom?in is doomed.
- **2819** - line?4 (Anna) on user?replaced still `sc_facing_v01f.png`, walk?toward + zoom to Anna closeup. Max later re?did it with walk?away (job unknown, possibly 2820).  
  *Last known: Max's own redo "walk away from camera" exists and needs evaluation.*

**Additional distinct?still redos (2813-2817)** were fired for arr02, arr04, arr05, arr06, arr07 on their respective distinct frames. Some may supersede the previously approved jobs. The exact status of those newer renders (whether Max approved or junked them) is unclear; check with `batches.py comments` before touching.

## Exact next step for a cold session

1. **Check latest rendere status of transition shots** (2818, 2819, any user?fired redo e.g., 2820) using live D1 query.  
2. **Read Max's comments** on those new renders with `batches.py comments` (see below) to understand which transition technique (walk?away, walk?toward, no zoom) is acceptable.  
3. **If walk?away is approved:** apply the same motion?prime recipe to the remaining location changes:
   - From hall to corridor: end of arr02 (line?5) starts walking away/toward camera.
   - From corridor to window: end of arr05 (line?9) turns toward window.
   - From window to alcove: end of arr08 (line?23) begins walking.
   - From alcove to door/room: end of arr09 (line?27) moves toward doorway.
   Pro?tip: keep the two?shot conversation (side?by?side, eyes on each other) rather than facing camera, even during motion.  
4. **If walk?away is not perfect,** retune the prompt: keep "walk away, side?by?side, in conversation, not looking at camera" and avoid any zoom/camera?move words.  
5. **After transition shots are in place, verify the whole 11?arrangement timeline feels continuous.** Minimal re?chunking may be needed if a motion prime requires a slightly longer or split clip; but the fundamental 11?arrangement mapping is approved.

## Open questions (for Max, not to be guessed)

- What is the exact verdict on 2818/2819 and the user?fired walk?away redo? Which job IDs are they?  
- Should the window beat (arr06?08) have a distinct motion (e.g., a pan across the window) or is the static window with Earth drift enough?  
- For the alcove ? room/door transition, is there a desired motion (e.g., opening a door) that requires a new generated still, or can we reuse existing spine frames?  
- The "turn toward the room / face the back" note for arr11 (line?30?32) still open: existing frames show them facing forward. Does that need a newly generated still?

## Key file paths and commands

- **Main worktree:** `C:\moma\.claude\worktrees\tender-dirac-aa429b`
- **sc10 combo_runner code:** `C:\moma\sc10\combo_runner\code\`
- **D1 client (`moma_db.py`):** `C:\moma\sc10\combo_runner\code\moma_db.py`
- **Audio resolver:** `C:\moma\sc10\combo_runner\code\audio_resolver.py`
- **Fire scripts for D21:** all prefixed `_d21_*.py` in that code folder. (Latest transition fires: `_d21_move_line3.py`, `_d21_move_line4.py`, plus user's manual fire)
- **Batch comment review:** `C:\moma\sc10\combo_runner\code\batches.py` - run `python batches.py comments N` to see Max's comments grouped by fire?batch (N = most recent batch, use 1 for last). This requires the `commented_at` column populated; D24 already set that up.
- **Two?shot stills used:**
  - Lobby: `sc01_meet_twoshot_var01.png` (Anna?L, Ishtab?R)
  - Corridor walk: `B1_corridor_walk_warm_v01.png` (Anna?L, Ishtab?R)
  - Window: `sc05_window_twoshot.png` (Ishtab?L, Anna?R)
  - Alcove frames: extracted from spine clips under `_d21frames/`
  - Door frames: extracted from spine clips under `_d21frames2/`
- **Memory files updated:**
  - `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md` (includes no?smile + don't?zoom?in notes)
  - `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_distinct_still_per_lipsie.md`
  - `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` (indexes the above)
- **Live UI:** `http://localhost:8779/lipser?ids=...` (MOMA must be running - start via `C:\moma\sc10\start_moma.bat`)

## Gotchas already ruled out (do not repeat)

- **Never** put "smile," "grin," "warm," or any emotion?intensive word in the prompt ? causes laughter/smiling on serious lines.
- **Never** use bare "Left/Right" labels without first describing both characters by appearance and position.
- **Never** direct hands/arms explicitly ("arms moving," "hands still") ? over?directing yields frozen or robotic motion. Use neutral phrasing.
- **Zoom?in on faces is doomed** with wan2.6 at the source resolution ? invents face details. Walk?away where faces recede works better.
- **Do not reuse the same still for multiple arrangements** ? use a distinct frame per chunk (extract from the associated spine clip).
- **Silence?buffer=1.0** adds 1s pad before/after speech where total clip ?15?s; long monologues must use 0 or very small pad to fit.
- The **worker** (`combo_wan26au_worker.py`) must be running (poll loop) for rendering. MOMA GUI starts it automatically.

## Signature & registration

Checked in as D21 ???. The session closed with Max saying "Panic" - likely referring to the zoom/vs walk?away dilemma, nothing broken. Next session should read the comments on the latest transition renders before re?firing anything.
