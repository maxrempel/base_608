# Scribe handover - milestone 9 (~678K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 16:11:41 by deepseek-v4-pro

HANDOVER - P3 OMEGA ("foreign-DNA insertion detector") - Scribe report

**GOAL (in Max's own words, from the conversation):**
Detect foreign (non-human) DNA spliced cleanly into Kristen's genome - the literal "alien DNA insert" test. After cataloguing everything, look for insertions that are rare (a few % of people), artificial-looking (no natural transposition scar), transposon-like but not known transposons, and ideally absent in the mother (non-parental). The method must be documented as a growing reference catalogue; the project is long-term, cross-referencing multiple self-reported abductees. Budget: $4 for optimisation, $20-25 for the whole project. Machine: use asto (borrowed shared server, keep all four resources under 50%, ideally under 70%).

**DECISIONS MADE AND WHY**

1. **"Option B" - junction half-chimera contigs (two half-bridges), not a single spanning omega contig.**
   - Why: the per-cluster assemblies rarely produced a full `human|FOREIGN|human` contig (the original "omega" shape). Instead, we recover **one-sided extensions**: a contig that is solidly human-anchored on one end with a non-human overhang on the other. Two facing half-chimeras at the same locus corroborate the insertion. This approach is length-independent (works for 1 kb or 50 kb inserts) because we never need to cross the middle. Max chose this explicitly ("Option B is terrific").

2. **Classification gates are not binary on/off filters.**
   - Why: Max insisted we must not blindly exclude things. The rule: **recover generously, keep everything, annotate every candidate along multiple axes** (human-mapping status, kraken2 taxon, repeat family, mappability, support, overhang length), then **cluster candidates and calibrate the thresholds from the real distribution**. Only then do we draw the cutoffs. This avoids the trap of a silent exclusion hiding a real signal.

3. **Pilot on Oliver's good bwa-aligned BAM, not on Kristen's vendor DRAGEN BAM.**
   - Why: The DRAGEN-aligned BAM has ~8? fewer soft-clipped reads than a proper bwa alignment (team measurement). The detector relies on soft-clips; running on the starved vendor BAM gives only a lower bound, not a trustworthy negative. Oliver's freshly bwa-aligned BAM is soft-clip-rich, so it provides both a real test and ample signal for calibration. Kristen's genome will be re-aligned with bwa later for the definitive mother-son comparison.

4. **Compute stays on asto; no EC2 cloud transfer.**
   - Why: The BAM lives on asto. The real upload from asto to the cloud is only ~2.7 MB/s (despite a fast local path), so moving 35 GB would take ~3.6 hours and hog the slow internet. EC2 was spun up and immediately aborted after measuring this. Public-data scans work on EC2 (e.g., X12B's 1000 Genomes job) because data is already in-region. Sol is banned - the hardware corrupts BAMs on write (two random CRC/BGZF corruptions confirmed, consistent with bad DIMM/disk).

5. **Kristen bwa realign queued low+slow.**
   - Max wanted to kick it off at minimal resources: ~2 cores, niced, ~25% of the box, run for a couple of days. This is to eventually provide a well-aligned BAM for P3's mother-son comparison. P1 previously retired the realign, but Max overruled for P3. The task was routed to X5 (who owns the resumable alignment pipeline) and x1 (who stages Kristen's fastq).

6. **Methodological rules now encoded in global2.md:**
   - a) **Pilot-prove before scale**: you must exhaustively QC a small chromosome/region before running genome-wide. The chr22 QC caught massive over-calling (half the "foreign" payloads were human repeats), proving that raw junction counts are not the answer.
   - b) **Use the LLM to look at real data close-up**: do not rely solely on aggregate pass/fail counts; actually examine the reads, alignments, and specific loci to spot artifacts.

**CURRENT STATE**

- **Positive control** built and **passing**: a synthetic genome with a known 1 kb (and 5 kb) foreign insert. The Option B detector finds the insert at the correct locus, two-sided, with recovered overhangs. Noise behaviour correct (stray one-sided candidates not promoted).
- **Chr22 QC on Kristen vendor BAM** complete. Outcome: raw detector gave 2 two-sided + 46 half-sided candidates, but after re-mapping the payloads to human and running kraken2, **both two-sided candidates turned out human** and half the payloads mapped back to human. The honest chr22 answer is **zero genuine foreign insertions** - the correct clean baseline, reached correctly rather than from a broken detector.
- **Genome-wide run on Kristen vendor BAM paused** (and will not be resumed; the data is too soft-clip-starved for a definitive answer).
- **chr19 run on Oliver's bwa BAM** launched on astolfodebian (tmux session `oliver19`, tracking file `/home/rempel/genomics/omega_run/out/oliver_chr19/`). It is running the full pipeline: extraction of clipped reads, clustering, per-cluster assembly with fishing (wider window), then `omega_junction.py` (Option B) to produce junction candidates with overhang sequences. This run is in progress and should be done or near done.
- **Kristen bwa realign** routed to X5+x1; status unknown (likely not yet started).

**EXACT NEXT STEP** (what a fresh session should do immediately)

1. Check that the chr19 Oliver run is complete. The tmux session may still be alive; check `tmux ls` on asto for `oliver19`. If finished, the output will be in `/home/rempel/genomics/omega_run/out/oliver_chr19/junction.tsv` (or similar). The directory structure follows the convention of `omega_run_region.sh`.

2. Once the junction candidates are available, **annotate all payloads**:
   - Extract the overhang sequences (the script `omega_junction.py` can be modified to emit a FASTA of overhangs - currently the script might not do that; check `qc_chr22.sh` as a template).
   - Map them back to GRCh38 with `minimap2 -a -x sr` (sensitive short-read mode) to identify human repeats.
   - Classify with kraken2 (database on asto) to get taxonomic origin.
   - Include the mapping/mappability and kraken results as extra columns in a full inventory TSV.

3. **Manually inspect the most promising candidates** (the ones that neither map to human nor are classified as human by kraken2). Look at the actual sequences, the alignments, and the genomic context (segdup overlap, centromere/telomere, low mappability). This is the "LLM looks at real data close-up" step.

4. Once the annotated inventory is clean, **cluster candidates by their payload features** (taxon, human-mapping identity, overhang length, etc.) and **calibrate the cutoffs** for what counts as a genuine foreign insertion. The calibration should be based on the distribution of all candidates (including the known-human ones, which form the baseline). Nothing is excluded until this step is done.

5. Only after the pilot passes this exhaustive QC on chr19, scale to **genome-wide on Oliver** (if time/CPU allow) or at least a few more chromosomes to build a proper catalogue. The Kristen bwa realign will be needed later for mother-son comparison; check with X5 on its status.

**OPEN QUESTIONS AWAITING MAX** (none critical, but eventual)

- After the annotated chr19 pilot, Max should review a few example candidates and the proposed calibration thresholds before scaling genome-wide. He will likely want to see the classification axes and the cluster plots.
- The Kristen realign task routing to X5/x1: if they haven't started, Max may need to re-emphasise or confirm the resource budget.

**KEY FILE PATHS, NAMES, COMMANDS**

- **Remote machine**: astolfodebian.tail251d88.ts.net (user rempel, SSH key `~/.ssh/bitwarden_ed25519`). Use `distrobox enter ubuntu` for tools.
- **Working directory**: `/home/rempel/genomics/omega_run/`
- **Scripts** (all on asto in `scripts/`):
  - `omega_extract.py` - extract soft-clipped reads from BAM for a region.
  - `omega_percluster.sh` - resumable per-cluster assembly with fishing (wider window) and junction detection. Uses `omega_junction.py` as the final step.
  - `omega_junction.py` - Option B junction detector: finds half-chimera contigs, pairs them, reports insertion candidates with overhang lengths.
  - `omega_run_region.sh` - wrapper to run extraction ? clustering ? percluster for a given region.
  - `omega_genome.sh` - genome-wide scatter-gather driver (paused; still uses old filtering, needs update with annotation gates).
  - `qc_chr22.sh` - template for payload extraction, re-mapping and kraken2 classification.
  - `make_pc.sh` - build positive control (synthetic genome, simulate reads, align, run detector).
- **Input BAMs**:
  - Oliver's bwa BAM: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (indexed)
  - Kristen's vendor BAM: `/home/rempel/genomics/kenefick/kristen/kristen.mq.bam` (soft-clip poor)
- **Reference and masks**:
  - GRCh38: `/home/rempel/genomics/omega_run/ref/GRCh38.fa`
  - Segdup BED: `/home/rempel/genomics/omega_run/ref/segdups_nochr.bed` (or `/home/rempel/genomics/kenefick/analysis/segdups_nochr.bed`)
- **Outputs** (to review):
  - chr19 Oliver run: `/home/rempel/genomics/omega_run/out/oliver_chr19/` (look for `junction.tsv` or `junctions.txt`)
  - Positive control: `/home/rempel/genomics/omega_run/poscontrol/`
- **Memex design doc**: `C:\claude_base\projects\XG1\kenefick\omega_detector\OMEGA_PIPELINE_DESIGN_v01_tomemex.md` (contains ALL decisions, breakthroughs, calibration rules).
- **Git repo**: `C:\claude_base` - all scripts and design docs committed under `projects/XG1/kenefick/omega_detector`.
- **Team board**: Python at `C:/claude_base/branch_bulletin/bcast.py`; use `post` to communicate, `catchup` to read. My thread is in room `omega_contig`.

**GOTCHAS AND DEAD ENDS ALREADY RULED OUT**

- **Sol is unusable**: hardware corruption (bad DIMM/disk) silently corrupts BAM files on write. Never copy data to Sol for anything critical.
- **EC2 for this single genome is a dead end**: asto's uplink is only ~2.7 MB/s, making data transfer too slow and expensive. EC2 only works when the source data is already in the cloud (e.g., public S3).
- **DO NOT use PowerShell to strip carriage returns**: `tr -d "\r"` in PowerShell becomes `tr -d "r"` (deletes all 'r' letters). Use bash inside a heredoc or pass commands directly, or use `tr -d '\015'`.
- **BAM corruption from `rsync --partial`**: the vendor BAM on Sol got a bad block that `samtools quickcheck` missed; always do md5 verification and a full decode scan if copying BAMs.
- **The earlier genome-wide "0 hits" on Kristen was a combination of a broken detector (Option A) and soft-clip starvation**, not a clean genome. Do not interpret any negative result on the vendor BAM as definitive.
- **The mkdir-before-redirect bug**: in `omega_genome.sh`, the per-chromosome log redirect happened before the output directory was created, causing every chromosome to fail instantly. That was fixed.
- **Resumable `.done` markers** are implemented per cluster and per chromosome. When restarting a run, existing work is skipped
