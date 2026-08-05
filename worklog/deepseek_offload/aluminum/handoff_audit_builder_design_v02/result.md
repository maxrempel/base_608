Add AuditLoader:

- Glob `handoff_v*/candidate_audit_v*.txt`; parse `key=value` lines. Accept only keys matching `^(primary_retained_row|strict_prestrand_row)_chr\d+$`; prefix maps to tier `primary`/`strict_mapq60`, suffix to chromosome. Unknown keys raise.
- Duplicate audit: same value idempotent; differing value raises Conflict.
- For each audit, find rows by `(family, tier, chromosome)`. If count != 1, fail closed.
- Derive state only from exact phrases: `reviewed`, `single-strand technical failure`, `parents alternate 0 in bounded review`, `post-strand count 0`, `biology NO`/`not validated`; otherwise leave `not_reviewed`.
- Return `{row_id: (state, source_file)}`; never mutate candidate tables.

Tests:
1. Conflicting duplicate audits rejected.
2. Identical duplicate audit accepted.
3. Exactly one row attaches mapped tier/state; zero/multiple rows fail closed.
4. Exact phrase maps to conservative state; unknown text stays `not_reviewed`.
5. Unmatched historical rows remain `not_reviewed`; tables unchanged.
