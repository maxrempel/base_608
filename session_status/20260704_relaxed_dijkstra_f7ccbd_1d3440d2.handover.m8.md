# Scribe handover - milestone 8 (~609K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 15:00:41 by deepseek-v4-pro

# HANDOVER: P3 OMEGA - Foreign-DNA Insertion Detector (Kristen / "Antoinette")

---

## GOAL (in Max's words)

Build a detector for foreign (non-human) DNA spliced into Kristen's genome. The target: germline clean-cut insertions where the human genome was cut at **one** spot, foreign DNA dropped in, and the two human sides stitched back - no human letters lost. Find them, catalog them by origin and insertion signature, and surface anything that looks artificial or non-human. This is a **long-term cataloging project** to be cross-referenced across multiple self-reported abductees over time.

Max's prediction: there will be **tons** of uniform, transposon-like-but-not-transposon insertions, not a single clean alien hit.

---

## DECISIONS + WHY

### 1. Method: Option B - "two half-chimeras" (the breakthrough)
**Original idea (Option A):** assemble one contig that spans the whole insert - `human | FOREIGN | human` in a single piece.

**Why Option B won:** For inserts longer than the read-fragment length, a single spanning contig breaks. Instead, assemble **two facing junction contigs** - each human-anchored on one side with a foreign overhang on the other. A **left half-chimera + right half-chimera at the same locus = the insertion**. This handles any insert length (validated at 1 kb and 5 kb positive controls) and recovers the payload from both directions.

**Decision maker:** Max - "Option B is terrific."

### 2. No blind exclusion - inventory first, calibrate second
All candidates are **kept and labeled**, not dropped silently. The 5 "gates" are annotators/counters, not filters. A full census gets produced first; we look at the real distribution and *then* decide thresholds.

**Why:** Max's core instinct - you can't defend "we found nothing" if the pipeline silently deleted candidates along the way. Also protects against the trap where a silently-dropped artifact masks a real signal at the same locus.

### 3. Hunt the rare tail, not unique or consensus
Real alien insertions are expected at ~2-5% population frequency - absent from the consensus genome, present in a small fraction of people. Not strictly unique (artifact-prone) and not common (ordinary human variants).

### 4. Four classification dimensions (not just "human vs. alien")
Every candidate is annotated across:
- **A - Origin + % relatedness** (human-out-of-place ? animal ? bacterial ? near-human-diverged ? unknown). "Nearly human but not human" (~90-98% identity) is a top-priority bin.
- **B - Insertion signature** (natural transposon scar vs. artificial/engineered - a transposon without its natural target-site duplication = candidate engineered, super-interesting).
- **C - Population frequency** (rare tail: a few % of population).
- **D - Cross-locus payload clustering** (look for a large family of near-identical inserts at scattered loci - Max's predicted transposon-like signal).

### 5. EC2 aborted - asto is the right place
**Attempted:** Spin a c7i.4xlarge on AWS us-west-2. **Measured real asto?cloud upload at ~2.7 MB/s** - 35 GB BAM = ~3.6 hours, and it hogs asto's bandwidth from Oliver. X12B's cloud works because their data is public and in-region (free instant read); ours is private behind a slow uplink.

**Decision:** compute stays where the data lives (asto). Instance terminated at negligible cost (~$0.20).

### 6. Sol ruled out - hardware corruption
Two copies of the 35 GB BAM onto Sol produced **two different random CRC32/BGZF corruptions at different offsets**. Confirmed by X10A as known bad hardware. Team rule: no genomics on Sol.

### 7. Using vendor BAM directly (no 15-hour realign needed for P3)
X10A found INSurVeyor gets 0 assemblies on Kristen's DRAGEN vendor BAM vs. 35k on Oliver's bwa-aligned BAM, triggering a diagnostic. P3 confirmed: the vendor BAM **keeps soft-clip sequences intact** (13,541 soft-clipped reads in 4 Mb of chr20 with full 150 bp sequence). The earlier "0 hits" on P3 was the broken **Option-A detector**, not the BAM. P3 runs fine on the vendor BAM.

### 8. Speed architecture: resumable, staggerable, chromosome-split
Per-chromosome `.done` markers. Per-cluster `.done` markers. Pilot-then-extrapolate. Target: ideally ~5 h, ?1 day acceptable, >1 day = suspicious (red flag to investigate, not wait out).

---

## CURRENT STATE

**What is DONE:**
- The **validated, working foreign-DNA insertion detector** (`omega_junction.py` + surrounding pipeline) - Option B junction half-chimera approach.
- **Positive controls PASS:** a synthetic genome with a known 1 kb insert is detected two-sided at the correct locus, recovering ~890 bp of the payload. Also passes at 5 kb insert.
- **First real run on Kristen:** chr22 of the vendor BAM produced **2 two-sided insertion candidates** (at chr22:19.9M and 22:22.4M) + **46 half-sided junctions** - the detector is alive and producing the signal Max expected.
- All code committed to git (branch `relaxed-dijkstra-f7ccbd`), auto-synced to Memex via `_tomemex` design doc.

**What is IN FLIGHT / BLOCKED:**
- **Genome-wide run on Kristen's vendor BAM** - launched on asto, completed chr1-4 (0 hits with the old broken detector), paused to yield to X10A's Oliver INSurVeyor (load hit 18, over the 12 threshold). chr1-4 results may be discarded (they used the broken Option A method).
- **Payload classification** - the candidates found on chr22 need to be classified (is the overhang truly foreign, or a human repeat / segdup artifact?).
- Waiting on **asto to free** from Oliver's priority work (X10A's INSurVeyor). The genome run is fully resumable.

---

## EXACT NEXT STEP

**When asto load drops below ~12 (Oliver's INSurVeyor done):**
1. Resume the genome-wide run on `kristen.mq.bam` (vendor BAM, at `/home/rempel/genomics/kenefick/kristen.mq.bam` on asto) using the **validated Option B** pipeline (the updated `omega_percluster.sh` with the wider fishing window + `omega_junction.py`).
2. Run in distrobox on asto, throttled (NPROC=3-4 niced, under 50% CPU/RAM/disk), resumable via per-chromosome `.done` markers.
3. Once genome-wide candidates are collected, run payload classification: kraken2 for organism ID, UniVec for vector check, RepeatMasker for known human mobile elements, T2T/pangenome alignment to rule out reference-gap artifacts.
4. Produce the full **inventory census** (`omega_census.py`): every candidate with all four classification dimensions, nothing silently excluded. Show the distribution, then calibrate thresholds.

**Key scripts (all on asto at `/home/rempel/genomics/omega_run/scripts/`):**
- `omega_genome.sh` - genome-wide scatter-gather driver (mkdir-before-redirect FIXED)
- `omega_run_region.sh` - per-chromosome pipeline
- `omega_percluster.sh` - resumable per-cluster assembler (with READCAP + wider fishing window)
- `omega_junction.py` - **the validated Option B junction detector** (the one that actually works)
- `omega_census.py` - inventory census script
- `make_pc.sh` - positive control builder (validates the whole pipeline)
- `omega_detector_v01.sh` - legacy Stage-1 extractor (still functional, but the Python extractor `omega_extract.py` is more robust)

**Launch command (from host, in tmux to survive SSH drops):**
```bash
tmux new -s omega -d "distrobox enter ubuntu -- bash -c 'cd /home/rempel/genomics/omega_run && nice -n 15 env BASE=/home/rempel/genomics/omega_run/out/genome NPROC=3 READCAP=2000 bash /home/rempel/genomics/omega_run/scripts/omega_genome.sh > /home/rempel/genomics/omega_run/out/genome_run.log 2>&1'"
```

**Watch with:** `tmux attach -t omega` or `tail -f /home/rempel/genomics/omega_run/out/genome_run.log`. Status check: `ls -d /home/rempel/genomics/omega_run/out/genome/chr*/RUN_COMPLETE`.

---

## OPEN QUESTIONS (awaiting Max)

1. **Adjacency tolerance** - I defaulted to allowing the two human anchors within ?20 bp of exact-adjacent (exact gap recorded per hit). Strict zero was discussed but not mandated.

2. **Minimum reads per junction side** - I'm using MINSIDE=8. Never explicitly calibrated with Max.

3. **Payload classification thresholds** - once the census comes back, we need to calibrate what counts as "near-human-but-not-human" (what % identity cutoff?) and what insertion-signature features flag "artificial." This was explicitly deferred to "look at the numbers first."

4. **Population-frequency reference** - X11B was building a cross-locus recurrence map + segdup masks. Current masks on asto are X9A's `segdups_nochr.bed` (numeric contigs). Full T2T/pangenome reference-gap gate (x1's task) is not yet on asto - only partially built on Sol/Lak.

---

## KEY PATHS / IDs / NAMES

| Item | Value |
|---|---|
| **Project** | XG1 / P3 OMEGA |
| **Branch** | `relaxed-dijkstra-f7ccbd` (C:\claude_base\.claude\worktrees\) |
| **Key dir** | `C:\claude_base\projects\XG1\kenefick\omega_detector\` |
| **Design doc** | `OMEGA_PIPELINE_DESIGN_v01_tomemex.md` (in that dir, Memex-synced) |
| **Kristen alias** | Antoinette |
| **Kristen vendor BAM (asto)** | `/home/rempel/genomics/kenefick/kristen.mq.bam` (35 GB) |
| **Reference (asto)** | `/home/rempel/genomics/refs/GRCh38.fa` (numeric contigs, no "chr" prefix) |
| **Segdup mask (asto)** | `/home/rempel/genomics/_analysis/segdups_nochr.bed` |
| **Run output dir (asto)** | `/home/rempel/genomics/omega_run/out/genome/` |
| **Scripts dir (asto)** | `/home/rempel/genomics/omega_run/scripts/` |
| **asto** | 192.168.1.243, 16 cores, ~31 GB RAM, Liz's box (borrowed), distrobox "ubuntu" |
| **Sol** | 192.168.1.113, 8 cores, 28 GB RAM, **CORRUPT - no genomics on Sol** |
| **Lak** | 192.168.1.199, Nextcloud host, critical - don't touch |
| **Centauri** | Windows box, same room |
| **EC2 instance** | Terminated - not worth it (slow upload from asto) |
| **Team board** | `C:\claude_base\branch_bulletin\bcast.py` |
| **Room** | `omega_contig` (on bcast) |
| **X1** | Working body, owns T2T/pangenome ref-gap gate (on Sol/Lak) |
| **X5** | Built Oliver bwa align, has Kristen fastq, realign queued |
| **X7A** | Originated the contig idea, handed ownership to X21B |
| **X10A** | P1 manager, INSurVeyor on Oliver/Kristen, coordinates asto priority |
| **X11B** | Cross-population recurrence counter, segdup masks |
| **X12B** | Running EC2 for 1000-Genomes scan (different project, public data) |

---

## GOTCHAS / DEAD ENDS

1. **Sol CORRUPTS DATA on write** - two copies of the 35 GB BAM gave two different random corruptions. Team rule: **no genomics on Sol.** Don't even try.

2. **EC2 is blocked by asto's slow uplink** - ~2.7 MB/s to us-west-2 = 3.6 hours for the BAM, and it hogs bandwidth from Oliver. Only viable if data is re-downloaded cloud-to-cloud from Sequencing.com (x1's territory, not set up).

3. **DRAGEN vendor BAM gave 0 INSurVeyor hits but is FINE for P3** - the soft-clip sequences are intact (confirmed on chr20). The 0 was the broken Option-A detector, not the BAM. Do NOT wait for the 15-hour realign for P3.

4. **Must mask AND cap reads before assembly** - chr21 alone produced 3,451 candidate sites (many in centromere/repeats, support 1,000+ reads). Without a segdup mask + READCAP, the assembler OOM-kills on the giant pileups. The fix: READCAP=2000, and only pass candidates through per-cluster assembly. Everything still gets counted in the census.

5. **`bash -n` before launch, not bash** - and strip CR with bash `tr -d '\015'`, **never** with PowerShell's backslash-r (it deletes all literal 'r' letters from the script).

6. **mkdir the chromosome output dir BEFORE redirecting the log there** - a one-line bug (`$O/region_run.log` redirected before `mkdir $O`) silently killed every chromosome. Fixed in `omega_genome.sh`. Also hardened against false "GENOME_COMPLETE" when zero chromosomes actually ran.

7. **Use tmux for long asto jobs** - asto's Tailscale SSH drops, killing foreground processes. Launch in `tmux new -s omega -d "..."` and check with `tmux attach -t omega`.

8. **`quickcheck` lies** - it only validates the BAM's end-of-file pointer. A corrupt block mid-file passes quickcheck. Use **full read-scan** (`samtools view -c`) or **md5sum** to verify copies.

9. **The "omega" shape alone fires thousands of times** - every Alu/LINE/HERV insertion looks like one. The shape is just the doorway; the payload classification and rarity checks are the whole game.

10. **There is NO positive control path in the current genome run** - the validated positive control (make_pc.sh) is a synthetic test, not wired into the real run. It lives as a separate validation script. If the real run returns surprising results, re-run `make_pc.sh` to confirm the pipeline is still working.
