# Scribe handover - milestone 9 (~677K tokens)
# session: 20260711_jolly_austin_dd9aa0_aa619d47
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-11 07:09:24 by deepseek-v4-pro

# HANDOVER - OMEGA Insertion/Deletion Analysis (Session X21G ? QP3)

---

## GOAL (in Max's own words)

Max has **two separate questions**, and I was conflating them. The correction at the end is the load-bearing instruction:

**QUESTION 1 - NON-PARENTAL ALLELES (non-parental modifications).**
"First we are testing the non-parental alleles, insertions or deletions in the child, resolving phasing." Take **every** child variant (insertion and deletion) that the mother lacks, phase it onto the maternal haplotype, and report **all** that land on the maternal copy. The only two gates: (a) it resolves through phasing, (b) it's on the maternal haplotype. **No rarity filter. No editorializing about which are "surprising."** If nothing survives phasing ? question solved, done.

**QUESTION 2 - RARE VARIANTS.**
"Either child or mother having rare variants which are not present in databases." Does the child OR the mother carry insertions/deletions absent from population databases (gnomAD, T2T-CHM13, HPRC pangenome)? No phasing, no inheritance - just rarity per person. All variants included, no exclusions.

Max's exact words: "don't decide for me which variants are surprising or not surprising - all the variants I'm interested in, absolutely all, no exclusion, no exception."

---

## DECISIONS MADE + WHY

1. **The two questions are SEPARATE - never mix them.** Rarity belongs to Q2 only. Q1 has no rarity gate. Max corrected the earlier analysis that pre-filtered Q1 to "rare" before phasing - that was wrong.

2. **Phasing methodology:** Use the existing whatshap phased VCF for Oliver (`oliver.phased.vcf.gz`), X8A's per-block maternal-side table (`per_block_maternal_side_min1.tsv`), and soft-clip reads at each insertion/deletion locus to vote the haplotype. For deletions, the junction positions (start/end) are used; for insertions, the soft-clip reads at the insertion point carry the phase-informative hets.

3. **Father ignored entirely.** Anything that can't be confidently phased to the maternal side is dumped, per Max's rule: "if you can't define the faith, dump them."

4. **Mother BAM:** `kristen.bwa.fixed.bam` (~30? coverage, bare contig names). Oliver BAM: `oliver.mq.bam` (~80? coverage, bare contig names). The coverage difference (~2.6?) explains raw count differences - not biology.

5. **Population resources used:**
   - gnomAD-SV v4.1 (`gnomad_sv_v4.1.sites.vcf.gz` - 63k genomes, chr-prefixed)
   - T2T-CHM13 second complete genome (blast DB)
   - HPRC v1.1-mc pangenome VCF (`hprc-v1.1-mc-grch38.decomposed.vcf.gz` - 94 haplotypes, chr-prefixed)
   - All live on asto under `/home/rempel/genomics/popref/`

6. **SV caller for deletions:** delly v1.2.6, called on both BAMs (matched to correct reference with bare contig names). PASS-only calls.

7. **Clean framing:** Variants the child has that the mother lacks are "differences of unknown parental origin until phased" - not "could be paternal" hedging.

---

## CURRENT STATE

**Question 1 (corrected) - IN FLIGHT.**
I launched `q1_nonparental.py` on asto at the end of the session. It:
- Detects ALL child-specific insertions (via soft-clip reads) and deletions (via delly calls) that the mother lacks (mother has good coverage but no variant)
- Phases every one onto the maternal haplotype using the existing phased VCF + maternal-side table
- Outputs the raw maternal-phased set (no rarity filter)
- Running in tmux session `q1_chain`, writing to `/home/rempel/genomics/popref/q1_result.txt`
- **Status at session end: still running** (the collector was waiting for `Q1_CHAIN_DONE`)

**Question 2 - PARTIALLY DONE, NEEDS CLEAN CONSOLIDATION.**
- Child insertions: fully categorized (1,107 into 9 classes), frequencies checked against all three databases
- Child deletions: delly called (10,925 PASS), frequencies checked against databases
- Mother insertions: soft-clip catalog built (234 classified), comparable to child's
- Mother deletions: delly called (9,089 PASS)
- **Not yet done:** a single clean table showing "child rare/novel variants" + "mother rare/novel variants" - the insertion side is mostly there, the deletion side needs the same rare/novel extraction (no phasing)

---

## EXACT NEXT STEP

1. **Check Q1 status:** `grep Q1_CHAIN_DONE /home/rempel/genomics/popref/q1_result.txt`. If not done, wait on the tmux session `q1_chain`. 
2. **When Q1 finishes:** Read the raw maternal-phased list - these are the non-parental allele candidates. No rarity filter, no judgment. Present them all.
3. **Then complete Q2:** Extract rare/novel insertions and deletions for child AND mother separately - filter to "absent from gnomAD AND absent from HPRC pangenome AND absent from T2T-CHM13." Present as a clean table per person.
4. Append both to the report at `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` and commit.

---

## OPEN QUESTIONS AWAITING MAX

- **Deletions for Q2 on the mother:** need to confirm whether the existing delly calls on Kristen are sufficient or need filtering (the raw set has some delly artifacts with impossible multi-megabase sizes).
- **Oliver has no vendor SV VCF** - only Kristen does. For apple-to-apple deletion comparison we used delly on both, which is correct. But the early deletion work was gated on this.
- **Centauri download:** you mentioned it, but the HPRC file fit on asto (1.7 GB, 55% free = ~575 GB), so no Centauri was used.

---

## KEY FILE PATHS & IDs

**BAMs (asto):**
- Oliver: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (80?, bare contigs)
- Mother: `/home/rempel/genomics/kenefick/kristen.bwa.fixed.bam` (30?, bare contigs - **NEVER delete this file**, I depend on it)

**Phasing data (asto):**
- `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`
- `/home/rempel/genomics/_analysis/x8a_phasing/per_block_maternal_side_min1.tsv`

**Population databases (asto):**
- gnomAD-SV: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (chr-prefixed)
- HPRC pangenome: `/home/rempel/genomics/popref/hprc/hprc-v1.1-mc-grch38.decomposed.vcf.gz` (chr-prefixed, indexed)
- T2T-CHM13: `/home/rempel/genomics/popref/` (blast DB)

**Detection outputs (asto):**
- Oliver insertions: `/home/rempel/genomics/omega_run/out/genome_oliver/`
- Mother insertions: `/home/rempel/genomics/omega_run/out/genome_kristen/`
- BLAST results: `char_blast.tsv` (query_id, qlen, pident, aln_len, etc.)

**Delly outputs (asto):**
- Oliver: `/home/rempel/genomics/popref/oliver_delly.bcf`
- Mother: `/home/rempel/genomics/popref/kristen_delly.bcf`

**Q1 active output:** `/home/rempel/genomics/popref/q1_result.txt`

**Scripts (local, transfer to asto):**
- Categorizer: `scratchpad/categorize.py`
- Deletion rarity: `scratchpad/del_rarity.py`
- Deletion difference-hunt: `scratchpad/diff_del.py`
- Full 355 filter: `scratchpad/full355.py`
- Insertion difference-hunt: `scratchpad/ins_diff.py`
- Q1 corrected (in flight): `scratchpad/q1_nonparental.py`
- Phasing: `scratchpad/phase_del.py`, `scratchpad/phase_ins15.py`, `scratchpad/phase_chr22.py`

**Report:** `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` (14 commits)

**Repeat consensi:** `/home/rempel/genomics/popref/repeats/` (Alu subfamilies young?old, L1, SVA, satellites - blast DB built)

**Contig naming convention:** Oliver BAM uses bare contigs (`1`, `2`, ...); population VCFs use `chr1`, `chr2`. Always normalize when querying.

---

## GOTCHAS & DEAD ENDS

1. **Do NOT pre-filter Q1 by rarity.** That was Max's key correction at the end. Q1 = all child-specific variants phased to maternal, nothing else.

2. **chr-prefix mismatch:** gnomAD-SV and HPRC use `chr1`; Oliver's BAM uses `1`. Always add/remove prefix when querying.

3. **Mother coverage caveat:** Kristen is 30? vs Oliver's 80?. A "mother lacks" call at low coverage may be a caller sensitivity gap, not a real difference. Guard with minimum coverage threshold (~15 reads).

4. **Pericentromeric/satellite artifacts:** Any variant in a pericentromeric region (elevated low-MAPQ reads, satellite sequence like GGAAT/CATTC) is likely a mismapping artifact - even if it looks "private." The chr17, chr20, and chr22 pericentromeric leads all resolved this way.

5. **Conflation of Alu freshness:** Young Alu (AluY, near-consensus) are actively jumping elements. Old Alu (AluJ, diverged) are dead copies carried in segmental duplications. Both are categorized, but only young ones are meaningful "jumps."

6. **delly artifacts:** Some delly calls show impossible multi-megabase "deletions" - these are imprecise/translocation artifacts. Filter by size (cap at reasonable) before trusting.

7. **astro compute cap:** ?4 cores. asto freed up to 55% disk (~575 GB). distrobox container `ubuntu` has pysam, samtools, bcftools, tabix, minimap2.

8. **CRLF issue:** Scripts written on Windows must be stripped of `\r` before running on asto - send via raw-bytes SSH pipe, never via `cat > file` with Windows line endings.

9. **HPRC queries are positional:** The pangenome VCF uses decomposed records - a 300 bp Alu insertion may not match an exact-position query. HPRC is reliable for *positive* hits (found = present) but undercalls negatives (absent may just mean unrepresented at that exact coordinate). Use for confirmation, not disproof.

10. **The father bottleneck:** Without the father's genome, "maternal side" labels from X8A's per-block table can flip. Maternal calls with low confidence (<0.5) should be treated as unphaseable. This is the honest ceiling on Q1 - short reads + no father = many events won't phase.
