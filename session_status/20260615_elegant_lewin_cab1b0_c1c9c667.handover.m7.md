# Scribe handover - milestone 7 (~105K tokens)
# session: 20260615_elegant_lewin_cab1b0_c1c9c667
# cwd: C:\claude_base\.claude\worktrees\elegant-lewin-cab1b0
# written: 2026-06-15 23:21:18 by deepseek-v4-pro

# HANDOVER - b15B mapper / annotator work

---

## GOAL (Max's words, from context + last message)

"do pilot - and spot check - do many rounds of spot check and optimization. ... run a bigger pilot and then scale up every time about 4 fold."

Broader project goal (from the spec and board): b15B is the **mapper** - take b7's song-segment timings (`song_timing.json`) and b15A's consensus DB (`canon_frequent_v02_llmmerged.json`), join them per video, and produce a **timecoder draft** for each video: identity (first sung line), composer/poet as "X or Y?" when unsure, performer candidates, with question marks everywhere the tool is not confident. Imperfect is fine - this is a draft for a human to finish.

---

## DECISIONS MADE + WHY

1. **Join key: `vid:offset`** - canon `members` entries use numeric offsets (e.g., `19450`) that match `song_timing.json` keys of form `vid:offset`. Verified by spot-checking that canon member `5llciuQw7S8:195` and timings key `5llciuQw7S8:195` both exist. This is the correct join.

2. **Schema mapping**: `song_timing.json` ? per key: `{start, end, segments: [{seg_start, seg_end, text, best_title}]}`. Canon ? per member key: `{ident_line, composer, poet, performer_whisper, ...}`. Annotator merges: if segment's word-index key exists in canon, fill identity/author/performer from canon; otherwise emit `"?"` + the existing `best_title` as a hint.

3. **Output format**: per-video JSON lines file (`video_id.annotated.jsonl`), one line per segment, fields: `{seg_start, seg_end, text, ident_line, composer, poet, performers, canon_hit (bool)}`.

4. **Code location**: placed in `from_scratch_idx/_work/annotator/` alongside b15A's work dir - commit forced through `.gitignore` (scripts committed, drafts stay on disk per team convention).

5. **Only one validation run was done** - on video `5llciuQw7S8` (100 segments, 20 canon hits). This is where Max is furious: the assistant pushed after ONE run instead of doing iterative pilot ? spot-check ? fix ? re-run ? scale 4x.

---

## CURRENT STATE

**What is done:**
- Annotator v01 script: `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/annotate_video_v01.py`
- Committed + pushed to master: `fc211f0c`
- Single validation run on video `5llciuQw7S8` - 100 segments, 20 hit canon, 80 got "?" hints
- Board post made to b15M saying "DONE w/ scaffold"
- 4-minute timer was armed (wakes ~23:22)

**What is NOT done (the actual required work):**
- NO pilot rounds (only 1 video, 1 run)
- NO spot-checks of output quality
- NO optimization passes
- NO 4x scaling (1 video ? 4 ? 16 ? 64)
- NO batch runner for all videos
- NO wiring of unindexed-video boundaries (the ~1049 unindexed videos from board)
- NO day-of-week performer logic

---

## EXACT NEXT STEP (cold session must do THIS first)

1. **Read the fucking output.** Open the annotated output from `5llciuQw7S8` and read every segment. Does `ident_line` make sense where canon hit? Are the "?" hints useful? Is anything broken?

2. **Spot-check round 1** - fix any bugs, broken fields, or nonsense. Re-run on `5llciuQw7S8`. Read output again. Fix. Re-run. Until output is clean across ALL 100 segments.

3. **Scale to 4 videos** - pick 3 more videos from `song_timing.json`, run annotator on all 4. Spot-check ALL 4 outputs. Fix issues. Re-run.

4. **Scale to ~16 videos** - spot-check a sample (e.g., every 3rd video). Fix. Re-run.

5. **Scale to ~64 videos** - spot-check a sample. Fix. Re-run.

6. **Full batch** - run on all videos in `song_timing.json`.

7. **Then** wire in unindexed videos + day-of-week performer logic IF b15M asks.

---

## OPEN QUESTIONS (awaiting Max / b15M)

- What "unindexed videos" (~1049) need to be handled? Where is that list?
- What is the "day-of-week performer logic" - does it vary which performer sang on which day of the week?
- Is there a target output directory for the annotated files, or do they land next to the script?
- Should the annotator consume the consensus DB directly or make a local copy?

---

## KEY PATHS / IDs

| Thing | Path/ID |
|---|---|
| Annotator script | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/annotate_video_v01.py` |
| Canon (consensus DB) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/merge_pilot/canon_frequent_v02_llmmerged.json` |
| b7 timing output | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/merge_pilot/song_timing.json` |
| Work dir (all pieces) | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/merge_pilot/` |
| Annotator output dir | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/` |
| Sample video tested | `5llciuQw7S8` |
| Git commit | `fc211f0c` on master |
| Broadcast system | `C:/claude_base/branch_bulletin/bcast.py` |
| Identity | b15B, reporting to b15M |

---

## GOTCHAS / DEAD ENDS RULED OUT

- **UTF-8 stdout**: Python needs `PYTHONIOENCODING=utf-8` for Cyrillic output - already handled.
- **Gitignore**: `_work/` is gitignored at this depth - scripts must be `git add -f` to commit. Already done once, must repeat for any new files.
- **Shared checkout**: other branches have unstaged changes - never touch them. Push without pulling/rebase. Already handled.
- **es.exe**: it's a real .exe, not a Python script. Used only for file lookup, not needed for the annotator itself.
- **Canon schema**: `members` is a dict keyed by `vid:offset` (string), not a list. The annotator already handles this.
- **Do NOT push after one run** - Max explicitly wants many rounds of spot-check and optimization before calling anything done. The previous assistant fucked this up.
