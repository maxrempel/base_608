# Task

Review this bounded diagnostic design for logical leakage or unfair negative-control handling.

Context: three prespecified accepted real loci and three deterministic nearby shams already have
fresh minimap2 CIGAR-bearing PAF alignments for all assembled contigs. Production OMEGA selects
the longest alignment per contig, then applies fixed gates: anchor at least 100 bases, terminal
overhang at least 30 bases, end slack at most 20 bases, and grouping within 50 bases.

Candidate diagnostic only: for every contig genome-wide, inspect all existing PAF alignments,
retain alignments that independently encode a qualifying terminal event or internal insertion
under those same gates, then choose the longest aligned-query candidate (map quality and input
order as deterministic ties). Apply this uniformly to all contigs before checking either signal
or sham windows. Do not use locus coordinates during alignment selection. Report signal
locus-window, junction-class, exact-coordinate/payload recovery and sham false positives.

Question: Is this a fair diagnostic of secondary/supplementary representation, and what exact
limitation must accompany it? Return a compact review only.
