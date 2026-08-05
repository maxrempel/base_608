# Aluminum survivor-enrichment implementation review

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Review this fixed statistical implementation for pitfalls. Do not invent data
or change categories.

Inputs are a checksum-sealed atlas with 11 complete families, 242
family-by-chromosome cells, 16 primary parent-absent loose candidate rows, 10
of which pass the unchanged strand rule, and one independently computed strict
mapping-quality-60 survivor.

Frozen primary analyses:

- Family and chromosome concentration, expected probabilities proportional to
  primary callable positions.
- Two three-level cell partitions, with candidate exposure weighted by primary
  callable positions:
  - primary callable / mapped: <0.60, 0.60-<0.80, >=0.80;
  - strict callable / primary callable: <0.25, 0.25-<0.40, >=0.40.
- Report observed, expected, standardized incidence ratio, exact binomial 95%
  interval divided by exposure share, and a fixed-seed 1,000,000-draw
  multinomial Pearson goodness-of-fit P value.

Frozen conditional tests among the 16 loose leads:

- Outcome is passage of the primary strand rule.
- Repeat strand; alignment identity bins 0.82-<0.90, 0.90-<0.97, >=0.97;
  coverage bins 0.75-<0.85, 0.85-<0.95, >=0.95.
- Transition/transversion; direction; Alu-oriented candidate base.
- Report category counts, survival proportion, category-versus-remainder risk
  ratio with Haldane-Anscombe correction when needed, log-Wald 95% interval,
  and Fisher exact for binary or 1,000,000-draw fixed-margin
  Fisher-Freeman-Halton-style Pearson P for larger tables.

The strict survivor is descriptive only. Full repeat/sequence enrichment
against callable bases is not estimable because the sealed atlas does not
retain those labels for every callable position. Missing background must not be
approximated or called zero.

Return a compact checklist of statistical, reproducibility, and interpretation
pitfalls plus any precise corrections needed. Never call technical survivors
biological de novo mutations.
