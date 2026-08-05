# Scribe handover - milestone 11 (~825K tokens)
# session: 20260618_priceless_bhabha_01109a_feeabb00
# cwd: C:\moma\.claude\worktrees\priceless-bhabha-01109a
# written: 2026-06-18 20:04:42 by deepseek-v4-pro

# HANDOVER - D25 (was D23, was D21 sc10 lipsie work)

## GOAL (Max's words)

Rebuild sc10 as **merged multiline lipsies** (~4 lines per clip), one per arrangement. Update the storyboard + player + renderer so the system natively supports these merged clips (each covers multiple script lines). Polish the storyboard UI (whole-scene default, white-circle ratings, job-id labels).

---

## WHAT WE ACTUALLY BUILT

### 1. sc10 - 11 merged multiline lipsies, all approved

The entire scene (33 lines) was rebuilt as merged lipsies. Each covers a natural beat, ranging from 1 line (forced by the 15s clip cap for long monologues) to 7 lines (short staccato dialogue). All 11 are approved by Max.

**Final job map (scene order):**

| arr | lines | job id | location/still |
|-----|-------|--------|----------------|
| 01 | 0-3 | 2774 | greeting hall (`sc01_meet_twoshot`) |
| 02 | 4-5 | 2775 | greeting hall |
| 03 | 6-7 | 2810 | walking corridor (`B1_corridor_walk_warm`) |
| 04 | 8 | 2812 | walking corridor (Anna monologue, 14s ? forced single) |
| 05 | 9 | 2811 | walking corridor |
| 06 | 10-16 | 2805 | window with Earth (`sc05_window_twoshot`) |
| 07 | 17-22 | 2806 | window |
| 08 | 23 | 2807 | window (Ishtab monologue, 13s ? forced single) |
| 09 | 24-27 | 2808 | alcove (frame extracted from approved spine clip) |
| 10 | 28-29 | 2794 | doorway/room (frame from spine) |
| 11 | 30-32 | 2795 | doorway/room |

Arr04 and arr08 are the only singles - they're 13-14s monologues that fill the 15s clip cap alone. Everything else is 2-7 lines.

**Full scene link:** `http://localhost:8779/lipser?ids=2774,2775,2810,2812,2811,2805,2806,2807,2808,2794,2795&title=sc10%20FINAL`

### 2. The prompt recipe that finally worked

Roughly $8-10 of fires to converge on this. Key lessons saved to memory files:

- **Describe-both-first + speak-ORDER:** "On the left, a young woman with long red hair... On the right, an older woman with long dark hair... Anna on the LEFT speaks first; then Ishtab on the RIGHT answers." Bare "Left/Right" labels are ignored by wan2.6 - explicit speak-order is what fixes the speaker swap.
- **NO smile/grin words** anywhere in the prompt. "Minimal grins" triggers excessive smiling ? laughing at serious topics. Use "calm, formal, serious, composed."
- **Walking shots need neutral hand phrasing.** "Only the speaker's lips move" froze Ishtab's hand mid-air unnaturally. "Arms moving naturally" produced robotic periodic motion. Neutral (don't direct hands at all) is the best lever.
- **Monologues:** only the one speaker's lips move; listener stays completely still.
- **"They keep looking at each other"** (not the camera) - in profile.
- **Each still must be different** per arrangement (not yet done - saved for next round).
- **1s silence pads** (`silence_buffer=1.0`) where they fit inside the 15s cap.

These rules saved in: `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md`, `feedback_distinct_still_per_lipsie.md`, `feedback_variation_not_verbatim.md`, `feedback_dont_block_poll.md`, and `MEMORY.md`.

### 3. System changes (pushed to master)

**Renderer (`render_mixboard_video_v01.py` - v09):**
- Collapses consecutive lines pinned to the same lipsie into ONE segment (since each merged clip carries its own multi-line audio).
- Commit df9d5f2 (v09).

**Storyboard (`storyboard_editor.html` - v45-49):**
- Lines sharing one merged lipsie collapse into **ONE row** - the clip tile shown once, all speaker lines stacked in the left column with separators.
- **Whole-scene is permanent default** (toggle button removed). No more per-arrangement filter hiding the scene.
- **2ND SPINE** filtered to exact same-combination takes only (match spine pick's `line_hash`). Shows approved AND done (not junk).
- 2ND SPINE take button shows **job id** (not "move to spine").
- Rating dots are **small white circles** (`?`), positioned off the LIP badge (spine tile: bottom-left; 2ND SPINE: top-left).

**Player (`mixboard.html` - v48):**
- Merged lipsie plays **once** (not N times for N lines). Real cause: the video-`ended` advance path still did `+1` per line; now skips consecutive same-clip lines. All 6 advance points patched.
- Next/Prev move clip-to-clip, not line-by-line.

**Slideshow server (`slideshow_server_v01.py`):**
- Serves `Cache-Control: no-cache, no-store, must-revalidate` on HTML/JS pages - edits surface instantly, no hard-refresh needed.
- `approved_images` endpoint now exposes `lip_rating` and `fit_rating`.

### 4. Spine population

The 11 merged lipsies are pinned to `line_current_clip` for all 33 lines (written directly to the DB, NOT via `/api/storyboard/assign` - that API overwrites `jobs.line_hash` which would corrupt the merged lipsies' synthetic hashes). Old sc10 spine backed up to `G:\My Drive\00Main2026\sc10_spine_backups\sc10_spine_backup_20260618_080616.json`.

---

## DECISIONS + WHY

- **Merged per-beat, not per-line:** Max's ask - "all 4 or so lines together in one actual scene." One lipsie per natural beat, each plays its own baked multi-line audio. Better flow than per-line clips.
- **Split at 15s clip cap:** wan2.6-i2v-flash max is ~15s. Two long monologues forced into singles (line 8 ?14s, line 23 ?13s). The rest comfortably fit 2-7 lines.
- **Pinned via direct DB write (not API):** The `/api/storyboard/assign` endpoint overwrites a job's `line_hash`. Merged lipsies carry synthetic hashes - overwriting them would break the spine-to-lipsie link. So `line_current_clip` was written directly.
- **Stills traced from spine, not invented:** For alcove/doorway beats where no standalone two-shot existed, frames were extracted from the already-approved spine clips. Those frames are the developed visuals.
- **Whole-scene default:** Max hated the per-arrangement toggle - it hid the scene. Toggle removed; storyboard always shows all merged rows.
- **Lane split:** After tripping over each other (3 sessions editing one file), lanes were assigned: D25 = player/render-server; D23/D24/D26 = storyboard pile/UI/data.

---

## CURRENT STATE

- **sc10 is complete and fully approved.** All 11 merged lipsies on master, spine populated, storyboard shows them grouped, player plays them correctly, assembly renders a clean 2:24 draft video.
- **D25 is idle.** Lane is player/render-server only. No storyboard edits (not our file). Session has been running 4-minute check-ins with nothing to do.
- **D24/D26** are doing pile cleanup (role-retag of images) and spine-UX work (sorting by spine assignment). Their lane, not ours.
- **Board** is the songs team (b15merger/b27/B26/B30, different repo) - unrelated to MOMA.

---

## EXACT NEXT STEP

**For a fresh session:** The sc10 work is done. The next actionable items (queued, NOT started) are:
1. **Next-round production polish** (distinct still per beat - every arrangement starts from a different image; arr11 faces turned toward the room; arr07 warmer Anna delivery).
2. **Canonical-hash backfill** - old takes (2761-2812) predate the d-team's `merge_hash` system and carry per-fire hashes. They need re-tagging to their beat's `merge_hash` so 2ND SPINE shows them grouped. **BUT** this is the d-team's domain (`fire_merge_lipsie.py`/`merge_ops.py` own the `merge_hash` scheme). Check with them first - they may have already done it.
3. **Scene-switch propagation to all tabs** (handed off to a fresh D23 on the d-team board, not yet completed).

---

## KEY PATHS / IDs

- **Worktree:** `C:\moma\.claude\worktrees\priceless-bhabha-01109a`
- **sc10 code:** `C:\moma\sc10\`
- **Player:** `sc10/sound_assembly/code/mixboard.html` (v48)
- **Storyboard:** `sc10/sound_assembly/code/storyboard_editor.html` (v49, owned by D23/D24/D26 - DO NOT EDIT)
- **Renderer:** `sc10/sound_assembly/code/render_mixboard_video_v01.py` (v09)
- **Slideshow server:** `sc10/sound_assembly/code/slideshow_server_v01.py`
- **MOMA combo_runner:** `sc10/combo_runner/code/`
- **Spine backup:** `G:\My Drive\00Main2026\sc10_spine_backups\`
- **Assembly video:** `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene10_20260618_081035.mp4`
- **DB:** D1Client in `sc10/combo_runner/code/moma_db.py`
- **Approved job IDs (all 11):** 2774, 2775, 2810, 2812, 2811, 2805, 2806, 2807, 2808, 2794, 2795
- **Two-shot stills:** `sc01_meet_twoshot_var01.png` (greeting, Anna-L/Ishtab-R); `B1_corridor_walk_warm_v01.png` (walking corridor); `sc05_window_twoshot.png` (window, Ishtab-L/Anna-R)
- **Frame-extracted stills for alcove/door:** `_d21frames/frame_alcove_27.png`, `frame_door_29.png`, `frame_door_32.png`
- **Memory files:** `C:\Users\maxre\.claude\projects\C--moma\memory\` (specifically `feedback_no_grin_smile_words.md`, `feedback_distinct_still_per_lipsie.md`, `MEMORY.md`)
- **Servers:** MOMA UI on 8779, slideshow on 8790
- **Broadcast board:** `python C:/claude_base/branch_bulletin/bcast.py read`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py read`

---

## GOTCHAS + DEAD ENDS

1. **DO NOT edit storyboard_editor.html** - D23/D24/D26 own it. This session's lane is player + render-server. Pull before touching anything (concurrent sessions).
2. **DO NOT use `/api/storyboard/assign`** for merged lipsies - it overwrites `jobs.line_hash`, breaking their synthetic shared hash.
3. **"Smiles," "grins," "warm"** in prompts cause wan2.6 to produce laughing/excessive smiling. Dead end. Use "calm, formal, serious, composed."
4. **Bare "Left"/"Right" labels are ignored** - wan2.6 can't reliably map L/R to who speaks. Must use explicit speak-order: "X on the left speaks first, then Y on the right answers."
5. **Directing hands in walk-and-talk** is a wan2.6 weak spot: "completely still" freezes the hand mid-air, "arms moving" produces robotic periodic motion. Neutral phrasing is best.
6. **Bracket/preceding dialogue text** scrambled speaker assignment (the model got confused by too many lines). Dead end - use speak-order instead.
7. **Arrangement filter hides the scene** - the old storyboard scoped to one arrangement beat. Fixed with whole-scene default. But if you see only one row, check `WHOLE_SCENE` in the JS.
8. **Context is ~93%** at handover time. Very high; keep lean.
