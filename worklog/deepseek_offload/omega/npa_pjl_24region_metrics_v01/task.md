# Task

Draft a compact deterministic Python 3 program for a private genomic read-level comparison. Return only the complete program in one fenced code block.

Inputs:
- A variant TSV with columns: region_index, chrom, pos, ref, alt, region_id, region_start, region_end.
- Three sample sources in a JSON file. Each sample has sample_id, role, source_type (`cram` or `bam_dir`), source_path, and optional reference.
- For `cram`, query each requested region with `samtools view -h -T REFERENCE SOURCE REGION`.
- For `bam_dir`, a response manifest maps region to one coordinate-sorted BAM. Query that BAM with `samtools view -h BAM REGION`.

Privacy:
- Never emit or retain read names or SAM records.
- Write only aggregate per-sample/per-region metrics to a private TSV.
- Subprocess stdout must be consumed internally, never echoed.

Required deterministic metrics:
- raw primary records in region;
- records remaining after excluding flags unmapped, secondary, QC-fail, duplicate, and supplementary (mask 1796);
- records covering the exact site through a CIGAR-aligned base;
- ref, alt, and other base counts;
- variant allele fraction;
- alt forward/reverse counts;
- distinct alt alignment-start count;
- alt median mapping quality and base quality;
- max soft-clip length among alt reads;
- read-group counts summarized as number of groups, dominant group fraction, and a stable semicolon-delimited `RG_ID=count` string;
- library, platform-unit, platform, and sample metadata for observed read groups from the SAM header, summarized without read identifiers.

Frozen assessment:
- strict pass is depth >=20, alt_count >=10, VAF 0.25 through 0.75 inclusive, and alt on both strands.
- Report stage denominators and strict pass only; do not tune or add gates.

Implementation details:
- Parse CIGAR correctly for M, =, X, I, D, N, S, H, P.
- Base positions are one-based.
- Use csv/json/subprocess only from the standard library.
- Fail closed on missing source, missing manifest match, samtools error, duplicate variant key, or malformed input.
- Sort output by region_index then sample_id.
- Include SHA256 of each source file queried and the manifest where applicable, but do not hash the same large source repeatedly.
- Command line: program variants.tsv samples.json output.tsv.
