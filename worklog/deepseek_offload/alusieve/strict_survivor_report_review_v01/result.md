**Independent compact review — ALUSIEVE strict-survivor checkpoint**

**Scope limitation:** The report text and all seven TSV evidence files were not provided in the prompt and are not accessible in this environment. Consequently, I cannot verify any specific numeric calculation, threshold, or row-level agreement between the report and the tables. The review below is therefore limited to general scientific/audit requirements and to what can be said from the filenames alone.

**Actionable corrections**

1. **Provide the actual evidence or make the report self-contained.** The report cannot be independently reviewed from filenames alone. A reproducible audit needs the report text plus at least the decisions TSV and the exact-calls TSV included in the deliverable.

2. **Add a per-trio, per-site decision table.** For every candidate, the report should list: chromosome, position, ref/alt alleles, child genotype, mother genotype, father genotype, child alt depth, child total depth, child allele fraction, parent alt depths, mapping quality, strand bias, coverage in all three members, nearby alternate haplotypes, and the final classification. Without this mapping, "sequence-supported de novo" cannot be traced back to evidence.

3. **Define the exact threshold and falsification rule.** State explicitly what counts as "sequence-supported": e.g., child alt allele present at ≥20x depth and ≥25% allele fraction; both parents homozygous reference with zero alt-supporting reads at that site. Then state the falsification limit: any candidate with a non-zero parental alt read, low child depth, low allele fraction, poor mapping quality, or strand bias must be downgraded. If the report lacks this, it is under-specified.

4. **Reconcile all exact calls with the decisions TSV.** The `bcftools_independent_exact_calls_v01.tsv` and `strict_survivor_adjudication_decisions_v01.tsv` must have one row per candidate and identical variant coordinates. If any decision row lacks an exact-call row, the classification is unsupported. If any exact-call row is missing from decisions, the count is incomplete.

5. **Do not infer de novo status from absence alone.** The `trio_site_threshold_evidence_v01.tsv` should include the reference genotype in parents and the child’s allele balance at the candidate site. Absence of a row in a threshold table is not evidence; a true negative call must be explicitly present with sufficient depth.

6. **Check for hidden parental alt reads.** A common overclaim is calling a child de novo when one parent has 1–2 alt reads below a filter. The report should state the maximum allowed parental alt depth and confirm that no candidate violates it.

7. **Use haplotypes only as confirmation, not as the primary de novo criterion.** Nearby haplotype linkage can support shared inheritance, but it cannot establish that a child’s allele is absent in both parents. The exact parental genotype at the candidate site is the decisive evidence. If the report treats nearby phase as sufficient, that is an overclaim.

8. **Report coverage at the candidate site for all three samples.** The `trio_nearby_haplotype_coverage_v01.tsv` and `high_coverage_panel_nearby_phase_v01.tsv` suggest coverage and phase were evaluated, but the report should state the minimum site depth required in each of mother, father, and child. Without a declared minimum, a "strict survivor" label is not scientifically meaningful.

9. **Separate "sequence-supported" from "consistent with" or "cannot exclude".** Any candidate that has insufficient depth, missing parental coverage, or residual ambiguity must be labeled "not sequence-supported" or "unresolved," not grouped with confirmed de novo calls. If the summary counts all survivors as confirmed, that is an overclaim.

10. **Provide negative controls or validation metrics.** The report should state how many known inherited variants passed through the pipeline and whether any were incorrectly labeled de novo. Without this, the false-positive rate is unknown.

**Final verdict**

From the supplied materials, no `sequence-supported de novo` classification can be justified. The report and TSV contents were not made available for independent review. At minimum, the report must include explicit per-site evidence tables, declared thresholds, parental zero-alt-read requirements, and a falsification rule. Until those elements are present and visibly consistent with the TSVs, every "sequence-supported de novo" call must be treated as unverified.
