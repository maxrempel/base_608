# Scribe handover - milestone 6 (~450K tokens)
# session: 20260618_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-18 06:46:20 by deepseek-v4-pro

## HANDOVER - D22 (branch off D21), in-progress

---

### GOAL (Max's words)

Two workstreams, both done or nearly done:

1. **D21 (done):** Rebuild sc10 (the Anna?Ishtab two-hander) as merged multiline lipsies - ~4 lines per clip, each on the correct location still, one clip per story beat. "I like all lipsies be multiline. Ideally 4 lines or so. Rearrange arrangements to implement."

2. **D22 (in progress):** UI fixes across MOMA - first the lipser showing actual lines, then a per-scene picker replacing the per-arrangement filter, then a trim-audio bug fix. **The final D22 instruction (not yet done):** update `memory.md` to **raise the rank** of the rule: *"Since Max sees only merged main moma branch, Claude must always merge and push before asking Max to verify."*

---

### DECISIONS MADE + WHY

#### D21 - sc10 rearrangement

- **arr01 (greeting, lines 0-3) approved as job 2774.** The winning prompt style came after ~15 failed experiments:
  - "Smiles" *must not appear* - wan2.6 turns it into random laughter bursts and idiotic penguin-nodding.
  - Writing the spoken lines into the prompt *is mandatory* (Max insisted), but bare "Left/Right" labels are ignored by the model. The best approach: **describe both characters and their positions first, then give the lines in quotation marks** (used for alcove refire 2796).
  - Camera gaze is a known poison - the model defaults to characters looking at the camera. Fix: "keep their eyes on each other" + use the two-shot still as input so the composition reinforces profile/mutual gaze.
  - The locked template: *"The atmosphere is of a formal meeting of officials. The speakers keep looking at each other. Minimalistic nods. Royal postures. Minimal grins. Calm, formal, official."* Plus the quoted Left/Right lines.

- **The scene moves along a path** (from the existing per-line spine):
  - lines 0-9: meeting hall (`sc01_meet_twoshot`, Anna-L/Ishtab-R)
  - lines 10-23: corridor + window with Earth (`sc05_window_twoshot`, Ishtab-L/Anna-R - flipped sides)
  - lines 24-27: alcove (no standalone still; extracted a clean frame from the approved spine lipsie)
  - lines 28-32: doorway/room (same - frame extraction from approved clip)

- **Two lines had to stay single** because they're long monologues that alone fill the 15s wan26flau clip cap: line 8 (Anna, 14s) and line 23 (Ishtab, 13s).

- **The frame-extraction trick for alcove/doorway:** Pulled mid-frames from the already-approved spine lipsie mp4s using ffmpeg, viewed them to confirm they show both characters, and fed those PNGs as the wan26flau input still. This worked - 2793/2794/2795 all rendered.

- **Total D21 jobs: 2774-2796** (some were junked/aborted mid-session). The final arrangement with job IDs per beat is:
  - arr01: 2774 (approved)
  - hall beats: 2775, 2776, 2777, 2778
  - corridor/window: 2785, 2786, 2791, 2792
  - alcove: 2793 (original, had speaker swap) ? refired as 2796 (describe-both-first fix)
  - doorway/room: 2794, 2795

#### D22 - UI fixes (3 of 4 done)

- **Lipser showing lines (done + pushed, `2ebba53`):** Modified `runner_core.js` - the lipsie row now parses the prompt for quoted Left/Right lines and displays them in the freed prompt cell. Comment 1 & 2 boxes moved into the actions (buttons) column. Syntax-checked, cache-busted.

- **Scene picker (done + pushed, `0c9715b`):** Replaced `arrangement_picker.js` - it's now a Scene selector that fires all arrangement IDs of the chosen scene. Updated `runner_core.js` to filter by the id-list. Mixboard/storyboard already worked per-scene (they read `scene_rank`), so they needed no change beyond a hard-refresh to see the new dropdown label. Prompter's server-side filter remains single-arrangement (known limitation, flagged to Max). One shared file served by all three servers.

- **Trim audio fix (done + pushed, `7fbbefe`):** `shared_ui/popup.js` - `_openTrim` now sets `vid.muted=false`, and the START scrub handle no longer calls `vid.pause()` on every drag (so if playing, audio continues from the new position). Verified the mp4 contains an aac audio track. Cache-busted.

- **MEMORY.md rule-rank update (NOT YET DONE):** This is the exact next task.

---

### CURRENT STATE

- **sc10 all rendered** but Max hasn't fully reviewed/junked/approved each chunk beyond arr01 (2774) and the alcove refire (2796). The rest (2775-2795) are rendered and viewable in the lipser but their approval status is unknown.

- **MOMA is up** on localhost:8779 (combo_gui), 8790 (mixboard/storyboard), 8791 (prompter). The UI changes (lipser lines, scene picker, trim audio) are live on master after a refresh.

- **D21 scratch scripts** were moved to `sc10/combo_runner/local_state/d21_scratch/` (38 files, not deleted).

- **Three D22 commits on master:**
  - `2ebba53` - lipser show lines + move comments
  - `0c9715b` - scene picker
  - `7fbbefe` - trim audio fix

- **The MEMORY.md update** has not been started. It's the next action.

---

### EXACT NEXT STEP

**Update `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`** - raise the rank (likely promote to a top-tier rule, or bold/emphasize) of the rule:

> "Since Max sees only merged main moma branch, Claude must always merge and push before asking Max to verify."

This means: commit, push to master, THEN show Max the result/link. Never ask Max to check something that only exists locally.

Then commit + push the MEMORY.md change itself, probably with a D22 tag.

---

### OPEN QUESTIONS (still awaiting Max)

- **D21 sc10 approval sweep:** Which of the 12 chunks (aside from 2774 and 2796) are approved? Max hasn't reviewed the full batch.
- **Prompter full-scene view:** The picker sends all arrangement IDs but prompter's server-side filter only uses the first one. Max was told this - no response yet on whether to fix it.
- **Lipeser "useless things":** Claude offered to strip the duplicate clip-thumbnail, the separate status column, the label box - no direction yet on which to cut.
- **Drag-to-auto-play for trim:** If Max wants the instant you grab the trim handle to also auto-start playback (even from paused state), that's not done yet.

---

### KEY PATHS & IDS

- **MEMORY.md:** `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`
- **sc10 source stills (two-shots):**
  - Hall: `sc01_meet_twoshot_var01.png` (Anna-L/Ishtab-R)
  - Window: `sc05_window_twoshot.png` (Ishtab-L/Anna-R)
  - Corridor walk: `B1_corridor_walk_warm_v01.png` (Anna-L/Ishtab-R walking toward camera)
- **Frame-extracted stills (for alcove/door):** in `output_stills/_d21frames/` - `frame_alcove_24.png`, `frame_alcove_27.png`, `frame_door_29.png`, `frame_door_32.png`
- **UI files modified:**
  - `sc10/combo_runner/code/runner_core.js` (lipser lines + scene filter)
  - `sc10/combo_runner/code/arrangement_picker.js` (scene selector)
  - `sc10/shared_ui/popup.js` (trim audio fix)
- **D21 scratch:** `sc10/combo_runner/local_state/d21_scratch/` (38 scripts)
- **Key D21 jobs:** 2774 (approved arr01), 2796 (alcove refire), 2775-2795 (rest of scene, rendered, unreviewed)
- **Remote:** origin = a-demo (`https://github.com/angryskiff/a-demo`), branch = `main` (renamed from master in some contexts - push happened to master per the transcript)

---

### GOTCHAS

- **"Smiles" in a wan2.6 prompt causes laughter + random head-bobbing.** Never use emotional adjectives. Use "calm, formal, official, minimal nods, minimal grins."
- **Bare "Left:" / "Right:" labels are invisible to wan2.6.** Must describe characters by name + hair color + clothing + position FIRST, then give the lines.
- **The window two-shot has Ishtab on the LEFT, Anna on the RIGHT** - opposite of the hall and corridor stills. Future scenes must check the still visually before labeling.
- **The 15s clip cap is a hard wan26flau limit.** Long monologues (line 8, line 23) can't share a clip with neighbors. Short staccato exchanges can pack 6-7 lines into one clip.
- **Never ask Max to verify something that isn't pushed to master.** He only sees the merged branch. This is the rule being promoted now.
- **Trim dialog was muting audio** via two bugs: default `muted` state + `vid.pause()` on every scrub drag. Both fixed in `popup.js`.
- **D21 scripts were moved, not deleted** - they're in `local_state/d21_scratch/`. Don't delete them; Max may want to review.
