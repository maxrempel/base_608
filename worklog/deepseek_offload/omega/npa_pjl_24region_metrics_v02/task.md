# Task

Return only one complete Python 3 program in a code fence, at most 320 lines.

Build a deterministic private genomic metrics tool:
`python program.py variants.tsv samples.json output.tsv`

`variants.tsv`: region_index, chrom, pos, ref, alt, region_id, region_start, region_end.
`samples.json`: list of sample_id, role, source_type, source_path, optional reference.
For source_type `cram`, source_path is one CRAM and query with `samtools view -h -T reference CRAM region`.
For `bam_dir`, source_path contains `alignment_extract_response_manifest_v01.tsv`; map its region column to its BAM column and query the matching BAM with `samtools view -h BAM region`.

Never print/store read names or SAM records. Consume subprocess output internally. Write aggregate rows only.

For each sample/region, report:
raw primary region records; usable records after excluding flag mask 1796; records with a CIGAR-aligned base at one-based pos; ref/alt/other counts; VAF; alt forward/reverse; distinct alt alignment starts; alt median MAPQ and base quality; max alt soft clip; read-group count, dominant RG fraction, stable `RG=count` summary; observed RG metadata summaries for library, platform unit, platform, and sample from @RG headers.

Strict pass is exactly: depth>=20, alt>=10, VAF in [0.25,0.75], alt both strands. Add no gates.

Parse CIGAR M,=,X,I,D,N,S,H,P correctly. Use only standard library. Fail closed on missing inputs, manifest mismatch, samtools error, duplicate variant key, or malformed input. Sort region_index then sample_id. Add SHA256 for every queried source and manifest, caching hashes. No read identifiers.
