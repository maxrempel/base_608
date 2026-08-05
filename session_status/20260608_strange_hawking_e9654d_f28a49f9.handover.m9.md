# Scribe handover - milestone 9 (~139K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# cwd: C:\moma\.claude\worktrees\strange-hawking-e9654d
# written: 2026-06-08 11:53:51 by claude-opus-4-8

# HANDOVER - MOMA Line-Merge (you are D1)

## GOAL (in Max's words)
"Implement line combining into a single lispie." The discovery: WAN26flash can alternate speakers - you put it in the description and it actually alternates the speakers in one generated talking-video. So you can now make scenes with 2-6 lines where two or more speakers speak in turn, all as one clip. Max wants "a full cycle rework of the moma system to allow for merging of lines."

The trigger will be a command Max types to any session: "merge lines 2,3,4" (or similar). The key requirement, in his words: "make sure that sessions which skip instructions are forced to do the proper format programmatically, not only by a command in memory... Need a programmatic control over sloppiness of llm." The Notion script stays formally perfect (edited largely by hand, maybe with a script template), and everything downstream is propagated programmatically.

This session is now **D1**, owning the **transformation** (the merge plumbing). A separate worker **D2** owns **firing** (the actual WAN26flash generation). Firing is explicitly NOT your concern - Max said "firing comes later."

## DECISIONS + WHY

1. **Merge mark = `[[MERGE]]` ... `[[/MERGE]]` block in the Notion script.** Max rejected several alternatives:
   - Paired typed tags were first flagged as typo-prone - but Max ultimately CHOSE them anyway, reasoning "the cost of error is little, not a big deal."
   - A Notion native callout block was proposed (no closing tag to forget) - rejected implicitly, Max went back to the text block.
   - Per-line `[[merged]]` markers and numbered `[[merge1]]` - Max rejected: "inflexible," and random 2-digit numbers would "confuse future sessions."
   - **Final: plain `[[MERGE]]` / `[[/MERGE]]` block. Locked.**

2. **No re-sass.** Merges happen mid-edit. Do NOT re-run sass on everything. Instead: grab the already-produced per-line MP3 intermediates and concatenate them into the merged MP3. "Just grab intermediates and merge them... propagate down."

3. **Naming:** merged file named like `lines2-4` (e.g. `lines2-4.mp3`).

4. **Merged unit = one identity, one slot.** It takes ONE slot in sb and ONE lipsie. Max's clarification: "we don't care what was before. If we merge - we produce top to down." The replaced individual lines are dropped; the merged unit propagates downstream. libup collapses the old rows into the one merged row.

5. **Freed media goes to the "second spine."** When 3 lines collapse to 1, the per-line images/lipsies are NOT deleted - they move to the second spine. (See dictionary note below - this is Max's term and was wrong in prior sessions.)

6. **Deferred / out of scope for now:**
   - **Pause adjustment between merged lines** - Max: "one more funny request - we need to adjust the pauses bw the lines in the merge, note for later." Explicitly later.
   - **Firing** (the WAN26flash call: which still goes in, the alternate-speakers description) - now D2's job.

## CURRENT STATE - what's done
All design is locked and durable (committed + pushed):

- **Dictionary updated** with Max's term. `C:\claude_base\user_dictionary_tomemex.md` now defines **"second spine"** Max's way: a parallel storyboard lane that holds **several images AND lipsies** per line (not one-per-line). Committed in claude_base.
- **Spec memo written and committed** in moma master: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md` - captures the whole transformation (the `[[MERGE]]` block, concatenate intermediates / no re-sass, `lines2-4` naming, merged unit with own identity, libup collapses members, freed media to second spine, pause-adjust + firing marked deferred).
- **Second spine pinned to code:** investigation of the full storyboard render landed it at the storyboard's per-line **dups lane** (the alternates beside each line's main pick). Caveat recorded in the memo: the dups lane currently shows **lipsies only**, so merge work must **widen it to hold images too**. This pin was committed + pushed.
- A 4-minute wakeup timer was armed earlier (autonomous-continue authorization). May or may not still be relevant given the session split.

## EXACT NEXT STEP
Push the transformation forward (Max is frustrated by waiting - he expected progress, not blocking). Concretely: read `sass`, `libup`, and `sass_prep` to pin the **exact code spots where merge plugs in**, then write a concrete implementation plan into the spec memo. Specifically nail down:
- Where sass/parser reads the `[[MERGE]]` block out of the Notion script.
- Where the per-line MP3 intermediates live and how to concatenate them into `lines2-4.mp3`.
- How the merged unit gets its single identity / slot.
- How libup collapses the member rows into one and routes freed images/lipsies into the second spine (dups lane), including widening that lane to accept images.

**Hard limit Max set:** do NOT run live edits to the TTS or DB-remap scripts while he's away. Those need his `doit22` command. Reading and planning are fine; live destructive runs are gated.

## OPEN QUESTIONS (awaiting Max)
1. **Exact storage table behind the second spine.** D1 deliberately did NOT guess a D1 table. Max confirmed he only knows the *visible* part and won't deal with "inner shit." Plan: when implementing, open the storyboard, have Max point at the lane on screen, then trace it into the code yourself. Do not pester him for the table name.
2. **Firing mechanics** - now D2's, not a question for you.

## KEY PATHS / IDS / NAMES
- Worktree cwd: `C:\moma\.claude\worktrees\strange-hawking-e9654d`
- Spec memo: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md`
- Dictionary: `C:\claude_base\user_dictionary_tomemex.md`
- Storyboard UI: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- Code names found: `line_current_clip` (the talking-video / lipsie pick lane), `line_current_still` (still-image pick). NOTE: second spine is NOT `line_current_still` - it's the **dups lane**.
- Status script used: `C:\claude_base\compaction_kb\scripts\session_status.py report "..."`
- Commit trigger word: `doit22` (Max's go-ahead for live implementation).
- User name in dictionary files: tomemex (Max).

## GOTCHAS / DEAD ENDS RULED OUT
- **Don't re-propose the merge-mark format.** It's settled as `[[MERGE]]`/`[[/MERGE]]`. Callout blocks, per-line markers, numbered markers all rejected. Cost-of-error is accepted as low.
- **Don't re-sass.** Merge reuses existing intermediates.
- **Don't conflate "second spine" with `line_current_still`** - that was the earlier wrong guess. It's the dups/alternates lane, holds multiple images + lipsies.
- **Don't ask Max for internal table names** - he only knows the visible UI by design.
- **Don't touch firing** - that's D2.
- **Don't run live TTS / DB-remap edits without `doit22`.**
- Max is running many parallel chats/workers and is impatient with idle waiting - bias toward concrete progress over more pingpong design questions.
