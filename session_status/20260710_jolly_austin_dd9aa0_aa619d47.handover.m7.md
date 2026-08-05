# Scribe handover - milestone 7 (~530K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-10 15:29:32 by deepseek-v4-pro

# HANDOVER - P3 OMEGA: Alien/Engineered Insertion Detection (X21G / QP3)

## GOAL (in Max's words)

Find alien/engineered DNA insertions in **Oliver** (the experiencer's son) vs his mother **Kristen Kenefick**. The target class: a **human sequence copied from somewhere else in the genome into a NEW site, with IMPERFECT homology** - its own characteristic mutations. "Aliens are distant human relatives," so an insertion is a relocated-and-diverged human piece, not foreign DNA.

Max wants **two completely separate analyses, never conflated:**

1. **RARITY vs population** - for child AND mother separately. Catalog **every** insertion/deletion each person carries (nothing excluded), categorize them (Alu with freshness/age, LINE, SVA, satellite, STR, low-complexity, segdup, unique/novel), and measure how rare each is in the population. "I'm interested in all classes. Don't just ignore them because they're convenient to ignore."

2. **NON-PARENTAL, maternal-phased ONLY** - phase the child's insertions. Keep only the ones cleanly phased to the **maternal** chromosome. Dump everything unphaseable ("if you can't define the faith, just dump them"). Flag any that sit on the maternal haplotype but are absent from the mother = de-novo on maternal copy. **Fathers ignored entirely** - no hedging about "could be paternal."

He also wants: **no conclusions** in his absence, just data and quantification. Graphs eventually, but numbers and words now. Download any missing data properly. Cap at ?4 CPU cores on asto.

---

## DECISIONS MADE + WHY

### 1. Split into two independent analyses (Max's reframe)
Max explicitly called out conflation of "rarity of insertions/deletions compared to general population" with "lack of Mendelian transmission." These are now tracked and reported separately.

### 2. 150bp size floor dropped ? 30-50bp small-insertion scan
Max questioned the floor twice. Pilot on chr22 confirmed it was hiding real candidates. Genome-wide scan completed.

### 3. Mother-presence test uses soft-clip detection, NOT k-mers
A k-mer-based mother check gave **false de-novo positives** (missed the mother's reads on chr6:32501633, chr17:21871982). The reliable method: go to the exact coordinate in the mother's BAM and count reads that soft-clip into the same inserted sequence vs reads that cross cleanly. This matters for every future mother-check.

### 4. Categorizer built from real repeat-family consensi, not k-mer heuristics
Fetched 25 Alu/L1/SVA/satellite consensus sequences from Dfam, built a local blast database, classify every insert by blast identity to the consensi. Alu sub-class by age (AluY ? young/active, AluS ? mid, AluJ ? old/dead). STR and low-complexity detected via k-mer diversity.

### 5. Population frequency from TWO sources
- **gnomAD-SV v4.1** (63k genomes, on asto) - works but blind to segdup/repeat regions.
- **HPRC v1.1-mc-grch38 decomposed VCF** (94 haplotypes, just downloaded to asto) - resolves carrier frequency in repeat regions gnomAD can't see.

### 6. delly launched for deletion analysis (apples-to-apples)
The mother has vendor SV calls but the child doesn't, so direct comparison is impossible. Decision: run the *same* SV caller (delly v1.2.6) on both BAMs for a matched deletion comparison.

### 7. Child-vs-mother insertion count difference is COVERAGE, not biology
Oliver's BAM is ~80?, mother's is ~30?. The ~2? higher insertion count in the child is fully explained by sequencing depth. When using identical soft-clip extraction methods, the insertion *spectra* (class distributions) are the same shape.

### 8. chr12:30348820 "top candidate" demoted
Ranked #1 for alien potential (unique sequence, 23.7% diverged, relocated 100kb on chr12). But: it's **homozygous** in the son (both chromosome copies carry it = inherited from BOTH parents, not de-novo), the mother carries the identical sequence letter-for-letter, and it's an old segmental duplication. Max caught the homozygous error - correct alien shape is heterozygous-in-son + absent-in-mother.

---

## CURRENT STATE - WHAT IS DONE

### Analysis 1 (Rarity, categorized) - COMPLETE for insertions
- Child: 1,107 inserted payloads reconstructed and categorized into 9 classes.
- Alu (204): sub-classed by age - ~65 young/active (AluYb8/AluYa5/AluY), ~115 mid-age (AluS*), ~24 old (AluJ*).
- STR/tandem: 252. Low-complexity: 262. LINE/L1: 26. SVA: 4. Satellite: 15. Segdup/multicopy: 102. Unique-relocated: 27. Unclassified/novel: 215.
- Population frequency attached (gnomAD-SV v4.1 + CHM13 presence): most classes overwhelmingly COMMON. ~50 insertions are both unique/novel-class AND rare/novel in population.
- Mother: soft-clip catalog built (349 two-sided loci, 234 classified). Comparable spectrum to child.
- **HPRC pangenome VCF downloaded** (~1.7 GB to asto) - pending processing to fill the gnomAD-blind repeat-region gap.

### Analysis 2 (Non-parental, maternal-phased) - COMPLETE, zero confirmed de-novo
- Child's unique/novel insertions (242) phased against whatshap phase blocks + maternal-side table.
- 145 unphaseable ? dumped (per Max). 19 paternal ? ignored. 15 maternal-inherited. 2 maternal-de-novo candidates appeared but **both dissolved under close read-level look** (chr6:32501633 - mother actually has it, k-mer check was wrong; chr17:21871982 - satellite mismap artifact).
- **Genome-wide small-insertion (30-50bp) scan completed**: 149 not-from-mother candidates ? phased ? 4 maternal-de-novo surfaced. 3 were obvious repeats, 1 looked real:
  - **chr9:2226585** - 37bp unique insert (`TGCCACTAAACTATAATCACCACAAGGAGCAAGCCAA`), son heterozygous (10 insert / 54 clean), mother genuinely absent (0 insert / 40 clean), 87.5% identity to a chr5 locus. But **maternal-side phasing confidence is only 0.500** (coin-flip) and **direct mother-genotype phasing failed** (short reads don't reach the informative heterozygous sites). Unresolvable with short reads ? dumped. **This is the single locus to revisit if long-read data or the father's genome ever becomes available.**
- **Bottom line: zero confirmed non-parental insertions.** The limiter is short-read phasing + no father, not absence of biology.

### Deletions - IN FLIGHT
- delly v1.2.6 launched on **both** BAMs (Oliver first, then Kristen), ?4 cores, sequential.
- Running detached in background (tmux session or nohup).
- When finished: build matched child-vs-mother deletion comparison, categorized by size and population frequency.

### HPRC pangenome frequencies - PENDING PROCESSING
- File: `hprc-v1.1-mc-grch38.vcfbub.a100k.wave.vcf.gz` at `/home/rempel/genomics/popref/`
- Download completed (1.7 GB).
- Needs: tabix index (if not already), then query all 1,107 insertions against the 94-haplotype carrier count ? real frequency for the gnomAD-blind repeat/segdup insertions.

### Infrastructure
- Everything on **asto** (astolfodebian.tail251d88.ts.net), user rempel.
- pysam/tabix/minimap2/blastn live in the `ubuntu` distrobox container ? all python scripts must be invoked as `distrobox enter ubuntu -- python3 /path/to/script.py`.
- BAMs: Oliver = `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (bare chromosome names `1`,`2`,...), Kristen = `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` (chr-prefixed names `chr1`,`chr2`,...).
- Phasing data: `/home/rempel/genomics/_analysis/x8a_phasing/` - `oliver.phased.vcf.gz`, `kristen.phased.vcf.gz`, `per_block_maternal_side_min1.tsv`.
- gnomAD-SV: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (uses `chr` prefix).
- T2T-CHM13: `/home/rempel/genomics/popref/chm13v2.0.fa` + blast DB.
- Consensi DB: `/home/rempel/genomics/omega_run/out/repeat_consensi/` (25 Alu/L1/SVA/satellite consensus sequences + blastn DB).
- Omega detection outputs: `/home/rempel/genomics/omega_run/out/` - `genome_oliver/` (reconstructed payloads, blast results, junction census), `genome_kristen/` (junction census only, payloads not assembled).
- Report: `C:\claude_base\projects\XG1\kenefick\omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` (9 commits, pushed).

---

## BACKGROUND JOBS RUNNING

1. **delly SV-calling**: Oliver first, then Kristen. Check status with `tail /tmp/delly_oliver.log` and `tail /tmp/delly_kristen.log` on asto. ETA: a few hours at ?4 cores.

---

## EXACT NEXT STEP (when session resumes)

1. **Check delly progress**: `tail /tmp/delly_oliver.log` and `tail /tmp/delly_kristen.log` on asto. If both finished, build the categorized child-vs-mother deletion comparison - del calls split by size (30-50bp, 50-500bp, 500bp-5kb, >5kb), each checked against gnomAD-SV + HPRC for carrier frequency.

2. **Process HPRC pangenome VCF**: tabix-index it (if needed), then query all child insertions against the 94-haplotype panel ? real carrier counts for the repeat-region insertions gnomAD couldn't resolve. Append to the report. This fills the one remaining gap in Analysis-1.

3. **Update the combined report**: append the deletion comparison and HPRC frequencies to `INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md`, commit, push.

---

## OPEN QUESTIONS AWAITING MAX

1. **Deletions**: I launched delly on both BAMs (Max said "ok go ahead"). This is running. When done, I'll present the child-vs-mother deletion comparison - no decision needed, just delivery.

2. **Download target**: HPRC VCF was downloaded to asto (it fits - 1.7 GB, 575 GB free). Done. No Centauri needed.

3. **chr9:2226585**: the one small-insertion lead. 37bp, unique sequence, son-has-mother-lacks, but unresolvable maternal-vs-paternal phase with short reads. **If long-read data or the father's genome becomes available, this is the top locus.** No action possible now.

---

## KEY PATHS

- Repo: `C:\claude_base\projects\XG1\kenefick\omega_detector\`
- Report: `INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md`
- asto BAMs: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (bare contigs), `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` (chr-prefixed)
- asto omega outputs: `/home/rempel/genomics/omega_run/out/genome_oliver/` and `genome_kristen/`
- Phasing: `/home/rempel/genomics/_analysis/x8a_phasing/`
- gnomAD-SV: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz`
- HPRC pangenome: `/home/rempel/genomics/popref/hprc-v1.1-mc-grch38.vcfbub.a100k.wave.vcf.gz`
- Consensi DB: `/home/rempel/genomics/omega_run/out/repeat_consensi/`
- delly binary: `/home/rempel/genomics/popref/tools/delly`
- delly logs: `/tmp/delly_oliver.log`, `/tmp/delly_kristen.log`

---

## GOTCHAS AND DEAD ENDS

- **k-mer mother-check is unreliable**: gave false de-novo positives because it missed the mother's reads. Always use the **soft-clip junction scan** on the mother's BAM at the exact coordinate. Method: count soft-clipped reads carrying the same inserted sequence vs clean-crossing reads.

- **Chromosome naming mismatch**: Oliver's BAM uses bare contigs (`1`, `22`), Kristen's uses `chr1`, `chr22`, gnomAD-SV uses `chr1`. Every query must match the target's convention. Past bug: pysam `fetch('12', ...)` silently returned nothing because gnomAD uses `chr12`.

- **gnomAD-SV is blind to segdup/repeat regions**: 32 of 47 relocations returned "absent" from gnomAD because gnomAD doesn't call well there. The HPRC pangenome VCF is the solution. Do not interpret gnomAD-absent as "rare" for a repeat-region insertion - it's "unreadable."

- **Homozygous insertion = COMMON, not alien**: a homozygous insert means both of the child's chromosome copies carry it ? inherited from both parents. The alien shape is **heterozygous-in-son + absent-in-mother**. Don't rank homozygous inserts as top picks (chr12:30348820 was this mistake).

- **Mother's lower coverage (30? vs son's 80?)**: the mother's cleaner readouts are partly just fewer reads. Low-count "absent-in-mother" calls need a coverage guard per the advisor (X8A?). chr9:2226585 had 40 clean mother reads so it's safe.

- **All Python must run inside the `ubuntu` distrobox container**: `distrobox enter ubuntu -- python3 /path/to/script.py`. Host Python lacks pysam/tabix.

- **CRLF line endings**: These are Windows-CRLF line endings. Always strip CR via `tr -d '\r'` or write scripts in Python to avoid shell quoting bugs.

- **asto guest-resource caps**: ?4 CPU cores, keep disk below 90%. Network throttled to ~50% of line speed for bulk downloads.

- **Online NCBI BLAST dead end**: The remote BLAST (`blastn -remote`) never returned from the guest box - likely outbound-throttled. Don't use it. The local blast against CHM13 and repeat consensi is sufficient.

- **Two-sided junction needed for reliable insertion**: insertions detected by one-sided soft-clips alone are often alignment artifacts. The chr16?10 candidate (chr10:38823515) appeared in the blast data but had **no real read-level junction** - assembly artifact.

- **Session name**: Max renamed me from X21D ? QP3 ? X21G across branches. Current identity is **X21G** on the `jolly-austin-dd9aa0` worktree. The board is disconnected (Max moved me to an independent board to avoid conservative peer influence).
