# Scribe handover - milestone 11 (~166K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# cwd: C:\claude_base\.claude\worktrees\focused-wilbur-d92388
# written: 2026-06-15 12:09:35 by deepseek-v4-pro

# HANDOVER - B15 Song Indexer (from-scratch COLLECT+MERGE+MATCH pilot)

---

## GOAL (in Max's words)

> "Build a full text collection of all songs and collapse multiple performances of the same song into a consensus. That's not well developed method, needs piloting and testing."

Then extended: prove it by throwing away a video's timecodes, sliding windows across its transcript, and re-discovering its songs using the consensus index - the real proof for the ~1049 unindexed videos. Use **first lines, not song titles** as the matching fingerprint. Collapsing is **additive** (keep every source performance; consensus sits on top - never trash sources).

---

## DECISIONS + WHY

1. **First-line matching, not full-text.** Consensus full-lyric matching was too slow (13,670 refs ? 400 windows). First lines are short, fast, and are the real fingerprint - Max's instinct. This also aligns with the "DeepSeek fuzzy matching" intent.

2. **Curated first-lines from queue.json over transcript-derived.** queue.json already has a `first_line` field filled for 16,582/24,124 rows (69%). Max pointed at this explicitly: "must use first lines." Switching to curated refs raised recall 37% ? 54%.

3. **Local/free matching first, DeepSeek for reasoning only.** First-line matching doesn't need an API - fuzzywuzzy and local embedding models cost $0/call. DeepSeek's real job is announce-detection and author/composer attribution. Even then, a full pass over all ~1049 transcripts costs only a few dollars - well under Max's $60 archive target.

4. **Dev budget $15, not waiting.** Max corrected the earlier "wait for greenlight on spend" posture: "use whatever for development, dev budget is 15 USD. I didn't say stop." Authorization is to keep moving and use DeepSeek for development within $15.

5. **Corpus kept out of git.** The 91MB song_corpus_v01.json lives in `from_scratch_idx/_work/`, gitignored. Scripts only in version control.

6. **B15's scope (from B14's handover):** offline COLLECT+MERGE+MATCH for the from-scratch indexer. Do NOT touch app.js, data.json, deployed radio timing (B6's domain), or the ~2M-clip YT search indexer.

---

## CURRENT STATE - WHAT IS DONE

### Built and validated scripts (all pushed to master):

| Script | What it does | Result |
|---|---|---|
| `build_song_corpus_v01.py` | Windows 21,218 performances from 452 transcripts using curated start times; collapses 3,057 recurring songs into consensus text additively | 13,670 distinct songs, corpus at `_work/song_corpus_v01.json` |
| `test_firstline_v01.py` | Leave-one-perf-out test: consensus first-line vs single transcript first-line for ID | **Consensus: 51% correct; single: 28%** - nearly doubles accuracy |
| `from_scratch_sim_v01.py` | True dry run: discards timecodes from 20 held-out videos, re-discovers songs by sliding first-line windows against consensus index (fuzzy ratio, cutoff 80) | **Recall 37%, precision 32%** - baseline |
| `from_scratch_sim_v02.py` | Same dry run but switched reference to **curated queue.json first_lines** with partial_ratio matching (cutoff 80) | **Recall 54%** (up from 37), **precision 17%** (down from 32) - matcher got too loose |

### Data discovered:
- **queue.json**: 24,124 song rows, `first_line` filled for 16,582 (69%), `title` for all
- **Transcripts**: 452 local transcript files at `song_timing/transcripts/`
- **Corpus**: 3,057 songs with ?2 performances (consensus candidates), 21,218 total performance windows

### Design doc updated:
- `B14_indexer_design_v01_tomemex.md` contains pilot methodology and all result numbers

### Broadcast board notified:
- B14 and B6 know B15's results and the matcher-vs-recall-vs-precision state

---

## EXACT NEXT STEP

**Find the recall/precision sweet spot by sweeping the match threshold.** v2's 54% recall / 17% precision means the matcher is too generous. The fixable knob: raise the cutoff, require longer curated first_lines, add a secondary confirm pass.

Specific actions, in order:

1. **Sweep `from_scratch_sim_v02.py` thresholds** (try cutoffs 85, 90, 92, 95) on the same 20 hold-out videos to find the recall-vs-precision curve. This is free, local, offline.

2. **Apply B6's normalization rules** to first-line matching. B6 has already built normalization for typo/accent/performer-prefix handling - that logic needs to be ported into the match step. Ask B6 for the exact rules or the normalizer code path.

3. **Add a cheap confirm pass**: after a fuzzy first-line match, do a rapid secondary check (e.g., check if the song's known key words appear nearby in the transcript window) to cut false positives.

4. **Build a local embedding matcher** (multilingual model like sentence-transformers) as a free, typo-tolerant alternative to fuzzy matching for the match step.

5. **Pilot DeepSeek announce-detection** on a small batch (5-10 videos) within the ~$15 dev budget, wiring up the "did the performer just announce a song?" detection that B14's design doc calls out.

6. Once precision is acceptable, scale the dry run from 20 ? all 452 indexed videos as a ground-truth benchmark.

---

## OPEN QUESTIONS

1. **B6's normalization rules** - exact code path or logic for typo/accent/performer-prefix handling. B15 posted this question to the board; no reply yet.

2. **The 31% of songs missing curated first_lines** - what's the plan for those rows? Are they being backfilled, or do they fall back to transcript-derived first lines?

3. **Clean lyrics source (Max's)** - Max mentioned "your clean lyrics + web are a later lever." Where do Max's private clean first-lines live, if separate from queue.json?

---

## KEY FILE PATHS

```
C:/claude_base/tools/tamza_songs/pipeline/song_timing/
??? queue.json                              ? curated song DB (has first_line!)
??? transcripts/                            ? 452 transcript files
??? from_scratch_idx/
    ??? B14_indexer_design_v01_tomemex.md   ? design doc (updated with results)
    ??? build_song_corpus_v01.py            ? corpus builder
    ??? test_firstline_v01.py               ? consensus-vs-single validation
    ??? from_scratch_sim_v01.py             ? v1 dry run (fuzz baseline)
    ??? from_scratch_sim_v02.py             ? v2 dry run (curated first_lines)
    ??? idx_validate_v01.py                 ? B14's validator scripts
    ??? idx_validate_v02.py
    ??? .gitignore                          ? ignores _work/
    ??? _work/
        ??? song_corpus_v01.json            ? 91MB consensus corpus (not in git)
```

Broadcast board: `C:/claude_base/branch_bulletin/bcast.py`
Worklog: `C:/claude_base/compaction_kb/scripts/worklog.py`
Resume snapshots: `C:/claude_base/compaction_kb/scripts/session_status.py report`

---

## GOTCHAS + DEAD ENDS RULED OUT

- **Cyrillic console encoding** breaks Python stdout on this Windows machine. Always set `PYTHONIOENCODING=utf-8` when running Python that might print non-ASCII.

- **Full-text lyric matching was too slow** (400 windows ? 13,670 long refs timed out after 10+ min). Ruled out in favor of first-line matching, which is fast and Max-approved.

- **An adviser falsely claimed B14's handover was skipped.** It was not - B14 handed B15 the job directly on the broadcast board and B15 has been building exactly that scope from turn one.

- **Do NOT touch**: `app.js`, `data.json`, the deployed radio website, the ~2M-clip YouTube indexer - those are B6's domain and B14's play-safe rules forbid modifying them.

- **Corpus is additive** - every source performance text is kept alongside the consensus. Nothing was dropped. queue.json is untouched by B15's scripts (read-only).

- **Compaction cliff**: context was at ~91% when the session was handed over. A resume snapshot was saved via `session_status.py report` covering all state. The cold session should read that snapshot first.

- **Dev budget**: $15 for development, $60 target for full archive indexing. Matching stays free/local; DeepSeek reserved for announce/authorship reasoning.

- **Autonomous loop**: heartbeat is armed via `ScheduleWakeup` with sentinel `<<autonomous-loop-dynamic>>`. Background tasks used `python -u` and output to temp task files for notification.
