# Scribe handover - milestone 2 (~166K tokens)
# session: 20260621_eautiful_williams_0dce4f_22fe15f0
# cwd: C:\claude_base\.claude\worktrees\beautiful-williams-0dce4f
# written: 2026-06-21 14:23:14 by deepseek-v4-pro

# HANDOVER - Media Kit Headshots + Rainbow Variations in MOMA

---

## GOAL (Max's words)

1. **Primary**: Take two headshots (`max rempel max port 2026 dnavibe.jpg` and `max port 2023.JPG`), generate 5 alien/space gray-teal Star Trek backgrounds plus 4 additional themes (mol-bio lab, mol-bio+shamanic, computer AR, celestial rainbow lightworker) - all preserving Max's face exactly. Create a **new arrangement/scene that is NOT the movie**. All outputs in one flat **undivided** folder. Check in as D50.

2. **Rainbow branch**: From `rainbow.jpg`, make abstract early-morning variations - color and shape only, no faces/dolphins/figures, plants and sky OK.

3. **CURRENT CRISIS (last user message)**: Images are being created on disk but are **NOT visible in MOMA**. Max says: "You broke something. Or moma is broken. You might have classified them wrongly. Fix that, elegantly, using proper process. Must work in moma, properly. Maybe moma is not properly tuned for non movie images. Troubleshoot. That is a branch, register as D51."

---

## DECISIONS MADE + WHY

### 1. Quality bug - medium ? low
- **Finding**: gpt-image-2 `quality=medium` takes ~10 min/image. `quality=low` (MOMA default in `paths.py`) takes ~30-43s - Max's normal speed.
- **Decision**: Switch both scripts to `quality=low` by reading from `paths.IMAGE_QUALITY` (MOMA's single source of truth). No hardcoded params.
- **Why**: Max explicitly required MOMA defaults. Timed test confirmed low=43s, medium=~600s.

### 2. No parallelization - saved to memory
- **Finding**: Max forcefully stopped a parallelization attempt: "fuck, don't parallelize, and write to memory md that parallelization kills api."
- **Decision**: Created `feedback_no_parallel_image_api.md` and indexed it in `MEMORY.md`. Both scripts use strict sequential loops.
- **Why**: Parallel calls to OpenAI images/edits endpoint kill the API.

### 3. Flat output folder - no A/B split
- **Finding**: Original script split outputs into `output/A/` and `output/B/` subfolders.
- **Decision**: All images now go directly into `media_kit/output/` (flat). The 3 already-done images were moved up, subdirs removed.
- **Why**: Max: "all of them under media kit, undivided."

### 4. New scene `media_kit` - non-movie
- **Decision**: Created scene `media_kit` with arrangement `mediakit-max-headshot-20260621` under it. Rainbow variations go under scene `media_kit` with arrangement `rainbow-variations-20260621`.
- **Why**: Max wanted "a new arrangement - scene - which is not the movie." Precedent exists (essay_nonhier, _orphans, tao-avatar scenes are already non-movie in the DB).

### 5. Engine: gpt-image-2 `images/edits`
- **Decision**: Used the same engine as the movie pipeline - `images/edits` endpoint with a reference strip + text prompt. This preserves face/glasses/beard/vest while swapping backgrounds.
- **Why**: Validated on first output (A_space_bridge.png) - face-lock works perfectly.
- **Note**: This is NOT the 5-reference movie recipe; it's the simpler single-reference path (like `fire_essay_illos.py` pattern).

### 6. fire_job() - the only legal write path
- **Decision**: Both scripts use `moma_db.fire_job()` with proper column whitelist and job_type=`image`. No raw SQL.
- **Why**: MOMA's mandated write path. Raw INSERT INTO jobs is forbidden.

---

## CURRENT STATE

### What is done:
- Both scripts written and functional:
  - `fire_mediakit_portrait.py` - 9 themes ? 2 inputs (18 portraits total)
  - `fire_rainbow_variations.py` - 6 abstract rainbow variations
- Scripts wired to `paths.py` defaults (quality=low, gpt-image-2, 1536?1024)
- At least 8+ images exist on disk in `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\output\`
- No-parallelization memory saved

### What is broken (THE ACTIVE CRISIS):
- Images exist on disk but are **NOT visible in MOMA's gallery/UI**.
- Max suspects: "classified them wrongly" / "MOMA is not properly tuned for non movie images."
- Max reassigned this as a **branch - register as D51**.

### Likely root causes (ranked by probability):
1. **Scene/arrangement tagging** - MOMA's gallery may filter by episode/scene hierarchy. The `media_kit` scene and its arrangements might not be picked up by the frontend query. The gallery likely expects scenes linked to the main episode or specific visibility flags.
2. **`hide_tile` flag** - `fire_job` sends `hide_tile=False` by default, but if the script isn't setting it properly, or if the scene has no tiles configured, the images may be invisible.
3. **Arrangement not linked to scene correctly** - `get_or_create_arrangement` may have the scene association, but MOMA might need additional metadata (e.g., arrangement belongs to a sequence, or scene must have episodes set).
4. **File path expectations** - MOMA's gallery may expect images under a specific path pattern that `media_kit/output/` doesn't match. The movie images live under `kazarian_episode/<episode>/<scene>/`.
5. **DB write succeeded but gallery reads stale** - D1 might have written correctly but some cache or view isn't refreshing.

### What is in flight:
- The background batch (`bub2ja8mq`) might still be running, sequentially firing remaining portraits + rainbow variations. These will also be invisible until the MOMA visibility bug is fixed.

---

## EXACT NEXT STEP (for D51)

**Register as D51**, then troubleshoot why images aren't visible in MOMA:

1. **Check the live DB state** - Query the `jobs`, `scenes`, `arrangements` tables for the `media_kit` scene and its jobs. Verify:
   - Scene `media_kit` exists with correct fields
   - Arrangement `mediakit-max-headshot-20260621` links to scene `media_kit`
   - Jobs exist with correct `arrangement_id`, `job_type='image'`, `hide_tile` flag
   - The `output_path` column matches actual disk paths

2. **Compare with a working visible arrangement** - Query a known-visible movie arrangement (e.g., from the movie episode scenes) and diff the schema - what fields make it visible that media_kit lacks?

3. **Check the MOMA gallery query** - Find the frontend or gallery endpoint that lists visible arrangements. It likely filters by episode ID, scene tag, or some visibility column. The `media_kit` scene may need to be added to an allowed list, or it needs a parent episode association.

4. **If the scene is structurally fine but MOMA filters by episode** - Either:
   - Add `media_kit` scene to an existing visible episode as a non-hierarchical scene, OR
   - Find and update whatever whitelist/tag MOMA uses for gallery inclusion

5. **Once visibility is fixed** - Verify the already-generated images appear, then ensure the running batch's new images will also appear.

---

## OPEN QUESTIONS (awaiting Max)

- Should `media_kit` live under a specific episode for gallery visibility, or should it be added to a global non-episode gallery?
- Is the gallery a Cloudflare Pages app, a static gallery generator, or something else? (Need to locate the frontend code that queries visible arrangements.)
- The running background batch - should it be stopped until visibility is fixed, or let it finish and fix visibility after?

---

## KEY PATHS & IDS

| What | Path/ID |
|------|---------|
| **Portrait script** | `C:/moma/sc10/combo_runner/code/fire_mediakit_portrait.py` |
| **Rainbow script** | `C:/moma/sc10/combo_runner/code/fire_rainbow_variations.py` |
| **Output folder (flat)** | `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/media_kit/output/` |
| **KAZARIAN_ROOT** | `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode` |
| **MOMA DB module** | `C:/moma/sc10/combo_runner/code/moma_db.py` |
| **MOMA paths config** | `C:/moma/sc10/combo_runner/code/paths.py` |
| **Photo A (landscape)** | `C:/Users/maxre/OneDrive/Pictures/max rempel max port 2026 dnavibe.jpg` |
| **Photo B (portrait)** | `C:/Users/maxre/OneDrive/Pictures/max port 2023.JPG` |
| **Rainbow reference** | `C:/Users/maxre/Downloads/rainbow.jpg` |
| **Scene name** | `media_kit` |
| **Arrangement (portraits)** | `mediakit-max-headshot-20260621` |
| **Arrangement (rainbow)** | `rainbow-variations-20260621` |
| **No-parallelize memory** | `C:/Users/maxre/.claude/projects/C--claude-base/memory/feedback_no_parallel_image_api.md` |
| **Memory index** | `C:/Users/maxre/.claude/projects/C--claude-base/memory/MEMORY.md` |
| **Background batch log** | `C:/moma/sc10/combo_runner/data/mediakit_fire.log` |
| **Rainbow batch log** | `C:/moma/sc10/combo_runner/data/rainbow_fire.log` |
| **User check-in** | D50 (original), **D51 (new branch for troubleshooting)** |

---

## GOTCHAS & DEAD ENDS

1. **Quality=medium is a ~10-min trap** - Never use medium or high without env var `MOMA_ALLOW_HIGH=1`. Stick to `paths.IMAGE_QUALITY` (default: low). Validated with timed test.

2. **Never parallelize** - OpenAI images/edits endpoint dies with concurrent calls. Sequential only. Saved to memory per Max's direct order.

3. **Python stdout block-buffers** - When redirecting to a log file with `>`, the log appears empty until the process exits. Use `-u` flag or check actual output files on disk to gauge progress.

4. **D1 is the live DB** - `combo_db.sqlite` is stale. All queries must go through `D1Client` in `moma_db.py`.

5. **`fire_job()` is the only legal write path** - Column-whitelisted, job-type-whitelisted. No raw INSERT.

6. **gpt-image-2 sizes** - 1536?1024 (landscape), 1024?1536 (portrait), 1024?1024 (square). The engine is `images/edits`, not `images/generations`.

7. **Input A is landscape, B is portrait** - Script handles staging correctly (A=1536?1024, B=1024?1536). Face-lock works on both orientations.

8. **The 3 original medium-quality images** - A_space_bridge, A_space_corridor, A_space_viewport were moved from `output/A/` to the flat `output/` folder. They may need re-firing at low quality if medium artifacts are unacceptable.

9. **The rainbow script hasn't run yet** - It was chained after the portrait script in the background command. If the portrait batch was killed or is still running, the rainbow batch may not have started.
