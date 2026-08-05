# Scribe handover - milestone 2 (~156K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 08:02:44 by deepseek-v4-pro

# HANDOVER: Omega Contig Detector - foreign DNA insertion hunt (Kristen dataset)

## GOAL (in Max's words)
Detect **clean-cut, germline foreign DNA insertions** in the human genome - a single breakpoint, foreign payload spliced in, and both adjacent human edges still intact. The signature is an **omega contig**: first ?100?bp and last ?100?bp map to human at exactly (or almost exactly) the same adjacent position, head?to?tail, with high homology; the middle maps to nothing human.  Target is present in ~99?% of cells (VAF not a bottleneck at 30?).  This is the "contig idea" / Path B - junction?anchored local assembly to *see* the inserted payload, not just count anomalies.

## DECISIONS MADE + WHY
1. **Naming** - "omega contig" (?) because it sits on two human "anchors" with a foreign loop rising between them.  Anchors ?100?bp each, must be colinear and adjacent.
2. **Adjacency tolerance** - allow anchors to land within **?20?bp of exact adjacency**.  The exact gap is recorded; zero?gap clean splices stand out.  Rationale: natural insertions often duplicate a few target bases, so a tiny window avoids missing near?perfect hits while still spotlighting "engineered" zero?gap ones.
3. **Germline first** - only insertions present in nearly all cells.  No VAF problem, no deep resequencing needed.
4. **Targeted assembly over whole?genome de novo** - extract only reads that cross a human/non?human boundary (soft?clipped), their fully?foreign mates, and any unaligned reads; assemble *only those*.  Same omega result for a fraction of the compute, no big?RAM AWS box required.
5. **5?gate specificity cascade** (x1's contribution, accepted) - the omega geometry alone fires on every Alu/LINE/HERV, so classification is everything.  Five filters: (a) not a known repeat, (b) not a T2T/pangenome reference gap, (c) not coding (to remove human genes that look alien), (d) not a known virus (or if viral, distinct enough to be novel), (e) not a lab artefact.
6. **Labour split** - x1 builds the T2T/pangenome reference?gap gate on Sol/Lak; X21B owns the detector core (extract, assemble, anchor?map) and the remaining gates.

## CURRENT STATE
- **Spec frozen** - both in the master brainstorm doc and the omega?detector design doc (see key paths).
- **Pipeline code exists** (committed and pushed):
  - Stage?1 (`omega_detector_v01.sh`): extracts soft?clipped reads (the clipped half + its mate) from Kristen's BAM.
  - Stage?4 (`omega_filter.py`): reads assembled contigs, maps their first/last 100?bp to hg38, checks adjacency (within 20?bp) and high identity.  Real logic, not a stub.
  - Design doc outlines full pipeline: extract ? assemble (megahit) ? map anchors ? omega?filter ? classify (5 gates) ? report.
- **Tools available** on asto (in distrobox): samtools, megahit, kraken2, blastn.  **minimap2 still needs to be installed** (for mapping anchors back to human).
- **Kristen's data**: BAM at `/home/rempel/genomes/kristen/kristen.mq.bam` (35?GB).  Human reference index likely present.
- **Compute blocker** - asto is currently maxed (load 27 on 16 cores, <1?GB free RAM) by Oliver's alignment.  Nothing has been run against Kristen's BAM yet; execution is **held** to avoid starving Oliver's job.
- **Team wiring** - X7A handed off; X11B will consume per?sample omega hits for a cross?person recurrence map; x1 is building the T2T/pangenome gate.
- **Autonomous loop** - a decel timer (15?min, re?arming via `ScheduleWakeup`) is running; the conversation was being continued without Max.  The loop expects max silence; it will check for work each tick.

## EXACT NEXT STEP
**Run Stage?1 (extract soft?clipped reads) as soon as compute is available.**  The pipeline is ready to fire the moment a machine has free CPU/RAM.  The immediate sub?tasks:
- Identify a free machine - asto may still be loaded; **Sol or Lak are candidates** (x1 is using one for the ref?gap gate, but there may be headroom).  AWS is an authorised backup.
- Ensure minimap2 is installed and the hg38 index exists.
- Execute `omega_detector_v01.sh` against `kristen.mq.bam`.
- If extraction succeeds, proceed to assembly (megahit), then mapping and filtering with `omega_filter.py`.

While waiting for compute: continue developing the missing classification gates (repeat filter, coding filter, virus filter, artefact filter).  The T2T/pangenome gate is being built by x1 simultaneously.

## OPEN QUESTIONS (for Max when he returns)
1. **Anchor adjacency tolerance** - you approved a small window (~20?bp) in principle but gave only a brief nod.  Is ?20?bp acceptable as the default, or do you want a strict zero?gap requirement for the "cleanest" insertions?  (The code records exact gap value, so zero?gap hits are still separately visible.)
2. **Execution target** - should we move the first run to a spare box (Sol/Lak/AWS) rather than wait for asto to free up?  Awaiting your greenlight (or implicit acceptance via silence).
3. **Payload verification** - once omega contigs are found, what threshold of "novel" is credible?  Do we need *both* ends anchored and middle unclassified, or is a one?anchor contig also useful?

## KEY PATHS & IDs
- **Project directory**: `C:\claude_base\projects\XG1\kenefick\`
- **Brainstorm doc**: `FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md`
- **Design doc**: `omega_detector\OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
- **Script**: `omega_detector\omega_detector_v01.sh`
- **Filter**: `omega_detector\omega_filter.py`
- **git remote**: `origin` (working branch is likely `master`, but the folder was added and pushed without creating a separate PR)
- **BCast board**: `C:\claude_base\branch_bulletin\bcast.py` (commands: `whoami`, `catchup`, `post`, `wake`)
- **Timer tool**: `C:\claude_base\tools\timer_decel\timer_decel.py`
- **Server asto**: `rempel@astolfodebian.tail251d88.ts.net` (distrobox with tools)
- **Kristen BAM**: `/home/rempel/genomes/kristen/kristen.mq.bam`
- **Autonomous sentinel**: `<<autonomous-loop-dynamic>>` (used with `ScheduleWakeup`)

## GOTCHAS & DEAD ENDS ALREADY RULED OUT
- **No full?genome de novo** - ruled out as too expensive; we only assemble reads that can possibly form an omega contig.
- **Raw soft?clip counts** - earlier attempts just counted anomalies; we moved to contig assembly to read the payload.
- **Foreign reads without human anchors** - earlier assemblies (X8A's) used only non?human reads, missing integrated insertions; we deliberately keep the human?anchored side.
- **False?positive tsunami from repeats** - the omega geometry alone fires on every Alu/LINE/HERV, so classification gates are mandatory.  Without them, the pipeline produces noise.  The 5?gate cascade addresses this, but only the reference?gap gate is being built by x1; the rest still need implementation.
- **Compute starvation** - starting a heavy assembly on asto right now would kill Oliver's alignment; execution must move to another machine.
