# Task

Review the smallest deterministic OMEGA positive-control repair test. Return a
compact technical recommendation only; do not draft a broad redesign.

## Frozen facts

- The failed sensitivity pilot is preserved unchanged.
- One S2 support-20 synthetic locus was inspected coordinate-free.
- The 120-base synthetic payload occurs exactly in the single assembled contig.
- Minimap2 produced one primary PAF alignment with only 10 query bases before
  and 2 after the alignment, so the current terminal-overhang parser emitted
  zero junction rows.
- The assembled contig therefore represents a full left-anchor + internal
  insertion + right-anchor haplotype, not either terminal half-chimera expected
  by the current parser.
- The parser currently recognizes only unaligned query sequence at a contig
  end: anchor at query start plus right terminal overhang, or anchor at query
  end plus left terminal overhang. It does not inspect internal insertion CIGAR
  operations.
- The canonical mapper currently runs minimap2 `-x asm5` without `-c`.
- Frozen thresholds must remain: human anchor minimum 100 bases, foreign
  sequence minimum 30 bases, two-sided evidence required. No Omun correction
  factor is allowed.

## Proposed smallest repair test

1. Add `-c` only for the bounded corrected pilot so minimap2 emits `cg:Z`.
2. Add a versioned parser that preserves the existing terminal-half-chimera
   behavior and additionally recognizes an internal query insertion (`I`) of
   at least 30 bases only when at least 100 aligned query bases occur on both
   sides in the same primary alignment. Emit one two-sided insertion at the
   reference position preceding that `I`.
3. Run exactly one corrected S2 support-20 spike and one S2 sham through the
   unchanged detector/assembly and this versioned canonical mapper/parser.
4. Require exact payload presence in the insertion sequence, spike recovery,
   zero sham calls, hashes, and preserved failed-pilot provenance.

Assess whether this is the smallest scientifically valid test, flag coordinate
or strand/CIGAR pitfalls, and specify fail-closed acceptance checks. Do not
change thresholds or treat right-anchor overhang as insertion length.
