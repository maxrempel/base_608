# Task

Review this final bounded OMEGA diagnostic design for coordinate leakage, unfair sham handling,
or an invalid exact-payload claim.

Frozen inputs: three prespecified accepted real loci and three deterministic nearby shams. Whole-
chromosome assembly and candidate discovery are already complete and outcome-blind. This is only
post-discovery refinement.

For each frozen signal or sham position:
1. extract fixed 800-base left and right reference flanks;
2. map every retained chromosome contig independently to each flank with the same mapper/settings;
3. require both mappings on the same contig and strand, at least 100 aligned query bases per anchor,
   each mapping reaching its junction-facing flank edge within 20 bases, non-overlapping query
   anchors, and at least 30 query bases between anchors;
4. define the between-anchor query sequence as the candidate payload;
5. report recovery at the fixed locus and junction bridge, and exact support only if the inferred
   payload contains both complete accepted terminal payload proxies in compatible orientation;
6. apply identically to signal and sham windows. No production threshold or Omun endpoint changes.

Question: Is this a valid diagnostic, and what exact limitation must accompany it? Return only a
compact review.
