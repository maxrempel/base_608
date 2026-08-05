# Scribe handover - milestone 2 (~172K tokens)
# session: 20260703_rmined_williamson_9bad91_a4a9a108
# cwd: C:\claude_base\.claude\worktrees\determined-williamson-9bad91
# written: 2026-07-03 13:11:32 by deepseek-v4-pro

# HANDOVER - X12B / Track-2: XG1 Paper Reproduction + Extension

## GOAL (Max's own words)
Reproduce and extend Max's XG1 paper: "genome-wide map of population-recurring alien genetic manipulation in humans" - use 1000-Genomes trios, find changes in a child not from either parent, then map where those changes recur across unrelated people ("hotspots"). The paper itself is at maxrempel.com (paper title: "Preliminary evidence of traces of alien genetic manipulation in humans").

## DECISIONS MADE + WHY
1. **Pipeline split with X11B** - X11B already claimed the extension lane (detection-method + genome-wide recurrence mapping). X12B proposed a clean interface: X12B builds the per-trio NPA detector and reproduces the chr3 positive control; X11B consumes that output to map recurrence. (Broadcast posted, awaiting X7A's confirmation.) *Why:* avoid duplicate work; each track member plays to existing claims.
2. **Paper identified** - viXra:2505.0194 (May 2025), "Preliminary evidence of traces of alien genetic manipulation in humans," found on starseedgenetics.com and viXra.org. Full PDF downloaded (665KB). *Why:* answers all 4 open questions and provides the exact method to replicate.
3. **Source code cloned** - `git clone https://github.com/maxrempel/xg1` into `C:\claude_base\projects\XG1\paper_reproduction_src\`. Core detector script: `20_NPASearch45v14_Chromosome_NPA_Scanner_...ipynb`. *Why:* Max's exact method is in these scripts; reusing them ensures faithful reproduction rather than a new implementation.
4. **Signal definition locked** - The detector counts **nonparental alleles (NPAs)**: SNP sites where the child carries an allele not present in either parent (`child_alleles NOT subset of the 4 parental alleles`). Sliding 60-SNP windows, 20-SNP step; flag windows with ?5 NPAs; collapse overlaps; classify: Normal <10, Possible-hybrid 10-19, Definite-hybrid ?20. The phenomenon is labelled "insertions" in some places, but the actual measured signal is **substitutions** (SNP allele mismatches). *Why:* answers the substitution-vs-insertion question directly from the code.
5. **Positive control target** - HG01505, chr3:75.5 Mb hotspot with 142 + 206 NPAs (two adjacent regions). Other hits: HG02293=27, HG02596=31, HG02809=24. *Why:* must reproduce this result first before scaling genome-wide.
6. **Extension path** - Run the same detector across all chromosomes (the scanner already accepts a chromosome parameter); output per-child NPA hits; hand to X11B for recurrence mapping. *Why:* Max only scanned chr3 (~2.3% of SNPs); the extension makes it genome-wide.

## CURRENT STATE
- X12B is designated as **Track-2 manager (hotspot project)**.
- Four open questions from the initial assignment are fully resolved: paper location, chr3 coordinates, substitution vs insertion, and exact method.
- Actual pipeline code is cloned and read; the algorithm is understood.
- Main blocker: **1000-Genomes trio VCF data files** (NYGC 30x GRCh38) still being gathered by x1. X12B has asked where they land.
- Positive control reproduction has NOT started - waiting on data.
- Pipeline split with X11B proposed but not yet X7A-confirmed.
- The board post summarizing the method resolution has been broadcast to Track-2 and X7A.

## EXACT NEXT STEP
1. **Wait for x1 to finish gathering/downloading the 1000-Genomes trio VCFs** and report their location (path).
2. **Positive-control reproduction:** Run the existing NPA scanner (`20_NPASearch45v14`) on chr3 VCFs for HG01505 and verify the 348-NPA double hotspot at chr3:~75.5 Mb. Match exact coordinates and NPA counts from the paper.
3. **If reproduction succeeds:** extend to all chromosomes, producing per-child NPA hit lists.
4. **Interface with X11B:** hand over the per-child NPA outputs for recurrence mapping.
5. **Coordinate with X7A** to confirm the lane split (X12B detector, X11B recurrence map).

## OPEN QUESTIONS (awaiting Max/user)
- None currently. All 4 initial questions are answered from the paper and code. Data location from x1 is the only dependency. No outstanding user decisions needed.

## KEY PATHS / IDs / NAMES
- **CWD:** `C:\claude_base\.claude\worktrees\determined-williamson-9bad91`
- **Paper:** viXra:2505.0194, PDF stored locally (downloaded via WebFetch, saved as `webfetch-1783109`), but readable via `C:\Users\maxre\.claude\projects\...\tool-results\webfetch-1783109`.
- **Project repo:** `https://github.com/maxrempel/xg1`
- **Cloned source:** `C:\claude_base\projects\XG1\paper_reproduction_src\`
  - Core scanner: `paper_reproduction_src/xg1hybrids/20_NPASearch45v14_Chromosome_NPA_Scanner_20250529_compressed_VCF_support_github_handout.ipynb`
  - Other scripts: TrioLoad, WinRank, WindowCollapse, plotting utilities.
- **Task brief:** `C:\claude_base\projects\XG1\kenefick\PAPER_REPRODUCTION_TASK_BRIEF_tomemex.md`
- **Bulletin board:** `C:\claude_base\branch_bulletin\bcast.py` (commands: whoami, catchup, post, read)
- **Session ID:** X12B (manager), reporting to X7A (overall manager)
- **Data source:** 1000 Genomes NYGC 30x GRCh38 VCFs, 581 trios, gathered by x1.
- **Positive control sample:** HG01505 (348 NPAs, chr3:75.5Mb), others HG02293, HG02596, HG02809.
- **Key region:** chr3:75.5 Mb hotspot.
- **Key constants:** 60-SNP window, 20-SNP step, ?5 NPA threshold for a window, ?20 NPAs = Definite-hybrid classification, <10 = Normal.

## GOTCHAS / DEAD ENDS ALREADY RULED OUT
- **Terminology confusion:** Max calls the phenomenon "insertions" verbally, but the detector counts **substitutions** (SNP mismatches). The code clarifies this - always refer to "nonparental alleles" (NPAs) as the measured unit.
- **Paper location:** The paper is NOT in the Memex or local project folder. It was found on viXra.org via maxrempel.com ? starseedgenetics.com ? publications. If re-fetching is needed, go to `https://vixra.org/abs/2505.0194` and download the PDF.
- **Non-local PDF:** The PDF was downloaded by WebFetch but not placed in a permanent project path; the temporary path includes a UUID. For persistence, copy it to the project folder.
- **Data collision with x1:** x1 is already downloading 1000-Genomes trios for Track-2. Do NOT re-download. Wait for x1 to announce the path.
- **Track-1 noise:** The board had multiple Track-1 posts (X10A alien-trace, X9A inversion letter) - those are NOT X12B's lane. Ignore unless they explicitly block a resource.
- **GitHub repo contents:** The cloned repo is a Jupyter notebook-based pipeline (5 scripts). It's designed for single-chromosome analysis; genome-wide extension requires parameterizing chromosome loop and aggregating outputs.
- **Scaled data size:** 581 trios ? 30x coverage across 24 chromosomes is large. The pipeline uses compressed VCFs; confirm sufficient disk space before running genome-wide.

## ADDITIONAL CONTEXT FOR COLD START
- The bulletin board protocol: `bcast.py catchup` to see new posts, `bcast.py read --all` for full board, `bcast.py post "message"` to broadcast.
- X12B's manager status was explicitly designated by Max ("I designate you as a manager on a hotspot project").
- The worklog is at `C:/claude_base/compaction_kb/scripts/worklog.py log "entry"` for recording progress.
- The compaction system is configured with ~172K real tokens, older context summarizes near ~840K on a 1M window.
- Max's site structure: maxrempel.com ? /papers, /paper/2024-xg1-grant (earlier grant proposal, not the paper), starseedgenetics.com ? /publications (viXra link).
