# Scribe handover - milestone 9 (~136K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# cwd: C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3
# written: 2026-06-10 15:44:45 by claude-opus-4-8

# HANDOVER - Music Overlay Tab (D10 / MOMA Sound Server)

## GOAL (in Max's words)
"Let's overlay the music... Let's add one track on top of the assembly." Max wants a postprocessing tab where he manually produces an assembled video, then opens this tab to add a music track on top. His vision: "the little video viewing rectangle, current sound track made of clips, and drop - load music interface - i add music file - a longer or shorter than assembly, align it, and woala - drag the line to create break points and build a volume curve... a shark tooth shape. Just shark tooth. so if i need smoothness, i simply add more break points. That's it. and play."

Latest refinement: video on top, **two sound tracks UNDER the video** - Track 1 = the assembly (clip soundtrack, full volume), Track 2 = the music (editable via the shark-tooth curve). The music source block must be **movable left and right by mouse click and slide** so Max can crop it that way.

## DECISIONS + WHY
- **Standalone postprocessing tab, no pipeline wiring.** Max said "Right now just an extra tab, postprocessing." He exports the assembly by hand, drops it in. "Bringing it back" into MOMA proper is explicitly later.
- **Export-first was Max's stated order** ("First we export. Adjust and then bring it back"), BUT D10 chose to build **preview-first** (full live curve editing + play now, the MP4 render as a one-click follow-up) because Max delegated the technical call ("you decide on the q - it is too technical for me"). The live preview runs 100% client-side via Web Audio - no server upload, no ffmpeg yet, no risk to existing tabs. **The MP4 export step is still owed and not built.**
- **Hosted on the existing sound server (port 8790) as a new `/music` route.** D10 picked this placement since Max said it was too technical to decide.
- **Shark-tooth = piecewise straight lines between draggable break points.** Top of lane = full music volume, bottom = silent. Click to add a point, drag to move, double-click to delete.
- **Crop via sliding:** the whole song draws at full length; parts slid off the edges go dim = cropped out. Sliding left crops the intro, sliding right adds lead-in silence.

## CURRENT STATE
- Tab built and serving live at `localhost:8790/music`. Max confirmed it "sort of works."
- First layout (video rectangle + side-by-side drop boxes + align bar + curve) worked.
- Second revision done: video moved to top, transport (Play + scrub) under it, then two stacked full-width tracks below - Track 1 Assembly (blue, full volume), Track 2 Music (green draggable block + shark curve underneath). Music block now draws at full length so sliding visibly crops.
- **BLOCKER (Max's last message):** "dropping is not working. The file load areas are not accepting drops or clicks." This regression appeared after the layout restack. The drop/click handlers for loading the video and music files are broken - most likely the restack changed or removed the elements/IDs that the drag-drop and click-to-browse handlers were bound to, or the new lane elements are overlaying the drop zones and intercepting events.

## EXACT NEXT STEP
Fix the file load areas in `music_editor.html` so they accept both **drops** and **clicks** again. Investigate whether the layout edits orphaned the drop-zone event listeners (changed element IDs, removed the original drop boxes, or stacked a track lane on top capturing pointer events). Re-bind dragover/drop and click-to-open-file-picker to the correct current elements. This is HTML-only - no server restart needed, just refresh the page to test.

## OPEN QUESTIONS (awaiting Max)
- Whether align/offset should also accept a typed number of seconds, or if drag + ?1s buttons are enough. (Asked, not yet answered.)
- Whether sliding-to-crop is the right behavior, or if he also wants to trim the music's END separately. (Asked, not yet answered.)
- Confirm the two-track layout feels right once dropping is fixed - D10 has been waiting on Max's "it works" before committing.

## KEY PATHS / IDS / COMMANDS
- Working dir: `C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3` (but edits were made directly to the LIVE tree below).
- **Live tree the running server reads from:** `C:\moma\sc10\sound_assembly\code\`
- New tab file: `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (the `/music` route was added here via two edits).
- Server port: **8790**. URL: `http://localhost:8790/music`
- Server has **no auto-watcher** - Python changes require a manual restart; HTML changes only need a browser refresh.
- Restart pattern used: `taskkill //PID <pid> //F` then from `/c/moma/sc10/sound_assembly/code` run `cmd //c "start /B C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe slideshow_server_v01.py"`. Verify with `curl -s -o /dev/null -w "%{http_code}" http://localhost:8790/music`.
- Last known server PID was 45284 (now stale - it was killed and relaunched; find current PID with `netstat -ano | grep ":8790" | grep LISTEN`).

## GOTCHAS / DEAD ENDS
- The first restart attempt failed because the `start` command got mangled by bash quoting; relaunch with the simpler `cmd //c "start /B ... pythonw.exe ..."` form worked.
- Edit the **live tree** at `C:\moma\sc10\...`, NOT the worktree, or changes won't reach the running server.
- The tab also appears in the Launch preview panel, but that panel shows only the static page - it won't function there because it needs the server. Always test via the `localhost:8790/music` link.
- Everything is currently client-side only; nothing is saved to disk. The MP4 export (ffmpeg) is the still-unbuilt next major piece after the drop fix.
- Nothing has been committed yet - D10 is holding the commit until Max confirms the tab works.
