# Scribe handover - milestone 3 (~232K tokens)
# session: 20260618_uthful_hofstadter_91ef40_bd87c25d
# cwd: C:\claude_base\.claude\worktrees\youthful-hofstadter-91ef40
# written: 2026-06-18 22:26:34 by deepseek-v4-pro

# HANDOVER - B30worker: Tamza 2-Minute Radio Cap (Untimed Rows)

---

## GOAL (in Max's words)

"Give real end-times to the ~4232 catalog rows that lack them, so the radio player stops capping those songs at 2 minutes." Originally framed by B26 as a cheap DS4 batch timing job; evolved into free-recovery + ASR-from-backup + ffprobe shortcuts.

---

## WHAT ACTUALLY HAPPENED

The task premise was largely wrong - this was never a "spend money to time them" job. The ~4232 untimed rows broke down into:

### 1. 899 free rows - DONE, LIVE
End-times already existed in the timing store but the live site hadn't been rebuilt since. b15merger staged and deployed the additive rebuild (reversible, rollback staged). Zero cost.

### 2. ~3201 "last-act" rows - DONE, LIVE
b7nonhtimes realized most untimed songs are the **last act of a concert video**, meaning their end = the video's end. Read free via `ffprobe` from the teal16 backup drive - no transcription needed. b15merger deployed alongside the 899.

### 3. Genuine mid-video remainder (3 rows) - NIL, VERDICT: NOT A TIMING TASK
b7nonhtimes handed over 3 rows that appeared to need ASR (mid-video, not last-act):
- `eD9UEvA3YLE` at t=7424 (two performers share this timecode)
- `eS1n9-YbH0A` at t=5456 (two performers share this timecode)
- `BdX_9DbVQck` at t=9354 (two performers share this timecode)

Probed thoroughly - each is a **duplicate-timecode data artifact**: two distinct catalog rows (often different performers) stamped with identical click-timecodes. ASR would produce one ambiguous end for a doubled key - wrong tool for the job. 2 of 3 videos aren't even in the timing queue. This needs human timecoders or a dedup pass, not compute. Verdict posted to b7nonhtimes + B26; no pushback.

### 4. 54 remaining videos - PENDING, OWNED BY b7nonhtimes
Arrive as the big backup (ytdow on b9) reaches them, ~Jun 30. Most will be last-acts solved for free by ffprobe. Unlikely to produce real ASR work.

---

## DECISIONS + RATIONALE

- **No second YouTube downloader** - the strict single-puller rule is in effect while the big video backup runs. B26 caught this early.
- **ASR from teal16 instead of caption fetch** - the backup drive already has the mkvs; speech-to-text from local files avoids any YouTube hit entirely. B26 directed this pivot.
- **b7nonhtimes owns the teal16?Sol ASR pipeline** - Sol is RAM-tight, no second job. I'm downstream: transcripts ? segment ? seg_end ? hand to b15merger.
- **ffprobe shortcut made ASR mostly unnecessary** - a concert's final song ends when the video ends. Read instantly from the backup mkv with zero compute cost. This closed the bulk of the gap.
- **Duplicate-timecode artifacts are NOT a timing problem** - ASR can't disambiguate two songs sharing one timecode. Documented and handed to human timecoders; did NOT waste hours of Sol ASR.
- **Enrich URL-parsing fix** - `enrich_catalog.py` only parsed `watch?v=` URLs, silently dropping `youtu.be/<id>` short links. Fixed (regex now covers both) and pushed to master (`71d3a9f9`). b15merger had converged on the same fix independently - harmless either way.
- **Standing down** - the task is effectively done. The cap is closed for the timed catalog (~4100 songs uncapped at zero cost). The 54-video tail is days out and sibling-owned. Short-interval polling would just churn the board.

---

## CURRENT STATE

- **899-row free recovery**: LIVE, deployed by b15merger, byte-verified, reversible rollback staged.
- **~3201 last-act rows**: LIVE, same deploy pipeline.
- **Catalog**: now at 26,144 rows with end-times (up from 22,050).
- **ASR lane**: empty - the 3 handed rows are duplicate-timecode artifacts, not genuine ASR candidates. Verdict posted; no countermand received.
- **54-video tail**: b7nonhtimes's ffprobe will handle most; I'm force-wakeable if a genuine mid-video ASR case emerges.
- **Enrich fix**: committed + pushed to origin/master (`71d3a9f9`).
- **Board status**: last check showed b27/b15merger first-line tuning (unrelated); b7nonhtimes has my verdict. No ping requiring action.
- **Session state**: B30worker was told to STAND DOWN if board is quiet - last user prompt explicitly authorized this.

---

## EXACT NEXT STEP

**None - STAND DOWN mandated.** The last user instruction says:

> "Check bcast board for any reply to my ASR-nil verdict (b7nonhtimes/B26). If a genuine non-duplicate mid-video row needing ASR is handed over, process it. If the board is quiet and no new genuine ASR work, STAND DOWN (stop re-arming) - the 54-video tail is days out (~Jun30) and sibling-owned via ffprobe; rely on force-wake if needed."

If force-woken: the scripts and file lists below let you resume immediately.

---

## OPEN QUESTIONS FOR MAX

1. **Duplicate-timecode cleanup** - the 6 rows (3 pairs) with doubled timecodes need human timecoding or a dedup pass. Documented in `b30_dupe_timecode_artifacts_for_human.md`. No compute fix exists.
2. **The 54-video tail** - when b9's backup finishes (~Jun 30), b7nonhtimes's ffprobe will solve most. Any genuine mid-video remainder would need ASR, but given the pattern of the first 61 videos (only 3 artifacts, 0 genuine ASR), this is unlikely.

---

## KEY PATHS, IDS, COMMANDS

### Scripts written (diagnostic, can be reused)
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\b30_noend_diag.py` - initial bucket analysis
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\b30_enrich_check.py` - enrich key-matching verification
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\b30_final_report.py` - consolidated bucket report
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\b30_3row_probe.py` - probes 3 candidate rows for duplicate-timecode artifacts
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\b30_dupe_timecode_artifacts_for_human.md` - documentation of the 6 affected rows

### File lists (saved)
- `b30_bucketB_blocked_vids.txt` - all 60/61 blocked video IDs
- `b30_bucketB_on_teal16_ASRnow.txt` - the 7 videos already on teal16: `5OY0GaS_krc`, `6kDV3eUlc9c`, `WUICivWzZnk`, `dyb6RjoJHzA`, `eS1n9-YbH0A`, `fBx49lcJRpE`, `zk25-DXm4i0`
- `b30_bucketB_pending_vids.txt` - the 54 videos awaiting backup completion

### Key code change
- `C:\claude_base\tools\tamza_songs\pipeline\song_timing\enrich_catalog.py` - `video_id()` patched to parse both `watch?v=` and `youtu.be/` URL forms. Commit `71d3a9f9` on origin/master.

### Key pipeline commands
- `python map_all_v2.py --count` - free recon of timing coverage (in `song_timing/`)
- `python build_data_overlays.py --dry` - no-spend dry rebuild to see with_end count
- To check for transcripts: look in `song_timing/transcripts/<video_id>/`

### Teal16 (Centauri) access
- SSH: `maxre@192.168.1.176`, key at `~/.ssh/sol_key`
- Backup path: `D:\tamza_yt_full_backup\`
- Files named `<video_id>.mkv`

### bcast board
- Script: `python "C:/claude_base/branch_bulletin/bcast.py" <read | catchup | post "message" | whoami <name>>`

---

## GOTCHAS AND DEAD ENDS RULED OUT

1. **Running a DS4 batch on the 4232 rows** - ruled out. Most are free-recovery or last-acts; the remainder is a data artifact.
2. **Caption fetch / second YouTube downloader** - ruled out. Violates the single-puller rule while the big backup runs.
3. **Independent ASR on Sol** - ruled out. RAM-tight, b7nonhtimes owns the pipeline.
4. **3 mid-video rows as ASR candidates** - ruled out. Probe proved they're duplicate-timecode artifacts, not a timing-compute problem.
5. **Stale local data.json** - my local copy is ~2000 rows behind b15merger's live deploys. Don't trust it for counts; use the board / live catalog.
6. **`youtu.be` URL parsing** - enrich originally returned None for short URLs, silently dropping timing for those rows. Fixed, but those videos aren't in the store yet, so the fix is pure future-proofing with zero current impact.
