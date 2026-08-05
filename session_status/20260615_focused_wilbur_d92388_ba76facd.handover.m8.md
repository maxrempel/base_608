# Scribe handover - milestone 8 (~125K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# cwd: C:\claude_base\.claude\worktrees\focused-wilbur-d92388
# written: 2026-06-15 11:12:22 by deepseek-v4-pro

# HANDOVER: B15 - Song Corpus Builder (from-scratch indexer, COLLECT+MERGE+MATCH)

## GOAL (Max's own words)

> "Build a full text collection of all songs and collapse multiple performances of the same song into a consensus. That's not well developed method, needs piloting and testing."

You are **B15** in the branch broadcast system. B14 (the manager) owns the overall from-scratch indexer for ~1049 unindexed videos. Your slice: the offline COLLECT + MERGE + MATCH pipeline - window every performance from the 452 local transcripts using curated start times, collapse recurring songs into a consensus text (additively, never trashing sources), and test whether the consensus actually identifies unknown performances better than a single noisy transcript.

## DECISIONS MADE + WHY

1. **Additive collapse - sources kept, never trashed.** Max explicitly corrected this. The consensus corpus stores every original performance text alongside the merged consensus. Rationale: the raw data is irreplaceable; consensus is a "view on top."

2. **First line > official title for song identification.** Max steered this. The first sung words after the intro are the real fingerprint. This changes the matching target from full lyric text to first-line strings (short, fast, high-signal). DeepSeek fuzzy matching will come later when Max green-lights spending.

3. **Clean lyrics and web search are a later lever.** Max said his clean lyrics (and web) are for a future pass. Web search is mainly for author/composer attribution, not song naming.

4. **Pivoted from full-text matching to first-line matching.** The initial test (400 held-out windows ? 13,670 full-lyric references) was too slow and didn't match Max's "first line" steer. Killed it and rewrote for first-line matching - short strings, fast, on-target.

5. **Consensus corpus file moved to `_work/` subfolder, gitignored.** The corpus is 91MB. B14 flagged this housekeeping. Scripts now read/write from `_work/song_corpus_v01.json`. `.gitignore` has `_work/`.

6. **Only from_scratch_idx files committed and pushed to master.** Other files modified by sibling branches (app.js, data.json, etc.) were excluded from the commit.

## CURRENT STATE - WHAT IS DONE

### Corpus built
- **`build_song_corpus_v01.py`** - reads `queue.json` + 452 transcripts from `song_timing/transcripts/`, windows every performance using curated start times, collapses 3,057 songs that appear in ?2 videos into a consensus text.
- Output: `_work/song_corpus_v01.json` (91MB, gitignored)
  - 13,670 distinct songs
  - 21,218 total performances
  - 3,057 songs have real multi-performance consensus (?2 videos)
  - Median intra-song similarity: 67
  - Every original performance text preserved alongside the consensus

### Pilot test PASSED
- **`test_firstline_v01.py`** - leave-one-performance-out test over 13,635 songs:
  - 600 unseen holdout performances
  - Consensus first-line correctly IDs the song: **51%** (307/600)
  - Single raw transcript first-line: only **28%** (170/600)
  - Conclusion: collapsing many noisy versions into one consensus roughly **doubles** the hit rate.
- Test result logged to worklog and posted to the broadcast board.

### Design doc updated
- `B14_indexer_design_v01_tomemex.md` - appended the pilot result as a "B15 pilot result" section.

### Committed, merged, pushed to master
- `idx_validate_v01.py`, `idx_validate_v02.py` (B14's validators, included for folder coherence)
- `build_song_corpus_v01.py`
- `test_firstline_v01.py`
- `B14_indexer_design_v01_tomemex.md`
- `.gitignore`

### Timers
- Autonomous loop is armed with `ScheduleWakeup` at dynamic pacing.

## EXACT NEXT STEP (proposed, awaiting Max's go-ahead)

> "The true from-scratch dry run - take an indexed video, throw away its timecodes, slide windows across its transcript, and see how many songs we correctly find+name with consensus first-lines. That's the real proof for the ~1049 unindexed videos."

This is the natural next build. It would simulate what the indexer actually does: blind sliding-window search over an un-indexed transcript, matching each window against the consensus first-line index. The leave-one-out test proved the consensus is better at identification - this dry run proves it works in the actual search setting.

Max has not yet replied to this proposal.

## OPEN QUESTIONS (awaiting Max)

1. **Where do Max's existing clean first-lines live?** Is there a file or DB offline? `first_line` in `queue.json` is mostly blank in the inspected sample. Currently using transcript-derived first lines - which work, but Max's clean ones would be better when available.

2. **Go-ahead on the sliding-window dry run.** Proposed but not yet authorized.

3. **DeepSeek fuzzy matching for fuzzy first-line matching.** Max mentioned this is where DeepSeek earns its keep, but it's a spend step - holding until green-lit.

## KEY PATHS / IDs / COMMANDS

| What | Path |
|---|---|
| Pipeline folder | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/` |
| Corpus builder | `.../from_scratch_idx/build_song_corpus_v01.py` |
| First-line test | `.../from_scratch_idx/test_firstline_v01.py` |
| Design doc | `.../from_scratch_idx/B14_indexer_design_v01_tomemex.md` |
| Validators (B14's) | `.../from_scratch_idx/idx_validate_v01.py`, `idx_validate_v02.py` |
| Corpus output | `.../from_scratch_idx/_work/song_corpus_v01.json` (91MB, gitignored) |
| Transcripts | `.../song_timing/transcripts/` (452 files) |
| Queue data | `.../song_timing/queue.json` (21,481 performances, 13,670 distinct titles) |
| Branch bulletin | `C:/claude_base/branch_bulletin/bcast.py` |
| Worklog | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| Session status | `C:/claude_base/compaction_kb/scripts/session_status.py` |

## GOTCHAS + DEAD ENDS

- **Full-text matching is too slow** for this scale (400 windows ? 13,670 long lyric refs timed out after 10+ min). First-line matching is fast and aligns with Max's steer anyway. Don't go back to full-text matching.

- **Cyrillic console encoding crashes** on basic `print()` - always use `PYTHONIOENCODING=utf-8` prefix when running Python in this project.

- **Context is high** (~63% at last snapshot). Resume snapshots are being saved via `session_status.py report` to survive compaction. If you wake up to a compacted session, this handover is your lifeline.

- **Don't touch B6's territory:** B6 owns radio timing / app.js refinement of *already indexed* videos. You own from-scratch indexing of *unindexed* videos. B14 is the manager coordinating both.

- **Commit hygiene:** Only commit your own files (`from_scratch_idx/`). Other files in the working tree are modified by sibling branches - don't stage them.

- **Corpus is 91MB** - it's in `_work/` and gitignored. Don't commit it. Regenerate if lost by running `build_song_corpus_v01.py`.
