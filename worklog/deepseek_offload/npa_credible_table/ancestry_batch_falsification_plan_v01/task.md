# Task: compact sealed plan for NPA ancestry/batch falsification

Privacy: private-authorized. Max explicitly authorizes participant scientific data for this private project. Do not include credentials, API keys, tokens, passwords, Bitwarden material, or unrelated secrets.

Do not open, infer, request, or discuss phenotype/autism values.

## Context

Project: NPA credible-table branch for three complete 1000 Genomes trios.

Frozen NPA filter: `npa_clean_germline_strict_v03_phase0_locked_2026-07-21`.

Current locked primary burden after real-read review:

| child | family | population | superpopulation | sex code | primary event burden | queue rows |
|---|---|---|---|---:|---:|---:|
| HG01087 | PR26 | PUR | AMR | 2 | 0 | 1770 |
| HG02280 | BB23 | ACB | AFR | 2 | 0 | 1831 |
| HG02683 | PK16 | PJL | SAS | 2 | 11 | 1211 |

Interpretation so far:

- The 11 included rows are provisional technical local NPA events, not confirmed biological de novo mutations.
- HG02683 has the fewest sampled queue rows but all 11 events.
- Sex does not explain the concentration because all three children have sex code 2.
- Ancestry/superpopulation is a serious confounder because the only burden-positive child is also the only SAS/PJL child.
- Broad run pattern: children are ERR398-series public CRAMs and parents are ERR324-series public CRAMs. Exact read-group/library/flowcell/lane batch is not yet recovered.
- Source material is high-coverage 1000 Genomes lymphoblastoid cell-line DNA. Per-sample cell-line history is not recovered.
- Contamination or sample-mixture estimates are not recovered.
- True callable-base or callable-site denominators are not recovered; only queue rows and technical strata exist so far.
- Phenotype/autism gate is fail-closed until non-phenotype confounders and analysis contract pass.

## Requested output

Draft a compact, phenotype-sealed plan to distinguish ancestry/batch artifact from a real NPA burden signal given 0/0/11 across AMR/AFR/SAS.

Specify:

1. the smallest ancestry-matched controls;
2. callable-opportunity normalization;
3. contamination and batch checks;
4. exact falsification criteria;
5. what result would reopen the autism gate;
6. what result would permanently close the autism gate for this 3-child dataset.

Keep it short and operational. Assume Codex will verify factual assumptions against local files before any action. Do not propose opening phenotype yet. Do not propose large compute as the immediate next step; start with bounded checks and the smallest useful controls.

