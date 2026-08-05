# Scribe handover - milestone 11 (~166K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# cwd: C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3
# written: 2026-06-10 15:58:28 by claude-opus-4-8

# HANDOVER - MOMA Music Overlay Tab

## GOAL (in Max's words)
Max ("D10") wanted to "overlay the music" on an assembled video. His vision: "i manually produce assembled video. And open music addition tab. It would have the little video viewing rectangle, current sound track made of clips, and drop - load music interface - i add music file - a longer or shorter than assembly, align it, and woala - drag the line to create break points and build a volume curve... a shark tooth shape. Just shark tooth. so if i need smoothness, i simply add more break points... and play. Each piece is like 4 minutes, with ability to scroll back and forth and adjust."

Refined later: video on top, **two stacked tracks UNDER it** - Track 1 = Assembly (clip soundtrack, full volume), Track 2 = Music (shark-tooth editable). Music block must slide left/right by mouse to crop naturally as it runs past the video edges ("i slide a sound track and it slides. As it slides beyond the assembly video, it is naturally cropped").

Sequence Max set: "First we export. Adjust and then bring it back. Bringing it back will be later. Right now just an extra tab, postprocessing." ? So this is a standalone tab; wiring it into the MOMA pipeline is a deliberately deferred LATER phase.

## DECISIONS + WHY
- **Hosted at `localhost:8790/music`** on the existing sound server - Max delegated this ("you decide on the q - it is too technical for me").
- **Preview is 100% client-side** (object URLs + Web Audio API) - no upload needed for tuning, isolated, zero risk to existing tabs.
- **Slide-to-crop** drawn by rendering the full music block from offset to offset+duration; off-edge parts clip/dim - matches a normal editor's mental model.
- **Export avoids Python's removed cgi/multipart module** (Python 3.14) - files upload as raw bytes to sid-keyed temp files, then a render call runs ffmpeg.
- **Committed the working preview BEFORE building export** (485aac0) as a safe fallback.

## CURRENT STATE - all done and shipped
The full feature is COMPLETE, tested end-to-end, committed and pushed to master:
- Preview tab works (Max confirmed: "It workked! wow!").
- Export MP4 works - verified with a synthetic test clip: video stream copied untouched, music mixed to AAC, correct duration, valid MP4.
- Two commits pushed: **485aac0** (preview/two-track/drop-zone fix) and **4fe022a** (export feature).
- Server was restarted after the Python edits; `/music` returns 200; endpoints live.

## THE LIVE QUESTION - what Max is asking RIGHT NOW
Max just said: **"wait, i already optimized things. Any way to save them?"**

This means: between sessions, Max made his OWN manual edits/optimizations to files in the worktree, and is worried the work this session did (the commits) may have overwritten or will overwrite his changes. He wants to recover/preserve HIS edits.

## EXACT NEXT STEP
Do NOT commit or overwrite anything yet. Investigate what Max changed and whether it survives:
1. Run `git status` and `git diff` in `C:\moma` (and check the worktree cwd `C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3`) to see uncommitted changes still present.
2. Check `git stash list` and the reflog (`git reflog`) in case his edits were stashed or sit behind the two commits.
3. Identify which files Max touched ("optimized things") vs. the two files this session committed (music_editor.html, slideshow_server_v01.py). If his edits are uncommitted and still on disk, they are safe - reassure him and offer to commit them separately. If they appear lost, use reflog/stash to recover.
4. Report findings plainly and ask Max what exactly he optimized so the right files are checked.

## OPEN QUESTIONS AWAITING MAX
- What did he optimize, and in which files? (Needed to locate and preserve his work.)
- Earlier unresolved nicety (low priority): should music offset/align also accept a typed seconds value, or are drag + ?1s buttons enough?

## KEY PATHS / IDS / COMMANDS
- Tab URL: `http://localhost:8790/music`
- UI file: `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server file: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py`
- The running server reads from the LIVE tree `C:\moma\sc10\...` (not just the worktree).
- Server endpoints added: `/music` (GET page), `/api/music_stage` (POST raw bytes, qs sid/role/ext), `/api/music_render` (POST JSON {sid, offset, points}), `/api/music_download?sid=` (GET mixed MP4).
- Temp staging dir: `<tempdir>/moma_music_export/{sid}_{role}.{ext}`, output `{sid}_out.mp4`.
- Commits: **485aac0** (preview), **4fe022a** (export). Branch: master.
- Restart server (no auto-watcher on 8790): find PID via `netstat -ano | grep ':8790' | grep LISTENING`, then `taskkill //PID <pid> //F`, then from `/c/moma/sc10/sound_assembly/code` run `cmd //c "start /B C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe slideshow_server_v01.py"`.
- ffmpeg is on PATH (v8).

## GOTCHAS / DEAD ENDS RULED OUT
- **Drop zones**: an earlier "drops not working" report turned out to be Max aiming at the wrong spot ("the areas were wrong, haha"), NOT a bug. The fix applied (changed `<label>` wrappers to `<div>` to avoid double-firing the file picker in Chrome) is a genuine robustness improvement and is committed - don't revert it.
- **Server relaunch quoting**: bash?cmd mangles `start "title" /B ...`. Drop the title; use `cmd //c "start /B ...pythonw.exe slideshow_server_v01.py"`.
- **Python 3.14 has no cgi module** - never reach for multipart parsing; raw-bytes upload pattern is in place.
- **MOMA conventions**: light theme (cream #faf8f5), edit the live tree at C:\moma\sc10, commit on master + push, hidden subprocess via CREATE_NO_WINDOW (0x08000000), windowless server via pythonw.exe.
- Editing Python files requires a manual server restart to take effect; HTML changes only need a browser refresh.
