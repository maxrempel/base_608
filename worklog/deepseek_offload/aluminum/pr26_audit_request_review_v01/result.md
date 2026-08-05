**1. Logical contradictions or missing technical controls that would make the frozen question unanswerable**  
No logical contradiction is present. The design is internally consistent: cohorts are defined, the zero count of loose non‑survivors is properly recorded as observed, and the matching rules are frozen.  

**Missing control – batch/read‑group confounding**  
The frozen matching rules do **not** require negatives to be matched on read group, lane, flowcell, library, or platform. If all four survivors happen to derive from a single library/batch while negatives come from different batches, any shared feature deviation (e.g., insert size, clipping, mapping quality) could be driven by batch effects rather than a genuine technical mechanism. This does **not** make the question unanswerable (the audit can still produce a deterministic result under its own rule), but the conclusion will be ambiguous and may misattribute a batch artefact as a “shared technical mechanism.”  

**Not a contradiction – strict‑tier presence feature**  
The feature “independent strict‑tier presence” may be uniformly absent (zero) for all PR26 survivors if the sole strict‑tier survivor lies outside PR26. That does not break the logic; it simply means that feature cannot deviate, so it will never satisfy the ≥3‑survivor criterion. The design remains answerable.

---

**2. Implementation checks Ben must perform (without changing frozen cohorts, matching rules, or thresholds)**  

- **Confirm zero loose non‑survivors** – Verify that the sealed atlas indeed contains zero PR26 primary loose non‑survivors under the frozen gate, and that this is not due to a filtering error.  
- **Verify negative uniqueness** – Ensure the eight callable negatives per survivor are distinct (no overlap across survivors). If overlap exists, confirm the frozen relaxation order handles ties and document it.  
- **Document deterministic relaxation order** – The matching rules for repeat strand, identity/coverage bins, etc. must be applied in a fixed, recorded sequence for the eight negatives per survivor. Check that no ad‑hoc relaxation occurs.  
- **Define “direction of deviation” precisely** – For each survivor, compare its feature value to the median (or mean) of its within‑element negatives and separately to the median of its other‑element negatives. A deviation is “same direction” if both comparisons show the same sign (higher/lower). A deviation of zero or ambiguous sign (e.g., one comparison higher, the other lower) must be treated as “not deviating.”  
- **Pre‑specify effect size and uncertainty metric** – Because of the small sample, use a non‑parametric effect size (e.g., median difference) and a compatible uncertainty interval (e.g., bootstrap percentile CI or exact CI for median). This must be frozen before computation.  
- **Check strict‑tier presence definition** – Confirm whether the feature is “candidate belongs to the strict‑tier survivor list” (binary) or “number of strict‑tier observations in the same repeat copy.” If the strict‑tier survivor is not in PR26, the feature is uniformly zero and should be documented as “unavailable” in the schema.  
- **Avoid data‑driven feature selection** – Only the predefined list of features may be tested; do not examine additional features or post‑hoc combinations.

---

**3. Minimal de‑identified result schema (preserves exact attrition, uncertainty, unavailable fields)**  

```
feature: str
survivors_available: int          # number of survivors with non‑missing feature data (max 4)
within_element_directions: [str]  # length = survivors_available, each "higher"/"lower"/"no_deviation"
other_element_directions: [str]   # same length, same ordering
consistent_across_strata: [bool]  # True if both directions match (both higher
