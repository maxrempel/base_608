# Scribe handover - milestone 5 (~400K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-17 23:35:11 by deepseek-v4-pro

# D21 Handover - sc10 Rearrangement into Merged Multiline Lipsies

## GOAL (Max's words)
Take sc10 - a 33-line Anna?Ishtab two-hander scene - and reorganize it from per-line lipsies into ~4-line merged multiline arrangements. Each arrangement becomes ONE multiperson lipsie fired off a two-shot still. The scene moves along a developed path (greeting hall ? corridor walk ? window ? alcove ? doorway/room), so each beat must use the correct location still, not a single static image.

## DECISIONS MADE + WHY

**Prompt template evolved through many failed iterations:**
- **Must include every spoken line in the prompt.** Non-negotiable from Max.
- **Lines in quotation marks, labeled by speaker.** Bare "Left/Right" labels are ignored by wan2.6 - instead, describe both characters by appearance and position first ("On the left: a young woman with long red hair... On the right: an older woman with long dark hair, red robes, jade beads..."), then the quoted lines.
- **Zero smile/grin words allowed.** "Smiles," "warm," "minimal grins" all trigger idiotic laughing, random bursts of mirth, or excessive smiling after lines end. The word "grins" specifically causes smiling even at "minimal." Removed entirely.
- **Characters stay in profile, eyes locked on each other, never at the camera.** The model drifts gaze to camera otherwise (looks like they're addressing a third party).
- **Only the speaker's lips move; the listener stays frozen.** Without this, the listener penguin-nods along. For monologues (lines 8, 23), only ONE speaker appears to move at all.
- **"Formal meeting of officials" tone** - minimal nods, royal upright posture, calm, composed, serious. No laughing at serious topics.
- **Describe-both-first** was the breakthrough fix for the speaker-swap problem (2793 alcove had Anna and Ishtab swapped).

**Location/path decisions:**
- arr01 (0-3) = greeting hall, static two-shot (`sc01_meet_twoshot`, Anna-L/Ishtab-R). Approved.
- Post-greeting beats (lines 4-9) must be **walking the corridor** (`B1_corridor_walk_warm`, Anna-L/Ishtab-R), NOT standing at the entrance. Max's comment on 2777: "they must be walking - why are they still standing at the entrance?"
- Window beats (lines 10-23) use `sc05_window_twoshot` (Ishtab-L/Anna-R - positions FLIPPED from greeting). Earth drifts past outside.
- Alcove (24-27) and doorway/room (28-32) had no standalone two-shot stills - solved by extracting frames from the already-approved spine lipsies, which show Anna-L/Ishtab-R throughout.

**15s clip cap forces two singles:**
- Line 8 (Anna monologue, ~14s) and line 23 (Ishtab monologue, ~13s) each nearly fill the 15s cap alone. They cannot merge with neighbors. This is a hard wan2.6 limit, not a choice.

**Silence pads:**
- Max asked for ~1s pads before/after speech. Set `silence_buffer=1.0` everywhere it fits within 15s. The two long monologues can't take full 1s pads.

**Behavioral rules saved for all sessions:**
- Never fire Max's prompt verbatim unless he explicitly says so. He asked for a "variation" once and got verbatim - wasted $0.30.
- Don't block on polling lipsie renders. Fire and stay responsive; use `ScheduleWakeup` to check back.
- No smile/grin words in any prompt, ever.

**Approved clips kept untouched during re-rolls.** When redoing with the final recipe, the 6 Max-approved jobs (2774, 2775, 2777, 2778, 2794, 2795) were preserved - only unapproved ones refired.

## CURRENT STATE

**Max's last action:** He commented, junked, or approved all done lipsies in MOMA. He reports some arrangements now show nothing - likely because the arrangement containers in MOMA's DB still reflect the old per-line structure, while clips were junked/regrouped under the new merged arrangement scheme. The arrangement?job mapping probably wasn't propagated back to MOMA's arrangements table.

**The final batch (2802-2808) was fired** with the consolidated recipe:
- 2802: arr03 (lines 6-7), walking corridor B1
- 2803: arr04 (line 8), walking version (alternative to approved 2777 standing)
- 2804: arr05 (line 9), walking version (alternative to approved 2778 standing)
- 2805: arr06 (lines 10-16), window
- 2806: arr07 (lines 17-22), window - orphan line 22 merged in
- 2807: arr08 (line 23), window, Ishtab monologue, one speaker only
- 2808: arr09 (lines 24-27), alcove frame, describe-both-first

Verification of whether 2802-2808 all rendered successfully was pending at transcript end (timer was armed).

**Approved (6 clips, do not touch):**
| Job | Arr | Lines | Location |
|-----|-----|-------|----------|
| 2774 | arr01 | 0-3 | greeting hall |
| 2775 | arr02 | 4-5 | hall (Max: "best one, smiles appropriate") |
| 2777 | arr04 | 8 | hall standing (Anna monologue) |
| 2778 | arr05 | 9 | hall standing |
| 2794 | arr10 | 28-29 | doorway |
| 2795 | arr11 | 30-32 | room |

**Redos/awaiting review (7 clips):** 2802-2808 as above. Plus walking alternatives 2803/2804 compete with 2777/2778.

## EXACT NEXT STEP

1. **Check render status** of 2802-2808. Any that errored need refire.
2. **Read Max's latest comments** on those jobs in MOMA - he said he commented/junked/approved all done ones.
3. **Fix the MOMA arrangement mapping.** The root of "some arrangements show nothing" is that the arrangement containers (arr02-arr11 in the `arrangements` table, IDs 3-7) still point to old per-line clips that were junked. Need to update each arrangement's associated jobs to the new merged lipsie IDs.
4. **Resolve the standing vs. walking duplicates** for arr04 and arr05 - Max approved 2777/2778 (standing) but also wanted walking; the walking redos 2803/2804 give him the choice.
5. **arr10/arr11 same-bg issue** still open - both use `door_pan_left` frame; Max may want arr11 on a different angle.

## OPEN QUESTIONS AWAITING MAX

- Did 2802-2808 all render? Any errors?
- For arr04 (line 8) and arr05 (line 9): keep the approved standing versions (2777, 2778) or switch to the walking redos (2803, 2804)?
- Do arr10 and arr11 need distinct backgrounds? (Both currently use the same `door_pan_left` frame.)
- Should the describe-both-first template be rolled backward to the approved clips (2774, 2775, etc.) for consistency, or leave them as-is?

## KEY PATHS, IDS, COMMANDS

**DB & scripts:**
- MOMA DB: `C:\moma\sc10\combo_runner\code\moma_db.py` (D1Client, method: `query_sql`)
- Worker: `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` (model: wan2.6-i2v-flash, prompt_extend=off)
- UI: `http://localhost:8779/lipser?ids=X,Y&title=...`
- MOMA stack launched via: `C:\moma\sc10\start_moma.bat` (port 8779)

**Stills (two-shots, Anna+Ishtab):**
- Greeting hall: `.../data/output_stills/sc01_meet_twoshot_var01.png` - Anna LEFT, Ishtab RIGHT
- Corridor walk: `.../data/output_stills/B1_corridor_walk_warm_v01.png` - Anna LEFT, Ishtab RIGHT
- Window: `.../data/output_stills/sc05_window_twoshot.png` - Ishtab LEFT, Anna RIGHT (FLIPPED)
- Alcove frame: `.../data/output_stills/_d21frames/frame_alcove_27.png` - Anna LEFT, Ishtab RIGHT
- Door frames: `.../data/output_stills/_d21frames/frame_door_29.png` and `frame_door_32.png` - Anna LEFT, Ishtab RIGHT

**Key scripts from this session:**
- `_d21_final.py` - fired the last redo batch 2802-2808
- `_d21_test3.py` - fired 3 test clips (2798-2800) with describe-both-first
- `_d21_phase1.py` / `_d21_phase2.py` - fired window and alcove/door chunks
- `_d21_spine.py` - ingested the full spine (lipsie?clip?still chain)
- `_d21_probe.py` / `_d21_probe2.py` / `_d21_probe3.py` - DB exploration
- `_d21_audit.py` - QC audit of all fired jobs

**Merged audio:** Single merged track (hash `d21e8...`) used throughout all arr01 attempts - Anna lines on even indices, Ishtab on odd, ~14.75s total for the 4-line greeting.

**Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` - D21 entries logged throughout.

**Memory files updated:**
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`

## GOTCHAS

1. **wan2.6 ignores bare "Left/Right" labels.** Must describe both characters by appearance + position first, then give quoted lines.
2. **"Smile," "grin," "warm" are poison words.** Even "minimal grins" triggers excessive smiling/laughing. Strip them completely.
3. **The greeting two-shot and window two-shot have FLIPPED character positions.** Anna is LEFT in greeting/corridor/alcove/door, but Ishtab is LEFT in the window still. Prompts must flip labels per location.
4. **The 15s clip cap is absolute.** Two monologues (line 8 ~14s, line 23 ~13s) force single-line arrangements.
5. **MOMA arrangements table must be updated** when clips are regrouped, or arrangements show empty.
6. **Never fire Max's verbatim prompt** unless he explicitly asks. He once said "make a variation" and got his own prompt re-fired - wasted $0.30.
7. **Don't block polling renders.** Fire, set ScheduleWakeup, stay responsive.
8. **The frame-extract method works** for locations without a standalone two-shot still - pull a mid-frame from the approved spine lipsie and feed it as the wan26flau input still.
9. **Post-greeting beats must use the walking corridor still** (`B1_corridor_walk_warm`), not the static greeting two-shot. Max was explicit: "they must be walking."
10. **Prompt text doesn't make them say words** - the audio track controls speech. The prompt only
