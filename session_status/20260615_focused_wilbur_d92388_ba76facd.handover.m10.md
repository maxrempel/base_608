# Scribe handover - milestone 10 (~152K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# cwd: C:\claude_base\.claude\worktrees\focused-wilbur-d92388
# written: 2026-06-15 11:43:23 by deepseek-v4-pro

# HANDOVER - B15: Offline Song Corpus Builder (From-Scratch Indexer)

## GOAL (Max's own words)
"Build a full text collection of all songs and collapse multiple performances of the same song into a consensus. That's not well developed method, needs piloting and testing."

Also: "I prefer first lines to names of songs" - the song fingerprint is the **first sung line**, not the official title. "Must use first lines."

Budget ceiling: full indexing of the entire archive (~1049 unindexed videos) should stay under **~$60 USD** total. DeepSeek API calls are the spend vector - B6 confirms even "cheap" DeepSeek accumulates charges fast.

## DECISIONS MADE + WHY

1. **Additive collapse, never trash sources.** Max was explicit: consensus sits on top, every original performance text is kept alongside. The corpus (91MB) preserves all 21,218 raw performances beneath 13,670 consensus entries.

2. **First line beats official title for identification.** A song is fingerprinted by its first sung words (the line after any spoken intro). The corpus is keyed on first-line, not title. This is where DeepSeek semantic matching earns its keep later - fuzzy-tolerant comparison of first-lines across performances.

3. **Offline fuzz-only baseline first, DeepSeek later.** The current dry-run uses crude edit-distance + token overlap matching (free, fast). DeepSeek is the lever to cut false positives (the "confident-but-wrong" guesses) - but it's the paid step and Max hasn't greenlit it yet. Hold there.

4. **Curated first-lines in queue.json are the gold source.** Found that `first_line` is already filled for 16,582/24,124 song rows (69%) in the existing queue.json. These are human-curated and cleaner than transcript-derived ones. Switched the matcher to use them (v2 sim).

5. **Corpus kept out of git.** The 91MB `song_corpus_v01.json` lives in `_work/` with a `.gitignore`; only scripts + design doc are committed.

## CURRENT STATE

**What's built and working:**
- `build_song_corpus_v01.py` - reads all 452 transcripts + queue.json, windows every performance, collapses multi-performance songs into a consensus first-line + full text. Keeps sources intact. Output: `_work/song_corpus_v01.json`.
- `test_firstline_v01.py` - leave-one-performance-out benchmark. Proved consensus first-line (51% correct) nearly doubles the hit rate vs one noisy transcript (28%).
- `from_scratch_sim_v01.py` - the real from-scratch dry run. 20 held-out indexed videos, timecodes discarded, sliding windows + fuzz match against the consensus index. **Result: 37% recall, 32% precision** (purely offline, no AI spend).
- `from_scratch_sim_v02.py` - same dry run but using the **curated** first-lines from queue.json and harder typo-tolerant normalization. **Launched in background; result may have landed by now.**

**What's committed + pushed to master:**
All scripts in `tools/tamza_songs/pipeline/song_timing/from_scratch_idx/` plus updated `B14_indexer_design_v01_tomemex.md`. Commits are on master (base `8c7994b5` plus follow-up pushes).

**What's in flight:**
The v2 curated-first-line simulation - launched as a background task. Output file path was a Claude task output; check the last task notification or run the script directly from the folder to get the result.

## EXACT NEXT STEP

1. **Check if v2 simulation completed.** The script is `from_scratch_sim_v02.py` in the `from_scratch_idx/` folder. Run it with `PYTHONIOENCODING=utf-8 python -u from_scratch_sim_v02.py` if it didn't finish. The expected output: recall + precision using the **curated** first-lines from queue.json (should be better than v1's 37%/32%).

2. **Analyze the v2 result against the budget.** The gap between current offline recall and acceptable coverage tells you how many DeepSeek calls are needed. Max's budget is ~$60 for the whole ~1049-video archive - so estimate: `(unindexed videos) ? (avg windows per video) ? (DeepSeek cost per call)` and see if it fits.

3. **If v2 shows meaningful lift** (curated first-lines improve recall meaningfully), commit the script and update the design doc with the new numbers. Post to the board for b14.

4. **Do NOT wire up DeepSeek yet** - Max hasn't explicitly greenlit the spend step, and B6's warning about accumulating costs is fresh. Present the numbers and the cost estimate first, then ask.

## OPEN QUESTIONS (awaiting Max)

1. **DeepSeek greenlight.** "Want me to wire it up and pilot it on a small batch (a few dollars), or hold?" - Max hasn't answered. Hold until he does.

2. **Missing 31% of curated first-lines.** Posted to b6/b14 on the board: where do first-lines for the remaining ~7,500 song rows come from? Are they in another file, or are they genuinely not curated yet?

3. **Your clean lyrics as a later lever.** Max mentioned his own clean lyrics + web as a future quality lever (web mainly for author/composer attribution, not naming). Not yet in play.

## KEY PATHS + FILES

| What | Where |
|------|-------|
| Corpus builder | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/build_song_corpus_v01.py` |
| First-line test (leave-one-out) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/test_firstline_v01.py` |
| From-scratch sim v1 (transcript first-lines) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/from_scratch_sim_v01.py` |
| From-scratch sim v2 (curated first-lines) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/from_scratch_sim_v02.py` |
| Corpus output (91MB, gitignored) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/song_corpus_v01.json` |
| Source data (452 transcripts, curated first_lines) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/queue.json` + `transcripts/` |
| Design doc | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/B14_indexer_design_v01_tomemex.md` |
| Board | `python C:/claude_base/branch_bulletin/bcast.py` (bcast.py commands) |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| Resume snapshot | `python C:/claude_base/compaction_kb/scripts/session_status.py report "..."` |

## GOTCHAS + DEAD ENDS

- **Console encoding:** Cyrillic in transcripts crashes default Windows console. Always use `PYTHONIOENCODING=utf-8` before Python commands.
- **Full-text matching is too slow.** The first attempt (matching 400 full-lyric windows against 13,670 long reference texts) was killed - too heavy and missed Max's "first line" steer anyway. All matching now uses first-lines only (short strings, fast).
- **Don't touch b6's territory.** b6 owns `app.js`, radio timing, and anything to do with already-indexed video refinement. b14 owns the overall from-scratch indexing design. B15's lane is the offline COLLECT+MERGE+MATCH corpus builder - the data, not the app or the runtime pipeline.
- **Corpus is additive only.** Never delete or overwrite source performance data - consensus sits on top, original rows stay intact.
- **DeepSeek is the only spend vector.** Offline matching is free. The $60 budget applies to DeepSeek API calls for semantic first-line matching + announce detection. Do not spend without Max's go-ahead.
- **queue.json `first_line` coverage is 69%, not 100%.** The v2 sim will show what recall looks like with the curated subset; the missing 31% may or may not matter depending on whether those are songs that actually recur (the consensus candidates).
