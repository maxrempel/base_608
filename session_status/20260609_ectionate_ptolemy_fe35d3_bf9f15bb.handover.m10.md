# Scribe handover - milestone 10 (~156K tokens)
# session: 20260609_ectionate_ptolemy_fe35d3_bf9f15bb
# cwd: C:\moma\.claude\worktrees\affectionate-ptolemy-fe35d3
# written: 2026-06-09 13:24:18 by claude-opus-4-8

# HANDOVER - B-roll Shuttle Clips via Keyframe Interpolation

## GOAL (in Max's words)
Make two silent b-roll clips: "one - the shuttle leaving titan station and another - arriving to earth orbit station." No sound - "The music will be added later." The shuttle must stay faithful to its real shape - "it is not an airplane or american shuttle, it is our fancy antigravity shuttle - need to stay faithful to shape" - and must have **no chemtrail / no exhaust plume**.

Max has spent ~10 hours fighting this. He is now **exploring options other than Wan**, which "is pretty retarded in physical movements" and whose output is "laughable." This session is the explore-alternatives track; **another session owns the closeup-still path** (the idea of generating a big shuttle-portrait still first). Keep them separate.

## DECISIONS + WHY
- **Abandon Wan2.6 i2v for this shot.** Single-frame image-to-video keeps redrawing the pod into a generic NASA shuttle with a flame. Wrong tool for "a faithful object moves across frame."
- **Rejected Kling** - Max tried it: "it changed the images by glamourizing them and there was no way to prevent that." (Note: the assistant initially blamed the input still as a tiny ambiguous blob, but Max corrected: **"the input was good."** The real failing is engines redrawing the pod during motion, not the source.)
- **Chosen approach: First+last-frame (keyframe) interpolation.** Feed two of our own renders as start and end; the AI only fills the in-between, so it can't reinvent the shape the way single-frame i2v does.
- **Chosen tool: Vidu** - built specifically to interpolate between two given frames, so it can't "glamorize" the way Kling did. Max explicitly said "Let's try vidu."

## CURRENT STATE
- Max just **logged into Vidu via Google as `max.rempel2@ggmail`** (note the typo - likely gmail) in his Chrome browser. The Vidu login page (https://www.vidu.com/login) was open via the Chrome MCP tools.
- His last instruction: **"do next steps."**
- Nothing has been fired on Vidu yet. No clip generated on the new path.
- Two old Wan clips (2743 leave-Titan, 2744 arrive-Earth) rendered but were rejected - they showed a NASA shuttle with a chemtrail.

## EXACT NEXT STEP
Proceed with a Vidu keyframe test, BUT the real blocker is unresolved: **we need a proper near?far pod image pair as the two endpoints.** The assistant checked `sc09_approach_v11_a.png` and `_b.png` and found they are nearly the same shot - a **weak motion pair**, not usable as distinct start/end frames.

So next: either (a) drive the Vidu web UI now that Max is logged in to run a start+end interpolation manually, or (b) wire **Vidu Q1 start-end** through the existing **fal.ai key** for a scripted run (no Vidu account needed for API). Before either, secure a genuine near?far endpoint pair - confirm whether the other session is producing it or make it here.

## OPEN QUESTIONS (awaiting Max)
- Web UI manual test vs. fal.ai API scripted run for Vidu?
- Who supplies the near?far pod endpoint pair - this session or the other one?
- (Earlier, never answered: in any exterior portrait, must the two faces be recognizable through the canopy, or just the shuttle shape correct? May resurface.)

## KEY PATHS / IDS / PRICING
- Working dir: `C:\moma\.claude\worktrees\affectionate-ptolemy-fe35d3`
- DB code: `/c/moma/sc10/combo_runner/code/moma_db.py` - class **D1Client**, method **`query_sql`** (NOT query / query_rows). Also `connect_db`, `fire_job`.
- Arrangement (the movie / correct home for clips): **sc9-arr01**
- Wan worker: `combo_wan26_worker.py` - claims `output_status='queued' AND engine='wan26'`, resolves `source_image` by absolute Windows path, one job at a time.
- Canonical antigravity shuttle shape: **shape:shuttle_ext, plate 873** = `...\interiors\shuttle\shuttle_v148a_bottom_bulge_a.png` (big crisp pod, Anna + Driver facing camera through canopy). Faces: Anna = plate 4, Driver = plate 1040.
- Candidate stills: `...\ships\space\sc09_approach_v11_a.png` and `_b.png` (too similar - weak pair); `...\ships\space\titan_leave_v08_..._redo...png` (the small-pod departure still).
- Old rejected Wan clips: **2743** (leave Titan), **2744** (arrive Earth orbit).
- Everything is on **fal.ai** - existing fal.ai key works for Vidu API (no new signup needed for scripted path).
- Vidu pricing (5s @1080p): **Vidu Q1 start-end ? $0.20** (purpose-built for start?end), Kling 2.5 Turbo Pro $0.35, Pika Pikaframes $0.30, Luma Ray2 $2.00. A test clip is 20-35 cents, not a money pit.
- Default kickoff signup email (if needed): `mass@tamza.com` (confirmation mail readable via MXroute). Max used his own Google instead.
- Search tool: `/c/claude_base/tools/es/es.exe` (Everything) for filename search on disk.
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`

## GOTCHAS / DEAD ENDS RULED OUT
- **Wan2.6 i2v** - dead end for faithful object motion; redraws the pod, adds chemtrail. 10 hours wasted.
- **Kling** - dead end; glamorizes/alters the source images, unpreventable.
- **Veo 3.1** - researcher flagged it as weak at holding an exact ship, no reliable negative prompt. Skip.
- Do **not** re-argue that the source still was bad - Max settled it: input was good, engines are the problem.
- The `sc09_approach_v11_a`/`_b` pair are near-identical - not a real motion pair.
- `b00` in filenames is a version tag, not "b-roll" - noise in searches.
- Near compaction (~169K, currently ~156K). Log milestones before context loss.
- The closeup-portrait-still idea belongs to the OTHER session - don't duplicate it here.
