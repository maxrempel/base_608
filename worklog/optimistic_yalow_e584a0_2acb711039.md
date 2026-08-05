
## [2026-06-10 07:03] b7 793da793
- DID: Built+shipped Android player fix in app.js: (1) CSS @media bottom-sheet so player is on-screen on phones, (2) per-song shareable address #song=vid_start that tracks the playing song, phone-Back closes player, cold deep-link auto-starts. Radio kept continuous (chose A, not single-song pages). QC 390x844 all 5 checks pass, 0 errors. Deployed+verified 37521 bytes, backup live_backup_20260610T140251Z.
- STATE: Live in ~5min. b7 solo, team halted; Max on break, authorized shipping.
- NEXT: Await Max phone test. Open: validate timing accuracy across Sol 100-song videos (+7s is 1-song band-aid). If pasting #song while already on page should work, add a hashchange listener (currently only fresh-load deep-links work, matching pre-existing #p/#a behavior).

## [2026-06-10 09:25] b7 793da793
- DID: Shipped Android player fix live (full-width bottom-sheet + per-song shareable #song= address + Back-closes; QC 5/5 at 390x844, 0 errors; backup live_backup_20260610T140251Z). Max actively sharing playlists with performers = current priority, and it's live/unaffected. Investigated Sol: pings but SSH port 22 closed/filtered from Pine .114 - cannot log in; Sol holds the harvested transcripts.
- STATE: DECISION: timing parked until Sol SSH is back (chose B: don't re-harvest on Pine, don't risk main YouTube IP). FULL HALT still in effect; b7 solo, staying quiet, NOT arming self-wake. DeepSeek key not on Pine (was on Sol).
- NEXT: When Max says Sol is up: SSH maxre@192.168.1.113 (key ~/.ssh/sol_key), verify worker (pgrep -cf 'venv/bin/python timing_pipeline'), check _work/song_timing.json count + harvest.log, resume phase-2 mapping. If IP moved off .113, find Sol's real IP. Also still open: validate ending accuracy across 100-song videos (+7s is a 1-song band-aid).

## [2026-06-10 12:49] b7 793da793
- DID: Sol back up; timing worker healthy (62/509 done, 4926 timings, $2.22, 0 err). Resuming integration.
- STATE: Sol pid 2808 running, polite-paced ~20 vids/hr. Pulling current song_timing.json to Pine to fold into data.json and deploy.
- NEXT: Pull Sol song_timing.json -> merge Pine durable store -> rebuild data.json (enrich folds seg_start/end) -> deploy to R2. Then let Sol finish rest, final integration at 509.

## [2026-06-10 12:52] b7 793da793
- DID: Integrated Sol's 62-video harvest into live catalog: merged store to 4971 entries, enriched data.json, DEPLOYED to R2 (verified). LIVE now has 4979 timed rows (was 45).
- STATE: data.json live + byte-verified, backup live_backup_20260610T195138Z. app.js unchanged (37521b). Sol worker pid 2808 still harvesting remaining ~437 videos, polite-paced.
- NEXT: When Sol finishes all 509 (or on Max's ping): re-pull song_timing.json, re-merge, re-enrich, re-deploy for the final timing set. No self-wake (FULL HALT).

## [2026-06-10 13:48] b7 793da793
- DID: NEW TASK ttt: paused Sol song worker (harvest.done flag set, cron won't relaunch), launched Telepathy Tapes transcript harvest on Sol (98 videos, pid 6947, en-orig only, no translate). Created Notion 'ttt' page under Lunar Paper (id 37b0316f-5560-814f-b500-eb3c1f9baca5).
- STATE: Harvest running on Sol ~/ttt/ via song venv youtube-transcript-api, polite 10-35s gaps, block-aware. Background waiter bk89epghg notifies on done flag. ETA ~40min.
- NEXT: On done: pull 98 transcripts to Pine, create child pages under ttt parent (batches of ~12). Then resume songs: rm ~/song_timing/harvest.done + run guard.sh.

## [2026-06-10 14:30] b7 793da793
- DID: ttt harvest DONE on Sol: 98/98 transcripts ok, pulled to Pine C:/claude_base/tools/ttt_transcripts (3.1MB). Wrote ttt_to_notion.py (API uploader, idempotent). Notion ttt page = 37b0316f-5560-814f-b500-eb3c1f9baca5.
- STATE: BLOCKED: internal token 'Sol Sync 20260319' 404s on Lunar Paper subtree - not connected. Need Max to add the Sol Sync connection to Lunar Paper page, then run uploader.
- NEXT: Max connects integration -> run python ttt_to_notion.py (creates 98 child pages, oldest-first) -> verify -> resume Sol songs (rm harvest.done + guard.sh).

## [2026-06-10 15:45] b7 793da793
- DID: ttt COMPLETE: uploaded all 98 transcripts to Notion as child pages under ttt (Sol Sync integration connected by Max, created=98 skipped=0, oldest-first, bookmark+text). Resumed Sol song worker.
- STATE: ttt task fully done. Song timing worker relaunched (harvest.done removed, guard.sh ran). Songs continue ~62/509 -> 509.
- NEXT: Songs harvest to completion; final catalog timing deploy when 509 done (route through b0 gate).

## [2026-06-11 13:51] b7 793da793
- DID: ttt harvest DONE (98/98 in Notion). Song timing harvest DONE (452/509, 21481 timings, 57 captions-disabled). Proposed manual-corrections overlay file + Deepgram route for the 57 owned videos.
- STATE: Live catalog still carries only 4979 timings; final 21481 deploy held (b0 gate + Max go). Manual-corrections file design proposed, awaiting Max's specific bad-song list. 57 gap-fill via Deepgram proposed, awaiting go.
- NEXT: On Max go: (1) Deepgram the 57 owned vids for timestamps; (2) build manual_overrides.json applied AFTER enrich; (3) fold all timings into data.json, deploy via b0 gate.
- LESSON: Channel owner can transcribe captions-disabled vids locally via Deepgram (no YT login, no translate) instead of treating them as unharvestable.

## [2026-06-11 14:17] b7 793da793
- DID: 21569-end data.json LIVE. Sol prepped (yt-dlp+deepgram-sdk, keys staged, 57 missing vids derived=2643 songs). Gave b6 Android app.js gate PASS. Explained gate/Deepgram/Whisper to Max in plain English.
- STATE: BLOCKING on Max 'go' to pick transcriber for the 57: recommended Groq Whisper ~$6 (vs Deepgram $40, OpenAI Whisper $54). Windowing does NOT cut cost (concert songs back-to-back). Max owns channel but a different account uploaded the 57 with captions off -> still must transcribe audio ourselves. Corrections-DB awaiting Max's wrong-song list. FULL HALT: no self-wake timer.
- NEXT: On 'go': kickoff1 register Groq (mass@tamza), run detached on Sol with guard, map_core->store->re-enrich->deploy=509/509. Plus free start re-snap on 452 via first_line.

## [2026-06-11 15:55] b7 793da793
- DID: fill57 video 1/57 done on Sol: 44/44 songs got start+end, $0.0144. Starts nudge median 10s (good), but 2/44 collided onto next song's start (catalog 60->244, 796->1072).
- STATE: fill57_groq.py running PID 15877 on video 2/57, guard armed. Chose option (a): let all 57 finish, then one collision-fix pass + redeploy through b0 gate. Live catalog still carries the 21,481 already-deployed timings.
- NEXT: Build collision-guard post-pass (reject seg_start that lands at/after next song start) to run on full store before enrich; applies to ALL videos not just 57. Get Max's manual wrong-songs list for overrides. Hold FULL HALT, no timer.
- LESSON: map_core occasionally snaps a song's start onto the NEXT song's start when the opening lyric isn't found in the transcript window; needs a monotonic-start guard.

## [2026-06-11 16:17] b7 793da793
- DID: Built+committed+pushed start-guard: 910 robot starts (4.2%) that slid onto next song repaired via durable auto_start_overrides.json (revert to curated marker, null bad end). Candidate data.json verified 26283 rows preserved, 910 applied 0 unmatched. Gate request posted to b0/safety.
- STATE: AUTONOMOUS mode (Max away hours, 240s rearm). Candidate output/data_startfixed.json READY. fill57 running under B8 (separate writer). B8 must apply auto_start_overrides.json in its post-57 deploy or my fix regresses.
- NEXT: On next wake: check board for gate PASS/objection; if PASS or no objection, copy data_startfixed.json->data.json and deploy --data (backs up live, byte-verifies, reversible). Then propose continuous auto-publish loop. Hold separate-writer discipline - never write Sol store.
- LESSON: Durable corrections belong in the apply_overrides override mechanism, not a one-off store delta - they survive every re-import = the continuous-improvement spec.

## [2026-06-11 16:51] b7 793da793
- DID: DEPLOYED start-guard to LIVE (910 starts reverted to curated marker, data.json 26283 rows byte-verified, backup live_backup_20260611T235051Z). Max authorized override of retired b0 gate.
- STATE: AUTONOMOUS. Start-fix LIVE+durable. fill57 running under B8. data.json deploy artifact NOT git-tracked (18MB); durable source auto_start_overrides.json IS committed+pushed.
- NEXT: Wire continuous auto-publish loop (periodic enrich->overrides->deploy as store grows). Ensure B8 post-57 deploy applies auto_start_overrides.json. Re-arm 240s.

## [2026-06-12 07:17] b7 793da793
- DID: Shipped 936 start-fixes live + built continuous publisher (hidden Pine task kartoteka_publish every 3h: pull Sol store, rebuild, guard starts all videos, gate, deploy-if-changed). Committed+pushed. Idempotent+self-logging.
- STATE: DONE: engine autonomous via cron. Start-fixes LIVE on tamza.com (26283 rows). publish_catalog.py no-op-guards identical bytes. B8 owns bot-blocked 57 downloads.
- NEXT: Watch publisher health (pipeline/logs/publish.log) + B8 bot-block resolving; 57 auto-ship on next 3h tick when store grows.

## [2026-06-12 09:21] b7 793da793
- DID: Autonomous watch ticks: confirmed to safety-watcher that b7 publisher is read-only on Sol store (scp-pull only, never writes). Periodic checks of store growth.
- STATE: All b7 deliverables DONE+LIVE+autonomous (kartoteka_publish task every 3h). B8 fill57 still stalled 10/57 on YouTube bot-block (B8 lane). Store unchanged.
- NEXT: Keep light watch; first new auto-deploy happens when B8 store grows + next 3h tick. Nothing for b7 to do until then.

## [2026-06-12 15:02] b7 793da793
- DID: b7 deliverables fully shipped+autonomous: 936 start-collision fixes LIVE on tamza.com; continuous publisher = Pine scheduled task kartoteka_publish (every 3h, hidden pythonw, self-logging, no-op-guarded, READ-ONLY on Sol store) auto-ships catalog when Sol timing store grows. All committed+pushed (publish_catalog.py, guard_starts.py, infra_map). 09:15 + 12:15 auto-runs verified healthy.
- STATE: DONE. In autonomous watch only. Separate sibling project (B9/b10/D8) doing full Tamza/Hucolo video backup to Centauri teal16 - NOT b7 lane. D8 owns the 57 song-timing pulls on Sol (still ~10/57, YT bot-blocked); when they land, my cron auto-ships them, no b7 action needed.
- NEXT: Keep light 30-min watch for publisher failures; nothing actionable until store grows. Loop can safely end if Max returns.

## [2026-06-12 15:33] b7 793da793
- DID: b7 DONE+autonomous. Live: 26283 rows, ~100% starts, 21109 ends (~80%). 936 start-fixes shipped. Publisher = Pine task kartoteka_publish (every 3h, hidden, no-op-guarded, read-only on Sol store) auto-ships when store grows. Auto-runs 09:15/12:15/15:15 healthy.
- STATE: Watch-only. Ends lag at 80% because end-detection is UPSTREAM (Sol pipeline / D8), not a b7-fixable gap; missing ends fall back to honest 120s cap. D8 at 17/57 downloads (bot-wall; trying Odysee). Sibling full-channel backup (B9/b10) = separate project, not b7.
- NEXT: Nothing actionable until Sol store grows -> cron auto-ships. Light 30-min watch for publisher failures.

## [2026-06-12 17:06] b7 793da793
- DID: b7 COMPLETE+autonomous (pre-compaction snapshot). Live tamza.com catalog: 26283 rows; starts ~85% transcript-detected (70% genuinely moved off human marker), ends ~80% (21109); 936 robot start-collisions snapped back to trusted markers. Continuous publisher = Pine scheduled task 'kartoteka_publish' (every 3h, hidden pythonw, self-logging pipeline/logs/publish.log, no-op-guarded, READ-ONLY scp-pull on Sol store). Auto-runs 09/12/15:15 all healthy. Committed+pushed: publish_catalog.py, guard_starts.py, infra_map.
- STATE: WATCH-ONLY autonomous mode (Max away). Nothing actionable for b7. End-coverage gap is UPSTREAM (Sol end-detection / D8), not b7-fixable. D8 (former b8) at ~20/57 downloads, YT bot-walled. Separate sibling project B9/b10 = full-channel video backup to Centauri, NOT b7 lane.
- NEXT: When Sol store grows, cron auto-ships -> no b7 action. Keep 30-min watch for publisher failure (gate-abort/deploy-fail in publish.log).

## [2026-06-12 19:58] b7 793da793
- DID: Continuous engine PROVEN self-improving: 18:15 auto-run DEPLOYED +801 new timed ends (21109->21910 live, ~83%) as D8 downloads grew the Sol store (29/57). No human push. b7 publisher = Pine task kartoteka_publish every 3h (hidden, no-op-guarded, read-only scp-pull on Sol store).
- STATE: Autonomous HOURLY watch (Max: 'you are working on continuing starts, rearm every hour'). Each 3h cron tick auto-ships new timing as D8's 57 downloads land. Starts ~85% transcript-detected/70% moved; 936 collisions guarded. Committed+pushed: publish_catalog.py, guard_starts.py, infra_map.
- NEXT: Keep hourly watch: confirm cron runs healthy (pipeline/logs/publish.log) + ends % climbs as D8 finishes 57. Nothing manual needed.

## [2026-06-13 08:32] b7 793da793
- DID: Autonomous hourly watch of starts job; checked D8 downloads (29/57, stalled on YT bot-wall) and cron health (last run 21:15 ok, next 09:15).
- STATE: Engine healthy+idle. Live=21910 ends. Publisher auto-ships when Sol store grows. D8 stalled their lane. Overnight cron slots skipped (Pine asleep) - harmless, store unchanged.
- NEXT: Next hourly wake ~08:32: recheck segs57 count + latest publish.log run; if store grew, confirm cron auto-shipped; else re-arm 3600s.

## [2026-06-13 13:50] b7 793da793
- DID: Investigated Max's '60% wrong starts' report. Read real transcripts vs detected starts (2 random samples, 34 songs total): detected seg_start is ~75-85% correct, NOT 40%. Found the real bug: the 'YouTube' link in the kartoteka player ignored seg_start and opened play_url's old human t= marker (early/announcement). Radio already used seg_start. Fixed YouTube link to seek seg_start (fallback to t= only when no seg_start). Deployed app.js live + byte-verified, committed c1265e3e on master/origin.
- STATE: Live player: both YouTube link AND radio now seek corrected start. Residual wrong starts = ~28% of songs with NO transcript fix yet (null/unchanged seg_start) fall back to the early human marker; plus ends harder. data.json+app.js fully live.
- NEXT: Improve detection COVERAGE for the ~28% unfixed starts (depends on D8 finishing the 57 downloads + reprocessing). Continue hourly autonomous watch of the publish engine.
- LESSON: A coverage metric ('has a seg_start') is NOT an accuracy metric ('start is correct') and NOT a wiring check ('does the UI use it'). Always verify the live UI actually consumes the data end-to-end, and trust Max's real listening over a tiny script sample.

## [2026-06-13 14:01] b7 793da793
- DID: ROOT CAUSE FOUND for Max's '60% wrong starts/ends' (he listens on RADIO, mostly HIS OWN songs). The 452 main videos use YOUTUBE AUTO-CAPTIONS (youtube_transcript_api, {t,d,x}) which are garbled for sung Russian -> DeepSeek maps onto noise. The 57 caption-less videos use Groq Whisper-large-v3-turbo (better). Mapping model = map_core.py SYS+_build_prompt, currently model='deepseek-chat' (V3) on Sol ~/song_timing/map_core.py. PLAYER YouTube-link bug already fixed+deployed (c1265e3e) - SEPARATE issue, do NOT conflate with algorithm. DeepSeek API now offers deepseek-v4-flash and deepseek-v4-pro.
- STATE: MAX'S NEW TASK (in progress): (1) switch map_core MODEL to deepseek-v4 (use v4-pro). (2) Test on 40 songs. (3) For manual review, dump ~300 CHARS of transcript each side of detected start AND end. (4) Really analyze the ALGORITHM + PROMPT - it needs fine-tuning. (5) If needed: search online for full-text song lyrics (anchor) and/or RE-TRANSCRIBE audio with Whisper instead of YT auto-captions. Prompt weakness spotted: SYS assumes MC lines are prefixed '>>' and sung lines tagged [music]/[музыка] - YouTube auto-captions provide NEITHER, so the prompt's cues don't exist in the real input.
- NEXT: Build a Sol script: sample 40 songs (incl Max's performances: performer~Ремпель/Дежурн), pull transcript +/-300c around current seg_start & seg_end, re-map with deepseek-v4-pro, write old-vs-new-vs-transcript to a review file; THEN read it and judge + tune prompt. Continue hourly publish-engine watch separately.
- LESSON: YouTube auto-captions are the upstream quality ceiling for sung Russian; Whisper re-transcription is likely the real fix. Prompt references caption markers that the actual transcripts lack.

## [2026-06-13 14:22] b7 793da793
- DID: Committed prompt v2 design update (51784c2c): verse/prose split + quatrain & timestamp end-prediction per Max's 3 new principles. Pushed.
- STATE: Prompt v2 spec complete in prompt_ru_v2_design_tomemex.md. NOT yet wired into Sol map_core.py. Blocked on Max's go-ahead for the 40-song flash test (touches shared Sol worker per D8/B80 coordination + DeepSeek cost).
- NEXT: On Max's 'go': set MODEL=deepseek-v4-flash in Sol map_core.py, wire SYS+_build_prompt from the design file, run 40-song test (incl Max's own performances), dump +/-300c flanks, manually judge.

## [2026-06-13 14:57] b7 793da793
- DID: v2 flash test: validated deepseek-v4-flash is a REASONING model (needs max_tokens>=3000 or content comes back empty -> first run's all-None was a token-cap bug, NOT the algorithm). Raised cap to 3000 in map_test_v2_flash.py, re-running 40-song test on Sol. Adopted Max's chop-the-middle idea + verse/prose + quatrain + timestamp into design.
- STATE: Sol SSH timing out ~2min (siblings b8/b9 heavy YT pulls + possible Sol blip). Test re-run was killed when SSH dropped (not nohup'd). test_v2_report.json on Sol has the OLD all-None run.
- NEXT: When Sol back: re-run test DETACHED (nohup) so SSH drops don't kill it; read report; if his songs look good, apply to Max's songs + publish so he listens on radio. Then implement chop-the-middle head+tail windows.

## [2026-06-13 15:15] b7 793da793
- DID: Sol back up. Launched v2 flash mapping test DETACHED (nohup pid 7894) on Sol: /home/maxre/song_timing/map_test_v2_flash.py --n 40 --out test_v2_report.json, log /tmp/v2test.log. Relayed Max's 'migrate heavy work off Sol to Lak+Centauri' to team (aimed at download workers b8/b9).
- STATE: Test running on Sol (DeepSeek-only, light). max_tokens=3000 fix applied. Awaiting completion (~3-5min).
- NEXT: READ /tmp/v2test.log + test_v2_report.json on Sol (ssh -i ~/.ssh/sol_key maxre@192.168.1.113). Judge Max's own songs (is_max=true rows): compare model_start/model_end vs flank_start/flank_end transcript dumps. If good -> apply v2 mapping to ALL Max's songs + publish (publish_catalog.py) so he listens on radio. Then implement chop-the-middle head+tail windows. Migration to Lak/Cent = team task, not b7-critical.

## [2026-06-13 15:28] b7 793da793
- DID: Max's verdict: feeding FULL per-song transcript is doomed (slow). NEW LOOP TASK: chop the middle - feed only HEAD (around curated start, for START) + TAIL (around next-song start, for END), drop song middle. Sample n=10, READ results, ITERATE the v2 prompt until sampled results look good. Keep a 4-min self-wake timer (autonomous).
- STATE: About to: kill the slow 40-song run on Sol (pid ~7895), edit map_test_v2_flash.py to chop middle, run --n 10, read /home/maxre/song_timing/test_v2_report.json, judge each (model_start/end vs flank dumps), tweak SYS/_build_prompt, re-run.
- NEXT: LOOP: (1) ssh sol, (2) run map_test_v2_flash.py --n 10, (3) read report, (4) judge his songs, (5) edit prompt in BOTH map_test_v2_flash.py AND prompt_ru_v2_design_tomemex.md, (6) repeat until good, (7) then apply to all Max songs + publish. Sol now has watchdog auto-reboot (b11). fill57 worker MIGRATED to Lak (b8).

## [2026-06-13 15:28] b7 793da793
- DID: CORRECTION: Max overrode the chop idea -> FULL TEXT must must must, do NOT chop the middle. Feed the complete per-song transcript window. Slowness is acceptable; correctness needs full text. Also: stop being passive/lazy - READ and JUDGE results, iterate prompt aggressively.
- STATE: Killing slow 40-run; launching n=10 FULL-TEXT unbuffered (python -u) so progress is visible.
- NEXT: Run map_test_v2_flash.py --n 10 (FULL windows, NO chop), READ test_v2_report.json, JUDGE each song's model_start/end vs flank transcript dumps, edit prompt in map_test_v2_flash.py + prompt_ru_v2_design_tomemex.md, re-run, repeat until good. 4-min timer. Then apply to all Max songs + publish.

## [2026-06-13 15:33] b7 793da793
- DID: n=10 FULL-TEXT v2 flash test DONE: 72s total (~7s/song), ~0.03 USD. 8/10 confident start..end (conf 0.8-0.9): Утречко 7623..7748, Сентиментальный марш 1516..1642, Гречица 5430..5550, Не бродяги 308..422, Год созреванья 2063..2144, Звезда упала 1012..1127, Псалом137 5310..5540, Та кухня 1353..1473. 2 returned None: 'Вторник.Второе августа'(xJ5LMJCVmVI), 'Говорите я молчу'(peYcl6VZJao).
- STATE: Full text is FAST and viable - my slowness fear was wrong. Report saved Sol:/home/maxre/song_timing/test_v2_report.json with flank dumps. NOT yet judged for accuracy.
- NEXT: NEXT (do NOT read full report into a near-full context - fresh session): ssh sol, read test_v2_report.json, for each of the 8 hits compare model_start vs flank_start.before/after (is start right after last prose, music incl?) and model_end vs flank_end. Investigate the 2 None (likely empty content again? bump max_tokens or check reason). Tune SYS/_build_prompt in map_test_v2_flash.py + prompt_ru_v2_design_tomemex.md. Re-run --n 10. Loop until good. FULL TEXT must (Max). Then apply to all Max songs + publish.

## [2026-06-13 16:42] b7 793da793
- DID: BLOCKER: b11 found Sol has BAD RAM (non-ECC single-bit flip, kernel GPF under mem stress). b11 is running SEQUENTIAL stress tests ~30min from 15:58 -> Sol crashes+auto-reboots repeatedly = UNRELIABLE for new test runs until ~16:30. Needs Max at Sol console w/ memtest86+ to pull bad DIMM. Sol PRODUCTION already migrated to Lak (b8 fill57 + b9 bulk backup).
- STATE: n=10 v2 report IS saved at Sol:/home/maxre/song_timing/test_v2_report.json (8/10 good picks) but NOT yet judged + at risk if Sol crashes mid-read. map_test_v2_flash.py + transcripts + queue.json all on Sol.
- NEXT: WHEN SOL STABLE (after ~16:30 or b11 says done): scp test_v2_report.json off Sol first (preserve it), then judge the 8 hits vs flanks + fix 2 None, tune prompt, re-run --n 10. CONSIDER moving the whole timing test to Lak (more reliable) since Sol RAM is bad. FULL TEXT must. Then apply to Max songs + publish.

## [2026-06-13 18:04] b7 793da793
- DID: Validated v2 song-timing 10/10 on Max's songs (token-retry fix rescued 2 empty-content crashes). Upgraded map_core.py to v2 (flash+RU prose-boundary, committed b6160d5d). Built map_max_v2.py batch; launched full 756-Max-song run on PINE (not bad-RAM Sol), pid 4116, writing _work/song_timing.json, resumable. Pulled store+452 transcripts off Sol to Pine first.
- STATE: Batch running ~90min on Pine. Background watcher ba4zf1w07 waits for DONE. Code committed+pushed master b6160d5d.
- NEXT: When batch logs DONE: run enrich_catalog.py -> build -> deploy_catalog.py to publish Max's songs to tamza.com so he listens on radio. Check coverage (some Max vids lack cached transcripts -> keep 120s cap, safe).
- LESSON: deepseek-v4-flash is a reasoning model: low max_tokens gets eaten by reasoning_content leaving message.content empty; escalate budget 3000->9000->16000 on empty content.

## [2026-06-13 18:17] b7 793da793
- DID: V3(deepseek-chat) opt round1 on 12 recent Max songs: 12/12 ends perfect, ~8/12 starts perfect. Weakness: V3 skips instrumental intro (starts at first sung word) #3/#8, grabs count-in #12; #6 is a spoken greeting wrongly mapped to next song verse.
- STATE: Full-756 batch KILLED (was running V3). Optimizing prompt for V3 on recent Max songs. opt_v3.py is the harness; test_runs/opt_v3_roundN.txt is the judge file. map_core MODEL now=deepseek-chat. 14 flash rows + some V3 rows already in _work/song_timing.json.
- NEXT: Edit opt_v3.py prompt: procedural 2-step prose-boundary algo + force music-intro inclusion + null-guard for non-song greetings. Run round2, judge. When good, remap recent 10-40 Max songs into store, enrich+deploy so Max can listen. Max away hours, autonomous w/ timer.
- LESSON: deepseek-chat (V3) is 5x cheaper than v4-flash (no reasoning tokens): ~$0.0007/song vs $0.0038. Ends are easy; the hard part for non-reasoning V3 is including the captionless instrumental intro after prose ends.

## [2026-06-15 17:26] b7 793da793
- DID: Investigated Max's first-word-start bug. Confirmed: LIVE Max songs (806 rows, 720 timed) carry b6's v2 prose-boundary starts which CORRECTLY include the instrumental intro (e.g. 'Твой ангел' NastMtX6Mhg: host ends ~1399, live seg_start=1406 in the intro, first sung word 1409.8). The OLD mapper=None bulk (~22k non-Max rows) still cuts intro = first-word. Max put b7 in charge of starts; b6 to retire. Method owned = song_timing_max_v2.json (prose-boundary, Max wins) overlaid via build_data_overlays.py, deployed from Pine, NO Sol.
- STATE: Max's own recent songs fixed+live as of b6 deploy ~16:23. Verified live via R2 boto3. Sol DOWN (RAM, 2-stick only per b11). publish_catalog.py cron still PULLS from Sol AND does NOT run build_data_overlays.py -> when Sol returns a cron run would REVERT Max's overlay. That is the durable risk to fix.
- NEXT: 1) Tell Max his recent songs are fixed+live (he saw stale/cache). 2) Cut Sol scp-pull out of publish_catalog.py + bake build_data_overlays.py into the chain so cron can't revert overlay and Sol stays retired. 3) Read build_catalog.py first to avoid double-enrich. Autonomous mode armed.
- LESSON: Live Max-song starts ARE correct (intro-included) via b6 overlay; the regression is my V3 first-word values + the cron path lacking the overlay, NOT the live data Max tested.

## [2026-06-15 17:31] b7 793da793
- DID: Shipped the durable starts fix. Edited build_catalog.py to merge Max v2 prose-boundary overlay (song_timing_max_v2.json) over base store at enrich time (overlay wins) + removed scp-from-Sol pull from publish_catalog.py (Pine-local store, abort-loud if missing). Tested via dry-run then deployed live through canonical chain: 26283 rows, 21996 ends. Verified Max starts keep intro (Твой ангел=1406 not 1409; guard reverted only 22/806). Committed b6e7fc9a, on origin/master (B15C pushed chain). bcast sent: b6 stand down on starts.
- STATE: LIVE catalog now served by the Sol-free overlay-baked pipeline. A future scheduled kartoteka_publish run can NO LONGER revert Max's intro-included starts, and Sol stays retired. Autonomous timer armed (~4min).
- NEXT: Optional follow-ups: (1) note Sol migration in infra_map_tomemex.md (kartoteka_publish no longer needs Sol). (2) the ~22k non-Max old rows still have first-word starts -- separate bigger remap job, NOT Max's own songs. (3) confirm with Max his recent songs now test correct after hard-refresh.

## [2026-06-15 19:28] b7 793da793
- DID: Launched FULL-catalog remap per Max's order ('finish all songs, autonomous'). New script map_all_v2.py (no performer filter, writes BASE store _work/song_timing.json in place, skips already-v2/done rows, resumable state _work/map_all_v2_state.json, atomic per-song checkpoint, cap $30). Detached hidden PID 7764, log _work/map_all_v2.log. Confirmed mapping (NastMtX6Mhg:286 -> start 284, into intro). bcast posted: HANDS OFF base store.
- STATE: 21481 songs to remap (2643 lack cached transcript = b15 domain). REAL cost ~$0.004/song (NOT my $0.0008 estimate) => ALL = ~$84. $30 cap maps ~7700 newest-first then stops. Each kartoteka_publish (cron 3h) auto-picks up progress since build_catalog merges base store. Max overlay song_timing_max_v2.json still wins for Max's own songs.
- NEXT: 1) Tell Max real cost ~$84 for all; $30 cap = partial; he decides whether to raise cap. 2) Monitor PID 7764 via _work/map_all_v2.log + state file. 3) When done/capped, run publish_catalog.py to ship, then QC a few non-Max starts vs transcripts. 4) If session compacts: process is detached+resumable, just re-check log/state.
- LESSON: deepseek-chat full-catalog remap costs ~$0.004/song (5x the Max-run rate); budget ~$84 for 21k songs.

## [2026-06-15 19:48] b7 793da793
- DID: Solved remap cost: switched map_all_v2.py to deepseek-chat + window-sampling + 300s window cap. Validated n=12 vs Max flash overlay (same start accuracy). Killed pricey flash job. Relaunched cheap run PID 32088, ~$0.0005/song, whole catalog ~$12, hard cap $30. Committed+pushed.
- STATE: Cheap full-catalog remap RUNNING (PID 32088, log _work/map_all_v2.log, state _work/map_all_v2_state.json). ~21438 songs to do. No Grok needed (b22 still registering it, now optional).
- NEXT: Monitor job to completion; when substantially done run publish_catalog.py to ship live + QC a few non-Max starts vs transcripts. Watch for b21 speech-entry miss-class (guard reverts wild jumps).
- LESSON: MEASURE don't theorize: n=12 small-window sample under-estimated cost 50x; a free offline window-size analysis revealed sparse-marker outliers (1295-cap windows) and a 300s cap fixed it. Reasoning models (deepseek-v4-flash) cost ~7x non-reasoning (deepseek-chat) for the same accuracy here.

## [2026-06-15 19:58] b7 793da793
- DID: QC'd 15 new deepseek-chat starts in 3 batches via _work/qc_starts.py. Picture converged: ~8/15 dead-on, ~6/15 small jitter (+-3-6s, biased slightly EARLY = includes a trailing announce/dedication line, which is the SAFE direction), ~1 suspicious non-song 'Клип' entry. No wild jumps. Genuine bad class = b21's ~274 non-song speech entries (Вступление/Рассказ/Объявления/Клип), tracked in qc_b21/start_quality_flags_*.tsv.
- STATE: Remap RUNNING PID 32088, 300/21438, ~$0.0005/song on track for ~$12. QC shows song starts are solid (slight-early bias is safe). Speech-entry class needs separate handling later.
- NEXT: Keep monitoring to completion; spot-check more batches on later ticks (qc_starts.py OFFSET 5); when substantially done run publish_catalog.py + consider nulling/guarding the ~274 speech-class starts.
- LESSON: deepseek-chat start bias is slightly EARLY (includes trailing dedication/author-announce), which is the safe direction for intro-inclusion vs clipping the song.

## [2026-06-15 20:24] b7 793da793
- DID: Cleared safety-watcher atomic-write pause (b21+me confirmed os.replace is atomic, cron-safe). Remap PID 32088 at 1130/21438, $0.70 spent, ~$0.0005/song.
- STATE: Cheap remap RUNNING steadily ~5% done, on track ~$12, hard cap $30. QC converged earlier (starts solid, slight-early=safe; ~274 non-song speech entries are the only bad class).
- NEXT: Keep monitoring; spot-check more QC batches (qc_starts.py OFFSET 5); when substantially done run publish_catalog.py + null/guard the ~274 speech-class starts.

## [2026-06-15 21:16] b7 793da793
- DID: Remap PID 32088 at 2660/21438 (~12%), $1.53, on track ~$12. b21 refined QC: guard_starts ALREADY reverts most bad starts (COLLIDE/PREROLL/BACKLOAD); residual uncaught = speech-preface starts on [музыка] sitting in-slot. b21 will re-run flag_bad_starts_v02.py against FINAL store when I post 'remap-done' and hand me a clean residual-only queue.
- STATE: Cheap remap RUNNING steadily, hard cap $30. Starts solid (QC converged). b21 waiting for remap-done ping to produce residual defect queue.
- NEXT: WHEN REMAP FINISHES: (1) bcast post 'remap-done' to ping b21; (2) run publish_catalog.py to ship live; (3) take b21's v02 residual queue and null/guard those speech-class starts.

## [2026-06-15 22:24] b7 793da793
- DID: Wrote+pushed report/method doc song_timing_full_remap_cheap_20260615_v01_tomemex.md (bug, cheap-config fix, measure-first lesson, QC, speech-defect class, run steps, handoff). Remap PID 32088 ~4110/21438 (~19%), $2.29, on track ~$12. Slowed timer to 3600s.
- STATE: Remap RUNNING, cheap-config validated, doc shipped. Timer now hourly (long quiet crunch).
- NEXT: On finish: bcast 'remap-done' to ping b21; run scripts/publish_catalog.py to deploy live; take b21 v02 residual queue and null/guard the ~274 speech-class starts.

## [2026-06-16 07:43] b7 793da793
- DID: Remap PID died ~33% (laptop sleep, no crash); relaunched PID 5656, resumed from 6992 done, 14489 left
- STATE: Remap running again, $3.77 spent, est $12.17 total, on track; doc+method committed
- NEXT: On finish: bcast remap-done to b21, run publish_catalog.py, process b21 v02 speech-class residual queue
