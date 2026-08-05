# Alusieve attrition evidence inventory v01 — result.md

## 0. Session boundary (observed fact)

This run had **no filesystem or tool access**. No project file contents, line numbers, or table columns were read. All path names below are taken verbatim from the task packet. Items marked **[packet]** are observed from the task text; everything else is **[inference]** and must be confirmed by a filesystem-enabled read-only pass before the audit relies on it.

Required governing-plan read (not performed, no tool available):

- `C:\claude_base\projects\XG1\kenefick\paper_repro\deployment\aluya5_family_stream_v01\ALU_DE_NOVO_1_BASELINE_AND_ATTRITION_PLAN_v01.md`

---

## 1. Retained columns/files per waterfall stage

**[inference]** The waterfall stages in the plan are: annotated copies → accepted copies → callable positions → child-supported alleles → parent-observed alleles → parent-absent loose leads → strand survivors → locus-review survivors.

**[inference]** Expected evidence roots encode the stream: `aluya5_exact_copy_npa_v01` for copy-level retention and NPA (no-parent-allele) decisions; `aluminum_atlas_v01` for locus-level evidence.

| Stage | Likely evidence root | Likely retained columns/fields | Status |
|---|---|---|---|
| Annotated copies | `aluya5_exact_copy_npa_v01` | copy ID, read ID, alignment start/end, clipping flags, start, duplicate flag, allele calls, quality | **[inference]**, verify headers |
| Accepted copies | `aluya5_exact_copy_npa_v01` | pass/fail flags, filter reason, mate status, mapping quality | **[inference]**, verify filter fields |
| Callable positions | `aluminum_atlas_v01` | locus ID, depth, coverage, reference/major/minor bases, strand counts | **[inference]**, verify depth columns |
| Child-supported alleles | `aluminum_atlas_v01` | allele, child count, child fraction, strand-support per allele | **[inference]**, verify strand columns |
| Parent-observed alleles | `aluminum_atlas_v01` | maternal allele counts, paternal allele counts, combined parent count | **[inference]**, verify parent columns |
| Parent-absent loose leads | `aluya5_exact_copy_npa_v01` and/or atlas | “NPA” leads, loose-lead flag, at least one supporting child copy | **[inference]**, verify NPA flag |
| Strand survivors | `aluminum_atlas_v01` | per-lead forward/reverse counts, strand-summary pass | **[inference]**, verify strand fields |
| Locus-review survivors | `aluminum_atlas_v01` | review tier, manual/automated call, final call status | **[inference]**, verify final-call fields |

**Action required before audit:** list actual file names and header rows under both roots; map each column to one stage. No column names can be cited yet.

---

## 2. Candidate and near-miss evidence files

**[inference]** Files containing real candidate or near-miss reads, mates, local alignments, alternate mappings, clipping, starts, duplicates, parental allele counts, or locus-depth evidence are expected primarily under:

- `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real\aluminum_atlas_v01`
- `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real\aluya5_exact_copy_npa_v01`

Expected evidence categories and the kind of file that would contain them:

| Evidence category | Expected file type | Location (inferred) |
|---|---|---|
| Candidate reads / near-miss reads | BAM/FASTQ or read-level TSV | under `aluminum_atlas_v01` |
| Mate evidence | paired-read records, mate flags | under `aluminum_atlas_v01` or copy root |
| Local alignments / alternate mappings | SAM/BAM alignments with CIGAR, MAPQ, XA tags | under `aluminum_atlas_v01` |
| Clipping and starts | alignment starts, soft/hard clip lengths | copy root or atlas per-read table |
| Duplicates | duplicate-flag fields, PICARD/UMI columns | copy root |
| Parental allele counts | parent count columns or parent BAM-derived tables | atlas |
| Locus depth | depth/coverage columns or depth-per-locus table | atlas |

**[observed gap]** No evidence files were actually enumerated in this session. A directory listing of both roots is the first required step.

---

## 3. Frozen threshold definitions and below-threshold retention

**[inference]** Frozen thresholds are expected in one or more of:

- the governing plan (`ALU_DE_NOVO_1_BASELINE_AND_ATTRITION_PLAN_v01.md`)
- the frozen caller (must not be edited)
- any threshold-calibration output under `outputs\real`

Candidate threshold types (to be confirmed):

| Threshold | Likely definition | Needed for audit |
|---|---|---|
| Copy acceptance | min mapping quality, min length, clipping cap | confirm value and where defined |
| Callable position | min depth, min base quality | confirm value |
| Child-support | min child allele count/fraction | confirm value |
| Parent-observed exclusion | min parental allele count to call “observed” | confirm value |
| Strand survival | min per-strand reads and min strand ratio | confirm value |
| Locus review pass | final review tier/call rule | confirm value |

**Below-threshold per-site retention:** **[inference]** The audit needs per-site values below each threshold (e.g., depth 3 where min-depth is 10) to build attrition curves. Whether such values were retained is **unknown** and must be verified from the atlas/copy tables. If only pass/fail flags were kept, the below-threshold raw evidence is a gap.

---

## 4. Prior spike-in truth and recovery outputs

**[inference]** The task packet directs a narrow search under:

- `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real`

for earlier NPA spike-in, real-read, alignment, dropout, candidate, and threshold-calibration outputs.

Known from the packet:

- `aluya5_exact_copy_npa_v01` name suggests an earlier “exact copy NPA” run that may contain spike-in truth attached to exact copy IDs.
- The word “spike-in” appears in the packet’s search list, implying prior synthetic-allele recovery runs exist or were planned.

**[inference]** Required recovery metrics for each spike-in run:

| Metric | Needed to know |
|---|---|
| Truth type | synthetic allele inserted into which background |
| Pipeline exercised | was the complete frozen pipeline invoked, or only a sub-step |
| Recovery | true-positive rate, false-positive rate per dilution |
| Locus/depth profile | at what depths spike alleles were recovered |
| Threshold calibration | which thresholds were tuned from which spike runs |

**Observed gap:** No spike-in output path or result table was provided in the packet; the existence, completeness, and frozen-pipeline coverage of prior spike-in runs is **unverified**.

---

## 5. Reusable scripts for audit-only computations

**[inference]** The `scripts` root is:

- `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts`

Expected reusable script categories (names not read):

| Audit need | Expected script category | Reuse condition |
|---|---|---|
| Threshold grids | threshold-sweep / calibration scripts that do not write production outputs | run read-only; must not alter frozen caller |
| Parental-dropout probabilities | probability or likelihood scripts using parental allele counts | read-only, no production writes |
| Repeat-mapping separation | alignment/read-separation utility (e.g., alternate-mapping resolver) | must not change frozen caller |
| Spike-in recovery | recovery/evaluation script comparing truth calls to pipeline calls | safe if it only reads pipeline outputs |

**[inference]** Reuse is permissible only for audit-only computations that do not modify production outputs, thresholds, or the frozen caller. Scripts that write into `outputs\real` must be treated as evidence producers, not production.

---

## 6. Evidence gaps and minimal next computations

| # | Gap | Minimal read-only/audit-only next step |
|---|---|---|
| 1 | No file listing obtained in this session | Run directory listing (recursive) of `aluminum_atlas_v01` and `aluya5_exact_copy_npa_v01`, plus `scripts`, saving only a manifest; no production writes |
| 2 | Waterfall column mapping unknown | Read header rows of each TSV/table; produce a stage→file→column map |
| 3 | Frozen threshold values not cited | Extract threshold constants from plan and frozen caller; store in audit-only notes |
| 4 | Below-threshold per-site values unknown | Check whether atlas/copy tables retain sub-threshold depth/allele counts; if absent, flag as a permanent evidence gap unless raw intermediate files exist |
| 5 | Spike-in truth/recovery coverage unknown | Search `outputs\real` for NPA/spike-in/calibration outputs; for each, record pipeline steps invoked and recovery metrics |
| 6 | Candidate/near-miss read evidence not enumerated | Produce a read-level evidence index (BAM/FASTQ/TSV paths, read counts, filters applied) |
| 7 | Reusable script list unknown | List scripts, dependencies, and whether they write outputs; classify as audit-safe vs production-coupled |
| 8 | No line-number citations possible | After filesystem access, re-issue inventory with exact line/column citations |

---

## 7. Consolidated observed vs inferred statement

**Observed (from task packet only):**
- Governing plan path exists as named.
- Two evidence roots exist as named.
- Scripts root exists as named.
- A narrow search under `outputs\real` is the mandated search scope for prior spike-in/calibration evidence.
- The five audit questions are as listed.

**Inferred (must be verified):**
- All column names, file formats, threshold values, recovery metrics, and script capabilities above.

**No biological, medical, or clinical claims are made in this inventory.**

---

*Prepared as a read-only evidence inventory. No project files were edited; no thresholds were changed; no pipeline was run.*
