# Scribe handover - milestone 1 (~129K tokens)
# session: 20260625_distracted_hertz_ec7101_257c6e71
# cwd: C:\moma\.claude\worktrees\distracted-hertz-ec7101
# written: 2026-06-25 13:55:44 by deepseek-v4-pro

# Handover: Session "distracted-hertz-ec7101"

## GOAL (Max's own words)
"Make four variations of that image, make them turn towards the planet and also make them be a little more straight and more royal and change the lighting a little bit. So do variations of the prompts. Use proper inputs, not variations, don't use derivatives, start from canonic inputs."

Max wants four prompt variations (not image derivatives) that:
- Reorient subjects toward a planet
- Make poses straighter and more "royal"
- Alter lighting
- Use canonical (registry-resolved) source plates, not already-processed images

## DECISIONS + WHY
The assistant chose to first locate the image Max referred to as "c470" before generating any prompts. Reasoning: you can't write variations without knowing the base image, its scene/arrangement, and its canonical inputs.

The assistant explored these paths:
1. **job 470** - queried by `id=470` in D1. Result: a 5-ref recipe row for `bg_window_pan_right_v01` (Anna+Ishtab two-shot). `output_file` was empty (no PNG rendered). Rejected because no rendered image exists and it's a two-shot, not matching "them facing planet."
2. **job 1847** - queried as `legacy_plate_id=470`. Result: `interiors/shuttle/shuttle_v97a_ext_a.png`, a shuttle exterior plate with no people. Rejected - doesn't match the description.

## CURRENT STATE
- **Blocked awaiting user clarification.** The assistant asked Max which image "c470" actually refers to, requesting the picks-link or actual job/lipsie ID.
- No prompt generation has started.
- No files have been modified.

## EXACT NEXT STEP
1. Wait for Max to provide the correct identifier (picks-link URL, job ID, or lipsie ID) for the image they want variations of.
2. Once identified, look up that job in D1 to find its canonical inputs (scene, arrangement, plate references).
3. Generate 4 prompt variations that:
   - Reorient subjects toward a planet
   - Make poses straighter/more royal
   - Change lighting
   - Use the canonical source plates (not derivatives of the existing image)
4. Submit or present those prompts to Max.

## OPEN QUESTIONS
- **What exactly is "c470"?** Neither `job 470` nor `legacy_plate_id 470` matches Max's description of characters that can be turned toward a planet. Max needs to clarify the identifier.

## KEY PATHS / IDS
- **D1 database access:** `c:/moma/sc10/combo_runner/code/moma_db.py` via `D1Client`
- **D1 table:** queried via `query_sql('SELECT id,role,scene_id,arrangement_id,output_file,out...')`
- **Job 470:** `bg_window_pan_right_v01`, Anna+Ishtab two-shot, no output_file (unrendered)
- **Job 1847:** `interiors/shuttle/shuttle_v97a_ext_a.png`, shuttle exterior, no people
- **Worktree:** `C:\moma\.claude\worktrees\distracted-hertz-ec7101`

## GOTCHAS / DEAD ENDS
- "c470" is not a standard D1 job ID. It may be a picks-link shorthand, a filename fragment, or a different identifier entirely. Do not assume it maps to `id=470` or `legacy_plate_id=470`.
- Job 470 has no rendered output - even if it were the right image, there's no PNG to view or use.
- Job 1847 is a shuttle exterior with zero characters - clearly not the image Max described.
- Max emphasized "use proper inputs, not variations, don't use derivatives" - so whatever workflow this is, it must resolve back to source plates from the registry, not chain off the current image file.
