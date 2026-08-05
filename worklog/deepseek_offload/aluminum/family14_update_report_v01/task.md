Draft a concise scientific report for the Aluminum ALU-DeNovo-1 cumulative atlas update from 13 to 14 complete families. Use only the aggregate facts below. Do not invent coordinates, genes, participant traits, mechanisms, or biological claims. Use plain English, lead with the scientific question and result, label the report PRELIMINARY dated 2026-08-01, and explicitly distinguish technical screen evidence from biological de novo evidence.

Frozen method and verification:
- The production gate was unchanged. Family 1377 completed all 22 autosomes once. Its handoff manifest SHA256 is 639565e455ffaf264918812ffffd871d40bb3c95900daada4e6a404bd7d96652; all 200 entries and per-chromosome checksums passed.
- Candidate-table duplicate check passed: 5 unique primary rows and 1 unique strict row. One strict row is the same biological candidate as one primary row, so cross-tier overlap is 1 and is not a duplicate conflict.
- All 6 tier rows had zero parent alternate reads under this bounded screen. This does not exclude parental mosaicism or prove germline de novo status.
- Family 1377: 3,419 accepted AluYa5 elements; 806,076 primary callable positions; 2,799 primary child-supported positions; 2,794 seen in a parent; 5 primary parent-absent pre-strand rows; 4 primary strand survivors. Strict: 290,066 callable; 971 child-supported; 970 seen in parent; 1 pre-strand and 1 strand survivor. The one primary failure had reverse-only support and failed strand balance.

Cumulative 14-family atlas:
- 14 complete families, 308 autosome-family cells, 23 primary parent-absent loose leads, 14 primary strand survivors, 3 strict occurrences.
- Exact cross-family candidate recurrence is zero. Chromosome hotspot Monte Carlo p=0.6336736633. Family hotspot Monte Carlo p=0.2780972190. No multiplicity-corrected hotspot signal.
- Family concentration exact multinomial p=0.01526576, frozen-eight Bonferroni p=0.12212608. PR26 has 4/14 survivors and drives the raw concentration; omit PR26 gives global p=0.06346489.
- Transition-versus-transversion strand passage: transitions 11/12 versus transversions 3/11; risk ratio 3.36111111; Fisher exact p=0.00275946; frozen-eight Bonferroni p=0.02207568.
- Leave one family out: the direction and nominal p<=0.05 persist for every omission; worst Fisher p=0.01976661. However, worst p times eight is 0.15813288, so the corrected association does not persist under the least favorable omission. This is a technical strand-passage association, not evidence of biological mutation enrichment.
- Biology validation remains NO. Missingness remains missing; zero screening candidates is not biological absence.

Write roughly 600-900 words in Markdown with: TLDR; question; what family 1377 added; cumulative findings; robustness; safe conclusion; next bounded step. The next bounded step is independent real-read/parental validation of the technical survivors and continued one-family-at-a-time production, not a gate change.
