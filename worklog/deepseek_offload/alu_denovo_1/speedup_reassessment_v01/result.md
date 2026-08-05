## Most Likely Missed Bottleneck & Best Redesign

**Bottleneck:** Per‑locus samtools invocations. Each of ~15k–20k AluYa5 loci × 22 chromosomes × 3 CRAM files spawns a separate `samtools view` (or `mpileup`) process. This causes:  
- Repeated process startup (~50–100 ms per call).  
- Fragmented CRAM index seeking and decompression (single‑region random access in CRAM is expensive).  
- Redundant reference base extraction and annotation parsing for every locus.  
Total overhead easily dominates the actual read filtering, likely 10–50× slower than a batched alternative.

**Best Redesign: Single‑pass pileup per trio**  
1. Merge all AluYa5 loci across autosomes into one BED file (positions fixed, invariant).  
2. Use a single `samtools mpileup` command with `-b triobams.list -l all_loci.bed -q <mapQ_cutoff> -Q <baseQ_cutoff> -d 10000`.  
3. Parse the pileup output: for each position, tally child alleles vs. parental alleles. Apply the same read‑level filters (e.g., mapQ≥60) that were applied in the per‑locus script.  
4. Output candidate positions where the child has an allele supported by ≥1 high‑quality read not observed in either parent.  

This eliminates repeated startup, inter‑chromosome checkpoint overhead, and redundant I/O. If pileup cannot replicate the exact read‑pair or CIGAR filters, use `samtools view -L all_loci.bed` for each sample (three consecutive invocations) and process all reads in memory per locus – still one streaming pass per sample instead of thousands of queries.

## Expected Speedup (Cautious)

- **Old:** ~8h / trio (19,000 sec) – dominated by per‑locus overhead.  
- **New:** Batch streaming reduces overhead to ~5–10% of original. Conservative estimate:  
  - CPU/filtering time unchanged (~20 minutes).  
  - I/O + startup reduces from ~7.5h to ~20 minutes.  
  - **Total ~40–50 minutes per trio → 10–12× speedup.**  
  More optimistic: 40× (if original overhead was 95%).  
  *Range: 5×–40×*, but likely >10×.

## Lossless Benchmark Plan

1. **Choose chromosome 22** (small, quick to test).  
2. **Old pipeline** on chr22: record exact output (list of candidate positions, with supporting read counts).  
3. **New pipeline** on same chr22: produce output with identical filtering logic (re‑implement the original filter, but batched).  
4. **Compare outputs** (sorted, tuple‑wise). Must be identical. If not, adjust filter parameters until identical.  
5. **Full trio**: run new pipeline on all 22 autosomes, measure wall time vs. old 7h56m. Confirm final candidate list matches old full‑trio output.  

*No per‑locus divergence allowed.* Use a regression test harness that diffs the sorted candidate list.

## Time Estimates for 50 / 100 / 300 Trios (If Redesign Works)

Assume linear scaling, no parallelization across chromosomes (single trio per job, 2 cores, 6 GiB).  

| Trios | Old (8h/trio) | New (1h/trio) | New (0.75h/trio) |
|-------|----------------|----------------|-------------------|
| 50    | 400 h (16.7 d) | 50 h (2.1 d)   | 37.5 h (1.6 d)   |
| 100   | 800 h (33.3 d) | 100 h (4.2 d)  | 75 h (3.1 d)     |
| 300   | 2400 h (100 d) | 300 h (12.5 d) | 225 h (9.4 d)    |

Even modest speedups dramatically reduce calendar time.

## Important Risks That Could Silently Change Calls

1. **Read‑filter parity** – The original per‑locus code may have used flags like `-F 0x100` (secondary), `-f 0x2` (proper pair), or custom mapQ thresholds tied to read alignment context. These must be exactly replicated in the batched `samtools mpileup` or `view` arguments. A mismatch will alter the candidate list.  
2. **Depth cap** – `mpileup -d` default is 250; if a locus has depth >250, bases are skipped, silently losing evidence. Use `-d 100000` or disable the cap.  
3. **Reference anchoring** – The original might extract reference bases via `samtools faidx` for each locus. In batch mode, pre‑extract the reference for all positions into a FASTA index or use the REF column from mpileup. Ensure identical reference extraction.  
4. **Indel handling** – If the “allele” is a structural variant (e.g., presence/absence of an Alu insertion), pileup may not represent it correctly. Then `samtools view -L` with read‑level processing is needed, which is still batched but requires careful parsing of split reads / discordant mates.  
5. **Random‑access indexing** – CRAM index efficiency varies. A single `samtools view -L` with thousands of regions may still cause fragmentation, but far less than per‑locus calls. Test with `samtools view -L` without sorting regions; if needed, sort the BED by coordinate to help index prefetching.
