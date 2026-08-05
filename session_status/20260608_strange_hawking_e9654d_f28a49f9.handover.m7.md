# Scribe handover - milestone 7 (~113K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# cwd: C:\moma\.claude\worktrees\strange-hawking-e9654d
# written: 2026-06-08 11:21:00 by claude-opus-4-8

# HANDOVER - moma line-merging feature

## GOAL (in Max's words)
"Implement line combining into a single lispie." The discovery driving this: WAn26flash can alternate speakers - you put the alternation in the description and it actually alternates speakers. So scenes can now hold an unlimited number of lines (normally 2-6) where two or more speakers speak in turn. Max wants "a full cycle rework of the moma system to allow for merging of lines."

The workflow Max envisions: by command to any new session ("merge lines 2, 3, 4"), the session performs "a fool proof merge - in notion - using some smart marks we need to invent," such that several lines in a row become one mp3 file. The lifecycle: split lines as usual, then assemble the combination, name it (e.g. `lines2-4`), lift to sb, and replace the multiple lines via libup.

**Core principle Max repeated and stressed:** "the key is here to make sure that sessions which skip instructions are forced to do the proper format programmatically, not only by a command in memory. Need a programmatic control over sloppiness of lllm." The Notion script should be formally perfect (edited largely by hand, possibly with a script template to help), and everything downstream propagates programmatically so sloppy sessions can't break the format.

## DECISIONS + WHY

1. **Merge mark = `[[MERGE]]` ... `[[/MERGE]]` paired text block.** I initially proposed this, then argued against it (paired tags can be left unclosed or mistyped, breaking the parse silently). I floated alternatives: a native Notion callout box (no closing tag to forget), then per-line `[[merged]]` markers, then numbered `[[merge1]]` markers. **Max rejected all alternatives** - callout/numbering felt inflexible, and numbered/random markers would "confuse future sessions." Max's ruling: "Lets use your initial solution. The cost of error is little. Not a big deal." So the locked decision is the plain `[[MERGE]]`/`[[/MERGE]]` block. Cost of error accepted as low.

2. **No re-sass on merge.** Originally I proposed each merged unit get its own merge_hash and remember its member line_hashes. Max overrode the "remember what was before" part: "we don't care what was before. If we merge - we produce top to down." Crucially, **merges happen mid-editing**, so the rule is: merge in Notion, then **grab the existing per-line MP3 intermediates and concatenate them** into the merged MP3 - do NOT re-sass everything. Just grab intermediates, merge them, propagate down, drop the replaced lines.

3. **Pause adjustment between merged lines - DEFERRED.** Max explicitly flagged this twice as a later request: "we need to adjust the pauses bw the lines in the merge, note for later." Do not implement now.

4. **Images on merge go to the "second spine."** When lines collapse, their images are not lost - they move into the second spine, which Max confirms already exists in sb.

## CURRENT STATE
Still in design/pingpong - **no code written yet.** The blocking item right now is naming/terminology, not implementation.

I went to investigate Max's "second spine" term (Max: "the sb has a second spine, i called it this way but you, opuses, forget my names and call them other way. Go fetch"). After grepping and reading the storyboard editor, I found two parallel per-line tracks in D1: `line_current_clip` (the talking video / lipsie pick) and `line_current_still` (the still-image pick). I guessed "second spine = the still-image lane (`line_current_still`)."

**Max corrected this guess:** "the second spine can hold images and lispies and several of them." So my one-track interpretation is wrong - the second spine is NOT just the stills lane. It can hold BOTH images AND lipsies, and SEVERAL of them. It is a holding area / container that takes multiple items of either kind. My investigation has not yet correctly identified what structure in the code corresponds to this.

## EXACT NEXT STEP
Max's instruction: "Investigate and update whatever you need so next sessions know my name." Two parts:
1. **Re-investigate the sb code to correctly identify the "second spine"** - the structure that holds multiple images AND lipsies. My `line_current_still` guess was wrong/incomplete. Look beyond the two per-line track fields for a multi-item container per line (or per merge unit).
2. **Update whatever documentation/dictionary the project uses** so future sessions know the term "second spine" maps to that structure. Max keeps a dictionary of his names (I tried grepping it for "spine" - see gotchas). Record the name there.

## OPEN QUESTIONS AWAITING MAX
- Confirmation of what exactly "second spine" maps to in code (still pending - my last guess was corrected, no replacement confirmed yet).
- The script-template-assisted Notion editing ("maybe using also a script template? That would be cool") - raised by Max as a nice-to-have, not yet specced.
- merge_hash / naming scheme (`lines2-4` vs hash-based) - proposed but not finalized after Max simplified the model.

## KEY PATHS / IDS / NAMES
- Working dir: `C:\moma\.claude\worktrees\strange-hawking-e9654d`
- Storyboard editor: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- Fields found: `line_current_clip` (clip/lipsie lane), `line_current_still` (still lane), `line_hash` (per-line identity tying MP3/clip/lipsie to a slot in sb), in D1.
- Systems/terms: **sass** (splits lines, produces per-line MP3 intermediates), **sb** (storyboard), **libup** (lifts/remaps and replaces lines after edits), **lipsie/lispie** (the talking-video unit), **WAn26flash** (model that alternates speakers via the description).
- Naming convention for merged file: `lines2-4` style, or `merge_<hash>.mp3` (not finalized).

## GOTCHAS / DEAD ENDS
- **Do NOT propose numbered or callout-based merge marks again** - Max already rejected them as inflexible/confusing. The decision is `[[MERGE]]`/`[[/MERGE]]`, final.
- **Do NOT re-sass on merge** - concatenate existing intermediates only.
- **Do NOT touch pause-between-lines yet** - deferred by Max.
- **Do NOT trust my `second spine = line_current_still` guess** - Max corrected it; the second spine holds multiple images AND lipsies.
- Max uses his OWN names for things and notes that Opus sessions forget them and rename. Treat Max's vocabulary as authoritative; fetch from his dictionary rather than inventing terms. I searched for a "spine" entry in the dictionary via grep but had not surfaced a clear authoritative definition before Max's correction.
- Behavioral note: Max is in design mode and wants one-thing-at-a-time pingpong, no coding until design is locked - except the current explicit instruction to investigate and update docs, which IS an action item.
