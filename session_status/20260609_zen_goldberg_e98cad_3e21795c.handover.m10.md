# Scribe handover - milestone 10 (~151K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# cwd: C:\moma\.claude\worktrees\zen-goldberg-e98cad
# written: 2026-06-09 12:54:26 by claude-opus-4-8

# HANDOVER - B-roll Shuttle Clips (Pod-on-Black Branch)

## GOAL (in Max's words)
Max needs two silent b-roll clips: "one - the shuttle leaving titan station and another - arriving to earth orbit station." Music gets added later, so the clips must be **silent** (no audio path). The shuttle is "our fancy antigravity shuttle" - NOT a NASA/American shuttle, and it must have **no chemtrail/exhaust plume**, and must stay **faithful to its shape**.

Max has spent ~10 hours fighting this. His verdict: "Wan's output is laughable" at physical movement. He tried Kling already - "it was a disaster." He is now exploring alternate approaches across multiple branches.

## CURRENT BRANCH (what THIS session is doing)
We are on git worktree `zen-goldberg-e98cad`. Max explicitly scoped this branch:

> "do pod on transparent or black and overlay. that's cool."

The idea: isolate our real pod on a **black/transparent background**, feed it to Wan i2v so Wan animates **movement only** (non-linear/curved motion is fine and desired), then **luma-key the black out** and **overlay the moving pod onto a real background plate** (station / Titan / Earth). Rationale: Wan can't reinvent a scene that's just a pod on black, so the shape survives - but we still get Wan's curved/banking motion that flat compositing can't give.

**Note:** A *different/other* session owns the "closeup-still-first, then animate, then reverse" path. Do NOT pursue that here - it's claimed elsewhere.

## DECISIONS + WHY
- **Silent = Wan2.6 clip lane, not lipsie/audio path.** Worker `combo_kling_worker` is the audio path; the silent i2v lane is `combo_wan26_worker`, which claims jobs where `output_status='queued' AND engine='wan26'`.
- **Rejected: smarter engines (Kling 2.5, Vidu, Veo).** A researcher recommended Kling 2.5 Turbo Pro (first-frame faithful + negative prompt for "no plume"). Max shut it down - already tried Kling, disaster.
- **Rejected: flat home compositing alone.** Max wants "more than linear motion," which deterministic 2.5D pan/scale can't deliver - hence the pod-on-black hybrid instead.
- **Diagnosis correction:** I initially blamed the source still (pod too small a "speck" ? engines upgrade it to a NASA shuttle). Max corrected me: **"the input was good."** So the real failure is engines redrawing the pod *during motion*, not bad input. Pod-on-black removes everything Wan could redraw.

## CURRENT STATE
- **Clip 2745 = the pod-on-black v01 test. IT JUST FINISHED.** The background watcher task `b3kc73a0m` completed (exit code 0). Output file: `C:\Users\maxre\AppData\Local\Temp\claude\C--moma--claude-worktrees-zen-goldberg-e98cad\3e21795c-220f-4ba4-91a8-5b9adbaa8d28\tasks\b3kc73a0m.output`
- The cutout source was made: rembg cut the real pod off plate 873 ? dropped on a pure-black 16:9 canvas, Anna + Driver still visible in canopy, travel room to the right. Saved at the broll_work path below. I verified the cutout visually before firing - clean, pod intact.
- 2745 fired as silent Wan26 i2v, motion-only.
- **Earlier dead clips (already judged failures):** 2743 (leave Titan) and 2744 (arrive Earth orbit) - both rendered but Wan drifted them into a generic NASA shuttle WITH a chemtrail. Abandoned.

## EXACT NEXT STEP
1. **Read the watcher output file** (`b3kc73a0m.output`, path above) to confirm 2745 rendered without error.
2. **Pull up clip 2745 and look at it** - did the pod hold its shape on black? Did Wan give usable (ideally curved) motion?
3. If shape held: **luma-key the black out and overlay the moving pod onto a real background plate** (station / Titan / Earth). Then present to Max for judgment.
4. **Present 2745 to Max here** - he said "when ready present them here." Use the clipper link format: `http://localhost:8779/clipper?ids=2745&title=...`

## OPEN QUESTIONS (awaiting Max)
- Does the keyed pod motion convince him? (Whole branch hinges on this single test.)
- If it works: which background plate for each clip (Titan station departure vs Earth orbit arrival)?

## KEY PATHS / IDS / COMMANDS
- **Working dir:** `C:\moma\.claude\worktrees\zen-goldberg-e98cad`; code lives at `/c/moma/sc10/combo_runner/code`
- **DB access:** `from moma_db import D1Client; d1=D1Client(); d1.query_sql("...")` for D1 (remote); `from moma_db import connect_db, fire_job` for local sqlite. (Note: method is `query_sql`, NOT `query` or `query_rows` - wasted several calls discovering this.)
- **Active clip:** 2745 (pod-on-black)
- **Dead clips:** 2743, 2744
- **Arrangement (the movie / correct home):** `sc9-arr01`
- **Canonical pod shape:** `shape:shuttle_ext`, **plate 873** = `shuttle_v148a_bottom_bulge_a.png` (the correct antigravity bean-pod with Anna + Driver in canopy). Faces: Anna = plate 4, Driver = plate 1040.
- **Pod-on-black cutout:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\ships\space\broll_work\pod_on_black_v01.png`
- **Plate 873 source:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\interiors\shuttle\shuttle_v148a_bottom_bulge_a.png`
- **Bad old stills (the dead clips used these):** `ships/space/titan_leave_v08_mirrored_b_redo...png` (departure), `sc09_approach_v11_a.png` (arrival)
- **Worker:** `combo_wan26_worker.py`, claims `output_status='queued' AND engine='wan26'`; resolves `source_image` by **absolute Windows path** - always pass full paths. PID file: `../data/wan26_worker_pid.txt`. Wan2.6 runs **one job at a time**, ~1-3 min each.
- **File search tool:** `/c/claude_base/tools/es/es.exe` (Everything CLI)
- **Cutout tool:** rembg (Python, available locally)
- **Worklog / status:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` and `session_status.py report "..."`
- **Clip viewer:** `http://localhost:8779/clipper?ids=...&title=...`

## GOTCHAS / DEAD ENDS RULED OUT
- **Wan2.6 single-frame i2v on a pod that's small/ambiguous = it redraws into a NASA shuttle + chemtrail.** Confirmed twice (2743, 2744).
- **Kling - already tried, disaster.** Do not propose it.
- **Smarter generative engines in general** - Max is skeptical; he wants the pod-on-black hybrid, not another model.
- **Pure flat/linear compositing** - rejected, Max needs non-linear motion.
- **Don't pursue the "closeup still ? animate ? reverse" path** - that's the *other* session's branch.
- The corrected understanding: **input was fine; the engine's redraw-during-motion is the enemy.** Pod-on-black is the chosen fix because it leaves Wan nothing to wreck.
