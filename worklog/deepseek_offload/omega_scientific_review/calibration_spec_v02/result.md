OMEGA/Omun Calibration Specification — Terse Outline

1. Calibration matrix axes and minimum cells
- Axis A: Sample source class: cultured public controls vs uncultured/blood-derived public controls.
- Axis B: Sequencing platform/chemistry pair; culture and platform are currently confounded in S2/S3.
- Axis C: XG1 Variant Discovery Manager version and parser configuration; pin version for every cell.
- Axis D: Normalization denominator: D10 callable bases.
- Minimum cells: at least 2 source classes × 2 platform pairs = 4 cells, each with ≥3 independent aggregate samples or batches. Existing 20 cultured public controls anchor the cultured row; uncultured/blood-derived cells are required before any S2/S3 comparison.
- Each cell must report: sample class, platform, VDM version, N, total D10 callable bases, total Omun, Omun/Gb, and per-sample range without identifiers.
- Omun definition fixed: clean deduplicated two-sided autosomal OMEGA detector loci, database-novel or known-rare <0.001, normalized by D10 callable bases.

2. Prespecified outputs
- Aggregate calibration table with all matrix cells, including the existing cultured control cohort: 143–224 Omun, 53.6989–84.0128/Gb, and S1 = 155 Omun, 58.1879/Gb.
- For each platform/VDM version, report a prespecified equivalence rule: uncultured/blood-derived Omun/Gb must fall within the cultured control min–max range after platform matching; if outside, calibration fails closed.
- Prespecified validation metrics:
  - GIAB known-length panel: exact calls, unresolved, false exact.
  - Synthetic positives: 100 bp reconstruct status; 5,000 bp positive unresolved status.
  - Real+sham retained panel: locus-window, terminal class, exact+payload proxy, sham rates.
  - Mapper diagnostic: number of real loci lost before parser formation, specifically when payload extension reduces opposite overhang below 30 bp.
  - Final local refinement: real, exact, and sham recovery rates.
- All outputs must be aggregate deidentified counts and rates. No participant identities, coordinates, read IDs, alignments, or sequences.

3. Acceptance criteria to reopen biology
- Reopen biological interpretation of S2/S3 low Omun only after:
  - The calibration matrix is complete with uncultured/blood-derived control cells and no missing platform/VDM cells.
  - Uncultured/blood-derived Omun/Gb overlaps the cultured control range on at least two platform pairs; no source-class effect or platform effect remains outside the prespecified equivalence margin.
  - Mapper diagnostic confirms no real loci are lost before parser formation when payload extension reduces opposite overhang below 30 bp.
  - Final local refinement recovers real positives and exact+payload proxy calls in the retained panel.
  - Exact GIAB panel is no longer 0/32 exact; 5,000 bp positives are no longer unresolved; real+sham retained panel no longer 1/3 and 0/3 for real classes while shams remain 0/3.
- Until then, any low Omun in S2/S3 is a calibration artifact or confounded measurement, not biological absence.

4. Fail-closed rules
- Do not interpret S2/S3 counts as biological absence; they are culture/platform-confounded.
- Do not launch production or issue any clinical/genomic interpretation from current calibration.
- Do not treat 0/32 exact GIAB calls, 30 unresolved GIAB loci, or 5,000 bp synthetic positive unresolved as acceptable.
- Do not accept the real+sham retained panel outcome as validated: real classes 1/3, terminal class 1/3, exact+payload proxy 0/3, while shams 0/3.
- Do not use 100 bp synthetic positive success as standalone evidence of full-length detection.
- Do not accept any VDM version change without rerunning the full calibration matrix.
- Any validation failure or missing calibration cell forces fail-closed status.

5. Smallest valid uncultured or blood-derived control comparison
- Minimum valid comparison: one aggregate cell of ≥3 unrelated public uncultured or blood-derived controls per platform, with the same pinned VDM version, same Omun inclusion rules, and each sample passing the same D10 callable-bases threshold used for cultured controls.
- No individual-level output; only pooled cell-level Omun and Omun/Gb.
- To resolve the culture/platform confound, the uncultured/blood-derived cell must be compared against a platform-matched cultured public control cell; unmatched comparison is invalid.
- Existing 20 cultured public controls are the cultured anchor where platform-matched.
- A single uncultured control sample is not sufficient; minimum 3 independent samples per platform cell, and 2 platform cells for an interpretable matrix.

6. Production needs for XG1 Variant Discovery Manager
- Preserve candidate OMEGA loci before parser formation; do not discard loci solely because payload extension reduces opposite overhang below 30 bp.
- Rework the parser/mapper handoff so real loci survive to local refinement; current mapper diagnostic shows real loci are lost before parser formation.
- Fix local refinement to recover real positives and exact+payload proxy calls while maintaining 0/3 shams; current refinement is 0/3 real, 0/3 exact, 0/3 shams.
- Add pinned versioning for VDM and parser configuration; record any change as a new calibration cell.
- Emit only aggregate Omun counts normalized by D10 callable bases, with no sequence-level or alignment-level artifacts.
- Do not enable production use until all fail-closed rules are cleared and acceptance criteria are met.
