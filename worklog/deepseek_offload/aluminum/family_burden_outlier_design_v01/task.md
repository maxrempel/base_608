Design a deterministic, coordinate-free Aluminum atlas summary that converts the sealed family_atlas_v01.tsv into science-ready burden distributions and an outlier table. Return a concise implementation specification and edge-case checklist, not prose interpretation.

Inputs per complete family include family_id, completion_state, biological_interpretation, total_primary_callable_positions, total_primary_npa_leads, total_primary_strand_strict_leads, total_mapq60_callable_positions, total_mapq60_npa_leads, and total_mapq60_strict_survivors. The source atlas has an ATLAS_COMPLETE_v01.ok marker that pins build_manifest_v01.json and all output hashes.

Requirements:
- Verify the atlas atomic marker and every pinned hash before reading rows.
- Exclude incomplete families from distributions but retain no hidden zero conversions.
- Emit one row per complete family and tier (primary, strict_mapq60).
- Preserve callable denominator, loose/pre-strand count, strand-survivor count, both rates per billion callable positions, descending tied ranks, and empirical midrank percentiles.
- Add exact 95% Poisson/Garwood rate intervals for both counts, including count=0.
- Mark rank-based review priority without calling any family biological or Starseed.
- Emit distribution summaries by tier and metric: family count, zero-count families, total callable, total count, pooled rate, mean/median/Q1/Q3/max family rate.
- Preserve biological_validation=NO and scientific_gates_changed=false.
- Write README, TSVs, JSON provenance, SHA256SUMS, and an atomic completion marker.
- Output must contain no coordinates, read identifiers, phenotype, or participant role IDs.
- State deterministic tie handling and percentile formula exactly.
- Recommend validation tests and identify small-n pitfalls.
