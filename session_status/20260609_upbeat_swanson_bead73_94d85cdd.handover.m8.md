# Scribe handover - milestone 8 (~130K tokens)
# session: 20260609_upbeat_swanson_bead73_94d85cdd
# cwd: C:\moma\.claude\worktrees\upbeat-swanson-bead73
# written: 2026-06-09 12:35:15 by claude-opus-4-8

# HANDOVER

## GOAL (in Max's words)
Max wanted help searching for two b-roll clips: "one - the shuttle leaving titan station and another - arriving to earth orbit station." He recalled both earlier attempts "failed miserably" but were "the right track." His instruction: "Let's start iterating. make the first two, both should be silent clips, no sound, The music will be added later." Final ask before this handover: "when ready present them here" - i.e., present the two rendered clips to him as soon as they finish.

## DECISIONS + WHY
- **Silent clips ? Wan2.6 i2v lane, NOT the lipsie/audio path.** Max explicitly wants no sound (music added later), so the work goes through the clip lane. The Wan2.6 worker claims jobs where `output_status='queued' AND engine='wan26'`, which is exactly the silent-clip lane.
- **Reuse the same source stills the failed attempts used** - because Max said those attempts were "the right track." The starting frames are kept; only the motion prompts were rewritten to clean, positive, minimal motion-only lines per the project's prompt rules.
- **Fire into arrangement sc9-arr01** - confirmed via app_state that this is the live movie arrangement, so the clips land in the actual film and not an orphan.
- **Pass full absolute Windows paths for source images** - the worker resolves `source_image` by absolute path, so this avoids "image missing" failures.

## CURRENT STATE
Two silent Wan2.6 clips were fired and are rendering:
- **Job 2743** = shuttle **leaving Titan** - was *running* at last check. Source still: `titan_leave_v08` png. Prompt: shuttle slowly flies away from the station, rising toward upper right, shrinking into distance; clouds drift slowly.
- **Job 2744** = shuttle **arriving Earth orbit** - was *queued next* (Wan2.6 does one at a time, ~1-3 min each). Source still: `sc09_approach_v11_a.png`. Prompt: small shuttle drifts slowly toward the station, gentle approach, barely moving.

The Wan2.6 worker process is confirmed alive and already grabbed 2743. A background watch loop was started to detect when both finish. A worklog milestone was logged.

## EXACT NEXT STEP
Confirm both 2743 and 2744 have finished rendering (output_status done/complete), then **present both to Max here** with a click-to-watch clipper link. Build the link the same way as before: `http://localhost:8779/clipper?ids=2743,2744&title=...`. Then judge the motion together and iterate.

## OPEN QUESTIONS
- None blocking. After presenting, await Max's verdict on the motion to decide next iteration (re-fire with adjusted prompt, swap source still, etc.).
- Earlier offered but not taken up: searching the stills/images for fresh exterior shuttle source plates if the existing stills prove inadequate. Hold unless Max revives it.

## KEY PATHS / IDS / COMMANDS
- Working dir for DB/worker code: `C:\moma\sc10\combo_runner\code` (`/c/moma/sc10/combo_runner/code`)
- DB access: `from moma_db import D1Client; d1.query_sql(...)` for D1 reads; `from moma_db import connect_db, fire_job` for local DB + firing.
- The correct query method is **`query_sql`** (NOT `query`, NOT `query_rows` - those don't exist / are wrong).
- Worker file: `combo_wan26_worker.py` - claims `output_status='queued' AND engine='wan26'`.
- Worker PID file: `../data/wan26_worker_pid.txt`
- Arrangement (the movie): **sc9-arr01** (read from app_state).
- Source stills (both confirmed on disk): departure = `titan_leave_v08...png`; arrival = `sc09_approach_v11_a.png`. Base media folder: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode`.
- Filesystem search tool: Everything CLI at `/c/claude_base/tools/es/es.exe`.
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Job IDs in play: **2743** (leave Titan), **2744** (arrive Earth). The original failed/junk attempts were 2639 (`sc09_b00_v04_wan.mp4`, departure) and 2677/2678/2679 (`sc09_lipsie_v26XX_wan26flau.mp4`, arrival).
- Preview server: `http://localhost:8779` - `/clipper` for silent clips, `/lipser` for audio/lipsie clips.

## GOTCHAS / DEAD ENDS RULED OUT
- The `b00` token is a **version tag, not a b-roll marker** - searching on it returns noise.
- Most clips in the shuttle group contain Driver/Anna faces/dialogue; only the four exterior ones above are pure b-roll.
- The original 2639 / 2677-2679 are old **junk-rated rejects** - usable only as starting references, not finals.
- None of the source material is explicitly labelled "Titan" vs "Earth"; the station identity must be eyeballed.
- Don't route silent clips through the lipsie/audio path - that adds sound, which Max does not want.
