# OMEGA detector sensitivity pilot: implementation review

Draft a compact implementation specification for an outcome-blind, deterministic positive-control pilot of the frozen OMEGA insertion detector.

The pilot must run on accepted S2, accepted S3 through its verified Centauri HTTP-range route, and two representative cultured controls. It must not inspect or use existing Omun outcomes when selecting loci or constructing truth. It must preserve the frozen detector settings: autosomes only; soft clip at least 30 bases; cluster window 20 bases; at least 5 clip records; clean-region mask; at least 8 reads on each breakpoint side; canonical two-sided assembly; callable D10 uses MAPQ at least 20 and base quality at least 20; rarity threshold 0.001 and frozen reference hashes.

Proposed method:

1. Select one or a few clean chr22 loci per sample deterministically from reference/mask and bounded depth summaries only, in a common callable depth band. Do not inspect candidate or outcome files.
2. Extract a small coordinate-sorted BAM slice from each accepted input.
3. Create synthetic high-quality reads from the frozen reference plus a deterministic non-reference payload, preserving a real sample read group. Include left-clip, right-clip, and overlapping insertion-spanning reads. Produce three truth tiers (8+8, 12+12, 20+20 breakpoint-side support) plus an unmodified sham interval.
4. Merge each spike with its original bounded slice, sort/index, and run the unchanged detector scripts. Run the unmodified slice through the same pipeline for false-positive measurement.
5. Keep a private truth manifest and expose only deidentified sample class, support tier, recovery stage, false-positive count, callable depth/quality match, attrition, checksums, and limitations.

Review the method for CIGAR/reference-coordinate correctness, assembly recoverability with MEGAHIT single-end reads, outcome blindness, gate preservation, and false-positive accounting. Recommend the smallest reliable pilot and explicit acceptance/failure criteria. Give pseudocode or shell/Python structure, not a long report. Do not include credentials, private participant metadata, read names, or genomic coordinates.
