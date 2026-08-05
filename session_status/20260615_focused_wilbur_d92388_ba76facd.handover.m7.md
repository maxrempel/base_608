# Scribe handover - milestone 7 (~106K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# cwd: C:\claude_base\.claude\worktrees\focused-wilbur-d92388
# written: 2026-06-15 11:03:39 by deepseek-v4-pro

# HANDOVER - B15: Song Corpus Consensus Builder

---

## GOAL (in Max's words)

Build a **full text collection of all songs** from the 452 local transcripts, and **collapse multiple performances of the same song into a consensus**. This method is not well developed - it needs piloting and testing. Consensus is **additive**: keep every source performance intact; the consensus sits on top, never trashes sources.

---

## DECISIONS MADE + WHY

1. **Data source: queue.json + 452 local transcripts in `song_timing/transcripts/`.** Probed and confirmed: 21,218 performances, 13,670 distinct song titles, 3,057 songs with ?2 performances (the consensus candidates). Each performance has `curated_start_times` for windowing the transcript.

2. **Consensus is additive, not destructive.** Max was explicit: keep every original performance text alongside the collapsed version. The `build_song_corpus_v01.py` script stores both `consensus_text` and a list of all `source_performances` with their full windowed lyric text.

3. **Clean lyrics + web search are a LATER lever.** Web search is mainly for **author/composer attribution** (music/lyrics credits), not for naming songs. Do not burn time on this now.

4. **First line > official title.** Max steered: the **first sung line** (first words after the intro) is the real fingerprint for matching unknown performances - more so than the official title. This means the corpus should ultimately be **re-keyed on consensus first line**, not title. That's where DeepSeek fuzzy-matching earns its keep (a spend step - hold until green-lit).

5. **DO NOT TOUCH B6's domain.** B6 owns radio timing + app.js refinement of already-indexed videos. B14 owns the from-scratch song indexer design and the queue.json indexing process. Stay in your lane: offline COLLECT + MERGE + MATCH.

---

## CURRENT STATE

### Done
- **`build_song_corpus_v01.py`** written and executed successfully at:
  `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/build_song_corpus_v01.py`
- Output: **13,670 songs, 21,218 performances, 3,057 with real multi-performance consensus.** Median intra-song similarity is 67 (reasonable for noisy transcripts).
- **`test_corpus_v01.py`** written at:
  `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/test_corpus_v01.py`
- Test methodology: leave-one-performance-out - remove one performance, build consensus from the rest, see if consensus identifies the held-out performance better than a single noisy transcript.
- The test was **launched and was still running** when the session compacted. It was matching 400 test windows against 13,670 full-lyric references - heavy compute.
- **Monitor was armed** on the test output file at:
  `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-focused-wilbur-d92388\ba76facd-fe3f-4804-b8d0-f40bd8415613\tasks\bwd3kqcmb.output`
- Monitor **timed out** - the last event before compaction was the timeout notification.

### In Flight
- The consensus test (`test_corpus_v01.py`) may still be running, or it may have completed and written results to the output file above. **This is the first thing to check.**

---

## EXACT NEXT STEP

1. **Check if the test finished.** Read the output file:
   `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-focused-wilbur-d92388\ba76facd-fe3f-4804-b8d0-f40bd8415613\tasks\bwd3kqcmb.output`
   If still empty/stuck, check for zombie Python processes (`tasklist | findstr python`) and re-run or kill/re-launch as needed.

2. **Report the test result to Max.** Does consensus text (collapsed from N-1 performances) actually identify the held-out Nth performance better than a single transcript? That's the pilot validation he wants.

3. **Re-key the corpus on consensus first line** (per Max's steer). The current corpus keys on title; the target should be the first sung words after the intro. Write a v02 that:
   - Extracts the first line from each consensus text
   - Re-keys the lookup dictionary on that first line
   - Handles fuzzy/near-duplicate first lines (this is where DeepSeek comes in, but confirm with Max before calling the API)

4. **Ask Max the open question** (see below) before building the first-line re-key.

---

## OPEN QUESTIONS (awaiting Max)

- **Where do Max's existing clean first-lines live?** In the data probe, the `first_line` field in `queue.json` was mostly blank in the sample. He mentioned having clean lyrics - are they in a separate file or DB? Knowing this determines whether the first-line re-key uses the transcript-extracted first line or Max's curated ones.

---

## KEY PATHS, FILES, IDs

| What | Path |
|------|------|
| Working directory | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/` |
| Transcripts (452 .json files) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/transcripts/` |
| Queue (21K performances, 13.7K titles) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/queue.json` |
| B14's design doc | `.../from_scratch_idx/B14_indexer_design_v01_tomemex.md` |
| Corpus builder (v01, DONE) | `.../from_scratch_idx/build_song_corpus_v01.py` |
| Consensus test (v01, IN FLIGHT) | `.../from_scratch_idx/test_corpus_v01.py` |
| Test output file (temp, may have results) | `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-focused-wilbur-d92388\ba76facd-fe3f-4804-b8d0-f40bd8415613\tasks\bwd3kqcmb.output` |
| Broadcast board | `python C:/claude_base/branch_bulletin/bcast.py` |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| Branch name | `focused-wilbur-d92388` |
| This branch's role | B15 (offline COLLECT+MERGE+MATCH) |
| Manager branch | B14 (from-scratch indexer, owns queue.json) |
| DO NOT TOUCH | B6 (radio timing, app.js, indexed videos) |

---

## GOTCHAS + DEAD ENDS RULED OUT

- **Console encoding on Windows:** Standard `python` will crash printing Cyrillic/non-ASCII. Always set `PYTHONIOENCODING=utf-8` before running scripts that print song titles.
- **Temp file paths:** The test output lives in a deep, GUID-heavy temp path - don't lose the reference; it's the only way to recover the test result without re-running.
- **Do not re-invent B14's work:** B14 already owns the indexing pipeline and the design doc. Read `B14_indexer_design_v01_tomemex.md` before making structural changes.
- **Do not touch indexed videos:** B6's domain is the already-indexed corpus and radio playback. The 452 transcripts here are the **unindexed** set - your work feeds into B14's pipeline, not B6's.
- **Consensus is additive - never delete sources.** Any merge/collapse script must preserve the original performance texts in full.
- **First line extraction isn't trivial:** Transcripts are noisy. The "first line" after an intro may have false starts, MC talk bleed, or wrong window boundaries. The DeepSeek fuzzy-matching step (when authorized) is meant to handle this fuzz.
- **Test is computationally heavy:** 13,670 references ? 400 test windows is ~5.5M sequence-matcher comparisons. If it hung or ran out of memory, the fallback is to sample (e.g., 100 test windows against 2,000 references) first.
