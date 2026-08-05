# Scribe handover - milestone 4 (~302K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 11:03:52 by deepseek-v4-pro

# Handover: Omega Foreign-Insertion Detector

## GOAL (Max's own words)
Find **germline clean-cut foreign-DNA insertions** in Kristen's genome - an "omega contig" where human-anchor | foreign payload | human-anchor, with the two human ends landing adjacent in the reference (one clean splice).  
Catalog **everything** that looks like an out-of-place insertion, classified by origin, relatedness, and insertion signature (natural vs artificial).  
Then hunt for:
- **Near-human-but-diverged** payloads (distant-relative alien signal)
- **Transposon-like but not known transposons** (uniform families of novel inserts)
- **Artificial insertion signatures** (missing natural transposition scars)
Later compare across multiple self-reported abductees.  
Speed target: ideally **~5 h**, ?1 day acceptable; >1 day = suspicious, investigate.

## DECISIONS MADE + WHY

1. **Targeted assembly, not full de novo**  
   Only extract reads straddling human/non-human boundaries, cluster by anchor locus, locally assemble - same omega signature, far cheaper, no giant RAM.

2. **Omega shape definition**  
   Two **anchors** ?100 bp each, colinear, head?to?tail adjacent (left end at chr:X, right end at chr:X+1). Tolerance ?20 bp, exact gap recorded per hit.  
   *Why*: maximises clean?cut insertions, tolerates small target?site duplications without losing near?clean ones.

3. **Inventory?first, calibrate?second (no blind exclusion)**  
   Every candidate stays; the 5 classification gates are **labelers + counters**. A full census is produced, then thresholds are set on real numbers. Nothing dropped silently.  
   *Why*: Max insisted - you can't defend a negative result if the pipeline deleted candidates along the way.

4. **Expanded payload taxonomy**  
   Not just "human/foreign". Every payload gets:  
   - **Origin** (human?out?of?place, animal, bacterial, viral, near?human?diverged, unknown)  
   - **% identity to human** (so "nearly human but not" surfaces)  
   - **Insertion signature** (natural transposon hallmarks TSD, poly?A tail, etc. vs. artificial/blunt)  
   *Why*: Max wants to catch everything from related?alien DNA to engineered transposons.

5. **Population?frequency prior**  
   Real alien insertions are **rare** (a few % of people), not common, not unique. Gate?5 records frequency, the sweet spot is the rare tail.  
   *Why*: Common = ordinary polymorphism; unique = artifact?prone. Rare tail is the search space.

6. **Cross?locus payload clustering**  
   Cluster payloads against each other; a **large family of near?identical inserts scattered genome?wide** that matches no known transposon = the predicted signal.  
   *Why*: Max's prediction - "tons of uniform transposon?like but not transposon inserts".

7. **Speed architecture**  
   - Split extraction **by chromosome** (24 parallel jobs), each with a `.done` marker.  
   - Assembly **per cluster, parallelised** (N at once), concurrency tuned to the box.  
   - **Pilot first** on chr21 to measure real timings, extrapolate ETA, size concurrency before full run.  
   *Why*: ?1 day target, resumable, staggerable.

8. **Machine choice: Sol, not asto**  
   asto is a borrowed shared machine, Omega is **4th in queue** - waiting forever. Sol is idle, 8 cores / 28?GB RAM / 826?GB disk, on same LAN. Copy BAM over LAN (gigabit, unaffected by dead house internet).  
   *Why*: avoid queue; respect guest limits on asto; Sol free and strong enough.

9. **Resource caps** (any machine)  
   CPU / RAM / disk I/O / network each **?50% ideal, ?70% hard max**.  
   *Why*: borrowed hardware, polite?tenant rule.

10. **Dead internet handling**  
    Downloads (mobile?element library, T2T refs) deferred; LAN transfer for binaries/data between asto and Sol is fine.  
    *Why*: house internet nearly unusable; LAN unaffected.

## CURRENT STATE

- **Pipeline scripts written, committed, and end?to?end validated** on a 2?Mb slice and full chr21 of Kristen's real data.  
  - Extraction (soft?clip detection, CIGAR parsing in Python) works with numeric contigs.  
  - Clustering, masked assembly, omega?shape filter all run clean; zero false positives on test regions.  
  - chr21 pilot: raw 3,451 clusters ? after segdup mask + two?sided balanced filter (L,R?8 reads) ? **332 real candidates** ? projects **~22?k** genome?wide.  
  - Pooled assembly gave zero hits; per?cluster assembly confirmed as the working detector.  
  - ETA: extraction + assembly ~30?min on 16 cores; total a few hours on Sol.

- **Gate?runner scaffolded**, but only gate?2 (kraken2 + UniVec) is ready on asto.  
  Missing: mobile?element library (gate?1), T2T/pangenome refs (gate?3, x1 building on Sol/Lak), population?cohort data (gate?5,
