# Scribe handover - milestone 3 (~228K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 10:06:42 by deepseek-v4-pro

# HANDOVER: Omega Contig Foreign DNA Insertion Detector

## GOAL (in Max's own words)

Find foreign (non-human) DNA *spliced into* the human genome - actual integrated insertions, not free-floating microbes. The working hypothesis is that ~2-5% of the human population carries alien-lineage DNA, so each insertion is **rare** (present in only a small % of people), absent from the consensus reference genome, and potentially showing up as obscure rare entries in databases. The detector should catalog **everything** out-of-place - human rearrangements, animal, bacterial, viral, transposons with artificial insertion signatures, near-human-but-diverged (distant relatives, since ~40% of the galaxy is populated with our relatives), and truly unknown/alien. Nothing blind-filtered; full inventory first, then calibrate thresholds on real numbers.

---

## DECISIONS MADE + WHY

### 1. Method: "Omega Contig" (Path B - targeted local assembly)
**What:** Reassemble DNA around junction sites so a single reconstructed piece reads `human-anchor | foreign payload | human-anchor`, with the two ?100 bp human ends landing **adjacent head-to-tail** in the human genome (single clean cut, no human letters lost, no overlap).  
**Why:** The aligner can't call the foreign part by itself - reads spanning the junction get soft-clipped (half maps to human, half dangles off into the unknown). By assembling locally, the payload becomes visible as a contiguous stretch. Beats the earlier "leftover-reads" approach (which could only find free-floating microbes, never integrated DNA).  
**Naming:** "Omega" = Greek ? - two feet (anchors) planted adjacent in the genome, a loop (foreign payload) rising between them.

### 2. Signature: Clean-cut germline insertions
- **Adjacent anchors** (within ?20 bp of exact, gap recorded per hit; strict zero-gap clean splices stand out).
- **Anchor length:** ?100 bp each end, high homology/identity.
- **Germline target:** ~99% of cells carry it (no VAF problem at 30x; assembles cleanly at full depth).
- Messy insertions (deletions, scrambling at the breakpoint) are deliberately ignored - go for the unambiguous ones first.

### 3. Targeted assembly over full-genome de novo
**Decision:** Pull only junction-crossing reads + their mates + fully-foreign reads, assemble locally around each breakpoint. **Not** full-genome de novo.  
**Why:** Same omega result for a tiny fraction of compute. Full de novo needs a huge-RAM AWS box and would reassemble 3 billion human bases just to find a few junctions. The targeted approach runs on a modest machine. Full de novo kept as an exhaustive backstop but not built first.

### 4. Five-Gate Filter Cascade - BUT as labelers, not deleters
**Core principle (Max):** **Inventory first, calibrate second. No blind exclusion.**  
Every omega candidate is **kept** and annotated through all five gates. Nothing is silently dropped. The first deliverable is a **full census** with per-category counts. Thresholds are calibrated only *after* seeing the real distribution. Excluded bins stay in the table with counts + reasons, always recoverable.

The five gates are now annotation layers:
1. **Human MEI filter** - tag as Alu/L1/SVA/HERV (each counted separately). Transposons with *artificial* insertion signatures (no TSD, no poly-A tail, CRISPR/blunt ends) get flagged as high-interest even if the element is known.
2. **Payload organism ID** - kraken2 (microbe/virus) and UniVec (lab vector/plasmid). Outcomes: known microbe, known virus, known vector, or **nothing** (true-unknown bin).
3. **Reference-gap check** - does the payload map to T2T/pangenome? If yes, it's a gap in GRCh38, not foreign. (x1 builds this gate.)
4. **Junction-spanning read proof** - require ?2 reads per side crossing the splice (physical evidence, not an assembly artifact).
5. **Population frequency** - how many control people carry the same payload at the same locus? **Rare tail** (~few % of population) is the sweet spot; common = likely polymorphism; utterly unique = possible but hardest to vet. "In a database" does NOT disqualify - what matters is *how common* it is there.

### 5. Expanded Target Taxonomy (two new dimensions per candidate)
Beyond "what organism," every candidate now carries:

**Dimension A - Origin + relatedness to human:**
- Human-out-of-place (rearrangement/insert of human DNA where it doesn't belong)
- Primate / mammal / other animal, out of place
- Bacterial / viral, out of place
- **Near-human-but-diverged** (~90-98% match to human - the "distant relative" / related-alien bin, highest interest)
- True unknown (matches nothing)
- Each gets a **percent-identity to human/primate** as a number, not a binary yes/no.

**Dimension B - Insertion signature:**
- **Natural** transposon (has target-site duplication, intact element ends, poly-A tail for L1/Alu)
- **Artificial** (lacks natural hallmarks - blunt ends, no TSD, CRISPR scar = candidate engineered insertion)

### 6. Population Frequency as the Main Calibration Axis
**Max's prior:** The real alien insertions are **rare, not unique** - ~2-5% foreign DNA, each insertion in only a small % of people, absent from consensus, at most an obscure rare entry in databases.  
**Consequence:** Gate 5 records **frequency** (what fraction of a cohort carries it), not a yes/no. "Found in a database" doesn't disqualify - "found in 80% of people" does. The sweet spot is the rare tail: not-in-consensus, present in a few percent of the population.

---

## CURRENT STATE

### Built and Validated
- **Design doc:** `OMEGA_PIPELINE_DESIGN_v01_tomemex.md` - frozen spec with omega/anchors naming, all five gates, inventory-first principle, expanded taxonomy, frequency dimension.
- **Brainstorm doc:** `FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md` - contains the conceptual history and the frozen refined spec.
- **Core pipeline (v01) - all four stages validated end-to-end on a 2 Mb Kristen test slice:**
  - **Stage 1: `omega_extract.py`** - Python CIGAR parser (mawk-safe) extracting junction-crossing reads + mates + fully-unmapped reads from Kristen's BAM. Verified on real data.
  - **Stage 2: `omega_detector_v01.sh`** - clustering extracted reads by anchor locus. Produced ~35 omega-shaped clusters from just 2 Mb (proving the shape fires thousands of times genome-wide, so the gates are everything).
  - **Stage 3: `megahit` assembly** - pooled assembly of clustered reads.
  - **Stage 4: `omega_filter.py`** - omega-shape check (anchor adjacency, homology, orientation). Correctly returned **zero** hits on the random test slice (no false positives).
- **v02 per-cluster assembly (`omega_percluster.sh`)** - assembles reads around each breakpoint separately for cleaner contigs. Built and committed; *not yet tested* because per-cluster megahit spawns proved too slow on a loaded machine.
- **Gate runner (`omega_gates.sh`)** - scaffolds the five-gate annotation cascade. Two gates fully operational (kraken2 organism-ID, UniVec vector check - both DBs installed on asto). MEI library, T2T/pangenome refs, and RepeatMasker are absent (x1 handles T2T).
- **All committed and pushed** to the `relaxed-dijkstra-f7ccbd` branch on origin.

### Dependency Inventory on asto
- **Ready:** samtools, megahit, minimap2, kraken2 + standard DB, UniVec + BLAST DB, blastn
- **Missing:** RepeatMasker / MEI library (Gate 1), T2T/pangenome reference (Gate 3 - x1 is fetching on Sol/Lak), control BAMs for frequency measurement

### Team Coordination
- **x1** - working body; building the T2T/pangenome reference-gap gate (Gate 3) on Sol/Lak; owns per-cluster refinement of the assembly
- **X7A** - original idea author; formally handed ownership to X21B
- **X10A** - Track-1 manager; confirmed no duplication (INSurVeyor on Kristen = clean negative, 0 passing insertions; structurally can't see integrated foreign DNA, so omega detector fills a real gap)
- **X11B** - building cross-person recurrence aggregator + segdup masks; his frequency counter is now central (it literally measures the population-frequency axis)
- **X5** - confirmed Oliver's alignment timeline (9/12 chunks done, frees asto ~13:30 asto-time)

### Blocker
**asto (the compute box) is saturated** by Oliver's BWA-MEM alignment (chunk 11 of 12 as of last check). The genome-wide omega run on Kristen is ready to fire but held pending CPU. Estimated unblock: ~13:30 asto-time, roughly now-ish at session end.

### Validation Bugs Found and Fixed
1. Kristen's BAM uses **numeric chromosome names** (`20`, not `chr20`) - the test slice initially returned 0 reads until corrected.
2. The distrobox only has **mawk**, not **gawk** - the original extraction awk depended on gawk's 3-arg `match()`. Fixed by rewriting Stage 1 as Python.
3. **minimap2 not installed** in the distrobox - installed it.
4. **CRLF line endings** from git on Windows broke the shell script on Linux - stripped.
5. **Per-cluster megahit spawn** (v02) proved too slow at genome scale - scaling issue found and recorded. Needs either parallel execution or a different assembler on a free box.

---

## EXACT NEXT STEP

**Launch the genome-wide omega run on Kristen the moment asto frees up (Oliver's alignment finishes).**

Concrete sequence:
1. SSH to asto, confirm bwa processes are gone and load is low.
2. Run Stage 1 (extraction) genome-wide: `omega_extract.py` pointing at Kristen's full `kristen.mq.bam`.
3. Run Stage 2 (clustering) on the full extraction output.
4. Run Stage 3 (assembly) - start with v01 pooled, then iterate to v02 per-cluster once CPU is abundant.
5. Run Stage 4 (omega filter) on the assembled contigs.
6. Produce the **first full census** - total omega candidates, per-gate annotation counts, frequency distribution.
7. Present the census to Max for calibration of thresholds.

Secondary: Test v02 per-cluster assembly on a clean box or parallelized once the genome-wide v01 run is underway. x1 should deliver the T2T/pangenome gate before the census reaches Gate 3.

---

## OPEN QUESTIONS (awaiting Max)

1. **Adjacency tolerance:** Allowing ?20 bp around exact adjacent, with exact gap recorded per hit (so true zero-gap splices stand out). Max was told this is the default; no objection raised yet. Object if you want strict zero only.

2. **Junction-spanning read minimum:** X21B proposed ?2 reads per side to prove the seam is physical (not an assembly artifact). Max hasn't addressed this yet. Default is ?2.

3. **"Near-human-diverged" % cutoff:** What percent-identity range defines the "related-alien" sweet spot? Context: too low (e.g. 80%) = artifact-prone or genuinely distant; too high (e.g. 99%) = likely ordinary human. Max hasn't set a number - this will need calibration from the actual distribution.

---

## KEY PATHS AND IDS

### Local (development)
- **Design doc:** `C:\claude_base\projects\XG1\kenefick\omega_detector\OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
- **Brainstorm doc:** `C:\claude_base\projects\XG1\kenefick\FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md`
- **Core scripts:**
  - `C:\claude_base\projects\XG1\kenefick\omega_detector\omega_extract.py` - Stage 1 extraction (Python, mawk-safe)
  - `C:\claude_base\projects\XG1\kenefick\omega_detector\omega_detector_v01.sh` - Stages 1-4 pipeline shell
  - `C:\claude_base\projects\XG1\kenefick\omega_detector\omega_filter.py` - Stage 4 omega-shape filter
  - `C:\claude_base\projects\XG1\kenefick\omega_detector\omega_percluster.sh` - v02 per-cluster assembly
  - `C:\claude_base\projects\XG1\kenefick\omega_detector\omega_gates.sh` - 5-gate annotation runner
- **Git branch:** `relaxed-dijkstra-f7ccbd` (on origin)
- **Worklog:** `C:\claude_base\compaction_kb\scripts\worklog.py`

### Remote (asto - the compute box)
- **SSH:** `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
- **Distrobox:** `distrobox enter ubuntu` (all tools inside this container)
- **Kristen BAM:** `/home/rempel/genomes/kristen/kristen.mq.bam` (~35 GB)
- **Reference:** `/home/rempel/genomes/GRCh38.fa` (numeric contigs: 1,2,3,...,X,Y - no "chr" prefix)
- **Extraction work dir:** `/home/rempel/genomes/kristen/omega_extract/`
- **Stage 1+2 output:** `/home/rempel/genomes/kristen/omega_extract/kristen_softclipped.txt`, `kristen_mates.fq`, `kristen_unmapped.fq`, `kristen_junction_clusters.txt`
- **Stage 3 assembly:** `/home/rempel/genomes/kristen/omega_extract/kristen_contigs.fa`
- **Stage 4 filtered:** `/home/rempel/genomes/kristen/omega_extract/omega_candidates.tsv`
- **Gate 2 DBs:**
  - kraken2: `/home/rempel/genomes/kraken2/` (standard DB)
  - UniVec: `/home/rempel/genomes/univec/UniVec` + `UniVec_Core` (BLAST DB built)
- **Oliver alignment:** running bwa-mem, 3 processes remain, no final BAM yet

### Board / Comms
- **Bulletin board:** `python "C:/claude_base/branch_bulletin/bcast.py"` (post, read, catchup, wake, room)
- **Omega room:** `python "C:/claude_base/branch_bulletin/bcast.py" room omega_contig` (x1+X21B+X11B)

### Other workers
- **x1** - working body, owns Gate 3 (T2T/pangenome), on Sol/Lak
- **X5** - manages Oliver's alignment on asto
- **X7A** - original contig-idea author
- **X10A** - Track-1 manager (INSurVeyor)
- **X11B** - cross-person recurrence aggregator + segdup masks

---

## GOTCHAS

1. **The omega shape alone means nothing.** Empirically proven: a 2 Mb test slice produced ~35 omega-shape clusters. Genome-wide that's **thousands** - every Alu, LINE, SVA, and HERV looks like an omega contig. The five specificity gates are not optional; they're the entire game. The census will be dominated by known human mobile elements.

2. **"Near-human-diverged" is the most exciting AND the most artifact-prone bin.** A ~95% human-like payload can be a distant relative (the target) OR an ordinary segmental duplication / paralog mismapping (exactly X11B's segdup warning). This bin stays in the catalog but gets flagged for extra cross-checks before interpretation.

3. **Asto uses numeric chromosome names** (e.g. `20`, not `chr20`). Any script or query using `chr20` will silently return zero hits. The Python extractor handles this, but downstream tools (minimap2 alignments, BLAST) need numeric contig IDs.

4. **The distrobox has only mawk, not gawk.** The original shell extraction died because mawk lacks 3-arg `match()`. The fix was rewriting Stage 1 in Python. Don't write new awk-dependent code without checking the flavor.

5. **Per-cluster megahit is too slow at genome scale.** Spawning one megahit per cluster (hundreds to thousands of clusters) serializes poorly even on a free box. The v02 per-cluster script exists but needs parallelization or a lighter assembler before it's practical for the full run. v01 pooled assembly works for the first pass.

6. **Kristen's BAM is aligned, not raw reads.** The extraction works from the BAM - it pulls reads with soft clips + unmapped reads + their mates. The pipeline assumes an existing BAM; it doesn't do alignment from FASTQ.

7. **No blind filtering - inventory first.** The design changed mid-stream from "gate = delete" to "gate = annotate-and-tally." All five gates must label, not drop. The output is a full census table with one row per candidate and per-gate annotation columns. Exclusions happen only after Max reviews the distribution.

8. **Population frequency is the calibration axis, not a yes/no filter.** "Found in a database" does NOT disqualify -
