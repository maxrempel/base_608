# Aluminum recurrence, hotspot, and attrition — PRELIMINARY

Build date in Los Angeles: 2026-07-30

## Scientific question and main result

Among 12 complete public parent-child trios, do the frozen
ALU-DeNovo-1 screening candidates recur at the same exact allele and locus, or
cluster on particular chromosomes beyond what callable sequence would predict?

**No exact candidate recurred in more than one family, and the observed
chromosome concentration is compatible with callable exposure.** The largest
primary-tier count was four on one chromosome; a fixed-count Monte Carlo check
gave P = 0.2421 for a maximum at least this large under exposure-
weighted allocation. This is no evidence for a population hotspot.

## What was analyzed

- Complete families: 12
- Accepted autosomes: 264
- Annotated AluYa5 copies: 43,932
- Alignment-accepted copies: 41,028
  (93.39%)
- Primary callable positions: 9,441,389
- Strict mapping-quality-60 callable positions:
  3,303,719
  (34.99%
  of primary callable positions)

## Candidate attrition

At the primary tier, 35,876
child-supported alleles were screened. Both parents accounted for
35,860; 16
parent-absent loose leads remained, and 10
survived the primary strand rule.

The strict tier was computed independently. It retained
12,315 child-supported alleles; all but
one were observed in a parent. One strict screening survivor remains. It is
not a validated biological mutation.

## Recurrence and concentration

- Exact allele-at-locus keys recurring across families: 0
- Primary loose occurrences: 16
- Separately computed strict occurrences: 1
- Chromosomes with the largest raw primary counts: chr1 (4), chr5 (3), chr2 (3)
- Families with zero primary loose leads: 4 of
  12
- Largest primary count in one family: 4
- Exposure-weighted family concentration check: P = 0.4211

Rates based on one event can look large when the callable denominator is small.
Therefore the chromosome table is descriptive; it does not establish a
hotspot. Population, platform, library, and batch structure are not adjusted
at this sample size.

## Safe conclusion

The current data show strong technical attrition and no reproducible
cross-family locus. The most useful next step is sequential monitoring as each
checksum-backed family arrives: retain the frozen exact recurrence test, update
exposure-normalized chromosome counts, and prioritize any future exact
cross-family recurrence or independently replicated strict survivor for
real-read and parental-dropout review. Do not change gates in response to these
outcomes.
