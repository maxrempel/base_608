# Scribe handover - milestone 9 (~742K tokens)
# session: 20260705_kind_carson_2cc207_efece3bd
# cwd: C:\claude_base\.claude\worktrees\kind-carson-2cc207
# written: 2026-07-05 15:04:27 by deepseek-v4-pro

# HANDOVER - KENEFICK / XG1 GENOMICS (Session X5, 2026-07-01 through 2026-07-04)

---

## GOAL (in Max's own words, paraphrased)

Analyze the Kenefick family's whole-genome sequencing data (Kristen + son Oliver) for the XG1 experiencer study. The mission: **"look for traces of alien manipulation but not at the expense of truth."** Address Kristen Kenefick's specific anomaly claims - too much homozygosity, missing a parent, multiple X chromosomes, XX/XY chimerism, extra/missing gene copies - with **court-defensible, probabilistic numbers** on every single one. Produce analysis, not reassurance. The "prize" is the raw reads (FastQ), which hold unmapped/non-human reads.

Secondary tasks that emerged:
- Download the entire family's data from Sequencing.com (Kristen's account) to Centauri's `D:\genomics\kenefick\`, staggered to avoid getting blocked (Kristen ? Oliver ? twins).
- Build an aligned BAM for Oliver (his account had only raw FastQ - no pre-aligned BAM existed).
- Hunt for non-human / engineered / inserted DNA traces across the available genomes.
- Compare Kristen against proper controls (1000G genomes) to defuse her "1,500 homozygous inversions" and "my son shares them" claims.
- Send a carefully-framed letter to Kristen, drafted by X7A, approved by Max, presenting findings fresh (never a "correction" - per Max's hard rule).

**Standing constraints:** Chat ID "X5" (was "x1"); lead replies with "? X5"; experiencer honesty rule (raw counts + observations, never "normal" reassurance, no overclaim); X7A owns ALL outbound prose to Kristen; X5 = analysis only; short ping-pong replies; ? purple TLDR; ? burning / ? minor questions; plain English; no code shown; detached processes with logs; no sloppy fallbacks. **CRITICAL: "Don't give too many promises, don't make too harsh conclusions unless you are sure."**

---

## TEAM STRUCTURE (as of session end)

Max reorganized the team into **two self-managed tracks** so he could focus elsewhere:

- **Track 1 (Kenefick / alien-trace):** managed by **X10A**. Workers: X5 (alignments/QC), X8A (phasing/SV-staging), X9A (inversions/controls), X21B (OMEGA insertion detector), X1D (Genome Explorer rebuttal), x1 (downloads).
- **Track 2 (XG1 paper + hotspot map):** managed by **X7A** (also owns Kristen comms). Workers: X11B (recurrence/hotspot aggregator), X12B (per-trio NPA detector).
- **X5 role:** alignment worker + QC for Track 1. Owns the Oliver BAM pipeline and the Kristen bwa re-align. Does NOT write email prose (X7A's exclusive domain).

---

## DECISIONS MADE + WHY

### 1. Microchimerism: ~0.3%, not 5-9%
Three independent measures converged: SRY (single-copy male gene) at ~0.04x vs 30x autosome = **f ? 0.3%**; single-copy Y panel at MAPQ?30 = **0.1-0.3%**; autosomal Oliver-specific strict test = uniform signal ~0.26% VAF ? f ? 0.38%, with 100% of 101 genome bins above noise floor. The prior "5-9%" was inflated by three stacked artifacts: averaging only covered spots in Y genes, X-gametolog cross-mapping, and Kristen's own FAIL-filtered heterozygous sites leaking into the Oliver-allele count. **Decision:** the letter's "5-9%" is wrong; the real signal is ordinary fetal microchimerism (~0.3%).

### 2. Inversions: 29 not 1,500
Kristen's flagship claim - "1,500+ homozygous inversions, humans average 40-50" - was debunked by X9A running one consistent caller (Manta) on both Kristen and controls. Her real homozygous count: **29** (~15-18 after removing duplicate artifact calls). The "1,500" was Genome Explorer miscounting raw breakends. **Controls** (NA12718, NA18530) showed 28 and 40, putting Kristen squarely at/below the range she cited. Two unrelated strangers share 55% of their inversions, so Oliver sharing 73% with Kristen = ordinary inheritance.

### 3. Non-human reads: oral bacteria (saliva), no anomaly
Kraken2 classified the 8.5M unmapped reads: **45% bacteria** (dominated by oral *Streptococcus mitis*), **54% unclassified** (human-reference gaps + uncharacterized microbes). Assembled contigs showed broad GC spread (0.22-0.71) - a mixture, not a single novel genome. UniVec (cloning vector) screen by X8A: only 101 hits (0.11%), all on bacterial contigs = benign.

### 4. INSurVeyor (non-reference insertions) on Kristen vendor BAM: diagnosed, no re-align here
After many failed runs (MQ tag missing ? filter crash; fixmate ? zero assemblies), X5 ran a **clip_compare diagnostic** comparing Kristen's DRAGEN-aligned vendor BAM against Oliver's bwa-aligned BAM on chr21. Result: **DRAGEN soft-clips ~8? less than bwa** (27,536 vs 228,400 per 2M reads). INSurVeyor needs stacked soft-clipped reads at breakpoints to assemble insertions ? DRAGEN's sparse clips never stack ? zero calls. **Decision:** the vendor BAM is not treated as "broken" - OMEGA (X21B's detector) runs on it as-is and is the primary insertion tool. No 15h Kristen re-align was needed *for INSurVeyor alone.*

### 5. Oliver alignment: non-resumable ? chunked + resumable (MAJOR LESSONS)
The original `bwa mem` on Oliver was a single 9h non-resumable stream. Max correctly demanded it be restarted as chunked + resumable. What followed was a cascade of self-inflicted plumbing bugs (see GOTCHAS). The eventual clean run produced both BAMs (`oliver.mq.bam` for insertions, `oliver.fixed.bam` for Manta/phasing) and QC'd excellent.

### 6. Kristen bwa re-align (low/slow, for OMEGA's full sensitivity)
After the DRAGEN diagnosis cleared the INSurVeyor question, Max and X10A decided to run a bwa re-align of Kristen from her **original pristine FastQ** (conventional path - x1 staged them from Centauri) at low/slow priority (nice -19, 4 cores, chunked/resumable, ~2 days). This produces `kristen.bwa.mq.bam` + `kristen.bwa.fixed.bam` for OMEGA's maximum-sensitivity insertion detection and for X8A's phasing.

### 7. Letter strategy (X7A owns all prose)
- **Email-01** (sent earlier in the project): incorrectly claimed 5-9% male microchimerism. Max: "NO correction email, EVER. Forbidden." Any new letter must present findings FRESH, never reference the old number.
- **Email-02** (sent by X7A, Max-approved): presented the ~0.3% microchimerism finding cleanly, with the attribution "one of your sons (fetal microchimerism); which son comes out when their DNA is sequenced." No mention of prior claims.
- **Email-03** (drafted, held for Max): inversion rebuttal (29 vs 1,500) + controls comparison.

### 8. X5 LESSONS - error post-mortem
Max requested a public post-mortem of all mistakes in the Oliver alignment saga. Written as `oliver_align_postmortem_errors_v01_tomemex.md` and shared to the team board as "X5 LESSONS." Key lessons: measure ETA upfront, never run non-resumable multi-hour genomics jobs, kill whole process trees not just parent scripts, **never use PowerShell `sed` to strip CR** (it deletes every letter "r"), `part_[0-9][0-9][0-9].bam` glob not `*.bam`, report in Max's timezone (Pacific), blocked >1h on a sibling ? force-wake or scream.

### 9. Asto guest rules + compute limits
Max authorized **70% of cores (~11 of 16) and 70% of RAM (~22GB of 31GB)** for X5's jobs on asto (Liz's guest box). The `bwa shm` (shared-memory index) trick keeps RAM safe - one 5GB index copy shared across all aligner threads instead of one-per-process.

---

## CURRENT STATE (what is done, what is in flight)

### ? DONE - Delivered and Verified

| Item | Status | Location / Notes |
|---|---|---|
| **Kristen full WGS download** | Complete | Centauri `D:\genomics\kenefick\kristen\` (2 FastQ ~27GB each, BAM ~34GB, VCFs, chip) |
| **Oliver full WGS download** | Complete | Centauri `D:\genomics\kenefick\oliver\` (2 FastQ ~44GB each, VCFs, chip) |
| **Twins chip data only** | Complete | Centauri `D:\genomics\kenefick\twins\` (WGS dropped - no funding, Max's call) |
| **Oliver BAMs (both)** | **QC'd EXCELLENT** | asto: `/home/rempel/genomics/kenefick/oliver/` - `oliver.mq.bam` (65.7GB, no markdup ? INSurVeyor) + `oliver.fixed.bam` (65.8GB, markdup ? Manta/phasing), both indexed, quickcheck PASS |
| **Oliver QC certificate** | Written + committed | `projects/XG1/kenefick/oliver_BAM_QC_certificate_v01_tomemex.md` - mapping 97.49%, paired 95.91%, dup 3.76%, depth ~73? (ordered 30?), breadth 99%+, X and Y at half-depth (male) ? |
| **Kristen microchimerism** | Complete (court-grade) | `kristen_microchimerism_report_v01_tomemex.md` - verdict: genuine ~0.37% fetal microchimerism from a son, genome-wide uniform, rare-allele enrichment z=336 |
| **Kristen CNV claim** | Complete | 64 gains + 69 losses = ordinary range; zero calls on chrX |
| **Kristen homozygosity/ROH** | Complete | 2.67M het sites, het/hom 1.77, zero long ROH = two parents |
| **Kristen ploidy (X count)** | Complete | Two X (X depth ratio 0.92-0.98 vs autosome; X heterozygous) |
| **Kristen non-human reads** | Complete | 8.5M unmapped ? oral bacteria (45% *Strep mitis*, 54% uncharacterized); assembled contigs = broad-GC mixture; no alien/engineered signal |
| **Inversion claim (Kristen)** | Complete (X9A) | 29 homozygous (not 1,500); controls 28-40; Oliver shares 73% = normal inheritance |
| **Single-genome alien-trace hunt** | Complete, clean-negative across all lanes | Transposons (Alu normal), non-human contigs, engineered signatures (UniVec benign), integration junctions - nothing anomalous |
| **Kristen INSurVeyor diagnostic** | Complete | Root cause proven: DRAGEN soft-clips ~8? less than bwa ? no insertions assembled. No re-align needed for this. |
| **X5 LESSONS post-mortem** | Written + committed | `oliver_align_postmortem_errors_v01_tomemex.md`; reusable toolkit (`reskit`) extracted by x30b |
| **SSH-key sync plan for Sol** | Designed (handed to X8A) | Script ready: `sol_sync_keys_v01.sh` - pulls via rsync from Centauri (cleaner source than Lak) |

### ? IN FLIGHT

| Item | Status | ETA |
|---|---|---|
| **Kristen bwa re-align** (for OMEGA full sensitivity) | **RUNNING** on asto since ~17:23, chunked in 4-core low/slow mode, nice -19, resumable | **~1.5-2 days** (splitting ? aligning 12 chunks ? merge ? dual BAM) |
| **X10A Oliver INSurVeyor** (insertion callset) | Running on `oliver.mq.bam` (launched immediately; 35k assembled) | Minutes/hours |
| **X9A mother-son Manta** (shared inversions) | Running on `oliver.fixed.bam` | Hours |
| **X8A pedigree phasing** (Kristen+Oliver maternal-hap) | Rerunning on single-sample phasing after whatshap --ped limitation found | Hours |
| **X21B OMEGA** (Oliver-alone insertion vetting) | Oliver alone = clean negative; non-parental test gated on Kristen `kristen.bwa.mq.bam` | ~2 days (when Kristen BAM lands) |

### ?? PARKED / BLOCKED

| Item | Reason |
|---|---|
| **Oliver INSurVeyor via X5** | X10A owns it (running on `oliver.mq.bam`). X5 never runs Oliver INSurVeyor. |
| **Twins WGS** | Closed - no funding (Max: "the question is irrelevant") |
| **INSurVeyor on Kristen vendor BAM** | Closed - diagnosed as DRAGEN soft-clip sparsity; no re-align needed for this |
| **P1 folder move** (? `projects/XG1/P1_KENEFICK/`) | Deferred to after active jobs land (manager-approved) |
| **XG1 recurrence/hotspot** (Track 2) | X11B+X12B built detectors, waiting on x1 to stage 1000G trio data |
| **Sol phasing** | Sol had disk corruption, then phasing moved to asto; Sol is now "disposable workhorse" per Max |

---

## EXACT NEXT STEP

**The ONLY active task X5 owns is the Kristen bwa re-align.** It's running detached on asto via:
```
nice -n 19 setsid bash kristen_chunked_align_v01.sh run
```
Script: `/home/rempel/genomics/kristen_chunked_align_v01.sh`  
Log: `/home/rempel/genomics/_analysis/kristen_bwa.log`  
Chunks: `/home/rempel/genomics/kenefick/kristen/chunks_bwa/`  
Chunk BAMs: `/home/rempel/genomics/kenefick/kristen/chunkbams_bwa/`  
Outputs (when done): `kristen.bwa.mq.bam` + `kristen.bwa.fixed.bam` in `kenefick/kristen/`

**On each wake, check:**
1. SSH to asto: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net "distrobox enter ubuntu -- bash -lc 'cd /home/rempel/genomics; bash oliver_status.sh'"` (create a Kristen-status equivalent if not present). Alternatively, read the log: `tail -20 /home/rempel/genomics/_analysis/kristen_bwa.log` and count `.bam.done` markers in `kenefick/kristen/chunkbams_bwa/`.
2. Measure ETA from per
