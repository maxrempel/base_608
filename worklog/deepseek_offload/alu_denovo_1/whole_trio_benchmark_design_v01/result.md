## ALU-DeNovo-1 Whole-Trio Benchmark: Implementation Specification & Checklist

### 1. Recommended Harness Structure

- **Top-level script** (`benchmark_trio.sh`): iterates over autosomes 1–22.
  - For each chr:
    1. Create clean output directory `bench/chr<chr>/`.
    2. Run optimized method with fixed resource constraints (2 cores, 6 GiB, low priority).
       - Two native chromosome-wide pileups (primary MAPQ30/Q25, strict MAPQ60/Q30).
       - Output per tier: `primary_summary.json`, `primary_candidates.tsv`, `strict_summary.json`, `strict_candidates.tsv`.
    3. Capture resource usage via `time -v` (wall, user+sys time).
    4. For each tier, invoke existing comparator on frozen vs optimized outputs.
       - Comparator exit code 0 = exact match; any diff returns non-zero.
    5. Record candidate counts from summary JSONs.
    6. Write atomic `status.chr<chr>.txt` containing:
       ```
       CHR=<chr>
       PASS=[OK|FAIL]
       TIER_PRIMARY_CANDIDATES=<N>
       TIER_STRICT_CANDIDATES=<N>
       WALL_SEC=<sec>
       CPU_SEC=<sec>
       ERROR=<detail if any>
       ```
    7. On any comparator fail or pipeline error, print immediate error and exit with code 1.
- **Aggregation script** (`aggregate_results.sh`): after all chromosomes, gather all `status.chr<chr>.txt` into a single CSV `bench_aggregate.csv` and compute total wall time.
- **Resume logic**: before running a chromosome, test for existing `status.<chr>.txt`; if present and `PASS=OK`, skip; otherwise re-run (deleting old results). This ensures independent resumability.

### 2. Exact Pass/Fail Conditions

- **Per-chromosome pass**:  
  - Optimized pipeline exits with code 0 (no errors, all required files produced).  
  - Comparator on **primary** tier returns exit code 0.  
  - Comparator on **strict** tier returns exit code 0.  
  - All files (`*_summary.json`, `*_candidates.tsv`, `status.` file) present and non-empty (except when zero candidates – TSV may be empty but must exist).
- **Per-chromosome fail**: any of the above fails → overall benchmark fails immediately.  
  - Write `STATUS=FAIL` in status file with error detail.  
  - Pipeline stops (error propagation via `set -e` or explicit checks).
- **Overall benchmark pass**: all 22 chromosomes pass (no fails encountered during whole run).

### 3. Runtime-Comparison Design

**Goal**: obtain a fair runtime estimate for the frozen method under identical hardware and constraints.

**Recommendation**:  
- **Run the frozen method on a measured subset of 3 chromosomes** that span low, medium, and high AluYa5 element density (e.g., chr21, chr7, chr1).  
- Use the exact same resource limits (2 cores, 6 GiB, low priority).  
- Record per-chromosome wall and CPU time for both tiers (sum of per-element pileups).  
- Fit a linear model: `time_frozen ≈ α + β * (#candidates)` (each chromosome run twice, once per tier – but tiers have same element set; include both runs).  
- **Extrapolate** to 22 autosomes using known candidate counts from the frozen outputs.  
- **Clearly label** the estimated total as “extrapolated from chr21,7,1”.  
- If any chromosome in the subset fails equivalence, the benchmark cannot proceed; in that case full frozen re-run might be needed, but that is out of scope.

**Why not full frozen re-run**: Doubles compute time and defeats the purpose of low-resource benchmarking. The subset approach is defensible because the frozen method’s cost scales linearly with candidate count per chromosome (per-element pileups are independent). The optimized method’s cost is roughly constant per chromosome (chromosome-wide pileup), so broken linearity would be obvious. Report both measured subset totals and the extrapolated total.

### 4. Smallest Set of Retained Aggregate Files

- **Per chromosome (11 files total per chr)**:  
  - `status.chr<chr>.txt` (aggregate summary)  
  - `*.primary_summary.json`, `*.primary_candidates.tsv`  
  - `*.strict_summary.json`, `*.strict_candidates.tsv`  
  - (Optional: comparator diff log only if needed for debugging, but not retained in final set.)
- **Aggregate across all chromosomes**:  
  - `bench_aggregate.csv` (one row per chr: chr, primary_candidates, strict_candidates, wall_sec, cpu_sec, pass)  
  - `bench_total.txt` (total wall time, CPU time, overall pass/fail status)  
  - `frozen_runtime_estimate.txt` (subset measured times and extrapolation details)

Total retained files: ~234 core files (22×10 + 3 aggregate). No interim CRAM copies, no intermediate pileup dumps.

### 5. Critical Review: One-Chromosome Equivalence vs. Whole-Trio Benchmark

**Observation**: The single completed chromosome shows exact equivalence in all outputs.  

**Sufficiency for whole-trio benchmark**: Not fully sufficient. The optimized method’s behavior may vary across chromosomes due to:  
- Different AluYa5 element densities (cache/memory pressure on pileup).  
- Chromosome-specific CRAM read distributions or paired-end overlap patterns that could interact with the two-tier reuse logic.  
- Variation in annotation completeness (e.g., some chromosomes may have missing or duplicated reference annotations causing candidate list differences).  
- Zero-candidate chromosomes (ensuring identical empty outputs is a separate edge case).  

Running all 22 autosomes under controlled comparison is **necessary** to detect any such hidden dependencies.  

**Caution for production switch**: Passing this benchmark proves **scientific equivalence** of outputs under unchanged thresholds. It does **not** prove:  
- Long-term stability (e.g., CRAM index corruption over repeated runs).  
- Resource guarantees (the optimized method uses less CPU but may have different memory peaks).  
- Pipeline integration (maintainability, logging, error handling).  

Therefore, this benchmark is a **necessary precondition** for a production switch, but additional validation (stress test, integration test, code review) is required before any production change.

---

**Checklist for implementer**:
- [ ] Script uses `set -euo pipefail`.
- [ ] Chromosome loop respects resource locks (e.g., `flock` or `nice` + `cpulimit` if available).
- [ ] Output directories cleaned on re-run (except skip if already PASS).
- [ ] Comparator invoked in exact order primary then strict.
- [ ] Time capture via `/usr/bin/time -v` (or `times()` shell wrapper).
- [ ] All hazard checks (CRAM index, annotation files, temp space) done before each chromosome.
- [ ] Candidate counts extracted from JSON keys (not TSV line count) to avoid empty-file ambiguity.
- [ ] Aggregate CSV written with header.
- [ ] Frozen total runtime extrapolation code included.
- [ ] Final report states that benchmark tests scientific equivalence only.
