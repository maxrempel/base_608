# OMEGA GRCh37 wrapper regression harness draft

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Draft a compact Bash or Python regression harness specification for an already authorized, truth-free/exposed OMEGA engineering regression. Do not access tools or files; reason only from this packet.

Frozen facts:

- New wrapper changes only parser binding from omega_junction.py to omega_junction_v02.py.
- v02 parser SHA256: e42c5a68ecddc8506a53631ca8569f1fb4111f35e71d36897bc0734129226c29.
- Reference is sealed hs37d5 FASTA and asm5 MMI; mask is sealed numeric 39,747-row hg19 segmental-duplication BED. No GIAB Tier1 detector mask.
- Thresholds: anchor_min 100, overhang_min 30, locus_win 50 where existing real-panel diagnostics use it; detector thresholds otherwise unchanged.
- Synthetic controls: two retained PAFs, known insertion lengths 100 and 5000. Existing locked evaluator script reconstruct_insertion_length_v01.py must be rerun unchanged; expect 100 exact and 5000 unresolved.
- GIAB32: 32 exposed/unblinded public HG002 controls. Existing retained MEGAHIT final.contigs.fa exists for each coded HG2LEN001..032. Map each assembly to sealed hs37d5 MMI with minimap2 asm5/cs, then run both old and v02 junction parsers with identical arguments. Record per-code candidate/header validity, verdict counts, representation, inserted_length_bp, parser attrition, output hashes, and old-vs-v02 differences. Do not use these old controls as new readiness evidence.
- Repeated coded smoke: run HG2LEN001 mapping/parsing twice into separate dirs and require identical normalized outputs/hashes.
- Protected real/sham diagnostic: existing Asto panel has three real and three sham loci, retained PAF/contigs, private paths. Re-run old and v02 parser on the exact retained PAF/contigs with identical args; report only deidentified aggregate window/junction/exact/payload recovery and sham accepted count. Do not copy coordinates/read IDs to Git or output.
- Preserve every failure and denominator. Never tune thresholds. Stop before the new 96-row blind panel.

Return:

1. A minimal harness structure and pseudocode/commands.
2. Exact checks needed to prove no semantic changes outside parser binding.
3. A compact TSV schema for public regression summary and a private per-code table.
4. Likely pitfalls, especially PAF cs-tag requirement, old/new output schema difference, reference-build separation, deterministic normalization, and preventing truth leakage.
