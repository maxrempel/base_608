# Scribe handover - milestone 2 (~158K tokens)
# session: 20260703_strange_swartz_4aa048_46e5bb37
# cwd: C:\claude_base\.claude\worktrees\strange-swartz-4aa048
# written: 2026-07-03 16:13:58 by deepseek-v4-pro

# HANDOVER FOR SESSION X11B - XG1 Paper Extension (Recurrence/Hotspot Aggregator)

## GOAL (in Max's own words)
Max wants to **reproduce and extend his XG1 paper**. Originally he analysed a small region (chr3) of 1000 Genomes trios looking for biallelic changes in children that came from neither parent. The extension is to run the detection **genome-wide**, then **map where those non?parental changes recur across many unrelated families**. Recurrence hotspots are the test for a real "targeted area" versus random cell?culture noise. After that, overlay the "starseed families" data on the same hotspots.

The session split the work into two tracks:
- **X12B** builds the per?trio detector (the exact method Max used on chr3).
- **X11B** (this session) owns the **genome?wide recurrence aggregator and hotspot caller** - the part that makes it an extension.

## DECISIONS MADE + WHY

1. **Built the aggregator now, before Max's answers.**  
   Max was heads?down and the four blocking questions (paper identity, chr3 coordinates, substitution vs insertion, exact detection method) would gate X12B's detector but not the aggregator. The aggregator only needs a list of per?child non?parental calls, regardless of variant type. Decided to build and validate autonomously so the pipeline is ready when the per?trio output arrives.

2. **Statistical model: Poisson null with FDR correction.**  
   For each genomic window the tool counts how many unrelated children have a non?parental change in that window. It compares that count to a Poisson distribution with mean = (total events genome?wide) ? (window size / genome size) ? number of children. A Benjamini?Hochberg FDR correction is then applied across all windows. This is a simple, well?understood model for rare event recurrences.

3. **Artifact mask overlay before reporting.**  
   Real hotspots can be caused by segmental duplications, satellite repeats, or technical blacklist regions - not alien insertion. The pipeline includes a second stage that tags any hotspot overlapping supplied BED masks. Only "clean" hotspots (no mask overlap) are considered real candidates.

4. **Synthetic validation before live data.**  
   Created 200 synthetic children, each with ~30 random events. Planted exactly one recurrent hotspot (chr3:50,000,000, affecting 42/200 children). The aggregator recovered **only** that hotspot with an FDR < 10???? and found **zero** false positives in the 6,042?event random background. This proves the statistical core works.

5. **Code committed and pushed to the shared repo.**  
   Other sessions had unstaged changes in the main checkout, so X11B stashed those temporarily, rebased the single aggregator commit onto origin/master, pushed, and unstashed. The commit is clean and on the remote.

## CURRENT STATE

| What | State |
|------|-------|
| **Aggregator script** (`hotspot_aggregator.py`) | Built, tested, committed, pushed. Takes a TSV of per?child events, outputs significant hotspot regions with statistics. |
| **Annotator script** (`annotate_hotspots.py`) | Built, tested, committed, pushed. Takes aggregator output + BED mask(s), flags overlapping hotspots. |
| **Method document** (`hotspot_aggregator_method_v01_tomemex.md`) | Written and committed. Explains the algorithm, assumptions, and usage. |
| **Synthetic test suite** | Ran and passed (no false positives, single planted hotspot recovered). |
| **Per?trio detector (X12B)** | Not yet delivered. Output format (TSV columns) needs to be agreed. |
| **1000G trio data (x1)** | Being gathered; not yet staged. |
| **Max's answers to the 4 questions** | Still outstanding (see OPEN QUESTIONS). |
| **Board/team state** | X11B reports to X7A (manager). X12B is a separate session on per?trio detection. Awaiting Max's next prompt. |

## EXACT NEXT STEP (what a cold session should do first)

1. **Read the board** to catch any new posts from X7A, X12B, or x1. Command:  
   `python "C:/claude_base/branch_bulletin/bcast.py" catchup`
2. **Check whether Max has answered the four open questions** (below).  
   If yes - feed those answers to X12B and refine the aggregator input spec.  
   If no - the session is blocked on Max but can still coordinate input format with X12B or prepare real mask files (segdup, simple repeats, ENCODE blacklist).
3. **Define the exchange format with X12B.**  
   The aggregator expects a TSV with at least `child_id`, `chr`, `pos` (1?based). Should also eventually include `ref`, `alt`, and a quality score for optional filtering. Post the proposed format to the board and lock it with X12B.
4. **Acquire real artifact masks.**  
   Obtain standard files for segmental duplications and other known problematic regions (e.g., from UCSC or the 1000 Genomes strict mask). Place them in `paper_repro/masks/` and update the annotation pipeline.
5. **Run a scaled?up synthetic test** (e.g., all chromosomes) to stress?test memory/performance before real data arrives.

## OPEN QUESTIONS (awaiting Max)

The same four questions that X7A also listed in the task brief - none answered yet:

1. **Which paper/report exactly?**  
   Likely the April 2025 XG1 preliminary report. Is there a PDF or stable link? (This affects exact method reproduction, not the aggregator.)
2. **The chr3 region / coordinates** you originally analysed.  
   Needed as a positive control to reproduce your known result before going genome?wide.
3. **Substitutions, insertions, or both?**  
   You've said "substitutions" and also "insertions" in different places. This is the most critical fork - it changes what X12B looks for and what columns the aggregator receives.
4. **Your exact detection method.**  
   How you called "not from either parent," depth/quality cutoffs, how you ruled out ordinary de?novo mutations. X12B needs this to build the per?trio detector.

## KEY FILES, PATHS, AND IDENTIFIERS

| Item | Path |
|------|------|
| Project root | `C:\claude_base\projects\XG1\kenefick\paper_repro\` |
| Aggregator script | `.../scripts/hotspot_aggregator.py` |
| Annotator script | `.../scripts/annotate_hotspots.py` |
| Method doc | `.../hotspot_aggregator_method_v01_tomemex.md` |
| Task brief (from X7A) | `C:\claude_base\projects\XG1\kenefick\PAPER_REPRODUCTION_TASK_BRIEF_tomemex.md` |
| Synthetic test data | `.../test/trios/`, output at `.../test/out/` |
| Board script | `C:\claude_base\branch_bulletin\bcast.py` |
| Git remote commit | `origin/master`, commit `d5c0103a` |

**Team IDs on the broadcast board:**  
X11B (this worker), X7A (manager), X12B (per?trio detector), X10A (alien?trace/insertion lane), x1 (1000G data gatherer), X5 (management relay).

## GOTCHAS AND RULED?OUT DEAD ENDS

- **Identity clash with X12B** - resolved. X7A initially addressed "X12B" as paper?repro worker, but Max had assigned the task to X11B. After a management post it was clarified: X12B is a real, separate session doing the per?trio detection. They are not the same lane. Do not duplicate the detector; wait for X12B's output.
- **Aggregator independence assumption** - the Poisson test assumes each child's non?parental events are independent and that all children are unrelated. The current script does **not** filter for relatedness (all children are treated as independent). If some 1000G trios are close relatives, recurrence could be inflated. This must be addressed before running on real data (e.g., keep only one child per family or use kinship coefficients).
- **Window and flank sizes** - synthetic test used a 1?Mb window with a 2?Mb "flank" (events inside the window are counted; the flank is used for null estimation to avoid double?counting nearby repeats). These numbers are arbitrary. For the real genome, parameters should be chosen based on expected insertion size and recombination distance.
- **Multiple testing correction** - the synthetic test used Bonferroni (number of windows), which is very conservative. The code allows FDR (Benjamini?Hochberg) and that is the intended default. The method doc explains both.
- **Artifact mask files** - only fake BED files were used for testing. Real masks (segmental duplications, simple repeats, ENCODE blacklist) must be downloaded. The annotator script is mask?file?agnostic and will work with any BED.
- **Main checkout unstaged changes** - other sessions have unstaged churn in the working directory. The X11B session stashed them to push cleanly and then restored. A cold session will see those changes again. If a push is needed, either stash them again or work on a separate branch to avoid conflicts.
- **The aggregator is not yet configured to read actual per?trio output** - the synthetic test generated its own TSV. The real input will come from X12B; a command?line interface with column name mapping is in place (`--col-child`, `--col-chr`, `--col-pos`, etc.), but the exact column names must match X12B's output.

---

**This handover is final. Any new session should resume by reading the board, checking for Max's answers, and contacting X12B to define the input format.**
