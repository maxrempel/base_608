
## [2026-06-08 14:24] b5 f73f8381
- DID: Root-caused timing bug (R4: 4 videos/133 rows, marker G4!=0 & I1==0); Max said ignore them, reported to B1, drop pending go. Logged R7 author-dedup (twin of R2).
- STATE: R4 not yet dropped from data.json. R7 proposed: shared person-alias registry for performer+author canonicalization, awaiting B1 ok.
- NEXT: On B1 go: drop 133 unadjusted rows + redeploy. Build shared registry for R2+R7.

## [2026-06-08 14:41] b5 f73f8381
- DID: Built+dry-ran R7 author canonicalization prototype (author_canon_v01.py): 26416 rows preserved, Ремпель->441 songs, 4903 canonical authors. Found 1 open fork (hyphen-split between co-author names) sent to B1.
- STATE: R7 design fully proven standalone, no deploy. Awaiting B1 ok on hyphen-split + b2 handoff-format sync + app.js lock (b6 has it). R4 timing drop still paused per Max 'wait wait'.
- NEXT: On B1 hyphen-split answer: finalize engine, sync format w/ b2, then wire app.js when lock frees. On Max go: drop R4 rows.

## [2026-06-08 15:05] b5 f73f8381
- DID: R7 author-canon engine fully designed+validated (author_canon_v02.py): safe hyphen rule (b0) verified, b2 confirmed 20/20 slug match zero retune, b0 design-cleared, hand-off format r._aauth=[{k,d}] agreed. No deploy.
- STATE: R7 BUILD-READY, blocked on app.js lock (B1/b6 doing author-radio 2-min-cap fix). R4 timing drop PAUSED awaiting Max 'wait wait'. Local data.json=26416 vs live=26283 (reconcile before R7 deploy).
- NEXT: When app.js lock frees + B1 go: build R7 on LIVE data.json, emit _aauth, b0 hard-gate (zero row change vs 26283, 6 doubles unsplit, Ремпель~441), then b2 wires #a index. Separately: get Max go on R4 drop.

## [2026-06-08 15:22] b5 f73f8381
- DID: R7 build (A=build-time) fully prepped+validated on LIVE pipeline/output/data.json (26283): Ремпель=431, 6 doubles intact, co-authors split, b2 20/20 slug match holds. Found live pipeline = pipeline/scripts/build_catalog.py (two-layer: stage_freeze_legacy + stage_recent_layer). Engine = author_canon_v02.py.
- STATE: Team consensus (b0+b2+b5+spec) = option A build-time. AWAITING B1 FORMAL GO before first data.json mutation. R4 timing drop still paused for Max.
- NEXT: On B1 go: add _aauth=[{k,d}] emit to build_catalog.py algorithmic step, rebuild->pipeline/output/data.json, deploy data.json FIRST under b0 diff-gate, then b2 wires app.js read-side. Engine logic in author_canon_v02.py (tokenize+matchkey+ALIASES+safe-hyphen).

## [2026-06-08 15:44] b5 f73f8381
- DID: R7 fully prepped+validated on live (Ремпель=431 LOCKED with b0, drift explained as base-file not engine). Flagged board-honesty gap (standby never cleared though team active). Offered Max direct-go option.
- STATE: BLOCKED on B1: needs to post bcast resume + give R7 step-1 GO. b0 gate-ready (26283 rows, 6 doubles unsplit, Ремпель=431, no fallback). Deploy order: data.json+_aauth first, then b2 app.js. R4 drop still paused per Max.
- NEXT: On GO: edit pipeline/scripts/build_catalog.py to emit _aauth=[{k,d}], rebuild pipeline/output/data.json, deploy that path via deploy_catalog.py, b0 diff-gates, then b2 wires read-side. Engine=author_canon_v02.py.

## [2026-06-08 16:04] b5 f73f8381
- DID: R7 author-canon STEP-1 DEPLOYED: build_catalog.py imports new author_canon.py, emits _aauth=[{k,d}]; rebuilt+deployed data.json to R2 (26283 rows, byte-verified); committed+pushed master df0a8e39
- STATE: Live data.json carries _aauth. Self-gate passed: 26283 unchanged, only _aauth added, 6 doubles unsplit, Ремпель=431. Old app.js ignores field. Rollback ready (live backed to archive/). Posted board for b0 gate.
- NEXT: Await b0 gate PASS, then b2 takes app.js lock for step-2 read-side rewire
- LESSON: Before an additive deploy, run UNMODIFIED build first to prove it byte-reproduces the live artifact -- catches spreadsheet drift / paused-rule entanglement before they ship

## [2026-06-08 16:25] b5 f73f8381
- DID: R7 COMPLETE END-TO-END: b2 deployed step-2 app.js (32699b, reads my build-time _aauth); R7 fully live. My build side closed (author_canon.py+build_catalog.py, master df0a8e39, pushed).
- STATE: Site now merges author spelling variants: 1542->1448 deduped, Ремпель=431, Visbor 665, Nikitin disambig OK, performers untouched, no fallback. Awaiting b0 step-2 gate.
- NEXT: b0 step-2 gate is the only open item; nothing for b5. R4 drop still paused per Max (already hidden in live build anyway). Re-implement R2/R3 as build rules = future.

## [2026-06-08 16:53] b5 f73f8381
- DID: R7 EPIC CLOSED: both gates passed (b0), spec marked DEPLOYED, committed+pushed master 480e31bd. Author merge fully live on tamza.com/kartoteka.
- STATE: Done: build (author_canon.py+build_catalog.py df0a8e39), read-side app.js (b2 65d8ccdd), spec doc (480e31bd). Live: Ремпель=431, author list 1542->1448, zero songs lost, no fallback, rollback backup in pipeline/output/archive/.
- NEXT: No open b5 work. R4 drop stays paused per Max (already hidden in live anyway). Future: merge R2+R7 alias maps into one shared registry. Standing by for next assignment.

## [2026-06-09 12:08] b5 f73f8381
- DID: R7 author dedup done+live (26283 rows, _aauth added, Ремпель=431). Team on STANDBY since 10:44.
- STATE: Paused, 4-min wake armed. R7 baked into monthly-build candidate (build_catalog.py). B6 running solo no-deploy song-timing pilot.
- NEXT: Auto-resume when standby clears; only role left = build-author support for monthly swap (b0/b2 own gate).
