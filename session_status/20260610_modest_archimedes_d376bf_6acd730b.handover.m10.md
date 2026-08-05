# Scribe handover - milestone 10 (~152K tokens)
# session: 20260610_modest_archimedes_d376bf_6acd730b
# cwd: C:\moma\.claude\worktrees\modest-archimedes-d376bf
# written: 2026-06-10 15:54:06 by claude-opus-4-8

# HANDOVER - MOMA Music Overlay Tab (D14)

## GOAL (in Max's words)
Max wanted to "overlay the music" onto an assembled video. His vision: a postprocessing tab with "the little video viewing rectangle, current sound track made of clips, and drop-load music interface" - drop a music file (longer or shorter than the assembly), "align it," then "drag the line to create break points and build a volume curve" that is a "shark tooth shape" ("Just shark tooth. so if i need smoothness, i simply add more break points"). Each piece is ~4 minutes with scroll back/forth to adjust. Export first, "bring it back" into the MOMA pipeline later.

Most recent request: "now little improvements - just made this into a branch, you are now D14. **Make both sound tracks look like histograms with bars.**"

## DECISIONS + WHY
- **Standalone postprocessing tab, no pipeline wiring yet.** Max explicitly said export first, bring-it-back later, "Right now just an extra tab, postprocessing."
- **Hosted on the sound server (port 8790) at route `/music`.** Max said the placement question was too technical and told the assistant to decide.
- **Preview-first, 100% client-side.** Files play straight from disk in the browser; music volume rides a Web Audio gain node following the shark-tooth curve. No server upload, no ffmpeg yet. Chosen because it's fast and risk-free to existing tabs. Export-to-MP4 (via ffmpeg) is a deliberate later step.
- **Layout: video on top, two stacked tracks underneath.** Max asked for this restack: "put the sound tracks UNDER the video. two tracks - the assembly and the music."
  - Track 1 = Assembly (clip soundtrack, full volume, drawn as a blue bar).
  - Track 2 = Music (shark-tooth volume curve; click to add break points, drag up/down = full?silent, double-click to delete).
- **Music block slides left/right by mouse to crop.** The full song draws at full length; parts that slide past the video edges go dim = cropped. Max confirmed this is exactly the behavior he wanted.

## CURRENT STATE
- The Music tab is **built, working, committed, and pushed to master.** A safe fallback exists.
- Drag-drop AND click-to-choose on the drop zones are both verified working on the live page (tested via Playwright - simulated a real file-drop and a picker-click, both fire correctly).
- Earlier drop-zone bug was a false alarm twice over: the assistant suspected a `<label>`+hidden-input double-click-fire bug and fixed it by making drop zones plain divs (single JS click only); but Max then revealed he was simply "dropping onto the wrong spot." The div-based fix is committed anyway and is fine.
- **Max has just turned this into a branch** and is now requesting the histogram-bar visual for both tracks. This work is NOT yet started.

## EXACT NEXT STEP
Make **both** sound tracks (Track 1 Assembly and Track 2 Music) render as **histograms with bars** - i.e. a waveform/amplitude bar visualization instead of the current flat colored bars. This is a visual improvement only. Edit `music_editor.html`. Since it's pure HTML/JS, **no server restart is needed - Max just refreshes the page.**

Note: confirm which git branch is now checked out before committing (Max said "just made this into a branch"). Verify with `git rev-parse --abbrev-ref HEAD` - earlier work was committed on master, so this branch was created after that commit.

## OPEN QUESTIONS (asked, not yet answered)
- Whether the music end should be trimmable separately, or sliding left/right (crop intro / add lead-in silence) is enough. (Max moved on without answering.)
- Whether offset/align should accept a typed seconds value vs. drag + ?1s buttons. (Unanswered.)
- The Export button (bake video + clip-audio + music-with-curve into one MP4 via ffmpeg) is offered and pending Max's go-ahead - NOT yet requested.

## KEY PATHS / IDS / COMMANDS
- cwd: `C:\moma\.claude\worktrees\modest-archimedes-d376bf`
- Tab HTML: `C:\moma\sc10\sound_assembly\code\music_editor.html`
- Server: `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (route `/music` added here)
- Live URL: `http://localhost:8790/music`
- Server port 8790; the running server reads from the **live tree at `C:\moma\sc10\...`** (not the worktree).
- Restart command (windowless), run from `/c/moma/sc10/sound_assembly/code`: `cmd //c "start /B C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe slideshow_server_v01.py"`. Find PID with `netstat -ano | grep ":8790" | grep LISTEN`.
- Worklog tool: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Key JS/markers in the HTML: `assemblyLane`, "Track 1", "Track 2", "drag the block".

## GOTCHAS
- **The sound server has NO auto-watcher.** Python (`.py`) changes require a manual kill + relaunch to go live. HTML changes do NOT - just refresh the browser.
- Earlier a relaunch command got **mangled by Bash quoting**; the clean form is the `cmd //c "start /B ... pythonw.exe ..."` one above. Use `pythonw.exe` for windowless.
- Drop zones must stay **plain divs** with a single JS-driven `.click()` - do NOT wrap a hidden file input in a `<label>` (causes Chrome to suppress the picker via double-fire).
- The drop-zone "not accepting drops" report was a **false alarm** - Max was aiming at the wrong area. No real bug there.
- `git status` shows unrelated junk in the repo - when committing, add **only** the two specific files (`music_editor.html`, `slideshow_server_v01.py`), never `git add .`.
- Favicon 404 in console is harmless - ignore it.
