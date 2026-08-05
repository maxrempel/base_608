# Task: Concise verifier design

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

Give a concise implementation checklist, data model, and 10 highest-value tests for a deterministic Python verifier of one ALU-DeNovo-1 family handoff. Do not write full code. Maximum 1,500 words.

Inputs: family root, family ID, output root. Tree has exactly chr1..chr22. Each chromosome has primary and strict summary JSON, candidate TSV, completion markers, provenance, and checksums. Handoff has a 200-entry absolute-path SHA256 manifest, its digest, metadata key-values, per-chromosome counts TSV, and atomic marker.

Verifier must fail closed on: missing/extra chromosomes; malformed/duplicate manifest paths; any hash failure; chromosome checksum failure; inconsistent family/role/chromosome; unexpected threshold; negative or irreconcilable attrition; candidate TSV row count not equal to summary pre-strand count; strict_read_support true count not equal to summary post-strand count; handoff count contradiction; duplicate/conflicting biological keys within a tier. Metadata omissions are reported, contradictions fail. Cross-tier exact overlap is counted, not treated as a duplicate.

Coordinate-free outputs: aggregate verification JSON; candidate audit text with tier/chromosome counts, strand survivors, parent-alt count distribution, child read/strand/MAPQ/base-quality/depth ranges; provenance; checksums; atomic marker. Never print coordinates/read IDs. Biology remains NO. Source is read-only; no rerun or gate change.

1377 expected aggregate: 22 chromosomes, 200 manifest entries; primary rows 5 on chr4=1, chr6=2, chr12=1, chr13=1; primary strand survivors 4; strict row 1 on chr4 and it survives; exact cross-tier overlap 1; all six parent_candidate_reads=0; one primary row is reverse-only. Handoff metadata gives table/pre-strand counts but omits post-strand and parental totals.
