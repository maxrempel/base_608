## Compact Specification and Scientific Interpretation Checklist

### 1. Exact survivor-versus-negative numerators and denominators

Define for each of the 4 survivors (`s = 1..4`):

- **Survivor numerator** `N_surv(s, cat)` = number of child reads supporting the candidate allele at survivor locus `s` that fall into category `cat`.
- **Survivor denominator** `D_surv(s, cat)` = total number of child reads supporting the candidate allele at locus `s` (i.e., all reads in survivor set for that locus).
- **Within-element negative numerator** `N_within(s, cat)` = number of primary-quality child reads at the matched within-element negative locus for survivor `s` that fall into category `cat`.
- **Within-element negative denominator** `D_within(s, cat)` = total primary-quality child reads at that within-element negative locus.
- **Cross-element negative numerator** `N_cross(s, cat)` and **denominator** `D_cross(s, cat)` analogous for the cross-element matched negative.

Categories required:
- **Pair orientation** (RF, FR, etc. – but note orientation is identical to strand in retained rows, so effectively strand categories).
- **Mapping quality** (exact integer values, or binned into intervals if sparsity causes zeros).
- **Soft clipping** (total soft-clip count per read, include 0).
- **Duplicate flag** (true/false).
- **Batch/read-group** (categorical labels, but raw labels not exposed – use generic category IDs like `RG1`, `RG2`, …).

All numbers are **descriptive read-level counts**; inferential statistics must treat locus as the unit.

### 2. Effect sizes (locus-level primary)

For each survivor `s` and each category `cat`, compute the **locus-level delta**:

- Within-stratum delta: `median(N_surv(s,cat)/D_surv(s,cat) - N_within(s,cat)/D_within(s,cat))` over categories? No – better: For each category, compute the difference in fraction between survivor and negative at that locus, then summarise across loci with median and range.  
  Already done for mapping quality, soft clip, duplicate fraction in frozen features. Extend to pair orientation and read-group.

- **Pair orientation**: For each orientation category, compute survivor fraction minus within-negative fraction, and survivor minus cross-negative fraction. Report median and range across 4 loci, plus sign consistency (e.g., 4/4 positive means all loci have higher fraction in survivor than in both negatives).  
  Frozen: 3/4 survivor loci show concentration in one orientation, but that orientation is shared by only 3/4. So the delta for that dominant orientation may be positive only for 3/4.

- **Read-group**: For each read-group category, compute delta. Frozen: all 4 survivors show read-group concentration relative to both negatives, but the dominant category differs. So deltas will be category-specific; summarise by “at each locus, at least one RG category has positive delta, but the category label varies”. Report median of the maximum delta per locus.

- **Duplicate fraction**: Already reported as zero in both strata for all 4. Effect size delta = 0 exactly.

- **Mapping quality**: Within median delta 0, cross median +2.75 but only 0/4 consistent direction. So no systematic shift.

- **Soft clip**: Within median +0.0643 (4/4 nonnegative? Range includes 0 so at least one locus zero), cross median +0.1382 (3/4 consistent direction, one negative). Soft clipping is moderately enriched in survivor reads, but not universally.

### 3. Estimable, noninformative, confounded

- **Estimable**:
  - Differences in read-level feature distributions between survivor and matched negative loci (within and cross), using locus-level medians/fractions as primary summary.
  - Direction consistency across 4 loci (e.g., 4/4 same sign).
  - Batch/read-group concentration (presence of any category with positive delta) – but cannot identify which group because labels differ per locus.
  - Pair orientation concentration per locus, and overlap across loci.

- **Noninformative by filtering**:
  - Duplicate flag: no variation (all zero delta) – noninformative for discrimination.
  - Library: constant across all loci – noninformative.
  - Transition/transversion: all survivors are transitions, so no comparison possible. This is a structural limitation of the current PR26 event set.

- **Structurally confounded**:
  - **Pair orientation and strand** are identical in the retained rows → cannot separate orientation effects from strand effects. Any conclusion about orientation is actually about strand.
  - **Read-group concentration** is confounded with batch, flowcell, lane, platform_unit (all are highly correlated in typical sequencing). The fact that the dominant read-group differs at every survivor means the concentration could be due to any of these confounded factors, not necessarily read group per se.
  - **Mapping quality cross-element delta** (median +2.75) may be driven by a single outlier locus (range -10 to +19, 0/4 consistent). Not robust.

### 4. Structural mismatch between survivor candidate-support reads and negative all-primary reads

- **Survivor reads** are only those that support the candidate allele (i.e., pass the allele-specific filter). They are a subset of all primary-quality reads at that locus – typically a minority.
- **Negative reads** are all primary-quality reads at the negative locus. Therefore the negative denominator includes reads that may not align to the alternative allele, whereas the survivor numerator includes only reads that do.
- This mismatch means:
  - Features that correlate with being a primary-quality read (e.g., mapping quality distribution, soft clipping) are inherently different because the survivor reads are a non-random subset. Any difference could be due to the allele-support filtering step, not to locus-specific technical artifact.
  - For example, survivor reads may have higher mapping quality simply because they must map well enough to call the alternative allele, while negative reads include poorly mapping reads that still pass primary quality.
- The design cannot disentangle “read feature bias caused by technical artifact at the survivor locus” from “read feature bias inherent to the allele-support read selection mechanism.” This is a fundamental limitation.

### 5. Can one pair-orientation or batch category account for all four survivors?

**Pair orientation**: 3/4 survivor loci show concentration in a single orientation. However, that same orientation is dominant in only 3/4 loci. The fourth locus either has a different dominant orientation or is balanced. Therefore **no single orientation can account for all four survivors**. At most 3/4 share the same orientation.

**Batch/read-group**: All 4 loci show concentration in some read-group relative to negatives, but the dominant group is different at every survivor. **No single read-group (or batch) is shared across all four survivors.** Therefore no single category can account for all four survivors.

**Conclusion**: Systematic technical artifact from a single orientation or batch is ruled out as the sole cause.

### 6. Do not expose coordinates, read names, sample identifiers, or raw read-group labels.

All above summaries use anonymous locus indices (1–4), category labels generic (e.g., “orientation A”, “RG_1”), and aggregate statistics (medians, ranges, consistency counts). No raw identifiers are revealed.

---

## Strongest Safe Conclusion

The four survivor loci cannot be explained by any single read-level technical artifact that is consistent across all loci. Specifically:

- No single pair orientation (strand) is enriched at all four (only 3/4 share the same orientation).
- No single read-group/batch is enriched at all four (the dominant group differs at each survivor).
- Duplicate fraction shows zero difference from matched negatives.
- Mapping quality shift is inconsistent (0/4 loci show a consistent directional delta), and the cross-element median +2.75 is fragile.
- Soft clipping shows a moderate enrichment in survivor reads compared to negatives (median deltas +0.064 within, +0.138 cross), but direction is not universal (3/4 consistent). This enrichment could reflect the allele-support read selection bias (structural mismatch) rather than a true artifact specific to the survivor loci.

Therefore, the surviving candidates are not the product of a uniform global technical artifact measurable in the retained features. However, the analysis cannot exclude:

- Locus-specific artifacts (e.g., a unique local sequence context causing misalignment).
- Confounded artifacts that manifest differently at each locus (e.g., batch effects that are not globally uniform).
- Unmeasured features (e.g., internal indel structure, read-start coordinate, full-reference remap multiplicity).

**Recommendation**: The audit supports no global systematic error, but locus-specific manual review of alignment complexity (especially soft-clip patterns) and a check of whether the soft-clip enrichment is consistent with known local misalignment motifs (e.g., homopolymers or repeats) are warranted before publication.

---

## Additional Aggregate Calculations Required Before Publication

1. **Locus-level confidence intervals** for the soft-clip delta (within and cross) using a bootstrapped median (or a non-parametric test) to assess whether the observed moderate enrichment is statistically distinguishable from zero given only 4 loci.  
2. **Pair-orientation delta consistency**: For the orientation that appears in 3/4 survivors, compute the median delta across those 3 loci and perform a sign test (or exact binomial) to confirm directionality.  
3. **Read-group concentration test**: For each locus, compute a permutation test (shuffling read-group labels across survivor and negative reads) to quantify whether the observed maximal delta exceeds chance. Pool the p-values across loci (e.g., Fisher’s method) to test for an overall effect.  
4. **Mismatch sensitivity analysis**: Compute the same deltas using only a subset of negative reads that are filtered to have mapping quality above a certain threshold (e.g., >20) to partially mimic the survivor read selection. If soft-clip delta disappears, the mismatch is the cause.  
5. **Stratify soft-clip delta by mapping quality** – check whether the soft-clip enrichment is driven by low-MQ reads that are excluded from survivor set.  
6. **Check whether any other retained field (e.g., distance from read edge, insert size) shows a consistent pattern** – not yet summarised in frozen features. Compute locus medians and deltas for those fields.  
7. **Document the read-group labels** (as anonymised codes) to confirm that the dominant group at each locus is indeed different (not just a different code but same underlying batch). This requires a cross-table of read-group vs. flowcell/lane – but cannot be done without linking to those fields. At minimum, verify that the libraries and platforms are identical, so the read-group difference is not trivial.

These calculations will quantify the robustness of the observed signals and address the major limitation of locus-level inference with only 4 data points.
