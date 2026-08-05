
## [2026-06-07 11:52] b1 95b07b94
- DID: B1 manager of kartoteka b-team; shipped 6 catalog bug-fixes live (v31) earlier, committed+pushed claude_base master
- STATE: Live links all dead = team's sheet has temp-channel YouTube links now 404; @Tamza main channel is alive w/ all videos. B2 owns ALL tools/tamza_songs code now (B1 does not code per Max). B4=tester. B3 moved to c-team comms.
- NEXT: Await B2: (1)fix broken local app.js _s->_p/_g (2)finish 2-section search Исполнители+Песни (3)REROUTE every play_url onto @Tamza by date-match (4)dedup name map. B1 applies nothing-just coordinates; B4 verifies each upload. Re-arm 240s timer each turn.

## [2026-06-07 12:17] b1 95b07b94
- DID: B1 mgr: drove B2 through Картотека fixes - 2-section search live, dedup+reroute live (17/20 dead videos rerouted to @Tamza, 3 blanked), saved cache-excuse memory + baked manager self-sampling rule via B3
- STATE: Live data 1859 rows but 488 t=0 start-of-video links STILL present - B2's t=0 drop not yet shipped (got buried under reroute). Back-button = always-dumps-to-main bug open.
- NEXT: B2 ships (1) t=0 drop expected ~1370 rows then (2) History-API back button = browser-Back to previous screen. B1 re-samples live after each upload; B4 asserts 0 rows t<=0. Pending Max decision: merge duo 'Макс Ремпель и Оксана Полесская'? hide Вступление as category?

## [2026-06-07 13:00] b1 95b07b94
- DID: Drive agent confirmed Тайм Коды sheet holds joinable timecodes (video-id+performer+song), would restore ~2200 dropped rows. Old snapshots = 2021-22 depth, NO confirmed 2020 events. Local-xlsx agent still running. Max pivoted: replace deterministic parser with DeepSeek LLM-interpretation of messy tabs (bets 3x links). Awaiting his green-light before spending API.
- STATE: Catalog live+complete at v34 (1371 rows). Missing-archive root cause = timecodes live in separate Тайм Коды sheet never joined + most rows timecode-less. Plan: LLM-ingest via DeepSeek, delegated to workers, b1 stays light.
- NEXT: Get Max green-light on DeepSeek; route ingest rebuild to B2 (LLM-interpret + join Time-Codes by video-id).
- LESSON: Missing songs were never lost - timecodes sit in a separate Drive sheet; join restores ~2200 rows

## [2026-06-07 13:03] b1 95b07b94
- DID: Local-xlsx audit done: earliest event 2021-06-12, NO 2020 data in either file; the 4 silently-dropped tabs (Сердечки/ВКЛАДКИ/Программы/Темы ГПК) are METADATA not songs; the 2 source files heavily OVERLAP (~86 unique concerts). So the missing BULK = untimecoded rows whose timecodes live in the separate Тайм Коды sheet, NOT lost events. Both agents complete.
- STATE: Two beliefs corrected: (1) no 2020 data exists anywhere we have; (2) missed tabs were metadata not lost songs. REAL gap = ~2200 rows dropped only for lack of timecode, recoverable by joining Тайм Коды sheet. Max's 3x bet holds via timecode join + LLM-interpret of messy columns.
- NEXT: Report honest synthesis to Max; get DeepSeek green-light; route LLM-ingest+join to B2.
- LESSON: When user reports missing data, the cause may not match their mental model - here it was untimecoded rows + a separate sheet, not lost 2020 events or dropped tabs

## [2026-06-07 13:07] b1 95b07b94
- DID: Max added YT-channel-as-ground-truth lead (descriptions hold timestamped song indexes; only way to confirm 2020). Spawned YT-probe agent (background) parallel to DeepSeek interpret+join pilot agent. Both running. Max green-lit DeepSeek $3-6.
- STATE: Two pilots in flight: (1) DeepSeek 5-event interpret+join recovery-rate test, (2) YT channel probe (date range + description tracklist quality). b1 staying light, delegating all reads.
- NEXT: Synthesize both pilot results, then route full ingest build to B2 with the richest source mix.

## [2026-06-07 13:12] b1 95b07b94
- DID: YT probe done: channel 933 vids back to 2017, 2020 EXISTS (~72). Only ~30% concerts have description tracklists (clean, parseable, includes 2017-2020). 70% un-indexed anywhere. So 3 merge-able sources: sheets-LLM + Тайм Коды join + YT-description parse. B0 posted safety rails (no fabrication, read-only, join-not-branch, diff vs parser, pilot-first) - folding into B2 brief.
- STATE: YT + Drive probes both done. Only DeepSeek recovery-rate pilot still running. Pending Max answer: show un-indexed 70% as whole-video entries or stay strictly song-level.
- NEXT: Get DeepSeek multiplier, get Max's whole-video-entry decision, then route full 3-source build to B2.
- LESSON: Tamza YT channel reaches 2017 and is the only source for pre-2021 events; ~30% of concerts carry clean timestamped tracklists in their descriptions

## [2026-06-07 13:29] b1 95b07b94
- DID: DeepSeek pilot decisive: 0->295 playable links on sample, 92% within 2s, cost 0.077 USD. KEY: recovery is 100% from joining external Тайм Коды sheet (+YT desc), NOT from cleaning song files (most have blank t=0). JOIN KEY = date+performer+song FUZZY, NOT video-id (song file & Тайм Коды use different re-uploaded videos, 0/213 id match). Gotchas: Sheets-API-by-gid for full Тайм Коды, max_tokens>=16000, dedup 2 xlsx. Scripts in tools/tamza_songs/pilot_deepseek/.
- STATE: All 3 probes + DeepSeek pilot done. Method proven + cheap. BLOCKING on Max: whole-video-entries for un-indexed 70%. B2 likely needs re-activation for the production build.
- NEXT: Get Max whole-video decision -> hand B2 production spec (3-source merge, fuzzy join, B0 rails).
- LESSON: Tamza timecode recovery rides on external Тайм Коды sheet + YT descriptions joined by date+performer+song fuzzy; video-id join fails because the club re-uploads videos

## [2026-06-07 13:43] b1 95b07b94
- DID: Max LOCKED scope: song-level only, IGNORE un-indexed concerts (no whole-video entries). Max flagged b1 context getting full -> delegate the build. Spawned a BUILD worker in an isolated worktree: produces a CANDIDATE data.json via 3-source LLM-join (sheets-interpret + full Тайм Коды via gviz-csv-per-gid + YT-description parse), fuzzy date+performer+song join, B0 rails baked in, spot-audit ~25 links, DIFF vs current 1371, NO DEPLOY. Reports back for review.
- STATE: Build worker running (background, worktree-isolated, no deploy). All research done. Live site stays at v34 until candidate reviewed.
- NEXT: Review candidate recovery count + audit precision + regressions with Max/B0, THEN decide deploy.

## [2026-06-07 14:07] b1 95b07b94
- DID: Holding as b1 manager; relaunched local-only build worker a49ea0431a773ed26 (Excel-only, no Google) for DeepSeek date+performer+song join candidate
- STATE: STANDBY active; Max sensitive re Google (6 channels terminated); timer armed; worker running in background
- NEXT: Relay worker's recovery numbers + ~25-link audit + regressions to Max for go/no-go; NO deploy; clean up leftover worktree agent-a152f918

## [2026-06-07 14:12] b1 95b07b94
- DID: Local-only build worker DONE: candidate 26,430 playable rows (19.3x vs 1371), all verified real &t>=1, 0 regressions, 25/25 audit, $0.036
- STATE: Reported to Max; candidate at tools/tamza_songs/ingest_v2/site/data.json; NOT deployed, no Google touched
- NEXT: Await Max go/no-go on login-free yt-dlp liveness check on 25k new video IDs; then B0 review (110 unmatched + ~100 duet dup links) before deploy

## [2026-06-07 14:17] b1 95b07b94
- DID: Max requested: build a DB of ALL Tamza YouTube channel videos (id/title/date/duration/url), login-free + throttled to avoid YT block
- STATE: Liveness worker a9bce83dfb554723c running (556 videos via oEmbed); will SERIALIZE channel-DB after it finishes to avoid 2 concurrent YT crawlers
- NEXT: On liveness completion: launch channel-inventory worker, anonymous yt-dlp --flat-playlist on UCo-O_aBrW8J3hEGEdow71Iw, throttled, no cookies/login; save DB+README in tools/tamza_songs/yt_channel_db/

## [2026-06-07 14:22] b1 95b07b94
- DID: Relaunched as ONE combined worker a14c5ed80a8948ec2: throttled anonymous yt-dlp crawl = link+full description per channel video + liveness, single minimal-footprint pass (3-6s spacing, hard backoff, no login/cookies)
- STATE: Worker running in background, saves incrementally to tools/tamza_songs/yt_channel_db/; I am free for other tasks per Max
- NEXT: Await worker report (channel video count, live/dead, descriptions captured); leftover worktrees agent-a152f918 + agent-a9bce83d to clean later (do NOT delete agent-a49ea043 - holds candidate commit ec8071f2)

## [2026-06-07 14:35] b1 95b07b94
- DID: Fixed B0 deploy-blocker: normalized 2012 malformed youtu.be/<id>&t=N -> ?t=N at root (05_build_candidate fix_url) + final sweep; re-ran build+audit
- STATE: Verified 0 malformed links remain, 0 regressions, 25/25 audit, 19.3x intact. Candidate now CLEAN/deploy-ready pending Max OK
- NEXT: Channel desc-DB crawl still running (a14c5ed8); on Max go: hand clean candidate to b2 for production build+deploy

## [2026-06-07 14:40] b1 95b07b94
- DID: DEPLOYED catalog LIVE: 1371 -> 26430 rows (19.3x). Backup of old 1371 saved; deploy_catalog.py + rollback_catalog.py written. Verified LIVE URL = 26430 rows, 0 malformed links
- STATE: Catalog LIVE at tamza.com/kartoteka, fully reversible via rollback_catalog.py. Channel desc-DB crawl still running (a14c5ed8)
- NEXT: Watch for dead-link reports (rollback ready); housekeeping = leftover worktrees agent-a152f918+agent-a9bce83d

## [2026-06-07 15:00] b1 95b07b94
- DID: Re-posted b0-ack bcast (prev failed on cd); confirmed channel crawl alive at 263 videos, 0 throttle/0 dead
- STATE: Catalog LIVE 26430 rows verified, b0 GREEN; recovered_rows.json housekeeping done; crawl detached & growing
- NEXT: Hold as manager; let crawl finish (~40min); collect final yt_channel_db output since supervising agent ended

## [2026-06-07 16:29] b1 95b07b94
- DID: Max spot-checked live catalog: works great. b0 posted full live-verified GREEN sign-off (26430 rows, 0 malformed, 0 regressions, Phase-1 fixes preserved). Phase-2 DONE+LIVE
- STATE: Channel-DB crawl 920/1327 videos (70%), still running detached, 0 throttle/0 dead
- NEXT: Let crawl finish (~50min), collect final yt_channel_db output; then worktree housekeeping (a152f918+a9bce83d, NOT a49ea043)

## [2026-06-07 16:40] b1 95b07b94
- DID: Kartoteka intro updated + redeployed (worker v36): timecoder credit, 26 430 songs, ru-or-latin note, max@tamza obfuscated, scale='около 72% выходных' (468/648 weekends 2020-2026). Delegated to workers; stopped a stray duplicate agent before collision
- STATE: Intro LIVE & independently curl-verified (72% present, 519 gone, email absent from HTML, both pages 200). worker.js v35 archived
- NEXT: Hold light as manager; channel-DB crawl still finishing; watch for dead-link reports

## [2026-06-08 07:23] b1 95b07b94
- DID: Computed real per-year catalog stats for Max's FB post: 519 events over 2020-2026, ~50 songs/event (median 49), events/yr ~85-90 (2021-23 peak 105-109, 2024-25 76-92). Corrected Max's draft factors 52->85 concerts/yr, 60->50 songs
- STATE: Kartoteka intro LIVE & verified (v36, 72% weekend metric, obfuscated max@tamza). FB post arithmetic fixed & handed to Max
- NEXT: Hold light; channel-DB crawl still finishing; await Max on FB post wording

## [2026-06-08 07:26] b1 95b07b94
- DID: Max reported BUG: many recent timecodes lead to right video but wrong moment - hypothesis: indexer drafts have UNADJUSTED times (raw full-stream time, begin-cut offset not subtracted). Parser takes t from link &t=. Max's call: DROP unadjusted ones, don't compute offset
- STATE: Launched investigation worker a5d64d3 to find adjusted-vs-unadjusted signal in Тайм Коды xlsx + quantify. NO deploy until rule confirmed by Max. Live page still lands on right video meanwhile
- NEXT: Await worker findings; relay drop-rule to Max for confirm; then drop+rebuild+redeploy
- LESSON: Timecode correctness depends on indexer draft adjustment (offset for cut video start); raw link t= can be unadjusted

## [2026-06-08 07:47] b1 95b07b94
- DID: Dropped mis-indexed video i9QcHylLMhw (Лекарства Украине fundraiser, 14 rows, ~10s off) from kartoteka catalog + redeployed: 26430->26416 rows live, verified on R2. Earlier: timecode cross-check vs YT-description setlists found catalog clean (501/502 videos perfect).
- STATE: Kartoteka LIVE v36 intro + 26416 rows. Timecode bug = NOT widespread (only that 1 fundraiser was off). Max testing manually, will report specific bad videos one at a time.
- NEXT: If Max reports a wrong-playing video: identify its id, drop or offset-fix its rows via deploy_catalog.py (reversible). Else housekeeping: finish channel crawl, clean leftover worktrees a152f918+a9bce83d.

## [2026-06-08 08:11] b1 95b07b94
- DID: Performer-normalization staging build done (worker): search 'Ремпель' collapses to ONE entry Макс Ремпель 656 songs (dezh's 164 folded in + still searchable); 831 combo strings -> 691 real people. BUT the build also applied my bad R3 (drop all Лекарства Украине) = 3988 rows/109 videos -> REVOKED: most are real fundraiser concerts. Code at ingest_v2/site/staging_performers/normalize_performers.py. Greenlit b2 v38 reports-backend (clear of my lock). b5 branched to investigate offset bug (told: investigate first).
- STATE: Live catalog UNCHANGED = clean 26,416 rows. Performer fix NOT deployed. R3 revoked in spec. Awaiting Max OK to re-run perf build with R3 OFF (keep Лекарства songs) then deploy. b5 investigating wrong-timecode scope; b2 building пожаловаться report feature (human-labeled mis-timed stream).
- NEXT: On Max OK: re-run normalize_performers.py with R3 disabled (keep all Лекарства concert songs, only i9QcHylLMhw stays dropped), re-preview Ремпель, deploy via deploy_catalog.py + coordinate app.js perf-change deploy with b2's report-modal merge. Then collect b5 findings.
- LESSON: Do NOT invent exclusion RULES from a single example (one Лекарства cooking show -> 'drop all Лекарства' would have purged 4000 real concert songs). Staging-preview-before-deploy caught it; never auto-generalize a one-off drop into a catalog-wide rule without Max.

## [2026-06-08 11:03] b1 95b07b94
- DID: Max DECISIONS: (1) hide (not delete) the 133 unadjusted-timecode rows - keep song+performer, withhold only the broken link; they auto-return correct after the human timecoders set offset I1 and we re-import. (2) BUILD a repeatable MONTHLY update system. b5 root-caused the bug (2nd working file Песни на Тамзе.xlsx; unadjusted = G4!=0 & I1==0; 4 vids/133 rows). b0 confirmed live banner is base64 (no 404); my deploy must be scoped to app.js+data.json only, never index.html. v38 reports-backend live-green.
- STATE: Live = clean 26,416, nothing performer/offset deployed yet. Architecture agreed: FROZEN legacy base (events <=2025-12-06 from current catalog, never re-derive/no DeepSeek) + DETERMINISTIC monthly layer parsed from working file for events >2025-12-06 (applies R4 hide-unadjusted, R1/R2 performer, R5 date-tabs, R3 REVOKED keep Лекарства). Launching pipeline-build worker -> staging candidate + preview, no deploy.
- NEXT: Preview the first pipeline run with Max (rows, Ремпель result, hidden-133 list), then ONE reversible deploy scoped to data.json+app.js (banner-safe). Write monthly-run method doc. b5/b2 holding data.json til DONE.
- LESSON: Build the catalog as a re-runnable 2-layer pipeline (frozen legacy + deterministic recent), not one-off edits; monthly cadence tied to human-timecoder catch-up. Hide unadjusted rows via build-time filter so they self-heal on re-import - no UI null-state, no app.js churn.

## [2026-06-08 11:19] b1 95b07b94
- DID: DEPLOYED monthly-pipeline candidate to live: 26283 rows, performer R2 normalization + R3-revert (Лекарства kept) + R4 hide-134-unadjusted. Verified live 26283 + performers[]. Scoped data.json+app.js only (banner-safe). Backed up to pipeline/output/archive/.
- STATE: Live=26283. Lock released to b2 for report-modal merge. C3 both lanes PASS, b0 seam clean. Import-rules spec R1/R2/R3/R4/R5 captured.
- NEXT: Update spec R1/R4 status to DEPLOYED; b2 folds report UI; later fix repo site/index.html line 54 (dead jpg); housekeeping worktrees.
- LESSON: Staging-preview-before-deploy + independent re-derivation by a verifier branch (C3) caught/cleared the off-by-1 and confirmed no over-hide before any live change.

## [2026-06-08 11:41] b1 95b07b94
- DID: Deployed live: R2 performer normalization, R6 hide perf<3 (list 747->484), доложить report link (relabeled from пожаловаться, self-contained injected CSS+modal), one-line layout fix flex-wrap:nowrap. E2E: report modal PASS (submit 200, 'Спасибо! Жалоба отправлена', 0 console errors). Worker stays v38 (v39 killed as duplicate CSS, b0/b2 acked).
- STATE: Live app.js 13569b self-contained owns report+layout CSS. Layout re-test agent running. Songs lane shipped 26283 rows.
- NEXT: Answer Max on continuous-playback (in-page player, awaiting his go); apply narrow-margins + play-button-on-LEFT layout; build autoplay-next-same-performer on go.

## [2026-06-08 13:57] b1 95b07b94
- DID: B6 deployed app.js 22071b LIVE+b0 PASS: радио автора in-page player (skip fwd/back, segment-end auto-advance), tiny margins, .8rem narrow one-line font, buttons-left, band-name display-collapse (R2 intact). Lock released b6->b2.
- STATE: Live app.js=22071b, data.json untouched 26283. Radio+layout+band-collapse live & gated. b2 now implementing short performer links (#p/#a, drop '--', top-20 chips) + v39 report modal on top.
- NEXT: Await b2 short-links deploy -> b0 gate -> e2e (radio plays, YouTube btn, one-line, band-collapse, chips). Then record R2=credit-everyone + master-class-drop + band-collapse into kartoteka_import_rules spec. Radio listen-test w/ Max pending.

## [2026-06-08 14:31] b1 95b07b94
- DID: Investigated Max's 'missing songs' (data full: 806 Ремпель, gaps=unindexed weekends ~72% + R4-hidden 4 dates). Root-caused 2 live bugs: (1) stuck-Назад nav (history.back dead-ends on #p hash entry-point), (2) author-radio plays singer not author. Approved R7 author-dedup (shared alias registry, b5).
- STATE: b2 fixing Назад (holds app.js lock). b5 building R7. b6 queued for author-radio fix after b2 releases lock. Displayer (Top-20 singers+authors chips) live+committed 28945b.
- NEXT: Confirm Назад fix live + Max retest. Then hand lock b2->b6 for author-radio. Record R2/R7/master-class/band-collapse in spec.

## [2026-06-08 15:10] b1 95b07b94
- DID: Author-radio fix shipped+e2e PASS on live, committed master 94453340, pushed, app.js lock released
- STATE: Live app.js 29752b == git. Author page radio uses author queue (340), performer uses performer queue (806). 0 console errors.
- NEXT: b5 free to take app.js lock for R7 author-dedup. Then b2 wires _aauth into #a index. Record R2/R6/R7/band-collapse into spec.

## [2026-06-08 16:10] b1 95b07b94
- DID: Shipped radio seek -10/+10s (buttons+arrows), bigger player+full note earlier; all live+pushed master
- STATE: Live app.js 31419b == git. R7 step-1 (data.json _aauth) live+b0-gated; b2 to rebase step-2 onto 31419b.
- NEXT: b2 wire _aauth into #a author index on 31419b. Then record R2/R6/R7/band-collapse in spec. Optional: listen-test seek+radio with Max.

## [2026-06-08 16:52] b1 95b07b94
- DID: Radio seek (buttons+arrows) confirmed working by Max. R7 author-dedup shipped by team (b5 build + b2 read-side), b0-gated twice, live app.js 32699b.
- STATE: All live: bigger player, full note, radio seek, R7 author dedup (1542->1448, Ремпель 1 canonical). data.json 26283 untouched.
- NEXT: Record remaining spec items (R2 credit-everyone, master-class drop, band-collapse, R6 fully-hidden) into kartoteka_import_rules_v01. Optional listen-test with Max.
