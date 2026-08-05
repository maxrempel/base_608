# Scribe handover - milestone 9 (~715K tokens)
# session: 20260705_admiring_diffie_13ddd6_e5142a61
# cwd: C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6
# written: 2026-07-05 15:48:28 by deepseek-v4-pro

# ? P3 OMEGA - HANDOVER FOR A COLD SESSION

---

## GOAL (in Max's own words)

Find **inserted DNA in Oliver's genome that is human-like but slightly diverged from the human consensus (0.5-10%)**. The hypothesis: aliens are humanoid, related to us, and would insert DNA that is **nearly-human but not quite** - drifted, rare, out-of-place. These inserts should show up as "omegas" (two human ends flanking a diverged middle), and the decisive filter is **non-parental**: present in the son but absent in the mother (or, via phasing, present on the maternal haplotype the son inherited but absent from the mother herself). The project is long-term; the first deliverable is a rigorous census of everything found, honestly classified.

---

## DECISIONS MADE + WHY

1. **Option B (fish-to-extend, NOT fish-to-close).** Max opted for detecting insertions via two facing "half-chimera" contigs (human-anchored on one end, extending into foreign/diverged sequence on the other). A single spanning `human|INSERT|human` contig is not required - two halves meeting at the same locus are the signal. *Why:* length-independent (a 1 kb or 50 kb insert reads the same), more robust than bridging the whole payload.

2. **Inventory-first, calibrate-second (no blind exclusion).** Count every candidate, annotate along all axes, learn the real-vs-artifact boundary from the distribution. Nothing is silently dropped. *Why:* Max's explicit rule - you cannot defend "nothing was found" if the pipeline deleted candidates en route.

3. **Out-of-place, NOT foreign-vs-human.** The target is **human-like but diverged/distant/relocated**, not "non-human." A payload that maps 100% to a different chromosome = interesting (relocated). A payload that is 93% human-like = interesting (drifted). A payload that is "unclassified" alone = NOT a finding. *Why:* the aliens are related to us - their inserts ARE expected to be human-ish, just slightly off.

4. **Divergence axis: 0.5-10% from GRCh38 consensus.** The sweet spot after recalibration. <0.5% = ordinary human polymorphism; >10% = not human-like enough to be related-aliens. *Why:* Max's correction after the "null" result - I had wrongly collapsed "maps to human" into "dismiss." The right axis is *how much* it differs from consensus.

5. **Pilot-prove before scale (hard rule in global2).** A small chromosome or region must be exhaustively QC'd before any genome-wide run. Positive control must PASS. Every candidate on the pilot must be examined close-up. *Why:* Max's standing rule - proper research, prevents chasing broken-detector zeros or over-caller noise.

6. **Manager/worker split.** Max split X21B into manager (keeps the plan, makes decisions, talks to Max) and X21C (production worker - runs code). X1 is also a P3 worker (gate3: T2T/pangenome/paralog filter). *Why:* X21B was polluting context with hands-on coding. The manager should NOT write code.

7. **Kristen BAM: bwa realign needed, not the DRAGEN vendor BAM.** The vendor BAM has ~8? fewer soft-clips, affecting detector sensitivity. X5 is producing `kristen.bwa.mq.bam` on asto (~4-5h ETA, was ~2 days but X5 bumped to 16 cores). *Why:* a clean negative on the vendor BAM is only a lower bound.

8. **Machine decisions:** asto (borrowed from Liz, 16 cores) - keep all four resources under ~50% / 70% max, niced. Sol is **banned** for genomics (corrupts data on write - two copies gave two different random corruptions). EC2 aborted (real asto upload to cloud is ~2.7 MB/s ? transfer too slow for private data). Xena exists as a spare server but not yet configured.

9. **Positive control first.** A synthetic genome with a known foreign insert, simulated reads, aligned to an insert-free reference. The detector must find it. Passes at 1 kb and 5 kb inserts (finds them two-sided at the correct locus). *Why:* without this, "0 hits" is uninterpretable.

---

## CURRENT STATE

### What's done (end-to-end, committed and merged to master)

- **Detector built and validated.** `omega_junction.py` (Option B half-chimera detector), `omega_percluster.sh` (resumable per-cluster assembler with READCAP and ulimit guards), `make_pc.sh` (positive control generator).
- **Genome-wide scan on Oliver (Oliver's good bwa-BAM):** 24/24 chromosomes, **743 two-sided insertions**, 21,049 half-sided junctions.
- **All 743 characterized:** mapped to GRCh38, measured divergence from consensus, taxonomically classified (kraken2), filtered for repeat-bleed recruitment, gene context annotated (GENCODE v46).
- **Deep-dig completed:** every candidate bin exhaustively examined. The honest result: all strong candidates trace back to known human sequence (the non-reference genome, fosmid clones, NA12878, etc.) - nothing exotic in Oliver alone. This is a **rigorous earned negative**, not a quick pass.
- **Recalibrated to the right axis (0.5-10% divergence):** when re-analyzed by *how much* each payload differs from GRCh38 consensus (not just whether it maps), there are **115 diverged human-like candidates** (0.5-10% divergence).
- **Paralog/segdup filter applied (by X21C):** cut 115 ? **22 clean single-locus non-segdup candidates.** The other 93 were multi-locus/high-identity paralogs - false alarms.
- **Non-parental sieve built and validated (k-mer method):** `nonparental_kmer.py` does NOT use soft-clips (DRAGEN-vs-bwa incompatible), it uses k-mer presence in raw reads - method-agnostic, validated Oliver-vs-Oliver returns all INHERITED as expected.
- **Research plan documented:** `OMEGA_RESEARCH_PLAN_v01_tomemex.md` - directions A (non-parental/phasing), B (paralog/segdup), C (archaic/population), D (families), E (cohort recurrence), F (gene function), G (dirty junctions).
- **Saved rules in global2.md:** "PILOT-PROVE BEFORE SCALE", "USE THE LLM TO LOOK AT REAL DATA CLOSE-UP", "RESPONSIBILITY TO ESCALATE BLOCKS" (blocked session waits briefly then alarms Max itself), and dictation-bug artifacts to ignore.

### What's in flight (work delegated to workers)

- **X21C (primary production worker):** reconstructing the 22 clean candidates to longer sequence (?400 bp per end) to strengthen the divergence signal, then running the maternal-haplotype non-parental test using X8A's existing phasing data.
- **X5 (P1, bwa realign):** producing `kristen.bwa.mq.bam` on asto (~4-5h ETA, 16 cores).
- **x1 (P3 worker, gate3):** building the T2T/pangenome reference-gap filter + providing the additional divergence reference for candidates that survive the reconstruction.

### What's blocked (genuinely, not sleeping)

- **Kristen.bwa.BAM** - the final non-parental sieve (is the insert in Oliver but absent from the maternal haplotype?) needs the fresh bwa-BAM. X5 is actively running it; ETA ~4-5h. This is a **real moving block** (not a sleep-forever).
- **Phasing data from X8A** - the maternal-hap assignment for Oliver's chromosomes is already computed (X8A's P1 pedigree phase). X21C should query X8A for the file path and integrate it into the sieve.

---

## EXACT NEXT STEP (for the manager)

1. **Wait for X21C to report the 22-candidate reconstruction results** - they should be longer, stronger, and annotated with proper divergence-from-consensus numbers.
2. **When Kristen's bwa BAM lands** (X5 will wake you), check with X21C: has the sieve run? What's the `MATERNALLY_ABSENT` count?
3. **Review the survivor list with Max in plain English** - which inserts, what genes, how diverged, and how many survive the non-parental + phasing filter. This is the real deliverable.
4. **If zero survivors:** the honest negative is earned and documented. Pivot to cohort-repeatability (direction E: same pipeline on other experiencers).
5. **If survivors exist:** send them through the archaic/population filter (direction C) and the cohort-repeatability check (direction E).

---

## OPEN QUESTIONS (awaiting Max)

- **Tolerance for the adjacency rule:** currently ?20 bp around exact head-to-tail, gap recorded per hit. Max had said to discuss - not yet confirmed.
- **Minimum reads per seam:** leaning ?2 per side. Not yet locked.
- **Xena (spare server):** Max mentioned it exists, is free, and could be spun up. Needed: IP, SSH key, OS confirmation, whether samtools/minimap2 are present. Manager should ask Max for these details when heavy compute is needed next.
- **Centauri** (Windows box in the same room): mentioned as having space, but Max wants it throttled if used. Not needed yet (Sol has 826 GB).

---

## KEY FILE PATHS

### Local (Pine, repo root `C:\claude_base\`)
- `projects/XG1/kenefick/omega_detector/OMEGA_PIPELINE_DESIGN_v01_tomemex.md` - **canonical design doc** (read first, contains breakthroughs + corrected target + full QC history)
- `projects/XG1/kenefick/omega_detector/OMEGA_RESEARCH_PLAN_v01_tomemex.md` - **research plan** (directions A-G, manager-owned)
- `projects/XG1/kenefick/omega_detector/FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md` - origin doc (Max's Path A/B/C)
- `projects/XG1/kenefick/omega_detector/` - all detector scripts
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - rules auto-loaded every session

### Remote (asto, `rempel@astolfodebian.tail251d88.ts.net`, SSH key `~/.ssh/bitwarden_ed25519`)
- `/home/rempel/genomics/omega_run/` - main run directory (symlinks to BAM/ref, scripts in `scripts/`)
- `/home/rempel/genomics/omega_run/out/genome_oliver/` - **Oliver genome-wide results** (per-chrom `chr*/`, `genome_run.log`, tmux session `omega`)
- `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/` - **characterization output** (payloads, `char_blast.tsv`, `CHARACTERIZATION.txt`, candidate lists)
- `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/diverged115_ranked.tsv` - the 115 cleaned candidates
- `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/cand27_ntblast.tsv` - nt-BLAST results for the 27 candidates
- `/home/rempel/genomics/omega_run/out/genome_oliver/out_of_place/` - out-of-place census (older axis, pre-divergence recalibration)
- `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` - Oliver's good bwa BAM (65.7 GB) - **the correct one**
- `/home/rempel/genomics/kenefick/kristen/kristen.mq.bam` - Kristen's vendor DRAGEN BAM (35 GB) - **the old, sensitivity-reduced one, NOT for production**
- `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` - Kristen's bwa realign (**in progress, X5, ~4-5h ETA**)
- `/home/rempel/genomics/omega_run/ref/GRCh38.fa` - human reference (numeric contigs - NO `chr` prefix)
- `/home/rempel/genomics/omega_run/ref/chm13v2.0.fa` - T2T-CHM13 full assembly (downloaded, ready)
- `/home/rempel/genomics/omega_run/scripts/` - all production scripts (CR-stripped via bash `tr`, NEVER PowerShell)
- `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/cand22_clean.tsv` - the 22 post-paralog-filter candidates (X21C's output)

### Team coordination
- `python C:/claude_base/branch_bulletin/bcast.py` - bcast board (room `omega_contig` for P3, use `read`/`post`/`wake`)
- Key contacts: X21C (production worker, clone), x1 (gate3 worker), X5 (bwa realign, Oliver alignment owner), X8A (pedigree phasing/maternal-hap), X10A (P1 manager, resource coordination)
- Name anonymization: Kristen?Antoinette, Oliver?Theodore, Kenefick?Whitfield (use on shared/cloud artifacts)

---

## GOTCHAS + DEAD ENDS RULED OUT

1. **Sol corrupts data on write** - two BAM copies to Sol produced two *different* random corruptions (CRC32 and BGZF errors at different offsets). `samtools quickcheck` false-passes because it only checks the EOF magic bytes. Team rule: **no genomics on Sol.** asto uses symlinks to the verified BAM (no copy = no corruption).

2. **EC2 is not worth it for single-private-BAM runs.** Real asto?us-west-2 upload is ~2.7 MB/s (measured, not guessed), so transferring 35 GB takes ~3.6 hours. EC2 is good only for data already in the cloud (like X12B's public 1000-Genomes reads in-region). Re-downloading Kristen from Sequencing.com cloud-to-cloud is theoretically possible but belongs to x1's lane.

3. **DRAGEN vendor BAM has ~8? fewer soft-clips than bwa.** The vendor BAM is usable (OMEGA detector works on it), but any negative result is a **lower bound**, not a clean negative. The production detector should run on bwa BAMs. Oliver HAS a proper bwa BAM (`oliver.mq.bam`). Kristen's is being produced now.

4. **Soft-clip-based non-parental comparison is broken** - the first sieve v1 (counting clips per locus) failed validation because Oliver's DRAGEN BAM has ~8? fewer clips than the incoming Kristen bwa BAM. The fix is v2: k-mer presence in raw reads (alignment-method-agnostic). Validated Oliver-vs-Oliver: all 12 test candidates correctly returned INHERITED.

5. **"0 hits" is meaningless without a positive control.** Earlier in the session, "0 hits" was reported twice - once from a broken Option A detector, once from a mkdir-before-redirect bug that silently killed every chromosome and then ran a census over zero results. Both were caught. The positive control (`make_pc.sh`) now runs first and must PASS before any genome-wide run.

6. **Divergence vs. GRCh38 alone is an artifact trap.** A payload that is 85% identical to GRCh38 may be 100% identical to the full human pangenome (T2T, fosmid clones, NA12878) - just missing from the old reference. **Every diverged candidate must be checked against T2T + nt-BLAST.** The ~115 "diverged" candidates from the recalibration
