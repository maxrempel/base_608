# PRELIMINARY Aluminum leave-one-family-out robustness v02

Date: 2026-07-30. Last edited: 2026-07-30 by Codex (GPT-5.6 SOL).

## Question and main result

This analysis asks whether two raw technical patterns in the sealed 12-family atlas survive removal of one family at a time. They do not provide biological validation.

**Main result:** PR26 drives the family-concentration pattern. The transition-versus-transversion effect remains positive after removing PR26, but its nominal exact-test evidence disappears. Neither pattern supplies a multiplicity-corrected biological signal.

## Exact robustness results

| Pattern | All 12 families | Remove most influential family | Safe interpretation |
|---|---:|---:|---|
| Family concentration | 4 of 10 survivors in PR26; SIR 4.96 (95% CI 1.51-9.15); global exact p=0.0362 | Remove PR26: 6 survivors across 11 families; global exact p=0.6118 | The raw concentration does not persist without PR26. |
| Transition passage | transitions 8/9 versus transversions 2/7; RR 3.11; risk difference 0.603; Fisher p=0.0350 | Remove PR26: transitions 4/5 versus transversions 2/7; RR 2.80; risk difference 0.514; Fisher p=0.2424 | Direction persists, exact evidence does not. |

SIR means standardized incidence ratio: observed PR26 survivors divided by the count expected from PR26's callable exposure. RR means risk ratio: transition passage fraction divided by transversion passage fraction.

## Influence and multiplicity

- The exact global family test is p=0.03617 before correction. The frozen enrichment multiplicity family contains eight estimable tests: four callable-background global tests and four conditional-feature global tests. Across those eight tests, the family result's Bonferroni adjusted value is 0.28934.
- The focal PR26-versus-exposure exact binomial p=0.00596 becomes 0.04767 under the same conservative eight-test correction. Because PR26 was selected from the observed concentration, this focal value is a post-selection sensitivity statistic, not confirmatory evidence.
- PR26 produces the largest loss of exact substitution evidence: Fisher p changes from 0.03497 to 0.24242 when PR26 is omitted.
- SH028 produces the largest attenuation of the substitution point estimate: RR falls from 3.11 to 2.22, while Fisher p=0.09491.
- Across all 12 substitution omissions, the smallest raw Fisher p is 0.01099 and its 12-fold Bonferroni value is 0.13187.

## Limits

These are 16 loose technical leads and 10 strand survivors. No biological validation was performed. The leave-one-family-out rows are sensitivity checks, not independent replications. No production was rerun, no candidate was relabeled, and no threshold, family, or callable denominator changed.

## Conclusion

PR26 concentration is family-specific and disappears when PR26 is removed. The transition passage advantage is directionally stable but inferentially fragile: after removing PR26, the effect remains RR 2.80, yet Fisher p=0.24242. Neither pattern survives a global multiplicity-aware interpretation, and neither is biological evidence.
