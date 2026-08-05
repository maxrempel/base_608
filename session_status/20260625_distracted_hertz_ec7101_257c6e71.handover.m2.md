# Scribe handover - milestone 2 (~151K tokens)
# session: 20260625_distracted_hertz_ec7101_257c6e71
# cwd: C:\moma\.claude\worktrees\distracted-hertz-ec7101
# written: 2026-06-25 13:59:51 by deepseek-v4-pro

# HANDOVER - D-75 Session: Window Planet Royal Variations

---

## GOAL (Max's exact words)

> "Could you make four variations of that image, make them turn towards the planet and also make them be a little more straight and more royal and change the lighting a little bit. So do variations of the prompts. Use proper inputs, not variations, don't use derivatives, start from canonic inputs."

The image in question: `sc_window_orig_B_v01.png` (a two-shot of Anna and Ishtab in a corridor with a window view, arrangement 2).

---

## DECISIONS + WHY

1. **Canonical inputs only - no derivatives.** Max was explicit. Instead of taking a previously rendered PNG and running img2img or variation-mode, we resolved the 5 canonical reference plates from the registry for arrangement 2 (Anna+Ishtab). These are the original face/body plates, not prior outputs.

2. **Arrangement 2 over arrangement 4.** Both `sc_window_orig` (arr 2) and `sc_window_pan_right` (arr 4) exist. The user initially linked `pan_right_B_v01` but corrected to `orig_B_v01`. Arrangement 2 is Anna+Ishtab (two women); arrangement 4 is Anna+Sergio (man+woman). Arr 2 matched "both women turn toward the planet."

3. **Lighting sweep as the variable.** All four variations share identical structure, posture, and composition. Only the lighting clause changes. This keeps the comparison clean and avoids confounding variables.

4. **Script approach over manual firing.** Wrote `fire_window_planet_variations.py` in the combo_runner code directory to programmatically fire 4 jobs via the existing `moma_db` D1Client. Edits were needed after a first-run error (likely missing import or method name).

5. **No commits made.** The session ended with jobs fired but nothing pushed or committed to the worktree. The script file was written but may or may not need to persist.

---

## CURRENT STATE

**Fired and queued - 4 jobs:**

| Job ID | Lighting |
|--------|----------|
| J2939  | cool planetshine |
| J2940  | warm cabin rim + cool window fill |
| J2941  | soft diffuse, low contrast |
| J2942  | hard key from above-right |

**Picks-link for review:**
`http://localhost:8779/imager?ids=2939,2940,2941,2942&title=window%20planet%204var%20royal%20turn-to-planet%20lighting%20sweep`

**Arrangement used:** arrangement 2 (`sc_window_orig`, Anna+Ishtab)

**5 canonical refs:**
1. BG: `bg_corridor_window_v01` (corridor window interior)
2. Anna face (red-haired woman, registry plate)
3. Anna body (white hooded linen cloak, hood always down)
4. Ishtab face (elderly indigenous woman, registry plate)
5. Ishtab body (colorful robes, jade beads, fabric headband)

**Prompt skeleton (shared across all four):**
- 5 refs as above
- Use EXACTLY the corridor window interior from ref 1 as background
- DO NOT CHANGE FACES - each woman exactly matches her ref
- Anna 15% taller than Ishtab (5'9" vs 5'0")
- Both women turn toward window, gazing at planet below
- Upright regal posture, shoulders back, chins level, hands clasped before them
- Calm, formal, serious
- Soft haze filter on faces, matte skin, no gloss, no specular highlights, real pores, no makeup, documentary
- Bergman / Tarkovsky / understated
- 16:9 landscape, 1536?1024, film grain
- Lighting clause is the ONLY variable between jobs

**D-75 check-in:** Done. ??? D-75, peer mode, no timer. Caught up on board - no storyboard work overlap.

**Worktree:** `C:\moma\.claude\worktrees\distracted-hertz-ec7101`
**Code root:** `C:\moma\sc10\combo_runner\code\`
**Helper script written:** `C:\moma\sc10\combo_runner\code\fire_window_planet_variations.py` (temporary, may be cleaned up)

---

## EXACT NEXT STEP

1. **Wait for J2939-2942 to finish rendering** (check the imager picks-link or query D1 for job status/output_file population).

2. **Present the four results to Max** so he can compare the lighting variants and select which direction to pursue further.

3. **Clean up** `fire_window_planet_variations.py` if it was a one-shot - or keep it if Max asks for more sweeps from the same canonical arrangement.

---

## OPEN QUESTIONS

- **None pending from Max.** He said "Thank you very much" and asked for the D-75 check-in. No follow-up questions were asked of him. The ball is in the system's court to render the four jobs.

---

## KEY PATHS / IDs / COMMANDS

- **D1 database queries:** via `python -c "from moma_db import D1Client; d=D1Client(); ..."` from `C:\moma\sc10\combo_runner\code\`
- **Arrangement 2:** `sc_window_orig` (Anna+Ishtab two-shot at corridor window)
- **Arrangement 4:** `sc_window_pan_right` (Anna+Sergio - ruled out, wrong pairing)
- **Data root:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\`
- **Output stills path:** `.../combo_runner/output_stills/`
- **Imager URL base:** `http://localhost:8779/imager?ids=...`
- **Still URL base:** `http://localhost:8779/still/...`
- **Branch bulletin:** `python "C:/claude_base/branch_bulletin/bcast.py" whoami D-75` and `catchup`

---

## GOTCHAS

- **`output_file` may be empty for some D1 rows** - a queried job row (job 470) had no rendered PNG. Don't rely on `output_file` as proof of existence; cross-check against the filesystem or the imager.

- **`moma_db.py` method names:** The transcript shows `d.query()` and `d.query_sql()` both exist. The correct one depends on context - `query_sql` takes raw SQL, `query` may be a higher-level wrapper.

- **The user corrected the image URL mid-session** - from `pan_right_B_v01` (arr 4, Anna+Sergio) to `orig_B_v01` (arr 2, Anna+Ishtab). Always confirm which arrangement Max means before firing, especially when the scene has multiple window variants.

- **Worktree is `distracted-hertz-ec7101`** - any new files or commits from this session live there, not on the main working copy. If a cold session resumes, make sure the worktree is still active or has been merged.

- **No derivatives rule:** Max explicitly rejected "variations" and "derivatives." Future requests for variations on this scene should always resolve back to the canonical registry plates, never use a previous output as input.
