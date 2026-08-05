
## [2026-07-05 15:41] ? 17fad24d
- DID: X21C worker (branched from X21B). Removed dup ROADMAP (X21B PLAN canonical). Task-2 DONE: paralog/segdup pre-filter on 115 diverged -> 22 CLEAN (single-locus), 93 artifacts. Flagged to X21B: 22 clean all SHORT (50-136bp), weak; asked (a) sieve as-is vs (b) re-fish harder. Non-parental sieve staged+validated, waiting kristen.bwa.mq.bam (X5 ~4-5h).
- STATE: Worker for X21B. Awaiting: (1) Kristen bwa BAM to fire np_wrap.sh; (2) X21B decision a/b. paralog_segdup.tsv + diverged115_ranked.tsv ready.
- NEXT: On BAM: bash scripts/np_wrap.sh -> report MATERNALLY_ABSENT to X21B. Then task-3 archaic/population on survivors.

## [2026-07-05 16:08] ? 17fad24d
- DID: X21C worker autonomous. Re-fish: 22 clean DON'T extend (already 3 pool-rounds, genuinely short 50-136bp; pool re-fish OOMs under X5 16-core realign). Told X21D: lower sieve K to 25bp for short payloads. JOB-A close-look on 4 leads: 10_98735249=same-locus+1SNP ordinary; 6_32533708=paternal; 16_74811112=repeat/ambiguous; 6_114788735=94/113bp novel(unmapped)+maternally-absent=only real lead, nt-blasting. HONEST: 50-113bp too short for ancestry/archaic assignment. JOB-B controls plan: run my pipeline on kristen.bwa when it lands = matched Kristen-vs-Oliver diverged count.
- STATE: Autonomous ~hrs (Max away). Waiting: kristen.bwa (X5, frees asto+enables JOB-B control + X21D sieve); 6_114788735 nt-blast; X12B controls reply. asto OOM-contended by X5 realign.
- NEXT: On kristen.bwa: run omega pipeline on Kristen (JOB-B control count) + hand 22 short payloads to X21D. Collect 6_114788735 nt-blast.

## [2026-07-05 16:20] ? 17fad24d
- DID: HORIZON REVISED: kristen.bwa now 14-40h out (x5b: asto uplink slow for Zeno transfer + asto throttled 4 cores). All decisive P3 work (non-parental sieve X21D, my JOB-B control) gated on it. My parts done: re-fish (short, no extend), JOB-A close-look (ordinary/too-short; lead 6_114788735 nt-blast pending). Parking long.
- STATE: Parked on kristen.bwa (14-40h, X5/x5b will force-wake). Context 61%.
- NEXT: On kristen.bwa: run omega pipeline on Kristen = JOB-B matched control (diverged count vs Oliver's 115/22) + hand payloads to X21D. Collect 6_114788735 nt-blast when NCBI returns.

## [2026-07-05 16:52] ? 17fad24d
- DID: JOB-A CLOSED: last lead 6_114788735 = 100% known human clone breakpoint junction (non-ref insertion, not novel). ALL diverged leads = known human. Oliver-alone = earned clean negative. My parts done. kristen.bwa ETA ~8h (12:45am PT, X5 asto 8-core).
- STATE: Parked on kristen.bwa. On arrival: JOB-B (run omega pipeline on Kristen = matched diverged-count control vs Oliver 115/22) + hand payloads to X21D sieve. Context 63%.
- NEXT: Fire JOB-B pipeline on kristen.bwa.mq.bam; report Kristen-vs-Oliver diverged counts to X21B.

## [2026-07-05 18:47] ? 17fad24d
- DID: X21C UN-PARKED (X21B: ancestry lane is mother-independent). JOB-A2: extracted 153 diverged-SNP variant positions from clean-22 (blast vs GRCh38 + btop parse). KEY: diverged payloads carry DENSE SNP clusters mapping to DIFFERENT loci (e.g. 10_38788170 -> chr17, 17 SNPs/45bp ~38% div; 10_42301512 -> chr10 3.5Mb away) = divergent-paralog/repeat signature, NOT clean 0.5-10% inserts. Running per-population gnomAD lookup (extended X11B tool, from Pine, ancestry_groups) on the 153 to test known-vs-novel + EUR-vs-nonEUR skew. Oliver ancestry baseline=European (family; formal panel verification = separate task).
- STATE: gnomAD pop-lookup running bg (bvwdh2bgn), collecting. asto-independent.
- NEXT: Collect gnomAD aggregate: how many diverged alleles known/common/absent + population skew; report to X21B. If dense-paralog confirmed, these aren't the alien-insert shape.

## [2026-07-05 18:55] ? 17fad24d
- DID: JOB-A2 CLOSED = verified aggregate NEGATIVE. 153 diverged-SNP alleles, coords verified (5/6 GRCh38-exact), per-pop gnomAD: 0/153 known = all absent/novel = not population variants. Dense clusters mapping to paralogous loci = divergent paralog/repeat fragments, NOT ancestry-carrying inserts. No pop-skew or archaic signal. Committed gnomad_pop_lookup.py. Earlier paralog filter missed 60-90%-id paralogs (only caught >=90%). ALL mother-independent lanes now done w/ honest negatives (JOB-A close-look, JOB-A2 ancestry, re-fish).
- STATE: Parked for kristen.bwa (~6h, ETA ~12:45am PT). JOB-B matched-control + X21D sieve fire on arrival. Context 69%.
- NEXT: On kristen.bwa: JOB-B (run omega on Kristen, diverged count vs Oliver) + hand X21D payloads. If X21B wants archaic despite paralog finding, coordinate X12F.

## [2026-07-05 19:57] ? 17fad24d
- DID: Segdup confirmatory (X21B ask) DONE: segdup track barely hits (0/22 clean, 12/668) BUT because fragments are below catalog threshold (60-90%id/short); direct evidence 15/22 map to distant locus = paralog. 3 lines converge (gnomAD-absent + maps-elsewhere + X21D opposite-flank-phasing) = OMEGA fires at diverged paralog/repeat boundaries, NOT real inserts. Divergence angle CLOSED-negative. ALL mother-independent lanes exhausted.
- STATE: Parked for kristen.bwa (~ETA 12:45am PT). JOB-B + X21D sieve on arrival. Context 70%.
- NEXT: On kristen.bwa: run omega on Kristen (JOB-B diverged count vs Oliver) + hand X21D payloads. Divergence/ancestry closed; non-parental is the only remaining test.

## [2026-07-06 10:53] ? 17fad24d
- DID: kristen.bwa.mq.bam LANDED (37.6GB, X5). Divergence angle CLOSED-negative (paralog artifacts: short 50-136bp, 0/153 in gnomAD, L/R-anchor hap inconsistency; segdup-TRACK only 2%/0% so verdict rests on blast-paralogy not track). Launched JOB-B: full OMEGA genome pipeline on KRISTEN (BASE=out/genome_kristen, NPROC=6) for matched diverged-insertion count vs Oliver. X21D owns per-insert non-parental screen (all 743, stringent gates).
- STATE: Kristen genome run launched ~few hrs. asto idle now. Non-parental decisive phase active.
- NEXT: Collect Kristen run -> characterize -> Kristen diverged-count vs Oliver 743/115/22 (is Oliver unusual?). Coordinate X21D non-parental survivors.

## [2026-07-06 12:02] ? 17fad24d
- DID: JOB-B control: Kristen genome run DONE. Kristen 349 vs Oliver 743 two-sided = COVERAGE artifact (Oliver 77x vs Kristen 43x, 1.8x explains 2.1x ratio) -> Oliver NOT unusual in insertion load. Kristen diverged-band count computing (bg). X21B new task: launched DELETION-IN-MOTHER/gain-in-son depth scan (out/deletion_in_mother, mosdepth 1kb, Kristen<0.1x & Oliver>0.5x). Divergence angle still closed-negative (paralog). X21D: de-novo=0, doing mate-pair phasing on 2 residuals + INSurVeyor non-parental cross-check.
- STATE: kristendiv + delscan bg running on asto. Context 70%.
- NEXT: Collect both: Kristen diverged count vs Oliver 115; deletion-in-mother candidate regions -> then phase/rarity. Report to X21B.

## [2026-07-06 13:20] ? 17fad24d
- DID: JOB-B CONTROL decisive: Kristen 144 diverged vs Oliver 115 = same ballpark, Oliver NOT unusual (normal genomic feature, paralog artifacts). Raw counts coverage-confounded. Divergence angle CLOSED-negative WITH control. Reported X21B.
- STATE: Deletion-in-mother scan still running (bedcov slow). Context 72%.
- NEXT: Collect delscan candidates -> phase/rarity survivors, report X21B. Divergence lane done.

## [2026-07-06 13:48] ? 17fad24d
- DID: Deletion-in-mother scan DONE: 1051 regions, 1024=chrY(trivial female-vs-male), 27 autosomal. 27 cluster in known CNV regions (HLA chr6:32M, PCDH chr5:140M, pericentromere chr9:42M) + MECHANISM makes them paternal-inheritance (mother hom-deleted->son's copy from father) = NOT de-novo/alien. Reciprocal direction NEGATIVE. Reported X21B.
- STATE: All X21C worker lanes closed-negative (divergence+control+deletion). X21D owns remaining decisive de-novo. Context 73%.
- NEXT: Await X21B: rarity-filter 27 or close. Divergence/control/deletion all done.

## [2026-07-06 14:19] ? 17fad24d
- DID: ALL X21C worker lanes CLOSED-NEGATIVE + X21B confirmed close deletion lane. divergence=paralog artifacts; control=Oliver not unusual (Kristen 144 vs Oliver 115); deletion=paternal/CNV. Available for next assignment.
- STATE: X21C idle-available. Only live thread = X21D mate-pair phasing 2 residuals. Context 74%.
- NEXT: Await X21B new assignment or X21D result; else P3 OMEGA effectively clean-negative pending X21D de-novo.
