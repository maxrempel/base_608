# Preliminary Report on Omun Insertion Rates in Starseed Participants and Cultured Controls

**Date:** 2026-07-25  
**Status:** PRELIMINARY – not for public distribution or clinical use

---

## 1. Scientific Question

Do the aggregate Omun insertion rates of three deidentified Starseed participants (S1, S2, S3) fall within the range expected for cultured human genomes from the 1000 Genomes Project, given that Omun endpoints are database-novel or known-rare autosomal OMEGA insertions?

---

## 2. One-Paragraph Main Conclusion

Among the three Starseed participants, S1 shows an Omun rate (58.2 per billion callable bases) that lies within the 95 % prediction interval of the 20 cultured controls (54.0 to 86.6 per Gb) and near the lower end of the control distribution. In contrast, S2 (1.13 per Gb) and S3 (0.375 per Gb) have rates far below any control (lowest control: 53.7 per Gb). However, this comparison is severely confounded by culture and sequencing platform differences: all controls were cultured cells from the 1000 Genomes Project, whereas S2 and S3 are uncultured or not culture‑matched, and S1 has unknown culture status. Without matched uncultured controls, the very low rates in S2 and S3 cannot be attributed to any biological property of the participants and could reflect technical artifacts (e.g., DNA quality, library preparation, or platform batch effects).

---

## 3. Table-Ready Explanation of All Individuals

The table below defines all key terms and lists every sample used in this report.

**Term definitions**  
- **Omun:** Clean, deduplicated, two-sided autosomal OMEGA insertion loci that are either new to databases or known with a population frequency below 0.001.  
- **Callable bases:** Autosomal bases passing the locked D10 callability filter (denominator).  
- **Rate:** Number of Omun loci per billion callable bases (Gb).  
- **Starts2 passes:** A stricter, read‑level diagnostic that counts how many Omun loci survive an additional read‑support check. This is *not* a truth validation and does not revise the Omun burden.

| Sample / Group | Culture Status | Omun Count | Novel | Rare | Callable Bases | Rate (per Gb) | Starts2 Passes |
|----------------|----------------|------------|-------|------|----------------|---------------|----------------|
| **Starseed participants** | | | | | | | |
| S1 | Unknown | 155 | 140 | 15 | 2,663,784,865 | 58.19 | 64 |
| S2 | Uncultured or not culture‑matched | 3 | 3 | 0 | 2,664,221,029 | 1.13 | 1 |
| S3 | Uncultured or not culture‑matched | 1 | 1 | 0 | 2,664,016,901 | 0.375 | 1 |
| **Cultured controls (n=20)** | | | | | | | |
| Mean ± SD | All cultured (1000 Genomes) | 187.6 ± 20.3 | – | – | – | 70.32 ± 7.60 | – |
| Range | – | 143 – 224 | – | – | – | 53.70 – 84.01 | – |

Note: Control starts2 pass rate overall (excluding one unavailable audit) is 1,386/3,575 = 38.8 %.

---

## 4. Control Spread and Focal Comparison

- **Control distribution:** The cultured controls span a rate range of 53.7 to 84.0 per Gb. The approximate 95 % confidence interval for the mean rate is 66.8 to 73.9 per Gb; the 95 % prediction interval for a single new cultured genome is 54.0 to 86.6 per Gb.  
- **S1 (rate 58.2):** Falls within the prediction interval. Only 1 of 20 controls (EUR_02, rate 53.7) lies at or below S1.  
- **S2 (rate 1.13) and S3 (rate 0.375):** Lie far below the prediction interval. No control (0 of 20) has a rate at or below these values.  

Because S2 and S3 are not culture‑matched to the controls, this extreme deviation cannot be interpreted as a biological difference. Culture‑related factors – such as increased DNA damage, altered insertion detectability, or sequencing platform artifacts – could explain the gap. Uncultured controls are required before any conclusion about the participants themselves can be drawn.

---

## 5. Technical‑Audit Attrition and What It Means

The “starts2” column reports a stricter read‑level diagnostic: it counts how many Omun loci also satisfy an additional, more stringent read‑support criterion. In the controls, 38.8 % of Omun loci pass this diagnostic. For the Starseed participants, the counts are:
- S1: 64/155 (41.3 %)  
- S2: 1/3 (33.3 %)  
- S3: 1/1 (100 %, but based on a single locus)

These numbers reflect technical read‑support attrition, not a measure of truth or falsehood. They are useful for evaluating the sensitivity of the detection pipeline and for monitoring batch‑to‑batch consistency, but they do *not* alter the reported Omun burdens. A low starts2 pass rate does not invalidate an Omun call.

---

## 6. Topology Boundary and How to Test Scattered/Dispersed Topology

The concept of “scattered” or “dispersed” topology refers to whether the Omun insertions cluster in a few genomic regions or are spread across the genome. Reliable topology assessment requires a larger set of loci than available here.

- **S2:** Only 3 Omun loci – insufficient to draw any topological conclusion.  
- **S3:** Only 1 Omun locus – insufficient. A larger, previously supplied category for S3 contains 7 deduplicated autosomal loci and 6 clean loci, but this set is still too small for robust topology testing.  
- **S1:** 155 loci could, in principle, support a topology analysis, but such an analysis must be performed separately from the Omun burden calculation.  

**How to test:**  
1. Use a named, larger preserved category (e.g., all OMEGA insertion calls, not just Omun).  
2. Compute genomic distances or cluster statistics (e.g., nearest‑neighbor distances, scan statistics) against a null distribution derived from matched controls.  
3. Report dispersion metrics without mixing them into the Omun definition.  

Until a larger, verified set of insertions (from both participant and control samples cultured and processed identically) is available, no topology claim can be supported.

---

## 7. Smallest Practical Uncultured Matched‑Control Acquisition/Analysis Plan

To eliminate the culture/platform confound, the following minimal plan is recommended:

1. **Acquire 10–20 uncultured whole‑blood or tissue DNA samples** from publicly available healthy‑donor repositories (e.g., HapMap, Simons Genome Diversity Project) that have been sequenced on the same platform (or a comparable platform) as the Starseed samples.  
2. **Process all samples** through the same bioinformatics pipeline (alignment, D10 callability, OMEGA detection) used for the Starseed participants.  
3. **Compute Omun rates** using identical filters.  
4. **Compare S2 and S3 rates** to the uncultured control distribution.  

If the uncultured control rates cluster near the cultured control rates (≈ 50–85 per Gb), then the very low rates in S2 and S3 become genuinely remarkable. If uncultured controls also show low rates, then the culture effect explains the difference.

---

## 8. Claims Not Supported Yet

The following statements are **not** supported by the present data:

- That S1, S2, or S3 have a biological enrichment or depletion of Omun insertions relative to any human baseline.  
- That the low Omun rates in S2 and S3 indicate a non‑human origin or a distinct biological lineage.  
- That the Omun loci in any participant exhibit scattered or dispersed genomic topology.  
- That the technical starts2 diagnostic confirms or refutes the validity of any Omun call.  
- That any observed difference is biologically meaningful, because culture/platform confounding has not been addressed.  

Any claim beyond simple descriptive statistics must await culture‑matched controls and an independent replication.
