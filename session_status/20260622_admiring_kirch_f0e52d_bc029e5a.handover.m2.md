# Scribe handover - milestone 2 (~165K tokens)
# session: 20260622_admiring_kirch_f0e52d_bc029e5a
# cwd: C:\moma\.claude\worktrees\admiring-kirch-f0e52d
# written: 2026-06-22 17:28:49 by deepseek-v4-pro

# HANDOVER - D40: Named Music Projects ("uei starseeds pitch")

---

## GOAL (Max's words)

> "In moma we already have overlay audio, Create a new scene outside of movie, call it uei starseeds pitch. Import this video 'C:\Users\maxre\Videos\starseeds_pitch_20260622_cleanup\starseeds_pitch_cleaned_v10.mp4' and this audio 'C:\Users\maxre\Downloads\Celestial Docking Lights (1).mp3' and let me adjust audio position in the music tab. register check in as D40"

Max wanted a **named, standalone music-overlay project** - separate from the movie pipeline - pre-loaded with his video + music, openable in the existing MOMA Music tab, so he can drag the audio offset and Export an overlaid MP4.

---

## DECISIONS + WHY

1. **Persistent Nextcloud-synced folders** for project storage (`SOUND_DATA_DIR/music_projects/<slug>/`) instead of reusing the existing fragile tempdir staging (`{tempdir}/moma_music_export/`). Rationale: Nextcloud sync means the project survives reboots, travels between machines, and outlasts tempdir cleanup. Long-term elegance over shortcut.

2. **Named projects keyed by URL slug** (`?project=uei_starseeds_pitch` on the `/music` page). The old music tab was a single global project via localStorage key `moma_music_overlay_v1`; now project mode namespaces localStorage + auto-saves offset/points to the server folder via debounced POST to `/api/music_project_save`.

3. **Shared ffmpeg helper** `render_music_overlay(vpath, mpath, outp, offset, pts)` extracted from the old inline movie-render code. Both the old `/api/music_render` and the new `/api/music_project_render` call this same function - no code drift between the two render paths.

4. **Three IIFEs in `music_editor.html` guarded with `if(PROJECT) return;`**: `autoLoadFromExport()` (movie export auto-load), `startAssemblyWatch()` (polls `/api/export_video/latest`), and `restoreSession()` (restores from server-staged temp files). These are movie-pipeline features that must not activate when a named project is open.

5. **Reusable import CLI** (`music_project_import.py`) rather than a one-off script. Takes `--slug --title --video --music --reset`. Preserves prior offset/points unless `--reset` is passed.

6. **Video v09 used, not v10**: the transcript discovered `starseeds_pitch_cleaned_v10.mp4` does not exist on disk; the latest cleaned version is `v09`. This was flagged explicitly to Max (? block) - not silently substituted.

---

## CURRENT STATE

### Code - all committed, merged to master, pushed

- **`sc10/sound_assembly/code/slideshow_server_v01.py`**
  - VERSION bumped to v40 (NAMED MUSIC PROJECTS), VERSION_PREV preserved v39 text inline.
  - Module-level helpers added after line 169: `MUSIC_PROJECTS_DIR`, `music_proj_slug()`, `music_proj_dir()`, `music_proj_read()`, `render_music_overlay()`.
  - New GET endpoints: `/api/music_projects` (list), `/api/music_project` (state JSON), `/api/music_project_file` (serve video/music with Range support), `/api/music_project_download` (serve overlay_out.mp4).
  - New POST endpoints: `/api/music_project_save` (persist offset/points/title), `/api/music_project_render` (ffmpeg render to project folder).
  - New method `_send_obj(self, obj, code=200)` - sends JSON response.
  - Existing `/api/music_render` refactored to call `render_music_overlay()`.
  - Syntax verified via `ast.parse`.

- **`sc10/sound_assembly/code/music_editor.html`**
  - Header: added `<span id="projTag">` (shows project title or errors in red).
  - After `SAVE_KEY`: added `PROJECT` const parsing `?project=` from URL, namespaced `SAVE_KEY` when in project mode, added `saveProjectState()` (debounced 600ms POST to `/api/music_project_save`), hooked into `saveState()`.
  - Export handler: project-mode branch posts to `/api/music_project_render` then `window.location = data.url`.
  - Three movie IIFEs guarded with `if(PROJECT) return;`.
  - Added `loadProject()` IIFE: hides drop zones, fetches project state, loads video + music via `/api/music_project_file`, applies saved offset/points, sets up audio graph (ensureAudio/musicEl/gainNode/computePeaks).
  - Version text bumped to "named projects (?project=) ... v06 ... 2026-06-22".

- **`sc10/sound_assembly/code/music_project_import.py`** - reusable CLI
  - Syntax verified via `ast.parse`.
  - Uses the same sys.path hack as the server to import `paths` and resolve `SOUND_DATA_DIR`.

### Live system

- **Port 8790 server running** from master checkout (`C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py`).
- **Project imported**: `SOUND_DATA_DIR/music_projects/uei_starseeds_pitch/` contains:
  - `project.json` (slug, title "UEI Starseeds Pitch", video name, music name, offset 0.0, points [])
  - `video.mp4` - `starseeds_pitch_cleaned_v09.mp4`
  - `music.mp3` - `Celestial Docking Lights (1).mp3`
- **Verified**: `curl http://localhost:8790/api/music_project?slug=uei_starseeds_pitch` returns valid JSON with both files present.
- **D40 bcast** registered.

### Open URL

`http://localhost:8790/music?project=uei_starseeds_pitch` - Music tab loads with video + "Celestial Docking Lights" already in place, drop zones hidden, project title in header, auto-save active.

---

## EXACT NEXT STEP

**None - the task is complete from the implementation side.** Max needs to:
1. Open the URL.
2. Adjust audio position in the Music tab (drag offset or nudge).
3. Click Export to render the overlaid MP4.
4. **Confirm whether v09 is acceptable or if he has a v10 elsewhere** (see Open Questions).

---

## OPEN QUESTIONS (awaiting Max)

1. ? **Video version**: Max specified `starseeds_pitch_cleaned_v10.mp4` but only `v09` exists on disk. Max needs to either accept v09 or provide the location of v10. If v10 is found, re-run:
   ```
   python C:\moma\sc10\sound_assembly\code\music_project_import.py --slug uei_starseeds_pitch --title "UEI Starseeds Pitch" --video "<path-to-v10>" --music "C:\Users\maxre\Downloads\Celestial Docking Lights (1).mp3" --reset
   ```
   The `--reset` flag will overwrite the video file but preserve offset/points if Max had already started positioning.

---

## KEY PATHS / IDs

| What | Path |
|---|---|
| Server source | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` |
| Music tab UI | `C:\moma\sc10\sound_assembly\code\music_editor.html` |
| Import CLI | `C:\moma\sc10\sound_assembly\code\music_project_import.py` |
| Projects data dir | `{paths.SOUND_DATA_DIR}/music_projects/` (Nextcloud-synced) |
| This project | `.../music_projects/uei_starseeds_pitch/` |
| Video (in project) | `.../uei_starseeds_pitch/video.mp4` (v09 of starseeds_pitch_cleaned) |
| Music (in project) | `.../uei_starseeds_pitch/music.mp3` (Celestial Docking Lights (1)) |
| Live URL | `http://localhost:8790/music?project=uei_starseeds_pitch` |
| Server port | 8790 |
| Check-in label | D40 |
| Worktree (archived) | `C:\moma\.claude\worktrees\admiring-kirch-f0e52d` |

---

## GOTCHAS

1. **v09, not v10**: If Max insists on v10, it must be located and re-imported with `--reset`. The import CLI will overwrite `video.mp4` in the project folder.

2. **Server restart required after Python edits**: No code edits remain, but if any backend change is needed, the server must be killed and re-launched from the master checkout:
   ```
   taskkill /F /PID <pid-on-8790>
   cd C:\moma\sc10\sound_assembly\code
   start /B pythonw slideshow_server_v01.py
   ```

3. **`moma_data_root.txt` is gitignored**: Any import or server operation must run from `C:\moma` (the master checkout), NOT from a worktree. The worktree lacks this file, so `paths.py` resolution would fail.

4. **`_dt_now()` dead end**: Was briefly used but doesn't exist in the codebase - replaced with inline `__import__('datetime').datetime.now().isoformat(timespec='seconds')`.

5. **Junk line cleaned**: `music_project_import.py` had a leftover `shutil.cop2 = shutil.copy2  # noqa` nonsense line - removed during cleanup.

6. **Merge+push rule**: HARD RULE #1 - always commit, merge to master, and push BEFORE asking Max to verify anything, because servers serve from master and Max only sees master. This was followed.

7. **Preview panel**: The Launch environment kept noting `music_editor.html` was visible in its preview panel. This is a dev-environment artifact, not relevant to Max (who uses the browser at localhost:8790).
