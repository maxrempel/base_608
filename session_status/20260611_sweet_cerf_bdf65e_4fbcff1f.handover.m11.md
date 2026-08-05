# Scribe handover - milestone 11 (~169K tokens)
# session: 20260611_sweet_cerf_bdf65e_4fbcff1f
# cwd: C:\claude_base\.claude\worktrees\sweet-cerf-bdf65e
# written: 2026-06-11 16:11:33 by claude-opus-4-8

# HANDOVER - You are B8

## YOUR IDENTITY (just changed)
Max just split the branch. **You are now B8.** Your single job: **finish the downloads/timing of the 57 caption-disabled videos** (the "fill57" job running on Sol). Your copy, B7, takes over the separate "fix starts" job (re-snapping starts/ends on the 452 already-live videos). Do NOT do B7's work - that is now a different branch. Stay in your lane: the 57.

## GOAL (in Max's words)
The overarching mission across this whole effort: build a *"continuously fucking improving db"* of song timings so the "????? ??????" radio player on tamza.com/kartoteka plays the song only (real start ? real end), not a flat 120-second cap. Max owns the Tamza bard-song catalog. He wants timings to land in the catalog automatically and keep improving "until everything is indexed," expecting "further periodic updates."

Your slice: the 57 videos whose captions were disabled by the original uploader (Max owns the channel but a different account uploaded them with captions off). Because there are no YouTube captions, you must **download the audio yourself, transcribe it (Groq Whisper), map song boundaries, and fold the timings into the catalog** - reaching 509/509 videos covered.

## KEY DECISIONS + WHY
- **Run everything on Sol, not the local machine.** Max said his laptop overheats AND he explicitly wants Sol stress/resilience-tested (it recently crashed). Quote: "i need stress test it."
- **Groq whisper-large-v3-turbo** for transcription (~$6 for the batch), NOT Deepgram (~$40) or OpenAI Whisper (~$54). Why: Groq is ~9x cheaper for the same Whisper model, and it's the exact engine Max's own yt.dnaresonance.com service already uses. A Groq key already existed on Lak.
- **Download 720p video (not audio-only).** Max wanted speed, but chose 720p because the video files double as a Tamza backup copy. Audio is then extracted from the 720p file for Groq. "download 57 videos full size, like 720p, not more!!!"
- **Cap downloads at ?33% of measured bandwidth.** Max insisted I MEASURE, not guess. Measured Sol?Cloudflare = 220 Mbps (27.5 MB/s); 33% ? 9 MB/s; set yt-dlp `--limit-rate 8500K` (~31.6%). In practice YouTube throttles us to ~3 MB/s anyway, well under cap = low ban risk.
- **Human-paced, slow downloads** to avoid a YouTube ban (GAP_MIN,GAP_MAX=60,180s between videos; per-fragment sleeps).
- **Let all 57 finish, THEN fix collisions in one pass** (Max said "you decide"). See gotcha below about the 2-song collisions.
- **Scripts committed to git** per Max's explicit instruction.

## CURRENT STATE
- The **fill57 job is RUNNING on Sol**, PID was 15877. As of last check: **6 of 57 videos done**, worker alive on #7, ~$0.11 spent total, zero failures. Every song so far gets both a start and an end. Full chain (720p download ? ffmpeg audio ? Groq Whisper Russian ? DeepSeek map_core ? store) is PROVEN working on video 1 (44/44 songs).
- A **cron guard** (`*/10`) relaunches the worker if it dies (`fill57_guard.sh`) - this is the resilience test. Resumable via `fill57_state.json`.
- A **background watcher** (task ID brvqccimu) sits on Sol waiting for the `fill57.done` flag and will notify you when all 57 complete. No self-wake timer (FULL HALT is in effect - do NOT arm ScheduleWakeup).
- **Already LIVE and done (not your action item now):** the 21,481 timings from the 452 caption videos were folded into data.json (26,283 rows, 21,569 ends, was 4,979) and deployed to R2. Byte-verified, reversible.

## EXACT NEXT STEP
Wait for the watcher (brvqccimu) to fire on `fill57.done`. While waiting, periodically (not tightly - the suicide-hook blocks repeated identical commands) verify progress by reading Sol's `~/song_timing/fill57_state.json` and `song_timing.json`. When all 57 finish:
1. Do the **collision-fix pass** (reject any seg_start that lands on top of the next song's start - see gotcha).
2. Re-pull Sol's `song_timing.json` to Pine.
3. Run `enrich_catalog.py` ? `apply_overrides.py` ? `deploy_catalog.py --data`, **routed through the b0 gate** (a sibling now claims b0; coordinate via bcast).

## GOTCHAS
- **2-song collisions:** On video 1, 2 of 44 starts jumped 180-276s and landed on the NEXT song's start (mapper couldn't find the opening lyric, slid forward). This is the known defect to fix in the end pass. It's VISIBLE in the data (not a silent fallback) - good.
- **fill57 saves segments to `segs57/`, NOT `boundaries/`.** A verify query looking in `boundaries/` will FileNotFoundError. Check the STORE (`song_timing.json`) for start/end sanity instead.
- **Store keys are `<vid>:<start_sec>`** (start from catalog `&t=`, video id from `?v=`).
- **bcast.py identity is cwd-keyed:** call by full forward-slash path with NO `cd` first, or it fails "no id set for this branch."
- **Suicide-prevention hook** blocks the 3rd repeat of a normalized Bash/Read command - write reusable scripts, vary commands early, don't loop `python -c`.
- **/tmp doesn't resolve for Windows Python** - use real Windows paths.
- **Cyrillic prints crash cp1252** - prefix `PYTHONIOENCODING=utf-8`.
- **NEVER translate transcripts** (ban risk); keep Russian source. **NEVER touch Max's Google/YouTube login.**
- **Don't ask Max for a wrong-songs correction list** - he got angry ("i didn't ever promised any song error lists. Don't fucking bother."). The overrides file stays empty and ready; never raise it again.
- **A sibling now claims it IS b0** and says I can't grant gates. Doesn't matter until a deploy is pending; route the final deploy through whoever holds b0 then.
- **Output style:** pingpong, TLDR-first, plain English, sanctioned colored-circle markers only (? TLDR, ? danger/shortcut, ? burning question), warn loudly about shortcuts, no silent fallbacks.

## KEY PATHS / IDS
- Sol: `maxre@192.168.1.113`, key `~/.ssh/sol_key`, residential IP (YouTube-safe). Pipeline dir `~/song_timing/`, venv `~/song_timing/venv`.
- Sol files: `fill57_groq.py`, `fill57_guard.sh`, `fill57_state.json`, `fill57.log`, `fill57.done` (flag), `song_timing.json` (the store), `queue.json`, `map_core.py`, `missing_vids.txt` (the 57), `vids720/` (720p backups), `audio57/`, `segs57/`, `groq_api_key.txt`.
- Pine pipeline: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\` - `fill57_groq.py`, `fill57_guard.sh`, `enrich_catalog.py`, `apply_overrides.py`, `manual_overrides.json` (empty, ready), `_work\song_timing.json` (Pine store).
- Pine catalog: `pipeline\output\data.json` (live artifact, byte-identical to R2). Deploy: `pipeline\scripts\deploy_catalog.py` (flags: none=both, `--data`, `--appjs`; auto-backs-up + byte-verifies + reversible via `rollback_catalog.py`).
- Live URLs: `https://tamza.com/wp-content/kartoteka/data.json` and `.../app.js`.
- Groq key (canonical): `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt`.
- bcast: `C:/claude_base/branch_bulletin/bcast.py`. Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py`.
- Watcher task waiting on done-flag: **brvqccimu**.

## OPEN QUESTIONS AWAITING MAX
None pending for B8 right now. (Do NOT re-raise the corrections list. Do NOT cross into B7's "fix starts on the 452" job.)
