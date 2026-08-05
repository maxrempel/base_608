**PASS.**

Given the strict constraints, the design is logically sound and complete. No inherent contradictions or violations of the requirements are present. However, the pass depends on correct implementation of the many precise rules.

---

### **Five most dangerous implementation edge cases**

1. **Insufficient eligible negatives**  
   If a survivor’s chromosome lacks four within-copy or four cross-copy negatives (due to callability gate, global exclusion, or matching failures), the pipeline will stop with less than 32 negatives. The design does not specify a fallback. This breaks the downstream assumption of exactly 32 negatives and may cause a hard failure or silent bias.

2. **Non‑deterministic within‑copy ranking**  
   The “frozen SHA‑256” and consensus distance must be computed from stable, invariant inputs. If the consensus sequence, annotation version, or any input field changes between runs (even via library defaults), the ranking order becomes irreproducible. This undermines the deterministic order requirement and could alter selected negatives between executions.

3. **Cross‑copy matching relaxation ambiguity**  
   The phrase “only depth, then consensus base, then reference base may relax” is underspecified:  
   - What does “relax” mean? A tolerance (e.g., ±2 bp depth)? A fuzzy comparison?  
   - Is the relaxation applied sequentially (first relax depth, if still no match then relax consensus base while resetting depth, etc.) or incrementally (allow depth relaxation first, then add consensus base relaxation later)?  
   The exact semantics must be hard‑coded; any misinterpretation will produce a different set of matched negatives.

4. **Global exclusion list inconsistency**  
   The exclusion set must be **identical** for all survivors. If it is built per survivor from its own annotation, two survivors may exclude different positions, causing a position that is a primary candidate in survivor A to be selected as a negative in survivor B. The design requires a singular, pre‑computed global exclusion list, but implementation mistakes (e.g., union vs. per‑survivor) are catastrophic.

5. **Atomic output marker + summary**  
   The “atomic marker plus a separate coordinate‑free summary” implies that the marker must be written only after all tables are fully written (manifests, hashes, etc.). If the process crashes after the summary but before the marker, or vice versa, downstream tools may see an incomplete output set (e.g., missing tables but marker present). The atomic trigger must be **truly transactional** (e.g., file rename after all writes succeed).

---

### **Minimum tests before handing to Ben**

1. **Guard against insufficient negatives**  
   - Create a survivor that yields only 2 within‑copy and 3 cross‑copy negatives (e.g., by seeding only 5 eligible loci).  
   - Verify the pipeline **does not crash** and either (a) gracefully outputs the reduced set or (b) issues a clear, fatal error message. Do not silently produce a partial output that violates the 32‑negative assumption.

2. **Deterministic ordering reproducibility**  
   - Provide identical input twice (same annotation, same frozen CRAMs, same hash‑seed).  
   - Run the full pipeline two times and compare the ordered list of selected negative loci per survivor. They must be **byte‑identical** (same coordinates, same order, same consensus distance and SHA‑256 values).

3. **Cross‑copy relaxation logic**  
   - Injected scenarios:  
     * A candidate matches only after relaxing depth (set all other fields exact).  
     * A candidate matches only after relaxing depth *then* consensus base (depth relaxed, then consensus base relaxed while resetting depth? – the exact rule must be documented and tested).  
     * A candidate never matches even after all relaxations.  
   - Verify the output contains exactly the expected matched negatives and no invalid matches.

4. **Global exclusion list consistency**  
   - Two survivors share several primary candidate positions (e.g., from the same chromosome).  
   - After selection, confirm that **no** locus selected as a negative by any survivor appears in the union of all primary/strict candidate positions from **any** survivor. This must hold cross‑survivor.

5. **Shared mechanism boundary cases**  
   - Build a test where feature direction is present in exactly 3 survivors (both negative strata) and absent in 1 survivor — check that `shared_mechanism` is true.  
   - Build a test where only 2 survivors show direction — check `shared_mechanism` is false.  
   - Build a test where all 3 survivors come from the same batch — verify that `batch_collinearity` flag is set to `shared_mechanism_not_separated_from_batch`.  
   - Build a test where the 3 survivors are from different batches — verify the flag is not set.  
   - Include a case with zero counts to verify the exact small‑sample uncertainty calculation (e.g., Fisher’s exact test) does not crash.
