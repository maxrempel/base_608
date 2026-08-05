# Task

Review the design for a final coordinate-free synthesis of a completed,
checksum-sealed PR26 technical audit. Return a compact specification and
scientific interpretation checklist, not code.

Frozen design:

- 4 survivor loci.
- 16 within-element callable negative loci.
- 16 cross-element callable negative loci.
- Survivor metrics use child reads supporting the candidate allele.
- Negative metrics use all primary-quality child reads at callable negative
  loci.
- No production rerun, cohort change, matching change, or gate change.
- Biological validation remains NO.

Available retained fields:

- per-read mapping quality, base quality, distance from read edge, total soft
  clipping, insert size, strand, pair orientation, duplicate flag, read group,
  library, platform, platform unit, flowcell, lane, SA/XA/NH-derived
  alternative-alignment flag;
- per-locus survivor and matched-negative medians/fractions;
- frozen batch and feature summaries.

Unavailable:

- complete CIGAR/internal insertion-deletion structure;
- aligned read-start coordinate;
- full-reference remap multiplicity.

Required final synthesis:

1. Exact survivor-versus-negative numerators and denominators for pair
   orientation, mapping quality, soft clipping, duplicate flag, and
   batch/read-group distributions.
2. Effect sizes that do not pretend reads are independent biological
   replicates. Keep locus-level direction/effect summaries primary; read-level
   counts are descriptive.
3. State what is estimable, noninformative by filtering, or structurally
   confounded.
4. Explain the structural mismatch between survivor candidate-support reads
   and negative all-primary reads.
5. Explain whether one pair-orientation or batch category can account for all
   four survivors.
6. Do not expose coordinates, read names, sample identifiers, or raw
   read-group labels.

Known frozen feature results:

- mapping-quality locus deltas: within median 0 (range -1 to 0), cross median
  +2.75 (range -10 to +19), consistent nonzero direction 0/4;
- soft-clip-fraction locus deltas: within median +0.0643 (range 0 to +0.2528),
  cross median +0.1382 (range -0.0442 to +0.3315), consistent direction 3/4;
- duplicate-fraction locus deltas: 0 in both strata for all 4;
- pair-orientation concentration: 3/4 survivor loci, but the same dominant
  orientation is shared by only 3/4 and orientation is identical to strand in
  the retained rows;
- read-group concentration relative to both negative strata occurs at 4/4
  loci, but the dominant read-group category differs at every survivor;
- library is constant across all loci;
- all 4 survivors are transitions, so transition-versus-transversion
  comparison is non-estimable within PR26.

Give the strongest safe conclusion and list any additional aggregate
calculation that is necessary before publication.
