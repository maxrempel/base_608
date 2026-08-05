# Scribe handover - milestone 8 (~122K tokens)
# session: 20260615_elegant_lewin_cab1b0_c1c9c667
# cwd: C:\claude_base\.claude\worktrees\elegant-lewin-cab1b0
# written: 2026-06-15 23:39:56 by deepseek-v4-pro

# HANDOVER: b15B Song-Timing Mapper - Session State

---

## GOAL (Max's words)

Build a song-timing annotator that produces per-video **timecoder drafts** - for every song segment in a video, output timing boundaries, song identity (first sung line), composer/poet, and performer candidates. The tool must join DeepSeek's segment boundaries against a canon database of frequent songs.

**Critical operating principle Max drilled in**: *Pilot first, eyeball the real data, do many rounds of spot-check + optimize, THEN scale up ~4x each round.* Do not blindly scale without validating on a small sample, and do not commit unreviewed output as final.

b15M assigned **b15B = mapper** via the branch broadcast board.

---

## DECISIONS + WHY

1. **Text-matching, not offset-joining.** b15M insisted the matcher use the segment's transcript text against canon song lines, not the offset key (`vid:offset`) I initially planned. I verified that canon `members` use offset keys that match `vid:offset` format, so the join *does* work mechanically - but b15M wants semantic text matching, so I pivoted.

2. **QC/spot-check role, not parallel annotator production.** On wake I found b15M had already produced `draft_PtfcXsg_Ad8` in the same annotator directory. To avoid clobbering or duplicating, I took a **read-only QC partner** role - own filenames (`qc_report_b15B_*.txt`, `qc_pilot_b15B.py`), no writes to b15M's draft. This respects the shared-checkout constraint and the pilot-eyeball principle.

3. **Dominant defect is the splitter, not the identifier.** QC on the pilot video (PtfcXsg_Ad8) showed DeepSeek split out only **56 of 81 real songs (69% recall)**. 25 songs were simply never separated - they can never get a correct identity downstream. 10 segments merged two songs into one. This means tuning **segmentation recall** (the spec's "central knob") is the bottleneck, not polishing the song matcher.

4. **Committed the scaffold, not the drafts.** `annotate_video_v01.py` was force-added and pushed to master (`fc211f0c`) because `_work/` is gitignored. Draft output files stay on disk uncommitted (same discipline as b15A).

---

## CURRENT STATE

### Done
- **`annotate_video_v01.py`** committed + pushed to master (`fc211f0c`). Joins canon v02 + b7 timing data, produces per-video timecoder draft. Validated on one sample video (20/100 canon hits).
- **Pilot QC complete** on video `PtfcXsg_Ad8`. Full QC report written (`qc_report_b15B_*.txt` in annotator dir).
- **QC findings quantified**: 56 segments produced vs 81 ground-truth songs; 27 missed song-starts; 10 merged song pairs; 8-segment Vysotsky propagation run (one wrong author stamp applied to 8 consecutive segments).
- **Posted findings to b15M** on the branch broadcast board: bottleneck = splitter recall, asked whether to tune splitter next or build author-run guard.

### In flight
- **4-min autonomous timer armed** - next wake will check board for b15M's response.
- If b15M is silent on wake, I committed to **verify the Vysotsky propagation run** myself (read-only, no collision). That means checking whether those 8 segments really are different songs from a single performer, or a genuine bug in the author-stamping logic.
- **Budget noted at $15** - no further spend mentioned.

---

## EXACT NEXT STEP

On next autonomous wake (4-min timer), **check the branch broadcast board** for b15M's response. Two branches:

- **If b15M replied with direction** ? follow it (likely: tune splitter threshold OR build the author-propagation guard that prevents one performer stamp from bleeding across segment boundaries).
- **If b15M is still silent** ? verify the Vysotsky run. Read the 8 consecutive Vysotsky-stamped segments from b15M's draft alongside the ground-truth song list, determine whether they're genuinely different songs (real propagation bug) or actually fine (one performer doing a medley). Write findings to a new `qc_report_b15B_vysotsky_*.txt` and post to board. **Do not modify b15M's draft file.**

---

## OPEN QUESTIONS

- Which does b15M want next: **splitter tuning** (adjust DeepSeek boundary threshold to catch more song starts) or **author-run guard** (prevent one performer stamp from propagating across adjacent segments)?
- What is the intended scale-up path after splitter recall is fixed - which ~4 videos are in the next 4x batch?
- Are the ~1049 unindexed videos (standing order on the board) the eventual full batch, or is b15A's from-scratch indexer meant to handle those separately?

---

## KEY PATHS & IDS

| What | Path |
|---|---|
| **Annotator tool (committed)** | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/annotate_video_v01.py` |
| **b15M's draft (do not overwrite)** | `.../annotator/draft_PtfcXsg_Ad8` |
| **QC pilot script** | `.../annotator/qc_pilot_b15B.py` |
| **QC report output** | `.../annotator/qc_report_b15B_*.txt` |
| **Canon DB (frequent songs v02)** | `.../merge_pilot/canon_frequent_v02_llmmerged.json` |
| **Consensus DB** | `.../merge_pilot/` (same dir) |
| **b7 timing output** | `.../merge_pilot/song_timing.json` (keys: `vid:offset`) |
| **Segment data (DeepSeek)** | `.../seg_phase1_PtfcXsg_Ad8.json` (has performer/author/title/confidence, NO transcript text) |
| **Branch broadcast CLI** | `C:/claude_base/branch_bulletin/bcast.py` |
| **Worklog script** | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| **Git commit hash** | `fc211f0c` on master |
| **Video under pilot** | `PtfcXsg_Ad8` (81 ground-truth songs) |
| **Sample video validated** | `5llciuQw7S8` (100 segments, 20 canon hits) |

---

## GOTCHAS

1. **Shared checkout collision risk.** b15M is actively writing to the same `annotator/` directory. Always write to **distinct filenames** (`qc_report_b15B_*`, `_inspect_b15B_*`) and never touch `draft_PtfcXsg_Ad8`. Force-add scripts on commit; leave drafts uncommitted.

2. **Git pull-rebase blocked.** Siblings have unstaged changes in the shared worktree. Can only `git push` (my commits sit on top of latest pushed commit). Never touch siblings' in-progress files.

3. **`_work/` is gitignored.** All commits to files under `_work/` must use `git add -f`. Drafts should *not* be committed.

4. **DeepSeek segments have NO transcript text.** They carry `performer`, `author`, `title`, `confidence` - not the sung words. To text-match against the canon, the pipeline needs the video's transcript (separate file, not yet located for PtfcXsg_Ad8). b15M's draft already bridged this gap somehow (likely from the transcript directly).

5. **Canon offset keys vs b7 timing keys.** Canon `members` use offsets like `195`, `845`; b7 `song_timing.json` uses `vid:offset` like `vid:112`. They *do* match (numeric offset after `vid:`), but b15M wants text-based matching instead.

6. **Do not sleep/laze.** Max will call it out immediately. If there's established work to continue, do it. The autonomous loop exists to advance work, not to wait idly.

7. **es.exe is the local search tool** - use it to locate files, not `cat`/`grep`. It's at `C:/claude_base/tools/es/es.exe`.

8. **UTF-8 encoding required** for Cyrillic (Russian song titles/authors). Always set `PYTHONIOENCODING=utf-8` or use scripts that handle encoding.
