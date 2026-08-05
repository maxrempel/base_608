1. **Exact same-batch controls exist?** No. The two available PJL controls (HG02495, HG02605) have batch signatures differing from signal and from each other, and no accepted CRAM/CRAI handoff or read-group manifest establishes same-batch status for any candidate. HG02653 is unavailable; the remaining seven alternates have no accepted deployment record.

2. **Narrowest result‑producing bypass:** Use the two PJL controls (HG02495, HG02605) as the **available but mismatched** control set. Proceed with a **two‑control falsification unit** that compares signal metrics against each control individually and against the pooled control pattern. No same‑batch trio can be assembled; this bypass yields the smallest defensible step.

3. **Predeclared control selection and denominators:**  
   - Controls: HG02495 (PJL‑A), HG02605 (PJL‑B).  
   - Denominators: 24 signal regions for each control (all rows from frozen pilot).  
   - Note: HG02653 is excluded; no other control has accepted evidence.

4. **Falsification criteria (minimum thresholds to reject same‑batch null):**  
   - Alt‑bearing rate: signal 24/24 (100%) vs. controls 14/24 (58%) and 7/24 (29%).  
   - Both‑strands rate: signal 20/24 (83%) vs. 9/24 (38%) and 2/24 (8%).  
   - Median alt MAPQ: signal 23 vs. 19 and 2.  
   - Strict connected‑locus pass rate: signal 0/5 vs. control‑A 1/5.  
   - Batch signatures: signal differs from both controls.  
   - Any one of these disparities falsifies the hypothesis that signal shares the same platform‑batch as the controls. Recommended criterion: **alt‑bearing >50% in controls** (falsified if control alt‑bearing is <50% while signal is 100%); **both‑strands >40%** in controls (falsified if control rate is <40% while signal is >80%). Apply both criteria jointly.

5. **What cannot be concluded:**  
   - That the signal is a falsification (only that it **differs** from the available controls; a true batch signature mismatch may reflect genuine technical variation).  
   - That any single control represents a valid negative or positive for the signal’s platform‑batch.  
   - That the missing HG02653 or any alternate control would match the signal.  
   - That the two controls are themselves same‑batch (they are not).  
   - That the phenotype or family structure of the signal is relevant (sealed).
