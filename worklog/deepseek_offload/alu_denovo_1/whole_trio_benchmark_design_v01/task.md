# ALU-DeNovo-1 whole-trio benchmark design review

Design a concise, fail-closed benchmark harness for an existing genomic
analysis. Return only a compact implementation specification and a checklist;
do not invent biological conclusions.

Known facts:

- A frozen method analyzes one chromosome twice: primary MAPQ 30/baseQ 25,
  then strict MAPQ 60/baseQ 30. It repeatedly performs one pileup per accepted
  AluYa5 element.
- A candidate optimized method performs one chromosome-wide native pileup per
  sample per quality tier, then reuses that tier's evidence across all accepted
  AluYa5 copies.
- On a completed chromosome containing the only strict candidate, the optimized
  method now matches every frozen summary value, TSV field, row, and candidate.
- A single lower-threshold pileup cannot be reused for the strict tier because
  native paired-read overlap handling changes effective base qualities at the
  two gates. The safe optimization therefore uses two native chromosome-wide
  passes, one per unchanged tier.
- The same trio has frozen results and retained target CRAM subsets for all 22
  autosomes.
- A comparator already checks primary and strict summary JSON plus exact TSV
  fields and rows, failing nonzero on any difference.

Requirements:

1. Benchmark all 22 autosomes without changing scientific thresholds.
2. Preserve frozen outputs and existing production.
3. For each chromosome, run the optimized method into a new benchmark folder,
   compare both tiers exactly, and stop immediately on any difference.
4. Record per-chromosome wall time, CPU time if practical, candidate counts, and
   comparison status.
5. Record aggregate optimized runtime.
6. Obtain a fair frozen-method runtime estimate. Recommend whether to rerun the
   entire frozen trio or use a clearly labeled measured subset/extrapolation;
   prioritize a defensible measured result.
7. Keep Asto modest: 2 CPU cores, 6 GiB memory, low priority, one chromosome at
   a time.
8. Make every chromosome independently resumable and preserve atomic results.
9. Identify validity hazards, especially cache effects, CRAM reader state,
   missing annotation files, stale output markers, and candidate-free
   chromosomes.

Return:

- recommended harness structure;
- exact pass/fail conditions;
- runtime-comparison design;
- the smallest set of retained aggregate files;
- critical review of whether one chromosome exact equivalence is enough to
  justify the whole-trio benchmark (not production switch).
