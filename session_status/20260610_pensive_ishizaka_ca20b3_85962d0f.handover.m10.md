# Scribe handover - milestone 10 (~152K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# cwd: C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3
# written: 2026-06-10 15:51:24 by claude-opus-4-8

# HANDOVER - MOMA Music Overlay Tab

## GOAL (in Max's words)
"Let's overlay the music... Let's add one track on top of the assembly." Max wants to take a manually-assembled video, open a music-addition tab that shows "the little video viewing rectangle, current sound track made of clips, and drop - load music interface." He adds a music file (longer or shorter than the assembly), aligns it, then "drag the line to create break points and build a volume curve. As in normal video editors, the curve is a shark tooth shape. Just shark tooth. so if i need smoothness, i simply add more break points." Each piece is ~4 minutes, with scrub back/forth to adjust. He just confirmed the preview works ("It worked! wow!") and said **"export yes. go"** - he wants the Export feature built next.

## DECISIONS + WHY
- **Standalone postprocessing tab, no pipeline wiring yet.** Max: "First we export. Adjust and then bring it back. Bringing it back will be later. Right now just an extra tab, postprocessing." So this is a self-contained tool: drop video + drop music by hand, tune, export. Re-integrating into MOMA's pipeline is explicitly deferred.
- **Hosted on the existing sound server (port 8790) at route `/music`.** Max said the placement call was "too technical" and told D10 to decide. D10 chose to hang it on the sound server.
- **Preview-first, then export.** Built full live curve editing in pure browser (Web Audio) first because it needs no ffmpeg and can't break existing tabs. Export-to-MP4 (the ffmpeg render step) was intentionally left as the follow-up - which is now the active task.
- **Layout: video on top, two stacked tracks underneath.** Max: "put the sound tracks UNDER the video. two tracks - the assembly and the music." Track 1 = Assembly (clip soundtrack, full volume, blue). Track 2 = Music (shark-tooth curve, green block).
- **Music block slides left/right to crop by mouse.** Max: "make music source movable left and right so i can this way crop. just by mouse click and slide." The whole song draws at full length; parts sliding past the video edges go dim = cropped. Max confirmed this crop behavior is exactly right.

## CURRENT STATE
- The Music tab is **live and working** at `http://localhost:8790/music`. Max confirmed it works.
- Everything runs 100% client-side in the browser right now - drag/drop video + music, align, draw shark-tooth volume curve, scrub, live preview. **Nothing is saved to disk yet.**
- Drop zones and click-to-choose both verified working (simulated drop + picker-click via Playwright).
- Work is **committed and pushed to master** - safe fallback exists. Only the two relevant files were staged (there was unrelated junk in `git status` that was deliberately excluded).
- A worklog milestone was logged.

## EXACT NEXT STEP
Build the **Export button**: bake video + clip-audio (assembly track) + music-with-curve into one final mixed MP4 via ffmpeg. The mix rule already established for preview: the video's existing clip-soundtrack stays at full volume, and the music rides underneath following the shark-tooth volume curve. The export must reproduce that same mix as a rendered file. This is the first step that needs ffmpeg (the server side), unlike everything so far which was browser-only.

## OPEN QUESTIONS (asked, not yet answered by Max)
- Whether the align/offset should also accept a **typed number of seconds** or if drag + ?1s buttons are enough.
- Whether music end-trim should be a **separate** control vs. just sliding the block (Max only confirmed slide-to-crop; never answered the end-trim question).

These are minor polish items - do not block the export work on them.

## KEY PATHS / IDS / COMMANDS
- Tab HTML: `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (route `/music` was added here)
- Server port: **8790**, served from the live tree at `C:\moma\sc10\...` (this is where the running server actually reads from).
- Python for relaunch: `C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe`
- Restart pattern that works (windowless, from the code dir):
  `cd /c/moma/sc10/sound_assembly/code && cmd //c "start /B C:\\Users\\maxre\\AppData\\Local\\Python\\bin\\pythonw.exe slideshow_server_v01.py"`
- Worklog tool: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- cwd of session: `C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3` (but edits go to the real live tree at `C:\moma\sc10\...`).
- Git: on master, committed + pushed.

## GOTCHAS / DEAD ENDS RULED OUT
- **The sound server has NO auto-watcher.** Server-side (`.py`) changes require a manual restart. HTML-only changes do NOT - just refresh the browser. The export work will touch the server, so a restart will be needed.
- **Server PID was 45284** in this session; find current PID with `netstat -ano | grep ":8790" | grep LISTEN`.
- **The `start` relaunch command is quoting-fragile** - a fancier quoted form got mangled once. Use the simple `start /B ...` form above.
- **The "drop not working" scare was a false alarm** - Max was aiming at the wrong spot on screen; drop zones are fine. (D10 had pre-emptively also fixed a real classic bug: a `<label>` wrapping a hidden file input PLUS a JS `input.click()` double-fires and Chrome suppresses the dialog - drop zones were changed to plain divs so only the single JS click fires. Keep them as plain divs.)
- **The Launch preview panel shows the static HTML** but it's non-functional there - it needs the server. Always use the `localhost:8790/music` link for the working version.
- A harmless favicon 404 appears in the browser console - ignore it, not a bug.
