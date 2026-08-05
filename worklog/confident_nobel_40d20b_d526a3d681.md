
## [2026-07-04 17:22] ? b18ce36a
- DID: Fixed storyboard reel-open slowness (D04B): moma_db D1 calls now use keep-alive requests.Session; /api/job reuses one connection. ~12s -> ~1.5s per reel-open. Committed+pushed to moma master eb5b3b5.
- STATE: MOMA servers restarted with fix live on Pine (8779/8790).
- NEXT: None - verified. Max to confirm by clicking a reel.

## [2026-07-04 23:27] ? b18ce36a
- DID: Fixed scene-filter leak (prev-scene reels showing in wrong scene view). Root cause: arrangement_picker broadcast selection only on boot/change; when localStorage arr-filter got clobbered to '[]' (search-widen/load race) it never healed -> all scenes leaked. Fix: picker re-asserts selection every 2s poll; added no-op guards to prompter+mixboard so heartbeat doesn't blink. Server filter was already correct (proven). moma master 67ad744.
- STATE: Committed+pushed. Static JS - needs browser hard-reload to load.
- NEXT: Max to hard-reload ReelMaker tab (Ctrl+Shift+R) and confirm sc09 reels gone from Scene 11 view.

## [2026-07-05 00:03] ? b18ce36a
- DID: Found WHY scene-filter fixes 'kept not working': runner cache-buster assetver omitted arrangement_picker.js, so picker edits never bumped ?v= -> browsers served CACHED old picker on normal reload (only hard-reload worked). Added ARR_PICKER_JS to assetver max(). Runner restarted; verified server serves new picker (re-assert) at bumped ?v=. Also confirmed the imager images Max saw are genuine sc11 (bg_sc11_service_desk_room, fresh worker batch), NOT cross-scene leak; sc11 has 119 junk+80 done images so whole-scene view is a big pile. moma master 59fa6a8.
- STATE: Cache-buster+picker fixes pushed+live. Max must HARD-reload once to clear old cached picker; after that normal reloads get fresh JS.
- NEXT: Max hard-reload imager+reelmaker (Ctrl+Shift+R), confirm leak gone. If cross-scene junk persists below fold, investigate further.

## [2026-07-07 17:52] ? aa619d47
- DID: X21G autonomous run start: Max wants POPULATION FREQUENCY (rare vs common) + full SIZE of the confirmed OMEGA insertions. Method: insertion is absent from GRCh38 ref but should appear in OTHER assemblies (T2T-CHM13, HPRC pangenome) / SV catalogs (gnomAD-SV, dbVar, DGV); count carriers = frequency.
- STATE: Read-level sweep of 47 relocations DONE: 0 de-novo, 0 son-differs; all inherited (mother identical) or artifacts. Now pivoting to freq+size of top insertions (chr12:30348820 etc). Autonomy ~2h then sleep.
- NEXT: 1) inventory local T2T/HPRC/SV on asto 2) full size+seq of top6 3) frequency per locus 4) report then sleep

## [2026-07-07 18:00] ? aa619d47
- DID: X21G: gnomAD-SV frequency DONE (fixed chr-prefix bug that had hidden all matches). Of 47 relocations: 2 common>5% (chr11:38980211 AluY AF=0.50 ~500bp; chr6:168659935 AF=0.19), 1 low, 6 rare<1%, 32 no-INS-within-500bp (mostly segdup/repeat regions gnomAD can't resolve = freq unreadable, not proven rare), 5 alt-contig. Catalogued sizes ~270-500bp = Alu/MEI scale. chr12:30348820 not a common catalogued INS but in gnomAD-blind segdup region.
- STATE: Frequency answered for gnomAD-visible ones. 32 need T2T-CHM13 assembly presence check (chm13v2.0.fa + chm13_blast db already on asto/omega_run/ref). NCBI online blast dead from guest box - dropped.
- NEXT: 1) blast the 32 gnomAD-blind payloads vs chm13_blast -> present in 2nd assembly? 2) measure true sizes 3) write report projects/XG1/kenefick/omega_detector/ + sleep

## [2026-07-15 12:10] ? fdb57dd4
- DID: Built external PrintScreen->LightShot reroute (AutoHotkey v2 script at C:\claude_base\tools\printscreen_reroute\printscreen_to_lightshot_v01.ahk), running as AutoHotkey64. Bare PrintScreen -> sends Shift+PrintScreen (LightShot's real hotkey). Root cause of bare-dead: OneDrive 'save screenshots' + Win Snipping grabbed bare key; Shift+PrtSc slipped past. Max PROHIBITS changing his LightShot Shift+PrintScreen binding - reroute must stay external.
- STATE: AHK reroute deployed+running; awaiting Max physical test of bare PrintScreen. LightShot ignores injected keys in my SendInput tests, so AHK send may or may not trigger it.
- NEXT: If Max says dead: switch AHK send mode (SendEvent/SendPlay or DllCall keybd_event); do NOT touch LightShot config or restart his OneDrive/PowerToys.
