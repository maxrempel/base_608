Return a compact implementation checklist, maximum 2,500 characters, for a deterministic Python Rule A audit aggregator. No tools/files.

Inputs: sealed family_atlas_v01.tsv plus one private per-occurrence TSV for one family. Rule A means >=1 same-alternate parental read at MAPQ>=50/BQ>=30. Per-occurrence input has family_id, tier (primary or strict_mapq60), unique occurrence_key, frozen_strand_survivor, and either rule_a_flag or rule_one_read_mapq50_bq30. Header-only is valid when canonical pre-strand counts are zero.

Fail closed on family/count/hash mismatch, missing/extra/duplicate rows, bad tier/boolean. Output only coordinate-free family-tier aggregates: canonical pre-strand, flagged, unflagged, canonical survivors, survivor flagged/unflagged; plus provenance, hashes, atomic marker, biology=NO. Never mutate caller or atlas. List the essential invariants and 6 unit tests.
