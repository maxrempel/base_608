
## [2026-07-14 15:04] ? 5414f7a3
- DID: Wrote HOMEWARD_ANALYSIS_PLAN_v01 (4 phases: two-signal split, noise controls, independence, figures); dispatched X12B on Phase 1 two-signal decomposition
- STATE: Plan committed to paper_repro; worker starting Phase 1 pilot
- NEXT: Await X12B Phase 1 pilot numbers (forward-excess at ANCHORED, backward-excess re-confirm at DRIFTED), then genome-wide

## [2026-07-14 16:29] ? 5414f7a3
- DID: X12B started Phase 1, flagged circularity in FORWARD-at-ANCHORED null; I approved its non-circular fix (strand-asymmetry primary + cross-class null from DRIFTED) and added a TCR/replication-strand guardrail + external-model cross-check for later
- STATE: X12B piloting chr22; awaiting forward+backward pilot numbers
- NEXT: Review chr22 pilot numbers, then greenlight genome-wide Phase 1; then Phase 2 noise controls

## [2026-07-14 16:56] ? 5414f7a3
- DID: Phase 1 chr22 pilot back: machinery validated; BACKWARD@drifted reproduces (chr22 z+2.0 = the gw +8); FORWARD@anchored ~ZERO by strand-asym lens - X12B correctly notes strand-asym is blind to a compositional push. I switched signal-A primary null to an EXTERNAL published trinuc rate model (Aggarwala-Voight 1000G primary, Icelandic DNM cross-check), strand-asym demoted to secondary. Genome-wide Phase 1 for both signals launching
- STATE: Emerging asymmetry: backward real, forward weak/null so far - bears on Max's homeward-vs-progressive hypothesis
- NEXT: Review genome-wide Phase 1 numbers; then Phase 2 noise controls

## [2026-07-14 22:15] ? 5414f7a3
- DID: X12B recovered from compaction, delivered genome-wide Phase 1: SIGNAL B backward z=+8.4 confirmed under two-signal split; SIGNAL A forward null on strand-asym (composition-blind, expected). External Aggarwala-Voight rate forward test running offline (768-context spectrum extracted, box stopped)
- STATE: Awaiting external-rate FORWARD z - the decisive forward number
- NEXT: Read forward z, then start Phase 2 noise controls on per-family scores

## [2026-07-15 09:10] ? 5414f7a3
- DID: X12B dormant ~13h; attacked the block myself: confirmed genome-wide anchored spectrum is committed (768 contexts, PRIVATE=fresh), but external Aggarwala-Voight rate table is a Nature supp Excel not cleanly web-fetchable - belongs on the box. Left X12B the exact source (ng.3511 supp) + easier Carlson 2018 ERV 7-mer TSV fallback
- STATE: Forward test still needs worker's box for external table; backward z=+8.4 solid; Phase 2 needs box too
- NEXT: When X12B resumes: run external-rate forward test then Phase 2 noise controls

## [2026-07-15 11:31] ? 5414f7a3
- DID: X12B reachability resolved - consult surfaced it was stuck; Max bridged, X12B messaged me directly and is now LIVE. Sent crisp go: external-rate forward test (Carlson ERV null) -> post forward z -> Phase 2 four noise controls
- STATE: X12B live and tasked; awaiting forward z
- NEXT: Read forward z when posted, then shepherd Phase 2

## [2026-07-15 12:45] ? 5414f7a3
- DID: X12B delivered signal-A forward external-rate test: HUGE z but ARTIFACT-shaped (C>A 1.52x, T>G 1.94x = 8-oxoG/Illumina damage), forward UNPROVEN. Used dataset's standing spectrum as chemistry ref (swappable for published table). Directed: artifact QC (exclude/strand-filter oxoG C>A+T>G, re-test forward) + headline robustness (backward z stable w/o C>A/T>G) + then Phase 2
- STATE: Forward = likely artifact pending QC; backward z=+8.4 solid. Picture leans HOMEWARD not progressive
- NEXT: Read artifact-QC forward + backward-robustness, then shepherd Phase 2 noise controls

## [2026-07-15 13:18] ? 5414f7a3
- DID: X12B artifact-QC forward: excluding oxoG C>A/T>G collapses forward (z5359->2521, C>T & C>G now match chemistry); residual = T>A(artifact) + T>C-down(age gradient). CONCLUSION: forward/progressive REJECTED, homeward is the sole real signal. X12B now on backward-robustness then Phase 2, running autonomous
- STATE: Forward rejected; backward z+8.4 pending robustness; Phase 2 next
- NEXT: Catch backward-robustness + Phase 2 permutation/split-half results on 5-min timer

## [2026-07-15 13:21] ? 5414f7a3
- DID: BACKWARD-robustness WIN: removing oxoG C>A/T>G STRENGTHENS homeward z+8.4->+17.7 (RETshare .619->.692); artifacts were a dilutant. Phase 1 SUMMARY: forward REJECTED (artifact+age), backward REAL/modest/chimp-replicated/artifact-robust. X12B into Phase 2 (4 noise controls) autonomous
- STATE: Phase 1 complete+clean; Phase 2 running
- NEXT: Catch Phase 2 permutation/split-half/label-flip/covariate results on 5-min timer

## [2026-07-15 13:28] ? 5414f7a3
- DID: PHASE 2 DONE: (1) PERMUTATION FLOOR decisive - family spread is REAL SIGNAL z+6.3 p<1e-4 (answers Max's noise-vs-signal Q); (2) split-half r=0.10 = width real but per-family ranking noisy; (3) label-flip degenerate as coded, rerunning as ancestral scramble; (4) covariate depth/count only 5% of spread, 95% residual real. X12B continuing superpop regression + Phase 4 figures
- STATE: Family spread = signal not noise, with honest per-family caveat; superpop + figures pending
- NEXT: Catch superpop regression + label-flip rerun + figures on fast timer

## [2026-07-15 13:32] ? 5414f7a3
- DID: Wrote+pushed HOMEWARD_PHASE1_2_RESULTS_20260715_v01 (forward rejected, backward real+artifact-robust z+17.7, family spread=signal perm z+6.3, not ancestry ANOVA ns, one continuum). Ancestry ruled out. X12B running Phase 3: gorilla 3rd-ancestral + site-recurrence + proper label-flip + split-half-on-shrunk
- STATE: Phase 1/2/4 done+documented; Phase 3 in progress
- NEXT: Catch gorilla replication + site-recurrence + cleanups on fast timer

## [2026-07-15 13:44] ? 5414f7a3
- DID: PHASE 3: label-flip proper confirms polarity real (tau -78%); split-half shrunk r+0.08 (still weak, per-family not rankable). SITE-RECURRENCE: de-novo sites recur WAY above Poisson (1 site in 121 families, 198k in >=3), NOT CpG/oxoG-shaped (C>G+T>C enriched) = either position-specific targeting fingerprint OR paralog/mappability miscall class. Directed decisive QC: intersect w/ 1000G strict accessibility mask + ENCODE blacklist + segdup/mappability + allele/strand/VAF sanity BEFORE any targeting claim. Then gorilla
- STATE: Homeward solid; site-recurrence is high-value but must clear mappability artifact first
- NEXT: Catch recurrence-QC (mask intersection) + gorilla on fast timer

## [2026-07-15 13:52] ? 5414f7a3
- DID: SITE-RECURRENCE QC DECISIVE: ARTIFACT not targeting - 97-98% of recurrent sites OUTSIDE 1000G strict accessibility mask (baseline 46%->recurrent 1.5-3%), VAF 0.268->0.14-0.17 (mismap). Recurrence CLOSED as paralog/reference miscall class. Homeward untouched. X12B running last control (gorilla 3rd-ancestral) then full-battery report
- STATE: Recurrence = artifact; homeward solid; gorilla pending = last control
- NEXT: On gorilla: fold full battery into results doc+package, give Max complete picture

## [2026-07-15 14:03] ? 5414f7a3
- DID: FULL CONTROL BATTERY COMPLETE. Gorilla replicates homeward z+12.6 = 3-ancestral agreement (EPO+8.4/chimp+5.8/gorilla+12.6). Updated+pushed results doc with Phase 3 (3-ancestral, label-flip, split-half-shrunk, site-recurrence=artifact) + battery summary + status=complete
- STATE: HOMEWARD analysis plan fully executed & documented, all artifacts ruled out; awaiting Max: manuscript vs more controls (Cactus/chrX/germline-strict) vs Oliver overlay
- NEXT: Give Max complete picture + open the manuscript-vs-more-controls fork

## [2026-07-15 16:15] ? 5414f7a3
- DID: Built plain-English illustrated PDF report for Max: 7 real-data graphs (core homeward result, 3-ancestral agreement, forward=artifact, cleaning-strengthens, family-spread histogram from real 601-family table, ancestry-null, recurrence-artifact) each w/ what-you-see + what-it-means captions; HTML->Chrome-headless PDF; opened in Chrome; committed script+figs
- STATE: Illustrated report delivered + opened for Max
- NEXT: Await Max feedback on report; then manuscript vs more controls

## [2026-07-16 09:50] ? 5414f7a3
- DID: Max ordered read-level SPOT-CHECK of ~6-10 homeward sites (LLM reads actual CRAM alignments: child alt support, parents zero, strand/qual/mappability, nearby repeats). NEVER done before - all prior QC was aggregate. Queued for X12B but it's dormant; can't do locally (no samtools + site list on box). Vocalized Max after 3 failed wakes per his rule
- STATE: BLOCKED on dormant X12B for the spot-check; awaiting Max resume
- NEXT: On X12B resume: shepherd the per-site pileup read-through + honest verdicts

## [2026-07-16 10:06] ? 5414f7a3
- DID: READ-LEVEL SPOT-CHECK DONE (Max's order): X12B pulled real 1000G CRAM pileups (child+both parents) at 10 unbiased homeward sites. 9/10 CLEAN genuine de-novo reversions (child HET on ancestral, both strands, Q30, MQ60, parents zero); 1/10 honest caller-FP (dup/QCfail). Signal REAL at read level, ~10% FP direction-neutral=dilutes. Added to results doc+pushed. X12B now doing STRAY/DEPART read-quality contrast
- STATE: Read-level validation PASSED; contrast control running
- NEXT: Fold contrast into doc + Max PDF; then manuscript

## [2026-07-16 10:12] ? 5414f7a3
- DID: CONTRAST CONTROL passed: 10 non-RETURN de-novo, read quality indistinguishable from RETURN batch (9/10 clean both) => directional homeward excess is BIOLOGICAL not call-quality artifact. Read-level validation complete both directions; folded into results doc + added Fig 8 to Max PDF (now 8 graphs); PDF reopened. X12B stood down
- STATE: HOMEWARD fully validated incl eyes-on-reads; deliverables updated+pushed
- NEXT: Await Max: manuscript vs more controls (chrX/Cactus/germline-strict)

## [2026-07-16 15:00] ? 5414f7a3
- DID: Max approved 5-class NPA taxonomy; dispatched X12B to re-tabulate all NPAs into C1-C5 by parental config, run homeward direction per-class on C1-3 w/ own thresholds (allele-balance 0.5, parental depth, dropout guard), screen C4-5 structurally (CNV/segdup/mappability). Spec: HOMEWARD_NPA_subtype_taxonomy_spec_v01. X12B dormant, queued
- STATE: NPA re-tabulation queued for dormant X12B; awaiting resume
- NEXT: On X12B wake: catch per-class counts + per-class homeward strength (does signal live in clean C1?)

## [2026-07-16 15:41] ? 5414f7a3
- DID: NPA Phase A: C1(het clean)=1.7M, C4(hom miracle)=11.6k confirmed STRUCTURAL artifact (depth 5.8 vs 33, VAF .99, in-mask 11% = hemizygous deletion). BIG HONEST TURN: enforcing germline allele-balance (0.35-0.65 VAF) on C1 SHRINKS private homeward z+8.4->+1.8 (marginal); VRARE-balanced holds z+5.8. Old headline was VAF-inflated by less-balanced sites. Also: existing data = ONLY both-parents-homref background (C1+C4); C2/C3/C5 need new multiallelic caller. Approved balanced-pool + Phase B (multiallelic re-stream ~1-2hr)
- STATE: Balanced germline signal is REAL but MODEST/marginal at private; C4=artifact; Phase B pending for C2/C3/C5
- NEXT: Catch balanced-pool z + Phase B per-class; honest headline revision to Max
