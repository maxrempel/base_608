# Scribe handover - milestone 1 (~108K tokens)
# session: 20260701_ous_proskuriakova_ec37b0_9e6507fa
# cwd: C:\moma\.claude\worktrees\zealous-proskuriakova-ec37b0
# written: 2026-07-01 09:53:27 by deepseek-v4-pro

# Handover: image prompt refinement for sc11-arr02 tea-scene - comparing s3027 vs s3041

## GOAL (Max's own words)
> "So now look at the 3041 and compare them. So essentially what we need, we need these kind of chairs, three cups, actually four cups of tea, the pastries, the napkins, and wait for more."

Max wants to merge the best details from job `s3041` (the chairs, the specific tea cups / podstakannik, the pastries, the napkins) back into the `s3027` style composition for the next image generation job. They have more requirements to come; the phrase "wait for more" means the session is paused for further input.

## DECISIONS + WHY
- **Lookup method**: The assistant initially failed with inline Python calls because of shell escaping and method name mismatches. Decision: write a disposable script (`_d57_lookup.py`) that imports `moma_db.D1Client` and queries the D1 database directly. This worked cleanly and was then deleted. If you need to query the DB again for these jobs, either reuse the same pattern or call `d1.query_sql()` from a script, never from a heavily quoted shell line.
- **Comparison focus**: s3041 (v31) introduced a whole new greeting-stand composition with detailed objects. The assistant explicitly listed the additions: Vienna bentwood Thonet chairs (white), the 4 tea vessels (Werner's podstakannik / ref 11, plus 3 plain white teacups), pastries on a plate arranged on a white napkin, fresh apples in a bowl, and all four characters standing behind their chairs (overhead three-quarter angle). This is the feature set Max wants to "bring back" into the earlier seated scene version (s3027, v19).
- **No final direction yet**: Because the user clearly said "wait for more," the assistant only concluded the comparison and noted that these elements from s3041 should be retained. No new prompt has been drafted.

## CURRENT STATE
- Both job prompts have been retrieved from the D1 database.
- s3027 (job ID 3027) is **sc11-arr02 v19**: the reference image is `sc11_heights_v16.png`. The scene is four characters (Anna seated left, Ishtab standing leaning, Werner seated middle, Derek seated right) in an Art Nouveau room with a round table, low vase of forest flowers, cups of tea. All are smiling, Werner and Anna meet eyes, Derek wears a black beret and is twisted/long. Soft documentary lighting.
- s3041 (job ID 3041) is **v31**: reimagines the scene with "first meeting greeting moment," all four STANDING behind their chairs, Vienna bentwood Thonet chairs (white), 4 tea vessels (one podstakannik for Werner, three plain cups for others), pastries on a napkin, fresh apples, white napkins, overhead three-quarter angle.
- **Comparison result**: The elements to keep from s3041 are the **chairs (Thonet, white)**, **4 cups of tea (3 cups + 1 podstakannik)**, **pastries**, **napkins**, and whatever else Max adds next.

## EXACT NEXT STEP
1. **Wait for Max** to provide the rest of the description (the "more" in "wait for more").  
   The next user input will likely cover one or more of:  
   - pose (seated vs standing)  
   - table arrangement details  
   - lighting/mood tweaks  
   - any new reference images  
   - which job number or composition to start from (likely a new version building on s3027 with s3041's props).
2. Once that arrives, create a **combined prompt specification** that merges:  
   - the baseline composition & character arrangement from s3027 (or whatever Max specifies)  
   - the specific objects & chair detail from s3041  
   - any new instructions.
3. Then either craft a new output prompt and insert it into the combo-runner pipeline (e.g. via a new job entry) or discuss with Max the next steps for generation.

## OPEN QUESTIONS AWAITING USER
- Are the characters to remain **seated** (like s3027) or **standing** (like s3041)? Or a new arrangement?
- Does Derek still wear his **black beret** and remain "twisted"?
- Should we retain the **matte skin / documentary / pastel / bright light** look from s3027, or does s3041 have a different lighting scheme?
- What **background / room details** (Art Nouveau window, planet, etc.) from s3027 are still required?
- Any new **reference images** to add (beyond the existing 10-11 refs)?
- Which **job number / version** tag should the new image use?

## KEY FILE PATHS / IDs
- Database client: `C:/moma/sc10/combo_runner/code/moma_db.py`  
  Use `D1Client()` and its `query_sql()` method.
- Job ID `3027` (s3027): sc11-arr02 v19, source file `sc11_heights_v16.png`
- Job ID `3041` (s3041): v31, added the detailed objects and standing composition
- Output images: stored as files referenced by the `output_file` column; exact paths not yet needed, but can be looked up from those rows if required.

## GOTCHAS
- **Shell quoting**: Do not attempt to run a multi-layer-escaped Python oneliner with SQL inside shell commands; the D1 client's string handling can break. Always write a small temporary Python script (like the `_d57_lookup.py` approach) and execute it, then delete it.
- **Method names**: The `D1Client` exposes `query_sql(sql)`, not raw `execute_raw` or bare SQL methods without parameters. Check the source if unsure.
- **Waiting state**: This is an **active but paused** session - do NOT generate anything until Max provides the remaining details. When they do, simply resume from this handover.
