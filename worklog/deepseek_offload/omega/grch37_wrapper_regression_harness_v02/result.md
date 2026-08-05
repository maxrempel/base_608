## 1. Minimum harness stages

- Validate sealed inputs: hash `hs37d5`, the numeric genomicSuperDups BED, all synthetic PAFs, and the 32 HG002 PAFs; reject any missing or altered file.
- Run the old v01 wrapper and the new v02-binding wrapper with identical command-line arguments, environment, working directory, temp paths, and input streams. Apply to: 100-bp synthetic PAF, 5000-bp synthetic PAF, 32 mapped HG002 assemblies, and the protected 3-real/3-sham panel.
- Capture all raw outputs, stderr, exit codes, warning counts, and per-code TSVs before any aggregation or normalization.
- Repeat one exposed coded smoke test twice, from clean independent directories, and compare both runs to each other and to the main runs.
- Run a differential comparator: canonicalize and compare old/new per-code outputs row-by-row, including denominators, failure rows, and failure strings.
- Aggregate only at the public layer; never place per-code detail into public output.

## 2. Checks proving no semantic change except parser binding

- Compare the wrapper source diff: the only allowed change is the explicit binding/import of the frozen `omega_junction_v02.py` module.
- Assert the loaded parser is exactly that frozen file by path and content hash; also check for stale `__pycache__` or shadowed modules.
- For every control, assert old and new runs produce identical per-code TSVs after stable sorting and canonicalization.
- Assert identical exit codes, stderr, warnings, failures, and denominator counts; every failure in old must appear in new with the same code and reason.
- Assert no threshold, default, or config parameter changed: same CLI flags, same environment, same reference path, same mask path.
- Assert all inputs are validated as hs37d5: PAF target names, contig set, and BED coordinates must match the sealed reference; no hg38 or alt-containing PAFs are accepted.
- Assert the only loaded exclusion mask is the sealed numeric genomicSuperDups BED; log absence of GIAB Tier1 and any third BED.
- Assert protected and blind panel truth never appears in private outputs, and that the regression stops before the 96-row blind panel.

## 3. Public aggregate and private per-code TSV columns

Public aggregate TSV columns:

`run_id | parser_version | control_group | control_id | n_input | denominator | n_failed | n_passed | pass_rate | mean | median | sd | min | max`

This is aggregate only; no per-code, per-sample, or per-locus rows are public.

Private per-code TSV columns:

`run_id | parser_version | sample_id | control_type | code | code_description | chromosome | start | end | ref | alt | raw_cs | filter_status | denominator | failure_flag`

No new panel truth column, no protected status column, and no blind-panel rows are written.

## 4. Ten highest-risk pitfalls

1. **PAF cs tags**: v02 may parse `cs` differently (e.g., match length vs substitution/deletion representations). Only comparing final junction codes can hide changes in cs decoding. Compare raw `cs` strings as a regression artifact.
2. **Output-schema differences**: v01 and v02 may emit columns in different order, use different names, or change coordinate systems. Assert identical schema before comparing values.
3. **Deterministic normalization**: Row order, float formatting, `NA`/`NaN` spellings, hash seed, and locale can make identical runs look different. Canonicalize and sort before comparison; set `PYTHONHASHSEED`.
4. **Reference-build assertions**: Shared contig names can hide hg38 or alt-aligned PAFs. Check target names, MD5 of the reference header, and
