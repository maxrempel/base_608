# Scribe handover - milestone 2 (~166K tokens)
# session: 20260621_objective_brown_34df83_d06b7b43
# cwd: C:\claude_base\.claude\worktrees\objective-brown-34df83
# written: 2026-06-21 14:50:01 by deepseek-v4-pro

# HANDOVER - D57/D58 Media-Kit Image Generation (MOMA)

---

## GOAL (Max's words)

*"Preparing a headshot for the media kit - take this one and use MOMA, to generate with 5 different backgrounds - theme is aliens and space, Star Trek, ships. Make it gray-teal. Create a new arrangement - scene - which is not the movie. Check in as D50 in moma team."*

Then expanded:

*"Once done, present them to me and try same with this input [max port 2023.JPG]. Next, let's try a bg which is a mol-biology lab, then same with shamanic additions, then computer artificial reality, then I know - celestial spirit art in rainbow lightworker tones. Yay! That's what I want."*

Then further:

*"Make variations of this theme - color and shape wise but without faces or dolphins, nothing substantial, abstract, but OK for plants and sky. Make it early morning theme. [rainbow.jpg]"*

Key constraints added mid-session:
- **NEVER parallelize** the image API - it "kills api" (saved to memory)
- **Shoot all** themes (they're cheap, ~$0.315 for 5 medium, even less for low)
- **All under media_kit, undivided** (flat folder, no A/B subfolders)
- **Use MOMA defaults** from `paths.py`, never hardcode params

End of session: Max registers as **D58**, meaning a new cold session is picking this up.

---

## DECISIONS MADE + WHY

### 1. Engine: `images/edits` with gpt-image-2
- MOMA's default engine for preserving a subject and swapping only the background.
- Feeds a staged reference PNG + text prompt. Face/body/clothing preserved, background replaced.
- Verified working: first output (`A_space_bridge.png`) kept Max's face, glasses, beard, vest exactly on a gray-teal Star Trek bridge.

### 2. New non-movie arrangement: `media_kit`
- Scene: `media_kit` (created via `get_or_create_scene`), arrangement: `mediakit-max-headshot-20260621`.
- Precedent exists - MOMA already has `essay_nonhier`, `_orphans`, `sc200 tao-avatar` for non-movie stills.
- This keeps the media-kit content OUT of the movie production pipeline.

### 3. Output structure: flat, undivided
- Originally had `/A` and `/B` subfolders (per input photo). Max said *"all of them under media_kit, undivided"*.
- Fixed: all 18 portraits go into `media_kit/output/` with filenames like `A_space_bridge.png`, `B_celestial.png`.
- The 3 early images that had landed in `/A` were moved up and the stale subdir was deleted before re-firing.

### 4. Rainbow variations: separate arrangement, same scene
- Arrangement: `rainbow-variations-20260621`, output in `media_kit/rainbow_variations/`.
- Core prompt strictly forbids faces/people/figures/dolphins/animals; allows plants, clouds, sky, sacred geometry.
- Early-morning dawn palette. 6 variations (peach-gold, rose-lilac, mint-blue, golden-rings, rainbow-columns, dewy-meadow).

### 5. Quality: MOMA default = `low`, NOT `medium`
- **THE BUG**: Original script set `QUALITY = "medium"`. gpt-image-2 medium takes ~10 min/image.
- Max's normal speed is ~30 sec/image with `low` quality.
- Timed test confirmed: low = 43s (matches baseline), medium = the 10-min hog.
- Fix: Both scripts now read `paths.IMAGE_QUALITY` (the MOMA default, currently `"low"`). No hardcoded quality anywhere.

### 6. Sequential only - saved to memory
- Max: *"fuck, don't parallelize, and write to memory md that parallelization kills api"*
- Created: `C:/Users/maxre/.claude/projects/C--claude-base/memory/feedback_no_parallel_image_api.md`
- Indexed in: `C:/Users/maxre/.claude/projects/C--claude-base/memory/MEMORY.md`
- Scripts use a simple sequential `for` loop. No ThreadPoolExecutor, no asyncio, no multi-process.

### 7. Signed in as D57 (ex-D50)
- Renamed from D50 to D57 mid-session via `bcast.py whoami D57`.
- MOMA troubleshooting is a **separate branch (D51)** - D57 only does images.
- End of session Max says "Register as D58" - the next cold session will be D58.

---

## CURRENT STATE

### All 24 images are DONE and saved

**18 media-kit portraits** - flat folder:
`C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\output\`

| Input | Themes done |
|-------|------------|
| A (dnavibe selfie, 1536?1024 landscape) | All 9: space_bridge, space_corridor, space_viewport, space_hangar, space_starmap (all gray-teal Star Trek), molbio, molbio_shaman, computer_ar, **celestial** |
| B (2023 golden-hour portrait, 1024?1536) | All 9: same themes |

Face-lock verified on the celestial and space_bridge - face, glasses, beard, smile, vest all exact.

**6 rainbow abstract variations** - flat folder:
`C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\rainbow_variations\`

| File | Theme |
|------|-------|
| rv01_peach_gold.png | Peach-gold dawn |
| rv02_rose_lilac.png | Rose-lilac dawn |
| rv03_mint_blue.png | Mint-blue dawn |
| rv04_golden_rings.png | Golden sacred-geometry rings |
| rv05_rainbow_columns.png | Rainbow light columns |
| rv06_dewy_meadow.png | Dewy meadow dawn |

Abstract, no faces/dolphins/figures, plants and sky OK, early-morning palette, rainbow sacred-geometry mandalas.

### Scripts are committed + pushed

Both scripts live at:
- `C:/moma/sc10/combo_runner/code/fire_mediakit_portrait.py`
- `C:/moma/sc10/combo_runner/code/fire_rainbow_variations.py`

Commit: `mediakit portraits + rainbow variations - gpt-image-2, sequential, MOMA defaults`
Pushed to master (`git push` completed).

### MOMA DB: scene + arrangements created
- Scene `media_kit` (id created in live D1).
- Arrangements `mediakit-max-headshot-20260621` and `rainbow-variations-20260621` registered via `fire_job()`.

### Memory: no-parallelize rule saved
- `C:/Users/maxre/.claude/projects/C--claude-base/memory/feedback_no_parallel_image_api.md`
- Indexed in `MEMORY.md`.

---

## EXACT NEXT STEP

*Nothing to do - all 24 images are done, scripts committed, output folders opened. Max has the images.*

If Max wants **more variations or different backgrounds** in the new session:
- Edit `THEMES` dict in `fire_mediakit_portrait.py` to add new background prompts.
- Re-run: `cd C:/moma/sc10/combo_runner/code && python -u fire_mediakit_portrait.py`
- The script is idempotent - it skips any file that already exists in the output folder.
- Same for rainbow: edit `VARIATIONS` list in `fire_rainbow_variations.py` and re-run.

If Max wants a **completely different reference photo**:
- Add it to `INPUTS` dict in `fire_mediakit_portrait.py` (follow the pattern of A/B).
- Or write a new fire script using the same template (import paths, use `fire_job()`, sequential loop).

---

## OPEN QUESTIONS

*None left from this session. Everything Max asked for was completed.*

Potential for next session:
- Does Max want to curate/pick favorites from the 18 portraits?
- Does Max want the celestial theme applied to the second photo as well? (It already was - B_celestial exists.)
- Does Max want the outputs in a different format, resolution, or quality tier?

---

## KEY PATHS / IDs

### Input photos
| Key | Path | Size |
|-----|------|------|
| A | `C:\Users\maxre\OneDrive\Pictures\max rempel max port 2026 dnavibe.jpg` | 1536?1024 landscape |
| B | `C:\Users\maxre\OneDrive\Pictures\max port 2023.JPG` | 1024?1536 portrait |
| Rainbow ref | `C:\Users\maxre\Downloads\rainbow.jpg` | visionary lightworker art |

### Output
| What | Path |
|------|------|
| 18 portraits (flat) | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\output\` |
| 6 rainbow variations | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\rainbow_variations\` |

### Code
| What | Path |
|------|------|
| Portraits fire script | `C:/moma/sc10/combo_runner/code/fire_mediakit_portrait.py` |
| Rainbow fire script | `C:/moma/sc10/combo_runner/code/fire_rainbow_variations.py` |
| MOMA paths config (defaults) | `C:/moma/sc10/combo_runner/code/paths.py` |
| MOMA DB client (fire_job, D1Client) | `C:/moma/sc10/combo_runner/code/moma_db.py` |
| Concept arrangement (engine reference) | `C:/moma/sc10/combo_runner/code/concept_arrangement.py` |
| Essay illos (fire template) | `C:/moma/sc10/combo_runner/code/fire_essay_illos.py` |

### Config values (from `paths.py`)
- `IMAGE_MODEL` = `"gpt-image-2"`
- `IMAGE_QUALITY` = `"low"` ? **this is the normal fast path (~40s/img)**
- `IMAGE_SIZE` = `"1536x1024"` (landscape default; portrait overrides per input)
- `OPENAI_KEY_FILE` points to API key
- `KAZARIAN_ROOT` = `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode`

### Memory
| What | Path |
|------|------|
| No-parallelize rule | `C:/Users/maxre/.claude/projects/C--claude-base/memory/feedback_no_parallel_image_api.md` |
| MEMORY.md index | `C:/Users/maxre/.claude/projects/C--claude-base/memory/MEMORY.md` |

### Scenes / Arrangements in live D1
- Scene: `media_kit`
- Arrangement 1: `mediakit-max-headshot-20260621` (portrait backgrounds)
- Arrangement 2: `rainbow-variations-20260621` (abstract dawn variations)

---

## GOTCHAS

### 1. `quality="medium"` is ~10 min/image - never use it
Max expects ~30 sec/image. That's `low` quality. Medium is the 10-min hog. Both scripts now use `paths.IMAGE_QUALITY` (low) as the MOMA default. If you override quality, you must ask Max first.

### 2. Never parallelize the OpenAI image API
Max: "parallelization kills api." Scripts must use strict sequential `for` loops. No `ThreadPoolExecutor`, no `asyncio`, no multi-process. This is saved to cross-session memory.

### 3. Use `fire_job()` - never raw INSERT
`moma_db.py` has a `fire_job()` function that is the ONLY legal write path to the `jobs` table. It enforces a hard whitelist of allowed job types (`image`, `clip`, `lipsie`) and allowed columns. Raw SQL INSERT is forbidden and will be caught.

### 4. Python stdout is block-buffered when redirected
If you redirect Python output to a log file (`> file.log 2>&1`), the log appears empty until the process exits. Don't trust `tail -f` on the log - count actual output PNGs instead.

### 5. Scripts are idempotent
They skip any output file that already exists. Safe to re-run. Safe to kill and resume.

### 6. The live DB is Cloudflare D1 - not SQLite
`combo_db.sqlite` is stale. Use `D1Client` from `moma_db.py` for all queries against the live schema.

### 7. D57 (images) vs D51 (MOMA troubleshooting)
These were split into separate branches mid-session. The next session registering as D58 should be aware that if MOMA workers are being restarted (by D51 or another branch), the Python fire scripts can get killed mid-run. Since they're idempotent, just re-run them.

### 8. gpt-image-2 `images/edits` uses a staged reference
The script stages each input photo to a fixed-size PNG (matching the target size) before feeding it to the API. The staged files are in `media_kit/output/` as `max_A_dnavibe_staged.png` and `max_B_2023_staged.png` - these are temporary, cleaned up by the script. The face-lock prompt (`KEEP_CORE`) is clothing/palette agnostic to avoid biasing the background swap.

### 9. MOMA uses `arrangement` not `scene` as the production unit
When creating new content, you register an arrangement under a scene. The distinction matters because D1 schema, `fire_job`, and `concept_arrangement.py` all key off `arrangement_id`.
