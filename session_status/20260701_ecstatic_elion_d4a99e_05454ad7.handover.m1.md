# Scribe handover - milestone 1 (~126K tokens)
# session: 20260701_ecstatic_elion_d4a99e_05454ad7
# cwd: C:\moma\.claude\worktrees\ecstatic-elion-d4a99e
# written: 2026-07-01 10:03:34 by deepseek-v4-pro

# HANDOVER - D57 (sc11 table arrangement image generation)

---

## GOAL (Max's words)

Max wants a final reference image for Scene 11, arrangement 02 - the four characters (Werner, Derek, Anna, Ishtab) at a tea table in an Art Nouveau room. Specifically:

- **White Vienna bentwood Thonet chairs** (curved frames, round cane seats, painted clean white) - from s3041
- **Smaller round table** - 4 chairs placed symmetrically around it
- **Werner and Derek SEATED** at the table
- **Anna and Ishtab STANDING** behind their chairs (just arrived / first-meeting greeting moment)
- **4 tea vessels**: Werner gets a podstakannik (Russian metal tea-glass holder), the other 3 get plain white teacups on saucers
- **Pastries** on a plate arranged on a white napkin
- **White napkins** neatly folded
- **Fresh apples** in a small bowl
- **Low vase of forest flowers** as centerpiece
- **Art Nouveau interior** with curved window and planet visible (from p1189 / earlier room refs)
- **Height proportions reference** always included (sc11_heights_v16.png)
- **All 8 portrait refs** (face + body for each of the 4 characters) - faithful face similarity must be preserved
- Derek always wearing a BLACK BERET
- Matte skin, documentary, soft pastel, gentle bright light
- Werner and Anna meet eyes; all four happy and friendly, smiling warmly

---

## DECISIONS MADE + WHY

1. **12 refs used in fire attempt (v34)**: 1 height ref, 1 p1189 interior backdrop, 2 previous images (s3027 + s3041), 8 portraits (4 faces + 4 bodies). Max explicitly asked for both previous images plus all portraits plus height ref.

2. **p1189 accepted as interior backdrop** even though it's technically a station exterior (`titan_station_v04_artnouveau_legs_a.png`). D57 noted the discrepancy but Max said "use this as the interior backdrop" so D57 used it. This may need revisiting - the actual Art Nouveau room from s3027/s3041 refs is what Max wants the room to look like.

3. **Detached execution**: Max interrupted the inline fire and instructed detached run (`nohup python -u ... &`) because it was taking too long. Standard practice for long API calls.

4. **Speed bottleneck identified**: 12 PNG refs = ~26 MB raw (~35 MB base64-encoded on the wire to OpenAI). Each ref is ~1536x1024 at ~2 MB. Portraits don't need full resolution - downscaling to 512px would cut total to ~5-8 MB. Also the previous-image refs (s3027, s3041) are essentially "style guidance" and could potentially be dropped if the prompt is detailed enough - saving another ~4 MB.

---

## CURRENT STATE

**v34 (job 3086) landed** - `sc11_arr02_v34.png`. DB registered manually after the detached script failed to register (missing `conn` arg to `fire_job`).

**What v34 got right:**
- Werner and Derek seated, Anna and Ishtab standing behind chairs
- White chairs around a small round table
- Art Nouveau room with planet window
- Derek in black beret
- Flowers, pastries visible
- Overall composition matching the brief

**What v34 got wrong / needs fixing:**
- Only **3 cups** visible (Max asked for 4: 1 podstakannik + 3 teacups)
- Chairs are too **plain** - don't read as Vienna bentwood Thonet from s3041
- General prompt refinement needed for table objects and chair style

**Temp files cleaned**: `_d57_fire.py` and `_d57_fire_log.txt` were deleted after the fire completed. The fire script will need to be recreated for the next attempt.

---

## EXACT NEXT STEP

1. **Fire a revised version** focusing on fixing the chair style and table objects:
   - Strengthen prompt language for "Vienna bentwood Thonet chairs, curved wood frames, round cane seats, painted clean white"
   - Emphasize "4 tea vessels: one ornate metal podstakannik for Werner, three plain white teacups on saucers for the others"
   - Consider refs from s3041 more prominently for chair/table styling

2. **Speed optimization** (if Max wants): Downscale ref images before upload - portraits at 512px are sufficient. D57 already suggested this and Max was interested. The combined ref size dropping from 26 MB to ~8 MB would cut API upload time significantly.

3. **Consider whether p1189 is the right backdrop** - it's a station exterior. The room interior from s3027/s3041 may be what Max actually wants. Clarify with Max if the returned v34 room looks right.

---

## OPEN QUESTIONS FOR MAX

- **Is p1189 (station exterior) the right backdrop, or should we use the Art Nouveau room interior from s3027/s3041 instead?** The room in v34 came from p1189 which is technically an exterior shot. Max may want the curved-window interior room from previous images.

- **Downscale refs for speed?** Max expressed interest in why the fire was slow. The 12-ref upload to OpenAI is the bottleneck. D57 offered to downscale portraits and/or drop the full previous-image refs. Awaiting Max's decision on this for the next fire.

- **All four standing vs. two seated + two standing?** v34 has Werner/Derek seated and Anna/Ishtab standing (as Max instructed). Confirm this is the desired dynamic for the final image, or if all four should eventually be seated in a later version.

---

## KEY PATHS, IDs, AND NAMES

| What | Value |
|---|---|
| **Latest result** | job 3086, `sc11_arr02_v34.png` |
| **Output path** | `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/scenes/scene10_images/combo_runner/data/output_stills/sc11_arr02_v34.png` |
| **Previous good ref** | s3027 = job 3027 (v19, sc11_arr02, 10 refs, tea scene) |
| **Better chair/style ref** | s3041 = job 3041 (v31, 11 refs, Thonet chairs, podstakannik, pastries, all standing) |
| **Interior backdrop** | p1189 = `titan_station_v04_artnouveau_legs_a.png` (KAZARIAN_ROOT, not OUTPUT_STILLS) |
| **Height reference** | `sc11_heights_v16.png` |
| **Canonical portraits** | 8 refs: Anna face+body, Ishtab face+body, Werner face+body, Derek face+body (plates from pre-merge legacy IDs) |
| **DB module** | `C:/moma/sc10/combo_runner/code/moma_db.py` - D1Client with `query_sql()` method |
| **Fire function** | `fire_image()` in combo_runner, accepts `ref_bytes_list` (list of bytes), NOT `ref_bytes` |
| **Image viewer** | `http://localhost:8779/imager?ids=3086` |
| **KAZARIAN_ROOT** | `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode` |
| **OUTPUT_STILLS** | `.../combo_runner/data/output_stills/` |

---

## GOTCHAS & DEAD ENDS

1. **`fire_image` parameter name**: It's `ref_bytes_list` (list of bytes objects), not `ref_bytes`. Using the wrong name causes a silent or confusing error.

2. **p1189 path is under KAZARIAN_ROOT, not OUTPUT_STILLS**: Unlike s3027/s3041 which are in the combo_runner output_stills directory, p1189 is a legacy plate stored under `kazarian_episode/ships/space/`. Path resolution needs to account for this.

3. **DB registration after detached fire**: The detached script omitted the `conn` argument to `fire_job`, so the job didn't auto-register. Had to register manually afterward. Future detached fires should pass `conn` to `fire_job`.

4. **Canonical portraits are pre-merge legacy IDs**: When looking up portraits, they're old plate IDs not in the current jobs table format. Need to use the `legacy_plate_id` or `slot_key` fields to find them.

5. **Don't inline long API calls**: Max interrupted the synchronous fire - anything taking >30s should be run detached with `nohup` and logfile monitoring. Use `tasklist | grep python` to check if the detached process is still alive.

6. **12-ref upload is slow**: ~26 MB of PNGs = ~133 seconds to OpenAI. The API processes each ref individually as base64. This is the known bottleneck. Portraits at 512px are sufficient for facial detail; no need for 1536x1024 portrait refs in a group scene composition ref.

7. **Deleted temp scripts**: `_d57_fire.py` and `_d57_fire_log.txt` were cleaned up at end of session. Any new fire attempt will need a fresh script.
