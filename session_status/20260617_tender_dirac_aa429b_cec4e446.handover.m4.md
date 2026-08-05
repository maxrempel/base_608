# Scribe handover - milestone 4 (~302K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-17 21:25:27 by deepseek-v4-pro

# HANDOVER - D21: sc10 Arrangements, Merged Multiperson Lipsies

---

## GOAL (Max's words)

"Produce a lipsie" for each arrangement in sc10, merging ~4 lines per lipsie into ONE multiperson clip. The existing spine has per-line lipsies - the method changes to **merged multiline** using traceable location two-shots already in the system. Each prompt MUST include the actual lines labeled Left/Right.

---

## DECISIONS + WHY

1. **Merged multiline lipsie method**: Instead of per-line clips, merge consecutive lines' audio into one track (ffmpeg concat via pydub), fire as a single wan26flau lipsie. Audio ?15s to fit the model's clip cap.

2. **Approved arr01 prompt template (job 2774)** - "formal meeting of officials, keep looking at each other, minimal nods, minimal grins, royal postures" + four lines labeled Left: / Right: with quotation marks. This beat works because arr01 (lines 0-3) is in the greeting hall, static.

3. **"Smiles" and "warm" break the model**: wan2.6-i2v-flash turns positive emotion adjectives into bursts of laughter and random hamster-nodding. Dropped entirely.

4. **Lines MUST be in every prompt**: Max was explicit - every prompt includes the actual spoken lines, labeled Left/Right, in quotes. No exceptions.

5. **Bracket text (extra dialogue padding) scrambles speaker positions**: Tried on 2767/2768, model swapped Anna off the left. Abandoned.

6. **Location path exists in the spine**: Greeting hall ? corridor/window (Earth drifting) ? alcove ? doorway/room. Each beat's lines trace to a location-specific still. Using the wrong still (static greeting two-shot for walking beats) is what broke the first arr02-04 batch.

7. **Two behavioral rules saved to MEMORY.md**:
   - When Max asks for a "variation," do NOT re-fire his verbatim prompt - he already did that. Fire the variation only.
   - Do NOT block on polling renders. Fire and keep responding; let the detached worker render.

---

## CURRENT STATE

### ? DONE - arr01 (lines 0-3, "greeting")
- **Job 2774** APPROVED - the formal-officials template.
- Audio: merged 4-line track (hash d21e8...), ~14.75s.
- Still: `sc01_meet_twoshot_var01.png` - Anna LEFT (red hair, white cloak), Ishtab RIGHT (elder, red robes), in the domed meeting hall.
- Prompt (verbatim, the winner):
  ```
  The atmosphere is of a formal meeting of the officials.
  The speakers keep looking at each other.
  Left: "I am here as a historian from the Milky Way Alliance."
  Right: "Welcome, Anna."
  Left: "Thank you. My assignment is to witness preparations for the Contact."
  Right: "And you've arrived at exactly the right moment."
  Minimalistic nods. Royal postures. Minimal grins.
  ```

### ? IN FLIGHT - arr02 (lines 4-9, "turning point / babies")
- **Jobs 2775, 2776, 2777, 2778** were FIREd on the greeting two-shot.
- Lines 4-9 are in the **meeting hall** per spine trace, so the greeting two-shot MAY be correct for some sub-beats but the lines involve panning/moving (per prior per-line clips).
- **Status at session end**: 2775-2777 were rendered, 2778 rendering. Max flagged arr02 as showing "wrong input" - the still choice needs verification.
- These 4 clips are: [4+5], [6+7], [8], [9].

### ? IN FLIGHT - arr03 (lines 10-21, "they think they're alone / searching the sky")
- **Jobs 2785, 2786** FIREd on `sc05_window_twoshot.png` (window with Earth, Ishtab-L/Anna-R - positions REVERSED from greeting hall). Two merged clips: [10-16] and [17-21].
- At session end: rendering in detached worker.

### ? IN FLIGHT - arr04 (lines 22-29, corridor walk-and-talk)
- **Jobs 2787, 2788, 2789, 2790** FIREd on `B1_corridor_walk_warm_v01.png` (Anna-L/Ishtab-R walking toward camera). Four clips: [22], [23], [24-28], [29].
- 2787-2789 done, 2790 still rendering at session end.

### ?? JUNKED
- 2779-2784 (first arr03/04 batch on wrong greeting still).
- 2761-2773 (prompt experiments, smile disasters, bracket scrambles).

### ? REARRANGEMENT TALKED BUT NOT YET ACTED
Max wants the whole scene rearranged into ~4-line multiline lipsies. Later discussion produced this target structure (NOT yet fired except where overlaps exist):

| new arr | lines | location (from spine trace) | still needed |
|---|---|---|---|
| 02 | 4-5 | hall (`bg_meet`) | `sc01_meet_twoshot` |
| 03 | 6-7 | hall | `sc01_meet_twoshot` |
| 04 | 8 | hall?ship (Anna monologue) | `sc01_meet_twoshot` |
| 05 | 9-13 | ship view | ? |
| 06 | 14-20 | corridor+window | `sc05_window_twoshot` |
| 07 | 21-23 | corridor+window | `sc05_window_twoshot` |
| 08 | 24-27 | alcove (`fix_alcove`) | **NO character two-shot - extract frame from existing clip** |
| 09 | 28-29 | doorway | **extract frame from existing clip** |
| 10 | 30-32 | doorway/room | **extract frame from existing clip** |

### ?? STILL PALETTE (confirmed character two-shots)
- `sc01_meet_twoshot_var01.png` - hall, Anna-L/Ishtab-R, static greeting pose
- `sc05_window_twoshot.png` - window with Earth, **Ishtab-L/Anna-R** (positions reversed!)
- `B1_corridor_walk_warm_v01.png` - corridor, Anna-L/Ishtab-R, walking toward camera
- Alcove & doorway: **no character two-shot exists** - only empty backgrounds (`fix_alcove_color_v01.png`, `bg_door_pan_left_v01.png`). The plan was to extract a frame from an already-approved CLIP for those lines and use that as the wan26flau still input.

---

## EXACT NEXT STEPS

1. **Check render status** of the in-flight jobs:
   - 2778 (arr02 [9])
   - 2785, 2786 (arr03 [10-16], [17-21])
   - 2790 (arr04 [29])
   - Poll: `SELECT id, output_status FROM jobs WHERE id IN (2778, 2785, 2786, 2790)`

2. **Resolve arr02 (2775-2778)** - Max said "wrong input." Either:
   - Keep them if they're acceptable (hall location matches lines 4-9).
   - Or junk and re-fire with the formal-officials prompt template + correct still.

3. **Extract still frames for alcove and doorway beats**:
   - Trace lines 24-27 and 28-32 through the spine: `lipsie ? clip ? clip's source still`
   - Grab a middle frame from each existing approved clip for those lines (ffmpeg frame extraction) to serve as the merged lipsie's still input.

4. **Re-fire the full rearranged scene** using the locked formal-officials prompt template, with each chunk on its correct location two-shot, and every prompt containing the actual lines labeled Left/Right.

5. **Watch for the walked lipsie edge-case**: `B1_corridor_walk` is a walk-forward still - wan2.6 animating a walking still while lip-syncing is unproven and may need a dedicated test.

---

## OPEN QUESTIONS AWAITING MAX

- **arr02 (2775-2778)**: Keep or junk? The greeting two-shot MAY be correct for lines 4-9 since those are still in the hall per spine trace, but Max flagged "wrong input."
- **Ship-view beat (line 9)**: What still to use? No dedicated two-shot traced yet.
- **The walk-and-talk quality**: Does wan2.6 handle lip-sync on a walking-forward still acceptably?

---

## KEY PATHS, IDS, COMMANDS

**D1 DB**:
- `C:\moma\sc10\combo_runner\code\moma_db.py` - D1Client with `query_sql()`
- Arrangement containers: arr01/id2, arr02/id3, arr03/id4, arr04/id5, arr05/id7
- Script lines in `script_lines` and `vocal_lines` tables

**MOMA stack**:
- UI: `http://localhost:8779/lipser?ids=X,Y` - review lipsies
- Worker: `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` - poll loop
- Start: `C:\moma\sc10\start_moma.bat`
- Worker log: `C:\moma\sc10\combo_runner\data\_d21_wan26au.log`

**Stills (full paths)**:
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\approved_stills\sc01_meet_twoshot_var01.png`
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\sc05_window_twoshot.png`
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\B1_corridor_walk_warm_v01.png`

**Audio merge script (proven)**:
- `C:\moma\sc10\combo_runner\code\_merge_fire_exp.py` - reference for the merge logic
- `C:\moma\sc10\combo_runner\code\audio_resolver.py` - `resolve_per_line_audio()` needs `vocal_line` param

**Helper scripts written this session**:
- `C:\moma\sc10\combo_runner\code\_d21_probe*.py` - D1 queries
- `C:\moma\sc10\combo_runner\code\_d21_spine.py` - full spine ingest
- `C:\moma\sc10\combo_runner\code\_d21_arr234.py` - original 10-clip fire (partly junked)
- `C:\moma\sc10\combo_runner\code\_d21_pathfix.py` - location-corrected re-fire for arr03/04

**Memory files updated**:
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` - line 74ff has both rules

**Worklog**:
- `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` - D21 entries registered at turns ~28, 68, 113, 131, 144

---

## GOTCHAS & DEAD ENDS

1. **Smiles/warmth = model laughter**: wan2.6-i2v-flash with any positive emotion adjective produces stupid head-nodding and bursts of laughter. Dead approach. The winning prompt is "formal, minimal nods, minimal grins."

2. **Bracket text (extra dialogue) scrambles speaker L/R**: Writing lines beyond the actual audio confuses the model about who's on which side. Dead approach.

3. **"Listener frozen" wording doesn't work**: Both "the listener stays frozen / only speaker moves" and "locked-off" variants failed to kill the penguin-nodding at 15s clip length. The fix was the overall "formal officials, minimal nods" tone.

4. **Window two-shot has REVERSED positions**: `sc05_window_twoshot.png` = Ishtab on LEFT, Anna on RIGHT. Every prompt for that still must label lines with Ishtab-Left/Anna-Right, not the greeting-hall orientation.

5. **15s clip cap is hard**: The merged audio must be ?15s or wan26au clamps it. Long monologues (line 8 = 14s, line 23 = 13s) force single-line merges.

6. **Walk-and-talk is unproven**: `B1_corridor_walk_warm` shows characters walking forward - wan2.6 may animate the walk oddly while lip-syncing. Unknown.

7. **Alcove and doorway have NO character two-shot**: Only empty backgrounds exist. The plan is to extract a middle frame from an existing approved CLIP for those lines as the merged lipsie's still - this is a frame-extraction step, not a generation step.
