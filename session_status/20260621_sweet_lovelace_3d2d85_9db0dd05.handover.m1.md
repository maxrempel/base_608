# Scribe handover - milestone 1 (~129K tokens)
# session: 20260621_sweet_lovelace_3d2d85_9db0dd05
# cwd: C:\claude_base\.claude\worktrees\sweet-lovelace-3d2d85
# written: 2026-06-21 14:06:39 by deepseek-v4-pro

# HANDOVER: Max's Headshot Background Variants (MOMA D50)

---

## GOAL (in Max's own words)

Two phases, both using MOMA's gpt-image-2 engine to swap backgrounds behind his headshot:

**Phase 1 (in flight when interrupted):** Take `max rempel max port 2026 dnavibe.jpg` and generate 5 variants with an "aliens and space, Star Trek, ships" theme in gray-teal tones. Not movie scenes - new arrangement. Checked in as D50. Results to be presented to Max.

**Phase 2 (next):** Same process on `max port 2023.JPG`, then generate additional background themes:
1. Molecular biology lab
2. Shamanic additions
3. Computer artificial reality
4. Celestial spirit art in rainbow lightworker tones ("That's what I want!")

---

## DECISIONS MADE + WHY

| Decision | Reasoning |
|---|---|
| Used `images/edits` endpoint (gpt-image-2) not `images/generations` | Must preserve Max's face/pose - edits takes a reference image, generations is text-only |
| New scene = `media_kit`, new arrangement = `media_kit` | Non-movie content lives under misc scenes (confirmed by D1 query); essay, orphans, tao-avatar exist already; this is its own thing |
| Landscape orientation kept | Source photo is landscape - preserves Max's natural pose |
| Quality = medium, not low | Media kit use case deserves better than essay-illo "low" default |
| Cost = $0.31 for 5 images | Medium quality ? 5 = acceptable for this purpose |
| Mandated write path via `moma_db.fire_job()` | All MOMA image jobs must write through the standard `_fire_job` function; Jobs table columns: scene_name, arrangement, job, status, UNIQUE(scene_name, arrangement, job) |
| Fire script modeled on `fire_essay_illos.py` | Closest existing non-movie still-image script; adapted to pass reference image + custom prompts |

---

## CURRENT STATE

**Script written and fire initiated, then interrupted by user mid-execution.**

- **Fire script:** `C:/moma/sc10/combo_runner/code/fire_mediakit_portrait.py` - written, saved
- **Script parameters:** Source = `C:/Users/maxre/OneDrive/Pictures/max rempel max port 2026 dnavibe.jpg`, arrangement = `media_kit`, quality = medium, 5 prompts (aliens/space/Star Trek/ships theme in gray-teal)
- **Execution:** Script was running (`python fire_mediakit_portrait.py`) when Max interrupted - unknown whether 0, some, or all 5 jobs fired and completed
- **D1 jobs:** May have partial entries in the Jobs table - need to query before assuming clean slate
- **D50 check-in:** Done via `bcast.py whoami D50`

**Max hasn't seen any results yet** - he said "Once done, present them to me."

---

## EXACT NEXT STEPS (in order)

1. **Query D1 Jobs table** to see what (if anything) landed from the first fire:
   ```sql
   SELECT * FROM Jobs WHERE arrangement = 'media_kit' AND scene_name = 'media_kit';
   ```
   Or via Python: `D1Client().query_sql("SELECT job, status, output_path FROM Jobs WHERE arrangement='media_kit'")`

2. **Check output directory** for any completed images:
   - Look under `KAZARIAN_ROOT` (confirmed as env-var driven, paths.py) at whatever path `fire_job` writes to for arrangement `media_kit`

3. **If incomplete:** Re-run the fire script (or complete it) - `python fire_mediakit_portrait.py` from `C:/moma/sc10/combo_runner/code/`

4. **Present results to Max** - likely show the image paths, let him view them

5. **Phase 2:** Adapt the same script (or write a companion) for:
   - Source: `C:/Users/maxre/OneDrive/Pictures/max port 2023.JPG`
   - Background themes: mol-bio lab ? shamanic ? computer AR ? celestial spirit art rainbow lightworker
   - Fire, present results

---

## OPEN QUESTIONS AWAITING MAX

- How many variants per background theme in Phase 2? (Phase 1 was 5; Phase 2 might be 1 per theme, or 5 each - ambiguous)
- Preference on orientation for Phase 2? (Phase 1 used landscape; `max port 2023.JPG` may be portrait - need to check)
- Does he want all Phase 2 results at once, or incrementally?

---

## KEY PATHS / IDS / COMMANDS

| What | Path/Value |
|---|---|
| Source image (Phase 1) | `C:/Users/maxre/OneDrive/Pictures/max rempel max port 2026 dnavibe.jpg` |
| Source image (Phase 2) | `C:/Users/maxre/OneDrive/Pictures/max port 2023.JPG` |
| Fire script (Phase 1) | `C:/moma/sc10/combo_runner/code/fire_mediakit_portrait.py` |
| MOMA code root | `C:/moma/sc10/combo_runner/code/` |
| DB client | `moma_db.py` ? `D1Client()`, method `fire_job()` |
| Config | `paths.py` ? `KAZARIAN_ROOT`, `IMAGE_MODEL` (gpt-image-2), `IMAGE_SIZE`, `IMAGE_QUALITY` |
| Board check-in | `python "C:/claude_base/branch_bulletin/bcast.py" whoami D50` |
| Scene name | `media_kit` |
| Arrangement name | `media_kit` |
| Image model | `gpt-image-2` via OpenAI `images/edits` |
| Image params used | quality=medium, landscape (from source) |
| Reference recipe doc | `C:/moma/memos/moma_5ref_recipe_tomemex.md` |
| Fire job standard | `C:/moma/sc10/combo_runner/code/fire_job_standardization_tomemex.md` |
| Orientation doc | `C:/moma/memos/moma_orientation_tomemex.md` |

---

## GOTCHAS

- **Interrupted mid-fire** - the D1 Jobs table may have partial entries. Do NOT blindly re-fire; query first or risk duplicates (UNIQUE constraint on scene+arrangement+job will block duplicates, but the status check matters)
- **`images/edits` requires a reference image** - cannot use `images/generations` for this task; Max's face must be preserved, the prompt controls only the background/atmosphere
- **`fire_job()` is the only sanctioned write path** - do not write Jobs rows directly
- **Arrangements already exist for misc content** (essay, orphans, tao-avatar) - `media_kit` is a new addition, not a replacement
- **Phase 2 source is a different file** - confirm `max port 2023.JPG` exists before firing
- **Gray-teal theme was Phase 1 only** - Phase 2 themes are distinct (lab, shamanic, AR, celestial rainbow)
