# Scribe handover - milestone 8 (~127K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# cwd: C:\moma\.claude\worktrees\strange-hawking-e9654d
# written: 2026-06-08 11:42:38 by claude-opus-4-8

# HANDOVER - moma line-merging feature

## GOAL (in Max's words)
"Implement line combining into a single lispie." The discovery: WAN26flash can alternate speakers - you put it in the description and it actually alternates the speakers in one clip. So scenes can now have multiple lines (normally 2-6) where two or more speakers speak in turn, all becoming ONE merged unit. Max wants "a full cycle rework of the moma system to allow for merging of lines."

The merge is triggered by Max's command to any session - "merge lines 2, 3, 4" etc. The deep requirement, in his words: "make sure that sessions which skip instructions are forced to do the proper format programmatically, not only by a command in memory. Need a programmatic control over sloppiness of llm." The Notion script must be formally perfect (edited largely by hand, maybe with a script template), and everything downstream propagates programmatically so sloppy sessions can't break format.

This chat OWNS the transformation. The "firing" (how the merged lipsie gets generated) is being done by Max manually in another chat and is OUT OF SCOPE here.

## DECISIONS + WHY

**1. Merge mark = `[[MERGE]]` ... `[[/MERGE]]` paired block in Notion.**
We explored alternatives and Max chose this deliberately. Per-line `[[merged]]` markers and numbered `[[merge1]]` versions were rejected as "inflexible." A Notion native callout box was proposed but not chosen. Max's reasoning: "The cost of error is little. Not a big deal." Paired tags have a known weakness (forget/typo the closing tag and parse breaks silently) - Max accepted this consciously.

**2. No re-sass. Grab intermediates and concatenate.**
Crucial: merges happen in the MIDDLE of editing. So we do NOT re-run sass on everything. We merge in Notion, then grab the already-existing per-line MP3 intermediates and concatenate them into the merged MP3. Then propagate down, dropping the replaced individual lines.

**3. Naming = `lines2-4` style** (e.g. `lines2-4.mp3`), reflecting the member line range.

**4. Merged unit has its own single identity, remembering its member lines.**
Originally proposed as merge_hash of (scene | member texts). BUT Max corrected the direction: "we don't care what was before. If we merge - we produce top to down." So it's a top-down produce, not a remap-from-history. The merged unit takes ONE slot in sb and ONE lipsie; libup collapses the old individual rows into the one merged row.

**5. Freed media goes to the SECOND SPINE.**
When N lines collapse to 1, their images/lipsies are not deleted - they move to the second spine. This is Max's own named concept (see dictionary below).

**6. Deferred / out of scope (noted for later):**
- Pause-between-lines adjustment within a merge - "one more funny request... note for later."
- The firing (which still goes in + the "speakers alternate" description for WAN26flash) - Max does this manually in another chat first, then we implement.

## CURRENT STATE
Design dialogue complete and the agreed transformation is recorded durably.

**Committed + pushed:**
- User dictionary updated with Max's term "second spine" (and Spine, Merge) - at `C:\claude_base\user_dictionary_tomemex.md`.
- Merge spec memo written at `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md` capturing: `[[MERGE]]` block, concatenate intermediates (no re-sass), `lines2-4` naming, merged unit with own identity, libup collapse, freed media to second spine, pause-adjust + firing marked deferred.

No implementation code written yet. We are at design-locked, ready-to-build.

## EXACT NEXT STEP
Wait for Max. He said: "Let's finish the transformation already planned. Then we will manually optimize the firing and then we will implement it." The transformation design is now finished and recorded. The sequence is: (1) firing optimized manually by Max in other chat ? (2) THEN implement. Implementation here happens via `doit22` when Max gives the word. Do not start coding unsolicited.

## OPEN QUESTIONS (awaiting Max)
1. **The exact storage behind the second spine** - which D1 table/structure actually holds it. I deliberately did NOT guess a D1 table. Max needs to point at it so it can be pinned in the memo before implementation.
2. Max's last message ("Deliberately, I know only the visible part and i don't do inner shit") signals he won't supply internal storage details from memory - so the second-spine storage likely must be discovered by reading the code, not asked of him.

## KEY PATHS / IDS / NAMES
- Worktree cwd: `C:\moma\.claude\worktrees\strange-hawking-e9654d`
- Spec memo: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md`
- Dictionary: `C:\claude_base\user_dictionary_tomemex.md`
- Storyboard editor: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- Status script: `C:\claude_base\compaction_kb\scripts\session_status.py`
- D1 per-line tracks found in code: `line_current_clip` (talking video / lipsie pick) and `line_current_still` (still-image pick).
- Pipeline stages referenced: **sass** (splits/produces per-line audio), **sb** (storyboard), **libup** (lifts/remaps into sb, collapses merged rows), **doit22** (Max's command to execute).
- Speaker example names used in dialogue: ANNA, DRIVER.
- Tooling: WAN26flash - generates a talking clip and can alternate speakers via its description.

## GOTCHAS / DEAD ENDS RULED OUT
- **Do NOT use per-line `[[merged]]` or numbered `[[merge1]]` markers** - Max rejected both as inflexible. Use `[[MERGE]]`/`[[/MERGE]]`.
- **Do NOT re-sass on merge** - merges happen mid-edit; only grab and concatenate existing intermediates.
- **Do NOT build identity from "what was before"** - produce top-down; history is irrelevant.
- **"Second spine" is Max's name and opuses keep renaming it** - he was annoyed that sessions forget his names. It is NOT just `line_current_still` (that's one-per-line); the second spine holds SEVERAL images AND lipsies. Honor his terminology exactly.
- Don't conflate firing with transformation - they're split across two chats deliberately. This chat = transformation only.
- Several Grep attempts for "second spine"/"spine2"/"secondary" found nothing - the concept exists in the UI/Max's head, not under that literal name in code. Look at the parallel clip/still lanes and DUPS/alternates area instead.
