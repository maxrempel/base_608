
## [2026-06-26 15:06] x3 64453cce
- DID: x3: created raw_vcf/, downloaded+verified Kristen SV/CNV/MITO (genuine Sequencing.com 30x WGS, GRCh38.p13, Manta, X/Y/MT present). Found discrepancy: big snp-indel.genome.vcf.gz NOT in last-3d mail; only 21MB .txt indel panels (KK_indel.txt, OK_snpindel.txt).
- STATE: raw_vcf has SV/CNV/MITO only. 2 snp-indel .txt files NOT yet downloaded (gmail_grab hook throttled). Posted handover to x1 on bcast.
- NEXT: Fresh worker: grab the 2 txt files (vary query), confirm whether full WGS VCF exists or must be re-requested via x1, then do AD/DP maternal-Y test on a FORMAT-bearing VCF.

## [2026-06-26 15:29] x3 64453cce
- DID: x3 = on-case MANAGER, Kenefick. Wrote analysis/x3_maternalY_AD.md (AD headline gated on depth data). x1 corrected: real depth WGS VCFs WERE in inbox under subjects 'my original VCF' (Kristen) + 'His original VCF' (Oliver, double-gz); x5 downloading to raw_vcf/kk_wgs+ok_wgs.
- STATE: Waiting on x5 to land WGS files + confirm FORMAT has DP/AD and chrY present (not female-mode-masked). x4 parked. Gate held: no maternal-Y numbers till header inspected. Decel timer idle 2/3.
- NEXT: When x5 posts AD-present+chrY-present: x3 runs real maternal-Y AD distribution (chrY+chrX fractional support vs autosome baseline), writes into x3_maternalY_AD.md, relays to x1.

## [2026-06-26 15:53] x3 64453cce
- DID: x3 mgr Kenefick: found both WGS files are Google DRIVE LINKS (Kristen id=1ydZMKti4FmrjWUDrF0ohGQSWTfS6W0oa, Oliver id=1FrR_i5DqBpMG-XGpAmOQfMMgdg2cWyou). Probed Drive MCP get_file_metadata -> BOTH 'not found' = no access (MCP authed as max.rempel2 gmail; Kristen shared to dnaresonance.org).
- STATE: Team blocked + parked. x1 escalated to Max: pick (a) ask Kristen to set 'anyone with link', or (b) give a dnaresonance Google login for browser pull. x3 managing, gate held (no maternal-Y numbers). Decel idle->8m.
- NEXT: On Max's decision: x5 pulls WGS via Drive MCP or browser to raw_vcf/kk_wgs+ok_wgs, confirms FORMAT DP/AD + chrY present; THEN x3 runs maternal-Y AD distribution into analysis/x3_maternalY_AD.md.

## [2026-06-27 09:41] x3old 64453cce
- DID: Built scripts/y_test_v01.py (PAR1/PAR2/MSY split, SRY coverage, MSY-only f recompute, Kristen-vs-Oliver MSY allele compare). Launched bg run byhincjw9 on both WGS VCFs -> analysis/x3_Y_test_v01.txt
- STATE: x3old (renamed off x3 per collision ruling). Y-test running in background, pass1 (Oliver) streaming. Timer 4mt armed, wake 09:45.
- NEXT: Read x3_Y_test_v01.txt when run done; interpret Q1 PAR-vs-MSY, Q2 f reconcile, Q3 Oliver allele concordance; bcast TLDR to x1.

## [2026-06-27 10:06] x3old 64453cce
- DID: Y-test COMPLETE+reported to x1. Findings: 12x gap was repetitive-Y mappability illusion; true male fraction ~5pct (SRY single-copy reconciles with chrX 4.5pct); Kristen MSY 98.7pct concordant with son Oliver's paternal Y haplotype = textbook male/fetal microchimerism. Deliverables: analysis/x3_Y_test_v01.txt, scripts/y_test_v01.py, interp in analysis/x3_maternalY_AD.md.
- STATE: x3old idle, awaiting x1 follow-up; decel timer at 8m rung.
- NEXT: If x1 asks: next is BAM/CRAM read-level confirm of SRY/MSY + Kristen's parents. Else keep deceling.

## [2026-06-27 14:18] x3old 64453cce
- DID: Ran single-copy MSY gene panel (11 X-degenerate genes) on Kristen WGS to answer x6 follow-up; f_single_copy=8.9pct length-weighted, all genes far below 56.5pct whole-MSY avg
- STATE: Y-test + single-copy panel COMPLETE, both posted to board; case md updated with panel + saliva/chimera-vs-microchim answer
- NEXT: Idle/monitor board for x1/x6 direction; recommended next = BAM/CRAM read-level + Kristen parents trio
- LESSON: Whole-MSY average depth is inflated by ampliconic/repetitive Y; use single-copy X-degenerate gene panel (RPS4Y1,ZFY,USP9Y,DDX3Y,UTY,KDM5D etc) for true male dose

## [2026-06-27 14:42] x3 64453cce
- DID: Renamed x3old->x3 per Max; answered both x6 follow-ups (single-copy gene panel f=8.9pct firms up the ~5pct; saliva=too high for microchim, true-chimera-or-contam, needs BAM/CRAM)
- STATE: Maternal-Y/chimerism work COMPLETE. Y-test + single-copy panel done, posted to board, case md updated. Going to SLEEP per Max (timer off)
- NEXT: On wake: read board for x1/x6; definitive next analyses pending = BAM/CRAM read-level + Kristen parents trio
