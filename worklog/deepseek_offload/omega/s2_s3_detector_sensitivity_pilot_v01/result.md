## Implementation Review & Specification

### Method Review

- **CIGAR/coordinate correctness**: Synthetic reads must use correct `SA` tags, CIGAR strings (e.g., `30S150M`, `150M30S`, `60M40I100M`) that align unambiguously to the reference locus. Overlapping insertion-spanning reads require two-side mates that jointly cover the insertion. **Recommendation**: Generate paired-end reads (insert size ~350 bp) with consistent orientation (FR) to match typical libraries. Use `wgsim` or custom Python with `pysam` to produce exact CIGARs. Validate with `samtools cigar` and `bamclipper`-like clipping compliance.
- **Assembly recoverability with MEGAHIT single-end**: MEGAHIT works on single‑end but paired‑end improves contiguity. **Fix**: Merge synthetic reads into the original BAM as paired-end (same read names with `/1`, `/2`). The original slice contains real paired reads; synthetic reads must be appended with proper pairing to avoid broken mates. Alternative: keep synthetic reads as unpaired but mark them with a unique read group and ensure the detector’s assembly step accepts single‑end input (check `megahit --single`). If the detector expects proper pairs, force paired synthetic reads.
- **Outcome blindness**: Loci selected purely from reference, mask, and depth stats; no candidate/outcome files read. Good. Depth band chosen from bounded summary (e.g., chr22:20,000,000‑20,500,000 with depth 30‑50x). Private truth manifest stored outside pipeline; no sample/tier labels in file names passed to detector.
- **Gate preservation**: All frozen settings are hard‑coded in the detector script; pilot must not alter them. Acceptable.
- **False‑positive accounting**: Run unmodified slice (sham) through the same pipeline; record any output call as FP. For spiked slices, all calls not matching truth are FP. Distinguish FP from detector failures (no call). Report per sample.

### Recommended Smallest Reliable Pilot

**Samples**: 2 accepted (S2, S3 via Centauri) + 2 cultured controls (e.g., NA12878, NA24385).  
**Loci per sample**: 2 clean chr22 regions (depth 30–50x, no repeats, no known variants).  
**Truth tiers per locus**: sham (0 support), 8+8, 12+12, 20+20. Duplicate each for reproducibility → 8 spiked intervals per sample.  
**Total runs**: 4 samples × (1 sham + 3 spiked) × 2 loci = 32 detector runs. Plus processing 2 loci × 4 unmodified slices = 8 FP baselines.

### Acceptance / Failure Criteria

| Metric | Acceptance | Failure |
|--------|------------|---------|
| Recovery (any tier) | ≥ 90% of spiked calls correctly detected (correct breakpoint, insertion sequence, TYPE=INS) | < 75% or any missing in 20+20 tier |
| False‑positive rate | ≤ 2% of total calls across all sham slices OR ≤ 1 call per slice | > 5% or any locus yields >3 FP calls |
| Depth/quality match | Callable depth (MAPQ≥20, BQ≥20) within 10% of planned depth across all tiers | Deviation > 20% |
| Attrition (reads failing QC) | ≤ 5% of synthetic reads dropped | > 10% |
| Checksums | All truth BAMs produce identical CIGARs to reference genome checkpoint | Any mismatch in CIGAR or sequence payload |
| Repeatability | Two replicates of same spike produce same call | Outcome varies between replicates |

Additionally: **Gate preservation check**: detector parameters must match frozen list (verified by `grep -E` in detector script). **Outcome blindness check**: no Omun outcome files read (verified via `inotify` on pipeline input directory).

### Pseudocode Structure

```python
#!/usr/bin/env python3
"""
OMEGA Pilot – Deterministic Positive-Control Spike-In
Run: <pilot.py> --config config.yaml --samples S2.bam S3.bam Ctrl1.bam Ctrl2.bam
"""

import yaml, pysam, random, subprocess, json, hashlib, os

# Stage 0: Configuration
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

REF = cfg["reference"]         # frozen reference FASTA
MASK = cfg["clean_mask"]       # BED of callable regions
DETECTOR = cfg["detector_bin"] # OMEGA detector executable
DEPTH_BAND = (30, 50)          # accepted depth range on chr22

# Stage 1: Locus Selection (deterministic, outcome-blind)
def select_loci(bam_path, ref, mask, n=2):
    # Use pysam idxstats, samtools depth on mask intervals
    # For each chr22 interval in mask, compute mean depth (skip if outside band)
    # Sort intervals by coordinate, pick first n with depth in band
    # Return list of (chrom, start, end) – start/end length ~1000 bp (spike window)
    pass

# Stage 2: Extract BAM Slices
def extract_slice(bam, region, out_bam):
    pysam.view("-b", "-h", "-o", out_bam, bam, region, catch_stdout=False)
    pysam.sort("-o", out_bam, out_bam)
    pysam.index(out_bam)

# Stage 3: Generate Synthetic Reads
# Payload: random 45bp non-reference sequence, MD5 deterministic
def make_synthetic_reads(ref_seq, ref_start, payload_seed, support_tier, read_group, out_fastq):
    # ref_seq = reference bases around insertion locus (chr22 region)
    # Pick insertion coordinate within region (e.g., mid)
    # Create three read types:
    #   1. Left-clip: CIGAR "30S150M", right breakpoint
    #   2. Right-clip: CIGAR "150M30S", left breakpoint
    #   3. Spanning: CIGAR "60M40I100M", inserts payload
    # Each read is paired; mate covers opposite side (insert size ~350)
    # Support_tier: number of pairs for each side (e.g., 8+8 means 8 RL pairs, 8 RR pairs)
    # Write to interleaved FASTQ (single-end if detector supports, else separate mates)
    pass

# Stage 4: Spike In
def spike_in(slice_bam, synthetic_reads_fastq, spiked_bam):
    # Convert synthetic FASTQ to BAM (using pysam or samtools fastq -> sam)
    # Merge with original slice (samtools merge)
    # Sort & index
    pass

# Stage 5: Detector Run (unchanged)
def run_detector(in_bam, out_dir):
    subprocess.run([DETECTOR, "-i", in_bam, "-o", out_dir], check=True)
    # Read all output files (*.vcf, *.log) into results dict
    pass

# Stage 6: Verification
def verify_results(truth_manifest, results, sample):
    # Check if each inserted call is recovered (approx coordinates, INS type, payload match)
    # Record FP from sham slices
    # Compute metrics
    pass

# Main
def main():
    truth_manifest = []
    for sample_bam in samples:
        loci = select_loci(sample_bam, REF, MASK)
        for region in loci:
            slice_bam = extract_slice(sample_bam, region)
            for tier in ["sham", "8+8", "12+12", "20+20"]:
                if tier != "sham":
                    syn_fq = make_synthetic_reads(REF, region, payload_seed=42, support_tier=tier)
                    spiked_bam = spike_in(slice_bam, syn_fq)
                else:
                    spiked_bam = slice_bam  # unmodified
                run_detector(spiked_bam, out_dir)
                results = parse_results(out_dir)
                record = {"sample": sample, "tier": tier, "region": region, "results": results}
                truth_manifest.append(record)
    # Compute overall metrics against acceptance criteria
    ok = check_criteria(truth_manifest)
    if ok:
        print("PILOT PASS")
        json.dump(truth_manifest, open("manifest.json","w"), indent=2)
    else:
        print("PILOT FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Shell Execution Wrapper (example)

```bash
#!/bin/bash
# Run for each sample
for bam in S2.bam S3.bam Ctrl1.bam Ctrl2.bam; do
    python pilot.py --bam "$bam" --ref ref.fa --mask callable.bed --out "${bam%.*}_pilot"
done
# Aggregate checksums
sha256sum truth_manifest.json
```

### Key Notes

- Use `PYTHONHASHSEED=0` and `numpy.random.seed(42)` for deterministic payload generation.
- Store private truth manifest with sample‑specific hashes; expose only de‑identified class (e.g., `accepted`, `control`) and tier.
- For Centauri route: BAM accessed via `http://.../S3.bam` using `samtools view -h https://...`; verify connectivity before pilot.
- **Edge case**: If MEGAHIT fails on single‑end synthetic reads, switch to paired‑end output (two FASTQ files) and merge into BAM with proper read pairs. Detector’s assembly step must accept PAIRED_END; update config if needed.
