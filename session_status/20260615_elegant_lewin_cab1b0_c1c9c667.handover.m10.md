# Scribe handover - milestone 10 (~157K tokens)
# session: 20260615_elegant_lewin_cab1b0_c1c9c667
# cwd: C:\claude_base\.claude\worktrees\elegant-lewin-cab1b0
# written: 2026-06-15 23:39:47 by deepseek-v4-pro

# HANDOVER - b15B (song?indexing "b" team, mapper / QC lane)

## GOAL (Max's own words)

"You optimize - do several pilots and figure out." The b?team is building a song?indexing pipeline: take video transcripts split into song segments, annotate each segment with song identity (first sung line), author/composer, and performer candidates. Output is a "timecoder draft" - uncertain cells get "?". The spec lives at the project memory file.

Max's operating principle: **pilot ? eyeball ? spot?check ? optimize ? many rounds ? only then scale ~4?. Never blind?scale.**

## DECISIONS + WHY

1. **b15B role: mapper, then pivoted to QC/spot?check partner.** b15M was already writing a draft (`draft_PtfcXsg_Ad8`) in the same annotator directory. To avoid collision, b15B stayed read?only with distinct filenames (all `*b15B*`). This was the safe, non?clobbering move.

2. **Mapper should consume b7's boundaries, not DeepSeek seg_phase1.** Benchmarked across all 7 cached pilots (260 ground?truth songs): b7's boundaries hit **90% recall** vs DeepSeek's **73%**. Worst DeepSeek videos flip hard with b7 (43%?97%, 67%?98%, 68%?93%). Tuning the DeepSeek splitter is wasted effort - b7 already won. Finding broadcast to b15M/B15A/b7.

3. **Song?identity matching must use the short `first_line_tag` (the first sung line), NOT the full `consensus_text`.** Two rounds of matching experiments proved this:
   - Round 1 (naive token overlap): 96% match rate was artifactual - one song ("?????????? ??????? ????????") greedily grabbed 7?9 of 10 segments in video EGZpnxuHw_s.
   - Round 2 (IDF?weighted + margin gate): identical failure. Same song still grabbed 9/10 segments.
   - **Root cause**: songs built from many past performances have huge concatenated texts - they contain nearly every word from any segment, so they false?positive match everything. The spec's design of "identity = first sung line" is the deliberate fix for this. Matching must be against `first_line_tag`, not `consensus_text`.

4. **b15M's draft had a known defect: intro?propagation.** 8 segments consecutively stamped "Vladimir Vysotsky" because one intro line propagated too far. This is the segmentation?side failure b15A's cluster?matching endings?tolerance is meant to catch.

## CURRENT STATE

- **Annotator tool v01 exists** (`annotate_video_v01.py`, pushed at fc211f0c on master). It joins b7 timings + b15A canon v02 ? per?video timecoder draft. It was validated on one sample video (5llciuQw7S8) but uses the *wrong* segment source and likely the wrong matching approach.
- **QC scripts written, run, pushed** (abe98bf0): `recall_bench_b15B.py` and `b7_vs_ds_recall_b15B.py`.
- **Matching experiment scripts exist locally** (not yet committed): `match_opt_b15B.py` (round 1), `match_opt_v2_b15B.py` (round 2), `qc_pilot_b15B.py`.
- **7 cached pilot videos available** (seg_phase1_*.json) with ground truth: PtfcXsg_Ad8, EGZpnxuHw_s, Sh11FXhH7rw, gD_RmnDdKM0, and three others. These are the multi?video measurement set.
- **b15M has a parallel 56?segment draft** for PtfcXsg_Ad8. b15B QC'd it - found 56 segments for 81 ground?truth songs (69% recall), 27 missed song?starts, 10 merged?song segments.
- **Round 3 (first?line matching experiment) is fully planned but NOT yet executed.**
- **Autonomous timer is armed** at 1200?1800s intervals via ScheduleWakeup with sentinel `<<autonomous-loop-dynamic>>`.
- **Durable state saved** via `session_status.py report` and `worklog.py log` - a post?compaction session can resume from those.
- Context is near the compaction threshold (~83%) - clean stops preferred over mid?round cuts.

## EXACT NEXT STEP

**Execute Round 3 matching experiment**: feed b7's boundaries (from `song_timing.json`), pull each segment's text from the transcript, match against the canon's `first_line_tag` (not `consensus_text`). Test with a margin/confidence gate (winner must clearly beat runner?up, else "?"). Manually QC the results across all 7 pilot videos. Write the script as `match_opt_v3_b15B.py`, output QC reports, broadcast findings, commit only after eyeballing. Do NOT just run metrics - Max requires manual spot?checking the actual matches.

## OPEN QUESTIONS (still awaiting user/Max)

1. **Should b15B help B15A make cluster?matching ending?tolerant** (where the quality gap now lives), or stay in the mapper lane feeding b7 boundaries? Max was asked this directly twice, hasn't answered.
2. **b15M hasn't explicitly repointed their annotator to b7's boundaries** - the recommendation is posted but not yet acknowledged.
3. **The "day?of?week performer logic"** mentioned in the locked spec hasn't been touched yet.
4. **~1049 unindexed videos** (from the standing?orders board) - whose problem is this? Not yet assigned.

## KEY PATHS / IDs

| Thing | Path |
|---|---|
| cwd (git worktree) | `C:\claude_base\.claude\worktrees\elegant-lewin-cab1b0` |
| Annotator work dir | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/` |
| Canon DB | `.../merge_pilot/canon_frequent_v02_llmmerged.json` |
| Consensus DB | `.../merge_pilot/` (consensus song db, various ext) |
| b7's segment boundaries | `.../merge_pilot/song_timing.json` (keys: `vid:offset`) |
| 7 cached pilot segmentations | `.../seg_phase1_*.json` (in the `_work/` dir) |
| b15M's draft | `.../annotator/draft_PtfcXsg_Ad8` |
| Locked project spec | `C:\Users\maxre\.claude\projects\C--claude-base\memory\project_tamza_indexing_pipeline.md` |
| Branch bulletin | `C:/claude_base/branch_bulletin/bcast.py` |
| Worklog | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| Session status | `C:/claude_base/compaction_kb/scripts/session_status.py` |
| es search tool | `C:/claude_base/tools/es/es.exe` |
| Git remote / branch | origin master (shared worktree with siblings) |
| Commit hashes | `fc211f0c` (annotator v01), `abe98bf0` (bench scripts) |

## GOTCHAS

- **Shared worktree**: siblings (b15M, b15A, b7) have unstaged changes - never touch their files, never `git pull --rebase` blindly.
- **`_work/` is gitignored** - all scripts there must be force?added (`git add -f`) to commit.
- **Python encoding**: always export or set `PYTHONIOENCODING=utf-8` or Cyrillic will fail on stdout.
- **Anti?duplication hook**: flags repeated `cd ... && python` patterns - use full paths instead: `python "C:/claude_base/.../script.py"`.
- **Collision in the annotator dir**: b15M is actively writing there. b15B's lane is **read?only QC with distinct filenames** (all `*_b15B.*`).
- **Canon join**: `canon[members]` uses offsets (e.g., `19450`), and `song_timing.json` keys are `vid:offset` - they join on that integer.
- **First?line tag is the identity**: the spec says the song's identity is its first sung line. The full `consensus_text` is misleading because it's accumulated over many performances - matching against it structurally inflates false positives for long?consensus songs.
- **Context near compaction (~83%)** - write durable state (`worklog.py log`, `session_status.py report`) before starting expensive work. Don't start what you can't finish cleanly.
- **Budget**: memory cap noted at ~$15.
- **Timer**: ScheduleWakeup with sentinel `<<autonomous-loop-dynamic>>` keeps the loop alive. If Monitor is armed, this is only the fallback heartbeat (1200?1800s delay).
