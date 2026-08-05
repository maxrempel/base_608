# Scribe handover - milestone 6 (~472K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 13:53:06 by deepseek-v4-pro

# HANDOVER: Omega Contig Foreign DNA Insertion Detector for Kristen

## GOAL (in Max's own words)
Find foreign (non-human) DNA spliced into Kristen's genome. Not just "alien-alien" - catalog everything: human-out-of-place, animal, bacterial, viral, near-human-diverged, and unknown. Look for artificial insertion signatures (CRISPR-style, no natural transposon scar). Look for transposon-like insertions that are NOT known transposons. Expect ~2-5% foreign DNA but each insertion rare in the population (a few percent of people, not common). Document everything as a reference catalog first, calibrate filtering only after seeing the real numbers. This is a long-term project to compare across self-reported abductees. Speed target: ideally 5 hours, <1 day acceptable, >1 day suspicious.

## DECISIONS MADE + WHY

- **Omega contig shape**: first and last ?100 bases must map to human, same chromosome, same orientation, adjacent head-to-tail (single clean breakpoint). The middle maps to nothing human = foreign payload. Tolerance: within ~20 bp of exact adjacency, gap recorded. This captures clean insertions and ignores messy ones. Target: germline (~99% of cells), so VAF not a limit at 30x.

- **Inventory-first principle** (Max): The 5-gate cascade is NOT a delete-filter. Every candidate is kept and labeled. Output is a full census with per-category counts. Excluded bins stay visible with reasons. Nothing dropped silently.

- **Four classification dimensions** (Max):
  - A: Origin + % relatedness (human-out-of-place, near-human-diverged, known organism, unknown)
  - B: Insertion signature - natural (TSD, poly-A tail) vs artificial (blunt ends, no scar)
  - C: Population frequency - rare tail (a few % of people) is the sweet spot; "in a database" doesn't disqualify unless common
  - D: Cross-locus clustering - a large family of near-identical payloads at scattered loci that matches no known transposon = predicted signal

- **Targeted assembly, not full de novo**: assemble only reads around junction neighborhoods (soft-clipped + mates) instead of whole genome. Same omega result, vastly cheaper. v02 per-cluster assembly assembles each breakpoint separately for cleaner contigs.

- **Resumable, chunked, scatter-gather**: split by chromosome, each chromosome has a RUN_COMPLETE marker. Per-cluster assemblies have .done markers. Genome driver skips completed work. NPROC tunable per machine load.

- **Resource policy on asto** (Liz's machine, borrowed): all four resources (CPU, RAM, disk I/O, network) capped under ~50% ideal, 70% hard max. Network near-zero (no internet downloads, everything local). asto runs distrobox with samtools/megahit/minimap2/kraken2 already installed.

- **Pilot-first graduated scaling** (Max): 5 MB slice ? chr22 ? chr21 (acrocentric stress-test) ? genome-wide. Each step measured before scaling.

- **Read-cap and per-worker memory limit**: to prevent OOM kills from huge centromere/repeat pileups (chr12 died repeatedly from this). Cap: READCAP=2000 reads per window, plus per-cluster memory ulimit.

## CURRENT STATE (as of last tick)

- The genome-wide run is **LIVE on asto** in a detached tmux session named "omega".
- Machine: asto (16 cores, 31 GB RAM), load currently moderate. BAM is clean and verified (symlinked, no copy needed).
- The run is throttled (nice -n 15), NPROC=3, READCAP=2000, resumable.
- So far: chr1 completed with 0 candidate foreign insertions. Remaining chromosomes (chr2-22, X, Y) are queued to process. ETA ~2-3 hours from launch (~16:20 PT).
- All pipeline scripts are committed and pushed to git origin. Latest versions include the fix for the mkdir-before-redirect bug and the false-completion guard.
- The 5-gate cascade is scaffolded but only gate 2 (kraken2 organism-ID, UniVec vector check) is fully built; gates 1 (mobile element repeat classifier), 3 (T2T/pangenome ref-gap check, assigned to x1), 4 (junction proof with spanning reads), and 5 (population recurrence) are designed but not fully implemented. The census script is ready.
- The earlier chr1-12 run on Sol is **discarded** because Sol's hardware corrupted the BAM. asto's BAM is clean.

## EXACT NEXT STEP

1. Wait for the tmux session "omega" on asto to finish all chromosomes (check with `tmux attach -t omega` or read the log at `/home/rempel/genomics/omega_run/out/genome_run.log`).
2. Once GENOME_COMPLETE appears, run the census: `python3 /home/rempel/genomics/omega_run/scripts/omega_census.py /home/rempel/genomics/omega_run/out/genome > /home/rempel/genomics/omega_run/out/census.txt` to generate the full inventory.
3. Present the census to Max: total omega candidates, per-category breakdown, and any candidates that pass all gates (especially near-human-diverged, unknown, or artificial-signature).
4. If any strong candidate survives, build the missing gates (1,4,5) to vet them further.
5. Extend to other genomes (Oliver, etc.) for population-frequency analysis once the pipeline is proven.

## OPEN QUESTIONS (awaiting Max)
- Adjacency tolerance: ?20 bp with gap recorded? (default used, Max didn't object)
- Minimum supporting reads per border: defaulted to 8 per side (balanced, two-sided), but not explicitly confirmed by Max
- Threshold for "near-human diverged" % identity: not yet set; design says 90-98% but needs calibration from actual data
- The "plan document to memex" Max mentioned writing - has that been done? If so, it should be folded in.

## KEY PATHS / IDs
- **Git repo**: `C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd` (local), origin `C:\claude_base`
  - Pipeline code: `projects/XG1/kenefick/omega_detector/`
  - Design doc: `projects/XG1/kenefick/omega_detector/OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
  - Brainstorm doc: `projects/XG1/kenefick/FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md`
- **asto (Debian via Tailscale)**:
  - SSH: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
  - BAM: `/home/rempel/genomics/kristen.mq.bam` (35 GB, numeric contigs, clean)
  - Reference: `/home/rempel/genomics/GRCh38.fa` (numeric contigs)
  - Segdup mask: `/home/rempel/genomics/segdups_nochr.bed`
  - Run dir: `/home/rempel/genomics/omega_run/` - symlinks to BAM, ref, mask; scripts under `scripts/`; output under `out/genome/`
  - Distrobox container: `ubuntu` (has samtools, megahit, minimap2, kraken2, blastn)
  - Tmux session: `omega` (detached, the genome run is inside)
  - Log: `/home/rempel/genomics/omega_run/out/genome_run.log`
  - LAN IP: `192.168.1.243` (same subnet as Sol/Lak, gigabit)
- **Sol** (home server, 192.168.1.113): has 8 cores, 28 GB RAM, 826 GB free but **hardware corrupts large writes** - do NOT use for BAM storage or heavy jobs. It was tried, BAM copy corrupted twice.
- **Lak** (192.168.1.199): hosts Nextcloud, keep free.
- **Branch Bulletin board**: `bcast.py` commands in `C:\claude_base\branch_bulletin\` - used for x-team coordination. Room "omega_contig" for x1 and X11B coordination.
- **x-team members**: x1 (X1) - working body assigned to gate 3 (T2T/pangenome). X11B - recurrence aggregator. X10A - Track-1 mgr, ran INSurVeyor on Kristen (clean negative). X7A - originated the contig idea.

## GOTCHAS / DEAD ENDS RULED OUT

- **Sol corrupts files**: Two separate CRC32/BGZF decode errors at different offsets when copying the BAM to Sol. The BAM quickcheck (samtools quickcheck) false-passed because it only checks the EOF. Verified by full read scan. Sol's RAM/disk is untrusted for large data. Do not use Sol.
- **chr13-Y silent failure**: Was initially blamed on BAM corruption, but the real root cause was a bug in omega_genome.sh: it redirected the chromosome's log to `$O/region_run.log` *before* `mkdir $O`, causing all chromosomes to die instantly with no visible error. Fixed by adding `mkdir -p` before the redirect. Also added a guard: if no chromosomes processed, census aborts instead of reporting "0 hits".
- **False GENOME_COMPLETE**: Same bug caused GENOME_COMPLETE to be set with zero chromosomes done. Added guard.
- **distrobox+nohup fragility**: Launching background jobs inside distrobox requires careful tmux/screen session management. The current run uses `distrobox enter ubuntu -- bash -lc '...'` inside a tmux session.
- **Contig naming**: The BAM uses plain numeric chromosome names (e.g., `20` not `chr20`). All scripts assume this.
- **mawk vs gawk**: asto's distrobox has only mawk, so the initial awk-based extraction was replaced with Python (omega_extract.py) for CIGAR parsing.
- **PowerShell carriage-return mangling**: Using `tr -d "\r"` in PowerShell-launched SSH commands deleted all literal 'r' letters (the backslash is eaten by PowerShell). The fix is to use `tr -d '\015'` (octal) or to strip line endings via bash on the target machine. Always verify scripts on the target with `bash -n` after copy.
- **Read-cap needed for centromere regions**: On chr12, a centromeric repeat pileup fed thousands of reads into megahit, causing OOM kill (systemd-oomd). Fixed by READCAP=2000 (reads per window) and ulimit per worker.
- **Segdup mask alone insufficient**: The segdup mask only removes ~16% of clusters. The additional filter of "two-sided, balanced borders with support 8-100 reads per side" is what drops the count from thousands to the real candidate set (~332 per chromosome for chr21). Still respects inventory principle - everything counted, strong candidates assembled first.
- **Resumability works**: .done markers per chromosome and per cluster correctly skip completed work on relaunch. The v03 per-cluster runner is robust.
- **No false positives so far**: The omega adjacency filter correctly returns zero hits on normal chromosomes (validation slice, chr22, chr21, chr1-11). Any hit that actually survives the geometry filter will be a real structural anomaly.

## BRIEF TIMELINE
- X7A handed off the contig idea. X21B took ownership.
- Spec frozen: omega contig, inventory-first, four dimensions.
- Pipeline built and validated on small slices.
- Infrastructure debugged: Sol proved unreliable, asto proved reliable after fixing the mkdir bug.
- Genome-wide run launched on asto, currently in progress.

## TO RESUME THE COLD SESSION
- The autonomous loop is armed. The tmux session "omega" should still be running on asto. Check `tmux attach -t omega` or read the log. If the run finished, run the census. If it died, diagnose using the per-chromosome logs and resume (the .done markers will skip finished chromosomes). Do not trust any Sol-side results. The user (Max) is taking a break; do not need their input unless a significant candidate insertion is found.
