# Scribe handover - milestone 9 (~685K tokens)
# session: 20260618_priceless_bhabha_01109a_feeabb00
# cwd: C:\moma\.claude\worktrees\priceless-bhabha-01109a
# written: 2026-06-18 16:07:46 by deepseek-v4-pro

# HANDOVER - sc10 Merged Multiline Lipsies (D21 ? D23)

## GOAL (Max's words)
Rebuild sc10 into ~4-line **merged multiline lipsies** (one clip per conversational beat, not per-line), arranged by location along the developed path (greeting ? corridor walk ? window ? alcove ? doorway/room). Then update the system (storyboard, player, renderer) to display/play the new merged arrangement properly. Refine storyboard styling (grouped rows, 2ND SPINE filtering, stars). Current final ask: **"remove stupid label 'move to spine' on a lispie in 2nd spine and add an id."**

---

## CURRENT STATE - WHAT IS DONE

### sc10 Scene: 11 Merged Lipsies, All Approved
All 33 script lines are covered by 11 merged multiline clips, each using a location-appropriate still and the locked "formal officials" template:

| Arr | Lines | Job ID | Location/Still | Status |
|-----|-------|--------|----------------|--------|
| 01 | 0-3 | **2774** | greeting ? `sc01_meet_twoshot` | approved |
| 02 | 4-5 | **2775** | hall ? `sc01_meet_twoshot` | approved |
| 03 | 6-7 | **2810** | walking corridor ? `B1_corridor_walk_warm` | approved ("excellent") |
| 04 | 8 | **2812** | walking corridor (Anna monologue) | approved ("perfect") |
| 05 | 9 | **2811** | walking corridor | approved ("great") |
| 06 | 10-16 | **2805** | window ? `sc05_window_twoshot` | approved |
| 07 | 17-22 | **2806** | window | approved |
| 08 | 23 | **2807** | window (Ishtab monologue) | approved ("good") |
| 09 | 24-27 | **2808** | alcove ? frame from spine | approved ("good") |
| 10 | 28-29 | **2794** | doorway ? frame from spine | approved |
| 11 | 30-32 | **2795** | room ? frame from spine | approved |

### System Updates (all pushed to master)
1. **Renderer** (v09, `render_mixboard_video_v01.py`) - collapses consecutive same-lipsie lines into one segment. Assembly video `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4` (2:24, draft).
2. **Storyboard** (v49) - groups merged lipsies into one row with stacked speaker lines; "Whole Scene" toggle; top-left alignment; darker/thicker dividers; 2ND SPINE filtered to same-`line_hash` only; star ratings as small white circles (?).
3. **Player** (v48, `mixboard.html`) - steps by distinct clip (not by line), so merged lipsies play once. All advance paths patched (video end, b-roll timeout, audio, Next, Prev).
4. **Server** (`slideshow_server_v01.py`) - sends `Cache-Control: no-cache, no-store, must-revalidate` on HTML pages; serves `lip_rating`/`fit_rating` in approved_images.
5. **Spine** - all 33 lines pinned directly to their merged lipsie jobs (via `line_current_clip`, NOT the assign API - that would corrupt synthetic hashes).
6. **Backup** - old sc10 spine saved to `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json`.

### Recipe That Cracks Merged Lipsies (Locked)
- **Describe both characters + positions first** (not bare "Left/Right" labels - wan ignores those).
- **Speak-order phrasing** ("left speaks first, then right answers") fixes the speaker-swap.
- **Neutral hand phrasing** for walking shots (directing arms causes frozen or robotic hands).
- **No smile/grin/laugh words** - wan turns them into random laughter.
- **"Composed throughout"** - keeps expression even after the line ends.
- **Monologues** - only the speaker's lips move.
- **Dialogue** - listener stays attentive but not frozen; "eyes on each other, never the camera."
- 1s silence pads where the 15s cap allows.

---

## EXACT NEXT STEP

**Remove the "move to spine" label from 2ND SPINE lipsies and add a job ID instead.** This is a storyboard_editor.html change. The 2ND SPINE tile rendering is in the loop that builds `.dup-thumb` elements - find where it renders any "move to spine" text/badge and replace it with the job ID number.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Canonical hash migration** - all takes of the same line-combination share a canonical hash so they group in the 2ND SPINE for star-comparison. Worth doing?
2. **Distinct still per arrangement** - next round must start each lipsie from a different image (different corridor framing, different window angle, etc.), not reuse one still per location.
3. **Production polish:** arr11 (2795) should face the room; arr07 (2806) needs warmer Anna delivery; arr02 (2775) has a last-half-second smile tail.
4. **Stars on spine tile** - done (white circles, bottom-left). Confirm they look right.

---

## KEY FILES & PATHS

| File | Purpose |
|------|---------|
| `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` | Storyboard UI (v49) - **the file to edit next** |
| `C:\moma\sc10\sound_assembly\code\mixboard.html` | Player (v48) |
| `C:\moma\sc10\sound_assembly\code\render_mixboard_video_v01.py` | Offline renderer (v09) |
| `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` | Server (port 8790) - serves no-cache, lip_rating |
| `C:\moma\sc10\combo_runner\code\moma_db.py` | D1Client DB access |
| `G:\My Drive\00Main2026\sc10_spine_backups\` | Old spine backup |
| `C:\Users\maxre\.claude\projects\C--moma\memory\` | Saved rules (no_grin_smile, distinct_still, variation_not_verbatim, dont_block_poll) |
| `http://localhost:8790/storyboard` | Storyboard URL |
| `http://localhost:8779/lipser` | Lipser URL |

### Key Job IDs
The 11 final merged lipsies: **2774, 2775, 2810, 2812, 2811, 2805, 2806, 2807, 2808, 2794, 2795**

### Key Stills
- `sc01_meet_twoshot_var01.png` - greeting/hall (Anna-L, Ishtab-R)
- `B1_corridor_walk_warm_v01.png` - corridor walk (Anna-L, Ishtab-R, walking toward camera)
- `sc05_window_twoshot.png` - window with Earth (Ishtab-L, Anna-R)
- `_d21frames/frame_alcove_27.png` - alcove two-shot (extracted from spine)
- `_d21frames/frame_door_29.png`, `frame_door_32.png` - doorway/room (extracted from spine)

---

## GOTCHAS & DEAD ENDS RULED OUT

1. **wan ignores "Left/Right" labels** - must describe characters and positions first, then use speak-order phrasing.
2. **"Smiles/grins/warm" words cause laughter** - even "minimal grins" triggers it. Ruled out permanently. Rule saved.
3. **"Completely still" listener freezes hands mid-air** on walking shots - ruled out. Neutral phrasing only.
4. **Directed hand motion becomes robotic** - wan2.6's weak spot. Neutral phrasing is the best lever.
5. **Bracket text (extra dialogue in prompt) scrambles speaker positions** - ruled out. Keep only the actual lines.
6. **Merged lipsie pinned to N lines replays N times** - the video-`ended` advance path (not audio) is what fires; all paths now patched to step by distinct clip.
7. **Old 2ND SPINE showed "parts"** (per-line lipsies that don't match the merged combination) - fixed by filtering to same `line_hash`.
8. **Storyboard only showed one arrangement** - the arrangement filter was scoped to one beat. "Whole Scene" toggle bypasses it.
9. **Stars covered by LIP badge** - repositioned: spine tile bottom-left, 2ND SPINE top-left.
10. **Never re-fire Max's prompt verbatim** - he said "make a variation," not "run my exact prompt." Rule saved.
11. **Never block on poll** - fire and stay responsive; the detached worker renders.

---

## SCRATCH SCRIPTS
Archived to `C:\moma\sc10\combo_runner\code\_d2x_scratch_archive\` - all `_d21_*.py` and `_d23_*.py` files.
