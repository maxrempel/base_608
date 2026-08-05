# Scribe handover - milestone 10 (~154K tokens)
# session: 20260609_upbeat_swanson_bead73_94d85cdd
# cwd: C:\moma\.claude\worktrees\upbeat-swanson-bead73
# written: 2026-06-09 13:51:08 by claude-opus-4-8

# HANDOVER - B-roll shuttle clips (Titan departure + Earth arrival)

## GOAL (in Max's words)
Max wants two B-roll clips: one of "the shuttle leaving Titan station" and another "arriving to earth orbit station." Both must be **silent clips, no sound** - "The music will be added later." This is the antigravity shuttle from the Kazarian episode, and Max is iterating because earlier attempts "both failed miserably" but were "the right track."

Critical correction from Max: it is **not an airplane or American/NASA shuttle** - it is "our fancy antigravity shuttle," and the clip "need[s] to stay faithful to shape." It must have **no chemtrail/plume**. Max is frustrated ("WAN is idiotic. I am desperate.").

## DECISIONS + WHY

- **Silent = the Wan2.6 clip lane**, not the lipsie/audio path. The wan26 worker claims jobs where `output_status='queued' AND engine='wan26'`. That lane produces no audio. Confirmed by reading the worker code.
- **Clips go into arrangement `sc9-arr01`** - confirmed this is the actual movie arrangement (read from app_state), so the clips land in the film, not an orphan.
- **The source stills are GOOD, Wan is the problem.** Initially the assistant wrongly assumed clip 2743's source still was a NASA shuttle. After actually opening the PNG, it was confirmed the source still is fine - a small dark pod, no plume. **Wan turned the good pod into a NASA shuttle and invented the chemtrail during animation.** Same story on 2744 (Wan invented a brown blob and got the facing wrong). So the real fight is with Wan hallucinating from a static frame, NOT the source stills.
- **The lever: starve Wan of room to invent.** Use a near-zero-motion prompt - hold the pod exactly, shape unchanged, only let clouds/planet drift slowly. The earlier "flies away / parabolic curve" wording is what gave Wan license to re-imagine the pod.
- **Also try Kling side-by-side** - Kling often holds shape better than Wan. Plan agreed: re-fire the same good source stills with a tight "hold shape, barely move" prompt on **both Wan and Kling**, compare which keeps the pod.
- **Canonical shuttle shape = plate 873** (`shuttle_v148a_bottom_bulge_a.png`), confirmed by Max as the correct antigravity shuttle. This is the shape reference if any image regeneration is needed.
- Max's earlier idea (make a closeup portrait still first, then animate toward station, then reverse the sequence) is on the table but currently superseded by the simpler "re-fire good stills with tight prompt + Kling comparison" approach.

## CURRENT STATE
- v01 clips **2743** (leave Titan) and **2744** (arrive Earth orbit) were fired and rendered cleanly but **both were rejected** by Max - Wan hallucinated a NASA shuttle + chemtrail (2743) and a blob + wrong facing (2744).
- The assistant just proposed re-firing both good source stills with a tight "hold shape, barely move" prompt, on Wan and Kling side by side.
- Max's last words: **"ok refire"** - approval to fire. NOTHING has been fired yet in response. This is the action to take.

## EXACT NEXT STEP
Re-fire the two B-roll clips using the **same good source stills** as before, with a **tight near-zero-motion prompt** (hold pod shape exactly, no flying-away wording, only clouds/planet drift slowly, clean seamless hull, no plume). Fire each on **both Wan2.6 and Kling** so they can be compared. Target arrangement **sc9-arr01**. Then watch in background and present click-to-watch links when ready.

- Leave-Titan source still: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\ships\space\titan_leave_v08_mirrored_b_redo_01_redo_01_redo_01_redo_02_redo_01_redo_01.png`
- Arrive-Earth source still: `sc09_approach_v11_a.png` (in the same kazarian_episode tree; confirmed on disk earlier)

## OPEN QUESTIONS
- Which engine wins (Wan vs Kling) - to be decided after viewing the side-by-side.
- Max earlier was asked whether the two faces (Anna + Driver) must be visible through the canopy vs just suggested; Max answered "either way" ? weight refs toward shuttle shape first, faces only suggested. (Relevant only if returning to the portrait-still plan.)

## KEY PATHS / IDS / COMMANDS
- Working dir: `C:\moma\.claude\worktrees\upbeat-swanson-bead73`; code in `/c/moma/sc10/combo_runner/code`
- DB access: `from moma_db import D1Client; d1.query_sql(...)` - the correct method is **`query_sql`** (NOT query / query_rows). Also `connect_db()` and `fire_job(...)` from moma_db.
- Wan2.6 worker: `combo_wan26_worker.py` - claims `output_status='queued' AND engine='wan26'`, resolves `source_image` by **absolute path**, runs one job at a time (~1-3 min each). Worker confirmed alive; pid file `../data/wan26_worker_pid.txt`.
- Image worker: `combo_worker.py`; concept-strip recipe via `concept_arrangement.py`.
- Arrangement: **sc9-arr01** (the movie).
- Canonical shuttle shape: **plate 873** = `shuttle_v148a_bottom_bulge_a.png` (shape:shuttle_ext). Anna = plate 4, Driver = plate 1040.
- Viewer base URL: `http://localhost:8779/` - `/clipper?ids=...`, `/imager?ids=...`, `/lipser?ids=...` with `&title=`.
- Search tool: Everything CLI `"/c/claude_base/tools/es/es.exe"` (search by filename), e.g. `es.exe titan_leave_v08`.
- Logging: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` and `session_status.py report "..."`.
- Rejected v01 clips: **2743** (leave Titan), **2744** (arrive Earth). Source-still IDs and the failed lipsie attempts: 2639 (departure exterior), 2677/2678/2679 (approach exterior) - all old "junk"-rated rejects.

## GOTCHAS / DEAD ENDS RULED OUT
- **Do NOT assume the source still is bad without opening it** - the assistant made this mistake once. The stills are confirmed good; Wan is the one inventing.
- **Avoid motion verbs** like "flies away," "makes a turn," "parabolic curve" in the prompt - that wording is what let Wan re-imagine/hallucinate the shuttle into a NASA craft with a plume.
- The `b00` tag is a **version tag, not a b-roll tag** - noise, don't filter on it.
- Most shuttle-group clips contain Driver/Anna talking; only the pure-exterior ones (2639, 2677-79) are silent b-roll candidates.
- Lipsie/audio path is the WRONG lane - these must be silent, so use the wan26 (and Kling) clip lane.
- Wan does one render at a time; expect queueing.
