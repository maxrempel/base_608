
## [2026-06-11 16:11] b8 4fbcff1f
- DID: Re-branched: I am now B8 (downloads/fill57). Sibling B7 takes start-fixing on the 452 caption videos. fill57 6/57 done on Sol, worker PID 15877 alive, watcher brvqccimu waits on fill57.done.
- STATE: B8 owns ~/song_timing/fill57_groq.py + the 57 no-caption downloads. B7 owns re-snapping starts on the 452. SHARED RISK: both write ~/song_timing/song_timing.json on Sol concurrently.
- NEXT: Brief B7 to write start-fixes to a SEPARATE file (not the live store) to avoid clobbering fill57's appends; merge at end. Keep watcher armed. Hold FULL HALT.
- LESSON: When two branches both edit one JSON store via read-modify-write, concurrent writes clobber; partition to separate output files and merge once.

## [2026-06-11 16:35] b8 4fbcff1f
- DID: B8 tick: fill57 8/57 done on Sol, worker alive, 0 failures. Built+committed collision_guard.py; audited LIVE store = 908/21714 (4.2%) impossible starts. B7 is shipping its own durable auto_start_overrides.json fix for those (autonomous, awaiting b0 gate).
- STATE: B8 owns 57 downloads (running, 10-min timer). DEPLOY SEQUENCE firmed: after fill57.done -> collision_guard --fix -> enrich -> apply_overrides(manual) -> apply_overrides(B7 auto_start_overrides) -> b0 PASS -> deploy --data. BOTH override passes required or B7 fix regresses.
- NEXT: Keep 10-min ticks until fill57.done (~49 videos left, ~12h). Then run deploy sequence through gate. No app.js.
- LESSON: B7 chose durable-override-file approach over store-merge for start fixes - more elegant (re-applies every deploy via apply_overrides), so final deploy must run apply_overrides for BOTH manual + auto_start files.

## [2026-06-11 17:19] b8 4fbcff1f
- DID: B8 tick: fill57 at 10/57 DONE, but videos 11 (BSFz6BFAa-8) and 12 (CF4TeAuS0DQ) FAILED with YouTube 'Sign in to confirm you are not a bot' (dl_fail), instant rejection at extraction.
- STATE: Worker alive, moved to video 13. 2 consecutive YT auth-wall failures after 10 clean downloads = possible IP bot-flag OR those 2 are login-restricted videos. CONSTRAINT: must NOT use Max's YouTube cookies (prohibited).
- NEXT: Watch next 2-3 videos: if failures continue = IP flag, PAUSE worker to avoid ban; if they succeed, the 2 were just restricted. Asked Max. Re-armed faster 240s timer to read the trend.
- LESSON: YouTube bot-check ('sign in to confirm not a bot') can appear mid-batch from a residential IP after ~10 downloads; instant-fail at extraction. Distinguish IP-flag (failures cluster/continue) from per-video login-restriction (isolated).

## [2026-06-12 13:23] b8 4fbcff1f
- DID: FIXED the YouTube bot-flag: researched online -> root cause is YT 'confirm not a bot' wall. Fix = yt-dlp --extractor-args youtube:player_client=tv_simply,default (TV-app client, no login/cookies needed). Verified on Sol via --simulate on 2 previously-failed videos (resolved 720p 136+251). Committed+pushed+scp'd to Sol, widened gap to 90-240s, re-enabled guard cron, relaunched worker pid 4820.
- STATE: fill57 RESUMING at 10/57 done (videos 11-16 will retry with new client). B7 built a continuous publisher (Pine cron kartoteka_publish every 3h, pull-only, guards starts on ALL vids) so finished timings auto-ship - I no longer need to deploy. Store=21957.
- NEXT: Verify next tick that videos 11+ download for real with tv_simply (not just simulate). If bot-flag returns despite tv_simply, escalate to po_token provider (bgutil) or longer wait. Keep 10-min ticks until fill57.done.
- LESSON: YouTube bot-wall on residential server: the tv_simply player_client bypasses it with NO login (Max's YT login stays untouched); pool with default to keep 720p itags. yt-dlp --extractor-args youtube:player_client=tv_simply,default.

## [2026-06-12 14:07] b8 4fbcff1f
- DID: B8 monitoring fill57 on Sol; tv_simply bot-flag fix holding, 13/57 done, 0 fails today, casualties 11-14 all recovering
- STATE: fill57_groq.py running on Sol (guard cron */10), worker alive, ~44 videos left at 90-240s gaps, spend ~$0.25
- NEXT: Keep 10-min tick monitoring; when 57 done OR fill57.done -> tell Max COMPLETE (B7 Pine cron kartoteka_publish auto-ships, no deploy by me) + STOP re-arming

## [2026-06-12 14:29] D8 4fbcff1f
- DID: D8 monitoring fill57 on Sol; tv_simply bot-wall fix holding (0 bot-walls); 15/57 done. NOTE: 1 transient HTTP-403 fail on IClIZlONxbs (different from bot-wall), worker continued
- STATE: fill57_groq.py alive on Sol (guard cron */10), ~42 left, spend ~$0.28. B9 (was D9) building Centauri Tamza-video backup, briefed with my 57 copies + tv_simply fix
- NEXT: Tighten tick to ~270s to see if 403s stack (=throttling=pause+escalate) or one-off. When 57 done OR fill57.done -> tell Max COMPLETE (B7 Pine cron kartoteka_publish auto-ships) + STOP re-arming

## [2026-06-12 14:53] D8 4fbcff1f
- DID: D8 monitoring fill57 on Sol; tv_simply bot-wall fix holding (0 bot-walls); 16/57 done, 1 isolated HTTP-403 straggler (IClIZlONxbs)
- STATE: fill57_groq.py alive on Sol (guard cron */10), ~40 left, spend ~$0.29. Backup team B9+b10 setting up Centauri (teal16, 192.168.1.176, D:/tamza_yt_full_backup); watcher flagged single-writer risk, I nudged them + offered my 57 Sol copies as seed
- NEXT: Keep 10-min tick; when 57 done OR fill57.done -> tell Max COMPLETE (B7 Pine cron kartoteka_publish auto-ships) + STOP re-arming. Stragglers need a guard relaunch / manual re-run

## [2026-06-12 15:18] D8 4fbcff1f
- DID: D8 (was B8) monitoring fill57 downloads on Sol via 10-min ScheduleWakeup ticks. tv_simply bot-wall fix HOLDING (0 bot-walls all day). 17/57 done, 1 isolated HTTP-403 straggler (IClIZlONxbs, harmless). Briefed backup team B9+b10; relayed Max: existing Tamza backup ~50-80% complete, B9 mapping it
- STATE: fill57_groq.py alive on Sol (maxre@192.168.1.113, ~/song_timing/, guard cron */10). Videos land Sol ~/song_timing/vids720/. ~40 left, spend ~$0.31. B9 single-writer owns full Tamza backup to Centauri(192.168.1.176 teal16)D:/tamza_yt_full_backup, HOLDING bulk pulls until D8 signals done (Sol+Cent share one home WAN IP). b10=setup only, stood down
- NEXT: Keep 10-min tick. WHEN 57 done OR fill57.done: tell Max COMPLETE; B7 Pine cron kartoteka_publish (3h, pull-only) auto-ships timings - NO deploy by me; POST --joint 'D8 DONE @B9 clear to start bulk'; STOP re-arming. Stragglers need guard relaunch/manual re-run (one-pass loop). Identity: D8==B8, done-signal comes from D8

## [2026-06-12 16:13] D8 4fbcff1f
- DID: D8 monitoring fill57 on Sol via 10-min ticks; tv_simply bot-wall fix holding (0 bot-walls); 21/57 done, 1 isolated HTTP-403 straggler (IClIZlONxbs)
- STATE: fill57_groq.py alive on Sol (maxre@192.168.1.113 ~/song_timing, guard cron */10), videos land ~/song_timing/vids720/, ~36 left, spend ~$0.42. B9 single-writer owns full Tamza backup to Centauri(192.168.1.176 D:/tamza_yt_full_backup), HOLDING bulk pulls until D8 signals done (shared home WAN IP); b10 setup-only stood down
- NEXT: Keep 10-min tick. WHEN 57 done OR fill57.done: tell Max COMPLETE; B7 Pine cron kartoteka_publish (3h pull-only) auto-ships timings NO deploy by me; POST --joint 'D8 DONE @B9 clear to start bulk'; STOP re-arming. Stragglers need guard relaunch/manual re-run. D8==B8

## [2026-06-12 16:37] D8 4fbcff1f
- DID: D8 monitoring Sol fill57 song-timing job, 23/57 done as of 16:19, tv_simply bot-wall fix holding (0 bot-walls all day)
- STATE: Worker alive on Sol, downloads progressing at 90-240s gaps, 1 isolated HTTP-403 (IClIZlONxbs 14:24) baseline. ~/usr/bin/bash.43 spend. B9 holding bulk Tamza backup until D8 signals 57-done (shared home WAN IP)
- NEXT: Keep 600s monitor ticks; on completed=57/fill57.done: tell Max COMPLETE, note B7 kartoteka_publish cron auto-ships (no deploy), POST --joint to clear B9, stop timer

## [2026-06-12 16:59] D8 4fbcff1f
- DID: D8 monitoring Sol fill57, 24/57 done as of 16:45 (Pn3k-SEpGaY 68 songs), tv_simply fix holding 0 bot-walls
- STATE: Worker alive, ~/usr/bin/bash.47 spend, 1 isolated HTTP-403 baseline (IClIZlONxbs). B9 holding bulk Tamza backup on shared home WAN IP until D8 done-signal
- NEXT: 600s monitor ticks; on 57/done: tell Max COMPLETE + note B7 kartoteka_publish auto-ships + POST --joint clearing B9 + stop timer

## [2026-06-12 17:42] D8 4fbcff1f
- DID: D8 monitoring Sol fill57, 26/57 done as of 17:09, tv_simply fix holding 0 bot-walls
- STATE: Worker alive, ~/usr/bin/bash.49 spend, 1 isolated HTTP-403 baseline (IClIZlONxbs). B9 holding bulk Tamza backup on shared home WAN IP until D8 done-signal
- NEXT: 600s monitor ticks; on 57/done: tell Max COMPLETE + note B7 kartoteka_publish auto-ships + POST --joint clearing B9 + stop timer

## [2026-06-12 18:04] D8 4fbcff1f
- DID: D8 monitoring Sol fill57, 29/57 done as of 17:49, tv_simply fix holding 0 bot-walls
- STATE: Worker alive, ~/usr/bin/bash.54 spend, 1 isolated HTTP-403 baseline (IClIZlONxbs). ETA ~midnight-1am. B9 owns full hucolo+tamza backup sizing/download; D8 stays on 57 song-timing lane
- NEXT: 600s monitor ticks; on 57/done: tell Max COMPLETE + note B7 kartoteka_publish auto-ships + POST --joint clearing B9 + stop timer

## [2026-06-12 19:02] D8 4fbcff1f
- DID: D8 bot-wall handling: PAUSED fill57 at 30/57 at 18:18 (2 consecutive auth/cookies fails WaxxIoIa0pA+Wo96_WRY8vA after 30 clean dls), killed worker + commented guard cron. After 40min cooldown RESUMED at ~19:02: uncommented guard cron + relaunched worker (alive)
- STATE: Worker running again at 30/57, testing if wall cleared. today-fails=3 (IClIZlONxbs 403 + 2 auth). B9 warned via bcast to HOLD bulk Tamza backup (shared home WAN IP flagged). ~/usr/bin/bash.57 spend
- NEXT: Wait ~5min, check next download: SUCCESS->back to 600s monitoring + tell B9 clear; FAIL again->re-pause + escalate to po_token or 2-4h wait. 3 failed vids need manual re-run at end (one-pass loop)
- LESSON: tv_simply held 30 videos then YouTube volume-throttled the home IP; 2 consecutive auth/cookies fails = wall returning, pause immediately to avoid deepening throttle

## [2026-06-13 13:43] D8 4fbcff1f
- DID: D8: after ~19h overnight rest (wall hit 18:18 on 06-12, was still up at 19:04 retry), RESUMED fill57 worker at ~13:42 on 06-13 to test if YouTube bot-wall cleared. Guard cron re-enabled, worker alive at 30/57
- STATE: Testing live - first download attempt in progress. Failed vids so far: IClIZlONxbs, WaxxIoIa0pA, Wo96_WRY8vA (won't auto-retry, need manual rerun). Max OK to manually solve a captcha puzzle once/twice if needed. Considering yt-dlp-invidious fallback plugin as durable self-heal. B9 still holding bulk backup (shared home IP)
- NEXT: Check log in ~3min: if download SUCCEEDS->wall cleared, normal 600s monitoring, tell B9 clear; if FAILS auth again->wall still up, re-pause + set up po_token or invidious fallback
- LESSON: after a YouTube volume-throttle on home IP, test resume after a multi-hour/overnight rest before building escalation infra - the rest often clears it for free

## [2026-06-13 14:08] D8 4fbcff1f
- DID: Quadrupled fill57 gap to 360-960s random (was 90,240) on Sol & restarted worker clean; wall cleared overnight, 31/57 recovering casualties. Flagged to Max that browser cookies = account-ban risk (his Tamza channel), holding cookies in reserve.
- STATE: Worker alive on Sol w/ wider gap, 0 fails today, 31/57 done. Awaiting Max's call on cookies (recommended NOT, or throwaway acct only).
- NEXT: Keep 600s monitor ticks; pause+escalate if 3+ consecutive auth fails; on 57/57 post --joint to free B9 for bulk backup, no deploy (B7 cron ships).

## [2026-06-13 14:33] D8 4fbcff1f
- DID: B8 (renamed from D8): running Sol fill57 worker, gap widened to 360-960s, restarted 14:06+14:15 (I wrongly relaunched a healthy worker twice - lesson: quiet log on wide gaps is NORMAL, never relaunch a worker:alive). 32/57 done, wall-casualties IClIZlONxbs+WaxxIoIa0pA recovered. B80 owns token+login (insurance only), B9 owns bulk backup. Wall cleared overnight, 0 fails today.
- STATE: Worker alive on Sol, 6-16min gaps, ~32/57, 0 fails. B80 minting po_token off-YT on Sol:4416. Told B9 honestly I have NO tested Invidious pool - gave real pacing data instead (8500K rate, throttled after ~30 pulls, 19h rest clears).
- NEXT: Monitor every 15min; ONLY relaunch if worker:DEAD 2 ticks or pause if WALL (3+ auth fails). On 57/57 post --joint 'B8 DONE' to free B9, no deploy (B7 cron ships). NEVER touch Max's main YT cookies.
- LESSON: Wide download gaps make quiet logs normal - check worker:alive + file growth before EVER concluding stall; do not restart a live worker on thin evidence (cost Max production twice).

## [2026-06-13 14:56] b8 4fbcff1f
- DID: Resumed Sol fill57 worker after B80 home-IP test; po_token plugin verified live in venv + provider :4416 healthy; confirmed B9 paced-parallel. Now investigating b11 report that SOL IS DOWN (host unreachable).
- STATE: 32/57 song-timings done, 0 fails today. po_token live. Conflict open: B80 says B9 hold-until-B8-DONE vs B9 says Max cleared throttled-parallel (asked Max to decide). Verifying Sol reachability now.
- NEXT: If Sol down: escalate to Max (needs physical/Tailscale power check), pause-watch every ~10min for Sol to return, then guard cron auto-relaunches worker. If Sol up: normal 12min monitor.

## [2026-06-13 15:18] b8 4fbcff1f
- DID: MIGRATING B8 off dying Sol per Max: VIDEOS->Centauri, PRODUCTION(worker)->Lak. Sol back up, worker was at 32/57 when migration ordered.
- STATE: Sol->Cent video copy RUNNING (detached pid 9812 on Sol, ~/vidcopy.log, 31 mp4s/42G -> Cent D:/tamza_yt_full_backup/song_timing_vids720). Lak recon done: py3.11+ffmpeg OK, yt-dlp ANCIENT(2023) must replace, NO docker (po_token provider skipped for now=insurance, 0 wall today). Worker deps: openai+requests+yt-dlp==2026.6.9+deepgram-sdk + local map_core.py. HARDCODED HERE=Path('/home/maxre/song_timing') line35 AND guard.sh - must edit to /home/mrempadmin on Lak. Resume state = queue.json+song_timing.json+fill57_state.json+fill57.log (copy ALL of ~/song_timing EXCEPT vids720+venv+__pycache__, <1G). API keys: deepseek_key.txt groq_api_key.txt deepgram_key.txt (in dir). player_client=tv_simply,default cookieless. Cent=D: label 16tbRaid 12.9TB free.
- NEXT: 1) tar project on Sol (excl vids720/venv/__pycache__) -> scp Sol->Cent relay -> Lak pulls from Cent (both SSH legs proven; Lak id_ed25519 in Cent authorized_keys). 2) On Lak: build venv (yt-dlp==2026.6.9 openai requests deepgram-sdk), edit HERE+guard.sh paths to /home/mrempadmin, set mrempadmin guard cron. 3) STOP Sol worker+cron (pkill + comment guard cron) so only ONE runs on the home IP. 4) START Lak worker, confirm resumes at 32/57 not 0. 5) coordinate board: B80(po_token), B9(on Cent for bulk). Lak access=lakarian-python MCP run_python_code (user mrempadmin, /home/mrempadmin).
- LESSON: Sol M720s hardware unreliable (frequent reboots/down) - moved production to Lak server (always-on, linger/systemd). Sol+Lak+Cent all same home LAN=same WAN IP, so migration buys reliability NOT IP-diversity.

## [2026-06-13 15:23] b8 4fbcff1f
- DID: MIGRATION COMPLETE: B8 production moved Sol->Lak, videos backing up Sol->Cent.
- STATE: Lak worker LIVE (pid 3068921, /home/mrempadmin/song_timing, venv yt-dlp 2026.6.9), resumed at 31/57 - PROVEN skipping done (vids720 empty, state done=31 unchanged). Sol worker STOPPED + guard cron commented '# MIGRATED-TO-LAK'. Lak guard cron set (*/10, linger=survives reboot). Sol->Cent video copy still running (detached pid 9812 on Sol, ~/vidcopy.log, ->Cent D:/tamza_yt_full_backup/song_timing_vids720). KEY: Cent(Windows)->Lak scp truncates binary - MUST use scp -O (legacy proto). Lak access=lakarian-python MCP.
- NEXT: 1) Monitor Lak worker via MCP (NOT sol_key SSH): load lakarian-python MCP, run_python_code to check pgrep + tail fill57.boot.log/fill57.log + completed count. First real download due in 6-16min - confirm it succeeds (po_token-less). 2) Finish/verify Sol->Cent video copy (check ~/vidcopy.log COPY_DONE_ALL; Sol now has 32 vids, copy may need re-run for stragglers). 3) On 57/57: post B8 DONE, B7 kartoteka_publish auto-ships. 4) Lak monitor cmd template in this log.
- LESSON: Windows-OpenSSH scp truncates binary files pulled by Linux scp; fix = scp -O (legacy protocol). Cost me 2 failed pulls before -O.

## [2026-06-13 15:24] b8 4fbcff1f
- DID: Max: Docker is NOT possible on Lak.
- STATE: Lak fill57 worker runs cookieless tv_simply,default - 0 wall all day, no po_token needed currently. Sol now hardware-hardened (b11: watchdog self-reboots 30s) but I'm NOT migrating back - Lak stands.
- NEXT: IF YT volume-wall returns on Lak (3+ consecutive auth/cookies DOWNLOAD FAIL): Docker is OUT on Lak. Options in order: (a) widen GAP_MIN/MAX beyond 360-960s; (b) run bgutil po_token provider in NODE/native mode (no Docker) on Lak; (c) point Lak yt-dlp at a po_token provider running on Sol or Cent over LAN (same home WAN IP so token valid) - coordinate with B80; (d) throwaway-acct cookies (yt_cookies_maxrempel35 exists, NEVER Max's main acct). Do NOT add Docker to Lak.
- LESSON: Lak (RempelServer/YunoHost Debian) cannot run Docker - any provider/service for Lak must be native/Node or hosted on another box.

## [2026-06-13 15:28] b8 4fbcff1f
- DID: Migration verified: Lak worker pid3068921 alive 31/57 on vid32; Sol vidcopy.log=COPY_DONE_ALL (32 vids); confirming Cent landing folder.
- STATE: Lak=production home. Sol=manual-restart spare only, NO auto-recovery expected.
- NEXT: Monitor Lak to 57/57. If YT wall returns on Lak (no Docker there), run bgutil po_token in Docker on SOL and serve Lak over LAN.
- LESSON: Sol policy per Max: usable on limited basis, manually restarted on crash, not relied on for uptime.

## [2026-06-13 15:49] b8 4fbcff1f
- DID: Lak worker advanced 31->32/57: vid32 Wo96 fully processed (downloaded 2.5GB + Groq transcribe + 77 songs mapped, +$0.03, total $0.647). Migration proven end-to-end on Lak. 0 wall-fails.
- STATE: Production fully on Lak pid 3068921, 32/57, healthy. Videos backup on Cent (31 done vids in D:\tamza_yt_full_backup\song_timing_vids720; the .f136 straggler was junk partial). Sol=manual spare (watchdog-armed by b11). b9 runs its proxy-split bulk backup in a SEPARATE outdir (option b agreed).
- NEXT: Monitor Lak to 57/57 via lakarian MCP. On 57/57: post 'B8 DONE' joint, B7 cron kartoteka_publish auto-ships, final Lak->Cent copy, stop.
- LESSON: fill57 stays cookieless tv_simply on Lak (0 walls all run); don't swap a healthy mid-run transcribe pipeline to b9's faster proxy method - different product (download+transcribe+map vs raw backup).

## [2026-06-13 16:15] b8 4fbcff1f
- DID: fill57 on Lak at 32/57, processing vid33 (downloaded 2.1GB 16:08, transcribing). 0 wall-fails entire run. Lak disk 744G free.
- STATE: Production on Lak pid 3068921 healthy+autonomous (guard cron */10 self-heals). Single /loop monitor armed ~16:33, 30min cadence. b9 bulk backup live on Lak in separate tamza_channel folder (no stomp). Sol=UNRELIABLE (b11 found bad non-ECC RAM, crashing during tests; needs Max+memtest86+ to pull DIMM).
- NEXT: Watch to 57/57. On done: tell Max COMPLETE, post --joint 'B8 DONE', B7 cron kartoteka_publish auto-ships, final Lak->Cent copy.
- LESSON: If fill57 ever hits a wall, best fallback is NOT Sol (bad RAM) - route downloads through b9's proxy-split split_backup.py on Lak (0-wall, no Docker, no Sol).

## [2026-06-13 17:04] b8 4fbcff1f
- DID: fill57 on Lak 35/57 (on vid36), 0 wall-fails whole run. Steady ~one video/8-12min.
- STATE: Production Lak pid 3068921 healthy+autonomous (guard cron self-heals). Single /loop monitor armed 17:35, 30min cadence. b9 bulk backup live on Lak in separate tamza_channel folder. Sol=bad RAM, unreliable.
- NEXT: Watch to 57/57 (22 left, ~3-4h). On done: tell Max COMPLETE, post --joint 'B8 DONE', B7 cron kartoteka_publish auto-ships, final Lak->Cent copy, stop.
- LESSON: Wall fallback = b9 proxy-split on Lak, NOT Sol (bad RAM).

## [2026-06-13 18:02] b8 4fbcff1f
- DID: fill57 on Lak 38/57 (vid39), 0 wall-fails entire run. ~one video/8-12min steady.
- STATE: Production Lak pid 3068921 healthy+autonomous (guard cron self-heals). b9 bulk backup separate tamza_channel folder. Sol=bad RAM unreliable. Re-establishing single 30min /loop monitor at 18:32.
- NEXT: Watch to 57/57 (19 left ~2-3h). On done: tell Max COMPLETE, post --joint 'B8 DONE', B7 cron kartoteka_publish auto-ships, final Lak->Cent copy, STOP.
- LESSON: Wall fallback=b9 proxy-split on Lak not Sol. Multiple overlapping /loop chains burn context - keep ONE.

## [2026-06-13 18:31] b8 4fbcff1f
- DID: Verified teal16=REAL RAID1 mirror (2x16TB Seagate ST16000NT001, 16TB usable, firmware/mobo RAID not Storage Spaces). Sol UP, 31 real song vids match teal16 by name. drives_registry.md found: drive=teal16.
- STATE: fill57 39/57 on Lak healthy, videos auto-drain Lak->teal16 via */30 cron. Sol song vids fully copied to teal16; about to size-verify before deleting from Sol.
- NEXT: Size-verify Sol vs teal16; if match, delete Sol vids720 to complete migrate-OFF-sol; keep monitoring fill57 to 57.
- LESSON: teal16 is named in zSyncMain/ssh/drives_registry.md; color+size naming; it IS a real RAID1 mirror confirmed via Win32_DiskDrive (2 member 16TB disks hidden from Get-Disk = firmware RAID signature).

## [2026-06-13 18:35] b8 4fbcff1f
- DID: Max approved (cautiously) switching fill57 to write directly to teal16 via SMB mount on Lak, instead of download-local-then-copy. KEY CONSTRAINT: do NOT do it during the live run - only AFTER 57/57.
- STATE: fill57 40/57 healthy on Lak. Videos drain to teal16 via */30 cron (working). Sol emptied. Pipeline must stay untouched until batch done.
- NEXT: AFTER fill57 hits 57/57: set up SMB mount of Centauri teal16 D: on Lak, point future runs' download dir there (eliminates copy step + */30 cron). Test on a fresh run, never the live one. Don't break anything.
- LESSON: Direct-to-teal16 mount is the elegant long-term design but risky mid-download (Cent reboots on Odysee sync = corrupt write); defer to post-batch.

## [2026-06-13 19:05] b8 4fbcff1f
- DID: fill57 monitor loop running on Lak, self-pacing ~25min. Sol emptied (31 vids byte-verified on teal16 RAID1). teal16=real RAID1 mirror 2x16TB Seagate on Centauri D:.
- STATE: fill57 ~40/57, worker alive pid 3068921, 0 walls, videos drain to teal16 via */30 lak2cent.sh cron. Max on break.
- NEXT: Keep monitoring to 57/57. On done: tell Max COMPLETE, post --joint B8 DONE, B7 cron auto-ships, final Lak->teal16 copy, STOP. AFTER batch: SMB-mount teal16 on Lak for direct writes (deferred, don't break live run).
- LESSON: b9: never curl/wget googlevideo for bulk DL (Google throttles dumb clients 200x); use yt-dlp native downloader.

## [2026-06-13 19:51] b8 4fbcff1f
- DID: fill57 monitor on Lak, self-pacing 25min. b9 PAUSED its backup after same-IP soft-wall; fill57 has home IP to itself, 0 walls. Sol emptied (31 vids byte-verified on teal16 RAID1).
- STATE: fill57 ~42/57, worker pid 3068921 alive, vid43 in flight. Videos drain Lak->teal16 via */30 lak2cent.sh cron. Max on break.
- NEXT: Monitor to 57/57. On done: Max COMPLETE + post --joint 'B8 DONE' (frees b9) + B7 cron kartoteka_publish auto-ships + final Lak->teal16 copy + STOP re-arming. AFTER batch: SMB-mount teal16 on Lak for direct writes (deferred, dont break live run). teal16=real RAID1 mirror 2x16TB Seagate on Centauri D:, in zSyncMain/ssh/drives_registry.md.
- LESSON: Reach Lak via lakarian-python MCP run_python_code (user mrempadmin). Cent reachable via sol_key SSH to 192.168.1.176. Lak->Cent scp uses Lak id_ed25519 + scp -O.

## [2026-06-13 20:17] b8 4fbcff1f
- DID: fill57 at 45/57, worker pid3068921 alive, vid45 jlwGxz-w1MA done 20:13. b9 acked FULLY PAUSED until B8 DONE (proxy-resolve = dumb-bucket trap, confirmed). 0 fresh walls.
- STATE: Monitoring to 57/57, ~12 left ~2h. teal16 RAID1 confirmed, Sol emptied, */30 lak2cent cron live.
- NEXT: On 57/57: tell Max COMPLETE, post --joint B8 DONE, final Lak->teal16 copy, STOP. Then deferred SMB-mount.

## [2026-06-13 20:51] b8 4fbcff1f
- DID: fill57 at 46/57, worker pid3068921 alive (vid47 lTwoF1m8pZc transcribing). 0 fresh walls. Multiple stale /loop dup chains draining, collapsing each to single 25min ScheduleWakeup.
- STATE: Monitoring to 57/57, ~11 left ~1.5h. b9 fully paused until B8 DONE. teal16 RAID1 confirmed, Sol emptied, */30 lak2cent cron live. Context ~66pct, compaction OK - summary+worklog cover resume.
- NEXT: On 57/57: tell Max COMPLETE, post --joint B8 DONE, final Lak->teal16 copy to D:\tamza_yt_full_backup\song_timing_vids720, STOP re-arm. Then deferred SMB-mount teal16 on Lak (Max approved, dont break live run).

## [2026-06-13 21:35] b8 4fbcff1f
- DID: fill57 at 49/57, worker pid3068921 alive (vid50 sh0oiKweBYo START 21:31, 64 songs). 0 fresh walls. Stale /loop dup chains still draining, collapsing each to single 25min wakeup.
- STATE: Monitoring to 57/57, 8 left ~1h. b9 fully paused until B8 DONE. teal16 RAID1 confirmed, Sol emptied, */30 lak2cent cron auto-migrating. Context ~81pct - compaction imminent, summary+worklog cover resume.
- NEXT: On 57/57 or fill57.done: tell Max COMPLETE, post --joint 'B8 DONE' (frees b9), B7 Pine cron kartoteka_publish auto-ships (no deploy), final Lak->teal16 copy to D:\tamza_yt_full_backup\song_timing_vids720, STOP re-arming. Then deferred SMB-mount teal16 on Lak (Max approved, dont break live run).

## [2026-06-13 22:09] b8 4fbcff1f
- DID: fill57 at 50/57, worker pid3068921 alive (vid51 wE6H246sagU downloaded 2GB 22:02, 87 songs - huge, transcribing). 0 fresh walls. Dup /loop chains draining, collapse each to single 25min wakeup.
- STATE: Monitoring to 57/57, 7 left ~45min. b9 fully paused until B8 DONE. teal16 RAID1, Sol emptied, */30 lak2cent auto-migrating. Context ~91pct - compaction imminent.
- NEXT: On 57/57 or fill57.done: tell Max COMPLETE, post --joint 'B8 DONE' (frees b9), B7 Pine cron kartoteka_publish auto-ships (no deploy), final Lak->teal16 copy to D:\tamza_yt_full_backup\song_timing_vids720, STOP re-arming. Then deferred SMB-mount teal16 on Lak (Max approved, dont break live run).

## [2026-06-14 07:59] b8 4fbcff1f
- DID: fill57 COMPLETE 57/57, fill57.done written 00:20:52, worker exited clean. B8 DONE joint posted (b9 freed). All 57 vids verified on teal16.
- STATE: DONE - monitor loop ended, no re-arm
- NEXT: None. B7 Pine cron kartoteka_publish auto-ships timings. Deferred SMB-mount teal16 on Lak = separate task, confirm w/ Max first.
