Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

# Independent review of ABO quantitative sensitivity v03

Review this bounded endpoint for arithmetic/statistical errors and overclaim.
Return ACCEPT or REJECT with only necessary corrections.

Design:
- Two focal sets: broad callable A=3,O=1,n=4; strict excluding one
  tag/deletion-discordant A call: A=2,O=1,n=3.
- Same-classifier 1000 Genomes Phase 3 Omni callable controls:
  A=475,B=299,AB=86,O=695,n=1,555.
- Six control views: overall plus AFR, AMR, EAS, EUR, SAS.
- Two binary outcomes: A versus non-A and O versus non-O.
- 24 exploratory rows total.
- Each row reports focal and control proportions, exact Clopper-Pearson
  proportion intervals, descriptive risk ratio and risk difference,
  conditional maximum-likelihood odds ratio with exact conditional 95%
  interval, and two-sided Fisher exact P.
- Focal ancestry is unknown; consumer arrays are not exact Omni matches.
- Control attrition is reported and ancestry-uneven: global 138/1,693
  unresolved, AFR 109/339 unresolved.
- No multiple-testing or enrichment claim is made.
- RhD is not revisited.

Key overall results:
- Broad A: risk ratio 2.4553; conditional odds ratio 6.8119, exact 95% interval
  0.5454 to 358.4086; Fisher P=0.08851.
- Strict A: risk ratio 2.1825; conditional odds ratio 4.5424, exact 95% interval
  0.2359 to 268.5235; Fisher P=0.22365.
- Broad O: risk ratio 0.5594; conditional odds ratio 0.4127, exact 95% interval
  0.00785 to 5.1525; Fisher P=0.63310.
- Strict O: risk ratio 0.7458; conditional odds ratio 0.6189, exact 95% interval
  0.01047 to 11.9111; Fisher P=1.0.

Proposed conclusion:
No stable unusual ABO pattern is established. The effect estimates are
compatible with very wide ranges; isolated nominal P values in unmatched
superpopulation sensitivities are not evidence of enrichment.
