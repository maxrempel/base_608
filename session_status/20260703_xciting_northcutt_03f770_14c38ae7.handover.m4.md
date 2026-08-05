# Scribe handover - milestone 4 (~301K tokens)
# session: 20260703_xciting_northcutt_03f770_14c38ae7
# cwd: C:\claude_base\.claude\worktrees\exciting-northcutt-03f770
# written: 2026-07-03 12:42:48 by deepseek-v4-pro

# Handover: X9A Inversion Lane - Kenefick Case

## Goal (Max's words)
"Address Kristen Kenefick's repeated 'inversions' claim. She says she has 1500+ homozygous inversions, her son shares them, and humans average 40-50. Show her flagged anomalies are normal by comparing to population databases + control genomes."

## Decisions made and why

1. **Re?call inversions from scratch instead of using her delivered SV file.**  
   The vendor (Sequencing.com) applied a filter `FILTER=PASS && ABS(SVLEN)<=100000` that silently removed *all* inversion calls because Manta writes inversions as BND pairs with no SVLEN. Her own file literally has zero inversions. So any count she cites didn't come from that file. We must run Manta on her BAM.

2. **Used the main chromosomes only (not the full reference) for Kristen, but built a name?matched reference with N?padded decoys.**  
   Her BAM is aligned to a 2581?contig GRCh38 (with decoys). The simple 25?contig reference failed because contig names didn't match. After several failed attempts with BAM subsetting (corrupted indices, broken reheaders), the successful approach was to give Manta the original full BAM and build a reference that contains the 25 main?chromosome sequences plus N?padded placeholders for all the decoy contigs, then restrict calling to main chroms. This avoided any BAM surgery.

3. **Control genomes: NA12718, NA18530, NA18488 (3 unrelated 1000G 30? CRAMs).**  
   X8A started the download but the curl/wget processes died between sessions (not detached properly). X9A took over the whole control lane with X7A's approval. Downloads survive session death through detached `setsid` execution.

4. **Bandwidth throttle required.**  
   Astolfo lives on a shared home link (Liz's house). The line was nearly saturated by our downloads. Max directed: measure the actual download speed, cap transfers to 70% during the day, 85% at night, re?measure every 3 hours. We measured ~1.66?MB/s total. Deployed a `throttle_daemon.sh` that uses `wget --limit-rate` with the capped value and re?probes the line periodically. The throttled daemon is currently downloading the remaining two CRAMs.

5. **Parallelising downloads was counterproductive.**  
   Three concurrent wgets split the same capped pipe and added overhead, so we reverted to serial. The throttle daemon downloads one CRAM at a time.

6. **Board pollution - x?only posts.**  
   After g4's order, all internal x?team genomics coordination is kept on the plain board (no `--joint` or `--all`).

## Current state

### Done and pushed
- Kristen Kenefick inversion analysis **complete** and committed to git (`7c35e768`):  
  - **Total inversions called: 263** (PASS)  
  - **Homozygous (1/1) PASS: 29** (the number she disputes; real distinct loci ~15-18 after removing duplicated breakend?pair double?calls)  
  - 83% of her inversions fall in known inversion?prone regions (segmental duplications, repeats)  
  - gnomAD?SV annotated: 42 of hers match known common population inversions  
  - The analysis document lives at `C:\claude_base\projects\XG1\kenefick\analysis\inversion_analysis_X9A_20260703_v01_tomemex.md`.  
  - X7A has drafted email 03 from this result.

### In flight on asto (remote compute, survives session death)

- **Control genome NA12718**  
  - Full CRAM downloaded (15.4?GB)  
  - Manta is running on it (candidate?generation stage) ? expected completion ~1?hr after last poll (the poll was set, result awaited).  
  - The pipeline for this run uses the full reference `~/genomics/controls/Homo_sapiens_assembly38.fasta`.

- **Remaining controls NA18530 and NA18488**  
  - Being downloaded one at a time by a `throttle_daemon.sh` (runs detached with `setsid`).  
  - Current speed cap is 70% of measured line speed (?1.16?MB/s).  
  - NA18530 partially complete (~6.7?GB). Once download finishes, no automatic Manta run is wired; the original orchestrator that sequenced download?plus?analysis was killed and replaced by the throttled download?only daemon. **So an explicit Manta launch will be needed for each remaining CRAM after it finishes downloading.**

- **Oliver (son) BAM**  
  - Alignment is in progress (coordinate?sort stage) by X5, expected ~1-3?h from the last update. Once ready at `~/genomics/oliver.fixed.bam`, X9A will run the identical Manta pipeline to compute mother?son inversion?sharing count.

### Tools/setup on asto
- Distrobox container `ubuntu` with samtools, bcftools
