# Scribe handover - milestone 1 (~134K tokens)
# session: 20260625_relaxed_franklin_b08c5c_bb37e216
# cwd: C:\moma\.claude\worktrees\relaxed-franklin-b08c5c
# written: 2026-06-25 13:57:43 by deepseek-v4-pro

# HANDOVER - "Four variations: turn toward planet, more royal, straighter, different lighting"

---

## GOAL (in Max's own words)
Make four variations of the image at `sc_window_pan_right_v01_B_v01.png`, with these changes:
- Characters turn **toward the planet**
- Posture: **more straight, more royal**
- **Change the lighting**
- Use **proper canonical inputs** - do NOT use derivative/variation images as sources. Start fresh from the registry-resolved plates that built the original, then modify the prompt.

---

## DECISIONS + WHY
- **"Proper inputs, not derivatives"** ? Max wants prompt variations from the canonical plates (the character/location/scene arrangement as registry-resolved assets), NOT img2img variation runs on the output PNG. This means: find the original arrangement that produced `sc_window_pan_right_v01_B_v01.png`, then fire 4 *new* generations with altered prompts.
- **Assistant identified** that "c470" (which started the thread) appears orphaned - the D1 `jobs` table showed `id=470` with an empty `output_file`, and `legacy_plate_id=470` pointed to a shuttle exterior (wrong scene). So c470 is not the source of this image.
- **The actual source** is the arrangement behind `sc_window_pan_right_v01_B_v01` - assistant was mid-investigation when interrupted, querying D1 to find the originating arrangement ID, and reading code to understand `fire_job` and `get_current_arrangement`.

---

## CURRENT STATE
- **Nothing has been generated.** No image variations were fired.
- The assistant was in the discovery phase: finding the canonical `arrangement_id` that produced the target PNG.
- Assistant had queried D1 for arrangements matching `output_file` ? no result yet visible.
- Assistant was reading `moma_db.py` functions (`fire_job`, `get_current_arrangement`, `app_state`) - likely to understand how to submit a job with the canonical arrangement + a modified prompt.

**What is known:**
- Target image: `sc_window_pan_right_v01_B_v01.png`
- Character 1: `anna` / Character 2: `ishtab` (from an earlier query hit on job 470 mentioning those roles)
- Scene: likely `window_pan_right` variant
- The PNG is served from `http://localhost:8779/still/` - local combo_runner is running.

---

## EXACT NEXT STEP
1. **Find the canonical arrangement** that built `sc_window_pan_right_v01_B_v01.png`. Query D1 for the arrangement row where `output_file` matches that filename, or trace it through the scene/role tables:
   ```sql
   SELECT id, role, scene_id, prompt_raw, output_file FROM arrangements WHERE output_file LIKE '%sc_window_pan_right_v01_B%'
   ```
2. **Extract its canonical inputs** - the scene plate, the character plates (anna, ishtab), lighting setup, and the `prompt_raw` that was used.
3. **Craft 4 new prompts** based on the original prompt, adding:
   - "facing toward the planet", "turned toward the planet"
   - "upright posture, regal bearing, royal stance, straight-backed"
   - "altered lighting" (e.g. rim light, golden hour, dramatic side light, etc.)
4. **Fire 4 new jobs** using whatever `fire_job` / combo_runner API the system uses - passing the same plates but with the modified prompts. Do NOT use the output PNG as an input.
5. Output the 4 resulting image URLs when complete.

---

## OPEN QUESTIONS (awaiting Max)
- **What kind of lighting change?** "A little bit" is vague - more dramatic? Warmer? Cooler? The prompt modifications should reflect some variety across the 4 (e.g., golden glow, harsh contrast, soft ambient, backlit from planet).
- **The planet** - what planet is visible through the window? Is "the planet" part of the scene plate already, or does it need to be added via prompt? The background plate likely already includes it, but the prompt should make the characters *engage* with it.

---

## KEY PATHS / IDS
| What | Value |
|---|---|
| Target PNG | `sc_window_pan_right_v01_B_v01.png` |
| Local stills URL | `http://localhost:8779/still/` |
| App code | `C:\moma\sc10\combo_runner\code\moma_db.py` |
| Working dir | `c:/moma/sc10/combo_runner/code` |
| Characters | Anna, Ishtab (two-shot) |
| Scene variant | `window_pan_right_v01` |
| D1 client class | `D1Client` (in moma_db.py) |
| Key functions | `query_sql()`, `fire_job()`, `get_current_arrangement()` |

---

## GOTCHAS / DEAD ENDS RULED OUT
- **c470 is a red herring.** The user used "c470" as a conversation starter, but job 470 in D1 has no output PNG. Job 1847 (legacy 470) is a shuttle exterior - wrong scene entirely. Don't chase c470.
- **Do NOT use the existing PNG as an img2img input.** Max explicitly ruled out derivatives/variations - this must be fresh generations from canonical plates.
- The `arrangement_id` was not successfully retrieved before interruption - it's still an unknown that needs resolving.
