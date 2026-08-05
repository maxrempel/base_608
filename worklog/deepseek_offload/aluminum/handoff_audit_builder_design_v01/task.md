---
title: Aluminum handoff-audit ingestion design
version: 01
date: 2026-07-31
last_editor: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Review a deterministic Python atlas-builder change. Return a compact patch
design and edge-case/test checklist, not a full report.

Current behavior:

- The builder scans retained per-chromosome `child_only_candidates_v01.tsv`
  tables and produces candidate occurrences.
- It currently marks `read_review_state=audit_present` only when a directory
  containing `audit` sits under that chromosome directory; otherwise it says
  `not_reviewed`.
- `technical_interpretation` is always `not_assessed` and
  `biological_interpretation` is always `not_validated`.
- A corrected atomic family handoff instead has a coordinate-free
  `handoff_v02/candidate_audit_v02.txt` with key/value lines:
  `family`, `biology`, one or more keys like
  `primary_retained_row_chr7` or `strict_prestrand_row_chr6`, and `attrition`.
- Each row-specific value records child support, single-strand direction,
  parent alternate-read count, pre-strand count, and post-strand count.

Required behavior:

1. Discover versioned `handoff_v*/candidate_audit_v*.txt` files beneath the
   retained root without opening genomic inputs.
2. Parse only exact supported row keys; reject duplicate/conflicting audit
   claims for the same family/tier/chromosome.
3. Attach a matching audit to candidate occurrences by family, tier, and
   chromosome. Do not infer a coordinate match when a tier/chromosome has more
   than one retained row unless the audit format becomes coordinate-specific.
4. Preserve the audit text as coordinate-free evidence provenance, and derive
   only conservative categorical states: reviewed, single-strand technical
   failure, no alternate parent reads observed in this bounded review,
   post-strand removed, and biological validation NO/not validated.
5. Candidate rows without a matching audit must remain `not_reviewed`.
6. Keep old historical builds deterministic and schema-compatible. New columns
   may be appended, not reordered destructively.
7. Recommend focused tests for correct attachment, missing audit, conflicting
   audits, ambiguous multiple rows, and no candidate-table mutation.

Give implementation pseudocode or concise code fragments and flag any unsafe
inference.
