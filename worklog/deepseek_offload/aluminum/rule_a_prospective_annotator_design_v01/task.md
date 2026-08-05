Design a concise deterministic Python 3 companion-audit annotator for the Aluminum ALU-DeNovo-1 atlas. Do not access files or tools. Return only architecture, input/output schemas, invariants, and test cases, under 6,000 characters.

Requirements:
- Rule A is audit-only: same alternate allele in either parent, at least one read with MAPQ >=50 and base quality >=30.
- Input 1 is the sealed Aluminum family_atlas_v01.tsv.
- Input 2 is one private per-occurrence Rule A TSV for one newly ingested family. It may use either rule_a_flag or rule_one_read_mapq50_bq30 and must include tier plus frozen strand-survivor state. It can contain private loci, but outputs must be coordinate-free.
- The private TSV must cover every canonical parent-absent pre-strand row for both primary and strict_mapq60 tiers, including zero-row families through a header-only file.
- Verify canonical counts exactly. Fail closed on duplicate occurrences, missing rows, extra rows, unknown tiers, family mismatch, ambiguous booleans, or atlas/source hash problems.
- Output one coordinate-free aggregate row per family+tier: canonical pre-strand count, flagged/unflagged, canonical strand survivors, survivor flagged/unflagged. Preserve canonical counts; biology=NO.
- Emit provenance with hashes, README, SHA256SUMS, and atomic marker. No production or caller mutation.
- Propose unit tests for full coverage, zero rows, duplicates, mismatch, and survivor preservation.
