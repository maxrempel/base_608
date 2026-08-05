Audit this truth-blind six-sample synthetic RHD caller plan. Return at most 8 bullets and 600 words. Name only concrete defects that could invalidate the pilot, plus minimal fixes.

Facts:
- Input manifest has exactly six opaque BAM/BAI pairs, verified by bytes and SHA256, and rejects columns named state/truth/seed/hap1/hap2/rhd_copy_count.
- `samtools depth -aa -d 0 -q 0 -Q MAPQ -r REGION BAM` runs at MAPQ 0 and 20. It requires one row per inclusive base.
- hg38 ranges: RHD chr1:25272509-25330445; RHCE chr1:25362249-25420825; flanks chr1:25230000-25250000 and chr1:25440000-25460000.
- Baseline is unweighted mean of RHCE and both flank mean depths. RHD/baseline ratio calls >=0.75 two-copy, >=0.25 one-copy, else zero-copy.
- RHtyper 1.1 command: `RHtyper -bam BAM -gene RHD -ref GRCh38DH.fa -gbuild hg38 -pre PREFIX -call -cov 30 -altN 3 -v 0`; logs and exit captured.
- Delly 1.2.6 command: `delly call -g GRCh38DH.fa -o SAMPLE.bcf BAM`; on success, bcftools queries CHROM/POS/END/SVTYPE/FILTER. Logs and exits captured.
- Every output is hashed into per-sample and overall immutable markers. Tool success counts are separate. Truth remains sealed.
- Required later scoring: depth copy state, RHtyper state, and exact Delly breakpoint scored separately; directional depth 2>1>0; no sham false deletion; Delly homology failure is missingness.

Answer these only: Are samtools options/denominators correct? Are depth normalization thresholds adequate for a synthetic 30x pilot? Is any caller invocation/output/failure behavior silently unsafe? What exact pre-unblinding check is missing?
