# XG1 participant-variant evidence extraction v01

Last edited: 2026-08-02 by Codex (GPT-5.6 SOL)

## Role

Act as a private scientific evidence extractor. Do not contact anyone and do not
copy interview, biography, medical-profile, or correspondence details. Use only
project labels and the minimum participant names needed to distinguish the two
requested analyses.

## Objective

Read the current local evidence for Kristen and Vittorio participant-specific
variant analyses. Return a compact evidence matrix for:

1. Kristen insertion detection;
2. Kristen maternal point substitutions / maternal phasing;
3. Kristen microchimerism;
4. Kristen structural-variant and inversion work;
5. Kristen OMEGA / Omun characterization;
6. Vittorio relationship validation;
7. Vittorio structural rarity, deletions, and insertions;
8. Vittorio OMEGA-type out-of-place insertion analysis.

For every analysis extract:

- exact hypothesis;
- exact input data and controls;
- candidate counts and attrition stages;
- strongest surviving locus or candidate, using genomic coordinates only when
  they are already in a scientific result file;
- strongest rejected locus or candidate and why it failed;
- real-read or alignment validation status;
- main alternative explanations;
- whether the conclusion is biological absence, evidence against the claim,
  insufficient power, or method limitation;
- concrete next falsification test.

Flag contradictions between older and newer reports. Prefer the newest
checksum-backed or technical report over drafts and letters. Do not treat an
email draft as scientific evidence.

## Starting paths

Kristen project root:

`C:\claude_base\projects\XG1\kenefick`

Prioritize these files and their directly linked scientific sources:

- `kristen_claim_checks_20260713_v01_tomemex.md`
- `kristen_control_table_20260713_v01_tomemex.md`
- `kristen_insertion_report_v01_tomemex.md`
- `kristen_insertion_detection_report_v01_tomemex.md`
- `kristen_microchimerism_report_v01_tomemex.md`
- `analysis\kristen_microchimerism_courtgrade_v04.txt`
- `analysis\kristen_femaleY_mismap_mechanism_X1D_20260705_v01_tomemex.md`
- `analysis\maternal_hap_candidates_MAF_gate_X1D_20260705_v02_tomemex.md`
- `omega_detector\SNV_MATERNAL_PHASING_PILOT_v01_tomemex.md`
- `omega_detector\INSERT_MATERNAL_PHASING_RESULTS_v01_tomemex.md`
- `omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md`
- `letters\kristen_maternal_point_substitutions_technical_report_v01.md`
- the latest relevant `letters\kristen_email_*_technical_report_v01.md` files,
  but only as leads to scientific evidence;
- `omega_detector\README.md` and the latest project, naming, and terminology
  indexes under `omega_detector\starseed_taygeta\indexes`.

Vittorio project root:

`C:\claude_base\projects\XG1\vittorio`

Prioritize:

- `VITTORIO_PIANTEDOSI_STATUS_v01_tomemex.md`
- `VITTORIO_RARITY_PILOT_chr22_v01_tomemex.md`
- `VITTORIO_RARITY_RESULTS_v01_tomemex.md`
- all scientific Markdown and TSV files under `report` and `catalogs`;
- scripts only when needed to understand filters or attrition.

## Output

Write only `result.md`. Begin with a one-paragraph executive summary, then an
evidence table, contradictions, decisive surviving/rejected loci, and missing
evidence. Cite every claim with an exact local path and line number when
possible. Do not generate a user-facing report and do not edit project files.
