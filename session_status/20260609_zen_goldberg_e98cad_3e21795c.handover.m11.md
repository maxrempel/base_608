# Scribe handover - milestone 11 (~166K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# cwd: C:\moma\.claude\worktrees\zen-goldberg-e98cad
# written: 2026-06-09 15:01:59 by claude-opus-4-8

# HANDOVER - Pod-on-Black B-Roll Branch (zen-goldberg-e98cad)

## GOAL (in Max's words)
Max needs two SILENT b-roll clips for his sci-fi movie (MOMA, scene sc09):
1. the antigravity shuttle **LEAVING the Titan station**
2. the shuttle **ARRIVING at the Earth orbit station**

Music is added later, so every clip must be silent (no audio). Hard constraint: the shuttle must stay faithful to **OUR antigravity pod shape** (NOT a generic NASA/American shuttle) and must have **NO chemtrail/exhaust plume** (it runs on antigravity).

This is a git worktree branch. **Another session owns a different approach** (the closeup-still / plate-873 path). THIS session explores other options - specifically the "pod on black/transparent ? animate motion ? key out ? overlay on real plate" idea, which Max explicitly asked for and branched.

## DECISIONS + WHY
- **Why pod-on-black, not direct i2v:** Single-frame image-to-video (Wan AND Kling) kept reinventing the small/ambiguous pod into a NASA shuttle with a chemtrail. Max spent ~10 hours; called Wan's output "laughable," Kling "an expensive disaster." Fix: feed Wan a pod on pure black - it has nothing to reinvent, so it just MOVES the pod. Decouples motion (Wan) from background (we own it). Max confirmed this works: clip 2745 pod shape "looks good."
- **Why NOT flat compositing:** Max wants non-linear/curved motion that flat 2.5D parallax can't give. That's the whole point of letting Wan do the move on black.
- **Why proper matte, not lumakey:** The first overlay (clip 2752) used ffmpeg lumakey = brightness-based keying. It punched out the pod's own dark/glassy areas ? semi-transparent ghost pod. Max rejected it: "the thing is transparent... you don't use good tech to remove bg. You need proper proper, ideal tracer... Black is not enough." Fix = per-frame rembg/u2net segmentation matte = solid object alpha regardless of internal darkness.
- **Why the full-res PNG, not the thumb:** Max gave a thumb path in `sound_assembly\data\thumbs_cache\`. That entire folder is the mixboard UI's small cached preview jpgs - never the real asset. DB trace (output_file column) showed the real full-res plate is `titan_leave_v04_bg_right_station_a.png`.

## CURRENT STATE
- **Clip 2745** (pod-on-black, Wan26, silent) - DONE, pod shape held, Max approved.
- **Clip 2752** (lumakey composite on Titan) - DONE but REJECTED (transparent ghost pod, bad matte tech). Dead end.
- **pod_matte_overlay.py** - CREATED, the live tool. Replaces lumakey with per-frame rembg solid matte.
- **Solid-matte composite render - RUNNING IN BACKGROUND** right now (subject = clip 2745's mp4, bg = full-res `titan_leave_v04_bg_right_station_a.png`). This is the in-flight work.
- Just answered Max's question: yes, the real high-res original was traced via the database - it's the full-res PNG, not the thumb.

## EXACT NEXT STEP
1. Wait for the background pod_matte_overlay.py render to finish.
2. Quick-check ONE small frame for matte quality (solid pod, no fringe, no ghost) - do NOT inhale full videos/large PNGs (near compaction).
3. Register the result as a done clip row via `fire_job` (job_type='clip', output_status='done', output_file=..., into arrangement sc9-arr01).
4. Present via picks-link: `http://localhost:8779/clipper?ids=N&title=...` (urlencoded).
5. Then address the SEPARATE "choppy" flight problem (Wan motion jitter / low effective fps) - via frame interpolation or a re-fired slower-motion black clip.
6. Factory completion: reverse the same clip to get the ARRIVAL direction for free; produce both Titan-departure and Earth-arrival b-rolls.

## OPEN QUESTIONS AWAITING MAX
- Does the solid-matte composite finally look right (opaque pod, clean edges, sitting properly over the station plate)?
- What exact motion does he want (recede toward station / bank away / slow rise)? - needed to re-fire the black clip if motion needs tuning.
- "Choppy" is acknowledged but not yet fixed - pending his look at the new composite.

## KEY PATHS / IDS
Base: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\`
- Canonical pod (plate 873): `interiors\shuttle\shuttle_v148a_bottom_bulge_a.png` - big bean-pod, Anna+Driver in canopy.
- Clean pod-FREE bg plate (job 1210, the composite target): `ships\space\titan_leave_v04_bg_right_station_a.png` (station on right).
- Thumb Max pointed at (NOT the asset): `scenes\scene10_images\sound_assembly\data\thumbs_cache\job_1210.jpg`.
- Failed-attempt sources: `ships\space\titan_leave_v08_mirrored_b_redo_...png` (departure, pod tiny blob); `ships\space\sc09_approach_v11_a.png` (arrival).
- Working files: `ships\space\broll_work\` - `pod_cutout_873_v01.png`, `pod_on_black_v01.png`, `composite_check_v01.jpg`.
- Output clips: `scenes\scene10_images\combo_runner\data\output_clips\` - `sc09_sc09_broll_podblack_20260609_v01_wan26.mp4` (2745, GOOD), `sc09_broll_podcomposite_v01.mp4` (2752, REJECTED).
- Tool: `C:\claude_base\tools\broll_overlay\pod_matte_overlay.py` - usage: `python pod_matte_overlay.py <subject_video> <bg_image> <out_mp4> [W] [H] [fps]`. Extracts frames, per-frame rembg u2net for solid alpha, alpha_composite over bg, re-encode silent h264.
- Code: `C:\moma\sc10\combo_runner\code\` - `moma_db.py`, `combo_wan26_worker.py`, `canonical_status.py`.
- Pod clip specs: 1280?720, 30fps, 150 frames (5s).
- Canonical assets: shuttle shape = plate 873 (`shape:shuttle_ext`); Anna face = plate 4; Driver = plate 1040.

## GOTCHAS / DEAD ENDS RULED OUT
- **DB method:** use `D1Client.query_sql(sql, params)` - NOT `query` or `query_rows` (those don't exist on D1Client; query_rows is MomaDB). Adviser said: note this and stop re-probing.
- **fire_job is the ONLY legal job insert** (`moma_db.py` ~line 473). Unknown kwargs raise. job_type='clip' with empty engine defaults to engine='wan26'. Auto-inherits arrangement_id from `app_state.current_arrangement_id` (= sc9-arr01); raises if no arrangement set (anti-orphan guard).
- **Silent clips = job_type='clip', engine='wan26'** (combo_wan26_worker claims `output_status='queued' AND engine='wan26'`). Worker resolves source_image by absolute path via os.path.exists - always pass full Windows paths. NOTE: wan26flau (wan2.6-i2v-flash) is the LIPSIE/audio path - NEVER use it for silent b-roll.
- **Lumakey is dead** - never key the pod by brightness again. Per-frame segmentation only.
- **Don't run parallel Bash searches that share a batch** - a sibling error cancel-cascaded a good es.exe call earlier. Run searches separately.
- **Thumbs_cache folder is ALL tiny previews** - never composite against anything in there; trace the DB output_file for real full-res.
- **Flip-flop warning:** I once wrongly blamed the source still as a generic NASA shuttle; Max corrected "the input was good." Do NOT reopen that - the input pod shape is correct; the failure was engines redrawing it. Adviser flagged me for reversing position mid-sentence - state things once, firmly.
- **STOP re-offering menus / reframing strategy every turn.** Branch is LOCKED: finish pod-on-black end-to-end (real solid-matte composite, not raw clips). Adviser flagged this repeatedly.
- **Context near compaction (~90%+, ~169K cliff).** Do NOT read large PNGs/videos into context. Keep replies short, plain-English, TLDR-first, no code shown, no Unicode, ~200 chars.
- **Presenting:** picks-links only - `http://localhost:8779/clipper?ids=N,N&title=<urlencoded>` for clips, `/lipser` for lipsies. A registered done clip row makes the composite viewable in /clipper.
