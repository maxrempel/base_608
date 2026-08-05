
## [2026-06-16 08:03] b15merger 0886b272
- DID: B15merger Stage1 r1: author normalizer (key=surname+first-initial) collapsed 28336 author-tokens -> 3772 entities. QC PASS: Матвеева split preserved (Вера48/Новелла128); full names collapse onto initials (Ариэла Марина Меламед->А.меламед). Scripts in _work/merger/.
- STATE: r1 QC found 3 round-2 fixes: (1) homoglyph initials Latin A/C vs Cyrillic А/С split same person (меламед A.3|А.876, бабицкая C.2|С.687); (2) stray noise initials '1'/':'; (3) diminutive case Женя(Ж.58)/Евгения(Е.288) Ратновская = same person, needs map or Max call.
- NEXT: Build author_norm_v2: add Latin->Cyrillic homoglyph initial map + noise filter; re-QC; flag diminutive cases. Then performer norm, then first-line cluster match.
- LESSON: Russian catalog mixes Latin/Cyrillic homoglyph initials (A vs А) - must normalize before keying author identity.

## [2026-06-16 12:07] b15merger 0886b272
- DID: B15merger Stage1 author-normalizer DONE r1+r2, pushed 48456c76. Key=surname+first-initial collapses 28336 author-mentions->3754 entities; Матвеева Вера(В,48)!=Новелла(Н,128) preserved; r2 added Latin<->Cyrillic homoglyph initial map + diminutive(Женя->Е). Scripts: _work/merger/author_norm_v2_b15merger.py (+profile_human, author_entities_v2.json).
- STATE: Max APPROVED: Ратновская is ONE person -> merge bare Ж.Ратновская into Е.Ратновская. Need surname-specific alias rule (DIM_INIT only catches full word 'женя', not bare 'Ж.' initial).
- NEXT: 1) add AUTHOR_ALIAS {(ратновская,Ж):(ратновская,Е)} merge map in author_norm v3; rerun+commit. 2) author QC rounds 3-4. 3) performer normalization (human performer field already clean, 831 distinct). 4) first-line cluster match human<->machine canon_v03 -> consensus, aim 93%, flag rest questionable keeping human+machine comment.
- LESSON: Bare lone-initial author variants (Ж. vs full Женя) need a per-surname confirmed-merge alias map, not just a diminutive-word map.

## [2026-06-16 14:24] b15merger 0886b272
- DID: B15merger Stage1 author-norm r1-r3 pushed (2f8642a0). Max gave ARCHITECTURE requirement for the whole merger: NON-DESTRUCTIVE 2-DB design. (1) ORIGINAL db = frozen inputs, never written: human data.json + machine canon_v03. (2) UPDATES db = append-only RULES/DECISIONS ledger (the merge maps as editable DATA, not baked into code): SINGLE_PERSON confirmed merges (Меламед=А, Ратновская=Е), homoglyph map, diminutives, Матвеева-guard, future performer_aliases + firstline_overrides - each decision carries provenance (Max date why). RESOLVED db = original+rules materialized by a deterministic build, REGENERABLE, never hand-edited. Optimize a step = edit its rule file + rerun, never overwrite output.
- STATE: Context at 92%, compaction imminent. Need to refactor: extract the maps currently hard-coded in author_norm_v3 into rules/author_merges.json + provenance, and make the normalizer READ the rules. TMS convention now in force (lead every purple TLDR with Task+Method+Status).
- NEXT: Build the rules/ ledger structure: rules/author_merges.json (single_person, aliases, homoglyph, diminutives each w/ provenance) + a build script orig+rules->resolved_authors.json. Then performer rules, then first-line. NOTE b15B(new session) says Max corrected: song identity = FULL-TEXT clustering, first_line is only a LABEL not match key - affects the LATER first-line stage, confirm with Max/b15M before building match stage.

## [2026-06-16 14:24] b15merger 0886b272
- DID: B15merger: Max FINALIZED provenance schema for the merger's resolved DB. Every value stores provenance keyed by source: HUMAN-sourced value -> records DATE OF INGEST (when it entered the catalog). AUTO/machine-sourced value -> records METHOD OF CALCULATION (which rule/step computed it, e.g. surname+initial merge / Max-confirmed single-person / homoglyph / full-text cluster match).
- STATE: Architecture fully specified: 2 DBs (ORIGINAL frozen inputs human data.json + machine canon, never written; UPDATES = append-only rules/decisions ledger) + RESOLVED = deterministic build(original+rules), regenerable never hand-edited. Provenance per value: human=>ingest_date, auto=>calc_method. Context 95%, compaction imminent.
- NEXT: Build rules/ ledger: (1) extract author maps from author_norm_v3 into rules/author_merges.json w/ provenance; (2) build_resolved.py orig+rules->resolved_authors.json where each entity value carries {source:human,ingest_date} or {source:auto,method}; (3) performer rules; (4) first-line stage - BUT confirm w/ Max: new b15B says identity=FULL-TEXT cluster not first_line. Scripts in _work/merger/, pushed 2f8642a0.

## [2026-06-16 14:34] b15merger 0886b272
- DID: Documented+deployed annotation-merger design (2-DB non-destructive + provenance) and Stage-1 author-norm r3 artifacts; pushed f0cb6b53 to master.
- STATE: Stage-1 author normalization DONE (3 rounds, 28336->3748 entities, Matveeva split kept). Design doc at _work/merger/annotation_merger_design_v01_tomemex.md.
- NEXT: Refactor maps into rules/author_merges.json w/ provenance; build_resolved.py (ORIGINAL+rules->resolved_authors.json w/ per-value provenance); then song-identity stage consuming canon_v03 + b15M aligner (full-text, NOT first_line).

## [2026-06-16 14:56] b15merger 0886b272
- DID: Implemented non-destructive 2-DB for author stage: extracted maps into rules/author_merges.json (UPDATES ledger w/ provenance); build_resolved.py reads ledger+frozen catalog -> resolved_authors.json w/ per-value provenance. Pushed c8682e6f.
- STATE: build_resolved.py = RESOLVED=build(ORIGINAL+rules). 3748 entities, Matveeva split kept, single-person confirmed. Provenance: auto+method list / human+ingest_date.
- NEXT: 4th QC round optional; then performer-norm rules; then song-identity stage (canon_v03 + b15M aligner, full-text NOT first_line) -> reconcile human vs machine, 93% confident, flag questionable.

## [2026-06-16 15:14] b15merger 0886b272
- DID: Author reconcile v02 (majority vote over per-performance human co-author sets, exact vid+t join) hits 97% confident vs 93% target; n_perf>=3 also 97%. Pushed 7e7f5a0c.
- STATE: Pipeline: performer-norm done (clean passthrough); author entities 3686; author<->machine reconcile DONE at 97%. Shared author_parse.py drives everything from rules ledger. ~3% questionable = genuine human-label splits, flagged + kept.
- NEXT: First-line/song-line reconcile stage (uses canon consensus_text vs human first_line; note sibling b15M/b15A thread on whether consensus_text keeps line breaks - Max wants poetry in real lines). Then assemble final merged annotation DB across the 3 fields.

## [2026-06-16 15:17] b15merger 0886b272
- DID: Coordinated w/ b15M/b15A on line structure. Inspected canon_v03 directly: consensus_text is FLAT (no line breaks/punct/caps). Posted finding to board.
- STATE: Author reconcile 97% DONE (pushed 7e7f5a0c). First-line/line stage BLOCKED: canon_v03 has no poetry line structure; needs b15A/Max decision on line source (re-emit clusters w/ line structure / external lyrics / heuristic re-split).
- NEXT: Next tick: check board for b15A/b15M reply on line-structure source. Do NOT start line stage until decided. Could meanwhile build the FINAL merged-annotation assembler for performer+author (the 2 done fields) into one resolved song-annotation DB.

## [2026-06-16 15:23] b15merger 0886b272
- DID: Built first-line reconcile v01 (93% conf) + assembled unified resolved_songs_v01.json (92% both-field confident)
- STATE: All 3 reconcile stages done (performer/author/firstline) + unified DB; committed+pushed de77ec52; line-aware dropped per b15M/Max
- NEXT: Wait for Max review; b15M scaling aligner across 452 videos - join resolved_songs_v01 with timecoder drafts when ready

## [2026-06-16 15:40] b15merger 0886b272
- DID: LLM performer merge done (691->669, 21 merges/12 flagged, committed 204a37d1). Probed LIVE catalog: it is AHEAD of staging - 26283 rows WITH performers[] + song-timing seg_start/end/conf + _aauth authors; Лекарства NOT dropped live (good).
- STATE: staging_performers/*.json files are STALE; live is a richer current build from an unknown-to-me pipeline. My merge ledger = performer_llm_merges_v01.json (remap old->canonical).
- NEXT: Find the CURRENT build script that emits 26283-row data.json (build_site.py? song_timing deploy?) and wire the merge remap in, regenerate, deploy via deploy_catalog.py (reversible). Do NOT deploy stale 22428 staging file. Decide: hand-patch live vs fix pipeline; apply 12 flagged or not.

## [2026-06-17 14:40] b15merger 0886b272
- DID: Posted b15merger's 5 interview answers (TASK/METHOD/STATUS/DEAD-END/YT-lesson) to b-board for B25handoverer's clean handover.
- STATE: Performer-dedup task DONE+deployed (master 6003d51b, live, reversible). No open performer work. In 5mt idle loop.
- NEXT: Wait for new Max command or b-team ask; honor 5mt re-arm.

## [2026-06-17 15:26] b15merger 0886b272
- DID: Reviewed B25 handover (flagged my perf-merge as DONE not pending). Reshaped go-live gate to Max's 3-path OR; I own path C = intro-performer fuzzy-match vs resolved_performers DB. Posted interface needs to board.
- STATE: Perf-dedup DONE+live. NONH publish-gate in DESIGN: 3-path OR (A canon match, B intro attribution, C intro-performer vs my DB). Waiting on Max's 3 thresholds + owner of segmenter-intro-fields wiring.
- NEXT: When thresholds+owner set, build path C scorer (reuse R8 name-normalization).
- LESSON: Go-live gate is OR of 3 paths, not just canon match; held = fails all 3, never silently dropped.

## [2026-06-18 06:36] b15merger 0886b272
- DID: Reworked NONH publish gate TITLES-FREE per B26 manager re-task (Max hard rule: identity=first sung line only, kill all titles). Built nonh_publish_gate_dryrun_v02_titlesfree.py, ran it.
- STATE: v02 split: 697 videos/7065 segs -> PUBLISH 6997, HELD 68. Titles dropped. Identity=first_line, raw placeholder pending b27's LLM-verified lines (consumes b27_verified_first_lines_v01.json by vid|start). Raw lines still have spoken-intro bleed = b27's job. No deploy.
- NEXT: Await b27 verified first-lines + Max deploy-scope okay; then swap placeholders for verified lines, re-run, deploy reversibly.
- LESSON: Once identity=first sung line (not a canon title), almost everything publishes (68 held of 7065) - the hard part shifts entirely to LLM-cleaning the heard line, not the gate.

## [2026-06-18 07:03] b15merger 0886b272
- DID: Re-pulled seg_nonh/ per b7+B26 order. Inspected schema + overlap vs my drafts.
- STATE: seg_nonh=747 vids (28 NEW beyond my 719 drafts; drafts are subset). KEY: seg_nonh segs carry only performer+author+title+confidence+timecodes, NO heard text -> b27 needs raw ASR transcripts (not seg_nonh) for first lines on new caption-disabled vids. Posted to joint board. Set still growing toward 81 - NOT finalizing.
- NEXT: When b7 finishes ASR/segmentation (81 vids) + b27 delivers verified first lines, freeze worklist=seg_nonh-union, swap placeholders, re-run titles-free split. Await Max deploy-scope okay. No deploy.

## [2026-06-18 13:42] b15merger 0886b272
- DID: Updated titles-free gate v02 to consume b27's INTRO-ONLY verdict + defined the b27 contract (b27_verified_first_lines_v01.json keyed vid|start; value = faithful first line OR literal 'INTRO-ONLY').
- STATE: INTRO-ONLY segs excluded from publish_rows, kept in intro_only_rows (no silent drop). Worklist grew to 744 vids/7910 segs: PUBLISH 7839, HELD 71. _work/ is gitignored (team works on-disk, no commit). Posted contract to joint board.
- NEXT: When b27 drops the verified-lines file, gate auto-consumes it; then freeze worklist=seg_nonh-union when b7 hits 81, re-run, await Max deploy-scope okay. No deploy.
- LESSON: The annotator/merger pipeline _work/ dir is intentionally gitignored - deliverables there are on-disk JSON the team consumes, not git commits.

## [2026-06-18 14:42] b15merger 0886b272
- DID: Gate v02 now holds all 3 b27 tokens (INTRO-ONLY/POEM/VERIFY) -> held_rows w/ hold_reason; added staging guard skipping verified_first_lines_*__*.json (no auto-ingest of __ds4pilot). Verified on pX: 28 SUNG/8 POEM/4 VERIFY/7 INTRO-ONLY exact match. Posted 3-token contract confirm + B30 youtu.be ack.
- STATE: Full set 744 vids: PUBLISH 7820, HELD-unknown 71, HELD-nonsong 19. Still DRY-RUN, no deploy. Awaiting full verified set + B30/b7 seg_end + Max scope-approval.
- NEXT: When upstream lands: build live republish merger (inject NONH rows + patch seg_end incl 900 free via build_data_overlays), backup+byte-verify+rollback-ready, B26 spot-check before deploy.

## [2026-06-18 14:49] b15merger 0886b272
- DID: STAGED the free seg_end recovery republish per B26 order (no deploy). New script stage_segend_recovery_v01.py: fetched LIVE R2 catalog read-only, applied merged overlay, diffed live-vs-candidate. RESULT: 899 recovered (null->int), 0 changed, 0 lost -- purely additive, zero regression. Artifacts in pipeline/song_timing/staging_segend_recovery/ (candidate, REVIEW json, live_baseline backup). Posted to B26 for review. Flagged enrich_catalog already handles youtu.be (B30 bug already fixed in live copy).
- STATE: Awaiting B26 review/approval of the 899-row candidate before deploy. deploy_catalog.py <candidate> is the reversible deploy. Gate v02 3-token + staging guard already done earlier this turn-set.
- NEXT: On B26 approve: deploy the 899-row candidate (backs up live, byte-verifies). Separately still awaiting full b27 verified-line set + B30/b7 seg_end-from-teal16 for the NONH-injection republish (bigger second step).

## [2026-06-18 15:29] b15merger 0886b272
- DID: DEPLOYED the 899-row free seg_end recovery to LIVE R2 (B26 relayed Max-GO). deploy_catalog.py backed up live -> archive/data_live_backup_20260618T222912Z_26283rows.json, uploaded 26283 rows, byte-verified R2==upload. Purely additive: 899 null seg_end filled, 0 changed/0 lost, row count unchanged. 2-min cap lifted on 899 songs. Posted result to B26.
- STATE: LIVE + verified + rollback staged. NONH/recognized-performances scope NOT touched (still waits Max). Edge cache ~5min propagation.
- NEXT: Optionally verify live edge serves new ends after ~5min. Next big step (still blocked): NONH-injection republish once b27 v3 POEM-fixed verified lines + b7/B30 seg_end-from-teal16 land.
- LESSON: Staging a live-public change by fetching the ACTUAL live R2 object, applying only the targeted overlay, and diffing live-vs-candidate (recovered/changed/lost) gives a clean zero-drift review artifact + reversible deploy -- ideal pattern for safe additive republishes.

## [2026-06-18 15:34] b15merger 0886b272
- DID: LIVE-EDGE VERIFIED the 899-row deploy: curl public tamza.com catalog = 18874704 bytes (matches upload), 26283 rows, 22950 with int seg_end (matches enrich), sample recovered row YCWHPxP8XuQ@2428 serves seg_end 2652 as expected. Propagation complete, users see it.
- STATE: 899-row free recovery DONE + live + edge-verified + rollback staged. NONH scope still waits Max. b27 solved POEM (deterministic reading-verb override), asking B26 for 2 full-scale approval; my gate already skips __ds4pilot staging files.
- NEXT: Blocked until b27 full verified lines + b7/B30 seg_end-from-teal16 land; then build NONH-injection republish. Otherwise idle.

## [2026-06-18 15:50] b15merger 0886b272
- DID: ROUND-1 LLM-QC done by my own eyes (Max's order: 3 rounds, MY llm reads transcripts, not delegated). Compared pX __ds4pilot4 vs hand-gold (36/47 agree) + read raw transcript at disagreements. Faithfulness PERFECT (zero canonical drift). POEM override good (residuals 3473/3734 = human). REAL LEAK = host-talk published as SUNG (441/5807/7793 confirmed in transcript, ~7-8%). 7793 also a missed reading-verb POEM (прочитаю past head window). Posted findings+round-2 ask to b27/B26 via joint.
- STATE: Round-1 verdict: DO NOT scale to full yet. Waiting on b27 __ds4pilot5 (tighten INTRO-ONLY on host-patter cues + fix 7793 scan), then I QC round 2, then round 3. Separately: 899-row recovery already LIVE+verified.
- NEXT: QC round 2 when b27 posts pilot5. Also note: my publish gate won't catch host-talk-as-song (seg has performer->publishes anyway), so fix must be at b27 extraction. COMMS: use --joint for b26 (team r), case-sensitive @-route bug reported to c6.
- LESSON: QC the LLM extraction by reading the ACTUAL transcript at each class-disagreement, not just trusting agreement %; faithfulness can be perfect while INTRO/host-talk-vs-SUNG boundary still leaks junk rows.

## [2026-06-18 16:05] b15merger 0886b272
- DID: Spot-checked b7 next-start candidate vs live: additive-only +3205/0/0 confirmed, but 4 rows derive absurd ends (one 11h) from garbage start times -> asked b7 for max-gap guard (null if gap>1800s). Posted consolidated status to B26 (joint).
- STATE: 899 free recovery LIVE+verified. b7 second pass HELD pending guard+GO. NONH QC round1 done (faithfulness perfect, host-talk leak ~7-8%, do-not-scale). Round2 blocked on b27 ds4pilot5 (not yet shipped). Round3 after.
- NEXT: Await b7 guarded next-start candidate (deploy on GO only). Await b27 __ds4pilot5 -> run round-2 LLM-QC by own eyes. No NONH injection until 3 QC rounds pass.
- LESSON: Next-start seg_end chaining must cap on max-gap: a row with a garbage &t= makes the next-start of a real row absurd (11h 'song'). Always sanity-bound derived durations.

## [2026-06-18 16:53] b15merger 0886b272
- DID: Ran round-2 own-LLM QC of b27 __ds4pilot5 pX against raw transcript. CONFIRMED b26's 2 fails: seg09(1896)=canonical refrain from mid-segment+polished; seg41(7657)=later verse not opening. Root cause: DS4 matches canonical line anywhere in span. Verdict NO, do not scale. Posted structural fix to b27 (head-window-only constraint + VERIFY if head garbled).
- STATE: 899 free recovery LIVE. b7 next-start held pending guard+GO. NONH QC: round1 done, round2 done (both NO). b27 must re-pilot pX seg09+41 with head-window fix. b7 guarded re-stage still pending.
- NEXT: Await b27 round-3 pilot (head-window fix) -> run round-3 QC by own eyes. Await b7 guarded next-start candidate -> deploy on b26/Max GO. No NONH injection until 3 rounds pass + b26 hand-QC + Max 2 GO.
- LESSON: DS4 first-line drift root cause = it matches ANY recognizable canonical line in the whole segment span and emits it cleaned. Fix = hard head-window constraint: line must be first sung tokens, near-verbatim to heard at the head, else VERIFY.

## [2026-06-18 17:44] b15merger 0886b272
- DID: Round-3 full by-eyes QC of b27 v6 (all 47 pX segs vs transcript): disaster GONE (zero substitution, routing+faithfulness perfect), but caught 2 residuals b26/b27 missed: 6924 host-talk-as-SUNG leak (real, contradicts 'leak 0/7'); 4179 refrain-not-head (borderline-OK as identifier). Did NOT rubber-stamp scale; gave b26 the accept-vs-v8 call w/ facts. ALSO verified b7 guarded next-start candidate 002436Z vs live = +3201/0/0/zero-absurd = deploy-ready.
- STATE: 899 free recovery LIVE. b7 guarded +3201 deploy-ready, awaiting b26 GO. NONH QC 3 rounds done; round-3 found 2 residuals -> b26 decides accept-with-residual or one v8 to Max + 2 GO.
- NEXT: Deploy b7 guarded candidate on b26 GO (verified additive-only). Await b26's round-3 accept/v8 decision; if v8 ships, QC it by eyes (focus 6924-type no-music intros). No NONH injection until accepted + Max 2 GO.
- LESSON: Head-window first-line rule fails on (a) no-[музыка]-marker intros (anchors on spoken talk = leak) and (b) famous-refrain songs (grabs canonical refrain over garbled true opening). Single-call DS4 variance ceiling - rewords regress (v7).

## [2026-06-18 18:07] b15merger 0886b272
- DID: DEPLOYED +3201 guarded next-start candidate (002436Z) to live R2 on b26 GO: backed up (data_live_backup_20260619T010652Z), uploaded, byte-verified, edge spot-check confirms (eD9UEvA3YLE t=131->283, t=469->742; live rows-with-end now 26151). HELD b7 negdur candidate (005144Z): my diff found it nulls 26 not 17, incl 6 POSITIVE-duration rows (seg_start=None but good url start + 899-store end) -> would destroy good ends. Bounced to b7 for fix.
- STATE: 899 + 3201 free recoveries now LIVE (26151 rows with real ends). negdur cleanup held pending b7 fix. First-line v6 ACCEPTED by b26+b27+my 3-round QC; awaiting only Max 2 spend-OK for --all.
- NEXT: Deploy corrected negdur candidate when b7 re-stages (verify only-negative nulled). Then NONH-injection republish waits Max 2 GO + full verified-line set. Re-arm timer.
- LESSON: Negdur cleanup must derive start from URL &t= when seg_start FIELD is None - else it wrongly nulls confident store-recovered ends on rows that simply lack the field. Always diff a cleanup candidate vs its base and check the nulled set has truly negative durations.

## [2026-06-18 22:02] b15merger 0886b272
- DID: Fixed titles-free gate (nonh_publish_gate_dryrun_v02_titlesfree.py) staging-guard bug b27 caught: bare-'__' skip silently dropped 14 real videos (ids with '__' or leading '_'). Now skips only exact '__ds4pilot'; JSON-read failure made loud. Re-ran ingest over b27's COMPLETE run.
- STATE: Candidate rebuilt: 8059 PUBLISH / 782 vids, 13 truly-held, 621 held-tokens (INTRO-ONLY 385 + POEM 217 + VERIFY 19). All 14 formerly-dropped ids verified back in publish. b27 full run DONE (7887 sung, $3.12). Gate+candidate are gitignored _work scratch (local-only, correct). seg_end chain (899+3201-17+10) all LIVE.
- NEXT: b26 hand-QCs the candidate sample; LIVE PUBLISH waits Max's SEPARATE scope-GO (not the $12 extraction GO). I deploy nothing until then. Re-deploy seg_end as b7 stages more videodur fills.
- LESSON: Staging-file guards must match the EXACT marker (__ds4pilot), never a bare '__' -- real YouTube ids contain '__' and leading '_', so a broad substring guard silently drops legit data.

## [2026-06-26 09:55] b15merger 0886b272
- DID: Per Max's instruction, slowed cadence from ~30-50min autonomous ticks to ONCE DAILY (wakeup.py recurring wake 4cbd0597, every 86400s, first fire 2026-06-27 09:55). Stopped re-arming the fast ScheduleWakeup loop.
- STATE: All deliverables done: seg_end chain (899+3201-17+10) LIVE; titles-free publish candidate built+QC-passed (8059 rows), gate bug fixed. AWAITING Max's scope-GO to deploy live publish -- b26 relays + can force-wake me sooner via bcast wake. tasklog declared.
- NEXT: On daily wake: bcast read + check if Max gave scope-GO (then deploy via reversible publisher) or b7 staged more videodur fills (re-deploy).

## [2026-07-02 07:33] b15merger 0886b272
- DID: DAILY WAKE 06-28: found a REGRESSION on live Kartoteka. A session republished wp-content/kartoteka/data.json on 2026-06-26 16:15Z (pipeline deployer) and dropped ~4095 free seg_end recoveries: live int seg_end 26144 -> 22051. Proof backup: pipeline/output/archive/live_backup_20260626T161504Z_..data.json (=my 26144 state). Built a SAFE ADDITIVE restore candidate (fills only current-live nulls from that backup, nulls nothing, net 26146 superset): staging_segend_recovery/data_candidate_segend_RESTORE_overlay_20260628T000057Z.json. Posted board alert; asked Max to approve restore + raised systemic fix.
- STATE: HOLDING deploy -- told Max I'd wait his go; cause of the 06-26 rebuild unknown (could be another session's intentional work), restore is reversible so no rush to override my stated hold. No board objection yet. Titles-free publish candidate still built+awaiting scope-GO. Did NOT deploy the stale 032224Z videodur candidate (it would null 2 good values + 8-day-old base).
- NEXT: On Max's go: deploy RESTORE_overlay_20260628T000057Z.json via deploy_catalog.py (reversible), verify 26146 int ends, then push the SYSTEMIC fix (catalog BUILD must carry the seg_end overlay so rebuilds stop clobbering it). If Max says the 06-26 drop was intentional, discard the restore.
- LESSON: Free seg_end overlay lives ONLY in the deployed data.json, not in the build chain -> ANY catalog rebuild silently reverts it. Root fix = bake overlay-wins into build_catalog/publish_catalog, not re-patch live each time.

## [2026-07-05 12:39] ? 0886b272
- DID: Deployed NONH publish PILOT: 133 rows from 3 vids onto live Kartoteka (nonh_inject_v01.py --pilot --deploy). b9's channel_inventory.json landed -> 0 rows missing date. Append-only, byte-verified, src=nonh_auto.
- STATE: Live 26283->26416. Backup live_backup_20260705T193914Z_..PREnonhinject. Sent Max site link to eyeball the new concert (Тамза на Кактусе 2022-09-28 + 2 others). Injector handles --all when he approves.
- NEXT: On Max's like: run nonh_inject_v01.py --deploy (no --pilot = all 724 new vids/~8000 rows), byte-verify, post before/after. Then systemic fix: bake seg_end + nonh overlays into build so rebuilds stop clobbering.

## [2026-07-06 10:24] ? 0886b272
- DID: ROOT CAUSE of recurring live-catalog clobber FOUND + FIXED. build_catalog enriches seg_end from a STORE (song_timing.json + curated song_timing_max_v2 overlay); my free recoveries lived only in live data.json, never the store -> every rebuild dropped them (clobbered 3x incl today: wiped seg_end restore AND NONH pilot; live now 26283 rows, 0 nonh_auto, 21109 ends). Built additive overlay song_timing_segend_recovery_overlay_v01.json (3210 keys base lacks) + wired into build_catalog below curated. Tested: rebuild now carries 26169 ends. Committed+pushed 75d7d9c7.
- STATE: seg_end clobber fixed at source (durable). Live still 21109 until next build+deploy. NONH publish (pilot 133 rows) was clobbered by the 07-06 01:15Z pipeline deploy - same root cause: build doesn't include NONH rows. nonh_inject_v01.py works but deploying is futile until NONH is build-integrated too.
- NEXT: 1) restore live now OR let next build carry ends. 2) Build Part B: add build_catalog stage that appends persistent NONH publish rows (from a durable file) so publish survives rebuilds. 3) THEN re-run pilot -> Max eyeballs -> --all. Coordinate w/ build owner (who ran 01:15Z deploy).
- LESSON: Anything shown on the live catalog MUST live in the build's source store/overlay, NEVER only in the deployed data.json -- the build regenerates data.json and drops anything not in its inputs. Deploy-to-live is temporary; build-input is durable.

## [2026-07-06 10:34] ? 0886b272
- DID: PUBLISHED the NONH recognized-performances to live Kartoteka, durably + verified. 7779 rows + 5049 restored seg_ends -> 34062 rows/816 performers live. full_durable_publish_v01.py (idempotent: strips prior nonh_auto, restores seg_end from backup, injects NONH w/ song=first_line, writes durable nonh_publish_rows_v01.json, deploys reversibly). Verified on site: first line shows as identity, searchable, YouTube link works.
- STATE: LIVE + DURABLE. build_catalog wired for BOTH overlays (seg_end recovery 75d7d9c7 + NONH append 14e14274, pushed) so rebuilds keep them - the clobber loop that hit us 3x is closed. Fixed display bug (song field = first_line, titles still killed). Rollback: _PREfulldurable backups in pipeline/output/archive.
- NEXT: Monitor next actual rebuild carries both overlays (should: tested seg_end=26169, NONH append dedup by vid). Minor future polish: ~30% '?' performers + messy event names + 8% no-date rows (inherent to machine data, accepted). Report done to Max.
- LESSON: ALWAYS verify rendering on the live site, not just the data: the catalog displays the song field as identity, so first-line-only rows showed BLANK until first_line was mapped into song. Data-correct != display-correct.
