# Scribe handover - milestone 11 (~166K tokens)
# session: 20260608_funny_booth_2ece92_7faee3c9
# cwd: C:\moma\.claude\worktrees\funny-booth-2ece92
# written: 2026-06-08 12:11:54 by claude-opus-4-8

# HANDOVER - MOMA Line-Merge, D2 (Firing)

## GOAL (in Max's words)
"Implement line combining into a single lispie." Max discovered that **wan26flash (DashScope wan2.6-i2v-flash) can alternate speakers** when told to do so in its prompt description - proven to work at least once. So now he wants to make scenes where 2-6 consecutive lines from multiple speakers (speaking in turn) collapse into ONE lipsie clip.

His framing: a per-session command like "merge lines 2,3,4"; a foolproof merge mark in the Notion script; and - his **#1 stated goal** - "a programmatic control over sloppiness of llm." The Notion script is edited by hand (by LLM), but everything downstream must be enforced **programmatically** so sloppy sessions that skip instructions are *forced* into the correct format, not just asked politely.

The work was split into a "team of equals." **This session is D2 = FIRING** (making the actual alternating-speaker wan26flash clip). **D1 = propagation** (Notion ? sb via sass/libup/sass_prep). This session does NOT touch D1's domain.

Max's last message: "what are you working on? Your task, i think it firing optimization." He's checking in - answer plainly: you are D2, firing optimization; prep is done, build is waiting on his go.

## DECISIONS + WHY
- **Merge mark = `[[MERGE]]` / `[[/MERGE]]` block** in Notion. Max rejected per-line markers (`[[merged]]`, `[[merge1]]`) as inflexible/confusing for future sessions. He accepted the paired-block weakness because "the cost of error is little."
- **No re-sass.** sass still cuts per-line MP3s as usual, then GRABS the existing intermediates and CONCATENATES them - because merges happen mid-edit and re-running TTS on everything is wasteful. Naming like `lines2-4` / `merge_<hash>.mp3`.
- **Merged unit = ONE identity** = `merge_hash`, which remembers its ordered member `line_hash`es. Lets libup collapse the old rows into one. "We don't care what was before - if we merge, we produce top to down."
- **Freed media goes to the "second spine."** When 3 lines collapse to 1, their images/lipsies are NOT deleted - they move to Max's "second spine."
- **D1/D2 boundary (confirmed on the board):** D1 produces `merge_<merge_hash>.mp3` plus a manifest item keyed by `merge_hash` carrying the ordered list of `(speaker, line_text, member_line_hash)`. D2 consumes that + a chosen still + per-fire L/R positions ? builds the alternating-speaker prompt ? fires ONE clip. **L/R screen position is NOT propagated by D1** (`speaker_position` is unpropagated) - it's a Max/firing per-fire decision.
- **Firing is already PROVEN, not invented.** Job 2713 (2026-06-03) was a working two-person merged-audio lipsie - Max said "it worked perfectly." So D2's job is to turn that one-off hack into a clean reusable helper, NOT to discover the recipe.

## CURRENT STATE
All **authorized PREP is done, committed, and pushed.** Nothing has been built yet - building waits on Max.
- D2 firing build plan written and pushed: `moma_line_merge_firing_d2_tomemex.md`.
- D1 has confirmed the contract on the bcast board; the two sides are fully decoupled.
- The proven one-off scripts have been read and understood.
- Autonomous timer is armed (sentinel `<<autonomous-loop-dynamic>>`); board is updated.

## EXACT NEXT STEP
**Wait for Max's `doit22`** to build the helper. The wan26flau doc explicitly says "ask first" before folding the manifest-injection hack into a first-class path - so do NOT build the firing code autonomously.

When the go comes, build **`fire_merge_lipsie(merge_hash, members, still, positions, scene_id, arrangement_id, motion=None)`**:
1. Verify D1's merged audio exists via `audio_resolver.resolve_per_line_audio` - raise LOUDLY if missing, **no silent fallback**.
2. Build the alternating-speaker prompt from the ordered members + L/R positions (use the proven job-2713 prompt as the template).
3. Fire via `fire_job(job_type='lipsie', ...)` then `UPDATE jobs SET lipsync_tool='wan26flau'`.

Right now (responding to Max's check-in): just tell him plainly what you're doing - D2 firing, prep done and pushed, helper ready to build on his word.

## OPEN QUESTIONS (awaiting Max)
1. **`doit22` to build the firing helper** - the one real blocker.
2. **Where does each speaker's L/R (or L/M/R) screen position come from** - read from the still, or Max tells you per-fire? (Asked twice; not yet answered.)

## KEY PATHS / IDS / NAMES
- Build plan (D2, mine): `C:\moma\sc10\combo_runner\code\moma_line_merge_firing_d2_tomemex.md`
- Transformation spec (D1's domain, shared): `C:\moma\sc10\sound_assembly\code\moma_line_merge_spec_tomemex.md`
- Dictionary (Max's terms): `C:\claude_base\user_dictionary_tomemex.md`
- Mandatory firing doc: `C:\Users\maxre\.claude\projects\C--moma\memory\project_wan26flau_lane.md`
- Proven one-off scripts: `C:\moma\sc10\combo_runner\code\_merge_fire_exp.py` (ffmpeg concat 2 MP3s ? fresh `lines_<TS>_mergeexp/` dir + manifest + verify) and `_fire_mergeexp.py` (reads sidecar, hardcoded PROMPT, fires).
- Storyboard render: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (render fn L620-768; dups filter ~L674).
- Worker: `combo_wan26au_worker.py` (wan26flau lane, ~$0.25/clip, still + audio_url ? talking clip in one call).
- Proven job: **2713**, 2026-06-03. Engine string `wan2.6-i2v-flash`. Winning prompt = "Two people talking in turn inside a calm cabin. The man on the right speaks first, looking at the woman; then the woman on the left answers him, looking back. Gentle, minimal, barely-moving. Visible skin pores, no makeup. Soft pastel, muted saturation, film grain. Documentary, unretouched."
- bcast coordination: `C:\claude_base\branch_bulletin\bcast.py` (whoami / catchup / post). This session = **D2**.

## GOTCHAS / DEAD ENDS
- **"Second spine" was mislabeled TWICE** (guessed = recycling pool, then = `line_current_still`). Max's actual definition: a parallel storyboard lane holding **several images AND lipsies** (more than one per line), where freed merged-away media lives. Pinned in code to the storyboard **dups-area** (~L670-689). Now in the dictionary marked "MAX'S TERM - two sessions got this wrong, do NOT redefine it." Do not re-guess.
- The dups filter at ~L674 is currently `cat==='lipsie'` only - must be **widened to include images** for merge (deferred, D1's side).
- **Motion-vs-progress trap:** an adviser repeatedly flagged that this session produced commits/memos/timers but zero implementation. That's *correct here* - building genuinely requires Max's `doit22`. Don't manufacture build work to look busy; don't re-ask answered questions on timer ticks; don't re-save already-committed design.
- **No re-grep fishing** - a near-death-spiral happened from ~8 "spine" greps. Read docs/code directly in single passes.
- **Never** query local `combo_db.sqlite`; Cloudflare D1 is the live source of truth. `fire_job()` is the ONLY way to insert into the jobs table.
- wan2.6-flash prompt rules: **NO negatives** (they backfire), Bergman/Tarkovsky minimal positives, antiglamour boilerplate.
- Deferred (Max said "note for later"): **adjusting pauses between lines inside a merge.** Not now.
- Standing rule: **ALWAYS MERGE PUSH.** Keep the `<<autonomous-loop-dynamic>>` timer re-armed each tick or the loop dies.
