# Task

Review and refine a cumulative population-atlas schema for an exact-copy
AluYa5 trio screen. Return a compact implementation specification, not code.

The frozen discovery method must not change. Each chromosome result currently
contains:

- family, child, mother, father, population, superpopulation, chromosome;
- annotated, alignment-rejected, and accepted AluYa5 copies;
- mapped positions, positions rejected by depth, callable positions;
- child-supported alleles, alleles seen in a parent;
- loose candidate count and strict candidate count;
- a candidate table with locus, genomic position, child base, direction, and
  read-support text;
- provenance and checksums.

The cumulative atlas must remain interpretable across a planned 600 trios. It
must preserve:

1. frozen denominators per chromosome and per trio;
2. loose-to-strict attrition;
3. validated read evidence without turning technical evidence into biology;
4. recurrence by exact locus and allele;
5. parental dropout and possible mosaic evidence;
6. ancestry, batch, and sequencing-platform fields only when legitimately
   available;
7. family-level provenance and completion state.

Propose the smallest durable set of tab-separated tables and required columns.
Define exact recurrence keys. Define controlled status values for validation,
dropout, mosaicism, and missing metadata. Explain what can be generated
automatically from current summaries and what requires a curated registry.
Include five fail-closed validation checks. Keep the answer under 1,200 words.
