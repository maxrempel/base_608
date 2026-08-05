# Aluminum atlas builder design review

Design a deterministic incremental population-atlas builder for the existing
ALU-DeNovo-1 retained outputs. Return a compact implementation specification,
test plan, and scientific safeguards. Do not write prose for participants.

Context:

- Aluminum is the cumulative atlas layer for a planned 600-trio public-family
  expansion.
- It must consume retained results only and must never rerun or redefine the
  frozen ALU-DeNovo-1 caller.
- Current retained root:
  `projects/XG1/kenefick/paper_repro/outputs/real/aluya5_exact_copy_npa_v01`
- Existing cumulative TSV columns:
  family_id, child_id, mother_id, father_id, population, superpopulation,
  chromosome, annotation_elements, accepted_elements,
  primary_callable_positions, primary_child_supported_alleles,
  primary_seen_in_parent, primary_npa_leads, primary_strand_strict_leads,
  mapq60_callable_positions, mapq60_child_supported_alleles,
  mapq60_seen_in_parent, mapq60_npa_leads, mapq60_strict_survivors.
- Production layouts vary historically. Candidate files can be directly under
  a chromosome directory as
  `primary_child_only_candidates_v01.tsv` and
  `strict_mapq60_child_only_candidates_v01.tsv`, or under
  `primary_v01/child_only_candidates_v01.tsv` and
  `strict_mapq60_v01/child_only_candidates_v01.tsv`.
- Candidate columns include family/sample metadata, exact element, chromosome,
  genomic and consensus positions, bases, direction, child support/fraction,
  parent reads, strand counts, quality summaries, trio depths/counts, alignment
  identity, and coverage.
- The exact recurrence key is assembly + chromosome + element + genomic
  position + child allele. Assembly is GRCh38DH/hg38 for current production.
- A family is complete only with all chr1-chr22 rows. Incomplete families may
  appear in chromosome tables but must not enter complete-family rates.
- Strict and primary tiers were computed separately and strict is not assumed
  to be a literal subset.
- Missing metadata must be `not_available`, not inferred.
- Candidate biological state is separate from technical screening. Default
  biological interpretation is `not_validated`; zero candidates means
  `none_observed_under_screen`, never biological absence.
- Required outputs should include:
  1. admitted chromosome table with denominators and completion state;
  2. complete-family summary;
  3. candidate occurrence registry for both tiers;
  4. exact-key recurrence table;
  5. population/superpopulation summary with explicit denominators;
  6. machine-readable build manifest, source hashes, and validation report;
  7. concise PRELIMINARY human report.
- Writes must be atomic and repeatable. Duplicate historical copies of the same
  family/chromosome must be detected and either proven identical or fail closed.
- Current completed cohort is small (10 families); no significance claims or
  Starseed comparison belongs in this atlas build.

Please recommend:

1. Exact output schemas and key invariants.
2. Deterministic discovery/admission rules robust to the two layouts.
3. Duplicate/conflict handling.
4. Scientific summaries that are meaningful now and scale to 600 trios.
5. Unit/integration tests, including synthetic duplicate conflict and
   incomplete-family cases.
6. Common statistical or interpretive mistakes to prevent.

Keep the response under 7,000 characters.
