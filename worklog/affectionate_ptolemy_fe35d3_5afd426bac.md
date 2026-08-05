
## [2026-06-09 12:43] ? bf9f15bb
- DID: v01 b-roll clips 2743/2744 rendered but Wan2.6 drifted shuttle into a generic NASA shuttle WITH chemtrail - ignored our antigravity pod shape. Canonical shuttle shape = plate 873 shape:shuttle_ext (shuttle_v148a_bottom_bulge_a.png). Anna face=4, Driver=1040. Max plan: still closeup of shuttle+2 people facing thru canopy -> animate toward station -> reverse clip for opposite direction.
- STATE: PIVOT: Max said stop, branch made. Research smarter ref-conditioned i2v video maker (better than Wan2.6 physics/English/no-chemtrail). NOTE combo_kling_worker.py already wired = Kling via fal.ai available now.
- NEXT: Search 2026 video gens (Kling2.5/Veo3/Runway Gen-4 refs/Vidu/Hailuo), recommend, maybe just route b-roll to existing Kling worker
- LESSON: Wan2.6 i2v does not hold first-frame shape and adds exhaust plumes; bad for faithful object b-roll

## [2026-06-09 13:24] ? bf9f15bb
- DID: EXPLORING Vidu for faithful b-roll. Wan2.6 AND Kling both FAILED: they reinvent/glamorize the pod and add chemtrails (single-frame i2v has weak shape lock). Max spent ~10h. DECISION: use Vidu Q1 START-END frame interpolation (feeds 2 of our own renders as endpoints, AI only fills between, cant redraw). Max logged into vidu.com via Google max.rempel2@gmail. Vidu also on our fal.ai key (FAL_KEY_FILE, see combo_kling_worker.py for fal call pattern) = API alt, no new acct. Pricing: Vidu Q1 start-end ~$0.20/5s, Kling2.5 $0.35 - all on fal.ai.
- STATE: Vidu logged in (browser tab 1294135580). NEED near->far pod PAIR as endpoints - dont have a good one. Canonical pod=plate873 shuttle_v148a_bottom_bulge_a.png (big bean pod, Anna+Driver facing thru canopy). approach_v11_a/b are near-identical=weak pair. Other session owns the closeup-still idea; THIS session explores engines.
- NEXT: Drive Vidu UI to start-end-frame create page; make/find a real near->far pod pair; run 1 test; judge shape fidelity. fal.ai Vidu wiring is the scripted fallback.
- LESSON: Single-frame i2v (Wan/Kling) cannot hold a faithful object during motion - it redraws/glamorizes. Use START-END frame interpolation or compositing instead.

## [2026-06-09 14:10] ? bf9f15bb
- DID: Vidu Q1 start-end interpolation cracked the faithful-pod b-roll problem (Wan/Kling both failed). Built faithful END frame by compositing real pod pixels bigger/moved; fired fal-ai/vidu/q1/start-end-to-video ~/usr/bin/bash.20, pod stayed faithful, no chemtrail.
- STATE: earth_arrive_v01.mp4 good shape but motion reads toward-camera/middle not toward-station. Rebuilding END frame to dock pod up-left by station.
- NEXT: Refire Vidu with pod-at-station end frame; then Titan-leave b-roll + reverse each for both directions.

## [2026-06-09 14:39] ? bf9f15bb
- DID: Vidu start-end b-roll: v04 fixed start glitch via seamlessClone erase of old pod footprint; clean end frame, good early/last static frames.
- STATE: Max says v04 motion is 'overall disaster' despite good static frames -- static QC missed motion artifacts. Building full-sequence montage to find what breaks in motion.
- NEXT: Inspect montage, diagnose motion failure, iterate endpoints/prompt.

## [2026-06-09 15:07] ? bf9f15bb
- DID: Deterministic pod-glide b-roll PERFECT geometrically per Max (earth_arrive_DET_v05.mp4): clean alpha matte, linear constant velocity, no tilt, shrinks into depth to station. Method: cut real pod, seamlessClone-erase footprint, sub-pixel warpAffine glide over static plate.
- STATE: Max wants Earth to SPIN via Wan to kill the 'boring' static feel. Plan: Wan-animate the pod-FREE plate (earth spin), then composite the deterministic pod glide on top so Wan never touches the pod.
- NEXT: Save clean plate PNG; fire Wan2.6 i2v on it (earth rotates, camera static); composite pod-glide frames over Wan bg; QC station survival.

## [2026-06-09 16:08] ? bf9f15bb
- DID: Arrival b-roll v05: Wan Earth-spin bg + deterministic pod glide composite. Added 0.5s empty start, pod emerges LARGE (~33%) from lower-right corner, decoupled scale(linear)/position(ease-out) so pod stays big gliding in then decelerates to halt SHORT of station (no dock). Files in broll_build/: earth_arrive_SPIN_v05.mp4, composite_over_wan_v05.py, wan_spin_earth_v01.py, plate_clean.png
- STATE: v05 rendered + QC'd good, awaiting Max approval
- NEXT: If approved: build Titan-leave b-roll (swap bg) + reverse for opposite direction
