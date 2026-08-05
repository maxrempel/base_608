Review the following truth-blind Python caller design for a six-dataset synthetic RHD structural-variant pilot. Identify only concrete correctness, reproducibility, or scientific-scoring defects that could invalidate the pilot. Keep the response under 1,500 words. Do not propose participant interpretation.

Requirements:
- Truth labels and seeds remain unavailable during caller execution.
- Score normalized RHD depth separately from RHtyper and exact Delly breakpoints.
- Depth uses exact hg38 RHtyper ranges: RHD chr1:25272509-25330445, RHCE chr1:25362249-25420825, plus chr1:25230000-25250000 and chr1:25440000-25460000 flanks.
- Directional ordering after unblinding must be 2-copy > 1-copy > 0-copy.
- Matched shams must produce no false deletions.
- Delly failure in homologous Rhesus boxes is technical missingness, never absence.
- Tool failures must remain visible and must not silently change genotype calls.

Implementation summary:
1. Verify a six-row mapped-manifest checksum and every BAM/BAI size and SHA256; reject truth/state/seed/copy fields.
2. For MAPQ thresholds 0 and 20, run `samtools depth -aa -d 0 -q 0 -Q MAPQ -r REGION BAM` across RHD, RHCE, and both flanks. Require exactly the inclusive region length in output. Define baseline as the unweighted mean of the three region mean depths. Define normalized ratio RHD/baseline. Blind copy call: >=0.75 two-copy, >=0.25 one-copy, otherwise zero-copy.
3. Run RHtyper 1.1 with `-bam BAM -gene RHD -ref GRCh38DH.fa -gbuild hg38 -pre PREFIX -call -cov 30 -altN 3 -v 0`; capture stdout/stderr and exit.
4. Run Delly 1.2.6 with `call -g GRCh38DH.fa -o SAMPLE.bcf BAM`; if exit 0 and BCF exists, run bcftools query for CHROM, POS, END, SVTYPE, FILTER. Capture all exits.
5. Hash every output; create one per-sample immutable completion marker and one overall marker. Overall marker reports depth, RHtyper and Delly success counts separately and states truth_unblinded=false, participant_input_read=false, Delly scoring separate.

Questions:
- Are samtools depth options and inclusive denominator correct?
- Is the baseline/threshold logic adequate for this blinded pilot?
- Could RHtyper or Delly invocation, output handling, or partial-failure semantics silently invalidate results?
- What minimal pre-unblinding checks must be added, if any?

Return a prioritized review with exact suggested changes only where necessary.
