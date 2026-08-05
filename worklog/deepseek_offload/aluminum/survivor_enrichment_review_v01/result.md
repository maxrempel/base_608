## Compact Pitfall Checklist

### Statistical Pitfalls

1. **Small total survivor count**  
   - Primary analyses likely use 10 survivors (or 16? ambiguity). With 242 cells, expected counts are nearly all <0.1, invalidating asymptotic chi-square. Monte Carlo multinomial test is appropriate but has extremely low power.  
   - *Correction*: Report exact P-value with confidence interval from simulation (already done). Acknowledge power limitation explicitly.

2. **Exact binomial interval for SIR**  
   - “Exact binomial 95% interval divided by exposure share” is ambiguous: computing binomial CI for count and dividing by expected proportion ignores the multinomial conditioning on total survivors. That yields overly narrow intervals.  
   - *Correction*: Use exact Poisson (Byar) or exact conditional binomial interval given the fixed total (i.e., Clopper–Pearson on the proportion of total survivors in the cell, then convert to SIR). Ensure denominator is the expected count (exposure share × total survivors). Document the exact formula.

3. **Haldane‑Anscombe correction in risk ratios**  
   - Adding 0.5 to every cell in every 2×2 table biases estimates away from zero even when no zero cells exist. The correction should be applied *only* when a zero cell occurs.  
   - *Correction*: Specify “Haldane‑Anscombe correction (add 0.5 to all four cells) when any cell is zero; otherwise use uncorrected Woolf log‑risk ratio.”  
   - Log‑Wald intervals with correction are anti‑conservative for very small counts; consider reporting exact unconditional intervals (e.g., Agresti‑Coul) as sensitivity.

4. **Multiple testing without adjustment**  
   - Two partitions (with three bins each) plus multiple conditional tests (strand, identity, coverage, Ti/Tv, direction, base) = many comparisons. No multiplicity correction is mentioned.  
   - *Correction*: State that all enrichment tests are exploratory; adjust P‑values via Bonferroni or false discovery rate if any formal claim is made. Provide raw P‑values and note the number of tests.

5. **Non‑exhaustive or overlapping categories in conditional tests**  
   - “Repeat strand; alignment identity bins …; coverage bins …” – these may overlap or not be mutually exclusive with the “Alu‑oriented candidate base”. Ensure each predictor is tested independently (separate models) to avoid double‑counting.  
   - *Correction*: Clarify that each predictor is tested in its own 2×K table; category‑versus‑remainder risk ratios are for individual categories only.

6. **Zero counts in sparse tables**  
   - With 16 observations, many categories (e.g., identity 0.82‑<0.90) may have zero survivors. Fisher exact test (or Monte Carlo) is valid, but the log‑Wald risk ratio interval becomes infinite or undefined.  
   - *Correction*: For empty categories, report “no survivors” and do not compute risk ratio; report exact Fisher P‑value only. If Haldane‑Anscombe is used, the interval will be finite but must be flagged as unreliable.

### Reproducibility Pitfalls

7. **Fixed seed not documented**  
   - “Fixed‑seed 1,000,000‑draw” is mentioned but the seed value is not given. Without the seed, the multinomial P‑value cannot be reproduced exactly.  
   - *Correction*: Record and report the seed (e.g., `set.seed(42)`) in the analysis script. Also store the RNG state.

8. **Ambiguity in survivor set for primary analyses**  
   - The input lists 16 loose candidates, 10 pass strand rule, and 1 strict survivor. It is unclear whether the primary enrichment analyses use the 10 passing survivors or all 16.  
   - *Correction*: Explicitly state: “Primary enrichment analyses are performed on the 10 survivors that passed the unchanged strand rule. Conditional tests (outcome = passage) use all 16 loose candidates.”

9. **Partition bin definitions are “frozen” but not explicitly justified**  
   - The cutpoints for primary callable/mapped (<0.60, 0.60‑<0.80, ≥0.80) and strict/primary (<0.25, 0.25‑<0.40, ≥0.40) are arbitrary. If these were chosen after seeing the data, that is a pitfall.  
   - *Correction*: Confirm that these bins were pre‑registered or justified by biological thresholds. If not, state they are data‑driven exploratory.

### Interpretation Pitfalls

10. **Conflating technical survivors with true de novo mutations**  
    - The strict survivor is “descriptive only” and the atlas lacks repeat labels for all callable positions. Any statement implying that observed enrichment reflects biological mutation mechanisms (e.g., “Alu‑oriented” implying mutational hotspot) is invalid without proper background.  
    - *Correction*: Use terminology like “technical survivors” or “candidate alignments.” Never call them “de novo mutations.” Clearly state that repeat/sequence enrichment cannot be estimated.

11. **Over‑interpreting conditional tests from 16 observations**  
    - Small sample size → wide confidence intervals and low power. A non‑significant Fisher test does not rule out an effect; a significant result may be due to one or two outliers.  
    - *Correction*: Emphasize that all conditional analyses are descriptive hypothesis‑generating. Provide exact counts for each category. Avoid causal language.

12. **Missing background implies zero background**  
    - The text explicitly warns: “Missing background must not be approximated or called zero.” This applies to any attempt to compute repeat enrichment outside the
