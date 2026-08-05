# Scribe handover - milestone 9 (~715K tokens)
# session: 20260707_confident_nobel_40d20b_aff9072d
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-07 14:30:20 by deepseek-v4-pro

# HANDOVER - P3 OMEGA: Alien Insertion Hunt in Oliver (Session QP3)

---

## GOAL (Max's own words)

Find **alien/engineered DNA insertions** in the genome of **Oliver** (son of experiencer Kristen Kenefick). The aliens are distant human relatives, so the insert is NOT non-human - it is **a human sequence copied from somewhere ELSE in the genome into a NEW site, with IMPERFECT homology (its own characteristic mutations)** - a "distant-relative" insertion. Human jumps, relocated, diverged.

Max explicitly rejects "clean negative" as a possible answer - it means the analysis was biased. He demands **quantitative distributions**, not conclusions. The task is to measure: how many insertions the method finds, and the **divergence distribution** of jumped human pieces from their original source.

Secondary: compare Oliver's count to unrelated controls to determine if he is unusual.

---

## DECISIONS + WHY

1. **Reopened the paralog/relocated angle (Max's reframe).** The earlier pipeline was discarding pieces that map to multiple human loci as "paralog artifacts." Max corrected this: a sequence that maps cleanly elsewhere but carries its own characteristic mutations at the new site IS the target. The discriminator became: consistent diagnostic mutations across uniquely-mapping reads = real relocated copy; mixed/inconsistent alleles = mismap artifact.

2. **Dropped the 150 bp floor** (to ~50 bp) when running the relocated analysis, per Max's question "why can't we look at 30-50 bp inserts?"

3. **Used direct sequence comparison** (blastn) instead of k-mer presence for the relocated-vs-source analysis - simpler, more interpretable.

4. **Disconnected from the team board** - Max moved QP3 to a separate board ('qp') to avoid "mainstream bias" from conservative peers.

5. **Close-look discipline:** every survivor gets read-level inspection (actual clipped reads, actual inserted sequence) before being trusted.

6. **Questioned de-novo insistence:** Max said relocated diverged human pieces are interesting *even if inherited*, not only if new-in-son. Inheritance is a ranker, not a filter.

---

## CURRENT STATE - What is done and what is in flight

### DONE (committed and pushed)

**The relocated-diverged re-analysis on Oliver, full pipeline:**

- **1,107** reconstructed insert payloads from Oliver's genome-wide OMEGA run.
- **Divergence distribution** computed across all 1,107 (best-hit percent identity to GRCh38):
  - 209 exact (0%), 2 at 0-0.5%, 21 at 0.5-2%, 29 at 2-5%, 35 at 5-10%, 84 at 10-20%, 26 at 20-40%, **701 no covered human match**.
  - Among the 406 that DO align: p75 = 11.0%, p90 = 17.1%, max = 32.9%.

- **48 few-locus relocations** (pieces mapping to 1-3 human loci - the "jumped" class). Divergence bins:
  - 0-2%: 21, 2-5%: 2, **5-10%: 7, 10-20%: 14, >20%: 4**.

- **23 unique-sequence + diverged >5% pieces** (complexity-filtered: not satellite junk).

- **Direct mother-presence test** on all 48 relocated pieces - for each, checked whether the mother's reads at that locus show the same soft-clip insertion signature. Result: ~32 inherited (mother has the same insert), ~6 unplaceable, ~4 low-coverage. One de-novo candidate (`chr10:38788170`) survived the screen.

- **Close read-level look at top candidates:**
  - `chr10:38788170` (the de-novo candidate) - son really has a coherent insertion (31 clipped reads, two-sided junction), but the inserted sequence is a **human CATTC/TTCCA pericentromeric satellite repeat**. Mother's 2 stray reads match it exactly - she has it too, buried in ragged satellite coverage. NOT de-novo.
  - Top cross-chromosome jumps (`chr10:81212447` chr13?10, `chr11:38980211` chr17?11, `chr12:30348820` local 100 kb): all are real unique inserted sequences (not satellites), but **all inherited** (mother homozygous or heterozygous for the same insert). One (`chr11`) is a known Alu jumping element. One (`chr10:38823515` chr16?10) was an assembly artifact - no real junction at the read level. The `chr12:30348820` 23.7%-diverged piece is the cleanest case: real, unique, homozygous in son, heterozygous in mother.

- **Clean single-pass classifier** on all 47 relocations: **31 mobile/repeat** (Alu, L1, satellite - ordinary jumping DNA) + **15 unique-locus copies** (but nearly all short, 52-130 bp, and near-identical <2% diverged to their source = ordinary segmental duplications). **No unique-AND-diverged-AND-read-confirmed relocation survives.**

- **Divergence?complexity scatter data** available for graphing.

- **Controls spec written** (`CONTROLS_SPEC_for_worker_v01_tomemex.md`) - self-contained instructions for a worker to run the identical pipeline on 3-5 unrelated 1000-Genomes genomes and compare counts against Oliver's yardstick.

### PARKED / DEFERRED

- **Mother finer class-breakdown** - the mother has 144 diverged payloads vs Oliver's 115, so Oliver is not enriched. The finer breakdown was never finished (asto saturated by sibling scans; script ready at `/home/rempel/genomics/omega_run/out/genome_kristen/kristen_control.sh`). This is confirmation-only (count-level answer is already in hand).

- **Unrelated-people controls** - spec written, needs a worker (PX1 or X21C) to execute.

### NOT YET STARTED

- **Small-insertion extension (30-150 bp)** - the 150 bp floor excluded ~837 pieces; QP3 was about to drop the floor and re-scan these when the session ended. This is the one class still not counted.

---

## EXACT NEXT STEP

**1. Drop the size floor and count small jumps (30-150 bp).** Take the already-extracted payloads below 150 bp (837 pieces were dropped at this cut), rerun the relocated classifier on them (direct blastn, same single-pass method), and fold them into the divergence distribution. This closes the last un-counted class.

**2. (In parallel, via a worker): Run the controls.** Paste the controls spec below to PX1 or X21C so they run the OMEGA pipeline on unrelated genomes and produce a comparison table. The spec is at `C:\claude_base\projects\XG1\kenefick\omega_detector\CONTROLS_SPEC_for_worker_v01_tomemex.md`.

**3. Graph the distributions.** All the raw data for a divergence histogram + divergence?complexity scatter is computed - build the visual.

---

## OPEN QUESTIONS STILL AWAITING MAX

- **Controls:** When do you want the unrelated-people comparison run? The worker spec is ready - just say go, or paste it to PX1/X21C yourself.

- **30-50 bp small inserts:** Should I drop the floor all the way to 30 bp, or start at 50 bp? Shorter = more noise from micro-indels and alignment errors.

- **Gene characterization:** The unique relocated pieces (even the inherited ones) land in specific genes - want that annotated, or skip since none survived the unique+diverged filter?

- **Long-read ceiling:** Short-read phasing cannot resolve pieces in het-deserts. If you ever want a definitive answer, long-read sequencing (PacBio/ONT) would close the unphaseable gap. But you said the budget is $50/day - so this is noted, not proposed.

---

## KEY PATHS / IDs / COMMANDS

### Local files (all under `C:\claude_base\projects\XG1\kenefick\omega_detector\`):
- `OMEGA_PIPELINE_DESIGN_v01_tomemex.md` - canonical design doc (BREAKTHROUGHS section, corrected target, calibration/QC findings)
- `OMEGA_RESEARCH_PLAN_v01_tomemex.md` - manager plan doc (hypothesis, pipeline, directions A-G)
- `CONTROLS_SPEC_for_worker_v01_tomemex.md` - paste-ready worker spec for unrelated-people controls
- `results/RELOCATED_DIVERGED_FINDINGS_v01_tomemex.md` - the quantitative findings writeup
- `results/relocated_single_few_classified_v01.tsv` - the 48-relocation table
- `results/diverged115_ranked.tsv` - earlier diverge-ranked set
- Scripts: `omega_junction.py`, `omega_percluster.sh`, `characterize.py/.sh`, `phase_insert_pilot.py`, `phase_join.py`, `phase_matelink.py`, `maternal_screen_743.py`, `decisive_denovo.sh`, `annotate.py`, `out_of_place.py`, `recon_classify.py`, `iterative_fish_all.sh`

### Remote (asto, `/home/rempel/genomics/omega_run/`):
- `out/genome_oliver/` - Oliver's full OMEGA run output (743 two-sided inserts, 1,107 reconstructed payloads)
- `out/genome_oliver/reconstruct_all743/` - **the main working directory:**
  - `all_payloads.fa` - the 1,107 payload sequences
  - `char_blast.tsv` - full blastn output (1.4 GB, pident in column 5)
  - `relocated_single_few_classified_v01.tsv` - the 48-relocation classification
  - `diverged115_ranked.tsv` - earlier diverge-ranked set
  - `cand27_ntblast.tsv` - nt-BLAST results for candidate set
  - `complexity_check.py` - computes 4-mer complexity per payload
- `out/genome_kristen/` - Mother's OMEGA run output (144 diverged payloads)
- `out/genome_kristen/kristen_control.sh` - parked mother-classifier script (ready, not yet run)
- BAMs: `oliver.mq.bam` (bwa, 65.7 GB), `kristen.bwa.mq.bam` (fresh bwa realign, 37.6 GB, indexed)
- Reference: `ref/GRCh38.fa`, `ref/chm13v2.0.fa` (T2T), `ref/gencode.v46.basic.gtf`
- X8A phasing outputs (reuse, don't rebuild): `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`, `kristen.phased.vcf.gz`, `per_block_maternal_side_min1.tsv`

### Identities:
- Session: **QP3** (formerly X21D), on the **'qp' team board** - disconnected from main board by Max
- Anonymization: Kristen?Antoinette, Oliver?Theodore, Kenefick?Whitfield
- asto is Liz's borrowed box - guest resource caps (CPU/RAM/disk-I/O/network each under ~50% ideal, 70% max)
- Oliver's genome: `oliver.mq.bam` (bwa-aligned, good data)
- Kristen's genome: `kristen.bwa.mq.bam` (fresh bwa realign by X5, now available)

### SSH (from Pine/laptop):
```bash
ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net
# Genomics tools live inside distrobox: distrobox enter --no-tty ubuntu -- bash -lc "..."
```

---

## GOTCHAS / DEAD ENDS ALREADY RULED OUT

1. **Never use Sol for genomics** - it corrupts data on write (bad RAM/disk, two copies gave two random CRC32 errors). Team rule.
2. **Never strip carriage returns with PowerShell** - `tr -d "\r"` in PowerShell deletes every letter 'r'. Use bash `tr -d '\r'` only.
3. **Never use setsid + distrobox** - distrobox needs a tty; setsid kills it silently. Use plain nohup or tmux for detached jobs.
4. **pgrep self-matching trap** - `pgrep -f my_script` matches the SSH command line that contains "my_script." Use bracket tricks (`pgrep -f "[m]y_script"`) or grep for the actual PID.
5. **DRAGEN vs bwa soft-clip difference** - Kristen's vendor BAM (DRAGEN) has ~8? fewer soft-clips than a bwa alignment. Oliver has proper bwa. This only matters for clip-based detection; k-mer presence (sequence in reads) is aligner-agnostic.
6. **EC2 transfer speed:** asto's real upload to us-west-2 cloud is **~2.7 MB/s** (NOT the 65 MB/s local/Tailscale path). For private data anchored to asto, compute stays where the data is. EC2 only wins for cloud-to-cloud (public data).
7. **The chr8 standout was a known human insertion** - a great validation of the detector, not an alien find. nt-BLAST resolved it to a catalogued "Homo sapiens non-reference insertion sequence" (GenBank MH534678).
8. **The earlier "0 hits" was a broken Option A detector**, not real data. Option B (junction half-chimeras) fixed it.
9. **chrY + unplaced/alt contigs are artifact-prone** - ~25% of insertions land there. Geterochromatin/satellite regions where aligners misplace reads.
10. **"Clean negative" does not exist in this data** (Max's rule) - any claim of zero should be re-examined as a possible filtering or method bias. Present distributions, not conclusions.
11. **The mother-presence test must use the SAME detector** the son was found with - soft-clip junction detection at the known coordinate. k-mer presence is an alternative but the direct read-clip check is more interpretable.

---

## CONTROLS SPEC (paste to PX1 or X21C)

```
Run the OMEGA relocation pipeline on 3-5 UNRELATED genomes as controls for Oliver.

FIRST: check if the P2 team's 1000-Genomes BAMs are already on asto
(reuse = no download; only download throttled if none exist).

Then run the IDENTICAL detect -> reconstruct -> blast -> classify pipeline
(scripts in /home/rempel/genomics/omega_run/). Report one table per genome:
two-sided loci, reconstructed payloads, few-locus relocations,
mobile-vs-unique split, diverged-count.

Compare against OLIVER'S YARDSTICK:
  161,354 candidate loci -> 1,107 payloads -> 47 relocations
  (31 mobile + 15 unique) -> ~23 diverged >5%

QUESTION TO ANSWER: is Oliver's number unusual or typical of any human?

pysam is in the asto 'ubuntu' distrobox container.
Report numbers + distributions, no conclusions.
Full spec file:
  C:\claude_base\projects\XG1\kenefick\omega_detector\CONTROLS_SPEC_for_worker_v01_tomemex.md
```
