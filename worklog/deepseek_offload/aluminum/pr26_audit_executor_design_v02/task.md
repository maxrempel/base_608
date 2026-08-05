# PR26 audit executor compact review v02

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Return at most 900 words. Review this fixed executor design; do not redesign
the science or draft code.

The executor must verify sealed sources, then read four frozen PR26 strand
survivors and zero loose non-survivors. Existing chromosome production cannot
be rerun.

For each survivor it maps the existing AluYa5 annotation with the unchanged
production alignment and considers annotation-derived positions in deterministic
order. It selects four primary-callable within-copy negatives and four
same-chromosome, different-copy negatives. Callability is the unchanged
mapping-quality 30, base-quality 25, trio depth 12 through 80 gate. All existing
primary and strict candidate positions are excluded globally. Within-copy
ranking is consensus distance then frozen SHA-256. Cross-copy matching fixes
repeat strand, identity bin, coverage bin, reference base, consensus base, and
child plus combined-parent depth; only depth, then consensus base, then
reference base may relax. The executor queries indexed CRAMs in sorted order
and stops a stage after the first four eligible loci, so it never performs a
chromosome-wide pileup. Negatives are unique across survivors.

At four survivors and 32 negatives it runs single-locus indexed pileups at
primary 30/25 and strict 60/30. It records exact trio counts and private
read-level mapping/base quality, edge distance, strand, soft clips, insert
size, pair orientation, flags, RG/library/platform/platform-unit, parsed
flowcell/lane, mate placement, and SA/XA/NH. Full-reference remap multiplicity
is explicit unavailable unless already retained. Child repeat-to-1 kb-flank
depth is computed once per selected repeat copy and cached.

Outputs are private locus/read/matching/feature tables, hashes, manifest, and
atomic marker plus a separate coordinate-free summary. Shared mechanism needs
the same predefined nonzero feature direction in at least three of four
survivors against both negative strata, with effect and exact small-sample
uncertainty. Batch collinearity becomes
`shared_mechanism_not_separated_from_batch`. Reads are not biological
replicates. No gate change, rerun, or biological claim.

Give:

1. PASS or FAIL.
2. Five most dangerous implementation edge cases.
3. Minimum tests required before handing to Ben.
