# Scribe handover - milestone 10 (~153K tokens)
# session: 20260608_funny_booth_2ece92_7faee3c9
# cwd: C:\moma\.claude\worktrees\funny-booth-2ece92
# written: 2026-06-08 11:59:42 by claude-opus-4-8

# HANDOVER - MOMA Line-Merge Feature

## GOAL (in Max's words)
"Implement line combining into a single lispie." The discovery driving this: **wan26flash can alternate speakers** - you put the speaker-alternation in the description and it actually lipsyncs turn-taking. Max: "let's assume we can make scenes with unlimited number of lines, normally 2-6 where two or more speakers are speaking in turn. Wow. That's a great improvement."

So MOMA needs a "full cycle rework" to allow merging dialogue lines: Max will issue a command to any session ("merge lines blabla, like 2, 3, 4"), and the system must collapse those lines into ONE mp3 ? ONE lipsie ? ONE slot in the storyboard.

**The deepest requirement (Max's real ask):** "make sure that sessions which skip instructions are forced to do the proper format programmatically, not only by a command in memory. Need a programmatic control over sloppiness of llm." The Notion script is edited largely by hand (maybe with a script template), but everything downstream must be enforced by code, not by trusting the LLM to follow instructions.

## DECISIONS + WHY

1. **Merge mark in Notion = paired text tags `[[MERGE]]` ... `[[/MERGE]]`** wrapping the run of lines.
   - Scribe pushed back twice (paired tags break silently if you forget the close; suggested Notion callout blocks, then per-line `[[merge1]]` numbered markers).
   - Max rejected callouts and numbered markers ("inflexible... future sessions would get confused") and explicitly chose the original block tags: **"Lets use your initial solution. The cost of error is little. Not a big deal."** - LOCKED.

2. **No re-sass.** Merge grabs the EXISTING per-line MP3 intermediates and concatenates them into the merged MP3. Reason: merges happen mid-editing; don't re-run sass on everything, just "grab intermediates and merge them." Production is top-down; "we don't care what was before."

3. **Merged unit gets its own single identity, remembers its member lines** - so it takes ONE sb slot and ONE lipsie, and libup can collapse the old individual rows. Member lines are dropped/replaced after merge.

4. **Freed media (images/lipsies of merged-away lines) ? the "second spine."** Not deleted - preserved for reuse.

5. **Naming:** the merged file is named like `lines2-4`.

6. **Deferred:** (a) pause adjustment between lines inside a merge - "note for later"; (b) the firing/optimization of the actual wan26flash call - "firing comes later," to be manually optimized then implemented.

## "SECOND SPINE" - Max's term, now in the dictionary
Max uses his own name "spine" and complained that opus sessions forget it. Investigation findings:
- The sb has two parallel per-line tracks. Initial guess was `line_current_clip` (talking-video/lipsie pick) vs `line_current_still` (still-image pick), with second spine = the still lane.
- **Max corrected this:** the second spine "can hold images AND lipsies and several of them" - so it is NOT the one-per-line `line_current_still`.
- Pinned in code (from reading the full storyboard render) to the **per-line DUPS lane** - the alternates area beside each line's main pick.
- **CAVEAT recorded:** the dups lane currently shows lipsies only; merge work must widen it to hold images too.
- Max only knows the visible part: "i know only the visible part and i don't do inner shit." He'll point at the lane on screen during implementation; tracing it to the D1 table is the assistant's job, NOT Max's.

## TEAM SPLIT (latest structural change - important)
Max split this work into a "team of equals" experiment on the bcast board:
- **D1** = propagation of the Notion line-merge into sb (the transformation: sass / libup / Notion?sb). D1 already posted a clean contract and added code insertion points.
- **D2 = THIS SESSION = firing.** Owns the wan26flash fire path only.

## FIRING - KEY FIND (D2's main result so far)
**The firing is already a SOLVED problem.** The wan26flau doc records a proven two-person merged-audio lipsie: **job 2713, dated 2026-06-03**, Max's verdict "it worked perfectly." Recipe: wan26flash lipsyncs turn-taking from ONE concatenated MP3 plus a prompt stating who speaks first/second and their left/right screen position. So D2's job is NOT to invent firing - it's to turn that working hack into a clean, reusable "merged-audio lipsie" fire path.

## CURRENT STATE (all committed + pushed)
- **Dictionary** updated with Max's terms (Spine, Second spine, Merge) - second spine defined his way (parallel lane holding several images AND lipsies). Committed in `C:\claude_base`.
- **Spec memo** written and committed in moma master, capturing the full transformation: `[[MERGE]]` block, concatenate intermediates (no re-sass), `lines2-4` naming, merged unit with own identity remembering members, libup collapses, freed media ? second spine, second-spine pinned to dups lane (with the "lipsies-only, must widen to images" caveat), pause-adjust + firing marked deferred.
- D2 has posted ACK + firing plan to the bcast board and saved status reports.
- An autonomous 4-min wake timer was armed (Max: "Set up 4 min wake up timer and if i don't answer and if safe, continue").

## EXACT NEXT STEP
This is an autonomous loop tick. As D2 (firing), continue safely without Max:
1. Re-read the bcast board for any new posts from D1; ACK/coordinate as needed.
2. Advance the firing design - draft the clean "merged-audio lipsie" fire path based on the proven job-2713 recipe (design/document only).
3. **Do NOT** run live edits to TTS or DB-remap scripts, and do NOT build the firing helper, while Max is away - his doc says ask first; this needs his `doit22`.
4. **Reschedule the loop:** call ScheduleWakeup with `prompt` = literal `<<autonomous-loop-dynamic>>`. If a Monitor is armed (check TaskList), keep `delaySeconds` 1200-1800s.

## OPEN QUESTIONS (awaiting Max)
1. **Left/right speaker position for the shared still.** When 2 speakers share one still, the prompt must say who's on the left vs right ("man on right speaks first"). That L/R info is stored NOWHERE today. Does it come from the still, or will Max tell it per-fire? - UNANSWERED.
2. **One wan26flash call or something else** for the merged lipsie (one still showing both speakers + merged audio + "speakers alternate")? Raised but deferred by Max ("firing comes later").
3. The exact D1 storage table behind the second spine - deliberately not guessed; Max will point at the lane on screen during implementation.

## KEY PATHS / IDS / NAMES
- Spec memo: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md`
- Storyboard UI: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- Dictionary: `C:\claude_base\user_dictionary_tomemex.md`
- Firing doc (proven recipe): `C:\Users\maxre\.claude\projects\C--moma\memory\project_wan26flau_lane.md`
- bcast board: `C:\claude_base\branch_bulletin\bcast.py` (whoami / catchup / post)
- Status script: `C:\claude_base\compaction_kb\scripts\session_status.py`
- cwd / worktree: `C:\moma\.claude\worktrees\funny-booth-2ece92`
- Per-line sb tracks: `line_current_clip` (lipsie pick), `line_current_still` (still pick)
- Worker: `combo_wan26au_worker`; tool name `wan26flau` (= wan2.6-i2v-flash); proven job **2713** (2026-06-03)
- Gate command from Max before any live build: **`doit22`**

## GOTCHAS / DEAD ENDS RULED OUT
- Do NOT use Notion callout blocks or numbered `[[merge1]]` markers - Max rejected both. The decision is plain `[[MERGE]]`/`[[/MERGE]]`.
- Do NOT re-sass on merge - concatenate existing intermediates only.
- Second spine is NOT `line_current_still`; it's the per-line DUPS/alternates lane (currently lipsies-only, must be widened to images).
- Don't ask Max about inner tables/storage - he only handles the visible UI.
- The b/c-teams on the bcast board are a DIFFERENT project (tamza catalog) - ignore them; our team is D1/D2.
- Firing is already proven - don't waste effort re-inventing it; the job is to make it clean/reusable.
- No live TTS/DB-remap edits and no helper-building while Max is away - wait for `doit22`.
