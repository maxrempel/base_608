# Scribe handover - milestone 6 (~475K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-10 12:14:12 by deepseek-v4-pro

# HANDOVER - OMEGA P3 alien-insertion hunt, X21G (was QP3, was X21D)

---

## GOAL (Max's own words, verbatim from the reframe turn)

> "I don't mind the insertion of the human sequence from one another place of the genome into the new place in the genome. That's also interesting... a human insertion but present elsewhere in the genome, but deviate by imperfect homology, some mutations anomalies variations."

> "Aliens are distant relatives... I'm interested in normal human pieces jumping... your task was to show if there were human jumps and measure, quantify the diversions of human insertions from the original."

**Latest reframe (this session, near the end):**
Max told me I was conflating two separate questions. He split them cleanly:

1. **RARITY vs the general population** - for both Oliver (child) and Kristen (mother) SEPARATELY. Take every insertion/deletion each carries, categorize ALL of them (nothing excluded - Alu, STR, satellite, segmental duplications, novel), and ask how rare each is in the population. For Alu, check "freshness" (consensus vs diverged - only young consensus Alu actively jumps; diverged ones are old/interesting). For every repeat, look at the actual sequence. This is NOT about inheritance.

2. **NON-PARENTAL, maternal-phased only** - phase the child's insertions to the maternal vs paternal chromosome. Keep only cleanly maternal-phased ones; dump everything unphaseable (fine to lose data). Fathers ignored entirely - no more "could be paternal" hedging. If it can't be phased, it's gone. Among maternal-phased ones, flag any absent from the mother = de-novo on the transmitted maternal copy.

Also: deletions should be cataloged too, not just insertions.

---

## DECISIONS MADE + WHY

### 1. "Clean negative" was wrong - Max's correction
When Max first asked for results, I hedged with "clean negative." Max was furious - said clean negative doesn't exist in real data, it's a mainstream-biased conclusion, not real work. He demanded quantitative distributions (how many, what divergence) not conclusions. **I dropped hedging entirely and switched to presenting distributions, numbers, and raw data.** This was a turning point.

### 2. The two analyses are SEPARATE - never mix them
Per Max's explicit instruction. Rarity (population frequency) and non-parental (maternal de-novo) are independent questions with different methods. I was mixing them before; Max corrected this.

### 3. Soft-clip method for mother-presence, NOT k-mers
K-mer-based mother-check gave 2 false de-novo candidates. The reliable method: go to the exact coordinate in the mother's reads and count **soft-clipped reads** (dangling = she has the insert) vs **clean-crossing reads** (she doesn't). K-mers missed the mother's reads in the MHC/HLA region. **Soft-clip is now the standard.**

### 4. Close read-level look is mandatory - "pilot QC discipline"
Every candidate that looked promising dissolved under the microscope. chr12:30348820: reads showed 100% agreement across all ~100 reads = single clean inherited insertion. chr10:38788170: satellite repeat, mother had it. Two maternal-de-novo candidates: both false positives (mother actually carries them, seen in soft-clips). The 2 chr22 small-insertion leads: phasing unresolvable, dumped. **Max insists on actually looking at the reads, and it's been correct every time.**

### 5. Size floor was too harsh - 30-50 bp class never scanned
Max flagged the 150 bp floor as questionable. I ran a pilot on chr22 and found 2 "not-from-mother" small insertions the big-pipeline completely missed (39 bp and 32 bp). These validated his instinct. **The genome-wide small-insertion scan is now running in background.**

### 6. asto disk full - downloads route to Centauri
asto (astolfodebian) is at 90% full (~130 GB free), below the guest-box floor. Big downloads (HPRC pangenome) must go to **Centauri** (teal16, ~12 TB free). Small things (repeat consensi) are fine on asto. Max confirmed: download properly, no rush.

### 7. Categorizer built - blast vs 25 repeat consensi
Instead of RepeatMasker (not installed), I fetched 25 Alu/L1/SVA/satellite consensus sequences from Dfam API, built a local blast DB, and built a classifier: blast each insert ? identify family (AluY/AluS/AluJ/L1/SVA/satellite) ? measure % identity to consensus (freshness) ? detect STR/low-complexity ? measure copy number (segdup vs unique). This gives the proper Alu freshness classification Max wants.

### 8. Child-vs-mother count difference is coverage, not biology
Oliver BAM is ~80? depth, mother's is ~30?. The ~2.6? coverage ratio fully explains Oliver's ~2? higher raw insertion count. Coverage-normalized, the spectra are the same shape. This was confirmed by sampling chr22 coverage.

---

## CURRENT STATE

### Analysis 1 (Rarity, both people, categorized) - DONE for the child, IN PROGRESS for the mother

**Child (Oliver) - full catalog built:**
- 1,107 total reconstructed insertions ? categorized into 9 classes
- 204 Alu, sub-classed by age: ~65 young/active (AluYb8, AluYa5, AluY), ~115 mid (AluS*), ~24 old/dead (AluJ*)
- 215 novel/unclassified, 27 unique-relocated, 262 low-complexity, 252 STR, 102 segdup, 26 LINE/L1, 15 satellite, 4 SVA
- Population frequency attached: gnomAD-SV (63k genomes) + T2T-CHM13 presence
- Most classes = common. The unusual bucket: ~50 unique/novel insertions absent from BOTH reference genomes

**Mother (Kristen) - soft-clip catalog built, but not a full assembly catalog:**
- 349 two-sided insertion loci detected (vs Oliver's 743 - depth difference)
- Soft-clip fragments extracted (~60 bp, not full ~300 bp assembled payloads)
- **Method-comparability problem flagged:** mother's short clip fragments can't match full Alu consensi, inflating her "non-repeat" count. For fair comparison, both must use the SAME method.
- Matched soft-clip comparison (both people) shows: distributions are nearly the same shape.

**Mother full assembly NOT YET DONE** - she has per-chromosome junction hits but no reconstructed payloads. Needs the `reconstruct` step run identically to the son's pipeline.

**Deletions - NOT YET DONE.** Only the mother has vendor SV calls (4,227 deletions, 1,731 insertions); Oliver has no SV VCF. Would need to call Oliver's SVs for a fair comparison.

### Analysis 2 (Maternal-phased non-parental) - DONE, result: ZERO confirmed
- Phased 242 child unique/novel insertions: 145 unphaseable (dumped), 19 paternal (ignored), 15 maternal-inherited, 2 maternal-de-novo candidates
- Both 2 candidates dissolved under close read-level look: one mother actually carries (k-mer miss), one satellite mismap
- 2 chr22 small-insertion leads also dumped: one phases cleanly but can't label maternal side (no father), one completely unphaseable
- **Bottom line: no confirmed de-novo-on-maternal insertion found**

### Small-insertion (30-50 bp) genome-wide scan - RUNNING IN BACKGROUND
Launched as a background job on asto (in the ubuntu distrobox container). Scanning all chromosomes for "not-from-mother" small inserts. Not yet collected.

### Frequency/size report - COMMITTED
File: `C:\claude_base\projects\XG1\kenefick\omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md`
Contains the full Analysis-1 child catalog, Analysis-2 results, coverage note, and small-insertion pilot addendum. Seven commits in.

---

## EXACT NEXT STEP (autonomous, no Max needed)

1. **Check the genome-wide small-insertion scan** - collect results, verify survivors with soft-clip method, attempt phasing on any not-from-mother ones.
2. **Rebuild mother's full assembled catalog** - run the same `reconstruct` pipeline on her two-sided loci that was run on Oliver, so we have comparable payload-level classifications (not just short soft-clip fragments). This fixes the method-comparability problem.
3. **Attach population frequency to the mother's catalog** - same gnomAD-SV + CHM13 check already done for the son.
4. **Consolidate into a proper categorical report** - the 9-class breakdown with rarity, for BOTH people, with the Alu-freshness sub-analysis Max specifically asked for.

**Two decisions that need Max (waiting):**
- Run SV calling on Oliver for deletion comparison? (Heavy job - only the mother has vendor SV calls)
- Download HPRC pangenome to Centauri for better repeat-region carrier-frequency resolution?

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Deletions:** call Oliver's SVs or just report the mother's? (Max said "deletions too" but Oliver has no SV calls yet - this is a real compute decision, not a trivial step.)
2. **HPRC download to Centauri:** Max said "download properly" - confirm Centauri (teal16) is the right target. The data would let me resolve carrier frequency for the 32 gnomAD-blind repeat-region insertions.
3. **Long-read:** Max killed long-read earlier due to $50/day budget, but this session proved short-read phasing is the hard ceiling for the non-parental analysis - most insertions are unphaseable. Worth revisiting if budget changes?

---

## KEY FILES, PATHS, AND COMMANDS

### On asto (astolfodebian.tail251d88.ts.net, SSH key: ~/.ssh/bitwarden_ed25519)
- **Son BAM:** `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (bwa, ~80?)
- **Mother BAM:** `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` (realigned, ~30?)
- **Son detection output:** `/home/rempel/genomics/omega_run/out/genome_oliver/`
  - Junction census: `JUNCTION_CENSUS_v2_annotated.tsv`
  - Reconstructed payloads: `reconstruct_all743/` (1,107 payloads)
  - Blast results: `reconstruct_all743/char_blast.tsv` (payload ? human genome)
- **Mother detection output:** `/home/rempel/genomics/omega_run/out/genome_kristen/`
  - Junction census exists per-chromosome; no full assembly yet
- **Phasing data:** `/home/rempel/genomics/_analysis/x8a_phasing/`
  - `oliver.phased.vcf.gz` / `kristen.phased.vcf.gz`
  - `per_block_maternal_side_min1.tsv` (maternal-side assignment per phase block)
- **Population resources:**
  - T2T-CHM13: `/home/rempel/genomics/_analysis/x8a_engscreen/chm13/` (fasta + blast db)
  - gnomAD-SV v4.1: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (63k genomes)
  - DGV: `/home/rempel/genomics/_analysis/x8a_engscreen/dgv_grch38/`
- **Repeat consensi + blast DB:** `/home/rempel/genomics/omega_run/out/repeat_consensi/` (25 sequences from Dfam; AluY/Ya5/Yb8/Sc/Sg/Sx/Jb, L1HS/L1PA*, SVA, satellites)
- **Categorizer scripts:** `/tmp/categorize.py` (in the ubuntu distrobox container)
- **Small-insertion scan:** running in `distrobox enter ubuntu` as background job
- **pysam location:** inside the `ubuntu` distrobox container (`distrobox enter ubuntu -- python3`)
- **Disk:** 90% full, ~130 GB free - guest-box floor reached

### In the repo (C:\claude_base\)
- **Report:** `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` (7 commits, all findings appended)
- **Controls spec:** `projects/XG1/kenefick/omega_detector/CONTROLS_SPEC_for_worker_v01_tomemex.md` (for PX1/X21C)
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` (all milestones logged)

### Session identity
- This session: **X21G** (was QP3, was X21D, was ?)
- Branch: `claude1/friendly-cartwright-40d9c2`
- Worktree: `C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0` (fresh - old one recycled)
- Board: moved to `qp` team board (independent from the main 14-session community per Max's instruction), but Max also said "no more boarding" - this session is fully independent now

---

## GOTCHAS AND DEAD ENDS

1. **chr-prefix bug in gnomAD-SV:** My loci use bare chromosome names (`12`) but gnomAD-SV uses `chr12`. Every pysam `fetch()` threw "invalid contig" silently ? all 47 read "absent." Fixed by prepending `chr`. This wasted significant time.

2. **K-mer mother-check is unreliable:** Produced 2 false de-novo candidates. The soft-clip direct read check is the standard now. When verifying mother presence, always look at soft-clips, not k-mers.

3. **"Son homozygous" ? alien - it means INHERITED from BOTH parents.** I ranked chr12:30348820 as #1 initially because it was homozygous (looked strong), but homozygous means both chromosome copies carry it = inherited from both parents = common, not de-novo. Max caught this. The alien shape is: son heterozygous (one copy) + mother absent.

4. **Mother coverage is ~30? vs son ~80?:** This alone explains the son's ~2? higher raw insertion count. Always normalize for coverage before comparing child vs mother.

5. **Short soft-clip fragments inflate "non-repeat" count:** A 60 bp clip can't match a full Alu consensus. For fair child-mother comparison, use the SAME extraction method (both assembled payloads OR both soft-clip fragments, not mixed).

6. **MHC/HLA (chr6:32.5M) and pericentromeric regions (chr17:21.8M) are phasing/read-mapping minefields:** Both maternal-de-novo candidates were false positives from these regions. Expect artifacts here and verify extra carefully.

7. **Online NCBI BLAST never returned from asto:** Outbound to NCBI likely throttled. All blast is done locally now (against CHM13 + repeat consensi).

8. **Temp files got corrupted across SSH runs:** The initial batch classifier ran on a stale/corrupted temp file (448 items with blank divergence instead of 48). Always regenerate candidate lists cleanly; don't trust temp files that survived multiple SSH sessions.

9. **Contig naming in BAMs:** Oliver's BAM uses bare `22`, not `chr22`. Always check the BAM header before queries.

10. **Windows CRLF in scripts:** Scripts written on Windows and piped to asto via SSH had `\r` characters. Use `tr -d '\r'` or pass raw bytes. The stable method: write script via Write tool ? pipe through Python subprocess with clean newlines ? ssh to asto.

11. **Distrobox container needed for pysam:** Host Python lacks pysam. Always `distrobox enter ubuntu -- python3` or `distrobox enter ubuntu -- bash -lc "..."` for read-level work.
