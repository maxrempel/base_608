# Scribe handover - milestone 10 (~152K tokens)
# session: 20260610_blissful_dijkstra_cd3f0f_a588cba3
# cwd: C:\moma\.claude\worktrees\blissful-dijkstra-cd3f0f
# written: 2026-06-10 15:56:18 by claude-opus-4-8

# HANDOVER - MOMA Music Overlay Tab (D15)

## GOAL (in Max's words)
Most recent task, verbatim intent: *"bring in slides with timings from sb, only for visualization, no action, but, i need timings. I guess, the easiest, it just to bring in just timings of slides and color normal slides as one color and b rolls as another color and give them numbers. Just to help with timeline. So no images, just shadings. to help me navigate the timeline."*

Translation: On the existing music-overlay timeline, Max wants a visual reference strip showing where each slide falls in time. No slide images - just colored shaded blocks placed at the correct timings, with normal slides in one color and B-rolls in another, each labeled with a number. Purely a navigation aid laid over/alongside the timeline. No playback or editing behavior tied to it.

"sb" = storyboard (the source of the slide timings). The cold session must locate where the storyboard's per-slide timing data lives in the sound server before building anything.

## BIGGER PICTURE (the project this sits in)
Max is building a **music-overlay / postprocessing tab** for MOMA. The loop he wants:
1. He manually exports the assembled video.
2. Opens this tab, drops the exported video + a music file.
3. Aligns the music, paints a shark-tooth (piecewise-linear) volume curve on it.
4. Previews live, tunes.
5. Eventually exports a final mixed MP4 (video + clip-audio + music-with-curve baked in).

The tab is **preview-first** - full live editing now; the MP4 export step is deferred (it needs ffmpeg) and is the planned next big feature *after* the current slides task.

## DECISIONS + WHY
- **Hosted on the sound server (port 8790) as a new tab, opened at `localhost:8790/music`.** Max said the placement call was too technical and told the assistant to decide. Chosen because it sits with the existing sound tooling.
- **Preview-first, export later.** Max explicitly said "First we export... Bringing it back will be later. Right now just an extra tab, postprocessing." Live curve editing built first; baking-to-file deferred.
- **100% client-side for the editor.** Files are dropped and played straight from disk in the browser; music volume rides a Web Audio gain node that follows the shark-tooth curve. No server upload, so existing tabs are never put at risk. (Export-to-MP4 will need server/ffmpeg work - not done yet.)
- **Layout: video on top, two stacked tracks underneath.** Track 1 = Assembly (clip soundtrack, full volume, blue). Track 2 = Music with the shark-tooth volume curve (green block). Max asked for exactly this restack.
- **Music block slides left/right to crop.** The whole song draws at full length; parts sliding past the video edges dim out = cropped. Max confirmed this is exactly the crop behavior he wanted.
- **Shark-tooth curve = piecewise straight lines.** Click lane to add break points, drag up/down (top = full music, bottom = silent), double-click to delete. More points = smoother. Max's explicit model.
- **Drop zones are plain divs, not `<label>`-wrapped hidden inputs.** See gotcha below.

## CURRENT STATE
- The Music tab is **built, working, committed, and pushed to master.** That commit is a safe fallback.
- Video-on-top + two-track layout: done and confirmed.
- Slide-to-crop on the music block: done and confirmed by Max.
- Drag-drop and click-to-choose on both drop zones: fixed and verified on the live page (a simulated file-drop set the filename; a picker-click fired exactly once).
- The "oops" earlier was a false alarm - Max was dropping files onto the wrong spot on screen; the zones were never broken.
- A new **branch/worktree** has been made for the current work; the assistant is now operating as **D15** in cwd `C:\moma\.claude\worktrees\blissful-dijkstra-cd3f0f`. The slides-timing task has NOT been started yet - it was just handed over.

## EXACT NEXT STEP
Begin the slides-timing visualization task:
1. First, locate the storyboard ("sb") timing data - find where per-slide start/end times and the slide-vs-B-roll type live in the sound server tree (start in `C:\moma\sc10\sound_assembly\code\`, grep the server and any storyboard HTML/JSON it serves).
2. Decide how to surface that as colored shaded blocks on the existing `/music` timeline: normal slides one color, B-rolls another, each numbered. No images, no playback hookup - pure visual shading aligned to the timeline's time axis.
3. Implement in `music_editor.html` (HTML/JS-only change = no server restart, just refresh). Confirm on the live page, then commit.

Do NOT start a timer (Max said "No timer").

## OPEN QUESTIONS (awaiting Max / to confirm as you go)
- Where exactly the storyboard timings come from and their format - must be discovered, not assumed.
- Two earlier ? questions were left unanswered and are now likely superseded, but note them: (a) should music offset/align also accept a typed number of seconds, or are drag + ?1s buttons enough? (b) should the music's *end* be trimmable separately, in addition to slide-crop? Don't block on these.
- The Export-to-MP4 button is the agreed next big feature *after* slides - don't start it unless Max redirects.

## KEY PATHS / IDS / COMMANDS
- Working tab URL: `http://localhost:8790/music`
- Tab HTML (edit here, client-side, refresh to apply): `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server (route wiring lives here; `/music` route added): `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py`
- The **running server reads from the live `C:\moma\sc10\...` tree**, not the worktree - edits there are live.
- Server runs on port 8790, launched windowless via `pythonw.exe` at `C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe`. (Earlier PID was 45284; will differ now.)
- Find/restart server: `netstat -ano | grep ":8790" | grep LISTEN` to get PID; `taskkill //PID <pid> //F`; relaunch from the code dir with `cmd //c "start /B C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe slideshow_server_v01.py"`.
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Current cwd / worktree: `C:\moma\.claude\worktrees\blissful-dijkstra-cd3f0f`
- Last commit message: "music overlay tab: two-track layout under video + robust drop zones" - pushed to master.

## GOTCHAS / DEAD ENDS RULED OUT
- **Drop zones must be plain divs.** A `<label>` wrapping a hidden file input *plus* JS calling `input.click()` double-fires and Chrome suppresses the file dialog. This was the actual fix; don't reintroduce the label wrapper.
- HTML-only changes need **only a page refresh**, not a server restart. Server restart is only needed when editing `slideshow_server_v01.py`.
- The sound server has **no auto-watcher** - Python edits require a manual kill+relaunch.
- A relaunch command earlier got **mangled by bash quoting**; the clean form that worked is `cmd //c "start /B <full pythonw path> slideshow_server_v01.py"` run from the code dir.
- The file also appears in a "Launch preview panel" as a static page - that version does NOT work (needs the server); always test via the `localhost:8790/music` link.
- The favicon 404 in the browser console is harmless - not a real error.
- When committing, **add only the two intended files explicitly** (`music_editor.html`, `slideshow_server_v01.py`) - the repo has unrelated modified/junk files; don't `git add .`.
