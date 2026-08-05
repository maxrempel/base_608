# Strict RHtyper canonical comparison contract review

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Return at most 500 words. Review this prospective contract for loopholes.

Goal: compare two RHtyper 1.1 runs while raw files remain preserved. Missing or extra files, fields, rows, tables, evidence records, interpretations, or values fail.

Explicit file roles:
- Six RHD/RHCE variant TSV files: raw bytes must match.
- Two coverage TSV files: every value must match; only the `prefix` field may replace an exact validated old/new run-root prefix.
- Allele-ranking TSV: exact field set. `ID` may replace only an exact validated run-root prefix. Compare exact row multisets including allele identity, serialized likelihood text and exact Decimal value, comment, and multiplicity. `Index` order may differ only within groups whose serialized likelihood strings are exactly identical; otherwise Index must match.
- Bloodtyping TSV: same exact path rule. Compare exact rows/fields/multiplicity. Index relaxation only for exact serialized-score ties established in the full allele-ranking table.
- XLSX: deterministic stdlib ZIP/XML extraction of sheet names, cell coordinates, types, formulas, and displayed values. Same explicit path and tie rules as TSV. Missing sheets/cells fail.
- PDF: pinned pdftotext binary. Extract page-separated text. Only exact path tokens at schema-declared table positions may change; no global regex. Compare extracted scientific tokens/tables exactly. Missing pages/tables fail.
- PNG and exonCNV: raw bytes must match.
- stdout/stderr: required and raw hashes retained; diagnostic, not scientific equivalence. Only schema-declared path tokens and table blocks may be canonicalized; other changes fail.
- Preflight evidence JSON: exact counts, filters, state, interpretation, and hashes of inputs/tools. Run-local output hashes may be compared separately.

No tolerance, rounding, pseudocount, genotype import, truth use, or arbitrary string scrub. Schema/tool/allowlist hashes freeze before replay.

List only: (1) fatal loopholes, (2) missing exact checks, (3) recommended minimal corrections.
