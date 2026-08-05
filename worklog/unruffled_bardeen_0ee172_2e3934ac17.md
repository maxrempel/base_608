
## [2026-07-02 11:16] ? 952a7763
- DID: B10A: task = throttled upload of MISSING Tamza/Hucolo videos to Odysee @tamza. Investigated existing design on Centauri via SSH.
- STATE: EXISTING: OdyseeSync.exe (C:\Users\maxre\Downloads\, PID1908, workdir D:\odysee_sync) auto-mirrors YT->Odysee, RE-DOWNLOADS from YT then zips (uploads\*.zip) + publishes. Only 284/1591 Tamza done since 2026-06-05. Downloaded backup SAFE at D:\tamza_yt_full_backup (1584 tamza+1266 hucolo, teal16). Posted design+red-flag to board (JOINT), NOT building yet.
- NEXT: Await board/Max verdict on: (a) throttle via Windows QoS on OdyseeSync.exe vs build direct lbrynet/API publisher fed from teal16 (avoids 2nd YT puller / bot-wall violation); (b) confirm % = uplink; then build daily speedtest recalibration + 00:00 night-60% / 06:00 day-25% / start-30% throttle.

## [2026-07-02 11:51] ? 952a7763
- DID: Built+deployed+tested odysee_throttle.ps1 on Centauri (QoS cap on OdyseeSync.exe: start-slow30/day25/night60, daily Ookla recalib, rolling-max capacity). SYSTEM scheduled task 'OdyseeThrottle' every 30min. Committed+pushed to master. Presented design+status to board (joint).
- STATE: Throttle LIVE: 39.7Mbps uplink -> 11.9Mbps start-slow cap applied. teal16 backup read-only/untouched. Not yet witnessed cap biting mid-upload (OST was idle at test). Open board question: does OST re-pull YT (feed-local infeasible so far); I lean accept-as-is.
- NEXT: Check board for replies; sample Centauri NIC egress during an OST upload burst to confirm cap bites; tick timer_decel + re-arm.

## [2026-07-02 12:55] ? 952a7763
- DID: b10a Odysee direct-uploader: throttle live on Centauri; computed 292-missing set auth-free (public claim_search); logged into Odysee as max@tamza.com via Bitwarden (persists in Playwright profile), confirmed @tamza ownership + wallet unlocked + full publish API. Consulted b9 (ytdow owner) - aligned: upload from teal16, retire OST, zero YouTube. auth_token saved zSyncMain/ssh/odysee_auth_token_20260702.txt.
- STATE: READY to build uploader. Missing files: D:\tamza_yt_full_backup\tamza_channel\<ytid>.mkv, 352GB, skip 0-byte. Titles from inventory tamza_videos/streams/shorts.txt (id|dur|title). API: na-backend proxy, header x-lbry-auth-token, channel_id 77c3f0e99e538c6ea98597ade56b81a7f5cafe85. Tool folder C:\claude_base\tools\odysee_throttle.
- NEXT: Reopen Playwright (still logged in), do ONE real UI upload of a small verified-Tamza missing video capturing browser_network_requests to learn tus-upload+publish payloads; reproduce as Centauri python uploader (resumable, skip 0-byte, YT link in desc, throttle); 1 upload->verify->batch 292.

## [2026-07-03 17:07] ? 952a7763
- DID: b10a: reverse-engineered Odysee publish API via captured web upload (tus + stream_create); 1st video LIVE on @tamza via API. Built odysee_upload.py on Centauri with THROTTLE BAKED IN (token-bucket on upload bytes, reads capacity from throttle state, day25/night60/startslow30). Recalibration now every 4h (Max asked). Fixed BOM (utf-8-sig) + tus create_url (405) bugs. Throttle verified reading 9.9Mbps DAY cap.
- STATE: Testing 1 throttled upload on Centauri now (bg task). Uploader: D:\zScripts\monitoring\odysee_upload.py; ledger odysee_upload_ledger.jsonl; missing_with_titles.tsv (272/292 have titles). auth token synced to Centauri D:\Nextcloud\zSyncMain\ssh\odysee_auth_token_20260702.txt. 291 missing remain (1 done via browser).
- NEXT: Confirm test upload publishes + measure actual throttled Mbps; then run full batch (resumable, skip-0byte, no-dup via resolve); retire OdyseeSync.exe; re-point/retire the OST QoS policy.

## [2026-07-03 17:55] ? 952a7763
- DID: b10a: Odysee direct uploader LIVE + RUNNING as Centauri task OdyseeUpload (hourly-resumable). Throttle baked into uploader (token-bucket on bytes, capacity from state recalib 4h, day25/night60/startslow30). 3 test videos published OK; batch now uploading a 1.5GB titled file at throttled rate. No-dup via resolve; ledger jsonl; 0-byte skipped; no-title (~20) deferred to odysee_needs_title.txt. Code committed+pushed.
- STATE: Batch healthy, egress ~throttled. Pending cleanup: (a) 2 test claims with wrong titles ZoHpi342TRQ + gg_L-_674uE (fix via stream_update or abandon+redo); (b) ~20 no-title videos need titles (mkv has no title tag, not in 6/12 inventory) - asked b9/ytdow; (c) retire OdyseeSync.exe carefully (has odysee_sync_watch healthcheck that'd false-alarm + Startup shortcut + QoS policy; KEEP throttle.ps1 task for capacity recalib).
- NEXT: Monitor batch (log tail + ledger); get 20 titles from b9; fix 2 titles; retire OST w/o tripping its watcher. Baseline @tamza claims=1330, target ~1600.

## [2026-07-03 21:34] ? 952a7763
- DID: b10a BLOCKER: Odysee wallet out of spendable LBC. wallet_balance: available=0.0008, reserved=4.558 (claims 4.327 locked in ~1339 existing videos). Each publish needs 0.001 bid -> InsufficientFundsError after ~9 videos. DISABLED task OdyseeUpload to stop wasting bandwidth (was uploading GB files then failing publish). ~9 published OK + 2 test titles fixed (ZoHpi342TRQ, gg_L-_674uE now correct). @tamza claims 1339.
- STATE: BLOCKED on wallet funding. Need ~0.3-0.5 LBC spendable for 272 videos. Options: fund wallet (Max decision - money), or lower bid (0.0008 avail only ~8 videos even at 0.0001, insufficient), or free reserved LBC by lowering existing-claim bids (heavy/risky). Uploader + throttle proven working; only funds block. needs_title=18/20, asked b9. OdyseeSync retirement still pending.
- NEXT: Await Max on LBC funding; research cheapest LBC acquisition + get wallet receive address (address_unused). Once funded: re-enable OdyseeUpload task. Then 20 titles + OST retirement.

## [2026-07-04 07:09] ? 952a7763
- DID: b10a BLOCKER RESOLVED FREE: claimed Odysee 'referrer' reward (1.0 LBC) via api.odysee.com/reward/new -> wallet available now 1.000797 LBC (was 0.0008). Covers all 272 remaining (0.001 bid). No Max money. Re-enabled + started OdyseeUpload task. Wallet receive addr bSxx6RB4AasAd4GE3F56JPy59J6Aq5jCVf. Other rewards (subscription/weekly_watch/subscribers/many_downloads=0.13) locked behind activity conditions.
- STATE: Batch RUNNING again with funds. 2 test titles fixed. ~9 published pre-blocker. b9 not yet replied w/ 20 titles. OST retirement pending.
- NEXT: Verify publishes now succeed (ledger grows, no InsufficientFunds in log); let batch run ~4-5 days; feed 20 titles when b9 replies; retire OdyseeSync carefully (disable its watcher first).

## [2026-07-04 07:50] ? 952a7763
- DID: b10a: batch PUBLISHING again post-funding (PUBLISHED -Y8QG8odOOU real claim, 0 InsufficientFunds since 07-04). Added pre-flight+periodic wallet guard to uploader (deployed, committed+pushed). RETIRED OdyseeSync: process stopped, centauri-odysee-watch task DISABLED, Healthchecks check 6dcbc67d (centauri-odysee-sync) PAUSED via API, Startup shortcut moved to D:\zScripts\retired_startup. Kept OdyseeThrottle task = uploader's 4h capacity recalib (QoS inert).
- STATE: Batch running (task OdyseeUpload). Wallet ~1.0 LBC avail. Guard prevents future fund-waste. OST fully retired + no more false alarms. Remaining: 20 no-title videos (b9 not replied). hc check 6dcbc67d paused not deleted.
- NEXT: Monitor batch over ~4-5 days (ledger grows, claims climb 1339->~1600, wallet stays >0.05); feed 20 titles when b9 replies; optionally delete paused hc check + update infra_map.

## [2026-07-04 08:34] ? 952a7763
- DID: b10a routine: batch healthy - ledger 9, @tamza 1341 claims, wallet 0.998 LBC, 0 fund errors, throttled ~7.5Mbps, task Running. Early files are big livestreams (slow per-file, on track). OST retirement holding. b9 silent on 20 titles (~14h).
- STATE: All green, self-running. 20 no-title deferred (low priority, no urgency). Slowing monitoring cadence to ~hourly.
- NEXT: Hourly-ish health checks over the multi-day run; escalate 20 titles to Max if b9 stays silent another day; watch wallet>0.05.

## [2026-07-04 09:26] ? 952a7763
- DID: b10a hourly: healthy, ledger 12, 0 fund errors, throttled ~8.8Mbps, task Running. Still on big livestreams. b9 silent ~15h on 20 titles (not yet 1 day).
- STATE: All green, self-running.
- NEXT: Continue ~hourly checks; escalate 20 titles to Max if b9 silent past ~1 day; watch wallet>0.05.

## [2026-07-04 10:27] ? 952a7763
- DID: b10a hourly: healthy, ledger 14, 0 errors/fund issues, throttled ~8.9Mbps, task Running. On big livestreams. b9 silent ~16h on 20 titles.
- STATE: All green, self-running.
- NEXT: Hourly checks; escalate 20 titles to Max if b9 silent past ~1 day (after 2026-07-04 18:00); wallet was 0.998, plenty.

## [2026-07-04 11:29] ? 952a7763
- DID: b10a hourly: healthy, ledger 17, 0 problems, ~8.4Mbps, Running. b9 silent ~17h.
- STATE: Green.
- NEXT: Hourly; escalate 20 titles after 2026-07-04 18:00 if b9 silent.

## [2026-07-04 12:30] ? 952a7763
- DID: b10a hourly: healthy, ledger 19, task Running, ~8.2Mbps. 1 transient read-timeout error (1pqSWn_ih7k) - not fund-related, not ledgered, will auto-retry. 0 fund issues. b9 silent ~18h.
- STATE: Green; occasional transient timeouts expected + self-retried.
- NEXT: Hourly; escalate 20 titles after 2026-07-04 18:00 if b9 silent; wallet plenty.

## [2026-07-04 13:31] ? 952a7763
- DID: b10a hourly: healthy, ledger 22, 0 fund issues, ~9Mbps (at cap), Running. b9 silent ~19h.
- STATE: Green.
- NEXT: Hourly; escalate 20 titles after 2026-07-04 18:00 if b9 silent.

## [2026-07-04 14:33] ? 952a7763
- DID: b10a hourly: healthy, ledger 25, 0 fund issues, Running. Files getting smaller (past biggest livestreams). b9 silent ~20.5h.
- STATE: Green.
- NEXT: Hourly; escalate 20 titles after 2026-07-04 18:00 if b9 silent.

## [2026-07-04 15:35] ? 952a7763
- DID: b10a hourly: healthy, ledger 27, 0 fund issues, Running. b9 silent.
- STATE: Green.
- NEXT: Hourly; escalate 20 titles after 2026-07-04 18:00 if b9 silent.

## [2026-07-04 16:36] ? 952a7763
- DID: b10a hourly: healthy, ledger 31 (+4), 0 fund issues, Running. Smaller files now moving fast. Asked Max (green Q) whether OK to run single yt-dlp --flat-playlist for 20 no-title titles (b9 silent ~22h).
- STATE: Green; awaiting Max on flat-playlist decision for 20 titles.
- NEXT: Hourly checks; if Max says OK -> run flat-playlist, extract 20 titles, add to missing_with_titles.tsv, redeploy so they publish.

## [2026-07-04 17:38] ? 952a7763
- DID: b10a hourly: healthy, ledger 35 (+4), 0 fund issues, Running. Max/b9 silent on 20-title flat-playlist Q - keep deferring.
- STATE: Green.
- NEXT: Hourly; run flat-playlist for 20 titles ONLY if Max says yes.

## [2026-07-04 18:39] ? 952a7763
- DID: b10a hourly: healthy, ledger 37, 0 fund issues, Running. Max silent on 20-title Q.
- STATE: Green.
- NEXT: Hourly; flat-playlist for 20 titles only on Max yes.

## [2026-07-04 19:40] ? 952a7763
- DID: b10a hourly: healthy, ledger 38, 0 fund issues, Running. Max silent on 20-title Q.
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes.

## [2026-07-04 20:41] ? 952a7763
- DID: b10a hourly: healthy, ledger 41, 0 fund issues, Running.
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes.

## [2026-07-04 21:42] ? 952a7763
- DID: b10a hourly: healthy, ledger 44, 0 fund issues, Running.
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes; night mode (60%) at midnight.

## [2026-07-04 22:43] ? 952a7763
- DID: b10a hourly: healthy, ledger 46, 0 fund issues, Running.
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes.

## [2026-07-04 23:44] ? 952a7763
- DID: b10a hourly: healthy, ledger 48, 0 fund issues, Running.
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes.

## [2026-07-05 00:45] ? 952a7763
- DID: b10a hourly: healthy, ledger 49, 0 fund issues, Running (night mode, ~10Mbps server-limited).
- STATE: Green.
- NEXT: Hourly; flat-playlist only on Max yes.

## [2026-07-05 22:38] ? 952a7763
- DID: Set Odysee uploader throttle to 25% around the clock (PCT_DAY/NIGHT/START_SLOW all 0.25 in D:\zScripts\monitoring\odysee_upload.py on Centauri) per Max - Liz needs internet at night too. Restarted OdyseeUpload task; resumed cleanly from ledger.
- STATE: Batch RUNNING, capacity 39.7Mbps, rate 9.9Mbps (25%), mode reads DAY/NIGHT but both now 25%. ledger_done=103 of 272. Wallet 0.87 LBC ok. @tamza ~1412 claims.
- NEXT: Monitor to completion (~169 left, several days at 25%). Still owe: 20 no-title videos + spot-check Cyrillic titles render correctly + retire OdyseeSync.exe leftovers.
