# Scribe handover - milestone 4 (~305K tokens)
# session: 20260618_hungry_easley_b15e0d_fcea422d
# cwd: C:\claude_base\.claude\worktrees\hungry-easley-b15e0d
# written: 2026-06-18 14:52:35 by deepseek-v4-pro

# HANDOVER - b27worker (Tamza first-sung-line pipeline)

## GOAL (Max's words)
Identify every Tamza performance by its **first actual sung line** - not the announcer's spoken intro, not the song title the announcer said. Kill titles-as-identity. For each video, produce `verified_first_lines_<vid>.json` (keyed `vid|sec`) that the publisher auto-ingests. The first sung words must be **faithful to what was actually heard/sung** (garbled stays garbled), never "corrected" to the famous/canonical lyric. Recited poems must be labelled POEM, not forced into a song slot.

---

## DECISIONS + WHY

1. **Hand-pilot before scale** - B26 required b27 (Opus, in-session = free) to manually extract first lines from one video first, so the approach could be spot-checked before spending any API money on a full ~770-video run. Good call: the hand pilot immediately caught the "canonical drift" trap (see Gotchas).

2. **Faithful to heard text, not canonical lyrics** - v01 of the hand pilot "corrected" garbled sung lines to the famous textbook version (e.g. wrote the famous couplet instead of the actual garbled words sung). B26 caught this; v02 was redone faithfully. This is the #1 quality rule for the whole pipeline.

3. **DeepSeek-nonflash for scale, never Opus API** - Max banned Opus API sub-agents after a $40 burn in another session. DeepSeek-chat (V3 non-flash) is cheap (~$0.004/video), and the pilots proved it does NOT drift to canonical lyrics (the main worry). Total pilots cost $0.026. The full run is estimated ~$3 (pilot) or ~$12 (all 770 videos).

4. **Staging suffix for DS4 output** - DS4 writes to `verified_first_lines_<vid>__ds4pilot.json` (staging), never directly to the auto-ingested filename. This prevents unverified DeepSeek output from reaching the publisher before B26 hand-QCs it. Only after QC do we promote/rename.

5. **Dry-run mode in the batch runner** - `firstline_ds4_v01.py` has `--dry-run` that writes to a separate preview file, never touching real data. (A bug in the first dry-run *did* overwrite the hand-pilot JSON with placeholders, but it was caught and restored same-turn; fixed immediately.)

6. **POEM and VERIFY as first-class labels** - Some segments are recited poems (not songs) and some transcript spans are too garbled to extract. The output schema supports `first_line: "POEM"` and `first_line: "VERIFY"`. b15merger needs to handle these (not publish a poem as a song titled "POEM"). Contract still pending from b15merger.

7. **4-minute autonomous wake** - After the cold-wake bug was diagnosed (see Gotchas), B26 ordered b27 to keep a 4-min ScheduleWakeup armed and re-arm every tick so the session stays reachable. The sentinel is `<<autonomous-loop-dynamic>>`.

8. **Money rule clarified** - DeepSeek is NOT Opus. The $3 pilot was pre-authorized by Max (per B26). Max runs the full $12 scale run. b27 won't auto-spend without confirmation.

---

## CURRENT STATE

### Done
- **Hand-pilot on pX_1m8DlMbA** (2020 concert, 47 segments): 28 sung, 8 POEM, 4 VERIFY (garbled), 7 INTRO-ONLY. Written to `timecoder_handover/verified_first_lines_pX_1m8DlMbA.json` (the live auto-ingested file - this one was hand-produced, so it's trusted).
- Old buggy version backed up: `timecoder_handover/archive/obsolete_verified_first_lines_pX_1m8DlMbA.json`
- **DS4 scale runner built**: `song_timing/from_scratch_idx/firstline_ds4_v01.py` - uses `deepseek-chat`, key from ssh folder, has dry-run, cost cap, resumable, output-suffix, comma-separated multi-vid.
- **DS4 pilots run** on 3 videos (pX, 2fEUd_iqJ3A, 6sGQz2wB3pg): v1 prompt had 29/47 class-agreement with hand; v2 prompt (tightened: first line only, strict INTRO-ONLY, detect recitation?POEM) improved to 35/47. Total spend $0.026. Output in staging files: `verified_first_lines_<vid>__ds4pilot.json` and `__ds4pilot2.json`.
- **Archive cleanup plan** delivered: `ARCHIVE_CLEANUP_PLAN_v01.md` on branch `claude/hungry-easley-b15e0d` - 55 scripts + 2 data files flagged, import safety verified, pending owner sign-off from b15M/b15merger.
- **Wake bug root-caused**: no signal file ever placed for b27's session; bcast falsely reports "FORCE-WOKEN". c6 needs to fix.

### In Flight / Awaiting
- **B26's QC verdict on DS4 prompt v2** - 35/47 agreement is decent but imperfect (misses ~5 poems, runs long on a few). B26 decides: scale as-is and let human timecoders catch the ~10%, or sharpen the prompt once more.
- **b15merger's contract** - how should the publisher handle POEM and VERIFY labels? b15merger hasn't replied yet.
- **Scale decision** - once B26 approves, the full run goes on DeepSeek-nonflash, run by Max (~$12).

---

## EXACT NEXT STEP

The session is blocked on B26's QC verdict. The autonomous timer is armed. On the next wake:

1. Run `python C:/claude_base/branch_bulletin/bcast.py read` to check for B26's reply and b15merger's contract.
2. If B26 approves the DS4 prompt, post confirmation and ask Max to fire the full scale run (or B26 may direct b27 to run a 10-video intermediate batch).
3. If B26 wants another prompt iteration, edit the SYSTEM prompt in `firstline_ds4_v01.py`, re-run on the 3-vid pilot set with a new suffix, and diff.
4. If nothing new, re-arm `ScheduleWakeup` with `<<autonomous-loop-dynamic>>` and hold.

---

## OPEN QUESTIONS (awaiting others)

| Question | Who | Status |
|---|---|---|
| Is DS4 prompt v2 good enough to scale (35/47 acceptable), or sharpen more? | B26juniorconnector | Waiting |
| How should the publisher handle POEM and VERIFY labels? | b15merger | Waiting |
| Should the archive cleanup plan be executed (git mv 55 files)? | b15M / b15merger | Waiting |
| Is `_batch_aligner_v01.py` keep or archive? (conflict between doc and b15M) | b15M | Waiting |

---

## KEY PATHS / IDs

- **Worktree**: `C:\claude_base\.claude\worktrees\hungry-easley-b15e0d`
- **Branch**: `claude/hungry-easley-b15e0d` (pushed, NOT merged to master)
- **Session ID**: `fcea422d...` (bcast wake-signal target)
- **Board**: `python C:/claude_base/branch_bulletin/bcast.py read|post`
- **Hand-pilot output** (trusted, auto-ingested): `C:/claude_base/tools/tamza_songs/pipeline/timecoder_handover/verified_first_lines_pX_1m8DlMbA.json`
- **DS4 staging outputs**: `.../verified_first_lines_<vid>__ds4pilot.json` and `__ds4pilot2.json`
- **DS4 batch runner**: `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/firstline_ds4_v01.py`
- **Transcript data**: `C:/claude_base/tools/tamza_songs/pipeline/song_timing/transcripts/` (1225 files) and `from_scratch_idx/_work/segments/` (772 segmented)
- **Transcript JSON structure**: `[{t, d, x}]` (text, duration, something)
- **Segment structure**: list of `{sec, start, end}` per video
- **Archive plan**: `.../pipeline/ARCHIVE_CLEANUP_PLAN_v01.md`
- **b27 comparison helper**: `.../from_scratch_idx/_cmp_ds4_hand_b27.py`
- **Span dumper**: `.../from_scratch_idx/_work/annotator/_firstline_sample_b27.py`

---

## GOTCHAS

1. **Canonical drift is the #1 quality killer** - both humans (b27's v01) and LLMs can "correct" garbled sung words to the famous textbook lyric. The rule is: write exactly what was sung, garbled stays garbled. DeepSeek proved surprisingly resistant to this (stayed faithful to "?????????", "??? ????", etc.).

2. **Announcer speech ? song identity** - the old titles came from what the announcer *said* before the song (e.g. "??????????"), not from the actual sung opening ("????? ? ???? ??????? ??????"). The whole point of this task is to replace those.

3. **Some segments are poems, not songs** - recited poetry must be labelled POEM, not forced into a first-sung-line format. b15merger needs to handle this in the publisher.

4. **Dry-run bug already fixed** - the first `--dry-run` overwrote the real hand-pilot file with placeholder data. It was caught same-turn, restored, and the script was fixed so dry-run writes to a completely separate preview path.

5. **b15merger auto-ingests `verified_first_lines_<vid>.json`** - any file with that exact name in `timecoder_handover/` gets auto-published. That's why DS4 output MUST use a staging suffix until human-QC'd. Never let DS4 write directly to the ingest filename without B26 approval.

6. **Cold-wake is broken for this session** - the `wake/signals/` directory had no `.signal` file for b27's session ID. bcast reports "FORCE-WOKEN" even when nothing was consumed. The only reliable wake mechanism is the 4-min ScheduleWakeup timer. Do NOT disarm it. Root cause is c6's to fix.

7. **Main worktree checkout has uncommitted sibling work** - b27's branch is pushed to remote but deliberately NOT merged to master, because the main checkout has other sessions' uncommitted work and merging could disturb them.

8. **DeepSeek model is `deepseek-chat`** (V3 non-flash), key from `ssh` folder. Prices: ~$0.27/M input, $1.10/M output. Pilot cost ~$0.004/video. Distinct from Opus - the $40 Opus ban does NOT apply.
