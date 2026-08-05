# PRELIMINARY

**Date:** 2026-08-01  
**Update:** Aluminum ALU-DeNovo-1 cumulative atlas, families 13 → 14  

## TLDR

The cumulative atlas grew from 13 to 14 complete families with the addition of Family 1377 under the unchanged production gate. Family 1377 contributed 4 primary and 1 strict strand-surviving candidate row, bringing the atlas to 23 primary parent-absent loose leads, 14 primary strand survivors, and 3 strict occurrences across 308 autosome-family cells. No biological de novo calls are made. The screen-level strand-passage association for transitions versus transversions remains significant in a single frozen test, but the leave-one-family-out corrected analysis does not persist under the least favorable omission. Hotspot and recurrence signals remain absent. Biology validation status remains NO.

## Question

Does adding one completed family to the cumulative AluYa5 atlas change the screen-level evidence for candidate de novo Alu insertions, and does any signal survive the same frozen verification and multiplicity controls?

## What Family 1377 Added

Family 1377 completed all 22 autosomes once. The handoff manifest SHA256 is `639565e455ffaf264918812ffffd871d40bb3c95900daada4e6a404bd7d96652`; all 200 entries and per-chromosome checksums passed. The candidate-table duplicate check passed: 5 unique primary rows and 1 unique strict row. One strict row is the same biological candidate as one primary row, so cross-tier overlap is 1 and is not a duplicate conflict. All 6 tier rows had zero parent alternate reads under this bounded screen; this does not exclude parental mosaicism and does not prove germline de novo status.

Family 1377 screen counts: 3,419 accepted AluYa5 elements; 806,076 primary callable positions; 2,799 primary child-supported positions; 2,794 seen in a parent; 5 primary parent-absent pre-strand rows; 4 primary strand survivors. Strict tier: 290,066 callable; 971 child-supported; 970 seen in parent; 1 pre-strand and 1 strand survivor. The one primary failure had reverse-only support and failed strand balance.

## Cumulative Findings

The atlas now contains 14 complete families, 308 autosome-family cells, 23 primary parent-absent loose leads, 14 primary strand survivors, and 3 strict occurrences. Exact cross-family candidate recurrence is zero. Chromosome hotspot Monte Carlo p = 0.6336736633; family hotspot Monte Carlo p = 0.2780972190. No multiplicity-corrected hotspot signal is present.

Family concentration exact multinomial p = 0.01526576; frozen-eight Bonferroni p = 0.12212608. PR26 has 4/14 survivors and drives the raw concentration; omitting PR26 gives global p = 0.06346489.

Transition-versus-transversion strand passage: transitions 11/12 versus transversions 3/11; risk ratio = 3.36111111; Fisher exact p = 0.00275946; frozen-eight Bonferroni p = 0.02207568. Leave-one-family-out: the direction and nominal p ≤ 0.05 persist for every omission; worst Fisher p = 0.01976661. However, worst p times eight is 0.15813288, so the corrected association does not persist under the least favorable omission. This is a technical strand-passage association, not evidence of biological mutation enrichment.

## Robustness

The production gate was unchanged. All frozen checks passed for Family 1377. The screen distinguishes technical evidence from biological de novo evidence. Zero parent alternate reads in a bounded screen is only technical absence; it is not proof of germline origin. Recurrence remains zero, and hotspot p-values are consistent with null expectation. The strand-passage association is reproducible in direction across all leave-one-family-out subsets at the nominal level, but the corrected least-favorable result fails. Therefore, the association is not robust enough to support a biological claim. Family concentration is also not robust to the frozen-eight correction and is driven by one family.

## Safe Conclusion

The 13-to-14 update is internally consistent under the frozen method. Family 1377 added candidates without introducing duplicate conflicts, parent-read matches, or recurrence. The cumulative atlas has no cross-family recurrence and no hotspot signal. The transition-versus-transversion strand passage remains a screen-level technical observation with nominal support, but its corrected least-favorable-omission p-value is 0.15813288, meaning the signal can be weakened by removing one family and multiplying by the frozen-eight multiple-testing factor. Biology validation remains NO. Missingness remains missing; zero screening candidates is not biological absence.

## Next Bounded Step

The next bounded step is independent real-read/parental validation of the technical survivors and continued one-family-at-a-time production. This is not a gate change.
