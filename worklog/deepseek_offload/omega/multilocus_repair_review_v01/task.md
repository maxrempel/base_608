Review this bounded positive-control repair design for scientific or fail-closed errors. Return only a compact checklist of concrete risks or corrections.

Context:
- A frozen three-locus OMEGA insertion pilot uses three distinct callable loci and one 20+20 synthetic spike plus one sham per locus.
- Attempt 1 is preserved. It produced 0/3 exact recoveries and 0/3 sham false positives. Two spike alignments had internal 120 bp insertions but canonical coordinates shifted by 1-3 bp and extracted sequences rotated because of boundary microhomology. The third assembled only a one-sided fragment.
- Corrected attempt keeps the exact same three loci, detector thresholds, parser omega_junction_v02, and bounded 1401 bp reference mapping.
- Each corrected 120 bp payload is deterministic and accepted only if its last base differs from the reference base immediately left of the breakpoint and its first base differs from the reference base immediately right. This prevents single-base indel boundary shifts.
- Each of 20 left reads contains 30 bp left reference anchor plus the full 120 bp payload; each of 20 right reads contains the full payload plus 30 bp right reference anchor. Twenty ordinary 150 bp flank reads per side remain. Sham contains no synthetic reads.
- Acceptance is exact and per locus: exactly one internal-cigar INSERTION_2sided call, inserted length 120, exact truth payload recovered once, truth payload present in a contig, exact zero-based coordinate, and no sham two-sided calls. All three loci and all three shams must pass.
- The original failed-pilot summary and attempt-1 public result are checksum-pinned inputs. Outputs and all mapping/reference/truth artifacts are checksum-manifested.
- No genome-wide scale-out, Omun threshold change, or correction factor.

Check especially: whether one-base boundary disambiguation is sufficient; whether the bridge-read geometry invalidates the narrow positive-control question; whether exact acceptance can accidentally pass a terminal half-chimera; and whether any failure evidence is overwritten.
