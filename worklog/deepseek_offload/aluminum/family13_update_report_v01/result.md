# PRELIMINARY Update 2026-07-31: Aluminum Cumulative ALU-DeNovo-1 Atlas Adds SH056 as Family 13

## Question and main result

Did adding SH056 as family 13 improve the sealed candidate atlas? The atlas now contains 13 complete families, 286 family-autosome cells, 20 retained candidate-table occurrences, 10,237,494 primary callable positions, and 3,586,389 strict callable positions. However, all three retained pre-strand rows added by SH056 failed the frozen strand-balance gate. Therefore SH056 added zero primary strand survivors, zero strict strand survivors, and zero biologically validated calls.

## Before and after

| Metric | Previous sealed atlas | New sealed candidate atlas |
|---|---:|---:|
| Complete families | 12 | 13 |
| Family-autosome cells | 264 | 286 |
| Retained candidate-table occurrences | 17 | 20 |
| Primary callable positions | 9,441,389 | 10,237,494 |
| Strict callable positions | 3,303,719 | 3,586,389 |
| Primary strand survivors | 10 | 10 |
| Strict strand survivors | 1 | 1 |
| Exact cross-family recurrence keys | 0 | 0 |
| Validated biological mutations claimed | 0 | 0 |

## SH056 technical validation

The SH056 input handoff v02 passed 200 of 200 checksum entries. The manifest digest was ccd6e5111eec18b2094a3b551b72958bcc2236f03f09ad3eee92890661822a6a. Production reconciled 22 of 22 autosomes with a clean exit and no restart, out-of-memory event, or swap.

SH056 added 3 retained pre-strand technical rows: two primary-tier rows and one strict-tier row. All three failed the frozen strand-balance gate. As a result, SH056 contributed zero primary strand survivors, zero strict strand survivors, and zero biologically validated calls.

For the two primary rows, explicit alternate support was zero in both parents. For the strict pre-strand row, exact parental counts were not available in the coordinate-free audit. That row must be reported as parental evidence not assessed, not as parent absent.

## Robustness and hotspot results

Exposure-weighted Monte Carlo hotspot tests with 100,000 draws gave chromosome p = 0.3483165 and family p = 0.5054149. There is no hotspot evidence.

Leave-one-family-out analysis showed that PR26 still accounts for 4 of the 10 primary strand survivors. The global exact family concentration p value is 0.0260592, with a frozen 8-test Bonferroni enrichment family value of 0.208474. Omitting PR26 leaves 6 survivors across 12 families and the global p value becomes 0.549165. The concentration is therefore PR26-driven and not robust.

For transition versus transversion passage, the current observation is 8 of 9 transitions versus 2 of 9 transversions, risk ratio 4.0, Fisher p = 0.0152201, and frozen 8-test Bonferroni = 0.121761. Omitting PR26 gives 4 of 5 transitions versus 2 of 9 transversions, risk ratio 3.6, Fisher p = 0.0909091. The direction remains the same, but the exact evidence is not robust.

## Safe conclusion and limits

No scientific gates changed. No production rerun was performed. Missingness remains missing. Validated biological mutations claimed: 0.

The technical validation of SH056 is clean, but technical success alone does not establish biological calls. The new pre-strand screening rows are separated from strand survivors and biological validation, and none of them survived the strand-balance gate. The strict pre-strand row has unassessed parental evidence. Hotspot and enrichment findings remain non-robust and sensitive to PR26. All counts above are aggregate atlas facts only; no coordinates, read identifiers, biological interpretation, or methods beyond those stated are added here.
