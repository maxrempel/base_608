# Scribe handover - milestone 2 (~166K tokens)
# session: 20260701_heuristic_tharp_6eb176_c8babc3a
# cwd: C:\claude_base\.claude\worktrees\heuristic-tharp-6eb176
# written: 2026-07-01 16:17:25 by deepseek-v4-pro

# HANDOVER - Max + Noeticus Interview Editing (2026-06-30)

## GOAL (in Max's words)
Assemble yesterday's video recording using the already-developed pipeline: cut out silence, use LLM to analyze retakes in the transcript, and **keep only the last take - never the middle one, always the last**. Clean up noises so that when one person is speaking, the other speaker's track is silenced. This is Max's own interview (not the earlier Oleg one). Eventually spin a branch to handle transcript editing while this session supervises.

## DECISIONS MADE + WHY

1. **Track identification**: Both MKV files have 3 audio streams. By subtraction analysis (T1 minus (T2+T3) = -54 dB residual vs. other hypotheses giving worse cancellation), determined:
   - **Track 1** = stereo mix (IGNORE - contains both voices)
   - **Track 2** = Noeticus (quiet speaker, ~-41 dB raw) - this is Claude/Opus in a browser
   - **Track 3** = Max (loud speaker, ~-21 dB raw)
   - Max confirmed by ear: "loudspeaker is Max, quiet speaker is Naeticus" (spelled Noeticus)

2. **Two separate recordings, not one**: The folder had multiple 2026-06-30 files. Only two are real:
   - `2026-06-30 15-19-01.mkv` = Part 1 (25 min)
   - `2026-06-30 15-52-35.mkv` = Part 2 (85 min)
   - Other files are 1-70s false starts ? ignored. Total ~110 min.

3. **Leveling pipeline** (user accepted): Two operations per speaker track, kept SEPARATE (no merge until user approves):
   - `dynaudnorm` - levels across time (evens out mic drift minute-to-minute)
   - `loudnorm` to -16 LUFS - both speakers matched to the SAME target loudness
   - Verified: Part 1 Max = -16.0 LUFS, Noeticus = -16.1 LUFS; Part 2 Max = -16.08, Noeticus = -16.22. Within 0.2 dB.

4. **Dense keyframe master** (user's instruction): Re-encode video with a keyframe every **0.5s** (= every 15 frames at 30fps). This is "the precision we need" to do all subsequent cutting via stream-copy with no re-render. User iterated from 0.7s ? 0.6s ? settled on 0.5s. This is the ONE intentional re-encode. Outputs are large (7.3 GB total) but regenerable and git-ignored.

5. **Transcript generation**: Deepgram nova-3, English (auto-detected, 0.99 confidence). Each speaker transcribed **separately from their own leveled track** - gives perfect speaker attribution without needing diarization. Also generated merged conversation text files (`part1_conversation.txt`, `part2_conversation.txt`).

6. **Git versioning**: Committed v01 (`b8f0a65`). All light files (code, transcripts, README, logs) are versioned. Heavy media is git-ignored (regenerable from sources + code).

## CURRENT STATE

| Stage | Status |
|-------|--------|
| Track identification | ? Done, user confirmed |
| Audio leveling + normalization | ? Done, user accepted |
| Dense-KF masters | ? Done, verified (keyframes exactly every 0.5s) |
| Per-speaker transcripts | ? Done (English, Deepgram nova-3) |
| v01 git commit | ? Done (`b8f0a65`) |
| Cross-talk silencing gate | ? NOT YET BUILT |
| Retake cutting (keep-last-take) | ? Waiting on branch |
| Merge into final output | ? Not yet - user wants to audition first |

**Two retakes already spotted** in Part 1 transcript for the branch:
- Turn 1: pre-interview direction ("start again", "don't reference human colony") ? cut
- Turn 5: explicit abandoned take ("I forgot to hold the record button... previous answer should be deleted, now starting again") ? cut up to the restart

## EXACT NEXT STEP

Max said he would **spin a branch** to do the transcript editing (read the conversation transcripts, produce a keep/cut list following the keep-last-take rule). This session acts as **supervisor**: review the branch's cut list against the rule, then build the cross-talk gate + execute the stream-copy final cut. The branch should be pointed at the README for full task briefing.

The cross-talk gate implementation is defined but not coded: use diarization timestamps (or per-speaker transcript timestamps since each speaker was transcribed separately) to build per-speaker gates - during speaker A's segments, silence speaker B's track entirely, and vice versa. Because the KF master has separate audio streams, this is a matter of applying gain=0 to one stream during the other's segments and then mixing.

## OPEN QUESTIONS AWAITING USER

- Nothing pending from Max. He needs to spin the branch for transcript editing. Once the branch posts a cut list, review it.

## KEY PATHS, FILES, IDS

**Project root**: `C:\Users\maxre\Videos\podcast_cleanup\max_interview_20260630\`

| What | Path |
|------|------|
| Source Part 1 | `C:\Users\maxre\Videos\2026-06-30 15-19-01.mkv` |
| Source Part 2 | `C:\Users\maxre\Videos\2026-06-30 15-52-35.mkv` |
| Leveled audio outputs | `...\01_leveled\part1_Max_leveled.mp3`, `part1_Noeticus_leveled.mp3`, `part2_Max_leveled.mp3`, `part2_Noeticus_leveled.mp3` |
| Un-leveled samples (for A/B) | `...\samples\FULL_Track1_MIX.mp3`, `FULL_Track2_quiet_speaker.mp3`, `FULL_Track3_loud_speaker.mp3` |
| KF master (Part 1) | `...\03_kf_master\part1_kf_master.mkv` |
| KF master (Part 2) | `...\03_kf_master\part2_kf_master.mkv` |
| Transcripts (JSON, per speaker) | `...\02_transcript\part1_transcript_Max.json`, `part1_transcript_Noeticus.json`, `part2_transcript_Max.json`, `part2_transcript_Noeticus.json` |
| Merged conversation text | `...\02_transcript\part1_conversation.txt`, `part2_conversation.txt` |
| Code (leveling) | `...\code\level_normalize.py` |
| Code (KF master) | `...\code\make_kf_master.sh` |
| Code (transcription) | `...\code\transcribe_speakers.py` |
| README / branch briefing | `...\README_tomemex.md` |
| Deepgram API key | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\deepgram_key_20260515.txt` |
| Existing retake cleaner method | `C:\claude_base\tools\retake_cleaner\retake_cleaner_v06_tomemex.md` |
| Existing podcast cleanup method | `C:\claude_base\tools\podcast_cleanup\podcast_cleanup_method_v01_tomemex.md` |
| Git commit | `b8f0a65` (v01) |

## GOTCHAS / DEAD ENDS RULED OUT

- **Track identification was non-trivial**: Track2 is silent in the first 2 minutes (only Max speaks), so early volumedetect on the first segment was misleading. Solved by measuring mid-file (ss=700s) where both speak, plus analytical subtraction. Track1 minus (Track2+Track3) gave the best residual at -54 dB, confirming Track1 = mix.

- **Noeticus is ~20 dB quieter raw**: Leveling it up to match Max will also raise background hiss during Max's speaking turns. This is exactly what the cross-talk gate solves - if the hiss bugs Max during audition, the gate is the next step. This is a known caveat, not a bug.

- **The Oleg interview folder is empty**: The earlier podcast cleanup work on Oleg was done in a different session/worktree. The method docs exist but the actual output files for Oleg are not at `podcast_cleanup\riverside_ep02\` (empty). The retake method itself is documented and reusable.

- **The smaller 2026-06-30 files are false starts** (1-70 seconds each) - ignore them, only the two real MKVs matter.

- **Cross-talk silencing is NOT built yet** - it was identified as a gap at the start of the session, the data exists (separate speaker tracks + timestamps from transcripts), but implementation has not started. This must be done after transcript editing produces the keep/cut list.

- **KF masters are 7.3 GB total** (5.6 GB for Part 2 alone). That's expected from a keyframe every 0.5s. Fine on the 476 GB drive, and they're regenerable + git-ignored. Can be deleted after the final cut is produced.

- **The pipeline avoids re-rendering**: After the one-time KF master encode, all cutting is stream-copy (ffmpeg `-c copy`), which is instant and lossless. The 0.5s keyframe interval is the precision budget for those cuts.

- **Speaker attribution is perfect** because each speaker was transcribed separately from their own isolated mic track - no diarization guesswork needed. The merged conversation text was built from the two separate transcripts.
