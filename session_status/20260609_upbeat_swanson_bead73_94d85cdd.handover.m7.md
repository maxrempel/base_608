# Scribe handover - milestone 7 (~109K tokens)
# session: 20260609_upbeat_swanson_bead73_94d85cdd
# cwd: C:\moma\.claude\worktrees\upbeat-swanson-bead73
# written: 2026-06-09 12:31:55 by claude-opus-4-8

# HANDOVER - B-roll Shuttle Clips (Titan departure / Earth arrival)

## GOAL (in Max's words)
Max wants help finding - and now generating - two b-roll clips:
1. "the shuttle leaving titan station" (a departure)
2. "arriving to earth orbit station" (an approach/arrival)

He asked me to "hold his hand" while searching, and to search independently too (via prompts and filenames). Now that candidates are found, his direction is: **"both failed miserably. But that's the right track. Let's start iterating."** He wants me to **make the first two clips**, both **silent (no sound/no audio)** - music will be added later.

## DECISIONS + WHY
- **Searched two ways simultaneously** - the database by prompt text, and the filesystem by filename - because clips may be discoverable by either, and Max explicitly wanted both approaches.
- **Treated the existing candidates as starting points only**, not finished assets, because Max confirmed they "failed miserably" but represent the right creative direction.
- **The two clips must be silent** - Max wants no audio baked in; music is a later step.

## CURRENT STATE
Search is complete. Candidates were located, confirmed on disk, and presented to Max. He approved the direction and asked to begin iterating by generating the first two clips (silent).

The found candidates (all old **junk**-rated rejects, never approved - use as references/starting points):

**Shuttle LEAVING station (departure) - 1 candidate:**
- ID **2639** (`sc09_b00_v04_wan.mp4`): small dark space shuttle moves slowly away from the station, turns away from camera, heads to top-right, shrinks to a dot, parabolic antigravity curve, no propulsion trace, clouds drift slowly.

**Shuttle ARRIVING to pearl/orbit station (approach) - 3 candidates:**
- ID **2677**: shuttle approaching station, slow gentle approach, calm space, no chemtrail/exhaust, faithful to ref shape and textures.
- ID **2678**: little dark space taxi on right approaching the fancy pearl-colored flying station on left, slow gentle approach.
- ID **2679**: same as 2678 but worded "space pod."

## EXACT NEXT STEP
Generate the **first two b-roll clips** - one Titan departure, one Earth-orbit arrival - both **silent (no audio track)**. Use the candidates above as the creative reference/starting prompts. Determine the generation/render workflow used in this repo (the combo_runner pipeline) and fire fresh clips rather than re-using the junk ones.

## OPEN QUESTIONS (awaiting Max)
- I had offered to also search the **stills/images** for exterior shuttle source plates so we could re-fire fresh b-roll - Max did not directly answer, but his "let's iterate / make the first two" implies proceed with generation. Confirm whether he wants source-plate stills pulled first, or to iterate directly on the existing prompts.
- None of the candidates is explicitly labelled "Titan" vs "Earth" - the station identity must be eyeballed. Confirm which visual = Titan station and which = Earth orbit (pearl) station.

## KEY PATHS / IDS / COMMANDS
- **cwd**: `C:\moma\.claude\worktrees\upbeat-swanson-bead73`
- **Code dir**: `/c/moma/sc10/combo_runner/code`
- **DB access**: Python `from moma_db import D1Client`; the correct query method is **`query_sql(...)`** (NOT `query` or `query_rows` - those don't exist).
- **Everything search tool (es.exe)**: `/c/claude_base/tools/es/es.exe`
- **Media library root**: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode`
- **Local review UIs**: clipper at `http://localhost:8779/clipper?ids=...` and `http://localhost:8779/lipser?ids=...` (note: arrival clips were lipsync-type, viewed via the `lipser` path)
- **Filename conventions**: `sc09_b00_vXX_wan.mp4` (b00 = a version tag, NOT a b-roll tag); lipsync clips like `sc09_lipsie_vNNNN_wan26flau.mp4`.
- Total library scanned: ~684 clips; the prompt search returned 56 hits across keywords titan/earth/orbit/station/approach/away.

## GOTCHAS / DEAD ENDS RULED OUT
- **Wrong DB methods**: `query` and `query_rows` both failed - only `query_sql` works on D1Client.
- **`b00` is a misleading tag** - it's a version number, not a "b-roll" marker. Don't filter on it expecting b-roll.
- **Most shuttle-group clips have faces/dialogue** (Driver/Anna talking) and are NOT usable as clean exterior b-roll. Only the pure exteriors are usable: departure **2639** and approaches **2677/2678/2679**.
- **The candidate filenames I first guessed didn't exist on disk** - files for 2677-2679 had to be found via looser filename search. All candidates are junk-rated and were never approved, so they're known-imperfect ("failed miserably") - reference material only.
