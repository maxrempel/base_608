# Task: Design a fail-closed Aluminum family handoff verifier

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

Draft concise Python 3 code or a precise implementation design for a reusable verifier of one retained ALU-DeNovo-1 family handoff. It must be deterministic, read-only, and fail closed. The caller supplies `--family-root`, `--family-id`, and `--output-root`.

Expected family tree:

- `chr1` through `chr22`, each with `complete_v01.ok`, `checksums_v01.sha256`, `provenance_v01.txt`, `primary_v01/{npa_summary_v01.json, child_only_candidates_v01.tsv, complete_v01.ok}`, and `strict_mapq60_v01/{same three files}`.
- `handoff_v01/{manifest_v01.sha256, manifest_v01.sha256.digest, handoff_metadata_v01.txt, chromosome_counts_v01.tsv, FAMILY_ALUMINUM_HANDOFF_COMPLETE_v01.ok}`. Exact marker basename may begin with the family ID.

Required verification:

1. Require exactly chr1..chr22 and reject extra `chr*` directories.
2. Parse the handoff manifest. Require unique absolute source paths, exact 64-hex hashes, expected family result prefix, and verify every mapped local file byte-for-byte. Verify the digest file equals the manifest SHA256. Record entry count.
3. Independently verify each chromosome checksum file and completion markers.
4. Parse all 44 summary JSON files. Require family ID/chromosome/roles consistent, unchanged expected primary and strict thresholds, and reconcile annotation/accepted/mapped/callable attrition as nonnegative. Sum candidate_count_before_strand_filter and strict_candidate_count separately by tier.
5. Parse all 44 candidate TSVs. Require exact family/role/chromosome fields, row counts equal each summary's pre-strand count, and strict_read_support true-row counts equal each summary's post-strand strict_candidate_count. Preserve tier separation.
6. Reconcile `chromosome_counts_v01.tsv` and `handoff_metadata_v01.txt` against actual rows and summaries. Metadata omissions should be recorded as omissions; numeric or label contradictions are hard errors.
7. Detect duplicates within each tier by exact biological key (assembly, chromosome, element, position, child allele), exact cross-tier overlap count, and conflicting same-key records. Do not print coordinates or identifiers in the coordinate-free report.
8. Summarize candidate evidence without coordinates/read IDs: per tier and chromosome, row count, strand survivors, parent_candidate_reads distribution, child read support, forward/reverse balance, MAPQ/base quality, depths, and whether parental evidence is bounded zero or not assessed. This is technical screen evidence only, biology=NO unless explicitly validated elsewhere.
9. Write coordinate-free `verification_summary_v01.json`, `candidate_audit_v01.txt`, `provenance_v01.json`, `SHA256SUMS_v01.txt`, and atomic `HANDOFF_VERIFICATION_COMPLETE_v01.ok` only after every hard check passes. Keep any detailed private internal table separate and do not include coordinates in retained reports.
10. Never alter source files, rerun production, change thresholds, or treat missingness as zero.

Family 1377 observed aggregate facts for test expectations: 22 autosomes; 200 manifest entries; primary table rows 5 across chr4=1, chr6=2, chr12=1, chr13=1; primary strand survivors 4; strict table rows 1 on chr4; strict strand survivors 1; exact cross-tier overlap 1; all six rows have parent_candidate_reads=0; one primary row has all ten child alternate reads on the reverse strand; biology=NO. Handoff metadata reports the pre-strand/table counts but omits post-strand and parental counts.

Return implementation advice/code under 10,000 characters. Focus on correctness traps and test cases.
