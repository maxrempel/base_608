# OMEGA GRCh37 wrapper regression review

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Return at most 900 words. Review this frozen engineering-regression design; do not write executable code.

- New immutable wrapper must differ from production v01 only by explicitly binding frozen `omega_junction_v02.py`; reference is sealed hs37d5 and the sole exclusion mask is sealed numeric genomicSuperDups BED. No GIAB Tier1 mask and no third clean BED.
- Run exposed controls only: retained 100-bp and 5000-bp synthetic PAFs; 32 old exposed HG002 assemblies mapped to sealed hs37d5; a protected 3-real/3-sham retained panel; repeat one exposed coded smoke twice.
- Old and v02 parsers receive identical inputs and arguments. Preserve denominators and every failure; no threshold tuning. Stop before the new 96-row blind panel.
- Public output is aggregate only. Private tables may hold exposed per-code results but no new panel truth.

Provide exactly four compact sections:
1. Minimum harness stages.
2. Checks proving no semantic change except parser binding.
3. Public aggregate and private per-code TSV column lists.
4. Ten highest-risk pitfalls, including PAF cs tags, output-schema differences, deterministic normalization, reference-build assertions, and truth leakage.
