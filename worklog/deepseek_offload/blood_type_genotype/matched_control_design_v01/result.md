## Compact Technical Recommendation

**Control Set Construction**  
- Use **1000 Genomes Phase 3 (2,504 individuals)** restricted to the **exact bi-allelic markers** observed in the local ABO/RHD panel (e.g., rs590787, known ABO coding SNPs).  
- **Defensible because**: direct marker match avoids imputation error; 1000 Genomes is a validated, widely-used reference with high call rates for common SNPs.  
- **Ancestry matching is not possible** without participant ancestry. Instead, report frequencies **separately for each 1000 Genomes superpopulation** (AFR, AMR, EAS, EUR, SAS) alongside the global frequency. This becomes a sensitivity analysis, not a matched control.  

**1000 Genomes Acceptability**  
- Acceptable **only** for markers present in both datasets (no imputation of untyped markers, no tag translation).  
- Ancestry handling: do not assign focal samples to any population. Present control frequencies stratified by superpopulation; note that any deviation may reflect latent ancestry differences.  

**Valid Statistical Endpoint (n=5 focal, with one related pair)**  
- **Primary**: Observed **ABO allele counts** (A, B, O) with **exact binomial 95% confidence intervals** (Clopper-Pearson).  
- **Comparison with control**: **Odds ratio** (e.g., A vs non-A) with **exact conditional maximum likelihood confidence interval** (e.g., `exact2x2` R package). Report each superpopulation separately.  
- **Relatedness**: Include both individuals but flag the pair. Perform a sensitivity analysis excluding one member.  
- **RhD**: Only report **presence of rs590787 tag**; no frequency estimate for RhD-negative.  

**Sensitivity Analyses**  
Label as sensitivity any analysis that:  
- Uses 1000 Genomes without ancestry stratification.  
- Includes the related pair in the primary test.  
- Assumes Hardy-Weinberg equilibrium in focal or control.  
- Attempts to infer RhD-negative from tag absence (prohibited in primary).  
- Extrapolates beyond directly observed markers.  

**Fail-Closed Implementation & Acceptance Checks**  
1. **Implementation**:  
   - Script verifies each marker exists in both local and 1000 Genomes VCFs; exit if mismatch.  
   - For each sample, ABO call is **only** assigned if at least one allele-defining marker is observed (e.g., rs8176719 for O, rs8176746/7 for A/B); otherwise `no-call`.  
   - RhD: output only the tag genotype; do **not** translate to RhD-positive/negative.  
   - All proportions use exact binomial CIs; control comparison uses `fisher.test` in R (two-sided).  

2. **Acceptance checks**:  
   - Confirm 100% consistency between local ABO calls and observed markers (e.g., no call if only heterozygote ambiguous).  
   - Verify no RhD status inference appears in output.  
   - Confirm relatedness flag is documented in results tables.  
   - Confirm that every focal sample’s callable markers are listed in a per-sample matrix (per directive 1).  
   - Confirm that no sample ancestry is assigned or implied.  

**Deliverable**  
A single table:  
- Columns: sample_ID, ABO_predicted_genotype (A1/A2/B/O1/O2/ambiguous/no-call), tag_rs590787_genotype, callable_markers_count, notes (e.g., related pair).  
- Append control frequencies from 1000 Genomes (global + superpopulations) for the same marker set, with exact CI.  
- No phenotype column.  

**Fail-close rule**: If any ABO or RhD marker is missing for a focal sample, call is `no-call`; do not impute.  
**Primary comparison**: ABO genotype distribution (exact test) vs. 1000 Genomes EUR+global; stratified by superpopulation as sensitivity.
