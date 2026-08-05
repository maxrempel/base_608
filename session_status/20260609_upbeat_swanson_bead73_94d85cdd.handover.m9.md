# Scribe handover - milestone 9 (~136K tokens)
# session: 20260609_upbeat_swanson_bead73_94d85cdd
# cwd: C:\moma\.claude\worktrees\upbeat-swanson-bead73
# written: 2026-06-09 12:41:34 by claude-opus-4-8

# HANDOVER - Shuttle B-Roll Iteration (silent clips for sc9-arr01)

## GOAL (in Max's words)
Max wants two B-roll clips: "one - the shuttle leaving titan station and another - arriving to earth orbit station." Both must be **silent clips, no sound** ("The music will be added later"). This is an iteration loop - earlier attempts at these two shots "both failed miserably," but Max says it's "the right track."

His refined plan (his own idea): "start from making an image with the shuttle closeup, so the portrait of the shuttle is big. with two people facing us. Then Ask it to go towards the station. Then reverse the sequence." (One render ? reverse it ? get both departure and arrival.)

Critically, his latest message corrects the direction: the shuttle and people should NOT be facing the camera. **"It should be facing the thing [the station]."** He is frustrated and "desperate" - keep tight, no over-explaining.

## DECISIONS + WHY
- **Use the Wan2.6 clip lane, not lipsie/audio lane** - because clips must be silent (music added later). The wan26 worker is the silent i2v path.
- **Reuse the same source stills the failed attempts used** - Max called those "the right track."
- **Target arrangement sc9-arr01** - confirmed this is the live movie arrangement (via app_state), so clips land in the film, not orphaned.
- **Shuttle identity is the core problem**: it is NOT a NASA/American shuttle and must have NO chemtrail/exhaust plume. It is "our fancy antigravity shuttle" - must stay faithful to a specific shape. The failed clips inherited a generic NASA-looking shuttle WITH a chemtrail because the *source still itself* was a generic shuttle, so Wan just preserved it.
- **Canonical shuttle shape identified**: `shape:shuttle_ext`, plate **873** = `shuttle_v148a_bottom_bulge_a.png`. This is the correct antigravity-shuttle shape the bad clips ignored.

## CURRENT STATE
- v01 clips were fired and rendered cleanly (no errors) but were **rejected by Max** for two reasons:
  1. It's the wrong shuttle (NASA-looking) + chemtrail present.
  2. (Latest, "Second idiocy") The new still brought the station into view unintentionally, AND the shuttle + people are facing the camera - they should be facing the station.
- Fired clips: **2743** (leave Titan, src `titan_leave_v08`) and **2744** (arrive Earth orbit, src `sc09_approach_v11_a`) - both now superseded/rejected.
- The new plan (close-up still ? animate toward station ? reverse) was being set up. The shuttle shape ref was just pinned. No new still has been successfully fired yet that satisfies the direction/framing constraints.

## EXACT NEXT STEP
Build the **close-up portrait still** of the antigravity shuttle correctly, honoring ALL of Max's constraints:
- Use canonical shape ref **plate 873** (`shuttle_v148a_bottom_bulge_a.png`) so it's OUR shuttle, not NASA.
- **No chemtrail / no exhaust plume.**
- Shuttle big in frame (portrait/close-up).
- **Do NOT bring the station into the frame** (that was the unintended "idiocy").
- Shuttle and the two people must be **facing AWAY toward where the station will be** - NOT facing the camera. (This contradicts the earlier "two people facing us" wording - Max has now reversed that. Latest instruction wins: facing the station/away.)
- Then animate: shuttle moves toward the station (recedes). Then reverse the rendered clip to produce the arrival.

## OPEN QUESTIONS (awaiting Max)
- The faces question was asked but NOT answered before Max's correction: do the two faces (Anna + Driver) need to be recognizable through the canopy, or just the shuttle shape correct with people merely suggested? Given the new "facing away" instruction, faces are now likely back-of-head / not visible - confirm whether faces matter at all now.
- Confirm whether the still should have empty space/sky where the shuttle is heading (so it can "go towards" something off-frame) rather than the station being visible.

## KEY PATHS / IDS / COMMANDS
- cwd: `C:\moma\.claude\worktrees\upbeat-swanson-bead73`
- Code dir: `/c/moma/sc10/combo_runner/code`
- DB module: `moma_db.py` - class **D1Client**, method is `query_sql` (NOT query / query_rows). Also `connect_db()` and `fire_job()`.
- Worker: `combo_wan26_worker.py` - claims jobs where `output_status='queued' AND engine='wan26'`; resolves `source_image` by **absolute Windows path**; runs one clip at a time (~1-3 min each).
- Worker PID file: `../data/wan26_worker_pid.txt`
- Stills base path: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\...`
- Canonical shuttle shape: `shape:shuttle_ext`, plate **873** = `shuttle_v148a_bottom_bulge_a.png`
- Anna face = plate **4**; Driver face = plate **1040**
- Arrangement (live movie): **sc9-arr01** (from app_state)
- Source stills used by failed v01: `titan_leave_v08...png` (departure), `sc09_approach_v11_a.png` (arrival)
- Everything search tool: `/c/claude_base/tools/es/es.exe`
- canonical status: `python canonical_status.py`
- Preview links open at `http://localhost:8779/clipper?ids=...` (clip lane) - pattern: `?ids=2743,2744&title=...`
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Status report: `python C:/claude_base/compaction_kb/scripts/session_status.py report "..."`

## GOTCHAS / DEAD ENDS
- **Do not use lipsie/audio lane** - clips must be silent.
- The DB has 56 "shuttle"-ish hits across 684 clips; most have Driver/Anna talking (dialogue/faces) and are NOT exterior b-roll. The `b00` tag is a VERSION tag, not "b-roll" - it's noise.
- The old candidate clips (2639, 2677, 2678, 2679) are all junk-rated rejects; none labeled Titan vs Earth explicitly.
- **The root cause of failure is the source still, not the motion prompt.** Cleaning the motion prompt alone (as done in v01) did NOT fix the NASA-shuttle/chemtrail problem because Wan faithfully preserved the bad source image. Fix the still first.
- Wan ignores shape unless the shape ref is strongly weighted - combining exact shuttle shape + exact faces in one shot is the riskiest ask. Weight refs deliberately.
- Direction instruction has flipped: earlier "two people facing us" is now overridden - shuttle/people face the station (away from camera).
- Compaction risk: ~136K tokens, wipe near ~169K. Save state soon.
