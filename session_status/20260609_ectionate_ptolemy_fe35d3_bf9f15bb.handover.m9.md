# Scribe handover - milestone 9 (~136K tokens)
# session: 20260609_ectionate_ptolemy_fe35d3_bf9f15bb
# cwd: C:\moma\.claude\worktrees\affectionate-ptolemy-fe35d3
# written: 2026-06-09 12:43:24 by claude-opus-4-8

# HANDOVER

## GOAL (in Max's words)
Max is making two silent B-roll clips for the movie: "one - the shuttle leaving Titan station, and another - arriving to earth orbit station." Music gets added later, so the clips must be silent (no audio). Both earlier attempts at these two shots "failed miserably," but Max considers the approach "the right track" and wants to iterate.

His latest pivot (the live question): he made a branch and wants research - **"any way to feed our portraits/template images and have a way smarter video maker that actually understands English? Wan is pretty retarded in physical movements. Maybe it is faster to make brolls in something entirely different."** So the immediate task is no longer firing more Wan jobs - it's **searching online for an alternative image-to-video tool** that (a) accepts our reference/portrait images, (b) understands plain-English motion direction better than Wan2.6, and (c) might be faster/better for B-roll.

## DECISIONS + WHY
- **Silent clips = Wan2.6 i2v lane, not the lipsie/audio path.** The worker claims jobs where `output_status='queued' AND engine='wan26'`. That lane produces no audio - correct for "music added later."
- **Reused the same source stills the failed attempts used** because Max said those were "the right track." Leave-Titan used still `titan_leave_v08...png`; arrive-Earth used `sc09_approach_v11_a.png`.
- **Rewrote prompts to clean, minimal, positive motion-only lines** per the project's prompt rules (no negatives crammed in).
- **Diagnosis after v01 failed again:** the rendered shuttle looked like a NASA/American shuttle **with a chemtrail**, NOT our fancy antigravity pod. Root cause identified: **the source still itself was a generic shuttle**, so Wan faithfully kept the wrong shape. This is the core problem.
- **Max's proposed fix (agreed, not yet executed):** Make a NEW still first - a close-up portrait of the shuttle, big in frame, two people facing us through the canopy. Then animate that still so the shuttle moves toward the station (recedes). Then **reverse the clip** to get the arrival shot - one render yields both directions.
- **Then Max pivoted again** to questioning Wan entirely - hence the online-research request. Wan's weakness is physical movement/English comprehension.

## CURRENT STATE
- v01 of both clips rendered cleanly (no errors) but are **rejected by Max** - wrong shuttle shape + chemtrail.
- Jobs **2743** (leave Titan) and **2744** (arrive Earth orbit) are the rendered v01s, in arrangement **sc9-arr01** (the movie). Both silent Wan2.6.
- The "still-first ? animate ? reverse" plan was articulated and locked in principle, but **nothing was fired for it.** Before firing, the assistant asked an open question (see below) which Max did NOT answer - instead he pivoted to the research request.
- A worklog milestone and a session_status snapshot were saved for the v01 firing.

## EXACT NEXT STEP
**Search online** for an image-to-video / video-generation tool that:
1. Accepts our own reference images (shuttle shape plate, character portraits) as input,
2. Follows plain-English motion instructions reliably (Wan2.6 fails at physical movement),
3. Could be faster/better than Wan for B-roll.
Report findings to Max - candidate tools, whether they take image refs, English-prompt fidelity, cost/speed. Do NOT fire more Wan jobs yet; Max is evaluating whether to switch tools entirely. This is on a fresh branch.

## OPEN QUESTIONS (awaiting Max)
- **Unanswered from before the pivot:** In the exterior shuttle close-up, does Max want the **two faces actually visible/recognizable through the canopy** (Anna + Driver), or just the shuttle shape correct with people merely suggested? (Combining exact shuttle shape + exact faces in one shot is the riskiest ask - answer weights the refs.) Max may answer this once the tool question is settled.
- Which alternative tool (if any) to adopt.

## KEY PATHS / IDS
- **cwd:** `C:\moma\.claude\worktrees\affectionate-ptolemy-fe35d3`
- **Code dir:** `C:\moma\sc10\combo_runner\code` (also `/c/moma/sc10/combo_runner/code`)
- **DB module:** `moma_db.py` - class **D1Client**, query method is **`query_sql`** (NOT `query` or `query_rows` - those don't exist). Also has `connect_db()` and `fire_job()`.
- **Worker:** `combo_wan26_worker.py` - claims `output_status='queued' AND engine='wan26'`; resolves `source_image` by **absolute path**; processes one job at a time (~1-3 min each).
- **Worker PID file:** `../data/wan26_worker_pid.txt`
- **Arrangement (movie home):** `sc9-arr01` (read from `app_state` table).
- **Rendered v01 jobs:** 2743 (leave Titan), 2744 (arrive Earth orbit).
- **Source stills:** `titan_leave_v08...png` (departure), `sc09_approach_v11_a.png` (arrival) - both confirmed on disk. These are the GENERIC-shuttle stills that caused the wrong shape.
- **Canonical real shuttle shape:** `shape:shuttle_ext`, plate **873** = `shuttle_v148a_bottom_bulge_a.png` (the correct antigravity-pod shape Wan ignored).
- **Faces:** Anna = plate **4**; Driver = plate **1040**.
- **Image root:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode`
- **Clip viewer:** `http://localhost:8779/clipper?ids=...` (silent/clip lane); `http://localhost:8779/lipser?ids=...` (audio/lipsie lane).
- **Everything search:** `/c/claude_base/tools/es/es.exe`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- **Status snapshot:** `python C:/claude_base/compaction_kb/scripts/session_status.py report "..."`

## GOTCHAS / DEAD ENDS RULED OUT
- **Wan2.6 keeps whatever shape is in the source still** - it does not invent our antigravity shuttle. Feeding a generic shuttle still = generic shuttle output. Any fix must start from a still that already shows the CORRECT shuttle shape (plate 873).
- **Wan2.6 also added a chemtrail/plume** despite intent for none - and is generally weak at physical movement/English. This is what triggered the tool-switch research.
- Earlier searches confirmed: across 684 clips, only the one departure (2639, `sc09_b00_v04_wan.mp4`) and three approach clips (2677/2678/2679) are pure exterior shuttle B-roll with no faces/dialogue - everything else in that group has Driver/Anna talking. All were **junk-rated rejects**.
- DB method-name confusion already cost time: the correct method is `query_sql`. Don't repeat `query`/`query_rows`.
- The `b00` token is a **version tag, not a b-roll marker** - searching on it returns noise.
