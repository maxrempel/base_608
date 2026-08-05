
## [2026-06-12 14:40] B9 46651386
- DID: Joined as B9 (Tamza b-team). Scoped Tamza full-channel YT backup: channel=936 videos (catalog=509). Got D8 bot-wall fix (yt-dlp tv_simply TV-client, no cookies). Centauri 16TB box NOT reachable from Pine.
- STATE: Max paused all downloads - wants optimal anti-block setup confirmed first. Access path to Centauri drive still undecided (A=RDP onto Cent, B=Sol, C=share).
- NEXT: Design optimal anti-block strategy; key insight = all home machines share ONE residential IP so pacing must be global across me+D8.

## [2026-06-12 14:59] B9 46651386
- DID: Inventoried Tamza+Hucolo. Tamza YT=1591 unique (936 vids+33 shorts+622 livestreams, 2720hr). Hucolo Odysee @hucolo=1167 vids (1570hr). Total 2758 vids/4290hr/~2-6TB. Lists in claude_base/tools/tamza_hucolo_backup/inventory/. All metadata-only, no downloads.
- STATE: Downloads still PARKED - B8 actively pulling 57 on shared home IP. teal16 access confirmed. Inventory summary written.
- NEXT: Wait for B8 done-signal, then design paced download (tv_simply client, run ON Cent). Verify Cent Odysee sync already-have before re-pulling Hucolo.

## [2026-06-12 15:21] B9 46651386
- DID: MAPPED what is where (B9, Tamza+Hucolo backup). SOURCE=YouTube for BOTH. Tamza YT(UCo-O_aBrW8J3hEGEdow71Iw)=936 vids+622 streams+33 shorts (tabs non-overlap, verified). Hucolo YT(UCj5wGWloHE8hKHPd5kqWsJQ)=730 vids+553 streams. Cent odysee_sync was YT->Odysee MIRROR-AND-DELETE: only 21 Tamza + 7 Hucolo real .mp4 remain locally (rest are empty sync-record folders: 304 Tamza, 121 Hucolo). So local backup ~1pct = effectively from-scratch.
- STATE: Downloads STILL PARKED. D8(=former B8) at 17/57 song-timing pulls on Sol; will post 'D8 DONE' on joint when finished - THAT is my go-signal. Sol+Cent+Pine share ONE home WAN IP. Odysee-sync client now PAUSED by Max (frees IP). teal16=Cent 16TB, ssh -i ~/.ssh/sol_key maxre@192.168.1.176, target D:\tamza_yt_full_backup (empty). Inventory lists in C:\claude_base\tools\tamza_hucolo_backup\inventory\.
- NEXT: Await D8 DONE. Then design paced bulk download (yt-dlp tv_simply TV-client, no cookies, --limit-rate ~8500K, 90-240s random gaps) run ON Cent (residential IP) straight into D:\tamza_yt_full_backup. Confirm with Max: shorts excluded, include livestreams. Job=~2841 videos. After backup: re-upload to Odysee + more video work.

## [2026-06-12 15:27] B9 46651386
- DID: CRITICAL CORRECTION: Odysee is NOT bot-tolerant. First real download test (yt-dlp @tamza item1) FAILED with HTTP 429 Too Many Requests + no formats. Likely triggered by my ~6 listing probes minutes earlier. So 'rebuild from Odysee at full speed' is WRONG - Odysee rate-limits too, needs pacing/backoff just like YouTube. Also got 302 Tamza YT-ids already-on-Odysee saved to inventory/tamza_on_odysee_ytids.txt (for matching D8's 57).
- STATE: Asked D8 for his 57 YT-ids to match vs the 302 on-Odysee list. Awaiting D8 reply. Odysee download capability UNPROVEN (429'd). teal16 target still empty. Both YouTube AND Odysee now known to rate-limit -> all pulls must be paced + backoff.
- NEXT: Wait for D8's 57 list; intersect with tamza_on_odysee_ytids.txt. Retry Odysee download AFTER a cooldown (single, slow, with --retries/--sleep-requests) to find safe Odysee rate. Re-plan: both sources need gentle pacing; no full-speed anywhere.

## [2026-06-12 15:33] B9 46651386
- DID: Got D8's full 57-id target list from Sol (~/song_timing/missing_vids.txt, not waiting for board reply). Ran match_ids.py: 17/57 confirmed on Odysee, 40 not in known set.
- STATE: match_ids.py + outputs in claude_base/tools/tamza_hucolo_backup/inventory/ (d8_57_ids.txt, matched_on_odysee.txt=17, missing_need_youtube.txt=40). on-Odysee map is only 302 of ~1292 real @tamza items, so 17 is a LOWER BOUND. Odysee 429s too.
- NEXT: Decide with Max whether id-level full-coverage matching (shorts-excluded, both sides) is worth building the claim-id->ytid map for. No downloads (YT gated on D8 DONE; Odysee needs cooldown).

## [2026-06-12 15:41] B9 46651386
- DID: Built build_odysee_map.py: enumerates @tamza (1292 claims, one flat call, no 429), then per-item -J fetch + parse description to extract source YT id. Tested: 10/10 extract OK at sleep=2, no 429.
- STATE: Full 1292 run launched in background (bg id bimbwycam) writing odysee_tamza_map.csv (claim_id,yt_id,note), resumable, exp-backoff on 429. ETA ~2.5h. KEY: --print description mangled UTF-8 tail; -J+json parse is the reliable extractor.
- NEXT: When map done: intersect its yt_ids with Tamza YT id lists (936 vid + 622 streams, shorts EXCLUDED both sides) for REAL coverage. Then same for Hucolo. No downloads (YT gated on D8 DONE).

## [2026-06-12 15:53] B9 46651386
- DID: AUTONOMOUS mode armed (wake 20min). Caught+fixed silent-fallback bug in build_odysee_map.py: Odysee 429s were recorded as 'no_yt_id'=false miss. Now 429/error -> retried, never written. Discarded corrupted rows, kept 13 confirmed-ok.
- STATE: Map build relaunched bg id bijlu68h6 at sleep=5 (slower, Odysee 429s after ~50 items at sleep=2). odysee_tamza_map.csv resumable. ETA ~3h. Wake re-arms each cycle.
- NEXT: Each wake: check map progress (wc -l csv + log tail), check board for D8 DONE. When map done: id-level coverage intersect (shorts excluded). Only start YT bulk after D8 DONE.

## [2026-06-13 12:45] B9 46651386
- DID: Overnight Pine run FAILED: Pine slept + job stuck 1hr on a dead Odysee claim (only 17 done). Fixed script error-handling (errors=2 quick retries then extract_error+move on; only 429=long backoff+leave-for-retry; per-item backoff reset). MOVED job to always-on Centauri.
- STATE: Centauri PID 10488 (D:\tamza_yt_full_backup\odysee_map\, job.pid file). Runs python -m yt_dlp (installed there), --sleep 5, hidden/detached, survives SSH close + Pine sleep. 18/1292 rows, 1275 todo. csv resumable.
- NEXT: Each wake: SSH Centauri, check job.pid alive + wc csv + log tail. If died/done: inspect. When map complete: id-level coverage intersect vs Tamza YT ids (shorts excluded). Watch board for D8 DONE.

## [2026-06-13 13:39] B9 46651386
- DID: Max: Centauri is Windows=less stable/more often down. MOVING map build from Centauri to Sol (Linux, always-on, more reliable). Map build is light metadata (1 yt-dlp -J per 5s) so won't disturb D8's YT pulls on Sol (diff service: Odysee vs YouTube, same IP ok).
- STATE: MID-MIGRATION. Centauri job=PID in D:\tamza_yt_full_backup\odysee_map\job.pid (~80 rows done). Target: Sol 192.168.1.113 ~/.ssh/sol_key, run build_odysee_map.py there under nohup. Files: build_odysee_map.py + odysee_tamza_claims.txt + odysee_tamza_map.csv (grab latest csv from Centauri to keep progress).
- NEXT: Kill Centauri job; scp Centauri csv->Pine->Sol (or just reuse Pine copies, resumable); ensure yt-dlp on Sol; nohup launch; monitor via SSH. Then id-level coverage when done. Watch board D8 DONE.

## [2026-06-13 13:49] B9 46651386
- DID: Migrated Odysee map-build off Pine/Centauri to always-on Sol (Linux); single clean writer PID 23736 in ~/odysee_map venv, sleep=5
- STATE: 91/1292 rows done; 3 dup claim rows from brief double-writer window (harmless, dedup at end); build several hours to finish
- NEXT: Each wake: ssh Sol check pgrep+wc+tail; on completion dedup CSV then id-level coverage match. Hold all YT downloads until D8 DONE on board

## [2026-06-13 14:13] B9 46651386
- DID: Decoded 'individous'=Invidious (open-source YT front-end). Researched 2026 status thoroughly. Max wants it self-hosted on Sol, Dockerized, throttled to 33% of measured max. Purpose ties to bulk backup (D8: route yt-dlp player-resolution via Invidious so bot-wall fires on instance IP not ours; bytes from CDN).
- STATE: Verdict: residential home IP = ideal for Invidious (datacenter/VPS blocked). Low danger for private LAN-only personal use. Self-host on Sol does NOT shield our IP (Sol=our home IP); shield needs EXTERNAL instances. Sol Odysee map build still running in parallel (~91+/1292).
- NEXT: Check Docker on Sol; if present, docker-compose Invidious LAN-only, then wire request throttle to 33% of measured-max rpm. Keep private (no public instance). Hold heavy use until D8 DONE to spare shared IP.

## [2026-06-13 14:16] B9 46651386
- DID: Sol Invidious setup IN PROGRESS: installed Docker 29.1.3 + compose 2.40.3 + git on Sol (sudo pass in zSyncMain/ssh/sol_sudo_password_20260523.txt), added maxre to docker group (active, docker ps works no-sudo). Cloned iv-org/invidious to ~/invidious. Shipped compose is DEV-only (builds locally, no Companion).
- STATE: Need PRODUCTION compose with invidious-companion (research: companion improves residential bot-detection resistance). Bind 127.0.0.1:3000 -> will expose LAN-only. Postgres14 + companion + invidious. Need hmac_key + companion SERVER_SECRET_KEY(16ch). Throttle 33%: no native dial, throttle = requests/min, measure max-before-block then cap 1/3.
- NEXT: Fetch official prod docker-compose.yml (companion) from docs.invidious.io/installation; write to ~/invidious-prod/docker-compose.yml on Sol; gen secrets; docker compose up -d; test localhost:3000/api/v1/stats; then bind to LAN IP 192.168.1.113. Sol Odysee map build still running parallel.

## [2026-06-13 14:19] B9 46651386
- DID: Invidious LIVE on Sol. Stack up via ~/invidious/docker-compose.prod.yml (invidious+companion+postgres14). companion healthy; stats endpoint + real video (dQw4) resolve title OK = metadata resolution works on Sol residential IP. Bound 0.0.0.0:3000 -> LAN at http://192.168.1.113:3000 (private, not internet-forwarded). Secrets in ~/invidious/secrets.txt (chmod600). Compose archived at C:/claude_base/tools/invidious_sol/.
- STATE: WORKING. Idle = zero YouTube load (only fetches on request) so safe alongside D8. Sol Odysee map build still running in parallel. Throttle-33% not yet wired (only meaningful at bulk-backup time via yt-dlp-through-Invidious; interactive browse is naturally light).
- NEXT: Optional: wire 33% rate cap when bulk backup starts (measure max rpm before YT block, cap 1/3). Add README to tools/invidious_sol. Commit+push. Restart policy unless-stopped = survives reboot. Heavy use after D8 DONE.

## [2026-06-13 14:26] B9 46651386
- DID: DIALOGUE (dia22). CORRECTED understanding of the real backup design (Max+B8 designed it; I'd missed it due to split-board comms bug, now patched by C10). DESIGN: download 2000 OWN Tamza/Hucolo videos by routing the METADATA/player-resolution request through OTHER PEOPLE'S public Invidious instances (their IP eats YouTube's bot-wall), while the HEAVY video bytes come direct from googlevideo CDN to us (CDN doesn't bot-wall). So a SELF-HOSTED Invidious on Sol is the WRONG config (it resolves from OUR IP = no shield).
- STATE: My Sol Invidious is live but is NOT the shield - keep only as private-YT bonus or tear down. Google Takeout was already tried + failed: 2000 videos came as dozens of browser download links, expire in 7 days, manual clicking didn't work = 2 days suffering (Max rejects Takeout). HONEST CONCERN raised to Max: 2026 public Invidious network has collapsed to ~couple instances, heavily rate-limited - thin supply may throttle us / be slow for 2000.
- NEXT: HOLDING per dia22. Offered to research live count+throughput of usable public Invidious instances. Next: sync with B8 (comms now fixed) to get their exact pipeline design; B80 building bgutil po_token+cookies as alt anti-block. Do NOT implement until Max says doit22. Sol Odysee map build still running parallel.

## [2026-06-13 14:28] B9 46651386
- DID: VALIDATED the real backup design via web research (Max confirmed 'Finally'). TOOL EXISTS: yt-dlp plugin 'yt-dlp-invidious' (github.com/grqz/yt-dlp-invidious, PyPI yt-dlp-invidious) - resolves video METADATA through EXTERNAL Invidious instances (their IP eats YouTube bot-wall), falls back to Invidious on 'confirm you are not a bot' errors, supports preferred_instance + retries + rotation when an instance gets IP-blocked. Video BYTES come direct from googlevideo CDN to us. This IS the 'metadata via other people's IPs, heavy traffic to us' design Max+B8 built.
- STATE: Takeout REJECTED for good: thousands of videos = dozens of 7-day-expiring browser links (2 days disaster); Dropbox too expensive; Google Drive fails (brand/Workspace account). Self-hosted Sol Invidious = WRONG for shield (our IP) - it's live but only a private-YT bonus. Real catch: 2026 public Invidious instances are FEW + rate-limited; rotation across pool is the documented mitigation (what the plugin does). B80 building alt path: bgutil po_token + cookies (authenticate as real client).
- NEXT: HOLDING per dia22 - do NOT build until doit22. Proposed next: sync with B8 (comms fixed by C10) for the working instance pool, then ONE agreed plan = yt-dlp-invidious plugin + instance list + 33% pacing, downloading 2000 Tamza+Hucolo to teal16 (D:/tamza_yt_full_backup on Centauri). Sol Odysee claim->ytid map build STILL running parallel in ~/odysee_map.

## [2026-06-13 14:44] B9 46651386
- DID: B8 ANSWERED (honest): B8 does NOT actually run Invidious - uses yt-dlp player_client=tv_simply,default COOKIELESS. NO battle-tested Invidious pool exists; the 'metadata from instance IP' was THEORY not validated. The PROVEN working method (B8 downloading right now, 32/57) = yt-dlp tv_simply + bgutil po_token + heavy pacing, NOT Invidious. B80 installed bgutil po_token provider (Docker :4416 restart=unless-stopped) into b8 venv = mints gvs po_token for tv_simply cookieless, resolves 720p clean, no cookies/JS.
- STATE: REAL pacing data from B8: LIMIT_RATE 8500K (~33% of 220Mbps); inter-video gap 90-240s; VOLUME-throttled after ~30 clean pulls on home IP (volume bot-wall, not per-video); 40min cooldown did NOT clear, ~19h overnight rest DID; now gaps widened to 360-960s (6-16min). Net: <30/burst, pace well under. To USE Invidious you must LIVE-probe instances from docs.invidious.io/api.invidious.io (/api/v1 + stream redirect), rotate on 403/429 - thin dying pool, risky for 2000.
- NEXT: REFRAMED PLAN for 2000 Tamza+Hucolo->teal16: copy B8's PROVEN method (tv_simply + bgutil po_token + wide 360-960s pacing = the real 33% throttle), NOT the unvalidated Invidious-pool route. Invidious = optional later optimization (offload flagged request off-IP) needing live instance testing. My Sol self-hosted Invidious = private-YT bonus only. HOLD bulk until B8 DONE (32/57). Roster: b6=player,b7=fixing,b8=video downloads,b80=login+token,b9=me=youtube blocks.

## [2026-06-13 14:59] b9 46651386
- DID: Validated the metadata/bytes SPLIT on Pine AND Lak: yt-dlp resolves CDN url (tv_simply,default cookieless, no po_token needed at low volume), then plain curl fetches bytes (http 206) with NO proxy and NO bot-wall. Public Invidious route DEAD (nadeko/nerdvpn/yewtu all disabled video API 401/403/Endpoint-disabled). Sol CRASHED ~14:40 (Max restarting; 2nd crash in 4 days, failed stress test). Switched host to Lak (RempelServer, always-on, 192.168.1.199 via lakarian-python MCP): updated its ancient 2023 yt-dlp to 2026.06.09 in ~/yt_backup_venv, proven resolve+curl split works. Built paced_backup.py (all-in-one yt-dlp version) at C:/claude_base/tools/tamza_hucolo_backup/.
- STATE: ARCH DECIDED: rotating residential proxy for the TINY metadata resolve only (new IP per video, never accumulates volume wall) + heavy ~2TB bytes direct from Google CDN to home IP = FREE. Cost ~$2-15 total since only KB/video goes through paid proxy. Lak ready as host (747G buffer, rsync to Centauri teal16 later). Max is READY TO PAY. yt-dlp lists 936 tamza_videos + 622 streams (shorts excluded) = 1558 + Hucolo 1167.
- NEXT: 1) Get Max go/no-go on IPRoyal PAYG residential proxy signup (I do signup via Playwright w/ mass@tamza, HE enters card). 2) Rebuild paced_backup.py to the SPLIT model: resolve-via-proxy (rotating) + curl-direct bytes, single-thread, wide pace, resumable, no-sloppy-fallback. 3) Land bytes on Lak then rsync to Centauri teal16. 4) Coordinate w/ b8 (shares home IP, but proxy isolates our metadata).
- LESSON: The metadata-resolve and CDN-byte-download are fully INDEPENDENT in yt-dlp: resolve with --get-url, then fetch the returned googlevideo URL with plain curl (http 206 range works), no session/proxy/po_token carryover. This is what makes 'proxy only the metadata, bytes direct & free' viable.

## [2026-06-13 15:18] b9 46651386
- DID: IPRoyal account CREATED + email VERIFIED. mass@tamza.com / CopperHarbor47lake# (saved to shared_logins_frequent.txt). Max solved the hCaptcha manually (Playwright window had been minimized). Browser now logged into dashboard.iproyal.com.
- STATE: NEXT IMMEDIATE: buy Residential Proxies smallest pack (1GB ~$7) -> enter Max's card (he gave it, DO NOT SAVE, never echo) -> go to residential access/Generate panel -> create ROTATING endpoint -> copy host/port/user/pass. Then wire into split runner on Lak and launch. Lak host READY (yt-dlp 2026.06.09 in ~/yt_backup_venv, resolve+curl split PROVEN). Sol back up but Lak is our host. Split arch validated: resolve via proxy(rotating) + curl bytes direct = ~$2-15 total.
- NEXT: 1) Playwright: navigate dashboard, buy 1GB residential, card entry, get rotating proxy creds. 2) Rebuild paced_backup.py to split model (resolve --proxy rotating + curl direct -o). 3) Launch on Lak writing to ~/yt_backup, rsync to Centauri teal16. Source lists already on... need to scp tamza_videos.txt+streams to Lak (Sol scp failed during crash).
- LESSON: mass@tamza.com is readable via IMAP witcher.mxrouting.net:993 (creds in mxroute_smtp_creds_20260528.txt, pass M4ss-Tamza-Send-2026=Kq9w) - used it to pull IPRoyal verify link autonomously, no need to ask Max to check email.

## [2026-06-13 19:10] b9 46651386
- DID: Ran decisive HYBRID test on Lak: proxy-resolve (default/web client) WORKS (returns 720p itag-136 googlevideo URL via proxy IP), but native-download of that handed-off URL = only 1.6 Mbit/s (throttled). yt-dlp throttle-solving is bound to it doing resolve+download in ONE process; a bare URL = dumb bucket. HYBRID REJECTED. tv_simply client currently flag-walled (429/DRM); default/web client still resolves.
- STATE: Pipeline PAUSED (pace cron commented, worker dead, drainer cron active). Core speed problem solved+committed d14cc98b: yt-dlp full-native no-proxy ~100 Mbit/s proven. Home IP soft-walled from MY test burst, needs cooldown. bcast'd b8 re same-IP coordination.
- NEXT: Let home IP cool (hours). Resume = un-comment pace cron once cooled + b8 cadence agreed. Deployed wide-pacing 300-600s design (b8-proven safe) is correct; no proxy. Consider po_token shield bgutil :4416 if default-client resolves wall at volume.
- LESSON: Cannot split yt-dlp resolve from download to dodge an IP wall: the anti-throttle token is only applied to fetches yt-dlp issues itself during its own extraction. A --get-url handoff to any other downloader (curl OR yt-dlp-on-bare-url) reverts to ~0.2-1.6 Mbit/s. Fast youtube download REQUIRES one yt-dlp process doing resolve+download together, forcing resolve+bytes onto the same IP.

## [2026-06-13 20:14] b9 46651386
- DID: Coordinated with b8 on bcast: agreed I stay FULLY PAUSED until b8 posts 'B8 DONE'. b8's fill57 finishing run (15 vids left, ~2-3h, one-at-a-time on home IP) is PRIORITY; two YT resolvers on the home IP at once is what caused today's wall. b7 confirmed NOT in contention (cached transcripts, zero YT). b8's proxy-resolve fallback rejected for me (= the dead hybrid, 1.6Mbit).
- STATE: Tamza backup PAUSED (pace cron commented, worker dead, drainer cron active, 3/1558 drained). Repo synced+pushed (99dbd475). Waiting on b8's 'B8 DONE' signal (~2-3h) to resume.
- NEXT: On 'B8 DONE': uncomment pace_controller cron on Lak (as mrempadmin) to relaunch the single yt-dlp-native worker (300-600s gaps, tv_simply,default, no proxy). Then monitor first few pulls for walls. The method is proven; only the same-IP timing was the blocker.
- LESSON: Same-IP YT contention is real and bites fast: b8's fill57 + my backup both resolving on the home WAN IP triggered the bot-wall within ~20min. Fix is serialization (one resolver at a time), NOT proxying (proxy-resolve+handoff throttles).

## [2026-06-14 08:57] b9 46651386
- DID: b8 posted 'B8 DONE' (fill57 57/57, home IP free). RESUMED tamza backup: restored pace_controller cron on Lak (uncommented */5), single yt-dlp-native worker relaunches within 5min (300-600s gaps, tv_simply,default, no proxy). Acked b8.
- STATE: Backup RESUMING - I am the only YT resolver on the home IP now. 3/1558 drained pre-pause. Method proven (~100Mbit/s native); same-IP contention was the only blocker, now cleared.
- NEXT: Verify first 1-2 pulls in /home/mrempadmin/yt_backup/out/backup.log are OK (no WALL) ~20min after relaunch. If walls reappear, re-pause + reassess. Else let it run; drainer ships .mkv to Centauri automatically.
- LESSON: Peer serialization worked: waiting out b8's fill57 run cleared the home-IP wall cleanly - no proxy gymnastics needed, just one resolver at a time.

## [2026-06-14 09:20] b9 46651386
- DID: Resumed backup on B8 DONE but it WALLED on every pull (3 walls/0 ok in 16min). Diagnosed: home IP is FINE (default/web client resolves 720p 136+251 direct, no proxy, no 429) - the cooldown worked. Root cause = tv_simply client itself is currently DEAD (returns no formats -> android fallback -> 'format unavailable'); web_safari also fails. tv_simply worked for b8 overnight but has gone intermittent again. bgutil :4416 po_token provider is DOWN for everyone (b8 ran without it). Re-PAUSED worker+cron to stop wall-hammering.
- STATE: Backup PAUSED again (cron commented 0918, worker killed, 3/1558 drained). DECISION NEEDED (Max's call): tv_simply=wall-resistant-but-currently-dead vs default=works-now-but-historically-walls-at-volume. Did NOT autonomously switch+blast 1555 vids (would risk re-flagging the just-cooled IP).
- NEXT: Either: (a) wait for tv_simply to recover (intermittent) then resume original recipe = clean, no change; or (b) Max approves switching worker to default client +/- start bgutil po_token shield as volume protection. Hourly check will test if tv_simply resolves again; if yes, resume as-is.
- LESSON: IP-flag vs client-flag are different failures with the same 'format unavailable' symptom: test multiple player_clients with a single --simulate resolve to tell them apart before assuming the IP is walled. default client working = IP is clean even when tv_simply 429s.

## [2026-06-14 12:53] b9 46651386
- DID: tv_simply client RECOVERED (clean 720p 136+251 resolve, no wall). RESUMED backup with ORIGINAL recipe unchanged - restored pace_controller cron + kicked it, single yt-dlp-native worker now ALIVE. No strategy change needed; this was the clean 'wait for tv_simply' path.
- STATE: Backup RUNNING again on home IP (only resolver). 3/1558 drained so far. Recipe: tv_simply,default, no proxy, 300-600s gaps. IP confirmed clean, tv_simply confirmed working this tick.
- NEXT: Verify in ~20min: backup.log shows OK pulls (no WALL/format-unavailable streak). If tv_simply flaps dead again + walls resume, re-pause. Else let it run; drainer ships .mkv to Centauri. ~1555 to go at ~7.5min spacing = several days (Max OK'd 1-2 weeks).
- LESSON: tv_simply flakiness is transient (dead one hour, fine the next) - a quick single --simulate probe each tick tells you whether to resume the original recipe vs wait, no code change needed.

## [2026-06-14 13:17] b9 46651386
- DID: Resumed after tv_simply recovered but it WALLED AT VOLUME: single --simulate probe passes, but sustained pulls at 300-600s cadence 429 every time (9 walls/0 new ok). Re-PAUSED (cron commented 1316, worker killed). KEY: the wall is VOLUME/cadence-driven on the home IP, NOT the client and NOT a dead-IP - probes pass between walls. b8 got 15 vids through with WIDER 6-16min one-at-a-time pacing + a rest.
- STATE: Backup PAUSED, safe cooling state. 3/1558 drained. Two failed resume attempts today both walled at the 300-600s pace. drainer cron still active (CDN-only, safe). IP is freshly hit - needs HOURS of rest before next try.
- NEXT: RECOMMENDED next (needs Max nod on timeline): (1) let IP cool several hours; (2) widen pace_controller gaps from 300-600s to ~600-1200s+ (b8's proven 6-16min profile) - this stretches 1555 vids to ~2-3 weeks, near/over Max's 1-2wk window, hence his call; (3) optionally stand up bgutil po_token shield :4416 for extra wall resistance. Do NOT auto-resume at 300-600s - it just walls.
- LESSON: A single passing --simulate probe does NOT prove the method works - the wall is volume/cadence-driven. Must distinguish single-resolve health from sustained-cadence health. b8's evidence: 6-16min wide pacing survives where 5-10min walls on the same IP.

## [2026-06-15 23:29] b9 46651386
- DID: Resumed tamza YT backup: widened pace_controller to 600-1200s (10-20min) gaps, re-enabled keeper cron, launched worker (pid 79371). IP cooled ~34h since last wall.
- STATE: Worker running on tamza_all.txt (1555 todo, 3 done). NO logged-in cookies yet - that's likely why some pulls hit format/wall errors. Max asked about cookies + wants a never-sleep timer.
- NEXT: Watch first results in 4min; if walls/format-fails persist, add Max's logged-in YT cookies (robust fix) to allow tighter pacing.
- LESSON: Max: play safe + use logged-in cookies + never fully sleep, you own this backup.

## [2026-06-15 23:39] b9 46651386
- DID: ROOT CAUSE FOUND + FIXED: tamza YT backup failures were NOT a volume bot-wall. Bare yt-dlp on Lak = ancient 2023.03.04 (can't solve YouTube JS n-challenge -> thumbnails-only -> false 'walls'). Fix stack: split_backup.py now calls /home/mrempadmin/yt_backup_venv/bin/yt-dlp (2026.06.09) + --cookies yt_cookies.txt (Max Firefox login, scp'd to Lak) + --remote-components ejs:github + installed deno 2.8.3 to ~/.deno/bin + pace_controller.sh exports deno on PATH. Worker pid live, 720p .part downloading at full speed. Pacing wide-safe 600-1200s.
- STATE: Worker running with full recipe; first 720p file downloading. Keeper cron */5 active, drainer */10 active. 3 done of 1558.
- NEXT: Confirm first .mkv merges + that subsequent pulls keep succeeding (no real walls now). If solid, consider TIGHTENING pacing since the wall was never the real issue - could finish far under 2 weeks. Commit the repo copy of split_backup.py to match deployed.
- LESSON: When YT downloads fail/look walled, FIRST check yt-dlp version + JS-runtime (n-challenge); a stale yt-dlp masquerades as a bot-wall. deno+cookies+ejs:github is the modern unlock.

## [2026-06-16 07:43] b9 46651386
- DID: Tamza YT backup running clean overnight on the fixed recipe: 23 OK / 0 walls / 6 err since fix. 26 videos done+drained to Centauri (0 local mkv, drainer keeping up). Worker pid 80365 alive, fill57 clear.
- STATE: Wide-safe pacing 600-1200s is averaging ~18-20 min/video => ~21 days for all 1558 (too slow for Max's 1-2 week target). Walls are now ZERO so pacing can safely tighten. Max is BACK at 07:43.
- NEXT: Propose to Max: tighten pacing (e.g. 180-420s) to finish in days - the wall was never real, cookies+modern yt-dlp = 0 walls. Await his OK (he said play safe). Then edit pace_controller.sh gaps + worker auto-picks up.
- LESSON: Wide 10-20min pacing = ~3 weeks for 1558; safe to tighten now that root cause (stale yt-dlp) is fixed and walls are 0.

## [2026-06-16 08:07] b9 46651386
- DID: SCOPE CONFIRMED by Max: back up ALL of it - Tamza YouTube (1558: 936 videos+622 streams) AND Hucolo Odysee @hucolo (1167) = ~2725 total. Tamza backup FIXED+running clean: 27 done/0 walls overnight. Recipe in /home/mrempadmin/yt_backup/split_backup.py = venv yt-dlp 2026.06.09 (full path) + --cookies yt_cookies.txt (Max MAIN Firefox YT login, scp'd) + --remote-components ejs:github + deno 2.8.3 on PATH; keeper pace_controller.sh cron */5 (gaps 600-1200s), drainer cron */10 ships .mkv->Centauri D:\tamza_yt_full_backup\tamza_channel then writes .done.
- STATE: OPEN: (1) SAFETY FLAG pending Max - using his MAIN account cookies for bulk YT download risks an account/channel ban; watcher wants explicit override. Max said 'i need all finished' but hasn't explicitly accepted ban risk or chosen throwaway. (2) Hucolo/Odysee 1167 NOT started - Odysee has no YouTube-style login-ban risk, simpler. (3) Pacing wide=~3wk; Max may OK tightening to ~4-6 days.
- NEXT: Confirm cookie decision with Max (main+accept risk, or throwaway). Then optionally tighten Tamza pacing. Then build Hucolo/Odysee downloader (yt-dlp supports odysee.com/lbry; list @hucolo channel, same resumable .done pattern, separate outdir). Keep watch timer armed.
- LESSON: Hucolo=Odysee (LBRY), different platform from YouTube - no cookie/ban concern there; only the Tamza YouTube half has the main-account-cookie risk.

## [2026-06-16 08:07] b9 46651386
- DID: Max CONFIRMED the YT cookies are from 'maxrempel35' = disposable throwaway account, NOT his main channel. Safety flag CLEARED, posted watcher override. Tightening Tamza pacing 600-1200s -> 180-420s (faster, ~5-6 days) since no main-channel risk.
- STATE: Tamza backup running on throwaway cookies; pacing being tightened to 180-420s. 27 done/1558.
- NEXT: Restart worker to apply new gaps; then build Hucolo/Odysee downloader (1167).
- LESSON: Cookies are maxrempel35 throwaway - safe for bulk; only risk is the throwaway itself getting blocked, so keep pacing moderate not reckless.

## [2026-06-16 09:34] b9 46651386
- DID: STANDING ORDER from Max: report ETA for Tamza AND ETA for Hucolo on every status/hourly check. Tamza: 32/1558 done, measured rate ~5 videos/hr at safe pace -> remaining 1526 ~= 13+ days (streams are big/slow, so ~2-3 weeks realistic). Hucolo: 1167 on Odysee, NOT started, downloader not built yet -> ETA unknown until I start it and measure (Odysee slower than YT).
- STATE: Tamza backup running clean 0 walls. Hucolo pending. ETA reporting now a standing duty.
- NEXT: Each hourly wake: compute Tamza ETA from done-count delta + report; report Hucolo ETA (TBD until its downloader runs). Build Hucolo downloader as Tamza nears done.
- LESSON: Max wants ETAs reported continuously - bake ETA calc into every watch tick.

## [2026-06-16 09:39] b9 46651386
- DID: MAX PIVOT (explicit, emphatic): DOWNLOAD EVERYTHING FROM YOUTUBE. FORGET ODYSEE entirely - do NOT build any Odysee/LBRY downloader. Hucolo content is to be pulled from YouTube, not Odysee.
- STATE: Tamza YouTube backup running clean (32/1558, 0 walls). Odysee plan CANCELLED. If Hucolo has its OWN YouTube channel separate from the Tamza channel, enumerate it (yt-dlp --flat-playlist channel/videos) and append those ids to the YouTube backup queue (tamza_all.txt or a sibling list), same split_backup.py recipe + .done resumable pattern.
- NEXT: Confirm whether Hucolo = a separate YouTube channel or all within the existing 1558 Tamza list. If separate, enumerate + add to queue. Report ETA in YouTube-only terms.
- LESSON: FORGET ODYSEE - everything backs up from YouTube only. No Odysee/LBRY work.

## [2026-06-16 12:14] b9 46651386
- DID: Hourly watch: Tamza YouTube backup at 42/1558 done, 0 walls, worker alive at 600-1200s gaps, fill57 clear. Rate ~15min/video.
- STATE: Pipeline healthy and unattended. ETA Tamza ~July 2 (~15.5 days). Odysee cancelled - all from YouTube.
- NEXT: Awaiting Max's answer: is Hucolo a separate YouTube channel (need link to enumerate+append) or already in the 1558? Keep hourly watch + report Tamza/Hucolo ETA.

## [2026-06-16 12:19] b9 46651386
- DID: Found Hucolo TV channel @Hucolo (UCj5wGWloHE8hKHPd5kqWsJQ): 730 videos + 554 streams = 1284. Enumerated from Pine, scp'd ids to Lak, appended to tamza_all.txt queue (now 2842 unique: 1558 Tamza + 1284 Hucolo, no overlap).
- STATE: Single worker will finish Tamza then auto-continue into Hucolo on cron relaunch. 42 done, 2800 remaining. ~16 min/video, 0 walls.
- NEXT: Hourly watch continues. ETA Tamza ~July 3, everything (incl Hucolo) ~July 17.

## [2026-06-16 12:35] b9 46651386
- DID: Max accepted 4-min gap. Edited pace_controller.sh to --min-gap 180 --max-gap 300 (avg 240s), killed old 600-1200 worker, relaunched. Worker live on full 2842 queue.
- STATE: Gap now 4 min avg. 42 done, 2800 remaining. ~6 min/video real cycle.
- NEXT: ETA Tamza ~June 23, everything ~June 28 (~12 days). Sync pace_controller change to repo+push. Keep hourly watch.

## [2026-06-16 12:54] b9 46651386
- DID: Split teal16 backup by channel: Hucolo -> hucolo_channel, Tamza -> tamza_channel. Edited drainer.sh to route by hucolo_all_ids.txt (1284 ids). Both remote folders created on Centauri D:\tamza_yt_full_backup, drainer ran clean.
- STATE: Pipeline live: 4-min gap, 2842 queue, channel-split drain, 0 walls. Verified teal16 separate from Odysee sync.
- NEXT: Hourly watch. ETA Tamza ~June 23, all ~June 28.

## [2026-06-16 12:57] b9 46651386
- DID: Max: report every 30 min (not hourly). Track walls strictly SINCE the 4-min change only (worker START 2026-06-16 12:34:57, gap 180-300s). Method: find last 'START pid=' line in out/backup.log, count OK/WALL/ERR in that segment.
- STATE: Since change: 4 OK, 0 WALL (too small to conclude, need hours). 17 walls total are OLD broken-method, pre-fix. 47 done overall of 2842.
- NEXT: Re-arm 30-min timer each fire; report post-change wall ratio + ETA (Tamza ~June 21, all ~June 26).

## [2026-06-16 13:59] b9 46651386
- DID: 30-min watch: since 4-min change (12:34) 9 OK / 0 WALL / 0 ERR. Worker alive, actively pulling big streams. Real rate settling ~7-8 min/video (big streams dominate, not the gap).
- STATE: 52/2842 done. New timing safe so far (0 walls in 85-min post-change window). Adopt TMS format in TLDRs per b15B.
- NEXT: Re-arm 30-min. ETA Tamza ~June 24, all ~June 30 (slower than June-26 guess bc streams are large).

## [2026-06-16 14:29] b9 46651386
- DID: 30-min watch: since 4-min change 14 OK / 0 WALL over ~2hrs. Rate ~8 min/video. Worker alive.
- STATE: 55/2842 done. New 4-min timing validated safe (14 videos, 0 walls). Sibling song-timing broadcasts are unrelated, ignored.
- NEXT: Re-arm 30-min. ETA Tamza ~June 24, all ~June 30.

## [2026-06-16 15:00] b9 46651386
- DID: 30-min watch 15:00: since 4-min change 19 OK / 0 WALL / 0 ERR (~2.4 hrs). Worker alive. Rate ~8 min/video.
- STATE: 60/2842 done. 4-min timing holding safe, zero walls. Pipeline fully autonomous (worker+drainer cron, channel-split to teal16).
- NEXT: Re-arm 30-min. ETA Tamza ~June 24, all ~June 30. RESUME NOTE for cold session: read this worklog; pipeline self-runs on Lak, just keep 30-min watch + report post-change wall ratio.

## [2026-06-16 16:02] b9 46651386
- DID: 16:02 watch: since 4-min change 28 OK / 0 WALL. 71/2842 done. Posted bcast clarifying b9=FULL VIDEO backup (not captions); b7f/b7nonhtimes own NONH caption crawl on same home IP. Coexisting, 0 walls; offered to pause my puller if their crawl hits 429.
- STATE: Pipeline autonomous, 4-min timing safe. SHARED-IP risk noted (my video puller + their caption crawl both on home WAN via Lak).
- NEXT: Re-arm 30-min. ETA Tamza ~June 24, all ~June 30. If walls appear, suspect combined-IP load - coordinate w/ b7f.

## [2026-06-16 16:33] b9 46651386
- DID: 16:33 watch: since 4-min change 33 OK / 0 WALL (~4 hrs). 75/2842 done. Worker alive.
- STATE: 4-min timing solidly safe. Pipeline fully autonomous on Lak (worker+drainer cron, channel-split drain to teal16). Coexisting w/ sibling caption crawlers on same home IP, no walls.
- NEXT: Re-arm 30-min. ETA Tamza ~June 24, all ~June 30. COLD-SESSION RESUME: pipeline self-runs; just check post-START-line OK/WALL in out/backup.log every 30min, report TMS TLDR.

## [2026-06-16 17:05] b9 46651386
- DID: 30-min tick 17:05: post-change OK=38 WALL=0, worker pid139557 alive, 81/2842 done
- STATE: 4-min gap validated safe ~4.5hrs (38 vids, 0 walls). Drain-by-channel live (tamza_channel/hucolo_channel on teal16).
- NEXT: Re-arm 30-min watch loop. Watch for walls; if any, suspect combined home-IP load w/ sibling caption crawlers, offer to pause puller.

## [2026-06-16 17:36] b9 46651386
- DID: 30-min tick 17:36: post-change OK=42 WALL=0, worker alive, 85/2842 done
- STATE: 4-min gap holding safe ~5hrs (42 vids, 0 walls). Channel-split drain live.
- NEXT: Re-arm 30-min watch. Watch walls; pause puller if combined home-IP load trips one.

## [2026-06-16 18:07] b9 46651386
- DID: 30-min tick 18:07: post-change OK=45 WALL=0, worker alive, 88/2842 done
- STATE: 4-min gap holding safe ~5.5hrs (45 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-16 18:38] b9 46651386
- DID: 30-min tick 18:38: post-change OK=49 WALL=0, worker alive, 92/2842 done
- STATE: 4-min gap holding safe ~6hrs (49 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-16 19:09] b9 46651386
- DID: 30-min tick 19:09: post-change OK=52 WALL=0, worker alive, 95/2842 done
- STATE: 4-min gap holding safe ~6.5hrs (52 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-16 21:08] b9 46651386
- DID: tick 21:08 (laptop slept ~2hr, 1st MCP timed out): post-change OK=66 WALL=0, 109/2842 done
- STATE: 4-min gap holding safe (66 vids, 0 walls). Worker alive - downloads advancing; pgrep-DOWN was false-neg from wrong flag.
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-17 06:27] b9 46651386
- DID: tick 06:26 (overnight, laptop slept ~9hr): post-change OK=154 WALL=0, worker alive, 197/2842 done
- STATE: 4-min gap proven robustly safe overnight (154 vids, 0 walls). Lak pipeline ran server-side regardless of laptop sleep.
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-17 06:58] b9 46651386
- DID: tick 06:58: post-change OK=160 WALL=0, worker alive, 203/2842 done
- STATE: 4-min gap robustly safe (160 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-17 07:29] b9 46651386
- DID: tick 07:29: post-change OK=166 WALL=0, worker alive, 209/2842 done
- STATE: 4-min gap robustly safe (166 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-17 07:59] b9 46651386
- DID: tick 08:00: post-change OK=172 WALL=0, worker alive, 215/2842 done
- STATE: 4-min gap robustly safe (172 vids, 0 walls).
- NEXT: Re-arm 30-min watch. Watch walls.

## [2026-06-17 08:10] b9 46651386
- DID: tick 08:10 + cadence change to 180min per Max: OK=173 WALL=0, 216/2842 done
- STATE: Switched watch from 30-min ScheduleWakeup to 3-hourly cron c157826e (sentinel autonomous-loop). Self-wake caps at 60min so cron used for 3hr cadence. Pipeline rock-solid 173/0.
- NEXT: Cron fires every 3h at :13. Stopped re-arming ScheduleWakeup (dynamic loop ends).

## [2026-06-17 09:27] b9 46651386
- DID: Named the backup system 'ytdow'; wrote ytdow_method_v01_tomemex.md + global2 section w/ NO-CIRCUMVENT rule (committed dafdbde7)
- STATE: Rule targets other sessions trying their own yt-dlp on big videos over the home IP = trips bot-wall, breaks ytdow. One puller per home IP.
- NEXT: 3-hourly cron c157826e watches backup. Next check ~11:13.

## [2026-06-17 09:43] b9 46651386
- DID: cron tick 09:43: post-change OK=189 WALL=0, worker alive, 232/2842 done
- STATE: ytdow rock-solid (189 vids, 0 walls). 3-hourly cron working.
- NEXT: Cron fires every 3h. Re-create cron ~Jun 24 (7-day expiry).

## [2026-06-17 12:43] b9 46651386
- DID: cron tick 12:43: post-change OK=214 WALL=0, worker alive, 257/2842 done
- STATE: ytdow rock-solid (214 vids, 0 walls). 3-hourly cron confirmed proper spacing.
- NEXT: Cron fires every 3h. Re-create cron ~Jun 24.

## [2026-06-17 14:35] b9 46651386
- DID: Priority pass LIVE: 93 caption-disabled Tamza vids now run FIRST in ytdow (pace_controller rewired, worker pid270107 switched, 80/93 remaining). Committed 7a4b1b32. Cadence -> 5mt during discussion.
- STATE: All 720p mkv. Worker auto-falls back to full queue when 93 drain. Confirmed to b7f; offered audio-only-to-Sol staging.
- NEXT: Watch every 5min while discussing; revert to 120mt (2h cron) when Max says discussion done.

## [2026-06-17 14:58] b9 46651386
- DID: Priority pass progressing: 16/93 done (77 left), worker on priority93, 0 walls. 5-min watch cadence active during discussion.
- STATE: ytdow priority93 healthy. Sol off-limits for ASR during RAM tests so 93 just need to reach teal16 (no rush). Awaiting Max: rush-gap? + discussion-done->120mt.
- NEXT: Keep 5min watch until Max says done, then 120mt (2h cron).

## [2026-06-17 15:24] b9 46651386
- DID: Reviewed B25handoverer's TAMZA_HANDOVER_START_HERE_v01 for my (b9/ytdow) part; posted corrections to board
- STATE: ytdow healthy: 281/2842 backed up to teal16, priority-93 at 19/93, 0 walls; worker pid 270107 on priority93.txt, big stream Dd2q4jee26E mid-download
- NEXT: Keep 5mt watch (timer armed 15:28) until Max says discussion done, then switch to 120mt via CronCreate

## [2026-06-17 15:56] b9 46651386
- DID: 5mt watch on ytdow priority-93 pass; advancing steadily at the safe 4-min gap
- STATE: priority93 at 25/93, worker pid alive, 0 walls all session; full 720p videos landing on teal16
- NEXT: Keep 5mt until Max says discussion done, then 120mt via CronCreate; held Qs: rush-gap? / discussion-done?

## [2026-06-17 16:22] b9 46651386
- DID: 5mt watch continuing on ytdow priority-93; verified two long gaps were just large videos (Dd2q4jee26E, mGQ0yZO5oIs 1.3GB) downloading, not stalls
- STATE: priority93 ~28/93, worker alive, 0 walls entire session; pace steady at safe 4-min gap
- NEXT: Keep 5mt until Max says discussion done -> then 120mt via CronCreate; held Qs: rush-gap? / discussion-done?

## [2026-06-17 16:52] b9 46651386
- DID: Continuing 5mt watch on ytdow priority-93 pass
- STATE: priority93 at 31/93, worker alive, 0 walls all session; b7nonhtimes disarmed, will wake-by-name when 93 land on teal16 AND Sol cleared to run ASR
- NEXT: Keep 5mt until Max says discussion done -> 120mt via CronCreate; at 93/93 completion wake b7nonhtimes

## [2026-06-17 17:22] b9 46651386
- DID: 5mt watch on ytdow priority-93 ongoing; several long gaps all confirmed = large 1GB+ videos (mGQ0yZO5oIs, UC4u6bbZALg) downloading, not stalls
- STATE: priority93 at 34/93, worker alive, 0 walls entire session; ~36% of the 93 done
- NEXT: Keep 5mt until Max says discussion done -> 120mt via CronCreate; wake b7nonhtimes at 93/93 if Sol cleared

## [2026-06-17 17:48] b9 46651386
- DID: 5mt watch on ytdow priority-93 steady; all long gaps confirmed = large 1GB videos downloading
- STATE: priority93 at 38/93 (~41%), worker alive, 0 walls entire session, ~1 vid per 5min at safe 4-min gap
- NEXT: Keep 5mt until Max says discussion done -> 120mt CronCreate; wake b7nonhtimes at 93/93 if Sol cleared

## [2026-06-17 18:10] b9 46651386
- DID: 5mt watch ytdow priority-93 ongoing, healthy
- STATE: priority93 at 41/93 (~44%), worker alive, 0 walls all session; many vids are 1GB so some 10-min gaps are normal big downloads
- NEXT: Keep 5mt until Max says discussion done -> 120mt CronCreate; wake b7nonhtimes at 93/93 if Sol cleared

## [2026-06-17 18:34] b9 46651386
- DID: Watched ytdow 93-vid priority pass on 5mt loop: 42/93 done, worker alive, 0 walls all session
- STATE: Healthy; 1 vid per ~5min at safe 4-min gap; large vids (1.1GB, 645MB) download normally
- NEXT: Continue 5mt watch until Max says discussion done, then switch to 120mt via CronCreate

## [2026-06-17 18:56] b9 46651386
- DID: ytdow 93-vid priority pass advancing steadily on 5mt watch: 47/93, worker alive, 0 walls all session
- STATE: Healthy; ~1 vid per 4-6min at safe 4-min gap; past halfway
- NEXT: Continue 5mt watch until Max says discussion done, then 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR-from-teal16

## [2026-06-17 19:20] b9 46651386
- DID: ytdow 93-vid pass: 49/93, worker alive, 0 walls all session; big vids (962MB) drain fine
- STATE: Healthy; ~1 vid/5min at safe 4-min gap; flat counts always = large vid download or pacing gap, never a stall
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 19:41] b9 46651386
- DID: ytdow 93-vid pass: 53/93, worker alive, 0 walls all session
- STATE: Healthy; steady ~1 vid/4-6min; flat counts = large vid download or pacing gap, verified each via .part
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 20:02] b9 46651386
- DID: ytdow 93-vid pass: 57/93, worker alive, 0 walls all session
- STATE: Healthy; steady ~1 vid/4-6min at safe 4-min gap
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 20:24] b9 46651386
- DID: ytdow 93-vid pass: 61/93 (2/3 done), worker alive, 0 walls all session
- STATE: Healthy; steady ~1 vid/4-6min at safe 4-min gap; ~32 left
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 20:46] b9 46651386
- DID: ytdow 93-vid pass: 63/93, worker alive, 0 walls all session; 1.66GB vid drained clean
- STATE: Healthy; ~30 left; steady ~1 vid/4-6min at safe 4-min gap
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 21:08] b9 46651386
- DID: ytdow 93-vid pass: 67/93, worker alive, 0 walls all session
- STATE: Healthy; ~26 left; steady ~1 vid/4-6min at safe 4-min gap
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 21:32] b9 46651386
- DID: ytdow 93-vid pass: 70/93, worker alive, 0 walls all session
- STATE: Healthy; 23 left; steady ~1 vid/4-6min at safe 4-min gap
- NEXT: Continue 5mt watch until Max says discussion done -> 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 22:01] b9 46651386
- DID: ytdow priority-93 tick: 74/93 done, worker alive, 0 walls; next vid 2wWS7xu-NW4 downloading healthy
- STATE: 5mt watch loop active per Max; safe 4-min gap, ~1 vid/4-6min
- NEXT: keep 5-min watch until Max says discussion done, then switch to 120mt via CronCreate

## [2026-06-17 22:24] b9 46651386
- DID: ytdow priority-93: 78/93, worker alive, 0 walls; EwoDzl5ItsM is a large vid (video stream done, now pulling audio f251) - count flat is that one big download
- STATE: 5mt watch loop active per Max; safe 4-min gap; 15 to go
- NEXT: keep 5-min watch until Max says discussion done, then 120mt via CronCreate

## [2026-06-17 22:48] b9 46651386
- DID: ytdow priority-93: 82/93, worker alive, 0 walls; big vid qHhMFocy-Bo (931MB) drained fine
- STATE: 5mt watch loop active per Max; safe 4-min gap; 11 to go
- NEXT: keep 5-min watch until Max says discussion done, then 120mt via CronCreate; at 93/93 wake b7nonhtimes for ASR

## [2026-06-17 23:13] b9 46651386
- DID: ytdow priority-93: 84/93, worker alive, 0 walls; ASR now running on Sol (b7, PID27020) pulling 82 ready mkv from teal16 NOT youtube; DMh2cWsiAtE big vid downloading
- STATE: 5mt watch active; B26 overnight mgr; my order=finish last 9 + keep ytdow healthy
- NEXT: drain final 9 (HB8j6T GhQH pVmmUs FM_GD xsORw hNT4 DMh2 SBBc FD2FB); post when 93/93 so b7 tops up vids.txt

## [2026-06-17 23:37] b9 46651386
- DID: ytdow priority-93: 88/93, worker alive, 0 walls; 5 left to pull
- STATE: 5mt watch; B26 overnight mgr; ASR running on Sol from teal16
- NEXT: drain final 5 (HB8j6T GhQH FM_GD SBBc FD2FB); post 93/93 to board so b7 tops up vids.txt; then worker auto-falls-back to tamza_all.txt

## [2026-06-17 23:58] b9 46651386
- DID: ytdow: 92/93 priority done (last=HB8j6T_FF4Y pulling), 0 walls; Max said continue full backup after 93
- STATE: worker still on priority93.txt; pace_controller auto-switches to tamza_all.txt when last prio lands; tamza_all 353/2842
- NEXT: confirm 93/93 + auto-fallback engaged, then steward full backup to completion (ETA Tamza ~Jun24, all ~Jun30); widen cadence after transition

## [2026-06-18 00:03] b9 46651386
- DID: ytdow MILESTONE: 93/93 priority caption-disabled pass COMPLETE, 0 walls; all on teal16; b7 ASR fully unblocked
- STATE: worker still on priority93.txt (queue drained); pace_controller cron */5 will flip to tamza_all.txt; tamza_all 354/2842; Max ordered continue full backup
- NEXT: confirm fallback worker starts on tamza_all, then widen to ~30min overnight cadence; steward full backup ETA Tamza ~Jun24 all ~Jun30

## [2026-06-18 01:10] b9 46651386
- DID: ytdow: 93/93 priority DONE 0 walls; auto-fallback confirmed clean - worker flipped to tamza_all.txt 00:05 (todo=2488); full backup running 355/2842; Max said good night, continue full backup
- STATE: overnight 30-min watch cadence; full backup self-sustains on Lak pace_controller cron */5 + drainer */10
- NEXT: monitor full backup to completion (Tamza ~Jun24, all ~Jun30); just confirm worker alive + 0 walls each 30min; B26 is overnight team mgr

## [2026-06-18 02:45] b9 46651386
- DID: Overnight ytdow watch tick: full Tamza queue 382/2842, 0 walls, worker alive on tamza_all.txt
- STATE: 93 priority pass complete+drained; full 2842 backup stewarding at 30-min cadence on Lak cron
- NEXT: Keep 30-min watch; confirm worker alive + 0 walls each tick; re-arm ScheduleWakeup 1800s

## [2026-06-26 09:53] b9 46651386
- DID: ytdow full backup 2334/2842, 3 old healed walls (>15h, 380 clean since). Added timestamp to 3-hourly cron reports (job aec2c0c6). Max approved: vocalize only if walls CLIMB (suspicious - many in a row, OKs stopping)
- STATE: Backup ~82% done, ETA all ~Jun27-28; 3-hourly cron drives old-format timestamped reports; worker self-heals on Lak
- NEXT: Each cron tick: status + report; vocalize if walls climb past ~5-in-a-row with no recovery

## [2026-06-28 21:36] b9 46651386
- DID: ytdow COMPLETE: 2842/2842 Tamza+Hucolo videos downloaded 720p + drained/size-verified to teal16 (2842 .done sentinels). 0 remaining, final 3 stragglers landed. Run had only self-healed walls, 0 critical.
- STATE: Backup DONE. Lak pace_controller still no-op-spawning every 5min; drainer cron */10 still on; my 3h report cron + 30min timer still running on a finished job. Awaiting Max's word to stand down.
- NEXT: If Max says stand down: CronDelete the report cron + stop timer + disable Lak pace_controller cron. Else keep light watch 1 day for teal16 spot-check.

## [2026-07-02 08:11] ? 46651386
- DID: Built ytdow self-refresh: refresh_queue.py scrapes both channels (Tamza+Hucolo videos+streams) via proxy twice-weekly (Lak cron Mon+Thu 04:37), appends new ids to tamza_all.txt. Tested live: added 9 new videos, 0 corruption. Mirrored to repo + method doc + infra_map, pushed master 0434722d. Recovered Hucolo channel id UCj5wGWloHE8hKHPd5kqWsJQ.
- STATE: ytdow COMPLETE (2842 orig on teal16 ~Jun28) + now self-sustaining via refresh_queue; worker+drainer crons pull new uploads hands-off
- NEXT: Light watch; only alarm if walls CLIMB; refresh runs itself

## [2026-07-03 06:10] ? 46651386
- DID: Delivered channel_inventory.json to b15merger (729 rows, 676 dated, committed 9d88b1c1) via proxy per-video extract - zero home-IP hit. Also flagged B10A's Odysee re-download risk (they pivoted to upload-from-teal16).
- STATE: ytdow COMPLETE + self-refreshing (refresh_queue twice-weekly); all deliverables done; Max asked to slow down a lot
- NEXT: Minimal cadence: 3-hourly report cron only, no frequent ScheduleWakeup loop; stay force-wakeable; refresh runs itself Thu 04:37
