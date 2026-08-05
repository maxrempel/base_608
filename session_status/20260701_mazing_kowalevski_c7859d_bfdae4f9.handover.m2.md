# Scribe handover - milestone 2 (~164K tokens)
# session: 20260701_mazing_kowalevski_c7859d_bfdae4f9
# cwd: C:\moma\.claude\worktrees\amazing-kowalevski-c7859d
# written: 2026-07-01 12:45:06 by deepseek-v4-pro

# HANDOVER - D-80: Fix Blank Input-Image Strip in Image Popup

## GOAL (Max's words)
> "Somebody just broke the visibility of the inputs in the pop-up, image pop-up. I opened the image pop-up from Imgur. But the thing is invisible in the, the inputs, the bottom strip of inputs, input images is broken. Could you please fix it?"

Max opened the image popup for job **s3087** (sc11_arr02, a 12-ref concept_strip) in the Imager and the bottom reference-image strip rendered blank boxes - the boxes and labels ("ref 1".."ref 12") were present, but the thumbnail images inside were invisible.

## DECISIONS MADE + WHY

### Root cause diagnosis
Jobs **3086-3089** (batch=None, engine=wan22, no label - produced by the redo/refire UI flow, not the D52/D55 fire scripts) store **bare basenames** in `plate_recipe.ref_paths` (e.g. `"sc11_heights_v16.png"`, `"anna_approved_headshot_white_cloak.png"`). Script-fired jobs (3080-3085) store **full absolute paths** and displayed fine.

The `/file` endpoint in `combo_gui.py` joined paths directly under `KAZARIAN_ROOT` top-level - bare basenames resolved nowhere there (files live in subfolders: `output_stills/`, `characters/<name>/`, `ships/space/`, etc.). All 12 thumbnails 404'd, and the `onerror` handler in `popup.js` faded them out.

### Fix approach chosen
Two layers were considered:
1. **Fix the `/file` server endpoint** to resolve bare basenames by searching project asset roots ? fixes ALL broken images including future ones; exact-basename match is legitimate since production filenames are unique.
2. Fix the redo/refire producer flow to store KAZARIAN-relative paths (root-cause hardening).

**Layer 1 was implemented** - it's the single-point fix that makes the strip render immediately for existing broken jobs and any future basename recipes. Layer 2 was left as optional hardening.

### Implementation
Added a **module-level basename index** (`_build_basename_index()`) to `combo_gui.py` after the THUMBS setup (~line 256). It walks the 7 standard asset directories under `KAZARIAN_ROOT` (`output_stills`, `characters`, `ships`, `interiors`, `scenes`, `props`, `references`) and builds a `dict[str, str]` mapping basename ? full absolute path. Cached once at module load.

Modified the `/file` endpoint's 404 branch (~line 1940): before returning 404, checks if the requested path is a bare basename (no path separators), and if so looks it up in the index. On hit, serves the file; on miss, falls through to 404 as before.

## CURRENT STATE - DONE ?
- `combo_gui.py` basename-index helper added and wired in.
- All 12 refs of s3087 verified to resolve (HTTP 200) via `curl`.
- Temp probe file `_d80_probe.py` deleted.
- Commit `7b2ae8e` pushed to master: *"Fix blank input-image strip in image popup (bare basename resolution)"*
- **Fix is live.** Refreshing/reopening the popup for s3087 shows the thumbnails.

## EXACT NEXT STEP
**None - the task is complete.** Max should reopen the image popup for s3087 (or any of 3086-3089) to confirm the strip renders. If he reports it still broken, next diagnostic step: check browser cache, verify the COMBO_API URL in `popup.js` resolves to port 8779, or check for a stale server process.

## OPEN QUESTIONS
- Should the redo/refire producer flow also be patched to store KAZARIAN-relative paths instead of bare basenames? (Root-cause hardening - not urgent, the server-side fix covers it.)
- The `_d56_refire_s3068.py` file in the working tree is not mine and was left uncommitted - needs triage (may be an in-progress fire script from another session).

## KEY PATHS / IDs / COMMANDS
| What | Value |
|---|---|
| Broken job | s3087 (also 3086, 3088, 3089 - all batch=None, engine=wan22) |
| Broken recipe type | `concept_strip` with 12 bare basenames in `ref_paths` |
| Fixed file | `C:\moma\sc10\combo_runner\code\combo_gui.py` (lines ~256-290 new index, ~1940 endpoint patch) |
| Popup code | `C:\moma\sc10\shared_ui\popup.js` (read-only - no changes needed) |
| Popup CSS | `C:\moma\sc10\shared_ui\popup.css` |
| Server port | 8779 (`COMBO_API` in popup.js) |
| Database | Cloudflare D1 via `moma_db.py` `D1Client` (methods: `get_job`, `query_sql`, `execute_sql`) |
| Project root | `KAZARIAN_ROOT` from `paths.py` |
| Commit | `7b2ae8e` on master |

## GOTCHAS
- `D1Client` has no `.query()` method - use `.query_sql()` or `.get_job()`.
- Bash heredocs eat Python backslashes - write temp `.py` scripts for multi-line Python probes.
- The recent commit `7b2ae8e` that added `_renderArrLines` (vocal-lines panel) looked suspicious but was **not** the cause - the strip bug predates it and is purely a server-side path-resolution issue.
- The `/plate/{id}` endpoint (for legacy plate IDs) was not the problem; the strip wasn't using plate IDs at all (labels showed "ref N" not "plate N").
- `popup.js` `_renderRefStrip` builds img URLs with `/file?path=` only when `ref_plate_ids` is absent - that's the code path hit by these jobs, and it's correct; the data (bare basenames) was the problem.
- The working tree had an unrelated file `_d56_refire_s3068.py` - left untouched; only `combo_gui.py` was committed.
