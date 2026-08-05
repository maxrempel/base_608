# Scribe handover - milestone 11 (~166K tokens)
# session: 20260608_dmiring_sanderson_f37aff_1e4b4f69
# cwd: C:\moma\.claude\worktrees\admiring-sanderson-f37aff
# written: 2026-06-08 15:27:15 by claude-opus-4-8

# HANDOVER - D3 / MOMA lipsie popup work

## GOAL (Max's words)
"made a fork, you are now stop whatever and figure out the problem - in 2nd spine - the lipsies are displayed as images. I expect them to be displayed as lipsies in the popup. I click on them, but they open a still. which is totally unexpected and wrong."

This is a **brand-new task on a fresh fork**. Drop everything prior. The problem: in the **second spine**, lipsie items show as static images, and when Max clicks one, the popup opens a **still image** instead of a playable lipsie (video). He expects clicking a lipsie to open the lipsie itself.

## CURRENT STATE
Nothing investigated yet on this new task. The transcript above (waveform fix, trim-block, dead-redo) is all PRIOR, CLOSED work - do not re-engage with it. Summary of what was already settled, so you don't waste cycles:
- The lipsie trim **waveform display** bug was fixed and pushed (master commit `9fdeab3`, added `object-fit:fill` to `#jpt-wave` img in `shared_ui/popup.js`). DONE.
- "Trim failed: unknown" in mixboard = the mixboard's intentional **player-only** `window.fetch` guard blocking all writes. By design, not a bug. Left unfixed pending Max's call (now superseded).
- "Redo button dead" was a false alarm - Max was in mixboard (where writes are blocked), not storyboard. Redo works fine in storyboard. RESOLVED.

## WHAT TO INVESTIGATE FIRST (the real next step)
The key phrase is **"2nd spine"** and **"displayed as images" vs "displayed as lipsies."** Likely causes to check, in order:
1. **How the popup decides video-vs-still.** The shared popup (`shared_ui/popup.js`, `MomaPopup.open(jobId, opts)`) opens either a playable video or a still depending on what data/URL it gets. Find where it chooses to render an `<img>` (still) vs a `<video>` for a lipsie job. The popup is opened from the storyboard via `MomaPopup.open(jobId, audioUrl ? {audioUrl} : undefined)` (storyboard_editor.html ~line 525).
2. **The "2nd spine" rendering path.** There appear to be multiple spines/lines in the storyboard. The second spine may be passing the wrong item type, a still/source-image URL, or a job id that resolves to an image job rather than a lipsie job. Find where the second spine builds its lipsie thumbnails and what it hands to the popup on click.
3. **Job-type detection.** Lipsie clips are `sc09_lipsie_v{id}_wan26flau.mp4` in `OUTPUT_LIPSIES`. The popup/combo_gui must distinguish a lipsie (video) from a still. Check whether the 2nd-spine items carry the right job_type / output_file so the popup knows to show video.

Use **live Playwright observation** (the decisive tool here, per repeated project lessons) - open the storyboard, find the 2nd spine, click a lipsie, capture what `MomaPopup.open` was called with and why it rendered a still. Do NOT speculate or rewrite blind.

## OPEN QUESTIONS FOR MAX (ask pingpong if stuck)
- What exactly is "2nd spine"? (Second line/row in storyboard? A specific named spine?) Confirm which UI element so you observe the right thing.
- Does the FIRST spine show lipsies correctly as playable, and only the 2nd is broken? (That contrast pinpoints the divergent code path.)

## KEY PATHS / IDS
- **Shared popup (ALL popup edits go ONLY here - hard rule):** `C:\moma\sc10\shared_ui\popup.js` + `popup.css`. Served by combo_gui at `http://localhost:8779/shared/popup.js` with `no-store` (browser always gets fresh - cache is NOT a factor).
- `MomaPopup.open(jobId, opts)` is the entry; storyboard calls it ~line 525 of `storyboard_editor.html`.
- **Storyboard UI:** `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (loads popup.js at line 1093, `MomaPopup.init` ~1095). NO player-only guard - writes work here.
- **Mixboard (player-only, AVOID for testing writes):** `C:\moma\sc10\sound_assembly\code\mixboard.html` - has a `window.fetch` wrapper (~lines 157-174) blocking all non-GET with fake 403 `{blocked,reason:'mixboard is player-only'}`.
- **Backend:** `C:\moma\sc10\combo_runner\code\combo_gui.py` (port 8779). Relevant endpoints: `/source/<file>` (serves stills), `/waveform/<jobId>`, `/api/lipsie/redo/<id>` (~line 2555), `/api/video/trim/` (~line 2989), `serve_file`/`/shared/` static serving.
- **Servers/ports:** combo_gui = 8779; slideshow_server_v01.py serves both mixboard AND storyboard = 8790 (`/storyboard`, `/mixboard`); prompter = 8791.
- **DB:** Cloudflare D1 via `moma_db.py` `connect_db()`; use `c.execute(sql, params).fetchone()` (NOT `.query` - that attribute doesn't exist).
- **Lipsie files:** `OUTPUT_LIPSIES` (in `paths.py`), named `sc09_lipsie_v{id}_wan26flau.mp4`. Search candidate dirs: `OUTPUT_CLIPS`, `APPROVED_CLIPS`, `OUTPUT_LIPSIES`.
- **Worktree:** prior session was in `C:\moma\.claude\worktrees\musing-gagarin-82b57d`. Max said "made a fork" - you are likely in a NEW worktree (cwd `C:\moma\.claude\worktrees\admiring-sanderson-f37aff`). Live servers read popup.js from the MAIN checkout `C:\moma`, so a fix must reach `C:\moma` (commit on master from main checkout, or merge) to go live.

## GOTCHAS / DEAD ENDS ALREADY RULED OUT
- **Don't blame browser cache** - popup.js is served `no-store`; served bytes == disk bytes (verified). Look for a real code path.
- **Don't test in mixboard** - it blocks all writes (player-only). Test lipsie/popup behavior in **storyboard**.
- **Don't fire a real redo** - wan26flau costs ~$0.25 per job. (Likely irrelevant to this task, but noted.)
- **Trim re-encodes all-intra** and bloats files (~3.27MB ? ~16MB); if you trim a test file, restore from `archive/` and clean up `.wave2.png`/preview/tmp. (Likely irrelevant here.)
- Job 2712 (10.02s lipsie) was used as a test fixture before and restored to original - leave it intact.

## PROTOCOL REMINDERS
- Replies to Max: **plain English, TLDR-first, pingpong, ~200 chars, no code shown.**
- After a working edit: **commit + push** (mandatory). Coordinate via bcast (`whoami d3` first, then `catchup`, then `post`) - siblings D1/D2 work on line-merge; avoid save conflicts.
- Near token limit (~166K now, compaction ~169K): write a `session_status.py report` snapshot before you run out.

## EXACT NEXT STEP
Open the storyboard live (Playwright, `http://localhost:8790/storyboard`), locate the "2nd spine," click a lipsie there, and capture exactly what `MomaPopup.open` receives and why it renders a still (`<img>`/`/source/...`) instead of a playable lipsie video. Compare against a working lipsie click (e.g. 1st spine) to find the divergent code path. Then trace back to where the 2nd spine builds its lipsie item / passes the job to the popup.
