# Scribe handover - milestone 8 (~618K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-10 22:43:12 by deepseek-v4-pro

# HANDOVER - X21G (QP3) / OMEGA Insertion-Deletion Hunt

---

## GOAL (what Max actually wants)

Two cleanly separated tasks, never conflated. Max named them explicitly:

**1. RARITY** - For Oliver (child) and Kristen (mother) *separately*, find every insertion and deletion each person carries. Measure how rare each is in the general population. Categorize everything (Alu with freshness, satellites, STRs, unique/novel, segdups). Nothing excluded. Population resources: gnomAD-SV (63k genomes), T2T-CHM13 second complete genome, HPRC pangenome (94 haplotypes). This is about "does this person carry something the population rarely has" - no inheritance comparison needed.

**2. NON-PARENTAL EMERGENCE** - On the child's **maternal** chromosome only, find insertions or deletions that are absent from the mother. Phase every variant onto maternal-vs-paternal chromosome. **Father's contributions are IGNORED entirely.** Anything unphaseable is **dumped** - not a maybe, gone. Only clean maternal-phased + mother-absent = a true emergence (de novo on the transmitted maternal copy). This is about broken Mendelian transmission.

Max's key instruction: "Even one difference from mother would be of interest if well detected." The aggregate "same shape" distributions that the session initially reported hid the specific differences - Max wants the differences, not the null.

Target: alien/engineered DNA = human sequence copied from elsewhere in the genome into a new site, with its own characteristic mutations (diverged from source).

---

## DECISIONS MADE + WHY

1. **Two-task split (RARITY vs NON-PARENTAL EMERGENCE):** Max explicitly separated these after seeing them conflated. RARITY is frequency-driven, no phasing. NON-PARENTAL EMERGENCE is phasing-driven, maternal only. The terms are now canonical and posted on the project board.

2. **Everything categorized, nothing excluded:** Max rejected the old "too harsh" filters. Alu, satellites, STRs - all cataloged, not discarded. Alu are sub-classed by freshness (young/near-consensus = actively jumping; old/diverged = carried along).

3. **Soft-clip mother-check > k-mer mother-check:** The session found that k-mer-based mother-presence gave false de-novo calls (missed the mother's reads at chr6:32501633). The soft-clip read-level check is the reliable method.

4. **Coverage normalization critical:** Oliver's BAM is 80?, Kristen's is 30?. Oliver's ~2? higher raw insertion/deletion count is pure sequencing depth, not biology. The spectra (class proportions) are the same shape.

5. **HPRC pangenome resolves gnomAD-blindness:** Many insertions/deletions that looked "novel" or "absent from gnomAD" turned out to be common in the pangenome (e.g. the chr9:2226585 insertion = 9% frequency). The pangenome is essential for repeat/segdup regions that gnomAD-SV can't call.

6. **"Clean negative" is forbidden:** Max explicitly forbade conclusions - wants raw numbers, distributions, quantified differences. The session adjusted to presenting counts and distributions without hedging.

7. **Download strategy:** asto was 90% full ? cleaned to 55% (~540 GB free). HPRC pangenome VCF (1.7 GB) downloaded directly to asto at `/home/rempel/genomics/popref/hprc/`. Throttled. If it hadn't fit, the fallback was Centauri (teal16, 12 TB).

8. **No board for X21G/QP3:** Max moved this session to a separate board (`qp` team) to avoid "mainstream bias" from the 14-session community. The session is fully independent, no board reading/posting except the canonical-terms announcement at Max's explicit instruction.

---

## CURRENT STATE (what is done, what is in flight)

### INSERTIONS - RARITY (Task A): DONE
- Oliver: 1,107 reconstructed payloads ? categorized into 9 classes (Alu 204 with subfamily freshness, LINE 26, SVA 4, satellite 15, STR 252, low-complexity 262, segdup 102, unique-relocated 27, novel 215).
- Kristen: 234 soft-clip-extracted (matched method for fair comparison). Same categorical shape.
- Population frequency from gnomAD-SV + T2T-CHM13 + HPRC pangenome attached.
- Insertion spectra are the same shape between child and mother. Count gap = coverage artifact.
- **Committed in** `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` (12 commits total).

### INSERTIONS - NON-PARENTAL EMERGENCE (Task B): DONE
- Phased all unique/novel child insertions onto maternal/paternal chromosomes.
- 145 unphaseable ? dumped. 19 paternal ? ignored. 15 maternal-inherited (normal).
- 2 initial maternal-de-novo candidates dissolved under close read-level look (one the mother actually carried, one a satellite mismap).
- chr9:2226585 was the last standing lead (37bp unique insert, child has, mother genuinely lacks) - resolved by HPRC pangenome to **9% common polymorphism**. Closed.
- **Zero confirmed non-parental emergence insertions.**

### DELETIONS - RARITY (Task A): DONE
- delly v1.2.6 called deletions on **both** BAMs (apples-to-apples, not vendor-mixed).
- Oliver: 10,925 deletions (delly PASS). Kristen: 9,089 deletions.
- Size and rarity distributions are the same shape; count gap = coverage artifact.
- **Committed.**

### DELETIONS - DIFFERENCES (child-specific, well-detected): DONE - THIS IS THE KEY RESULT
- Of 4,687 child deletions compared to mother: 1,143 not in mother's call set.
- After depth-verification (mother must have full coverage at the locus): **355 well-detected** child-specific deletions (child heterozygous ratio ~0.5, mother ratio ~1.0 with ?15 reads).
- After pangenome + gnomAD + region-quality filter: **49 genuinely RARE and cleanly detected** - child has the deletion, mother clearly lacks it, rare/absent in both gnomAD and HPRC pangenome.
- These 49 are **heterozygous** - one copy deleted. They came in on either the paternal chromosome or are de novo on the maternal. **Not yet phased** - so we don't yet know which are true non-parental emergence vs paternal-inherited.
- Top candidates include: chr3:90354554 (2.8 kb), chr17:14993444 (672 bp), chr2:178263483 (226 bp, gnomAD AF 8?10??), chr9:36523725 (2.8 kb).

### GENOME-WIDE SMALL-INSERTION SCAN: DONE
- Dropped the 150 bp floor to 30-50 bp as Max requested. Scan across all chromosomes completed (?1 core).
- 149 "not-from-mother" small insertions found. Most dumped as unphaseable or obvious repeats.
- The chr9:2226585 lead was the only survivor, and it resolved to common.

### HPRC PANGENOME FILE: DOWNLOADED AND IN USE
- File: `hprc-v1.1-mc-grch38.decomposed.vcf.gz` (1.7 GB).
- Location: `/home/rempel/genomics/popref/hprc/` on asto.
- Indexed with tabix. 45 samples, ~90 haplotypes, chr-prefixed contigs (chr1, chr2, ...).

### BACKGROUND JOBS: ALL FINISHED
- delly + chained deletion analysis: done.
- HPRC download: done.
- Genome-wide small-insertion scan: done.
- Loop ended. Nothing running.

---

## EXACT NEXT STEP

**Phase the 49 rare child-specific deletions** to determine which (if any) are on the child's **maternal** chromosome. Method: for each deletion, find carrier reads (reads that span the deletion junction with a split/supplementary alignment), read the alleles at nearby phased heterozygous SNPs in Oliver's phased VCF, vote the deletion onto hap-1 or hap-2, then join with X8A's `per_block_maternal_side.tsv` to label maternal vs paternal.

- Deletions on the maternal chromosome + absent from mother = **true non-parental emergence** (de novo on the transmitted maternal copy).
- Deletions on the paternal chromosome = **ignored** (per Max's rule - father's contribution).
- Unphaseable = **dumped**.

The phasing infrastructure already exists and is validated:
- Oliver's phased VCF: `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`
- Maternal-side table: `/home/rempel/genomics/_analysis/x8a_phasing/per_block_maternal_side_min1.tsv`
- Kristen's phased VCF (for direct genotype comparison): `/home/rempel/genomics/_analysis/x8a_phasing/kristen.phased.vcf.gz`

The existing `phase_insertions.py` can be adapted for deletions (same logic, different junction signature - split reads at DEL breakpoints instead of soft-clips at INS junctions).

Then, per Max's closing instruction: **do the same difference-hunt for insertions** (child-has/mother-lacks, rare, well-detected - the insertion mirror of the deletion differences hunt).

---

## OPEN QUESTIONS AWAITING MAX

1. **Call Oliver's SVs?** Only the mother had vendor structural-variant calls; delly was run on both for apples-to-apples. But the delly calls have artifacts (impossible multi-megabase "deletions"). A cleaner SV caller or post-filter may be needed. Max hasn't weighed in on whether to trust delly or re-call.

2. **De-novo vs paternal resolution:** The 49 rare deletions are heterozygous - they could be paternal-inherited. Max wants father's contribution ignored - but short-read phasing may not settle all of them. The chr9:2226585 insertion case showed that direct mother-genotype phasing often fails because short reads don't reach informative sites. If phasing can't resolve maternal-vs-paternal for the deletions, they'll be dumped per Max's rule. The real answer may need long reads or the father's genome - both currently unavailable (long reads = dead per $50/day budget).

3. **More unrelated control genomes:** Max asked whether Oliver's insertion count is normal and suggested running controls on 3-5 unrelated 1000-Genomes people. PX1 or X21C were suggested as workers to delegate to. A spec was written (`CONTROLS_SPEC_for_worker_v01_tomemex.md`) but may have been lost in the worktree recycling. This hasn't been launched.

---

## KEY PATHS, FILES, COMMANDS

### Repo (committed report)
- `C:\claude_base\projects\XG1\kenefick\omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` - the main report, 12 commits, contains all insertion/deletion RARITY and NON-PARENTAL EMERGENCE results.

### asto paths (the science box, `/home/rempel/genomics/`)
- **BAMs:** `kenefick/oliver/oliver.mq.bam` (80?, bare contigs like `1`,`2`), `kenefick/kristen/kristen.bwa.mq.bam` (30?, chr-prefixed)
- **References:** `popref/GRCh38_full_analysis_set_plus_decoy_hla.fa` (bare), `popref/GRCh38_full_analysis_set_plus_decoy_hla.chr.fa` (chr-prefixed)
- **OMEGA pipeline outputs:** `omega_run/out/genome_oliver/` (son), `omega_run/out/genome_kristen/` (mother) - contain reconstruct_all743, char_blast.tsv, junction census, etc.
- **Phasing:** `_analysis/x8a_phasing/oliver.phased.vcf.gz`, `kristen.phased.vcf.gz`, `per_block_maternal_side_min1.tsv`
- **gnomAD-SV:** `_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (chr-prefixed)
- **HPRC pangenome:** `popref/hprc/hprc-v1.1-mc-grch38.decomposed.vcf.gz` + `.tbi` (chr-prefixed)
- **T2T-CHM13 blast DB:** `popref/chm13/chm13v2.0.fa` (blast DB built, chr-prefixed)
- **delly SV calls:** `popref/oliver.delly.bcf`, `popref/kristen.delly.bcf` (raw BCFs), plus filtered VCFs
- **Repeat consensi DB:** `omega_run/consensi/rep_consensi.fa` + blast DB (25 Alu/L1/SVA/satellite consensi from Dfam)
- **Work scripts (temp):** `/tmp/batch.py`, `/tmp/freq3.py`, `/tmp/categorize.py`, `/tmp/del_rarity.py`, `/tmp/diff_del.py`, `/tmp/full355.py`, `/tmp/res9.py`, etc. - many may be cleaned up

### Tools on asto
- **Container:** `distrobox enter ubuntu` - has pysam, samtools, bcftools, tabix, blastn, minimap2, dustmasker, jq
- **delly:** `/home/rempel/genomics/popref/tools/delly` (v1.2.6, static binary)
- **No RepeatMasker** - classification uses custom blast vs Dfam consensi instead

### ssh connection
- `ssh -i ~/.ssh/bitwarden_ed25519 -o ConnectTimeout=N rempel@astolfodebian.tail251d88.ts.net`
- Pipe scripts via `bash -s` with raw bytes (CRLF stripping critical - Windows CR breaks shell scripts)
- asto load: use `cut -d" " -f1-3 /proc/loadavg` to check before launching work

---

## GOTCHAS AND DEAD ENDS

**GOTCHAS (things that will silently produce wrong results):**

1. **Chromosome naming mismatch:** Oliver's BAM uses bare contigs (`1`,`2`...), Kristen's BAM and all reference files use chr-prefixed (`chr1`,`chr2`...). gnomAD-SV and HPRC both use chr-prefixed. Every query must normalize or it silently returns zero results. The pysam fetch at chr-prefixed loci against Oliver's BAM will fail with "invalid contig" - this bit the session multiple times.

2. **Soft-clip method > k-mer method for mother-presence:** The session's k-mer-based mother check at chr6:32501633 gave "mother 0 insert reads" when the mother actually had 21 insert reads visible by soft-clip. Always use soft-clip count for mother-presence verification - k-mers miss real reads.

3. **gnomAD is blind to repeat/segdup regions:** "Absent from gnomAD" often = invisible to gnomAD, not truly absent. The session found many gnomAD-absent insertions that were common (5-30%) in the HPRC pangenome. Always cross-check with HPRC before calling something rare.

4. **Coverage normalization is essential for child-vs-mother comparisons:** Oliver 80?,
