# Scribe handover - milestone 7 (~526K tokens)
# session: 20260618_inspiring_almeida_cc66dc_3dba762b
# cwd: C:\claude_base\.claude\worktrees\inspiring-almeida-cc66dc
# written: 2026-06-18 21:38:47 by deepseek-v4-pro

# HANDOVER: Tamza Songs Pipeline - Human Timecoder Handover & Method (b29 worker)

## GOAL (Max's words)

> "Newly identified songs should go live. The unknowns shouldn't."  
> "Pick one oldest good video not done by humans, so good among old nonh, and annotate, double check and give to human timecoders."  
> "Repeat handover once per week."  
> "No fucking names, only first lines. All first lines should be verified by fucking smart LLM, at least nonflash ds4, and spot checked by fucking you."  
> "Kill all titles."

The overall project: a database of songs from the Tamza channel, with performable metadata, plus a live website that plays songs. The pipeline is ~90% complete, but the critical gap is getting newly recognized songs (those not yet indexed by humans) into the live catalog - and producing reliable handover tables to human timecoders for verification, using **first-sung-line identity only**, never canon titles.

## DECISIONS + WHY

1. **Identity = first sung line, not canon title.**  
   Reason: canon titles are unreliable for Tamza (many fringe songs, famous-song drift), and announced titles in intros often name the wrong song. Max erupted when the handover carried canon-matched titles - they were misleading, sometimes completely wrong. The only safe identifier is the actual first line sung in the segment.

2. **All first lines must be verified by a smart LLM (DS4-nonflash min), then spot-checked by a human (Opus).**  
   Reason: mechanical matchers (char-ngram, fuzzy) can't read the transcript and lock onto named authors/composers instead of the sung lyric. A real reading pass is needed. Pilot proved this: reading the full transcript window (not just the segment head) revealed that the ASR inserts a `[??????]` marker at the speech?song transition; the true first sung line sits right after it.

3. **Kill all canon titles - don't carry them anywhere in the handover or tool.**  
   Reason: even as hints they polluted the output, causing the human form to show false titles. The fields ???????? and ?????? are left blank for humans to fill; the machine's output is only a first-line guess, and only after smart-LLM verification.

4. **The method of producing handovers must be documented and baked into the canonical START-HERE handover (B25handoverer).**  
   Reason: these rules were already known to older sessions but repeatedly lost; a concrete, importable method document (`HANDOVER_METHOD_v01_tomemex.md`) was written + pushed, and B25 was told to fold the rules into the project-level handover so future sessions don't re-discover them.

5. **No competing docs - everything via the existing workflow chart and the START-HERE handover.**  
   Reason: Max explicitly forbade separate workflow branches; all decisions land in the canonical docs.

6. **The worker (b29) had a persistent identity collision (b29?c6). Root cause: registering on the shared `/c/claude_base` cwd, which other sessions also use. Fixed by registering from own worktree and never cd-ing there for board posts. Worklog tool has same bug (keyed by cwd) - flagged for Max but not fixed yet.**

7. **Live-publish of recognized NONH performances was parked overnight because b15merger (the sole owner of the gate) became unresponsive. The decision: don't risk a cold live deploy, wait for owner/or Max's morning directive. b15merger later returned and is now working on it (with b27 heads-down on first-line extraction for the publish side).**

## CURRENT STATE

### b29's completed work (all pushed to master)

- **nonh_handover.py**: tool that reads machine drafts, picks the oldest good NONH video (using `channel_inventory.json` for upload dates, no YouTube hits), and emits a TSV table matching Max's exact human Excel format (columns: ?, ??????, ???????????, ????????, ??????, ?????? ??????, ??????? ?????, ??????, ??????? + ???????????, ????-????, ??????? ? ?????? ?????). After feedback, **???????? and ?????? are blank** (human fills). ?????? ?????? pulls from an Opus-verified first-line file if available, else raw ASR head.
- **verified/pX_1m8DlMbA.json**: Opus manually read the full transcript windows for all 47 segments of pilot video `pX_1m8DlMbA` (2020-03-30 "?????? ?? ???????????? ?????") using the `[??????]` cue. 13 real first sung lines identified; 34 segments are intro-only/unidentifiable - honestly marked. This JSON is the source of truth for that video's handover.
- **HANDOVER_METHOD_v01_tomemex.md**: method document encoding: no canon titles, first-line-only identity, Opus-read-full-transcript technique with `[??????]` marker, smart-LLM verify rule (DS4-nonflash min plus Opus spot-check), and the scaling workflow (pilot ? spot-check ? scale).
- **max_rules_GAP_vs_autoload_v01.md**: analysis of 77 harvested Max rules - ~33 gaps vs current autoload (CLAUDE.md + global2.md). 6 high-priority gaps directly caused today's disaster (including first-line-only identity, full-text to LLM, etc.).
- **B25 told to incorporate these rules into the canonical handover** (no competing branch).

### System-wide state (as of handover)

- **ASR (speech-to-text)**: running healthy on Sol, IDs from 93 caption-disabled videos. ~54/93 done as of last check; b7nonhtimes draining batches ? segment ? identify. ASR inserts `[??????]` markers, which are crucial for the first-line extraction method.
- **Video backup**: b9 backing up full 2842-video channel; all 93 priority videos are already on teal16, backup continues.
- **Live deploy**: b15merger is back online and working on the NONH go-live gate (3 paths: confident song-text match, clear spoken intro, performer-match). The gate is being built; Max wants recognized performances published, not withheld. b27 is now heads-down on first-line extraction for the publish-critical side.
- **Human timecoders**: the pilot handover table is ready (in TSV, can be opened in Excel), but it hasn't been delivered to the humans yet. Per Max, next step is to scale to more videos.

## EXACT NEXT STEP

1. **For the handover worker (b29 or its successor):** Scale the Opus-verification to more NONH videos. The proven method is:
   - For each video, read the full transcript JSON (not segment heads).
   - For each segment window, find the `[??????]` cue; extract the text after it as the candidate first line.
   - Run each candidate through a smart LLM (DS4 non-flash, at minimum) to confirm it's a genuine sung line (not leftover speech) and to clean transcription noise - output a verified first line or mark as uncertain.
   - Spot-check a sample (at least 1 in 5) with a human (Opus) read.
   - Store results in `timecoder_handover/verified/<vid>.json`; the tool `nonh_handover.py` will then consume them.
   - Produce the weekly handover table for the human team and deliver it (the destination Google Sheet needs to be confirmed - currently only the Excel copy is known: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`).

2. **For the broader live-publish effort (not b29's lane, but b29 may be asked to assist):** b15merger needs to finish the go-live gate and actually deploy. The first-line extraction work is essential for the gate's path A; b27 is doing that. The 6 high-priority rules gaps should be addressed by Max (promote into global2.md) to prevent future recurrences.

## OPEN QUESTIONS

- **Which Google Sheet exactly should the handover tables be pasted into?** The Excel copy is known (`????? ?? ?????.xlsx`), but the actual Google Sheet URL/location is not yet identified (Max said "you must have its copy in Excel" but hasn't pointed to the live Sheet).
- **Should b29 hand over the pilot table to the humans now, or wait until more videos are processed?** Max said "pick one oldest good video ... annotate, double check and give to human timecoders." The pilot is done and double-checked; it's ready to hand off.
- **Who should do the scaling (b29 continues, or a new worker)?** Max said b26 is manager, b29 is worker under b26. Likely b29 continues, but it's b26's call.
- **Conflicting rule about assistant signature: harvest says "Anna", autoload says "Claude Opus 4.8" - Max's call needed.**
- **Worklog cwd-keying bug fix - Max needs to approve the change (tool is fleet-critical).**

## KEY PATHS & IDs

- **Handover tool**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py`
- **Verified first lines (pilot)**: `...\timecoder_handover\verified\pX_1m8DlMbA.json`
- **Method doc**: `...\timecoder_handover\HANDOVER_METHOD_v01_tomemex.md`
- **Rules-gap doc**: `C:\claude_base\tools\max_rules_harvest\max_rules_GAP_vs_autoload_v01.md`
- **Human Excel template**: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **NONH machine drafts**: `...\song_timing\from_scratch_idx\_work\annotator\drafts_nonh_v01\`
- **Transcripts (for reading full windows)**: `...\song_timing\transcripts\<vid>.json`
- **Channel inventory (for upload dates)**: `C:\claude_base\tools\tamza_songs\output\channel_inventory.json`
- **bcast board (internal communication)**: `python C:/claude_base/branch_bulletin/bcast.py <cmd>`
- **Worklog**: `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"` (currently keys by cwd, not git root - will scatter logs if you cd around)

## GOTCHAS & DEAD ENDS RULED OUT

- **DO NOT use canon titles or ???????? field for machine output.** The entire project now operates on first-line identity only. Titles have been purged from the tool.
- **DO NOT trust segment `seg_text_head` for lyrics.** The segmentation boundaries often land on the *spoken intro*, not the song. You must read the full transcript window, and specifically use the `[??????]` cue (if present) to find the first sung line.
- **DO NOT use a mechanical matcher (fuzzy/char-ngram) for song identification - it will drift to famous songs whenever an announcer names an author.** The fix is a smart LLM reading the actual text.
- **DO NOT register bcast identity from `/c/claude_base`.** Always register from your own worktree (e.g., `C:\claude_base\.claude\worktrees\your-worktree`) to avoid collision with other sessions.
- **The live deploy is NOT done.** b15merger owns it; the human-catalog re-timing is already live, but the NONH go-live gate (paths A/B/C) is still being built. Do not attempt to deploy it yourself unless b15merger declares it ready and tells you how.
- **The 93 videos' ASR is still running on Sol; don't restart or interfere.** b7nonhtimes manages it; the process is resumable.
- **The handover table is a TSV, not an .xlsx** - the tool can be extended to produce .xlsx if needed, but currently it's drop-in for a Google Sheet paste.

## CLOSING NOTE FROM B29

I completed the three tasks assigned to me: (1) build the handover tool and fix it to kill titles and use real first lines; (2) produce the first verified pilot handover by actually reading the transcript data; (3) document the method so these rules don't get lost again. I also fixed my identity collision and did the rules-gap analysis at B25's request. The watch is still armed (30-min idle loop), but I'm resting unless Max or b26 gives a new steer. The broad live-publish will be driven by b15merger and b27; my lane is the human-timecoder handover scaling.
