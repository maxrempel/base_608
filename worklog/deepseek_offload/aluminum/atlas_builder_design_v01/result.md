## 1. Exact Output Schemas & Key Invariants

**Output files (machine-readable TSV/JSON; one directory per build with date+commit):**

- `chromosome_admission.tsv`: columns `chromosome`, `tier` (primary/strict), `n_families_with_candidates`, `n_complete_families`, `total_denominator_families` (count of families with any chr row), `completion_state` (complete/incomplete).  
  Invariant: `total_denominator_families` = count of distinct families that appear in *any* chr table for this tier. `n_complete_families` = families present in chr1‑22 all.

- `complete_family_summary.tsv`: columns `family_id`, `tier`, `n_chromosomes_present`, `n_candidates_total`, `n_unique_exact_keys`, `n_occurrences_per_key` (JSON list).  
  Invariant: only families with exactly 22 chromosomes (1‑22) appear.

- `candidate_occurrence_registry.tsv`: columns `tier`, `family_id`, `child_id`, `chromosome`, `element`, `genomic_position`, `child_allele`, `occurrence_count` (across all families), `first_seen_family`, `first_seen_build`.  
  Indexed by exact recurrence key: `assembly + chromosome + element + genomic_position + child_allele`.

- `exact_key_recurrence.tsv`: columns `assembly`, `chromosome`, `element`, `genomic_position`, `child_allele`, `total_occurrences`, `distinct_families`, `distinct_children`.  
  Invariant: `total_occurrences` ≥ `distinct_families` (one child per family may have >1 occurrence? but by key identical, so should be 1 per child; but same key across multiple children in same family? rare).

- `population_summary.tsv`: columns `superpopulation`, `population`, `tier`, `n_families`, `n_complete_families`, `n_candidates`, `n_unique_keys`, `mean_candidates_per_family`.  
  Denominator = families with at least one candidate in that tier.

- `build_manifest.json`: `build_version`, `source_directory`, `input_layout_detected`, `file_hashes` (list of `{path, sha256}`), `admitted_tables`, `validation_passed`, `validation_errors`.

- `validation_report.json`: list of checks and pass/fail, e.g., duplicate detection, missing metadata not inferred, all chr rows accounted.

- `preliminary_human_report.txt`: concise, no significance tests, no Starseed, just numbers: total families, complete families, total candidates per tier, distinct keys per tier, population counts, any duplicate conflicts found.

**Key invariants:**
- Input never modified; only read.
- All metadata fields from `not_available` left as‑is.
- Biological interpretation always `not_validated` or `none_observed_under_screen`.
- Assembly fixed: GRCh38DH (or hg38) from input; if mixed, fail.

---

## 2. Deterministic Discovery/Admission Rules (Robust to Two Layouts)

**Discovery algorithm (repeatable, order‑independent):**
1. Walk `root` directory recursively.
2. For each file with name exactly matching one of:
   - `primary_child_only_candidates_v01.tsv`
   - `strict_mapq60_child_only_candidates_v01.tsv`
3. Record full path and detect layout:
   - If file is directly under a directory named like `chr[0-9]+`, then `chromosome = directory basename`.
   - Else if file is under `primary_v01/` or `strict_mapq60_v01/`, then `chromosome = name of parent of that directory` (e.g., `chr1/primary_v01/...`).
   - Otherwise, reject and fail closed with an error in validation report.
4. Parse TSV with set of known columns. Map to canonical columns:
   - `family_id`, `child_id`, `mother_id`, `father_id`, `population`, `superpopulation`, `chromosome`, `element`, `genomic_position`, `child_allele` (from `primary_child_supported_alleles` or `mapq60_child_supported_alleles` depending on tier).
5. For each row, compute exact recurrence key: `assembly + ":" + chromosome + ":" + element + ":" + genomic_position + ":" + child_allele`. Assembly is derived from file context (read header comment if present, else use "GRCh38DH").
6. Admit row if:
   - All required columns present and valid (non‑null, numeric where expected).
   - `chromosome` matches the directory‑derived chromosome; if mismatch, flag as error and exclude.
   - No missing metadata inferred; leave as `not_available`.
7. Build per‑chromosome tables: concatenate all rows for a given tier+chromosome, sorted by `family_id, child_id, genomic_position`.
8. Determine completion state: a family is complete for a tier if it appears in all 22 chromosomes (chr1‑22) in that tier's chromosome table. (Families may have rows in some chromosomes but not others.)

---

## 3. Duplicate/Conflict Handling

**Detection:**
- For each (tier, chromosome, family_id) group, detect if multiple source files provide rows for the same (family, chromosome). This can happen when historical copies are present in different layout directories.
- Compare rows row‑wise by exact recurrence key. If multiple rows have identical key, they must have identical values for all other columns (especially `primary_child_supported_alleles` and quality metrics). If any discrepancy, fail closed: record both in validation errors, do not admit ambiguous duplicates.
- If identical, admit one copy only (deduplicate).
- Log in validation report: `duplicate_rows_found`, `duplicate_rows_identical`, `duplicate_rows_conflict`.

**Conflict handling:**
- Conflict → build aborts with clear error listing conflicting files, rows, and differing columns.
- No human override; must be fixed upstream.

---

## 4. Scientific Summaries (Meaningful Now, Scalable to 600 Trios)

**Current (≤10 families):** Provide per‑family and per‑population counts. No rates that require denominator of all trios (since not all chromosomes necessarily present). Use `n_families_with_candidates` as denominator.

**Scaling:**
- All summaries use dynamic grouping by `family_id` and `chromosome`. No hardcoded thresholds.
- `complete_family_summary` can be joined with denominator from cohort registry (separate, not part of atlas builder) when that exists.
- `exact_key_recurrence` table will naturally grow; already keyed by recurrence, so efficient to update incrementally by appending new families and re‑aggregating.

**Outputs:**
- Chromosome admission includes `total_denominator_families` which is the count of families that have *any* candidate in that tier. This is meaningful even with few families.
- Population summary uses `n_families` as denominator; no comparison across populations allowed.
- Human report: "As of build YYYY-MM-DD, N complete families (of total M families with any candidate). Primary tier: X candidates, Y distinct recurrence keys. Strict tier: … No biological interpretation. No comparison with Starseed."

---

## 5. Unit/Integration Tests

**Test environment:**
- Create synthetic directory with two layout patterns.
- Use controlled TSV files with known columns.

**Tests:**
1. **Layout detection:** Provide `chr1/primary_child_only_candidates_v01.tsv` and `chr2/primary_v01/child_only_candidates_v01.tsv`. Verify both detected, parsed, chromosome assigned correctly.
2. **Duplicate identical:** Same family+chromosome in two files, identical rows. Assert one copy admitted, no conflict.
3. **Duplicate conflict:** Introduce a single column difference between duplicate rows. Assert build fails with `duplicate_rows_conflict` in validation report.
4. **Incomplete family:** Family appears in chr1‑21 only. Verify `complete_family_summary` excludes it; `chromosome_admission` shows `completion_state = incomplete`.
5. **Missing metadata:** Row with `not_available` in population. Assert not overwritten.
6. **Rejection of layout ambiguity:** Place file in non‑standard layout (e.g., `chr1/other/subdir/child_only_candidates_v01.tsv`). Assert fail closed.
7. **Exact key recurrence aggregation:** Two families share same recurrence key. Verify registry and recurrence count correctly.
8. **No input modification:** Check that source files unchanged after run (by hashing before and after).
9. **Empty chromosome:** Directory `chr22` exists but no candidate file. Should such directory be present? If missing, family incomplete. Test with a family missing chr22 entirely – admission shows 21 chromosomes.
10. **Assembly mismatch:** File header says `GRCh38` but another file says `hg19`. Assert fail closed.

---

## 6. Common Statistical or Interpretive Mistakes to Prevent

1. **Assuming missing chromosome means zero candidates instead of incomplete family.** Prevent: require explicit 22‑chromosome presence for completeness; never impute zero.
2. **Comparing primary vs strict rates without accounting for non‑subset property.** Prevent: always report tiers separately; in human report, state explicitly "strict is not a subset of primary".
3. **Labeling absence as "no de novo" (biological).** Prevent: always use `none_observed_under_screen`.
4. **Using total families in cohort as denominator without checking completeness.** Prevent: denominator only from families that have at least one candidate for that tier.
5. **Averaging per‑family rates when families have different numbers of callable positions.** Prevent: do not compute rate without callable positions (use `primary_callable_positions` or `mapq60_callable_positions` per family+chromosome as denominator, but only in dedicated analysis, not in build report).
6. **Ignoring family‑level recurrence in exact key table.** Prevent: recurrence table is per occurrence, not per family. Interpretation note: a key appearing in multiple families may be a recurrent element, but no significance claimed.
7. **Merging historical duplicate copies without identity check.** Prevent: enforce identity or fail closed.
8. **Using different assembly versions across files without explicit error.** Prevent: detect and abort.
