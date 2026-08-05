# Scribe handover - milestone 1 (~147K tokens)
# session: 20260701_amazing_perlman_1521cf_6b598cec
# cwd: C:\claude_base\.claude\worktrees\amazing-perlman-1521cf
# written: 2026-07-01 12:09:25 by deepseek-v4-pro

## Handover - Max & Noeticus Interview Editing (2026-06-30)

### GOAL (in Max's own words)
> "You should repeat the path which was already developed, the method of cutting out the silence and using your LLM, basically looking at the actual text and analyzing the retakes and keeping only the last one ... and also ... when one person is speaking, then another one should be silenced ... I think the principle was that we first put keyframes very frequently ... every 0.5 seconds ... that would be enough to do the cutting without re-rendering."

In short:  level the two individual speaker tracks, re?encode the video with dense keyframes, then apply a cross?talk gate (silence the non?speaking person) and a retake cleaner (keep only the last take of each segment), all using stream?copy cuts so nothing re?renders later.

---

### DECISIONS MADE & WHY

1. **Track identification** - The input MKV has three stereo audio tracks:
   - **Track1 = mix** (both voices) ? **ignored**
   - **Track2 = Noeticus** (very quiet mic)
   - **Track3 = Max** (louder mic)  
   *Why:* FFprobe volume detection, subtraction tests (T1 minus T2+T3 gave best silence at -54 dB), and Max listening to full-length exports confirmed this.

2. **Leveling & normalisation**
   - Applied **`dynaudnorm`** (dynamic normalisation with a sliding window) to even out level drift within each track over time.
   - Then **loudnorm** to **?16 LUFS** (integrated) for every track.
   - *Why:* Max wanted both speakers equally loud and no manual fader riding. The target -16 LUFS was chosen as a common broadcast standard; final measured levels were all within 0.2?dB of that target, verified with `ffmpeg ebur128`.

3. **Dense?keyframe master**
   - Re?encode the video **once** with a keyframe every **0.5?s** (15 frames at 30?fps) and burn in the **two separate leveled audio tracks** (Max & Noeticus) as separate streams.
   - *Why:* User specified 0.5?s precision; a keyframe every 0.5?s means any later cut (cross?talk gate, retake removal) can be done with `-c copy` (stream copy on video), avoiding a full re?render. This one re?encode is the only lossy video pass.

4. **Transcripts - no diarisation**
   - Each speaker's leveled track will be transcribed **separately** with Deepgram nova?3 (English).
   - *Why:* Since we have clean, isolated speaker tracks, diarisation is unnecessary and error?prone. Separate transcription gives perfect speaker labels and will later feed the LLM for retake detection.
   - Language was auto?detected from a 30?s sample ? **English** (confidence 0.99).

5. **Retake rule**
   - When multiple takes of the same line appear, **always keep the LAST one**, never the middle or first. The LLM will be instructed accordingly.

6. **No merge yet**
   - Max explicitly said: *"Don't merge them until I approve."* So all processing currently keeps the two speaker tracks separate; the final mix will happen only after editing and cross?talk gating, when Max gives the go?ahead.

---

### CURRENT STATE - WHAT IS DONE / IN FLIGHT

**Done & accepted:**
- All four speaker tracks leveled & normalised to -16?LUFS:  
  `01_leveled/part1_Max_leveled.mp3`, `part1_Noeticus_leveled.mp3`, `part2_Max_leveled.mp3`, `part2_Noeticus_leveled.mp3`.  
  Verified by measurement and accepted by Max.

**In flight (background jobs running in parallel):**
- **Dense?KF master encoding** (script `make_kf_master.sh`):
  - Part?1 (`2026-06-30 15-19-01.mkv`, 25?min) and Part?2 (`2026-06-30 15-52-35.mkv`, 85?min).
  - Output will land in something like `02_kf_master/` (the script creates an output folder; re?check after it finishes).
  - This is a **heavy job** - Part?2 alone is 85?min of 1080p re?encoding.

- **Transcript generation** (script `transcribe_speakers.py`):
  - Deepgram jobs for all four leveled tracks (2 speakers ? 2 parts) + merged conversation files per part.
  - Output JSON & plain merged text will be written to a `transcripts/` directory.

Both processes are running in the background on the current worktree. They will have completion notifications/logs. **Do not start a new session assuming they are done** - first check their status.

---

### EXACT NEXT STEP

1. **Wait** for the two background tasks to finish:
   - Dense?KF master encoding (likely the longest).
   - Transcript generation.

2. Once complete, **inform Max** and summarise:
   - Paths to the KF?master files.
   - Paths to the transcript JSONs & merged text files.
   - Confirm all outputs look sane.

3. Then the **editing pipeline** - two new work items (likely in parallel or ordered by Max):
   a) **Cross?talk gate** - for every timestamp where speaker A is speaking, silence speaker B's track (and vice versa). Use the per?speaker transcripts (or the KF?master's separate audio) to build the gating intervals.
   b) **Retake cleaning** - feed the merged transcript (or per?speaker transcripts) to an LLM, instruct it to identify retakes and keep **only the last one**, then produce a cut?list that can be applied to the KF?master via stream?copy.

   *Note:* Max said he would "spin a branch of you to do the editing of the transcript to remove the unnecessary parts." This may mean he wants to open a separate assistant session for the transcript editing, so ask whether to proceed immediately or hand the transcript to that branch.

---

### OPEN QUESTIONS (awaiting Max)

- After KF?master & transcripts are ready, should we **directly build the cross?talk gate + retake cleaner**, or does Max want to **spin a separate branch first** to manually review/edit the transcript?
- Any preferred output format for the final edited video (container/codec/bitrate) or stick with the same as source?
- Is Max happy with the -16 LUFS loudness, or should it be adjusted later?

---

### KEY FILES & PATHS

- **Source videos**:  
  `C:\Users\maxre\Videos\2026-06-30 15-19-01.mkv` (Part?1, 25?min)  
  `C:\Users\maxre\Videos\2026-06-30 15-52-35.mkv` (Part?2, 85?min)

- **Project root**:  
  `C:\Users\maxre\Videos\podcast_cleanup\max_interview_20260630\`

- **Leveled audio (done)**:  
  `.../01_leveled/part1_Max_leveled.mp3` (?16.0?LUFS)  
  `.../01_leveled/part1_Noeticus_leveled.mp3` (?16.1?LUFS)  
  `.../01_leveled/part2_Max_leveled.mp3` (?16.1?LUFS)  
  `.../01_leveled/part2_Noeticus_leveled.mp3` (?16.2?LUFS)

- **Processing scripts**:  
  `.../code/level_normalize.py` - leveling & normalisation (already run)  
  `.../code/make_kf_master.sh` - dense?keyframe re?encode (running)  
  `.../code/transcribe_speakers.py` - Deepgram transcription (running)

- **Logs**:  
  `.../logs/level_normalize.log`, `.../logs/make_kf_master.log`, `.../logs/transcribe.log`, `.../logs/lang_probe.json`

- **Existing method docs (reference)**:  
  `C:\claude_base\tools\retake_cleaner\retake_cleaner_v06_tomemex.md`  
  `C:\claude_base\tools\podcast_cleanup\podcast_cleanup_method_v01_tomemex.md`

- **Secrets**:  
  Deepgram API key in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\deepgram_key_20260515.txt`

- **Work?log (new entry)**:  
  Already logged via `C:\claude_base\compaction_kb\scripts\worklog.py` with the milestone "identified tracks, leveled, KF?master & transcripts started".

---

### GOTCHAS & DEAD ENDS RULED OUT

- **Don't confuse Track1 with a speaker** - it is the mix and of no use; we work exclusively with Track2 (Noeticus) and Track3 (Max).
- **Quiet?mic hiss**: Noeticus's track is ~20?dB quieter than Max's. Levelling it up makes background hiss audible during Max's turns. That will be fixed by the cross?talk gate (silence the other track when a speaker isn't talking). Do **not** apply aggressive noise?reduction before gating, or it may damage voice quality.
- **Keyframe precision**: The 0.5?s keyframe interval is **user?specified** and cannot be changed later without re?encoding. Do not use a coarser interval.
- **No re?rendering after KF master**: All subsequent cutting *must* use `-c copy` on the video stream. The KF?master re?encode is the only lossy video pass.
- **Last?take rule**: The retake cleaner must be explicitly instructed to keep the **last** take, never any middle one. The user was emphatic about this.
- **Parallel processing**: The current session launched two heavy background jobs. A new session **must check their status first** (read the logs and list expected output files) before proceeding to any cutting/gating steps. Do not assume they succeeded.
- **No video mix yet**: Don't produce a merged stereo mix until Max asks for it, and even then, likely only after editing. Keep the two audio tracks as separate streams in the KF?master so the gate can operate independently.
