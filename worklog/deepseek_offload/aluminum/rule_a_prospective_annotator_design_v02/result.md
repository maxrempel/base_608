**Implementation Checklist: Rule A Audit Aggregator**

1. **Load sealed atlas**  
   - Validate schema: `family_id`, `tier`, `canonical_pre_strand_count`, `row_hash` (or equivalent).  
   - Reject unknown columns, missing values, bad tier values (`primary`, `strict_mapq60`), non-integer counts.  
   - Compute SHA-256 over atlas rows sorted by `(family_id, tier)`; compare with sealed manifest hash. Mismatch → abort.

2. **Load per-occurrence TSV**  
   - Accept only one rule column: either `rule_a_flag` or `rule_one_read_mapq50_bq30` (map both to internal `rule_a`).  
   - Strict booleans only: `0/1`, `true/false`, or `True/False`; reject all else.  
   - Validate columns: `family_id`, `tier`, `occurrence_key`, `frozen_strand_survivor`, rule flag. No extras.  
   - Empty/header-only file is legal only if every atlas `canonical_pre_strand_count` is 0. Otherwise abort.  
   - Fail on duplicate `occurrence_key` globally or per family; fail on missing/unknown family or tier.  
   - Row count per `(family_id, tier)` must exactly equal atlas `canonical_pre_strand_count` for that pair.  
   - Reject extra blank lines, malformed TSV, or BOM.

3. **Core invariants (fail closed on any violation)**  
   - Atlas and input must have identical family/tier set.  
   - Every occurrence row maps to exactly one atlas row.  
   - No row exists without a valid strict bool for both rule flag and survivor.  
   - `flagged + unflagged == canonical_pre_strand` per family/tier.  
   - `survivor_flagged + survivor_unflagged == canonical_survivors`.  
   - `canonical_survivors ≤ canonical_pre_strand` (survivor implies an occurrence).  
   - No silent truncation; any mismatch or unrecognized data → no output.

4. **Aggregation (deterministic, sorted by family_id then tier)**  
   - Per `(family_id, tier)`, compute:  
     - `canonical_pre_strand` from atlas.  
     - `flagged`, `unflagged` from rule flag.  
     - `canonical_survivors` from `frozen_strand_survivor == True`.  
     - `survivor_flagged`, `survivor_unflagged` (survivor flag intersection).  
   - Use integer arithmetic only. No floating point, no timestamps, no randomness.

5. **Output**  
   - Coordinate-free rows: `family_id`, `tier`, the six aggregate counts above.  
   - Add provenance: input file names, atlas version/hash, per-occurrence hash.  
   - Add full-output SHA-256 and atomic marker (`atomic:1`, `biology:NO`).  
   - Never modify caller data, atlas, or any input file; write results only to a fresh immutable record.

6. **Unit tests (6)**  
   1. Happy path mixed flags/survivors with correct counts.  
   2. Header-only per-occurrence + all-zero atlas → zero aggregates.  
   3. Duplicate occurrence_key → abort.  
   4. Bad tier or malformed boolean → abort.  
   5. Row-count/family mismatch vs atlas → abort.  
   6. Atlas hash mismatch or missing family → abort.
