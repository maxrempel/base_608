---
title: Aluminum audit parser, concise design
version: 02
date: 2026-07-31
last_editor: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Answer in at most 900 characters.

Design a minimal Python change for an atlas builder. It scans candidate TSVs
by `(family, tier, chromosome)`. Add parsing of versioned key/value files named
`handoff_v*/candidate_audit_v*.txt`. Supported row keys are exactly
`primary_retained_row_chrN` and `strict_prestrand_row_chrN`; map them to tiers
`primary` and `strict_mapq60`. Reject conflicting duplicate audits. Attach an
audit only when exactly one candidate row exists for that key; otherwise fail
closed. Derive conservative states only when the text explicitly says them:
reviewed, single-strand technical failure, parents alternate 0 in bounded
review, post-strand count 0, biology NO/not validated. Unmatched historical
rows remain not_reviewed. Preserve coordinate-free evidence provenance and do
not alter candidate tables. List five focused tests. No prose introduction.
