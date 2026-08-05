# Scribe handover - milestone 2 (~165K tokens)
# session: 20260624_gallant_jennings_fcc500_0d65c121
# cwd: C:\moma\.claude\worktrees\gallant-jennings-fcc500
# written: 2026-06-24 14:24:00 by deepseek-v4-pro

# HANDOVER: MOMA Assemble-Video Fix (D45)

---

## GOAL (Max's words)
> "Assemble video has tons of troubles. First, it assembles poor resolution for some reason. Second, it dumps wrong videos, wrong reels into the video. It must take them from the primary spine and it takes them from somewhere else from the database completely randomly. Just re-edited, we redesigned the spine and the filters and the assemble video is using the old filters, so that's why it's completely broken. So, fix it."

Two concrete bugs to fix, both in the assemble-video renderer:
1. **Wrong reels** - assembler grabs random videos instead of the primary spine picks.
2. **Poor resolution** - output is low-res despite acceptable source media.

---

## DECISIONS MADE + WHY

### Bug 1: Wrong reels (root cause)
**Old code** (`build_primary_picks` in render_mixboard_video_v01.py): iterated per script LINE, collected ALL jobs matching that line_hash or birth_line_hash, sorted by a unified key (category rank, stars, recency), picked the first non-junk. No reel-membership filtering, no spot layout awareness. This grabbed reels whose membership didn't match the spot.

**New code**: rewrote `build_primary_picks` to:
1. Fetch the authoritative `/api/reel_membership_sc10` endpoint (server-side derived from the D1 merge_ops ledger - canonical single source of truth).
2. Build spot layout the same way storyboard_editor_v2.html does: `longestRangeFor` - each line gets the longest contiguous reel-membership range covering it. Sticky, pin-independent.
3. Per spot, pick media exactly as `groupLines()` does: STAGE 1 = newest reel whose reel_membership CSV EXACTLY matches the spot's line CSV; STAGE 2 = manually-pinned still from ST.assigned. Clips excluded entirely (match the player).
4. Return one pick per spot. No parallel re-derivation of membership - consumes the single source of truth.

**Why mirror the JS exactly**: the original fragility was re-implementing pick logic in Python independently. The fix follows the same algorithm but fetches the server's authoritative data rather than locally recomputing it.

### Bug 2: Poor resolution
**Root cause**: renderer forced 1280?720 (1.78:1) but all source media is 1.5:1 - reels are 1176?784, stills up to 1536?1024. This caused pillarboxing AND downscaling. Default quality was 'A' (veryfast/CRF 30/1400k) - tiny.

**Fix applied**:
- Target resolution changed to `1536, 1024` (1.5:1 - reels fit edge-to-edge, 1176?784 ? 1.306 = 1536?1024 exactly, no bars).
- Quality presets raised for the larger frame: C = fast/CRF 23/5000k (was veryfast/CRF 30/1400k).
- Server default quality changed from 'A' to 'C' in `/api/export_video`.

### Other design choices
- **Honest blank over wrong-reel fallback**: spots with no matching reel render black rather than silently grabbing a wrong reel. This matches Max's preference for no sloppy fallbacks.
- **Multi-line still spots get concatenated audio**: new `_concat_mp3` helper stitches per-line mp3s via ffmpeg concat demuxer (copy codec, no re-encode).
- **`collapse_merged_lipsies` deprecated but left in file** (prefixed "DEPRECATED in v10") - no longer called by main, kept for reference.

---

## CURRENT STATE

### Committed & pushed to master
- Branch: `master` (directly on C:\moma)
- Commit: `2a2f617` - "assemble-video v10: spot-based spine + native 1.5:1 resolution (D45, per Max)"
- Two files changed:
  - `sc10/sound_assembly/code/render_mixboard_video_v01.py` - VERSION bumped v09?v10, TARGET 1536?1024, new spot-based `build_primary_picks`, new helpers, quality presets raised.
  - `sc10/sound_assembly/code/slideshow_server_v01.py` - `/api/export_video` default quality 'A'?'C'.

### Verified before push
- `py_compile` passed both files.
- Ran `build_primary_picks(10)` live against the running servers: returned 11 spots matching the spine exactly (e.g., [0,1,2,3]?job 2774, [10-16]?2816, [17-22]?2806, etc.), 10 lipsie + 1 blank. No cross-spot reels.

### NOT yet done
- **Max has NOT verified the fix** - the assembled video has not been re-rendered end-to-end. He was asked at the end of the session: "Please re-run Assemble video on scene 10."
- A full render was not run from the command line (no `--scene 10 --quality C` test render). Only `build_primary_picks()` was tested programmatically.

### Unrelated noise in working tree
- `sc10/combo_runner/code/fire_mediakit_portrait.py` has unstaged edits (not our fix, was stashed during rebase and popped back). Do NOT commit this.
- ~45 untracked scratch files in sc10/combo_runner/code/ (`_d21_*.py`, `_d43_*.py`, `_spot*.py`, `fire_*.py`, `local_state/`). Ignore them.

---

## EXACT NEXT STEP

**Wait for Max to re-run Assemble video on scene 10 and report back.** He accesses it through the MOMA UI (slideshow_server serves the storyboard/mixboard pages; Assemble video triggers `/api/export_video` which spawns the renderer).

If Max reports issues:
1. Check the render log/output for any ffmpeg errors.
2. Verify the servers are running the updated code (slideshow_server:8790 must be restarted to pick up the Python changes - it loads modules at startup). This is a **critical gotcha**: Python servers don't hot-reload. If the server hasn't been restarted since the push, it's still running the old code.
3. If reels still wrong, re-run `build_primary_picks(10)` to see if membership data changed.
4. If resolution still bad, check that the renderer instance actually got the new TARGET constants (verify VERSION=v10 in the render log/manifest).

---

## OPEN QUESTIONS (awaiting Max)

- **Did the fix work?** Max needs to re-run Assemble video and confirm.
- **Is the 1536?1024 resolution acceptable?** It's 1.5:1 matching native media - no bars, no downscale. But the frame is larger than the old 1280?720, so file sizes will be bigger.
- **Is the blank spot (lines 24-28) correct?** Test run showed spot [24-28] with no matching reel renders blank. The JS storyboard player shows the same gap - this is a data issue (no reel covers that exact membership), not a renderer bug. Max may or may not care.
- **Did the servers get restarted?** Python servers need a restart to pick up the pushed code.

---

## KEY PATHS

| What | Path |
|------|------|
| Repo root | `C:\moma\` (master branch) |
| Renderer (FIXED) | `C:\moma\sc10\sound_assembly\code\render_mixboard_video_v01.py` |
| Slideshow server (FIXED) | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` |
| Storyboard editor (reference, NOT edited) | `C:\moma\sc10\sound_assembly\code\storyboard_editor_v2.html` |
| Combo runner scratch files (IGNORE) | `C:\moma\sc10\combo_runner\code\_d21_*.py`, `_d43_*.py`, `_spot*.py`, `fire_*.py` |
| Unrelated modified file (DO NOT COMMIT) | `C:\moma\sc10\combo_runner\code\fire_mediakit_portrait.py` |

## SERVER ENDPOINTS

| Endpoint | Port | What it does |
|----------|------|--------------|
| `/api/reel_membership_sc10` | 8790 (slideshow) | Authoritative reel?lines membership map |
| `/api/export_video` | 8790 | Triggers assemble-video render (spawns render_mixboard_video_v01.py) |
| `/scene_lines_manifest` | 8790 | D1 script_lines spine + audio overlay |
| `/api/storyboard_state_v2` | 8790 | Assigned line_hash?job_id map |
| `/api/jobs?filter=all&video_filter=all` | 8779 (combo_gui) | All jobs indexed by id |

## COMMANDS

Restart slideshow server (if needed):
```
cd C:\moma\sc10\sound_assembly\code && python slideshow_server_v01.py
```

Manual render test (for debugging):
```
cd C:\moma\sc10\sound_assembly\code
python render_mixboard_video_v01.py --scene 10 --quality C --out "G:\My Drive\00Main2026\00_rehearsals\test_v10.mp4"
```

Verify spots without rendering:
```
cd C:\moma\sc10\sound_assembly\code
python -c "import render_mixboard_video_v01 as R; picks, run = R.build_primary_picks(10); [print(f'{p[\"idx\"]:3d} spot_lines={p[\"spot_lines\"]} ? job {p.get(\"primary_job\")}') for p in picks]"
```

---

## GOTCHAS

1. **Python servers don't hot-reload.** If slideshow_server:8790 wasn't restarted after the push, it's still running the OLD code. This is the most likely cause if Max says "nothing changed."

2. **The v10 renderer is NOT backward compatible with the old pick dict shape.** Old manifests written by v09 have different fields. New manifests include `spot_lines` and `primary_job`. The `write_assembly_manifest` function was NOT modified (it reads the fields it needs), so old manifests won't re-render correctly with v10 - but this is a non-issue since manifests are per-render temporary artifacts.

3. **Line 28 overlap is data, not code.** Test showed line 28 in both blank spot [24-28] and reel spot [28,29] - the JS storyboard player shows the same double-coverage. This is contradictory merge_ops data, not a renderer bug. Don't "fix" this in the renderer; it must match the player.

4. **Do NOT commit `fire_mediakit_portrait.py` or scratch files.** If you need to push anything, stage specific files: `git add sc10/sound_assembly/code/render_mixboard_video_v01.py` etc. Never `git add -A`.

5. **Rebase before push.** The repo rule: `git pull origin master --rebase` before any push. D24fixer and D43 have been active on storyboard files.

6. **Max sees only master.** He runs the servers from master and verifies from the servers. No feature branches, no PRs - commit+push directly to master, then tell him to test.

7. **Reply style:** plain English, no code shown in messages to Max, ~200 chars pingpong. This handover is for a future Claude session, not for Max.
