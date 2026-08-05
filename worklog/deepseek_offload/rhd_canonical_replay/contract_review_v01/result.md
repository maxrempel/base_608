(1) Fatal loopholes  
- Path replacement is unanchored: `prefix`/`ID` may be replaced anywhere the old run-root appears, without requiring a full field/token boundary, occurrence-count identity, or verification that the remainder of the field is unchanged.  
- Tie-based Index relaxation is underspecified: “groups whose serialized likelihood strings are exactly identical” has no defined group key, so duplicate rows with identical serialized text but different allele/comment cannot be matched deterministically.  
- Bloodtyping Index relaxation references the full allele-ranking table but no algorithm links bloodtyping rows to ranking rows; a missing or altered ranking table could invalidate the tie permission.  
- PDF determinism is not established by a pinned binary: pdftotext output depends on command flags, poppler configuration, fonts, locale, and library versions. “Schema-declared table positions” is prose, not a schema.  
- Preflight output hashes “may be compared separately” makes hash comparison optional, so changed run-local output hashes can pass review.  
- XLSX “same explicit path rule” is vague; stdlib XML extraction must canonicalize namespaces, attribute order, cell formula/cached-value pairing, hidden sheets, and OOXML relationships.  
- Raw files have no explicit role or manifest, so “raw files remain preserved” is not actually checked.

(2) Missing exact checks  
- Exact schema version/hash equality between old and new runs, including the frozen tool/allowlist hashes.  
- Exact file manifest and field-set validation for every TSV, XLSX sheet, PDF page, and stdout/stderr block before comparison.  
- Path-token boundary and occurrence-count checks, including a rule that path tokens appearing in comments, evidence JSON, or displayed cells fail unless schema-declared.  
- Explicit Decimal canonical form (e.g., exponent notation, `-0` vs `0`) distinct from serialized likelihood text.  
- Cross-file referential integrity: row counts, Index values, and tie groups in bloodtyping must be validated against the allele-ranking table.  
- XLSX hidden sheets/duplicate sheet names and cached formula/displayed-value mismatches.  
- Raw input file hashes and preservation evidence as mandatory preflight fields.

(3) Recommended minimal corrections  
- Freeze a machine-readable schema listing exact fields, path-typed cells, PDF table coordinates, and stdout/stderr block boundaries; compare schema hashes.  
- Replace only an exact validated run-root string appearing as an entire field or complete path
