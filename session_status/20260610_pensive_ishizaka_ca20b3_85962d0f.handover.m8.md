# Scribe handover - milestone 8 (~120K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# cwd: C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3
# written: 2026-06-10 15:40:21 by claude-opus-4-8

# HANDOVER - Music Editor Tab (MOMA Sound Server)

## GOAL (in Max's words)
Max wants to overlay music onto an already-assembled video. His vision: "I manually produce assembled video. And open music addition tab. It would have the little video viewing rectangle, current sound track made of clips, and drop - load music interface - I add music file - longer or shorter than assembly, align it, and walla - drag the line to create break points and build a volume curve... the curve is a shark tooth shape. Just shark tooth. so if I need smoothness, I simply add more break points. That's it. And play."

The current ask (last prompt): "Now put the sound tracks UNDER the video. Two tracks - the assembly and the music. Make the music be able to edited via shark [shark-tooth curve]. Also make music source movable left and right so I can this way crop. Just by mouse click and slide left and right."

## DECISIONS + WHY
- **Standalone postprocessing tab, no pipeline wiring yet.** Max explicitly said: "First we export. Adjust and then bring it back. Bringing it back will be later. Right now just an extra tab, postprocessing." So this tab is self-contained - drop video + music, tune, (eventually) export. Re-integrating the result into MOMA is a future task.
- **Hosted on the sound server (port 8790) at the route `/music`.** Max said the placement question was "too technical" and told the assistant to decide. Chosen for cleanliness - new tab, isolated from existing tabs.
- **Preview-first, 100% client-side.** The tab plays both files straight from disk in the browser; music volume rides a Web Audio gain node following the shark-tooth curve. No server upload, no ffmpeg yet - this keeps existing tabs at zero risk and makes tuning instant. Export-to-MP4 (the actual mixed file, needs ffmpeg) is a deliberately deferred follow-up step.
- **Mix model:** the video's existing clip-soundtrack stays at full volume; the music rides *under* it following the curve.

## CURRENT STATE
- A working first version of the Music tab exists and is **live** at `localhost:8790/music`. Max tested it: "it sort of works. thanks."
- It currently supports: drag-drop video (left box) + music (right box), a green "music placement" bar to align music to video, a "volume curve" lane where clicking drops break points, dragging moves them (top = full music, bottom = silent), double-click deletes a point, straight lines between points form the shark-tooth. Play + scrub + live tuning all work. Nothing is saved to disk yet.
- The `/music` route was added to the server and confirmed returning HTTP 200 after restart.

**In flight / NOT yet done - this is the current request:**
1. Restructure the layout so **both sound tracks sit UNDER the video** as two visible lanes/tracks: one for the **assembly** (the video's own clip soundtrack) and one for the **music**.
2. Keep/confirm the **music edited via shark-tooth volume curve**.
3. Make the **music source itself slide left/right by mouse click-and-drag** so Max can crop it by repositioning (drag the music block horizontally, not just an offset bar).

## EXACT NEXT STEP
Edit `music_editor.html` to:
- Move the two audio tracks to render below the video rectangle, stacked: assembly track on one lane, music track on another.
- Make the music clip directly draggable horizontally with the mouse to reposition/crop against the video timeline (replacing or augmenting the current green placement bar + ?1s buttons).
- Ensure the shark-tooth volume-curve editing still applies to the music track in the new layout.
Then restart the server so the change goes live (see restart procedure under GOTCHAS), curl-check `/music` returns 200, and ask Max to test before committing.

## OPEN QUESTIONS (awaiting Max)
- Earlier unanswered: should the align/offset also accept a **typed number of seconds**, or is drag enough? Max hasn't answered - and his latest request ("movable by mouse click and slide") leans toward drag being the priority, so typed input is likely optional/secondary.
- Export-to-MP4 is agreed as a later step; not started.

## KEY PATHS / IDS / COMMANDS
- Working dir of this session: `C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3`
- **Live tree the running server actually reads from:** `C:\moma\sc10\sound_assembly\code\` - edit files HERE, not in the worktree, for changes to go live.
- Tab HTML: `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server file: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (route `/music` already wired in)
- URL: `http://localhost:8790/music`
- Server runs on port **8790**, launched windowless via `pythonw.exe`.
- pythonw path: `C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe`

## GOTCHAS / DEAD ENDS
- **The sound server has NO auto-watcher** - you MUST restart it manually for any change (HTML or .py) to go live.
- **Restart procedure:** find the PID with `netstat -ano | grep ":8790" | grep LISTEN`, then `taskkill //PID <pid> //F`, then relaunch from inside the code dir: `cd /c/moma/sc10/sound_assembly/code && cmd //c "start /B C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe slideshow_server_v01.py"`. The first relaunch attempt got **mangled by shell quoting** when the start command was over-quoted - use the simple form above. Verify with `curl -s -o /dev/null -w "%{http_code}" http://localhost:8790/music` (expect 200).
- The file also shows in the Launch preview panel as a **static page** - that version does NOT work because it needs the server. Always use the `localhost:8790/music` link.
- Last running PID observed was 45284 (now stale after restart - re-check before killing).
- Nothing is persisted to disk yet; all tuning is in-browser only.
