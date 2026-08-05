# Scribe handover - milestone 2 (~163K tokens)
# session: 20260628_wonderful_liskov_dcda0b_589c5f13
# cwd: C:\moma\.claude\worktrees\wonderful-liskov-dcda0b
# written: 2026-06-28 23:11:40 by deepseek-v4-pro

# HANDOVER - MOMA Music Save/Load Versioning (D51)

---

## GOAL (Max's words)
Fix music saving in the MOMA system before moving to SC11. The music overlay on finished scenes was "overlaid and lost" - every scene's music + parameters vanished when you started the next one. Requirements:
- Save **ALL** music overlay parameters (offset, volume curve / shark-tooth points)
- **Collect** the input files (scene video + music track) into one place - actually copy them, not just link
- Support **multiple saved versions** (~15), because "not always the latest version is the best" - keep options, allow loading a non-latest one
- Add a **Load button** so saved versions are visible and restorable
- "Don't forget to save the curve" - the volume envelope points must be in every save
- Auto-naming with timestamp plus an optional label

---

## DECISIONS + WHY

1. **New `music_saves/` directory, separate from `music_projects/`.** The existing `music_projects/` system (D40, 2026-06-22) was designed for standalone named projects with manual slugs and a different UI mode (`/music?project=<slug>`). Max never used it for scenes. Rather than force scenes into that model, we added a parallel versioned-save system that auto-names by timestamp and auto-prunes to 15 - simpler and directly wired to the global Music tab path Max actually uses (`/music`).

2. **Auto-naming: `scene_YYYY-MM-DD_HHMM` (plus optional label).** Max said "not too many, maybe 15" and wanted versioning without ceremony. Timestamp is guaranteed unique and sortable. An optional label box lets him annotate (e.g., "quiet intro," "louder drums").

3. **Staging re-use on Load.** The existing global tab stages media into `tempdir/moma_music_export/{sid}_{role}.{ext}` via `/api/music_stage`. Load copies the saved files back into temp staging under a **fresh sid**, so the existing waveform player, export, and playback all work without change. No special-case code needed for loaded media.

4. **Save format per version:** folder `music_saves/<timestamp>/` containing:
   - `save.json` - `{created, label, offset, points, vid_name, vid_ext, vid_size, mus_name, mus_ext, mus_size}`
   - `video.<ext>` - the collected scene video
   - `music.<ext>` - the collected music track
   This mirrors the established project.json format but without a slug/title - the timestamp IS the identity.

5. **Pruning: newest 15 kept.** After each Save, list saves sorted by name (timestamp), remove oldest beyond 15, delete their folders entirely.

6. **UI placement:** Save-version button + label input + Load-saved button appear in the global-mode toolbar (`#ctlBar`), only when `PROJECT` is null (not in project mode). The label input is a small text field pre-filled with empty string since Max accepted auto-naming.

---

## CURRENT STATE

### Done
- **Server endpoints added** (`slideshow_server_v01.py`, lines ~770-850 area):
  - `GET /api/music_saves` - lists all saves with metadata
  - `POST /api/music_save_version` - collects staged files + writes save.json, prunes to 15
  - `POST /api/music_save_load` - copies saved media to temp staging under new sid, returns {sid, offset, points}
  - `MUSIC_SAVES_DIR` constant (alongside `MUSIC_PROJECTS_DIR`)
  
- **UI added** (`music_editor.html`):
  - "Save version" button + label text input in global toolbar
  - "Load saved..." button in global toolbar
  - `saveVersion()` function - POSTs to `/api/music_save_version` with sid + label + offset + points, then alerts result
  - `loadSave()` function - GETs `/api/music_saves`, shows list with Load buttons; on Load click, POSTs to `/api/music_save_load`, then sets `musicOffset`, calls `restoreCurveForDuration(true)`, loads video/audio from the returned staged URLs
  - `relativeTime()` helper for displaying "2 min ago" etc.

- **Committed + pushed to master** (`git commit` with full message, `git push origin master` successful).

- **Server restarted** - old PID 22852 killed, new PID 12636 running on port 8790. Verified live: `curl localhost:8790/api/music_saves` returns `{"saves": []}`.

- **Verified:** Only one save exists on disk anywhere - the old standalone `uei_starseeds_pitch` in `music_projects/`. Zero scene music saves. The global tab was using browser `localStorage` only, explaining the total loss.

### In flight
Nothing actively in flight. The feature is complete and awaiting Max's test.

### What was NOT done
- No tests written. Max will test manually by using the buttons.
- No changes to `music_projects_method_v01_tomemex.md` doc (the method doc for the older D40 system).
- No backups of the files before editing (they're versioned in git).

---

## EXACT NEXT STEP

**Max needs to open the Music tab and test the Save/Load cycle:**

1. Go to `http://localhost:8790/music` (the global Music tab, NOT project mode)
2. Load a finished scene video + a music track (drag-drop or file inputs)
3. Adjust the offset, draw/anchor the volume curve points
4. Optionally type a label in the new text box
5. Click **"Save version"** - should see "Saved" alert
6. **Reload the page** (simulates losing session) or just clear/reload
7. Click **"Load saved..."** - should see the saved version listed
8. Click **Load** on that version
9. Verify: the video appears, music loads, offset is correct, **volume curve points are restored**

After Max confirms it works, the next task is to **start SC11** - the original reason for this detour.

---

## OPEN QUESTIONS (awaiting Max)

1. Does the Save/Load cycle work end-to-end? (Curve restoration is the critical test - the code calls `restoreCurveForDuration(true)` after load, which should rebuild the shark-tooth UI from the saved `points` array.)

2. Does Max want a **"Delete"** button per saved version in the Load list? Not implemented yet - only auto-pruning on Save. If he wants manual cleanup, that's a small addition.

3. Does Max want the label to be **required** or **optional**? Current behavior: empty label is allowed (just stores the timestamp).

4. Does Max want the saves path to be displayed anywhere (e.g., "Saved to ...")? Currently the alert just says "Saved: <timestamp> <label>".

---

## KEY PATHS, IDS, NAMES

| What | Path/Value |
|---|---|
| Sound assembly data root | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\sound_assembly\data` |
| Music saves directory | `.../data/music_saves/<timestamp>/` |
| Save file | `.../music_saves/<timestamp>/save.json` |
| Collected video | `.../music_saves/<timestamp>/video.<ext>` |
| Collected music | `.../music_saves/<timestamp>/music.<ext>` |
| Server file | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` |
| Editor file | `C:\moma\sc10\sound_assembly\code\music_editor.html` |
| Server port | 8790 (no watcher - **manual restart required**) |
| Current server PID | 12636 |
| Git branch | master (committed + pushed) |
| D51's signature | ??? D51 ? |
| localStorage key (global) | `moma_music_overlay_v1` |
| Temp staging | `%TEMP%/moma_music_export/{sid}_{role}.{ext}` |
| Old projects dir | `.../data/music_projects/` (contains only `uei_starseeds_pitch/`) |
| Method doc | `C:\moma\sc10\sound_assembly\code\music_projects_method_v01_tomemex.md` |

---

## GOTCHAS

1. **No auto-restart on the server.** Any edit to `slideshow_server_v01.py` requires manually killing the process and restarting: `taskkill //PID <pid> //F` then `pythonw slideshow_server_v01.py &`. The new PID is 12636.

2. **Global tab uses localStorage for session identity.** The `sid` is a random hex string stored in `localStorage` key `moma_music_overlay_v1`. If Max clears localStorage, the tab loses its link to staged media. The Save/Load system is designed to survive this - media is collected in `music_saves/` independently of localStorage.

3. **Staging is per-session, temp directory.** When you Load a saved version, the files are copied BACK into temp staging under a NEW sid. This re-uses the existing waveform/export pipeline. But it means the media exists in two places (the permanent `music_saves/` and the ephemeral temp staging).

4. **Pruning only happens on Save, not on Load or startup.** If Max saves exactly 15 versions, number 16 triggers deletion of the oldest one.

5. **No duplicate detection.** Saving the same setup twice (same video, music, offset, curve) creates two timestamp-named folders. This is intentional - "not always the latest version is the best" implies you might want multiple snapshots of similar states.

6. **The only existing save** (`uei_starseeds_pitch` in `music_projects/`) is NOT migrated or touched. It's in a different directory and a different format (project mode). The new saves are completely separate.

7. **Max sees only merged master** (HARD RULE #1). All changes were committed and pushed to `master`. The worktree `wonderful-liskov-dcda0b` is on master. Max doesn't need to switch branches.

8. **The prompt "Don't forget to save the curve" appeared duplicated** due to a UI bug on Max's side - the operative intent was the single command "Don't forget to save the curve, and do it!" (doit22). The curve IS saved in every version's `save.json` as the `points` array.
