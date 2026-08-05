Draft and critically review a lossless one-pass replacement for the analysis stage of:
C:\claude_base\projects\XG1\kenefick\paper_repro\scripts\analyze_aluya5_exact_copy_npa_v01.py

The current Python program:
- Loads exact AluYa5 RepeatMasker elements for one chromosome.
- Aligns each fixed reference element to the 281-base AluYa5 consensus.
- For every accepted element, independently calls pysam.AlignmentFile.pileup over that element for father, mother, and child.
- It is run twice: primary thresholds mapQ 30/baseQ 25, then strict thresholds mapQ 60/baseQ 30.
- pileup uses truncate=True, stepper="samtools", ignore_overlaps=True,
  ignore_orphans=True, max_depth=10000.
- It excludes deletions, refskips, secondary, supplementary, duplicate, QC-fail,
  non-ACGT bases, and records mapping quality, base quality, read-edge distance,
  strand, and query name.
- Candidate rules and all output fields must remain unchanged.

One-pass design:
1. Map each reference AluYa5 element to consensus once.
2. Make the union of all mapped genomic positions from accepted elements.
3. For each trio member, call pileup only once across the chromosome span at the
   LOWER thresholds, retaining observations only at wanted positions.
4. From the same stored observations, derive two evidence views:
   primary mapQ>=30/baseQ>=25 and strict mapQ>=60/baseQ>=30.
5. Evaluate both tiers with the original exact depth, child fraction, parental
   absence, strand, direction, and output rules.
6. Write two output directories matching the original primary and strict files.

Benchmark target:
- PR26 chromosome 5, because frozen primary and strict outputs each contain the
  same one candidate.
- Existing chromosome-specific CRAM inputs are retained on Asto.
- Do not modify the frozen v01 script or production launcher.

Important equivalence hazards to analyze:
- pysam overlap suppression and base-quality mutation.
- CRAM single-iterator behavior.
- element overlap and positions belonging to more than one annotation.
- exact Counter/field ordering and attrition counts.
- strict evidence must be a true subset of primary evidence.
- output path differs and should be normalized in comparison.
- old chunk extraction may contain duplicate read records; benchmark uses the
  exact same retained CRAMs, so those records must not be silently deduplicated.

Return concise implementation guidance plus a complete proposed Python v02
script. The v02 script must be standalone, must not change thresholds, and must
fail if the two threshold definitions are not nested.
