# Scribe handover - milestone 2 (~151K tokens)
# session: 20260701_etermined_greider_50df14_6380f3c0
# cwd: C:\moma\.claude\worktrees\determined-greider-50df14
# written: 2026-07-01 12:44:20 by deepseek-v4-pro

# HANDOVER - D57, sc11-arr02 Table Scene (Max's Instruction)

---

## GOAL (in Max's words)

Create a **sc11 arrangement shot** of four characters (Anna, Ishtab, Werner, Derek) in an **Art Nouveau interior** around a **small round white table** with **four white Vienna bentwood Thonet chairs** distributed symmetrically around it. The men are seated, the women have just arrived and stand behind their chairs. The table has four cups of tea, pastries, napkins, and a low vase of forest flowers. The interior must faithfully match the reference fed (p1184 - `station_wv_n_ls.png`). Portrait fidelity must be preserved. Characters must look at each other naturally, **not at the camera, not posing**. No glamorisation. Derek must be tall with long lanky legs, wearing his black beret.

---

## DECISIONS MADE + WHY

1. **Using `fire_image` with `ref_bytes_list`** - the combo runner's `fire_image` takes a list of binary PNGs as `ref_bytes_list` (not `ref_bytes`). This is the established pattern.

2. **12-ref (later 11-ref) concept strip** - each fire packs a height reference, an interior ref, one or two style/previous-render refs, and 8 portrait refs (4 faces + 4 bodies). The order matters: ref 1 is SIZE ONLY, faces come from portrait refs only.

3. **p1184 vs p1189: database duplication discovered** - legacy plate IDs conflict with auto-increment job IDs. p1184 in the imager = legacy plate 1184 = job 3060 = `station_wv_n_ls.png` (the correct Art Nouveau interior). p1189 = legacy plate 1189 = `titan_station_v04_artnouveau_legs_a.png` (a station EXTERIOR). Max confirmed p1184 is the right one. **A branch session was spawned to fix the duplication at the database level; D57 was told to ignore it and keep firing.**

4. **Dropping old "style" refs and using the latest render as a single style ref** - Max's instruction at the end: drop refs 3 (s3027/v19) and 4 (s3041/v31) because they confused the model. Replace with the **latest produced image** (v40) so the model builds on what it just made, rather than on older, different compositions.

5. **Derek body ref** - the approved Derek body refs are all upper-body crops. Max said the standing picture is "good enough." The height reference (`sc11_heights_v16.png`, ref 1) is supposed to carry his tall proportion. The prompt was beefed up to insist on "VERY TALL, tallest person in the room, long lanky legs."

6. **"Ishtab introduces Anna" staging** - Max specified that the narrative is: Ishtab is pointing at / presenting Anna, and everyone looks at Anna with warm smiles. This replaces the earlier "looking at each other" instruction for a more specific focal point.

7. **Antiglamour** - "matte skin, real pores, no makeup, documentary, not glossy, soft pastel" used consistently. Glamorisation was noted as a recurring problem.

8. **Interior insistence** - repeated failures to use the fed interior led to increasingly strong language: "ref 2 is the MOST IMPORTANT ref for the setting," with a whole paragraph listing every element of the room (walls, niches, plants, floor, lighting, window, sofa).

---

## VERSION HISTORY (what was fired, what it fixed)

| Version | Job ID | Key Change | Result |
|---------|--------|------------|--------|
| v34 | 3086 | First attempt, 12 refs, p1189 as interior | Disaster - wrong interior (station exterior), characters facing camera, wrong boots, chairs misaligned |
| v35 | 3087 | Auto-generated (no manual fire) | **The "good one" Max liked** - but background was wrong |
| v36 | 3088 | Swapped interior to sc11_arr01_v10.png, fixed seating, Derek body to table-seated | Better interior but not p1189 |
| v37 | 3089 | p1189 as interior (ref 2) | Similar to v36, interior still not p1184 |
| v38 | 3090 | p1184 interior, s3087's exact prompt | Closer to the good v35 quality, but interior not used enough |
| v39 | 3091 | Stronger interior language, antiglamour, Derek height, circular seating | Interior partially used (sofa appeared), characters more conversational |
| v40 | 3092 | Whole paragraph insisting on room reproduction, "most important ref" | Interior closer to p1184, niches and plants visible. Derek's body still compressed |
| **v41** | **IN FLIGHT** | **Dropped refs 3+4, added v40 as single style ref. Added "Ishtab introduces Anna, everyone looks at Anna."** | **Rendering** |

---

## CURRENT STATE

**v41 is rendering detached** - fired via `_d57_fire7.py`, output logging to `_d57_fire7_log.txt`. The monitoring loop is running: it greps for "Result:" and waits.

The v41 prompt (Max's exact specification from the last turn, with his edits applied):
- 11 refs: height ref, p1184 interior, v40 style ref, 8 portraits
- Room from ref 2 with curved window, white panelled walls, niches with plants, wooden floor
- Smaller round white table, four white Thonet chairs AROUND in a circle
- Werner seated, Derek seated (tall, long lanky legs, black beret)
- Anna and Ishtab standing behind their chairs, just arrived
- Ishtab introduces Anna, everyone looks at Anna, friendly smiles
- Four cups of tea, pastries, napkins, low vase of forest flowers
- Matte skin, documentary, soft pastel, gentle bright light, 16x9 landscape

---

## EXACT NEXT STEP

1. **Check if v41 landed** - look at `_d57_fire7_log.txt`. If complete, read the PNG and present it to Max via the imager link.

2. **If still rendering** - wait for it. The monitoring bash loop may still be running.

3. **Max will evaluate v41** - the problems he was tracking:
   - Interior from p1184 fully used (whole room, not just sofa)
   - Chairs symmetrically around table, not all on one side
   - Characters NOT facing camera, NOT posing
   - Anna's face faithful to her portrait
   - Derek tall with long legs
   - No glamorisation
   - Ishtab introducing Anna, everyone looking at Anna

4. **Cleanup** - after presentation, remove `_d57_fire7.py` and `_d57_fire7_log.txt`.

5. **If v41 still has problems** - next surgical edit should be a small delta on v41's prompt, not a ground-up rewrite. Keep the 11-ref structure. Possibly: even stronger interior language, or explicit chair position instructions (degrees around the table, e.g. 0?/90?/180?/270?).

---

## OPEN QUESTIONS (awaiting Max)

- Is Derek's body ref adequate, or should a different / new full-body shot be sourced?
- The "sofa" keeps appearing - does Max want it explicitly forbidden in the prompt, or does it come naturally from p1184?

---

## KEY PATHS & IDs

- **Output stills directory**: `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/scenes/scene10_images/combo_runner/data/output_stills/`
- **Database**: D1Client in `C:/moma/sc10/combo_runner/code/moma_db.py`
- **Imager**: `http://localhost:8779/imager?ids=<job_id>&title=...`
- **p1184 interior file**: `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/scenes/scene10_images/combo_runner/data/output_stills/station_wv_n_ls.png`
- **Derek body refs**: `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/characters/derek/approved/full_body/`
  - `derek_pose_05_table_forward.png` - seated at table (upper body crop)
  - `derek_pose_01_console_front.png` - standing at console (better body visibility?)
- **Height ref**: `sc11_heights_v16.png`
- **Canonical portraits** (face + body pairs): stored in character approved folders under `kazarian_episode/characters/`
- **s3087 (v35)**: job 3087 - the "good one" Max liked, used as quality benchmark
- **v40**: job 3092 - latest completed render, fed as style ref in v41
- **v41**: job 3093 (likely) - IN FLIGHT

---

## GOTCHAS & DEAD ENDS

1. **`ref_bytes_list` not `ref_bytes`** - `fire_image` expects a LIST of bytes objects, not a single bytes object. Using `ref_bytes=` gives a cryptic error.

2. **Database ID duplication** - legacy plate IDs (e.g. 1184, 1189) clash with job IDs. The `output_file` column in `jobs` table stores relative-to-KAZARIAN_ROOT paths for some, relative-to-OUTPUT_STILLS for others. A branch session is handling this.

3. **Don't over-specify** - v37 failed because it was too rigid ("EXACTLY from ref 2, keep UNCHANGED"). v35 worked because it was softer ("inspired by refs 2, 3, 4"). But the interior still needs strong insistence - finding the right balance is key.

4. **12 refs = slow** - ~130 seconds. 11 refs with auto-shrinking = ~54 seconds. The system auto-downscales refs before upload.

5. **Derek body refs are all upper-body** - no full-height standing shot in the approved folder. The height ref carries his proportions but competes with the body ref's crop. This is a structural limitation, not a prompt fix.

6. **Chairs on one side** - the model defaults to arranging chairs in a row facing camera unless explicitly told "AROUND the table in a circle, NOT all on one side." This needs strong language, possibly degree specifications.

7. **Anna's face drifting** - the "DO NOT CHANGE HER FACE" addition helped but wasn't foolproof. The portrait refs compete with style refs that show different compositions.

8. **v35 is the quality baseline** - s3087's prompt and ref structure produced the result Max liked. Future fires should start from v35's prompt, only changing what's explicitly requested.
