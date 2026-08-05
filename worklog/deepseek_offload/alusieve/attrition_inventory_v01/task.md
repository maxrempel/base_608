# Alusieve attrition evidence inventory v01

Last edited: 2026-08-02 by Codex (GPT-5.6 SOL)

## Role and boundary

Act as a read-only evidence analyst assisting Alusieve, the independent attrition auditor for Aluminum. Do not edit project files, run production, change thresholds, alter the frozen caller, rebuild Aluminum, or make biological claims. The scientific lead role must be named exactly `Aluminum Scientist`.

## Objective

Inspect the local Aluminum and ALU-DeNovo-1 project artifacts listed below and return a compact evidence inventory for a full filtering-attrition audit. Identify exactly what is already measurable, what raw or intermediate evidence is missing locally, and which existing scripts or prior control outputs can be reused without changing production.

## Governing plan

Read completely:

`C:\claude_base\projects\XG1\kenefick\paper_repro\deployment\aluya5_family_stream_v01\ALU_DE_NOVO_1_BASELINE_AND_ATTRITION_PLAN_v01.md`

## Evidence roots

- `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real\aluminum_atlas_v01`
- `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real\aluya5_exact_copy_npa_v01`
- `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts`
- Search narrowly under `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real` for earlier NPA spike-in, real-read, alignment, dropout, candidate, and threshold-calibration outputs.

## Questions

1. Map retained columns/files to every waterfall stage: annotated copies, accepted copies, callable positions, child-supported alleles, parent-observed alleles, parent-absent loose leads, strand survivors, and locus-review survivors.
2. Identify all files containing real candidate or near-miss reads, mates, local alignments, alternate mappings, clipping, starts, duplicates, parental allele counts, or locus-depth evidence.
3. Identify frozen threshold definitions and whether intermediate per-site values below each threshold were retained.
4. Identify prior computational spike-in truth and recovery outputs and state whether they exercised the complete frozen pipeline.
5. Identify reusable scripts for audit-only threshold grids, parental-dropout probabilities, repeat-mapping separation, and spike-in recovery.
6. List evidence gaps and the smallest read-only or audit-only next computation needed to close each gap.

## Output

Write only `result.md` in this run directory. Cite exact paths and line numbers or table columns where practical. Separate observed facts from inference. Keep the result under 2,500 words.
