
## [2026-06-08 15:44] d3 931c33bd
- DID: Joined bcast as d3; diagnosing 2nd-spine 'between-state' lipsie bug (LIP/orange tile shows still + opens still popup). Reproduced storyboard feed in a query: 0 lipsie tiles with non-video filename in current data -- every lipsie tile points at a real mp4. So either wrong scene or video-posters look like stills. d1 handed d3 the filter-code fix; d2 = data-row hiding only; d1 holds Part-3.
- STATE: STANDBY in effect but Max said 'fix it'. Blocked: need the offending tile's job-id from Max (asked). Feed query shows clean data, so cannot fix blind without seeing the real offending row.
- NEXT: Get job-id from Max OR live-Playwright the last sb line; pull that exact jobs row (job_type/output_status/output_file/input_file); if it's a no-video lipsie, fix the dups filter in storyboard_editor.html ~L677 to show lipsie ONLY if real finished video, keep merged_member media visible; commit+push; tell d-team.

## [2026-06-08 15:46] d3 931c33bd
- DID: Phase3: storyboard 'Redo lipsie -> Failed to fetch'. D1 max job id=2719, recent lipsies 2715-2719; storyboard popup shows lipsie id 12698 which DOES NOT EXIST in jobs. ALSO combo_gui send_error(404/500) paths lack Access-Control-Allow-Origin so cross-origin 8790->8779 errors surface as 'Failed to fetch'. mb auto-close already on master.
- STATE: Storyboard (8790) shows phantom 5-digit lipsie ids not matching D1 jobs.id (max 2719). Need storyboard data source / id mapping.
- NEXT: 1) grep slideshow_server_v01.py storyboard data endpoint + where 12698 comes from. 2) add ACAO to combo_gui send_error paths. 3) NO real redo fire (0.25). Worktree musing-gagarin.
- LESSON: Cross-origin fetch to Python BaseHTTPServer endpoint returning send_error(404/500) shows as 'Failed to fetch' because send_error omits Access-Control-Allow-Origin, hiding the real status.

## [2026-06-08 15:55] d3 931c33bd
- DID: Fixed 2nd-spine between-state bug: dup tiles now cat-aware (IMG/CLP/LIP badge+border), pushed master 17640eb, verified live via Playwright
- STATE: Bug closed. 9 'lipsie' tiles were actually approved sc09 stills; root cause was frontend costume leftover from when dups lane was lipsie-only, NOT D1 data
- NEXT: Watch d-team board for D1/D2 replies; nothing else outstanding

## [2026-06-08 16:05] d3 931c33bd
- DID: Both 2nd-spine between-states fixed+pushed (17640eb mislabeled stills, 9391126 videoless lipsies), verified live, Max acked 'good acceptable'
- STATE: Bug fully closed. Ran d3 liveness handshake re: watcher collision (2 d3 sessions). I am operative d3 with continuity
- NEXT: If another d3 replies within 8min, abort; else remain sole d3. Otherwise idle/standby

## [2026-06-08 16:24] d3 931c33bd
- DID: Verified 2nd-spine drag-to-junk already works (sandbox test, junked job2714, restored, no server mutation). Both between-state fixes already pushed (17640eb, 9391126)
- STATE: Max chose B (junk). No code change needed: drag 2nd-spine tile to junk box ejects it. To-pile felt broken only because 2nd-spine overlaps the pile (no-op). To-spine works via slot drag/move button
- NEXT: Idle. Watch board. No outstanding d3 work

## [2026-06-09 15:19] d3 931c33bd
- DID: First title b-roll inserted end-to-end (D6 implemented, D4 designed+steered)
- STATE: sc09 BROLL 'opening title card' line in Notion + script_lines row 90a50746f771cf; clip c2754 bound+pinned at SB idx=-1. Merge state on sc09 preserved (surgical insert, NOT pull+migrate). System f81afaa proven in production
- NEXT: Done; b-roll feature live. Future b-rolls: same recipe (BROLL: line -> hash -> assign)

## [2026-06-10 14:27] d3 931c33bd
- DID: Trim popup polish shipped: 3 commits on master (75f2498 false-failure fix; 5a5abf0 Untrim-in-trim + bigger video/no-prompt; 05e88df stay-in-trim after Apply). All pushed, live (static popup.js/css, browser refresh only).
- STATE: D9 branch idle under c0 FULL HALT but Max keeps re-arming 4-min timer manually. Trim feature complete. _applyTrim/_untrim rebuild trim panel via _openTrim on loadedmetadata; trim CSS hides prompt+left-top+thumbstrip, video 58vh.
- NEXT: Wait for Max's next trim-popup tweak. If resumed cold: verify at localhost:8790 storyboard trim popup.

## [2026-06-10 15:08] d3 931c33bd
- DID: Fixed Assemble Video button HTTP 500 (EXPORT_OUT_DIR off unmounted G: drive -> local rehearsal_exports), tested in browser DONE 1.87MB, committed+pushed 4c29ae1
- STATE: button works end-to-end through storyboard UI; server restarted on PID 52456 port 8790
- NEXT: await Max next instruction; brainstorm b-roll-into-libretto + music overlay still paused

## [2026-06-10 17:18] d3 931c33bd
- DID: Trim popup: added Play button (local start->end playback), kept native scrub bar for scroll, auto-play after Apply. Pushed 9a5fb4b. Earlier this session: 75f2498/5a5abf0/05e88df (false-failure fix, Untrim-in-trim, bigger video/no-prompt, stay-in-trim).
- STATE: D9 autonomous per Max. All trim work on master+pushed+live (static popup.js, refresh only). Tree otherwise has other sessions' uncommitted files - leave them.
- NEXT: Wait for Max's next trim tweak.

## [2026-06-18 15:59] d3 931c33bd
- DID: D23 CANONIZED merge ids: relabeled all 57 sc10 merged takes so each take's line_hash+birth_line_hash = deterministic SPAN id 'm'+sha(sc10|startLH|endLH). Now takes of the same line-combination share an id and GATHER in the 2ND SPINE (verified Playwright: L8 shows 2 alts, L9 2, greeting shows rated variant 2772 with stars). Span parsed from each take's vocal_line [idxs]. Pins(by job_id)+rendered audio unaffected. Saved rule project_merge_canonical_id.md. Also fixed v50 bugs (Whole Scene persist + merged move-to-spine). Scratch archived.
- STATE: Storyboard at v50. New takes 2813-2817 appeared (fired by Max/other session) - included in canonization. 2ND SPINE still only shows NON-JUNK same-span takes (junk excluded by design).
- NEXT: FUTURE merges MUST use canonical span id (not random) - rule saved. Pending: scope pool to scene in whole-scene? next-round production polish (distinct stills/arr11/arr07).

## [2026-06-18 17:22] D23 ????????
- DID: D24 owns storyboard_editor.html + pile UI (lanes set: D22=lipsie data, D23=mixboard/player). Pushed pile fixes: D23's scene-filter b2b3ab9 (I pushed it - was committed-unpushed), then MY bg-plate pile filter 647761d - getBinImages drops images whose filename matches bg patterns (bg_*, extrap, iter_bg, composite_bg, pair_strip, station, window_looking, milky, force#, _8ft, original/none). Max wants ONLY Anna+Ishtab two-shots; everything else (interiors/window-bg/station/solo) = clutter.
- STATE: slideshow_server (8790) reads storyboard_editor.html FRESH per request -> Max must HARD-REFRESH (Ctrl+Shift+R), normal reload served cached HTML. bg-filter is a FIRST PASS (filename heuristic ~80%): removes obvious backgrounds, may still show some non-two-shot character images (solo/facing). No clean metadata flag for 'two ladies'. Context ~81%.
- NEXT: Max hard-refreshes, flags any remaining clutter patterns or lost two-shots -> refine _bgRe in getBinImages. Possible next: a 'two-shots only' toggle, or curation by label. 32 sc10 images tagged outside arr2-7 are hidden by scene-filter (lost-relevant) - may need retag (D22 domain, has backups).

## [2026-06-19 18:30] D30recoder 931c33bd
- DID: SPOT1 fixed: D31 re-pinned J2774 to L0-3 (verified live D1 + browser). Answered root-cause on board: J585/J2826 were stray pins not in D21 map; my v2.28 filter only hid the empty spot, didn't cause it.
- STATE: Watching/consulting D31 per Max. SPOT1 looks good to Max. D31 found systemic bug: /api/storyboard/assign rewrites jobs.line_hash on every pin -> corrupts merged reel identity. I gave GREEN (v2 independent of that sync). D24fixer to confirm mb/popup before D31 removes it.
- NEXT: Watch D31 remove the line_hash rewrite from assign endpoint; re-verify v2 spots after; my uncommitted v2.06-2.08 needs git pull --rebase before any push (D24fixer v61 on master).

## [2026-06-23 16:32] D30recoder ????????
- DID: Extended death/hang watchdog to ALL paid workers (heartbeats in image/clip/kling/lipsync ds+bb; multi-instance watchdog table, commit dfb98a5). Watchdog immediately caught image worker DOWN+job queued. Root cause: Nextcloud data/ folder intermittently unwritable (OSError22) crashed workers writing pid there - moved image/clip/kling pids OFF Nextcloud to LOCAL_STATE_DIR like reel worker (49ea7e9). All 5 workers now healthy+beating.
- STATE: All workers up+beating, watchdog covers all 5, scheduled task every 3min live. combo_gui 8779 up.
- NEXT: Watch Nextcloud data/ writability - may recur; consider moving logs off Nextcloud too if it bites again.

## [2026-06-24 08:20] D30recoder 931c33bd
- DID: Shipped merge-history: dated Notion footprints + DB-stamped supersede trail (merge_ops.finish reason+timestamp; register_merge supersede footprint). Commit a199be7 pushed.
- STATE: register_merge.py + merge_ops.py are the canonical merge path; DB=source of truth, Notion mirrors via flat fail-open footprints (never touches freehand libretto).
- NEXT: Await Max: he questioned whether real [[MERGE]] freehand wrapping should be LLM-based (I confirmed it's a TODO, not Python).

## [2026-06-24 15:22] D43 ????????
- DID: spot9 reel finalized: 2936 approved+spine-pinned (warmer faces, 4 varied Italian/Jewish gestures, walking, only-speaker-gestures); junked losers 2934/2935 (2933 already junk)
- STATE: spot9 merge sp7a518eeb5e90 done; reel 2936 is canonical
- NEXT: await Max next spot; pending: move lipsync_temp out of Nextcloud (needs Max OK)

## [2026-06-25 16:58] D53 931c33bd
- DID: Fired D40 spot7 reels 2949(v1 face-each-other, junked) + 2951(v2 motion-arc, junked). Max approved D21's 2955 instead. Saved 2955 window-watch formula to moma_prompt_rules_tomemex.md; merged to master keeping D21's fuller entry (928a56a).
- STATE: spot7 done, 2955 approved + formula documented on master
- NEXT: Apply 2955 window-watch formula (back-to-camera + no-planet-name + bg-lock) to next spots if Max asks

## [2026-06-29 17:08] D53 931c33bd
- DID: Confirmed via D1 merge ledger that Notion Scene-10 page 3300316f (20260502) is authoritative (5 registered merges all in DB, reels fired Jun25); 3890316f (20260503) is dead clean fork. Max approved fixing both: archive dup Scene10 + fix scenes.json scene-55 pointer.
- STATE: About to: (1) fix scenes.json[55] from archived 3140316f-...-8012-... to current 3480316f-...-ba34-...; (2) rename/archive Notion dup page 3890316f + drop from Current Versions index.
- NEXT: Verify scene-55 current page via notion-fetch, edit scenes.json, commit+push, then do Notion archive.

## [2026-06-29 17:10] D53 931c33bd
- DID: DONE both housekeeping fixes. (1) scenes.json[55] repointed from archived OLD page 3140316f-...-8012 to current 3480316f-...-ba34; committed+merged+pushed to master (20c273c). (2) Notion dup Scene10 3890316f (20260503) renamed to 'OBSOLETE BACKUP...', moved to Archive folder 3430316f-...-79c; Current Versions index auto-cleaned (child-link removed on move), now shows only 3300316f (20260502) for scene 10.
- STATE: Investigation complete; both fixes live. Scene-10 authoritative page = 3300316f (DB-confirmed via 5 registered merges).
- NEXT: None pending unless Max finds more. Could optionally check other scenes for dup pages.

## [2026-07-04 14:51] D56A ????????
- DID: Researched in-system merge-audio glue for D02A: sc11 per-line voices live in lines_20260510_1714 (pre-v10, no line_hash); NO canonical glue tool exists; spot1 R0merge was hand-rolled ffmpeg concat keyed by register_merge sp-hash (verified 14.45s). Reported to D02A.
- STATE: Awaiting Max green light on building a canonical merge_hash->concat-existing->merge.mp3+merges.json tool. D02A wires to register_merge+fire; I draft member->file resolver (per-member list, handles Derek 'Yes' 3x collision, raise-on-miss).
- NEXT: On go: draft resolver in sc10/combo_runner/code or sound_assembly/code

## [2026-07-18 00:37] D56A ????????
- DID: Nadali D42b rebuild in progress
- STATE: 10 new reels 3328-3337 rendered done. assemble_nadali_video_v04.py updated: reads lines_20260718 (34 lines), ORDER_TO_JOB built dynamically (reuse_job + NEW_JOBS), builds nadali_uei_full_video_v06.mp4 in build_v07. Rendering now (52 segs).
- NEXT: When done: QC + re-upload v06 to R2 temp4 (replace v05, update index.html src, delete old, keep 14d lifecycle). Same maxrempel.com/temp4 link.

## [2026-07-26 14:34] ? bcc5a95d
- DID: Built combo_s2v_local_worker.py (local Wan2.2 S2V lipsync lane driving Taygeta via ssh/scp), registered in moma_restart.py + moma_worker_watch.py, committed+pushed to master.
- STATE: 3-window ~15s drift test (prompt 3aaa9021) still rendering on Taygeta; measured ~32s/step = ~11min/window, ~33min total. GPU 100%, healthy. New lane NOT yet fired against a real MoMA job.
- NEXT: When test finishes: scp mp4 back, inspect drift, show Max. Then fire one real s2vlocal job end-to-end.

## [2026-07-26 21:25] ? ????????
- DID: s2vlocal quality fixes: worker now auto-matches still aspect + remuxes 48kHz/192k audio (committed+pushed). 720p and 960x540 both OOM'd 16GB card; 832x480/32steps fits and is rendering as job 3416 (same line/still as 3413).
- STATE: 3416 running ~17min in; cloud ref reel=3407, first-bad-local=3413
- NEXT: vocalize Max on 3416 done; present 3407 vs 3416 side-by-side via /lipser picks-link

## [2026-07-26 21:47] ? ????????
- DID: Built reel-maker circular progress ring + self-calibrating ETA (worker writes progress/eta into lipsync_params since D1 ALTER is blocked; progressCell() in runner_core.js draws SVG ring; css added). Verified live: job 3441 shows progress=26. Fixed worker timeout-requeue loop (poll ceiling 29min->80min). All committed+pushed.
- STATE: 3441 rendering 832x480/32steps (~45min), ring live. cloud ref=3407, first-bad-local=3413. worker PID 48380 new code.
- NEXT: vocalize Max on 3441 done; present 3407(cloud) vs 3441(local) side-by-side via /lipser?ids=3407,3441

## [2026-07-26 22:45] ? ????????
- DID: s2vlocal job 3441 (lesson1 line 'Telepathy is not something you must manufacture', cam_right.png, 832x480/32steps/2win) still rendering on Taygeta ~65min in; GPU 100%, worker PID 48380 alive, queue 1. Worker fixes (aspect auto-match, 48kHz/192k audio remux, base ETA 3300s) committed+pushed master 96e38ad.
- STATE: 3441 still running, healthy; cloud ref=3407, prior local=3413 (bad, 480x480). Reel-maker progress ring+ETA already shipped (commit 0014b23).
- NEXT: When 3441 saves: vocalize Max, present 3407 cloud vs 3441 local side-by-side via /lipser?ids=3407,3441. If OOM/error, re-fire at auto 832x480.

## [2026-07-26 23:12] ? bcc5a95d
- DID: Root-caused the 3441 stall: 832x480/32step render takes ~75-100min but poll ceiling was 80min, so worker timed out and re-fired duplicates that never got captured. Fixed: raised ceiling 80->160min (commit 74ce659 area, pushed). Cleared Taygeta pileup, re-fired 3441 at 832x480/steps25 (proper 16:9, smoother motion, ~40min ETA). Worker PID 11168.
- STATE: 3441 re-queued and rendering fresh at 832x480/25steps; worker patience now 160min; aspect+audio worker fixes already in master. cloud ref=3407.
- NEXT: Monitor bzoqlpdjc armed for SAVED v3441. When it lands: vocalize Max, present /lipser?ids=3407,3441 cloud-vs-local.

## [2026-07-26 23:46] ? bcc5a95d
- DID: Lesson1 API-vs-local S2V comparison set up. Both s2vlocal renders queued sequentially (single worker, PID 11168, no-parallel guard now code-enforced+pushed). 3441=main line spot05 'Telepathy is not something you must manufacture' (still cam_right.png) at 832x480/25steps; 3442=5sec spot06 'So you moved on...' (still table_profile_r.png) same settings, queued behind. Cloud refs: 3407 (spot05), 3406 (spot06).
- STATE: Max went to sleep; DO NOT vocalize. Renders finish overnight ~40min each. Worker fixes all in master: aspect auto-16:9, 48kHz/192k audio remux, poll ceiling 160min, no-parallel guard, cold-start ETA 3300s.
- NEXT: When done, present side-by-side: cloud vs local spot05 -> http://localhost:8779/lipser?ids=3407,3441 ; spot06 -> http://localhost:8779/lipser?ids=3406,3442 . Also show output_prompt. Check both saved (output_file set, status done).

## [2026-07-26 23:48] ? ????????
- DID: OVERNIGHT BATCH: fired s2vlocal twins of the full approved Lesson1 opening (spots 1-10). Active queue: 3441(running),3442,3443,3444,3445,3446,3447,3448,3449,3450 - all 832x480/25steps, single worker PID 11168 sequential, no-parallel guard live. Each twin cloned still+blh+prompt from its cloud source (3403-3412) so audio via blh is correct.
- STATE: 10 local reels rendering overnight ~40min each (~6-7h total). Max asleep, NO vocalize. All worker fixes in master (aspect/audio/ceiling/guard).
- NEXT: Morning: verify each has output_file+done; present cloud-vs-local per spot in /lipser (e.g. 3407 vs 3441). If any errored, check s2v_local_worker.log and re-fire. Cloud opening jobs=3403-3412.

## [2026-07-27 08:00] ? bcc5a95d
- DID: NEW BUG (Max 2026-07-27): s2vlocal reels glitchy mouth 'from the middle' - portrait/face similarity GREAT but mouth super glitchy mid-clip. Tested 3441+3442, both 2-window. Strong hypothesis: Wan2.2 S2V multi-window EXTEND seam bug in ~/setup/scripts/s2v_render.py on Taygeta (window1 WanSoundImageToVideo -> Extend windows; seam at ~5s where glitch starts). Not poor quality - a fixable settings bug.
- STATE: 10-reel overnight batch (3441 run + 3442-3450 queued) all likely glitchy TRASH. Max order: FIX first, THEN stop current worker, trash all current-cue outputs, restart new batch with fixed render.
- NEXT: Research online Wan2.2 S2V extend/window mouth-glitch + correct params (motion_frames/overlap/audio slice); read render script; fix; stop worker PID 11168; junk 3441-3450 outputs; re-fire clean. Cloud refs 3403-3412.

## [2026-07-27 08:03] ? ????????
- DID: STOPPED+JUNKED the glitchy batch. Killed s2v worker PID 11168, interrupted+cleared Taygeta ComfyUI queue, marked 3441-3450 output_status=junk. Diagnosis (subagent, full result in tasks/a78312d7278d2ac40.output): in ~/setup/scripts/s2v_render.py the multi-window EXTEND loop feeds each WanSoundImageToVideoExtend the previous KSampler latent as video_latent, so frame_offset=video_latent.shape[-3]*4 does NOT accumulate -> audio window stops advancing after window2 -> glitchy mouth. Native design wants a CUMULATIVE (concatenated) latent fed to each Extend so offset grows by ~84/window.
- STATE: OPEN QUESTION: Max says even 5-sec clips glitchy throughout, but those were still 2-window (6s). Need to test a TRUE 1-window clip (audio<=4.2s) to isolate whether window-1 alone is also glitchy (=global setting: steps/sampler/cfg/shift/audio_scale/fps) vs purely the seam-offset bug. Worker currently STOPPED (not running).
- NEXT: FRESH SESSION: (1) read s2v_render.py extend loop; implement cumulative-latent fix (concat prior window latents into next Extend video_latent). (2) Fire ONE true single-window test (short audio) to check global quality. (3) If window1 also glitchy, chase steps/cfg/shift/fps=16/audio_scale vs known-good Wan2.2 S2V. (4) Verify ONE good clip before re-batching lesson1 opening (cloud refs 3403-3412). Restart worker: pythonw combo_s2v_local_worker.py. Worker has no-parallel guard + aspect/audio fixes already in master.

## [2026-07-27 08:13] ? bcc5a95d
- DID: Fixed s2vlocal jumpy/angry render: added ModelSamplingSD3 shift=8 node to Taygeta s2v_render.py (was missing -> violent motion), length 81->77, cfg 6->5, dropped 'static' from neg. Verified cloud prompts ARE copied+forwarded. Committed+pushed (worker + render mirror). Test job 3451 rendering on Taygeta (prompt_id ac3bd560, 2-window ~50min).
- STATE: Test 3451 in-flight on Taygeta; worker PID 35284 running; render v1 backup on Taygeta
- NEXT: When 3451 done: pull mp4, extract mid-speech frames, judge reserved-not-angry + non-glitchy. If good, batch rest of Lesson1 opening (twins of cloud 3403-3412) for Max to review. Do NOT self-approve.
- LESSON: Missing ModelSamplingSD3 shift node = default violent motion in Wan2.2 S2V; official workflow requires it. 'static' in a NEGATIVE prompt drives MORE motion.

## [2026-07-27 09:09] ? ????????
- DID: Shift-node fix VERIFIED on test 3451: window-1 frames calm/natural/reserved (angry look gone). But window-2 (multi-window seam at frame 77) renders DARKER+harsher = remaining problem. ALL 10 opening lines are 5-8.6s = 2-window, so all affected. Fix path: render each line as ONE longer window (no seam). Added --frames to s2v_render.py (single-window mode, redeployed). Fired QC single-window test (prompt_id 1887941e, 161 frames, reusing 3449 assets) to check if single window holds over 2x trained length.
- STATE: Single-window QC render in-flight on Taygeta ~47min. Worker NOT yet switched to single-window; will rewire only if test passes. Worker PID 35284 idle (no queued jobs).
- NEXT: When QC render done: pull qc_single161*.mp4, extract seam-region + spread frames, check NO darkening/drift/loop end-to-end. If clean: rewire worker to single-window (frames from dur, drop --windows), batch twins of 3403-3412. If it drifts/loops: fall back, report to Max, do not batch.
- LESSON: Wan2.2 S2V multi-window Extend drifts exposure darker in window 2; single longer window avoids the seam but may drift/loop past ~77 trained frames — must verify.

## [2026-07-27 10:37] ? ????????
- DID: Fixed s2vlocal jumpy/angry render + window-2 darkening. Root causes: (1) missing ModelSamplingSD3 shift node -> added shift=8; length 81->77, cfg 6->5, dropped 'static' from negative. (2) multi-window Extend drifts exposure darker -> switched to SINGLE-WINDOW render (no seam). Both committed+pushed to master. Worker restarted (PID 43032) with single-window code.
- STATE: Batch of 10 Lesson1-opening s2vlocal twins QUEUED (jobs 3452-3461, twins of cloud 3403-3412). 3452 rendering single-window 129f@832x480. Single worker + no-parallel guard renders one at a time, ~50-70min each, ~9-11h total. Prompts CONFIRMED copied from cloud source (worker forwards output_prompt).
- NEXT: Monitor overnight batch for stalls/errors; when all 10 done leave Max a picks-link on /lipser to review. DO NOT self-approve any reel.
- LESSON: wan2.2 S2V jumpiness = missing ModelSamplingSD3 shift node (needs shift~8); multi-window Extend = exposure drift, prefer one long window.

## [2026-07-27 11:17] ? ????????
- DID: Max reviewed first single-window S2V reel: still bad (helped a little, not enough). Searched online thoroughly. VERDICT: Wan 2.2 S2V is a weak model for talking-head (independent testers: 'cannot be recommended in current state'); the good earlier movie was Wan 2.2 I2V (silent), a different+better model than S2V. Fix = switch local lipsync engine to MultiTalk (short single-face champion, digital-makeup-on-face = reserved, fast, 16GB-friendly) or InfiniteTalk (more stable, slower). Kijai WanVideoWrapper already installed on Taygeta with multitalk/infinitetalk modules; GPU freed.
- STATE: Paused S2V batch: jobs 3453-3461 held, 3452 interrupted. Spawned Sonnet research agent for exact MultiTalk model files/URLs + verified node workflow. Worker (PID 43032) idle-safe (no queued jobs).
- NEXT: Get MultiTalk plan from agent, download weights to Taygeta, build multitalk render script, test ONE Anna reel, QC (no jitter/steady/reserved) before rewiring worker or batching. Do NOT self-approve.
- LESSON: Wan 2.2 S2V != Wan 2.2 I2V; S2V is the weak audio talking-head variant. For local talking heads prefer MultiTalk/InfiniteTalk via Kijai WanVideoWrapper.

## [2026-07-27 11:48] ? ????????
- DID: MultiTalk weights fully downloaded to Taygeta (16GB base Wan2.1-I2V-480p-fp8 + 2.6GB MultiTalk fp8). Fixed a SaveVideo format/codec bug in taygeta_multitalk_render.py (was 'C', hardcoded mp4/h264), redeployed. FIRED first MultiTalk test render: prompt_id 9542dc9e, using still mt_test_zoom_in.png + audio momajob3452_aud.wav (=cloud job 3403 Anna line), 201f 832x480 steps30 cfg6 shift5 blocks_swap25.
- STATE: MultiTalk render 9542dc9e RUNNING on Taygeta (~30-60min). Renamed session K2b->WD71 on 'wd' board. WD72 holds GPU, will test InfiniteTalk (fp8 file pinned: Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors from Kijai/WanVideo_comfy_fp8_scaled) after me. Bad S2V batch held (3453-3461).
- NEXT: When render done: pull mp4 from Taygeta ~/ComfyUI/output/mt_test01*.mp4, QC frames (steady light, reserved expression, faithful face, NO jitter) vs bad S2V reel. If clean -> rewire combo_s2v_local_worker.py to multitalk lane (RENDER_SCRIPT=s2v_multitalk_render.py) + commit + ping WD72 GPU-free. If not -> report Max. DO NOT self-approve.

## [2026-07-27 12:20] ? bcc5a95d
- DID: MultiTalk test render 9542dc9e FAILED at node MultiTalkWav2VecEmbeds: RuntimeError weight shape [1024] vs normalized_shape [768]. ROOT CAUSE: wav2vec2 model mismatch — the on-disk wav2vec2_large_english_fp16 is 1024-dim (large); MultiTalk/InfiniteTalk REQUIRE the 768-dim TencentGameMate/chinese-wav2vec2-base. The prior research agent's 'reuse the English wav2vec' advice was WRONG. Rest of pipeline (models load, graph wiring, SaveVideo mp4/h264 fix) is fine — only the audio encoder is wrong.
- STATE: GPU FREE (render errored, no output). MultiTalk fully installed except correct wav2vec2. Script taygeta_multitalk_render.py deployed+committed (SaveVideo bug fixed, NOT yet re-committed with that edit). WD72 holding for InfiniteTalk. Bad S2V batch held (3452-3461).
- NEXT: FIX: on Taygeta, use the DownloadAndLoadWav2VecModel node (auto-fetches chinese-wav2vec2-base 768-dim) OR wget the TencentGameMate/chinese-wav2vec2-base into ~/ComfyUI/models/wav2vec2/ and point Wav2VecModelLoader at it. Edit taygeta_multitalk_render.py node 4 accordingly, redeploy, re-fire same test (still mt_test_zoom_in.png + audio momajob3452_aud.wav, 201f). Then QC. Commit the SaveVideo fix too. Do NOT self-approve. I am WD71.
- LESSON: MeiGen MultiTalk + InfiniteTalk need 768-dim chinese-wav2vec2-base, NOT the 1024-dim large English wav2vec2. Wrong encoder = layer_norm [1024]vs[768] RuntimeError at MultiTalkWav2VecEmbeds.

## [2026-07-27 12:59] ? bcc5a95d
- DID: MultiTalk test02 (26ec72e3) failed at node 5 LoadWanVideoT5TextEncoder: 'fp8 scaled is not supported'. The umt5_xxl_fp8_e4m3fn_SCALED encoder is rejected by WanVideoWrapper's T5 loader. FIX: downloading non-scaled umt5-xxl-enc-fp8_e4m3fn.safetensors (~6.7GB @12MB/s) to Taygeta ~/ComfyUI/models/text_encoders/ (done-flag ~/t5_dl.done). Edited script node 5 to that filename, redeployed+committed+pushed. This is the 3rd bring-up fix (after wav2vec2 768-dim + SaveVideo mp4/h264).
- STATE: T5 download in progress on Taygeta. GPU free. Script taygeta_multitalk_render.py fully fixed on paper, awaiting T5 file to re-fire. WD72 holding GPU for InfiniteTalk. Bad S2V batch held (3452-3461).
- NEXT: When ~/t5_dl.done exists: re-fire test: ssh maxre@192.168.1.142 'cd ~/ComfyUI && ./venv/bin/python ~/setup/scripts/s2v_multitalk_render.py --image mt_test_zoom_in.png --audio momajob3452_aud.wav --frames 201 --width 832 --height 480 --steps 30 --cfg 6 --shift 5 --fps 25 --blocks_swap 25 --out_prefix mt_test03'. Then QC mp4 (steady/reserved/faithful/no-jitter vs bad S2V). If clean: rewire worker to multitalk + commit + requeue 3452-3461 + free GPU for WD72. If error: grunt-extract + fix. Do NOT self-approve. I am WD71.
- LESSON: WanVideoWrapper LoadWanVideoT5TextEncoder rejects fp8-SCALED umt5; use non-scaled umt5-xxl-enc-fp8_e4m3fn or bf16.

## [2026-07-27 13:43] ? bcc5a95d
- DID: MultiTalk bring-up: 4th fix = WanVideoVAELoader needs precision=bf16 (was missing). Committed+pushed+redeployed. Fired test04 prompt 73ff4f08. Fixes so far: (1) wav2vec2 768-dim base, (2) SaveVideo mp4/h264, (3) non-scaled fp8 umt5 T5, (4) VAE precision=bf16. All committed. All 5 model files now present on Taygeta.
- STATE: test04 rendering/validating. GPU busy. WD72 holding for InfiniteTalk. Bad S2V batch held 3452-3461.
- NEXT: Short-wake ~180s to catch a fast config error; if still running re-arm ~1500s to QC. If error: grunt-extract + fix next node. If mp4: QC vs bad S2V, if clean rewire worker to multitalk + commit + requeue + free GPU for WD72. Do NOT self-approve. I am WD71.

## [2026-07-27 13:54] ? bcc5a95d
- DID: MultiTalk bring-up fixes 5-6: (5) WanVideoModelLoader now loads full base Wan2_1-I2V-14B-480P_fp8 (MultiTalk file is add-on via multitalk_model input); (6) BlockSwap needs vace_blocks_to_swap=0 (sampler read None). All committed+pushed. Fired test06 prompt 68278929. Base model loaded (GPU hit 12GB) so loader chain is good; now past blockswap init.
- STATE: test06 rendering/validating. 6 config fixes total in taygeta_multitalk_render.py, all committed. Model files all present. GPU busy. WD72 holding for InfiniteTalk. S2V batch held 3452-3461.
- NEXT: Short wake ~180s: if rendering re-arm ~1500s to QC; if error grunt-extract+fix next node, refire mt_test07. When mp4: QC vs bad S2V (steady/reserved/faithful/no-jitter). If clean rewire worker RENDER_SCRIPT->s2v_multitalk_render.py + commit + requeue 3452-3461 + free GPU for WD72. Report Max verdict+frame. Do NOT self-approve. I am WD71.

## [2026-07-27 13:59] ? bcc5a95d
- DID: MultiTalk: ALL 6 config bugs cleared — test06 reached the SAMPLER and hit real CUDA OOM in VAE encode (10.74GB allocated, 441MB short) at 201 frames/blocks_swap25. Wiring 100% correct now. Refired test07 prompt 08b335a5 with blocks_swap 40 + frames 81 (CLI only, no code change) to fit 16GB.
- STATE: test07 rendering/OOM-check. If it renders, MultiTalk WORKS — then tune frames upward for production length + maybe VAE tiling. 6 config fixes committed. GPU busy. WD72 holding. S2V held 3452-3461.
- NEXT: Short wake ~180s: if OOM again -> add enable_vae_tiling=True to WanVideoDecode node 13 + lower res or frames; if rendering -> re-arm ~1200s to QC. When mp4: QC vs bad S2V. If clean rewire worker + requeue + free GPU for WD72. Note: production reels are 5-9s so need ~130-225 frames; if 81 works but 201 OOMs, must enable VAE tiling for full-length. Do NOT self-approve. I am WD71.

## [2026-07-27 14:06] ? bcc5a95d
- DID: MultiTalk test07 (blocks_swap40/frames81): ComfyUI PROCESS CRASHED mid-render (not OOM — 26GB RAM free; no oom-killer). All 6 config fixes correct; earlier 201f gave graceful CUDA OOM, but 81f/blocks40 hard-crashed the server. Restarted ComfyUI detached (nohup, log ~/comfyui_run.log).
- STATE: ComfyUI restarting on Taygeta. Need to check crash cause in ~/comfyui_run.log then re-fire. 6 config fixes committed. GPU idle. WD72 holding. S2V held 3452-3461.
- NEXT: When ComfyUI up (curl 127.0.0.1:8188/system_stats): check tail of ~/comfyui_run.log for the test07 crash traceback (Blackwell/sage/attention? VAE?). Then re-fire test08 at frames 81 blocks_swap 30 (moderate). If crashes again, try WITHOUT blockswap edge cases or lower res 640x384. If renders, QC vs bad S2V. Do NOT self-approve. I am WD71.

## [2026-07-27 15:52] ? bd549dbe
- DID: Lesson1 music underlay pilot. Built C:\moma\sc10\sound_assembly\code\music_underlay.py (chops select2 Suno tracks ~20s, loudnorm -16, stitches bed, mixes under voice at 50%). Voice assembly = C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\previews\lesson1_listen_20260726_v01.mp3 (284s, 34 spots). Output in ...\lesson1_production\music_mix\out\.
- STATE: Max REJECTED v01: no crossfade (I butt-joined pieces, only 0.3s edge fades = hard switches). He wants (1) REAL crossfade between music pieces, (2) music changes at LOGICAL places = at the REEL/spot boundaries of the lesson, whose positions-in-seconds come from MOMA. DO NOT delete anything in music_mix yet (Max wants to compare).
- NEXT: 1) Find existing optimized music-overlay/crossfade script (maybe D43b's, or elsewhere in claude_base). 2) Get reel boundary times in seconds for the lesson1 voice assembly (from lines_20260726/manifest.json + the assembly/concat script that built the 284s mp3). 3) Rewrite music_underlay to crossfade music AT reel boundaries. 4) Re-mix at 50%, let Max listen.

## [2026-07-27 15:55] ? bd549dbe
- DID: Lesson1 music underlay. My music_underlay.py v01 (C:\moma\sc10\sound_assembly\code\music_underlay.py) REJECTED: butt-join no crossfade. No prior overlay script recoverable (git never tracked it; no backup). Existing music system to inspect (maybe the optimized scheme): music_projects_method_v01_tomemex.md, music_editor.html, music_project_import.py in same folder - NOT yet read.
- STATE: NEW ALGORITHM from Max (verbatim intent): reels are ~6s each. Use ONE music piece per TWO reels, then change. Music-piece transitions MUST land exactly on reel boundaries, with a real CROSSFADE (acrossfade ~0.5-1s) at each. Steps: (a) get reel boundary times in seconds, (b) for each 2-reel group compute needed music length, (c) cut music pieces from select2 of exactly those lengths, (d) crossfade-glue them. THEN output a VIDEO: big NUMBER top-left = which music source piece is playing (any order); Max watches, says 'dump N', we replace those. Use select2 (now has LOTS more tracks) - pick lots of pieces. SKIP auto quiet/slow selection. music_gain=0.5. Light bg (never dark). DO NOT delete music_mix contents.
- NEXT: 1) Get EXACT reel boundary times: reel durations in lesson1_production/lines_20260726/manifest.json (34 spots ~6s, fields order/file/duration); find the assembler/concat script that built previews/lesson1_listen_20260726_v01.mp3 (284s) to get the inter-reel PAUSE so boundaries are exact (else drift). If not found, re-assemble voice from the 34 spot wavs with known pause so boundaries are controlled. 2) Rewrite music_underlay: 2-reel music segments, cut to exact length, acrossfade at reel boundaries. 3) Build QC VIDEO w/ big numbered top-left label per music piece, audio=voice+music@50%. 4) Let Max listen/watch, dump bad numbers, replace, rebuild.

## [2026-07-27 16:56] ? 5e7b151e
- DID: Lesson1 music-numbered video v02 DONE + approved by Max (C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\music_mix\out\lesson1_numbered_musicvid_50pct_v02_20260727_161424.mp4, 34 reels, 4:36, crossfade at trimmed reel boundaries from scene305 segments.json, numbers top-left, music 50%). Scripts: music_numbered_vid.py / _v02.py (NOT committed). Max then asked to 'produce the rest of the lesson' (expected ~20 min) through MOMA properly.
- STATE: KEY FINDING (Explore agent): the FULL AUTHORED lesson is only 34 spots ~4.4 min. Libretto = telepathy_lesson1_v01.md (spots01-10) + v02.md (spots11-34); NO v03+. Voice 100% done (34 wav in lesson1_production). Lesson1 = MOMA D1 scene_id='lesson1', arrangement_id=42 (hist. Scene 11 / Tape1Select). v02 video ALREADY covers all 34. So NOTHING rendered is missing; to reach ~20min the SCRIPT must be EXTENDED ('upgrade the notion'). That's creative content -> asked Max whether to draft the extra ~15min spots or he provides text.
- NEXT: AWAIT Max's answer on script content. THEN through MOMA: (1) extend libretto/Notion with new spots, (2) sass voice via sass_recipe_anna_lesson_v01.py --libretto <new>, (3) build_lesson1_audio_run_v01.py to register lines, (4) fire_lesson1_reels_v*.py (wan26flau, scene_id=lesson1, arr 42) - PAID ~ per reel, (5) worker renders, (6) render_mixboard_video_v01.py assemble, (7) music_numbered_vid on new segments.json. Do NOT circumvent MOMA. Cost gate at reel render.

## [2026-07-27 17:38] ? 5e7b151e
- DID: Max leaving for hours. AUTHORIZED autonomous job: import the REMAINING Lesson1 lesson text into MOMA, PRODUCE THE SOUND (voice spend authorized), place everything on the storyboard, and SIGNAL the other session to render the reels. All through MOMA, no circumvention. I (D42B) must NOT run the paid Wan/avatar render myself - other session does reels; I stage + signal.
- STATE: Launching background mule agent to: (1) FIND remaining lesson text (Notion first - the lesson opens 'You are already telepathic...'; else Memex/filesystem/telepathy_tapes) - do NOT fabricate if none exists, report loudly; (2) import into libretto telepathy_lesson1_v03.md (SPOT blocks from spot35, <=15s each) + reflect in Notion; (3) voice new spots via sass_recipe_anna_lesson_v01.py (Fish, authorized); (4) register + place on storyboard (scene_id='lesson1', arrangement_id=42); (5) stage lipsie jobs via fire_lesson1_reels pattern (NO paid render) + signal other session via fleetcomm + bcast/dm D43b. Lesson1 state: 34 spots done (v01 01-10 + v02 11-34), do NOT re-synth.
- NEXT: Await agent completion (background). On return verify: text source, #new spots/total/minutes, Notion write, voice done, storyboard placement, reel jobs staged, other session signaled. Music-numbered video v02 already approved (music_mix/out). Guard: no orphan media (fire_job/register only), no visible terminals, don't re-synth 34, don't run Wan, don't delete.

## [2026-07-27 17:41] ? 5e7b151e
- DID: Found full Notion Lesson1 libretto (3 approved pages: Min0-5=done, Min5-10 + Final5min=new). Wrote v03 libretto spots 35-112 (78 new spots, ~11min). Preflight passed all under 15s.
- STATE: Fish TTS synth running in background for v03
- NEXT: wait for synth, verify durations, then run build_lesson1_audio_run to register into D1, then write+run fire_lesson1_reels_v06 for spots 35-112, then signal fleetcomm+bcast

## [2026-07-27 17:47] ? 5d67b10d
- DID: H42B resumed after prior process death. DURABLE STATE CONFIRMED: v03 libretto (spots 35-112, 78 new spots from 3 approved Notion pages Min5-10 + Final5) imported AND git-committed (2316be4). VOICE for all 78 new spots ALREADY PRODUCED (78 wavs anna_*_spot35..112.wav in lesson1_production) - synth finished before the crash. So libretto imported + sound produced = DONE.
- STATE: Launched finishing agent (a69a8fe5): verify durations, REGISTER spots 35-112 into MOMA (build_lesson1_audio_run pattern, scene_id=lesson1 arr42), place on storyboard, write+run fire_lesson1_reels_v06 to STAGE lipsie jobs (wan26flau, no paid render), signal reel session via fleetcomm+bcast, commit+push fire script. NOT re-synthing, NOT running Wan.
- NEXT: On agent completion verify: registration count, storyboard placement, reels staged (status), signals sent, pushed. Then Lesson1 = libretto+sound complete, reels awaiting the render session. Max (H42B) expects on return: whole libretto imported + sound implemented (both durable-done).

## [2026-07-27 17:48] ? 5d67b10d
- DID: Registered lesson1 spots 35-112 audio: ran build_lesson1_audio_run_v01.py, merged manifest_v03.json (78 new spots) into lines_20260726/manifest.json alongside v01+v02; all 112 spots present, no gaps; verified all 78 new wavs <=15s (max 11.15s)
- STATE: Local audio manifest complete for spots 1-112. No D1 write yet.
- NEXT: Next: fire spots 35-112 onto lesson1 spine as output_status=held (matching fire_lesson1_reels_v02.py pattern), write fire_lesson1_reels_v06.py

## [2026-07-27 17:49] ? 5d67b10d
- DID: Fired fire_lesson1_reels_v06.py (new script, modeled on v02): placed spots 35-112 (78 lines) onto lesson1 spine as job_type=lipsie, scene_id=lesson1, arrangement_id=42, lipsync_tool=wan26flau, output_status=held. Job ids 3486-3564. Verified in D1: all 78 spots present, one row each, all held, no queued/render triggered.
- STATE: Registration + storyboard placement + staged (unrendered) reels all complete for spots 35-112. Nothing rendered, no cost incurred.
- NEXT: Next: signal reel-rendering session (fleetcomm + bcast), commit+push fire_lesson1_reels_v06.py to master, then done.

## [2026-07-28 02:03] H42B ????????
- DID: Locked Max's exact original lesson1 prompt verbatim (candlelight+alone+push-in); built scene-specific prompt_lock guard in wan26 worker (refuses render+spend on drift); banned table_low.png still; fired 8 gap reels
- STATE: 8 uncovered lines queued, guard live+committed+pushed
- NEXT: review 8 renders, approve/junk; offer to repoint held table_low reels

## [2026-07-28 02:46] H42B bd549dbe
- DID: Built scripted per-line gesture prompts for Lesson1 reels (permanent locked header + variable line->gesture->line->gesture body with timing, gestures from gesture_picker_v01). Fired 10 (spots 57-66, jobs 3570-3579) via sanctioned fire_job (DB raw-write guard blocks UPDATE). Committed+pushed ca999b1.
- STATE: Worker pid 23088 alive, draining earlier batch (3504 running, 3505-3507) then my 10. Coverage was 48/112 with video; +10 rendering. table_low.png banned; prompt-lock enforces candlelight/alone/push-in; new reels get worker's default anti-glossy negative prompt + audio auto-resolved from birth_line_hash.
- NEXT: Babysit render for ~8h: keep worker alive (relaunch HIDDEN if dead, never quit it), re-fire any hard 'error' among 3570-3579, do NOT fire beyond these 10 (Max reviews the new scripted style first), then HOLD.
- LESSON: Locking a prompt verbatim killed the per-line gesture orchestration; the fix is permanent(locked)+variable(scripted) split, not one static sentence. Fire reels via fire_job, not raw UPDATE (MoMA DB guard).

## [2026-07-28 08:41] H42B bcc5a95d
- DID: Redirected local render test to EXACT cloud Lesson1 formula (job 3403 prompt 'A woman sits at a kitchen table at night...', still zoom_in.png, audio momajob3452). Background mule ac2db103cf209c42c rendering s2v_real (S2V) + mt_real (MultiTalk 640x384) one at a time; extracts frames to scratchpad/renders/. Cloud reference frames cloud3403_start/mid.png extracted.
- STATE: Mule rendering; GPU busy; WD72 waiting. Cloud reel is the perfect benchmark. Key insight: local=Wan2.2 S2V (weak), cloud=Wan2.6 wan26flau (perfect) - same model family, different checkpoint.
- NEXT: On mule completion: view local frames vs cloud3403 frames, judge steadiness/expression/face-fidelity, report Max WITH pictures + honest verdict (can local match cloud, or render 20min/wk on cloud). Do NOT self-approve.

## [2026-07-28 08:59] H42B bcc5a95d
- DID: Lesson1 scripted reels: 9/10 rendered done (spots 57-61,63-66 = jobs 3570-3574,3576-3579). Spot62 (job3575) hit a transient 403 from Wan/dashscope; re-fired as job3580 (queued) via fire_job. New prompt style = locked permanent header + variable line->gesture->line->gesture body (gesture_script_v01 + fire_lesson1_scripted_v10_h01, pushed ca999b1).
- STATE: Worker pid 23088 alive. All 10 spots 57-66 now covered (9 done + 3580 rendering). ~46 held-only lines remain for future batches. Earlier batch (spots ~46-55) all done.
- NEXT: Babysit until 3580 done: run scratchpad/babysit_h01.py; keep worker alive (relaunch HIDDEN, never quit); re-fire any hard error for its line via fire_job. Do NOT fire beyond spots 57-66 - Max reviews the scripted style first, then bless before next batch. Keep lighting/prompt locked; table_low.png banned.

## [2026-07-28 09:15] H42B bcc5a95d
- DID: COMPLETE: all 10 scripted Lesson1 reels rendered done (spots 57-66). Jobs 3570-3574, 3576-3579, and 3580 (spot62 re-fire after transient 403; old 3575 errored, superseded). New style = locked permanent header + variable line->gesture->line->gesture body (gesture_script_v01 + fire_lesson1_scripted_v10_h01, pushed ca999b1).
- STATE: Worker pid 23088 alive/idle. All spots 57-66 covered; reels auto-seed onto empty storyboard spots. ~46 held-only lines remain for future batches once Max blesses the scripted style. Nothing rendering.
- NEXT: HOLD for Max's review of the scripted reels. Do NOT fire beyond spots 57-66 until Max approves the style. If Max says go, run fire_lesson1_scripted_v10_h01.py --n 10 for the next batch. Keep lighting/prompt locked; table_low.png banned.

## [2026-07-28 09:51] H42B bcc5a95d
- DID: Lesson1 reels: 10 scripted done (spots 57-66). Caught bad gesture: dying line spot62 got a TWO-FINGER counting gesture (keyword 'either' triggered it). Re-fired spot62 as job3581 with Max's prayer-45 gesture (both palms together, near-prayer, fingertips 45deg forward/down, then rest). MAX NOW COMMANDS the systemic fix: gesture assignment must be SEMANTIC (LLM reads each sentence's meaning + picks from an annotated catalog), NOT the keyword picker (he called keywords 'a super idiotic shortcut'). He authorized full implement.
- STATE: Keyword picker = gesture_catalog/gesture_picker_v01.py (detect_tags trigger words). Composer = gesture_catalog/gesture_script_v01.py (compose_scripted, permanent header + interleaved line->gesture body). Fire = code/fire_lesson1_scripted_v10_h01.py (fire_job path). Catalog = gesture_catalog/gesture_catalog_v01.json (41 gestures, currently only keyword tags, no rich meaning). prompt-lock enforces candlelight/alone/push-in. table_low.png banned.
- NEXT: IMPLEMENT SEMANTIC GESTURES: (1) annotate ALL 41 gestures in catalog with real semantic MEANING (emotion/idea/when-to-use) + add prayer-45 death/reverence gesture -> gesture_catalog_v02.json; (2) build semantic picker: LLM reads each sentence, picks best-meaning gesture from annotated catalog; use DeepSeek headless (sanctioned non-interactive route) or in-session Opus judgment; cache per line_hash. (3) recompose + re-fire reels with semantic gestures (keep permanent header locked). Max: 'Absolutely semantically, there is no way around.' Nothing blocking needed from Max; may show him key mappings (death/connection/telepathy) for taste. Also: junk old 3580 so board shows 3581.

## [2026-07-28 10:16] H42B bcc5a95d
- DID: Built SEMANTIC gesture system (Max: keywords prohibited). catalog_v02 = all 41 gestures annotated with MEANING + new prayer_palms_45 (death/reverence). gesture_script_v02.compose_semantic + gesture_assignments_v01 (67-71) + fire_lesson1_semantic_v11. Pushed 428d82b. Fired 5 semantic reels spots 67-71 (jobs 3583-3587). Fixed spot62 dying: two-finger -> prayer gesture (job3581 done, old 3580 junked). Posted reel REGISTRY to board (h01 claims 67-71; open 72-111). DM'd H03 to reconcile a STANDARD FORK.
- STATE: Worker pid 23088 alive: 3581 done, 3583 running, 3584-3587 queued. STANDARD FORK unresolved: h01 = candlelight header + curated semantic catalog; H03 = older lamplight/static header + DeepSeek free-text gestures (H03 holds spots 100-112, spot 112=job3582). Header candlelight is Max's latest lock; gesture-engine (catalog vs DeepSeek) is the real open question. Surfaced to Max (live). Tooling all in gesture_catalog/ + code/fire_lesson1_semantic_v11_h01.py.
- NEXT: Babysit 3583-3587 to done (scratchpad/babysit_h01.py, MINE=3581,3583-3587). When Max picks the unified standard: converge with H03 - proposal = candlelight header + catalog_v02, DeepSeek PICKS from catalog by meaning (keeps H03 scale + no-repeat image picker). Do NOT touch 100-112 (H03's). Do NOT fire beyond 67-71 without Max. Keep lighting/prompt locked; table_low.png banned.

## [2026-07-28 10:18] H42B 5d67b10d
- DID: H05 (branched from h01): claimed Lesson1 reels spots 72-76 on the bcast board (h01 has 67-71, H03 has 100-112). Authored gestures with the LLM per Max's new spec: each line = the woman's emotion + preceding/during/following gesture, ~7 beats per 15s proportional, tamed for heavy doctrine lines, warmer for the personal story/wonder. Fired jobs 3588-3592 via sanctioned fire_job. Committed+pushed 1b7d3bc (fire_lesson1_authored_h05.py). Locked header + semantic gestures = the standard Max wants (not H03's older-header/keyword variant).
- STATE: Worker pid 23088 alive, my 5 all queued (covered 5/5), 0 errors. Uses gesture_catalog_v02.json (42 gestures annotated with MEANING + prayer_palms_45). Permanent header locked; table_low.png banned. Board registry: OPEN spots 77-99 for other sessions.
- NEXT: Babysit until all 5 done: scratchpad/babysit_h05.py keeps worker alive (relaunch HIDDEN, never quit) + self-heals errors by re-running the idempotent fire_lesson1_authored_h05.py. Do NOT fire beyond 72-76 (my block). When all 5 done, park long + HOLD for Max's review. If Max wants more, claim the next OPEN block on the board first.

## [2026-07-28 10:32] H42B 5d67b10d
- DID: COMPLETE: all 5 semantic reels done (spots 67-71 = jobs 3583-3587) + spot62 prayer fix (3581). Zero errors. Semantic system live (catalog_v02 annotated + gesture_script_v02 + assignments + fire_v11), pushed 428d82b. Registry on board.
- STATE: Worker alive/idle. Team converging on MY standard: H05 claimed 72-76 using locked-header + semantic gestures. H03 (lamplight+DeepSeek, spots 100-112) still pending Max's ruling on the standard fork. Spots done so far: 57-71 (+ earlier ~46-55). Open for siblings: 77-99, 100-112(H03), 72-76(H05).
- NEXT: HOLD for Max: (1) his ruling on unified standard (recommend candlelight header + catalog_v02, DeepSeek picks from catalog by meaning); (2) his review of the semantic reels; (3) his go for more. Do NOT fire beyond 67-71 without Max. Do NOT touch 100-112. Keep lighting/prompt locked; table_low.png banned.

## [2026-07-28 10:39] H42B 5d67b10d
- DID: H05 COMPLETE: all 5 claimed Lesson1 reels (spots 72-76, jobs 3588-3592) rendered DONE. LLM-authored semantic gestures (emotion + preceding/during/following per line, ~7 beats/15s, tamed heavy lines / warmer story). Pushed 1b7d3bc. Board updated: 72-76 done, OPEN 77-99.
- STATE: Worker pid 23088 alive. My block done, 0 errors. Adviser note about 'stop building catalogs' already satisfied - H05 authored prompts directly (no picking tool in the fire path). Reels auto-seeded onto storyboard spots 72-76.
- NEXT: HOLD for Max's review of the new authored-gesture style before mass-producing 77-99. Do NOT grab another block unless Max says continue (other branches own other blocks; claim on board first if he does). Keep worker alive for siblings. Visual QC by Max pending.

## [2026-07-28 11:42] H42B 5d67b10d
- DID: STANDARD FORK RESOLVED: H03 converged on my candlelight header + gesture_catalog_v02 (DeepSeek now SELECTS gesture ids by MEANING via compose_semantic, no free-text); H05 also on my standard. Whole team aligned on candlelight+semantic. My reels 57-71 all done.
- STATE: Team: H03 owns 100-112 (re-firing under locked standard), H05 owns 77-82 (+redo spot76), OPEN 83-99, h01 67-71 done. TWO board facts to act on before any NEW fire: (a) Wan26 STOCHASTICALLY stamps text on ~1/5 clips (not from verbatim quotes) - some of my 15 reels may have stamped text -> needs Max visual review + re-render of any stamped; add no-text terms to negative_prompt as insurance. (b) fire_job was broken fleet-wide by ALTER commit 9acc2ee, fixed FAIL-OPEN in 7721c55 - git PULL before firing.
- NEXT: HOLD for Max review + go. Before firing more: git pull (get 7721c55); add no-text negative terms (text,captions,subtitles,letters,words,watermark) via lipsync_params; author semantic assignments by MEANING from catalog_v02; fire via fire_lesson1_semantic_v11_h01.py. Standard fork no longer needs Max ruling (team converged). Keep lighting/prompt locked; table_low banned.

## [2026-07-29 22:10] H42B ????????
- DID: Lesson2: fetched 3 approved Notion pages verbatim (22453 chars), built lesson_source_fetch_v01 + lesson_libretto_split_v01 (machine-verified verbatim split) + generalized recipe sass_recipe_anna_lesson_v02 (--lesson N) + build_lesson_audio_run_v02 + make_lesson_preview_v02. Split at 165 chars = 166 spots, worst-case 14.1s under the 15s reel ceiling.
- STATE: Anna voice synth running detached pid 50884, log _lesson2_v01b_synth_log.txt. First 200-char attempt aborted+archived (8 spots would exceed ceiling: real cps varies 12.3-20.4, not 17).
- NEXT: On synth completion: build_lesson_audio_run_v02 --lesson 2 (MOMA per-line audio identity), make_lesson_preview_v02 --lesson 2, present chromelink to Max. Do NOT fire reels - fleet HALT on lesson reels (duplicates), H01 owns rendering.

## [2026-07-29 22:44] H42B bd549dbe
- DID: Lesson1 FINAL music score in progress. Full 16-min assembly = G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene305_20260729_224203.mp4 (966s, sidecar .segments.json has trimmed reel boundaries). Building CLEAN final (NO burned numbers) via mule agent a57c2a0974ddb6d9d, script music_numbered_vid_v02.py adapted: 2-reel music pieces, acrossfade at reel boundaries, music under voice @50%, select2 as source, piece->source map txt kept for refinement.
- STATE: Mule agent rendering lesson1_FINAL_musicscore_50pct_v03_<ts>.mp4 into C:\...\lesson1_production\music_mix\out\. 16-min 1.4GB re-encode, takes minutes. Prior good QC builds still in out\ (v01 spots1-10, v02 full-34-reel-numbered). Do NOT delete music_mix contents.
- NEXT: When agent completes: present v03 to Max via localhost:47600 opener link. If a music piece is bad he refers to the piece->source map (v03 txt) to say which to dump/replace, then rebuild swapping that source.

## [2026-07-30 09:41] H42B bd549dbe
- DID: Lesson1 music. DEVIATION found: I re-encoded the whole 16-min avatar video (libx264) to bake music+numbers (v03 clean, v04 numbered). Max PROHIBITS video re-render - only the SOUNDTRACK may be re-rendered. Sanctioned system = MOMA music_projects: music_project_import.py -> music_editor.html at localhost:8790/music?project=slug (slideshow_server_v01.py port 8790) -> export via ffmpeg -c:v copy + amix (video stream copied, audio-only AAC). Placement stored in {SOUND_DATA_DIR}/music_projects/<slug>/project.json (offset + volume-curve points). Browser previews music live (Web Audio); numbers would be a PLAYER overlay, never baked.
- STATE: Corrected approach: mux the music-mixed soundtrack onto the ORIGINAL video with -c:v copy (no video re-render). Note: output ~=1.4GB (source bitrate) since video untouched; shrinking requires re-encode = prohibited. My music-bed audio (voice+music@50%, crossfaded at reel boundaries) is inside v03. NUMBERS cannot be baked (needs re-render); must come from the music_editor player.
- NEXT: 1) Produce sanctioned clean export v05: ffmpeg -i ORIGINAL(mixboard_assembly_scene305_20260729_224203.mp4) -i v03(for its mixed audio) -map 0:v -map 1:a -c:v copy -c:a aac. 2) For numbers: use music_editor.html player (localhost:8790/music) instead of burning in - may need extending the single-track system to multi-piece+numbers. 3) Confirm with Max whether he wants the export or to place music himself in the music_editor UI.

## [2026-07-30 12:09] H42B bd549dbe
- DID: Lesson1 music: v05 LOSSLESS clean (1.46GB, -c:v copy, no numbers) + v06 numbered compressed (125MB, 720p CRF26) delivered from assembly mixboard_assembly_scene305_20260729_224203.mp4. Max APPROVED the approach. Sanctioned rule: NEVER re-render the video for the lossless one (mux -c:v copy + music-mix audio); compressed+numbered may re-encode. Music method: 2-reel pieces from select2, loudnorm -16, acrossfade at reel boundaries (from the assembly's .segments.json), music under voice @50%, seed 42. Script: music_numbered_vid_v02.py; mule agent a57c2a0974ddb6d9d has full context.
- STATE: Max is assembling a NEW version of the lesson now (newer mixboard_assembly_scene305_*.mp4 will appear in G:\My Drive\00Main2026\00_rehearsals\ with a fresh .segments.json). He wants the SAME two outputs on the new assembly. Watcher armed for the new file.
- NEXT: When new assembly appears+stable: (1) rebuild music soundtrack on its NEW segments.json (2-reel pieces, crossfade at reel boundaries, @50%, seed42, select2); (2) v05-style LOSSLESS clean = mux new video -c:v copy + new mixed audio, no numbers; (3) v06-style numbered compressed = burn numbers then 720p CRF26; (4) present both localhost:47600 links. Output to lesson1_production\music_mix\out\, don't delete existing.

## [2026-07-30 12:31] H42B bd549dbe
- DID: Lesson1 music DESYNC root cause CONFIRMED + documented: approved rule = NEVER re-encode the video; overlay music with -c:v copy (video stream-copied) + re-encode AUDIO only (render_mixboard_video_v01.py v11 GLUE mode L71-78/792-799; slideshow_server_v01.py L341 music overlay uses adelay/atrim/asetpts). Re-encoding video (to BAKE numbers) causes A/V drift growing over minutes - Max saw it at ~7min in v07i/v08.
- STATE: Therefore: v07 LOSSLESS clean (lesson1_LOSSLESS_clean_v07_20260730_121926.mp4, video copied) is CORRECT + in-sync = the keeper. v07i (numbered fullres) + v08 (numbered compressed) are BROKEN by drift because they re-encode video to bake numbers. Numbered-baked video is impossible without drift. Numbers must come from a PLAYER overlay (music_editor) or a soft SUBTITLE track muxed with -c:v copy, never burned in.
- NEXT: Await Max choice: (a) deliver v07 + piece->source MAP (has per-piece timecode+source) so he picks bad music by timecode, no numbers needed; or (b) show numbers via music_editor player / soft-subtitle (-c:v copy, no re-encode). Do NOT produce more baked-number re-encodes. tempshare still pending Max's pick of which file.

## [2026-07-30 14:44] H42B bd549dbe
- DID: Lesson1 music DONE via new musicunder skill. Built from newest assembly mixboard_assembly_scene305_20260730_142710.mp4 (970.78s): BIG lesson1_LOSSLESS_clean_v10_20260730_143212.mp4 (1.4GB, video STREAM-COPIED - deep verify 29053 frames + same codec/fps as original) + SMALL lesson1_preview720_v10_20260730_143212.mp4 (121MB, CFR re-encode) + piece->source map v10. Deleted old big v05/v07/v09 per Max. Emailed Max both locations. Created skill musicunder (Claude: ~/.claude/skills/musicunder/SKILL.md; Codex: Nextcloud/claude_md_synced/codex_skills/musicunder/SKILL.md) + memory feedback_music_overlay_no_reencode.md + MEMORY.md pointer.
- STATE: All outputs in ...lesson1_production/music_mix/out/. One big file only. Rule now enforced by skill: NEVER re-encode video for music overlay (stream-copy video, one-pass audio mix from ORIGINAL; never chain audio from a re-encoded intermediate - that was the v07 desync cause). NOTE/quirk: loudnorm makes output audio 96kHz (orig 44.1kHz); timing verified fine but could add aresample=48000 to the chain for cleanliness.
- NEXT: Await Max's verdict on v10 music. If a stretch is bad he names the timecode -> swap that source track (map has per-piece timecodes) and rebuild. Uncommitted in moma: music_underlay.py, music_numbered_vid*.py (my scripts) - consider committing the sanctioned one only.

## [2026-07-31 11:22] H42B bd549dbe
- DID: Lesson1 credits slide text FINALIZED with Max (Art/Narration/Production/Voice/Video/Music column form; MOMA+FFmpeg lines REMOVED per Max). Verified music junctions on v10: all 56 music changes land on real 2-reel boundaries with 0.00s error (crossfade overlap IS compensated) - Max satisfied, music assignment APPROVED, do NOT re-randomize or rebuild the body.
- STATE: NEXT TASK PREPARED: Max will supply a TITLE slide and a CLOSING slide. Requirement: keep the approved v10 soundtrack EXACTLY (no re-evaluation), only EXTEND the music over the two new slides. Captured params slides must match for concat stream-copy: video h264 High, 1280x720, yuv420p, level 3.1, r_frame_rate 30/1, time_base 1/15360; audio aac 96000Hz stereo. Opening music track = map piece 1 '11 v9 Nice, slow, relaxed. 85% carrots.mp3' (src_offset 3.53s). Closing music track = piece 56 '11 v6 ... xylophone ... Spinach.mp3' (src_offset 62.11s, len 23.36s, ends 970.78s) -> continue that SAME track from src_offset 85.47s onward for the closing slide so it flows seamlessly, fade out at end.
- NEXT: When slides arrive: encode each slide video to the params above (silent), build title music (piece-1 track) + closing music (continuation of piece-56 track), extract v10 audio by COPY, assemble continuous audio = title_music + untouched v10 audio + closing_music, concat video title+v10+closing with stream copy, mux. NEVER re-encode the lesson body. Canonical body = lesson1_LOSSLESS_clean_v10_20260730_143212.mp4.

## [2026-07-31 13:36] H42B bd549dbe
- DID: Lesson1 slides+music: cut 10 closing-music candidates (last 7s of each select2 song, loudness-matched) to ...music_mix/closing_candidates/ (ALL_closing_candidates_7s.mp3 + closing_01..10.mp3 + closing_candidates_map.txt). Opened select2 folder for Max to pick the title-slide song/start point.
- STATE: SLIDES RECEIVED (paths): CLOSING = C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\titles\telepathy_title_experiments_v01\round3\rendered\telepathy_ending_grand_exhibition_anna_v02.png (Max: give it 7 SECONDS). TITLE = ...\round4\rendered\telepathy_intro_open_palms_lesson1_v03.png (CURRENT, but Max says a NEWER version is coming - wait for it / re-check before building). Body soundtrack v10 is APPROVED and must stay byte-identical.
- NEXT: WAITING ON MAX: (1) which closing candidate number, (2) title song + start point. THEN build: slide videos matched to h264 High/1280x720/yuv420p/level3.1/30fps/tb 1/15360 + aac 96000 stereo; title music + closing music; concat title+v10+closing with STREAM COPY (never re-encode the lesson body). Canonical body = lesson1_LOSSLESS_clean_v10_20260730_143212.mp4.

## [2026-07-31 14:14] H42B bd549dbe
- DID: Built Lesson 1 COMPLETE film v13 = title slide (7s) + approved v10 body (stream-copied, never re-encoded) + closing slide (7s). Trumpets song bookends: beginning under title, ending across tail+closing landing on its true final note (2.95s trailing silence cut). Levels 100% on slides, 50% under voice. Caught and fixed a real bug: v12's title slide was encoded 1920x1080 vs the 1280x720 body, so the join advertised the wrong resolution - v13 re-encodes ONLY the title slide and re-joins by stream copy. Frame proof 29053+210+210=29473 exact. Deleted defective v12 pair + 4.5GB of Nextcloud-resident intermediates.
- STATE: v13 master 1.38GB + 115MB preview + notes in Nextcloud music_mix/out. Nextcloud desktop client is uploading them to cloud.lakarian-city.ynh.fr now; background poller bf123jnh7 watching. Share tool = C:/claude_base/tools/tamza_songs/pipeline/scripts/upload_nextcloud_folder.py (OCS shares API); my thin wrapper at scratchpad/nc_share.py does status+share by remote path.
- NEXT: When both files are on the server: create public share links, verify each link actually loads (HTTP), then email Max the working link via mxmail_v01.py. Then update the musicunder skill: (a) working/pieces folder must live OUTSIDE Nextcloud, (b) slide encodes must match the body RESOLUTION too, not just codec/fps.

## [2026-07-31 14:38] H42B bd549dbe
- DID: Published Lesson 1 v13 complete film to Nextcloud and emailed Max two verified share links: streaming copy 115MB https://cloud.lakarian-city.ynh.fr/s/jZQHRetWCW5dTcJ and full-quality master 1.4GB https://cloud.lakarian-city.ynh.fr/s/LzRoJyo3NQrgYog . Both tested: page 200, video/mp4, range GET 206 so browser seeking works; master byte count matches local exactly (1447077264).
- STATE: v13 is the canonical complete film: title slide 7s + approved v10 body (stream-copied) + closing slide 7s, 984.65s, 29473 frames. Trumpets song bookends it, ending on its true final note. Music 100% on slides, 50% under voice. musicunder skill updated (Claude + Codex copies identical) with the resolution-mismatch trap and the keep-pieces-outside-Nextcloud rule. Nothing in the C:/moma repo changed this turn.
- NEXT: Awaiting Max's verdict on v13. If approved, update the memory file feedback_music_overlay_no_reencode.md CANONICAL RESULT block from v10 to v13 and write a short v13 report beside LESSON1_MUSIC_REPORT_v10_tomemex.md.

## [2026-07-31 17:02] H42B bd549dbe
- DID: Lesson 1 v14 delivered. Fixed BOTH v13 faults. (1) Last-spot desync root cause: v13 SPLICED the voice - kept v10's mixed audio to 948.22s then switched to voice re-extracted from the original. v14 splices nothing: voice is one unbroken stream from the original assembly delayed exactly 8.000s, video is the original's stream copied. (2) Intro music stopped at the slide and hard-cut; now trumpets run over the title slide + reels 1-4 and crossfade 1.2s into the approved bed at the reel-4/5 boundary (29.90s). Title slide 7.0->8.0s. Bed pieces 3..55 reproduced by PARSING the v10 map file so the approved music is bit-identical. Also fixed a mux trap: trailing loudnorm's lookahead truncated 1.8s of tail and amix ended when the voice ended - fix is to apad+atrim BOTH streams to the exact film length and drop the trailing loudnorm.
- STATE: CANONICAL = lesson1_COMPLETE_v14_20260731_161008.mp4 (985.653s, 29503 frames = 240+29053+210 exact, 1.38GB) + 115MB preview + notes, all in Nextcloud music_mix/out and uploaded. Verified share links emailed: listen https://cloud.lakarian-city.ynh.fr/s/Q3DMiqKKSs7BCEq master https://cloud.lakarian-city.ynh.fr/s/xwti6NRKPWd3z2G . v13 and two failed v14 attempts deleted. Build scripts in session scratchpad: build_v14.py + remux_v14.py, working folder outside Nextcloud.
- NEXT: Await Max's verdict on v14. If approved: update memory feedback_music_overlay_no_reencode.md CANONICAL RESULT from v10 to v14, and add to the musicunder skill the two new hard-won rules - NEVER splice the voice (rebuild the whole audio from the unbroken original + a rebuilt bed), and pad both streams to the exact length with no trailing loudnorm so the music reaches the last frame.

## [2026-07-31 19:08] H42B bd549dbe
- DID: Lesson 1 v15 built and delivered to Max's spec: title slide 3.5s + body 970.653s (video STREAM-COPIED) + closing 7.0s = 981.153s, 29368 frames (105+29053+210 exact). Trumpets bookend: opens on the track's FIRST NOTE (detected 0.75s into the file, quiet lead-in trimmed, NO fade-in) and ends on its LAST NOTE (2.95s trailing silence cut). Ramp 100->50 percent is 1.0s STRADDLING the cut (0.5s before Anna, 0.5s after). Middle bed = approved v10 pieces 3..55, order and offsets unchanged, parsed from the v10 map file. Voice one unbroken stream, never spliced. Levels: title -14.5, Anna -16.8, closing slide -12.9 dB.
- STATE: CANONICAL = lesson1_COMPLETE_v15_20260731_184635.mp4 + preview + notes in Nextcloud music_mix/out, uploaded, links verified and emailed. listen https://cloud.lakarian-city.ynh.fr/s/ZoFSMZ6p8zriz5Y master https://cloud.lakarian-city.ynh.fr/s/7NKmbwXoEqFiK5M . v13 and v14 deleted. Build script scratchpad/build_v15.py, working folder outside Nextcloud. Android Vocalizer returned HTTP 429 three times (sender status OK) so the channel is rate-limited; used email plus the desk attention alarm. A parallel sibling build sits at C:/moma/tmp/lesson1_complete_v15 - NOT mine, unverified.
- NEXT: Await Max's verdict. If approved: fold the slide+bookend recipe into the musicunder skill as parameters (slide seconds, first-note trim, last-note trim, straddling ramp) so it is one command next time, and update memory feedback_music_overlay_no_reencode.md CANONICAL RESULT to v15. Also investigate the Android Vocalizer 429.

## [2026-07-31 19:39] H42B bd549dbe
- DID: Recorded Max's absolute rule: RE-RENDERING VIDEO IS PROHIBITED, always. His words: production is lossless all-intra, we keep the SAME FRAMES forever and only insert keyframes, video never re-renders ever. Written to project memory as hardrule_never_rerender_video.md, indexed in MEMORY.md as HARD RULE #0d, and put at the top of the musicunder skill (Claude + Codex copies identical). Explicitly covers the mistake I made: producing an extra small compressed preview copy beside every master from v10 to v15 without ever asking - that counts as re-rendering and is banned unless Max asks.
- STATE: Lesson 1 v15 delivered and links verified. Master lesson1_COMPLETE_v15_20260731_184635.mp4 (981.153s, 29368 frames, stream-copied picture) https://cloud.lakarian-city.ynh.fr/s/7NKmbwXoEqFiK5M . Desk attention alarm confirmed working by Max after one crashed run - intermittent access violation in attention.py after it logs, worth a separate fix. Android Vocalizer still HTTP 429, channel rate-limited by a parallel Codex session.
- NEXT: From now on deliver the MASTER ONLY, no preview copy, unless Max asks. If v15 is approved, fold the slide+bookend recipe into musicunder as parameters (slide seconds, first-note trim, last-note trim, straddling ramp).

## [2026-07-31 19:58] H42B a87abd56
- DID: Lesson 1 v16 DELIVERED. Found and MEASURED the v15 bug: an in-line adelay=3500 in the mix filter chain SILENTLY DID NOTHING - the title slide rendered correctly but Anna's voice ran from frame one and the whole film sat 3.5s early (cross-correlation vs the original: r=0.71 at zero lag). FIX: build the delayed voice as a REAL FILE (3.5s silence wav concatenated with the original's extracted audio) and VERIFY it by cross-correlation BEFORE mixing; the build now hard-aborts unless r@0.0s<0.2 and r@3.5s>0.5. Measured 0.000 and 0.997. Also wrote the spec down as a contract: C:/moma/memos/lesson1_slides_agreement_v01_tomemex.md.
- STATE: CANONICAL = lesson1_COMPLETE_v16_20260731_195115.mp4 (981.153s, 29368 frames = 105+29053+210 exact, 1280x720, 1.38GB), uploaded to Nextcloud, link verified and emailed: https://cloud.lakarian-city.ynh.fr/s/egAasT3EKfbegwi . Full verification passed 9/9: no voice under the title slide (r=0.053), voice at 3.5s (r=0.880), sync holds at body 200/500/900/960s. NO preview copy made - Max's rule that re-rendering is prohibited. My broken v15 deleted. Build+verify scripts in scratchpad: build_v16.py, verify_v16.py. NOTE Codex is building competing files in the same folder (v116 x2, v117) - not mine, unverified.
- NEXT: Await Max's verdict on v16. If approved: fold the slide+bookend recipe into the musicunder skill as parameters, and resolve the two-sessions-racing problem - Codex has v15/v116/v117 in the same out folder.

## [2026-08-01 00:15] H42B a87abd56
- DID: Lesson 1 slides+music finished as v19 (C:\moma\tmp\v19). Trumpet bookends verified by correlation (open 0.71, close 0.67), voice offset flat +4.9ms across the film.
- STATE: Two real bugs found: asetpts=N/SR/TB re-timed the voice lane (Codex diagnosed the AAC priming excess first); acrossfade chain left the tail 1.2s short so the closing music was the wrong track. Both written into the musicunder skill + synced to codex_skills.
- NEXT: Max may publish v19. C: drive hit ZERO free during the build - Codex still holds ~35GB of intermediates in C:\moma\tmp.
