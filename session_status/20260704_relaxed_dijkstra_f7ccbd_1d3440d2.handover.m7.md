# Scribe handover - milestone 7 (~525K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 14:14:23 by deepseek-v4-pro

## Handover - Omega Contig Foreign?Insertion Detector (X21B/P3 OMEGA)

### Goal (in Max's own words)
Build a detector that finds **germline clean?cut foreign DNA insertions** in Kristen's genome - the literal "alien insert" test. The method is to reassemble reads across the splice into **omega contigs** (`human?anchor | FOREIGN payload | human?anchor`), catalogue **every** candidate (no blind exclusion), then classify by origin, insertion signature, and population frequency. The detector should produce some noise (e.g. ordinary transposons) so we know it's alive - zero hits across four chromosomes means it's too harsh.

### Decisions made and why

1. **Omega contig shape** - two human **anchors** (?100?bp, same chromosome, orientation, adjacent head?to?tail within ?20?bp) with a non?human middle. Named after ?: two feet planted, loop rising.
2. **Target germline** (~99% of cells). At 30? the VAF is no limit.
3. **Five?gate specificity cascade** (x1's contribution) - but converted from *delete?filters* to **labelers/counters** per Max's rule: *inventory everything first, calibrate thresholds later*. Nothing dropped silently.
4. **Machine saga** - Moved from **Sol ? asto ? EC2 ? back to asto**.
   - Sol had corrupting hardware (BAM got random CRC/BGZF errors on write) - abandoned.
   - EC2 attempted but asto's real upload to cloud is only ~2.7?MB/s (35?GB ? 3.6?h), aborting. Data must stay on asto.
   - Final home: **asto** (debian, 16 cores, borrowed). The BAM, tools, and scripts are all there. Run throttled (?50% of CPU/RAM/disk/net) and yield to higher?priority jobs.
5. **Pipeline built and validated end?to?end on small slices** (5?Mb, chr22, chr21). Extraction, clustering, assembly, and omega filter all run cleanly. The per?chromosome genome driver is resumable (`.done` markers).

### Current state
- The genome?wide run on asto **paused** after chr1?chr4 (so far: **0 omega hits**). asto is currently busy with Oliver's INSurVeyor; we yielded. Everything is resumable, no data lost.
- The pipeline's **omega filter returns zero hits even with extremely loose parameters** (anchor 30?bp, adjacency ?500?bp). The raw candidate sites are plentiful (~1400?1700 per chromosome), but the assembled contigs mostly have only one human mapping - i.e. they reconstruct the human locus, not a two?anchor omega. The filter therefore catches nothing, at any threshold.
- **There is no positive control** - we have never confirmed the pipeline can produce an omega hit on a known insertion. Thus "0 hits" is uninterpretable.

### Exact next step
**Max's last words** were to review the parameters because zero hits across four chromosomes means they are too harsh. The reply diagnosed that the issue is likely upstream of the filter (the assembler isn't producing the omega shape). Two concrete proposals were put to Max:

- **(A) Positive control first** - insert a known foreign sequence into a handful of synthetic reads and confirm the pipeline outputs an omega. This proves liveness.
- **(B) Direct soft?clip analysis** - gather the clipped?off payload sequences per site directly (no assembly) and classify them. This provides the expected "noise" signal and is more sensitive.

Max hasn't decided yet. The **next step is to wait for his direction** on which to pursue (or both). Meanwhile, asto can be checked periodically; once Oliver's job finishes, the remaining chromosomes (chr5?Y) can be resumed immediately if Max prefers to let the existing scan complete.

### Open questions for Max
1. **Which path first?** (A) positive control, (B) direct soft?clip cataloguing, or both in parallel?  
2. **Should the omega filter be loosened to allow** the payload to map to known repeats (Alu/LINE etc.) so we see the ordinary insertion "noise" you expect? Currently the filter demands the middle map to *nothing human*.  
3. **Do you want to let the paused genome scan finish** once asto is free, or pivot entirely to the new approach?

### Key file paths and IDs
- **Project root (Pine)**: `C:\claude_base\projects\XG1\kenefick\omega_detector\`
  - Core scripts: `omega_extract.py`, `omega_percluster.sh` (resumable, per?site assembler), `omega_run_region.sh` (per?chromosome driver), `omega_genome.sh` (whole?genome driver), `omega_filter.py` (omega geometry checker), `omega_census.py` (inventory counter), `omega_gates.sh` (gate runner), `omega_mask.py` (segdup mask filter)
  - Design docs: `FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md`, `OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
- **On asto** (via `ssh rempel@astolfodebian.tail251d88.ts.net`):  
  - Run directory: `/home/rempel/genomics/omega_run/` (symlinks to BAM, ref, segdup mask; scripts in `scripts/`; output in `out/genome/chr{1..Y}/`)  
  - BAM: `/home/rempel/genomics/kristen.mq.bam` (verified clean)  
  - Distrobox `ubuntu` has samtools, megahit, minimap2, kraken2, blastn, python3
- **Git**: all commits on `master` of `C:\claude_base`; team board via `python C:/claude_base/branch_bulletin/bcast.py`.
- **EC2** (already terminated): instance `i-096a1bc1b6557dd0e`, key `C:\Users\maxre\Nextcloud\zSyncMain\ssh\omega_ec2_antoinette.pem`.

### Gotchas and dead ends
- **Sol's disk corrupts BAM** - never put genomics data there.
- **asto's upload to cloud is ~2.7?MB/s** - moving the BAM off?site is not practical. Compute must stay on asto.
- **The `omega_genome.sh` bug** (log redirected before `mkdir`) has been fixed, but a past version caused instant failure. Current driver is fine.
- **The false "GENOME COMPLETE"** when nothing ran is now guarded against (census requires at least one chromosome with hits).
- **Contig naming**: the BAM uses numeric contigs (e.g. `20`), not `chr20`.
- **The omega filter is parameter?robust but the assembly output lacks two human anchors** - this is the current blocker. The pipeline's per?site assembly (megahit) may need a different input selection to force reconstruction of the junction rather than the host locus.
- **No positive control exists** - any future change to the pipeline must be verified with a synthetic known insertion before trusting results.

The next session should first get Max's decision on (A) vs (B), then act accordingly.
