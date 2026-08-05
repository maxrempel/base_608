# Concise ALU‑DeNovo‑1 Verifier Design

## Implementation Checklist (deterministic, read‑only, fail‑closed)

1. **Handoff atomic marker**  
   Verify handoff / `atomic.marker` exists and its content matches the expected SHA256 of the manifest file.

2. **Manifest loading**  
   - Read the handoff manifest (200‑entry, absolute paths + expected SHA256).  
   - Compute its own SHA256; compare with the digest provided alongside.  
   - Fail on format error, duplicate path, or path not beneath the `family_root`.

3. **Chromosome inventory**  
   - List all directories under `family_root`.  
   - Exactly `chr1`–`chr22` must exist; no extra, no missing.  
   - For each chromosome, required files: `primary_summary.json`, `strict_summary.json`, `candidate.tsv` (single TSV for *both* tiers?  
     The handoff per‑chromosome structure may separate `primary.tsv` and `strict.tsv`; the task says “candidate TSV”, singular.  
     Assumption: one `candidate.tsv` per chromosome containing both tiers flagged by a `tier` column, or two files.  
     For verifier design, treat as two logical candidate TSVs per chromosome
