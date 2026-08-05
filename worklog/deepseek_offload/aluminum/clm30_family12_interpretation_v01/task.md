# Aluminum CLM30 family-12 interpretation

Last edited: 2026-07-30 by Codex (GPT-5.6 SOL)

Draft a compact scientific interpretation of this deterministic atlas update.
Do not propose new computation. Do not claim biological absence or validated
de novo mutations. Distinguish screening evidence, exposure-weighted family
concentration, global multiplicity control, post-selected focal sensitivity,
and leave-one-family-out robustness.

Old sealed checkpoint:
- 11 complete families, 242 autosomes.
- Primary callable positions 8,630,460; strict callable 2,996,136.
- 16 primary loose occurrences; 10 primary strand survivors; 1 independently
  computed strict occurrence.
- Family exposure-weighted Monte Carlo p 0.497885.
- Exact global family concentration p 0.051648; 8-test Bonferroni 0.413187.
- PR26 focal exact binomial p 0.008213; 8-test value 0.065707.
- PR26 SIR 4.5366.
- Omitting PR26: global exact p 0.724057.

New checksum-sealed checkpoint after CLM30:
- 12 complete families, 264 autosomes.
- CLM30 adds 810,929 primary-callable and 307,583 strict-callable positions,
  with 0 primary leads, 0 primary strand survivors, and 0 strict candidates.
- Aggregate primary callable 9,441,389; strict callable 3,303,719.
- Candidate counts remain 16, 10, and 1; exact recurrence remains zero.
- Family exposure-weighted Monte Carlo p 0.421076.
- Exact global family concentration p 0.036168; 8-test Bonferroni 0.289341.
- PR26 focal exact binomial p 0.005959; nominal 8-test value 0.047671.
- PR26 SIR 4.9629.
- Omitting PR26: global exact p 0.611761.
- Minimum family-omission global p 0.019035; 12-omission Bonferroni 0.228424.
- Transition passage results do not change because CLM30 contributes no leads:
  8/9 versus 2/7, RR 3.111, Fisher p 0.034965; removing PR26 gives 4/5
  versus 2/7, RR 2.80, Fisher p 0.242424.

Key review issue: PR26 was identified from the same observed family
concentration, so its focal binomial statistic is post-selected. State whether
the 0.047671 sensitivity value can be called confirmatory given that the
pre-specified global family test remains non-significant after correction.

Return:
1. three short result bullets;
2. one plain-language conclusion;
3. two cautions.
