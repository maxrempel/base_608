# Scribe handover - milestone 9 (~136K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# cwd: C:\claude_base\.claude\worktrees\focused-wilbur-d92388
# written: 2026-06-15 11:36:09 by deepseek-v4-pro

## Handover for B15 - Song Corpus Builder (from-scratch indexer)

### GOAL (in Max's words)
"Build a full text collection of all songs and collapse multiple performances of the same song into a consensus."  This is a from?scratch indexing method (for the ~1049 unindexed videos) that needs piloting and testing.  The offline process is COLLECT ? MERGE ? MATCH.

### DECISIONS + WHY
1. **Additive collapse, never trash sources.**  When we collapse multiple noisy performances into one canonical text, the original per?performance texts are preserved alongside the consensus.  Max insisted on this; the corpus keeps every window.
2. **First line, not full lyrics, is the primary identifier.**  Max's steer: "first line > official title."  That is the real fingerprint for matching, and it makes DeepSeek fuzzy matching (later, with spend) worthwhile.  Consequently all matching and testing pivoted to first lines instead of full lyric text.
3. **Consensus first line beats single transcript.**  A leave?one?performance?out test (600 holdout first lines vs. 13?635 songs) showed that a consensus first line gives **51% accuracy** while a single noisy transcript first line gives only **28%**.  So collapsing roughly doubles the song?ID hit rate.
4. **Corpus kept out of git.**  The 91?MB `song_corpus_v01.json` lives in a `_work/` subfolder that is in `.gitignore`.  All scripts and the design doc are committed and pushed.
5. **Dry run is the real proof.**  Instead of a held?out test, Max approved a from?scratch simulation on indexed videos: throw away the timecodes, slide windows across the transcript, and see how many songs can be rediscovered using consensus first lines.  This simulates the exact task the ~1049 unindexed videos will face.
6. **Web search is for attribution only.**  Max: your clean lyrics + web are a later lever; web search is mainly for author/composer attribution, not for song naming.
7. **Test selection:** A full?text matching test (full lyric strings ? 13?670 entries) was too slow and didn't match the first?line steer - it was killed.  The first?line test is fast and on?target.

### CURRENT STATE
- **Corpus built** (via `build_song_corpus_v01.py`): 13?670 songs, 21?218 performances, 3?057 songs with ?2 performances were collapsed into a consensus first line (and full text).  All source performances kept.
- **Validation test completed** (`test_firstline_v01.py`): consensus first?line accuracy of 51%, single?transcript accuracy 28%.  Positive result logged and posted to the branch board.
- **From?scratch dry run completed** (via `from_scratch_sim_v01.py`): output file exists at  
  `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-focused-wilbur-d92388\ba76facd-fe3f-4804-b8d0-f40bd8415613\tasks\b3celh3gl.output`  
  (task completed with exit code 0).  **The result has NOT yet been read or analysed.**
- All pilot scripts and the updated design doc pushed to `master` (commit `8c7994b5`).  The heavy corpus is only local, in `_work/`.
- The branch bulletin caught up: b15 is registered, b14 (manager) is aware of progress.

### EXACT NEXT STEP
**Read and interpret the from?scratch dry?run output.**  
The file is `b3celh3gl.output` at the above temp path.  It should contain recall, precision, or a per?video breakdown of how many songs the system correctly identified (with no ground?truth timecodes).  Report the numbers to Max, and discuss whether the method is ready for prime time on the 1049 unindexed set or needs tweaks.

If the simulation already logged the output to a simpler file (e.g., inside the `from_scratch_idx/` folder), check there too, but the background task wrote to that temp path.  It is safe to open and parse.

### OPEN QUESTIONS (still waiting for Max)
- **Location of Max's existing clean first?lines / lyric database.**  `queue.json` has a `first_line` field but it is mostly blank.  The pilot used first lines extracted from transcripts (first sung words after intro).  Where are the clean lines stored (file, DB, elsewhere)?  This is critical for later refinement.

### KEY FILES / PATHS
- **Working root:** `C:\claude_base\tools\tamza_songs\pipeline\song_timing\`
- **Indexer folder:** `from_scratch_idx/`
  - `build_song_corpus_v01.py` - corpus builder (collect + merge)
  - `test_firstline_v01.py` - leave?one?out validation script
  - `from_scratch_sim_v01.py` - from?scratch dry?run simulator
  - `B14_indexer_design_v01_tomemex.md` - design doc (updated with pilot result)
  - `_work/song_corpus_v01.json` - 91?MB corpus (not in git)
  - `.gitignore` - contains `_work/`
- **Data sources:**
  - Transcripts: `../transcripts/` (452 files)
  - `queue.json` - the master video index (in `song_timing/`)
- **Completed task output:** `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-focused-wilbur-d92388\ba76facd-fe3f-4804-b8d0-f40bd8415613\tasks\b3celh3gl.output`
- **Logging/utilities:**
  - Work log: `C:\claude_base\compaction_kb\scripts\worklog.py log`
  - Resume snapshots: `session_status.py report`
  - Branch board: `python C:/claude_base/branch_bulletin/bcast.py`

### GOTCHAS
- **Full?text match dead end:** `test_corpus_v01.py` (full lyric matching) took >10?min and produced no output; it was killed.  Do **not** attempt full?lyric matching without the first?line workflow.
- **Corpus file must stay out of git.**  The `_work/` folder is ignored; never `git add` the JSON.
- **Unbuffered Python needed for background tasks:** The sim used `python -u` to see output promptly.
- **Autonomous wakeups:** The session uses `ScheduleWakeup` with the sentinel `<<autonomous-loop-dynamic>>`; a background task notification is the real wake signal, the timer is only a fallback heartbeat.  If work continues, re?arm the timer after finishing the current step.
