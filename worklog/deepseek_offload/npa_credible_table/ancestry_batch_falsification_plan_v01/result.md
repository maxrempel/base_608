### Compact Sealed Plan: Distinguishing Ancestry/Batch Artifact from Real NPA Burden

1. **Smallest ancestry-matched controls**  
   - Retrieve all **PJL** children from the same NPA-filtered 1000 Genomes trio dataset. If <3, expand to any **SAS** superpopulation (GIH, BEB, STU, ITU) processed with the same pipeline.  
   - Also retrieve 2–3 additional **AMR** and **AFR** children (e.g., HG01087 and HG02280 already exist) to confirm the pattern of zero burden is not idiosyncratic.

2. **Callable-opportunity normalization**  
   - For every child (cases and controls), compute **total callable bases** (sites passing `npa_clean_germline_strict_v03_phase0_locked_2026-07-21` filters) from the queue/strata.  
   - Express burden as **events per 1e6 callable bases**. Compare normalized rates across populations. If denominator missing, use total genotyped sites in the filtered VCF as proxy.

3. **Contamination and batch checks**  
   - **Contamination**: If verifyBamID metrics exist in 1000 Genomes metadata, check FREEMIX for all trio members of HG02683. Flag if >0.02.  
   - **Batch**: Extract read-group tags (SM, LB, PU) from CRAM headers for all three trios. Check if HG02683’s trio shares library/flowcell/lane with high-burden controls or differs from the zero-burden trios.  
   - **Pedigree QC**: Compute IBD sharing within trios (e.g., plink `--genome`) to rule out sample swaps.  
   - **Allelic balance**: For each of the 11 provisional NPA events in HG02683, plot depth-normalized alternate-allele fraction. Real germline heterozygotes cluster near 0.5; mixture/contamination produces spread.

4. **Exact falsification criteria**  
   - **Not falsified** (signal may be real) if:  
     * Normalized burden in HG02683 > **mean of SAS controls + 3σ** (or >5σ for <5 controls).  
     * No contamination (FREEMIX <0.02).  
     * No batch effect (HG02683’s library/batch does not correlate with high burden across non-SAS samples).  
     * Allelic balance of events is consistent with heterozygosity (median ~0.5, IQR narrow).  
   - **Falsified** (artifact) if any of:  
     * SAS controls have similar normalized burden (i.e., the 11 events are typical for SAS).  
     * Contamination >0.02 or sample swap detected.  
     * Batch covariate explains higher burden (e.g., all high-burden samples share a run).  
     * Allelic balance deviates strongly from 0.5 for majority of events.

5. **What would reopen the autism gate**  
   - The gate reopens if and only if:  
     * The signal passes all falsification checks (not falsified).  
     * The **only** remaining confounder is superpopulation (i.e., HG02683 has significantly higher rate than ancestry-matched controls).  
     * No contamination, batch, or technical artifact found.  
   - Reopening permits phenotype analysis *only after* documenting that the ancestry-matched normalization holds and the result is replicable in an independent SAS trio set.

6. **What would permanently close the autism gate** (for this 3-child dataset)  
   - The gate closes forever if:  
     * The signal is fully explained by ancestry (normalized rate falls within SAS control distribution).  
     * OR any contamination/batch artifact is confirmed.  
     * OR allelic balance indicates mixture.  
   - “Permanently” means this trio set cannot be used to infer any association with autism; any future analysis would require new data.
