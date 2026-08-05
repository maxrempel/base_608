# Scribe handover - milestone 11 (~166K tokens)
# session: 20260610_recursing_euclid_b4ec94_bdd1a66e
# cwd: C:\moma\.claude\worktrees\recursing-euclid-b4ec94
# written: 2026-06-10 17:17:09 by claude-opus-4-8

# HANDOVER - Scene 9 B-roll Assembly (D13)

## GOAL (in Max's words)
- "We added b roll clips to the sb [storyboard], but the video assembly, failed to take them - make it take them and assemble the video properly."
- Most recent and now-PRIMARY ask: **"The new assembly must push and replace the old one!!!! I manually loaded the new one."**

The original render bug is fixed. The live problem now is a **propagation/handoff problem**: when Max clicks Assemble Video, the freshly rendered file does NOT automatically replace/load in whatever he's viewing. He had to manually load the new file himself. He wants the new assembly to push out and replace the old one automatically.

## DECISIONS MADE + WHY
1. **Renderer rewritten to mirror mixboard.html, not its old scene_id logic.** The old assembler (`render_mixboard_video_v01.py` v05, Apr-18) predated b-rolls and storyboard pins. It picked media by scene_id (shared scene-wide, so it would grab a random dialogue clip for a b-roll line) and required every clip to have spoken audio (b-roll has none, so it dropped to a black frame). Decision: make the renderer follow mixboard's `buildLineData()` exactly - match media by `line_hash`/`birth_line_hash`, honor the storyboard-pinned `job_id`, and add a b-roll branch that plays a pinned no-audio clip ONCE at native length.
2. **B-roll segment always gets an audio stream.** Because ffmpeg concat with `-c copy` requires uniform codecs. If the clip has no audio, inject silent `anullsrc` (44100/stereo). Keeps concat valid.
3. **Merge only the single file I touched into master.** Master had unrelated uncommitted work (CLAUDE.md + scratch `_*.py`) from other sessions - left untouched, merged only `render_mixboard_video_v01.py`.

## CURRENT STATE
- **Render fix: DONE, verified, merged to master, pushed.** Bumped to v06. Confirmed d15's later push (17b7f4a) rebased on top of mine (1e2be1f) - did NOT clobber the fix. Live file on `C:\moma` master is v06 with the b-roll branch.
- **Proof the render works:** Max's own actual Assemble run at 17:11:43 produced a file containing both b-roll clips:
  - `L-1 clip 8.00s BROLL - opening title card` (start)
  - `L10 clip 5.00s BROLL - earth arrival` (end)
  - `mix: {'clip': 2, 'lipsie': 10}`, 12 segments, 52.1s
  - Output: `G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene9_20260610_171143.mp4`
- **Verified the Music-tab handoff at code level:** storyboard's exportVideo() auto-opens `/music?job=<jid>`, and `/api/export_video/file?job=` streams the real `_export_jobs[jid]['out']` (the actual G: drive file). So at code level the right file is referenced.
- **UNRESOLVED (the live issue):** Despite the above, the new file did NOT propagate to Max's view - he loaded it manually. So either the Music tab reused a stale browser window/cached video, or there's no mechanism that forces the existing open view to swap to the new render. This is the open work.

## EXACT NEXT STEP
Diagnose why the freshly-rendered video does not auto-replace what Max is watching, and make it push/replace automatically. Concretely:
1. Check `exportVideo()` in `storyboard_editor.html` (around line 506-540): it does `window.open('/music?job='+jid,'momamusic')`. A named window target ('momamusic') **reuses an existing tab without reloading its content** if already open - a strong candidate for "didn't propagate." The video element inside the music page likely keeps its old `.src`.
2. Inspect the music page's client JS (served by slideshow_server_v01.py) - how it reads `?job=` and sets the video `.src`. Confirm whether reopening with a new job actually forces the `<video>` to reload the new source (likely needs an explicit `.src` reset + `.load()`, or a cache-busting query param).
3. Fix so a new assembly forces the open view to swap to the new file: e.g., force-reload the named window, append a cache-buster to the video URL, or have the music page detect a new job param and reset the video element.

Servers run from main checkout `C:\moma` (master). The renderer is spawned fresh per export so no restart needed for renderer changes; HTML/JS changes need a browser refresh.

## OPEN QUESTIONS (awaiting Max)
- Was the asked-for behavior literally "clicking Assemble should auto-swap the video I'm already watching to the new render"? (Strong read of his message, but confirm scope - does he want it in the Music tab, the storyboard, or both?)
- Earlier unanswered question (now likely moot given his reply): whether he expected b-roll mid-scene vs. at the edges. His "I manually loaded the new one" implies the b-roll IS present once he loads the right file - so the edges-placement question is probably resolved. Confirm if needed.

## KEY PATHS / IDS / COMMANDS
- **Worktree (where I edit):** `C:\moma\.claude\worktrees\recursing-euclid-b4ec94`
- **Main checkout (where servers run, on master):** `C:\moma`
- **The fixed file:** `sc10/sound_assembly/code/render_mixboard_video_v01.py` (now v06)
- **Reference (source of truth, NOT edited):** `sc10/sound_assembly/code/mixboard.html` - `buildLineData()` ~line 382; player `clipNoAudio` ~line 1010.
- **Server:** `sc10/sound_assembly/code/slideshow_server_v01.py` on **port 8790**. Endpoints: `/scene_lines_manifest` (~504), `/api/storyboard_state_v2` (~969, returns `assigned`={line_hash:{job_id,scene_id,spine_pinned}}), `/api/export_video` (spawns renderer), `/api/export_video/file?job=` (streams real out path), `resolve_export_dir()` (~220, prefers G: rehearsals).
- **Storyboard UI (likely needs the fix):** `sc10/sound_assembly/code/storyboard_editor.html` v41, `exportVideo()` ~line 506-540.
- **Export logs dir:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\sound_assembly\data\export_logs\` - proof log: `exp_20260610_171143.log`.
- **Render output dir:** `G:\My Drive\00Main2026\00_rehearsals\`
- **bcast identity:** This session = **D13**. Commands: `python C:/claude_base/branch_bulletin/bcast.py whoami D13` / `catchup` / `post "..."`. Already posted "JOB DONE" for the render fix - but the propagation issue is now reopened, so that post is premature.

## GOTCHAS / DEAD ENDS RULED OUT
- **B-roll is in scene 9 (sc09), not scene 10.** The clips are pinned at scene_id='sc09' which is shared scene-wide - do NOT trust scene_id for picking media; use line_hash.
- **scene_id is NOT a unique per-clip id** - that was the trap the old renderer fell into.
- **grep against `/c/moma` shows OLD code while editing the worktree** - I once thought my edit failed because I grepped the wrong checkout. Always grep the worktree path when verifying your own edits.
- **Worktree lacks `moma_data_root.txt`** (gitignored per-machine config). To test-run the renderer in the worktree, copy it from `/c/moma/sc10/combo_runner/code/moma_data_root.txt`.
- **d15 did NOT clobber the fix** - already confirmed; don't re-investigate that. d15 also added a `.segments.json` sidecar (12 blocks).
- **The render itself is NOT the bug anymore** - proven by Max's own export log. Do not re-edit the renderer for this. The remaining work is purely the UI/handoff propagation (window.open reuse / video .src not reloading).
- **Named window `'momamusic'` reuse** is the leading suspect for non-propagation - start there.
