# PR26 technical-audit executor design review v01

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Design-review a deterministic Python executor for an already-frozen,
coordinate-private repeat-element technical audit. Do not change cohorts,
matching, thresholds, or biological interpretation. Do not draft a report.

## Sealed inputs and ownership

- Private request contains exactly four primary strand survivors from family
  PR26 and zero primary loose non-survivors under the frozen gate.
- Production results already exist for chromosomes 1 through 22. The executor
  must not rerun whole-family or chromosome candidate detection.
- Existing accepted per-chromosome trio CRAMs and CRAIs are readable.
- Existing per-chromosome primary and strict candidate TSVs and atomic
  completion/checksum files are readable.
- Per-chromosome RepeatMasker JSON contains AluYa5 records with:
  genoName, genoStart, genoEnd, repName, strand.
- GRCh38DH reference and 281-base AluYa5 consensus are pinned.
- The production mapping method globally aligns each repeat copy to consensus
  and accepts identity >= 0.82 and coverage >= 0.75.

## Frozen negative selection

For each survivor:

1. Select four within-element callable negatives. Exclude every candidate
   position. Prefer the same reference base. Rank by absolute consensus
   coordinate distance, then SHA-256 of:
   `20260729|PR26|within|candidate_key|element|position`.
2. Select four cross-element callable negatives from another same-chromosome
   AluYa5 copy. Never relax chromosome, repeat strand, identity bin, coverage
   bin, callability, or candidate exclusion. Exact matching adds reference
   base, consensus base, and child plus combined-parent depth within the larger
   of 20 percent or three reads. Rank by SHA-256 of:
   `20260729|PR26|cross|candidate_key|element|position`.
3. If fewer than four cross-element exact matches are found, relax only depth,
   then consensus base, then reference base, recording each relaxation.
4. A negative may be used for only one survivor.

Primary callability is the unchanged production gate: mapping quality >= 30,
base quality >= 25, and father, mother, and child depth each 12 through 80.
Candidate exclusion uses all retained primary and strict candidate TSVs.

To avoid a production rerun, the executor may generate annotation-derived
candidate positions, sort them deterministically, query indexed CRAMs in that
order, and stop each selection stage as soon as the first four eligible loci
are proven. It must not perform a chromosome-wide pileup or candidate scan.

## Frozen measurements

At four survivors and 32 selected negatives, use single-locus indexed pileups
at both primary (30/25) and strict (60/30) thresholds. Preserve exact trio
depth/base counts. For child reads preserve candidate or non-reference base,
mapping and base quality, read-edge distance, forward/reverse, soft clipping,
insert size, paired orientation, duplicate/secondary/supplementary state,
RG, library, platform, platform unit, parsed flowcell/lane where available,
mate placement, SA/XA/NH tags, and unavailable states. Read names and
coordinates remain private.

For each unique selected repeat copy, optionally compute primary-gated child
depth across the repeat versus 1 kb flanks. Cache by repeat copy. Do not
treat reads as independent biological replicates.

## Output and execution rules

- Refuse nonempty output roots.
- Verify all sealed source hashes before reading private candidate rows.
- Write private selected-locus, read-metric, locus-metric, matching-attrition,
  and feature-summary tables plus manifest, SHA-256 list, and atomic COMPLETE
  marker.
- Write a separate coordinate-free deidentified summary.
- Explicitly report unavailable measurements.
- Shared mechanism is supported only if the same predefined feature has the
  same nonzero direction for at least 3 of 4 survivors against both negative
  strata, with effect size and uncertainty. If collinear with batch, report
  `shared_mechanism_not_separated_from_batch`.
- No production rerun, threshold change, or biological claim.

Return:

1. PASS or FAIL on feasibility.
2. The smallest sound executor architecture.
3. Exact edge cases that would silently violate the freeze.
4. A compact output schema.
5. Recommended tests, especially for deterministic ranking, relaxation,
   duplicate exclusion, overlap handling, unavailable fields, and sealing.
