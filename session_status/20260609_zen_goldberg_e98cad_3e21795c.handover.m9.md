# Scribe handover - milestone 9 (~142K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# cwd: C:\moma\.claude\worktrees\zen-goldberg-e98cad
# written: 2026-06-09 12:52:02 by claude-opus-4-8

# HANDOVER - B-roll Shuttle Clips (Branch: pod-on-black-overlay)

## GOAL (in Max's words)
Two b-roll clips for the movie: one of the **shuttle leaving Titan station**, one of the **shuttle arriving to Earth orbit station**. Both silent (music added later). The shuttle is "our fancy antigravity shuttle" - must stay faithful to its shape, with **no chemtrail / no exhaust plume**.

This specific branch is a new idea Max just opened: **render the pod on a transparent or black background - just the movement - in Wan, then overlay it onto a background plate.** In his words: *"do pod on transparent or black and overlay. that's cool."*

Max's reasoning for this approach over a simple at-home overlay: he wants **more than linear motion** - a plain 2.5D composite move (scale + slide) felt too limited to him. Letting Wan generate the pod's motion in isolation (against black/transparent) gives richer movement, while the black/transparent background sidesteps the thing Wan keeps ruining - it can't reinvent a station or add chemtrails if there's nothing in the frame but the pod.

## DECISIONS + WHY
- **Wan2.6 i2v alone failed** after ~10 hours of Max's effort. It reinvents the antigravity pod as a generic NASA shuttle and adds a chemtrail. Max: "Wan's output is laughable."
- **Kling was already tried by Max and was "a disaster"** - do NOT propose Kling as the fix.
- The Assistant initially blamed the *source still* (pod too small/ambiguous), but **Max explicitly corrected this: "the input was good."** The pod in the source still IS the correct shape; the failure is engines redrawing it during motion. Do not re-litigate the input quality.
- **First+last-frame interpolation** (feed two of our own renders as start/end keyframes, AI only fills the middle) was discussed and Max said "ok let's try" - but he then interrupted and pivoted to THIS branch instead. Interpolation is a parked sibling idea, not this branch's task.
- **A separate session owns the "closeup still ? animate ? reverse" path** (build a big portrait still of the pod with Anna + Driver facing camera through the canopy, animate it pulling toward the station, then reverse for the arrival). That is NOT this session's job. This session = genuinely *other* options. Don't touch that path.
- Pure-compositing (cut pod, scale+slide over plate) was offered but Max found it too linear - hence this branch's hybrid: Wan-generated motion on black, then overlay.

## CURRENT STATE
- Branch made for the pod-on-black/transparent idea. **Nothing fired yet on this branch.** No firing without an explicit "go" from Max.
- Earlier this session: two silent v01 clips were fired and rendered cleanly (no errors) but the motion/shape was wrong (NASA-shuttle drift + chemtrail) - these are the rejected v01:
  - **2743** = leaving Titan (src `titan_leave_v08...png`)
  - **2744** = arriving Earth orbit (src `sc09_approach_v11_a.png`)
- Worklog milestones already logged for the v01 failure and the engine research.

## EXACT NEXT STEP
Set up a test for the branch idea: get the antigravity pod (canonical shape, plate **873**) onto a **black or transparent background** as a source still, then fire **one** silent Wan2.6 clip animating just the pod's motion (e.g. pod moving/receding) against that empty background. Then Max overlays it on a background plate to judge. Confirm whether Max wants black vs transparent (alpha) - transparent needs a format/pipeline that preserves alpha through Wan, which may not be supported; black is the safe fallback (key it out later). **Wait for Max's go before firing.**

## OPEN QUESTIONS AWAITING MAX
- Black background or true transparent/alpha? (Transparency through Wan2.6 may not survive - likely produce on black and key later.)
- Does he want to start from plate 873 (pod over planet - has a background already, would need the pod isolated onto black first), or from a fresh pod-on-black still?

## KEY PATHS / IDS / COMMANDS
- cwd: `C:\moma\.claude\worktrees\zen-goldberg-e98cad`
- Code dir: `C:\moma\sc10\combo_runner\code`
- DB access: `from moma_db import D1Client; d1.query_sql(...)` (the working method is **`query_sql`** - NOT `query` or `query_rows`). Also `from moma_db import connect_db, fire_job`.
- Wan2.6 silent-clip worker: `combo_wan26_worker.py` - claims jobs where `output_status='queued' AND engine='wan26'`. Resolves `source_image` by **absolute Windows path**. Does one job at a time (~1-3 min each). Worker PID file: `../data/wan26_worker_pid.txt`.
- Arrangement (the movie): **sc9-arr01** - clips must land here.
- Canonical pod shape: **`shape:shuttle_ext`, plate 873** = `shuttle_v148a_bottom_bulge_a.png` (the correct antigravity bean-pod; big crisp version shows Anna + Driver facing camera through canopy). Lives under `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\interiors\shuttle\`.
- Faces: **Anna = plate 4**, **Driver = plate 1040**.
- v01 source stills (under `...\kazarian_episode\ships\space\`): `titan_leave_v08_mirrored_b_redo...png` (departure), `sc09_approach_v11_a.png` (arrival).
- Viewer links: `http://localhost:8779/clipper?ids=...` (silent clips) and `/lipser?ids=...` (audio/lipsie path).
- Everything-search tool: `C:\claude_base\tools\es\es.exe`.
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`. Status report: `session_status.py report "..."`.

## GOTCHAS / DEAD ENDS RULED OUT
- **Do not suggest Kling** - Max already tried it, disaster.
- **Do not blame the source still / call the input ambiguous** - Max corrected this firmly. Input is good; the engine's redraw-during-motion is the real failure.
- **Silent clips = the clip/Wan2.6 lane, NOT the lipsie/audio lane.** Music added later.
- The `b00` tag is a **version** tag, not a b-roll tag - it's noise when searching.
- Most clips in the shuttle group have Anna/Driver talking; only a few are pure exterior b-roll.
- v01 clips 2743/2744 are rejected - don't present them as candidates.
- Near compaction (~169K; was ~142K at last note) - log milestones before long operations.
- This is exploratory: **no firing until Max explicitly says go.**
