# Scribe handover - milestone 9 (~139K tokens)
# session: 20260608_funny_booth_2ece92_7faee3c9
# cwd: C:\moma\.claude\worktrees\funny-booth-2ece92
# written: 2026-06-08 11:54:30 by claude-opus-4-8

# HANDOVER - MOMA Line-Merge Session

## ROLE ASSIGNMENT (read first)
The session just split into a team of equals. **You are D2 - you work on FIRING.** D1 owns propagation of the Notion line-merge down to the storyboard (sb). This handover documents everything discussed so far so you have full context; most of the work below was design owned by what is now D1's lane, but you (D2) need it because firing is the piece Max deferred and now wants worked.

Note on history: earlier in this same session, "firing later, finish the transformation first" was the agreed order. Max then reversed impatiently ("fuck, firing comes later. I expected much progress"), and immediately after split the session. As D2 you own firing now. Treat firing as live work, not deferred.

## GOAL (in Max's words)
"Implement line combining into a single lispie." We discovered WAN26flash can alternate speakers - you put alternating speakers in the description and it actually alternates them. So we can make scenes with an unlimited number of lines (normally 2-6) where two or more speakers speak in turn. Max wants "a full cycle rework of the moma system to allow for merging of lines."

The merge is triggered by Max's command to a session ("merge lines blabla, like 2, 3, 4"). The system must then perform a "fool proof merge - in notion - using some smart marks." The deep requirement: **"make sure that sessions which skip instructions are forced to do the proper format programmatically, not only by a command in memory. Need a programmatic control over sloppiness of llm."** The Notion script must be formally perfect; everything downstream propagates programmatically.

## DECISIONS MADE + WHY

1. **Merge mark = `[[MERGE]]` ... `[[/MERGE]]` block** wrapping the run of lines in Notion. Max rejected several alternatives: per-line `[[merged]]` (can't separate adjacent groups), numbered `[[merge1]]`/`[[merge2]]` ("inflexible"), and a Notion native callout box. He chose the paired text-tag block explicitly accepting its weakness: **"The cost of error is little. Not a big deal."** Decision locked.

2. **No re-sass.** The merge happens mid-editing. Do NOT re-run sass on everything. Instead: grab the already-produced per-line MP3 **intermediates** and concatenate them into the merged MP3. Then propagate the merged unit downstream and drop the replaced individual lines.

3. **Merged unit gets its own single identity.** Originally proposed as a merge_hash remembering member line_hashes, but Max simplified: "we don't care what was before. If we merge - we produce top to down." The merged unit takes ONE slot in sb and one lipsie. Naming convention: `lines2-4` (e.g. `lines2-4.mp3`).

4. **Freed media goes to the "second spine."** When 3 lines collapse to 1, their images/lipsies are NOT deleted - they move to the second spine.

5. **"Second spine" - Max's name, now defined.** Max corrected the assistant: the second spine "can hold images and lipsies and several of them." It is NOT `line_current_still` (one-per-line). It was pinned in code to the storyboard's per-line **dups lane** (the alternates shown beside each line's main pick). Caveat: the dups lane currently shows lipsies only, so merge work must widen it to hold images too. This was written into Max's dictionary so no future session mislabels it.

6. **Notion edit done largely by hand by the LLM**, possibly aided by a script template to keep the callout/block correct.

## CURRENT STATE
Done and durable (committed + pushed):
- **Dictionary updated**: `C:\claude_base\user_dictionary_tomemex.md` now defines Spine, Second spine (Max's way), and Merge (lines). Committed in claude_base repo.
- **Spec memo written**: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md` captures the full transformation - `[[MERGE]]` block, concatenate intermediates (no re-sass), `lines2-4` naming, merged unit = own identity, libup collapses replaced lines, freed media to second spine, second-spine pinned to the dups area. Pause-adjustment and firing both marked deferred. Committed in moma master.
- **A 4-minute wakeup timer was armed** for autonomous continuation. It is now superseded by the session split.

In flight / not done:
- Firing optimization and implementation (YOUR lane, D2) - not started.
- The actual merged-lipsie creation mechanism (the WAN26flash call) - never resolved (see Open Questions).
- The exact D1 storage table behind the second spine - pinned to the dups lane in the UI but the underlying table not fully traced.

## EXACT NEXT STEP (for you, D2)
You own firing. Max's stated sequence was: finish the transformation design (done), **"then we will manually optimize the firing and then we will implement it."** So your job is to **manually optimize the firing** of the merged lipsie before any implementation. Begin by resolving the core firing unknown below, then produce a concrete firing plan. Do NOT run live edits to TTS or DB-remap scripts without Max's `doit22` go-ahead.

## OPEN QUESTIONS FOR MAX
1. **How is the merged lipsie actually fired?** Audio is settled (concatenate intermediates). The talking video is the new magic: WAN26flash with alternating speakers. Unresolved: do you fire ONE WAN26flash call (one still showing both speakers + the merged audio + a description saying "speakers alternate"), or some other arrangement? This is THE firing question and it's yours.
2. The exact storage/table behind the second spine (UI = dups lane; underlying D1 table not confirmed).

## KEY PATHS / NAMES / COMMANDS
- Spec memo: `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md`
- Dictionary: `C:\claude_base\user_dictionary_tomemex.md`
- Storyboard UI: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- Relevant fields seen in code: `line_current_clip` (talking video / lipsie pick), `line_current_still` (still pick - NOT the second spine).
- cwd / worktree: `C:\moma\.claude\worktrees\funny-booth-2ece92`
- Scripts in play downstream: sass (line split + TTS), libup (lift-up / DB remap), sb (storyboard).
- Go signal for live changes: `doit22`.
- Status reporting script: `C:\claude_base\compaction_kb\scripts\session_status.py`.

## GOTCHAS / DEAD ENDS RULED OUT
- Do NOT use Notion callout boxes, per-line `[[merged]]`, or numbered `[[mergeN]]` marks - all rejected. Use `[[MERGE]]`/`[[/MERGE]]`.
- Do NOT re-sass on merge - grab intermediates and concatenate only.
- Do NOT call the second spine `line_current_still` - that's one-per-line; the second spine holds several images and lipsies.
- The dups lane currently holds lipsies only - widening it to images is required work, not assumed-present.
- **Pause-between-lines adjustment inside a merge** is a known future request - Max flagged it explicitly: "we need to adjust the pauses bw the lines in the merge, note for later." Deferred, but don't lose it.
- Don't block on Max or sit waiting - he is juggling many parallel chats/workers and gets frustrated by idle sessions. Make real progress; only hold the line for live destructive edits.
- Don't ask Max about inner plumbing/tables - "i know only the visible part and i don't do inner shit." Trace internals yourself from what he points at on screen.
