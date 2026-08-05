# Scribe handover - milestone 4 (~301K tokens)
# session: 20260617_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-17 23:35:11 by deepseek-v4-pro

# TAMZA HANDOVER - B26juniorconnector (junior connector/poker, in charge overnight)

## GOAL (Max's words)

Max brought me (B26juniorconnector) in as a **junior manager/connector/poker** - not a doer yet, but someone who reads the whole picture, relays decisions to the owners, lets them design, and keeps things moving. The project is near the end point: a clean database plus live catalog. **Newly identified songs should go live; unknowns shouldn't.** Also one hands-on task: pick the oldest good not-human-done NONH video, annotate it, double-check, and hand it to the human timecoders. Plus a weekly handover. Later Max gave me B27 as a worker to manage, and put me in charge with a 4-minute autonomous wake timer while he slept.

The core tension Max enforced: **(A) push the ready safe things live NOW, don't over-hold**, but (B) **don't lose/delete data** - back up live before deploy, keep unknown/held on disk, stay reversible.

---

## DECISIONS MADE + WHY

### 1. Go-live gate: 3 OR-paths, not just song-match
- **Path A**: segment text matches a known song in the 994-song reference (confident cluster match)
- **Path B**: clear spoken intro explicitly names the song ("this is my song" / names composer-poet)
- **Path C**: the spoken performer name in the intro matches the clean performer DB (Max's refinement: "if a performer says: this is Berkovsky/Nikitin/Sukharev - clear too")
- A segment that fails ALL THREE stays held as UNKNOWN.
- **Why**: song-match alone only catches ~12-20% on fringe/old videos, and those matches are often WRONG (famous-song drift - the machine reaches for famous songs, Tamza sings fringe ones). Paths B and C capture many more segments safely via performer attribution. Max wants the safe stuff live, not held.

### 2. Famous-song drift / Path A is unsafe as live-truth
- Independent LLM review of my handover table confirmed: ~half the "KNOWN" song titles on an old video (pX_1m8DlMbA, 2020) were WRONG - the matcher drifted to famous songs that contradict what was actually sung. Performers were mostly right.
- **Decision**: Path A titles on old/fringe videos should be marked "verify" not published as fact. Path C (performer matches DB) is the safer publish path. Max agreed - wrong titles aren't dangerous if marked uncertain and humans fix later; the real risk is losing data.
- **Max's override**: stop being afraid - publish the recognized performances now (cat 2 especially), just back up first and keep rollback.

### 3. Human-side remap catalog is ALREADY LIVE
- I ran `publish_catalog.py --dry-run` (safe, no deploy) to check readiness. Result: **"NO CHANGE since last publish - nothing to deploy."** 26,283 rows, 22,051 timed ends match the live SHA. The re-timing push Max ordered was already done.
- **Why this mattered**: I nearly wasted time trying to push something already live. The dry-run homework saved that.

### 4. Archive cleanup (B27's task) - staged for owner sign-off
- Assigned B27 to produce a concrete move-plan for archiving 55 legacy scripts + 2 data files. B27 delivered it fast: grep-verified **zero live imports**, flagged 4 unlisted files for owner decision, and found one doc/reality conflict (`_batch_aligner_v01.py`).
- **Decision**: execute the clean set on its own branch, hold merge until owners (b15M, b15merger, b15A, b7nonhtimes) sign off. b9 already approved. b15M was woken for the conflict file and stage-acks.
- **Why**: this is the literal root cause of branching bloat in the project - safe to clean, but collective approval per Max's instruction.

### 5. ASR (Sol speech-to-text) - the real blocker, now unblocked
- 93 NONH videos had no captions, needing Sol ASR. Sol was off-limits during RAM tests.
- When Max said Sol would be available, I **SSH'd teal16 directly** (Centauri) and counted: **82 of the 93 mkv were already staged there** from b9's pace-pass. Only 11 still pulling.
- Told b7nonhtimes to launch ASR immediately on the 82 ready videos. It adapted its script to pull audio from teal16 (not YouTube), launched detached on Sol.
- **Verified independently**: PID alive, `transcribe_v02.py` running, real Russian transcripts accumulating in `~/nonh_transcribe/out/`, crash.log clean. ~9 min per video on CPU ? many hours overnight.
- **Decision**: b7nonhtimes owns the full chain (ASR ? QC (many LLM passes per Max's instruction) ? segment ? b15A handoff). I'm watching, not interfering.

### 6. Handover table for human timecoders
- Picked oldest good NONH video not done by humans: **pX_1m8DlMbA** (2020-03-30, "?????? ?? ???????????? ?????", 47 segments, 10 identified).
- Discovered the human team's exact Excel format by reading the real `????? ?? ?????.xlsx` (one sheet per concert, 11 columns, performer-grouped).
- Built a reusable tool: `nonh_handover.py` with `pick` (oldest good video by upload date) and `table` (emits TSV in exact human Sheet format with performer grouping, timecodes, links, machine guesses).
- **LLM-reviewed ONCE** - caught the famous-song drift, weak first-line cells (spoken intro instead of sung line). Added warning row. NOT yet multi-pass vetted (Max wants "many times" with LLM).
- **Handed over the tool + first table** (pX_1m8DlMbA), ready to paste as a new concert tab in their Sheet.

### 7. b15merger's live publish - Max wants it TONIGHT
- Originally I over-held ("nothing NONH goes live tonight, wait for morning thresholds"). **Max pushed back hard** - wrong. The safe performer-introduced matches should go live NOW, not wait. Only hold the drift-risky cat 1 (cluster-match titles) and true unknowns.
- Redirected b15merger with loosened directive: publish recognized performances now, back up first, keep held set, reversible.
- **Status at last tick**: b15merger heads-down on it, not yet reported. Pinged once, no re-direct.

---

## CURRENT STATE (what is DONE vs IN FLIGHT)

### DONE:
- **Human-side catalog**: re-timed and **already live** (26,283 rows, 22,051 timed - confirmed via dry-run).
- **NONH machine indexing pipeline**: captions fetched (691/784), songs split by spoken-intro boundaries, 994-song frozen reference built, every segment matched as KNOWN or UNKNOWN.
- **Performer de-duplication**: live on the site.
- **Website features**: voting, login, playlists - live.
- **My handover tool + first table** (pX_1m8DlMbA, 2020-03-30): committed + pushed to master.
- **82/93 caption-less videos staged on teal16** (confirmed via SSH).

### IN FLIGHT:
- **ASR on Sol**: running detached (b7nonhtimes, PID 52723, `transcribe_v02.py`), 3/82 transcripts done initially, grinding overnight. Full chain to follow: repeated LLM QC passes per transcript ? segmentation ? b15A handoff.
- **Live publish of NONH recognized performances**: b15merger building/deploying the 3-path gate, Max wants cat 2 (performer-introduced) live tonight. Not yet reported complete.
- **Archive cleanup**: B27's plan ready, awaiting owner sign-offs (b15M, b15merger, b15A, b7nonhtimes). b9 approved. Executable on branch immediately.
- **b9**: pulling last 11 caption-less videos, ytdow backup ~290/2842 (ETA ~Jun24-30).
- **b7nonhtimes**: ASR running, then QC + segment + handoff to b15A for the 82+11 videos.

### NOT YET DONE / HELD:
- **NONH go-live gate fully deployed**: b15merger working it. The 3-path rule is set; the mechanism needs building and dry-running.
- **93-video ASR-to-segment chain**: only ASR started; QC, seg, match, identify all downstream.
- **Handover table multi-pass LLM vetting**: only one pass done. Max wants "many times" before it reaches humans.
- **Archive moves**: plan ready, not executed (owner sign-off pending).
- **Weekly handover cadence**: tool built, but the recurring process not yet established.

---

## EXACT NEXT STEP

1. **Confirm b15merger's live publish landed** - check board for report; if still silent after another tick, light status-check again. This is Max's top priority (recognized performances live, not held).
2. **Verify ASR progress on Sol** - next tick or the one after, SSH again and count transcripts in `~/nonh_transcribe/out/` to confirm steady progress. No action needed unless it died.
3. **Run multi-pass LLM vetting on the handover table** - Max's explicit requirement. Safe read-only analysis: re-check every KNOWN match against the heard text, flag/strip first-line cells that are intro chatter, sanity-check performer grouping.
4. **Release B27's archive clean moves** as soon as b15M ack's the conflict file - execute on branch, hold merge.
5. **Keep 4-minute autonomous watch** re-arming until Max wakes.
6. **Establish the weekly handover cadence** - tool is built, process not yet documented.

---

## OPEN QUESTIONS (awaiting Max or owners)

- **Max's go-live thresholds for morning**: the exact confidence/performer-match thresholds for paths A, B, C still need Max to tune when he's up. b15merger to produce a go-live-vs-held split + sample for that.
- **b15M's ack on archive conflict file** (`_batch_aligner_v01.py` doc-vs-reality) - needed before B27 executes that stage.
- **b15merger's publish status** - did it deploy? What went live? What was held?
- **Human timecoder Google Sheet format confirmation** - I matched the local Excel copy exactly, but Max should confirm the handover TSV columns are right before it becomes the weekly standard.
- **Path A (song-match) live-truth**: Max should decide if cluster-match titles go live with a "machine guess, verify" warning, or if that path stays held entirely on fringe videos.

---

## KEY PATHS + IDs

- **Pipeline root**: `C:\claude_base\tools\tamza_songs\pipeline\`
- **Handover tool**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py` (subcommands: `pick`, `table`)
- **First handover table**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\tables\handover_2020-03-30_pX_1m8DlMbA.tsv`
- **Human Excel**: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Channel inventory (upload dates)**: `C:\claude_base\tools\tamza_songs\output\channel_inventory.json` (935 videos with id, upload_date, title)
- **Start-here handover doc**: `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md`
- **Workflow map**: `C:\claude_base\tools\tamza_songs\pipeline\CURRENT_WORKFLOW_v01_tomemex.md`
- **Publish script**: `C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py` (gated, reversible, supports `--dry-run`)
- **Monthly update method**: `C:\claude_base\tools\tamza_songs\pipeline\method\monthly_update_method_v01_tomemex.md`
- **ASR ready list**: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\nonh_asr_ready_on_teal16.txt` (82 IDs)
- **ASR still-pending**: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\_work\nonh_asr_still_pending.txt` (11 IDs)
- **Sol SSH**: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` (Sol itself) | `ssh maxre@192.168.1.176` (teal16/Centauri)
- **ASR output on Sol**: `~/nonh_transcribe/out/*.json`
- **Picked video**: `pX_1m8DlMbA` (2020-03-30, 47 songs, oldest good NONH)
- **Board**: `python "C:/claude_base/branch_bulletin/bcast.py" [post|read|wake|catchup]`
- **Worklog**: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- **My identity**: B26juniorconnector (registered on the board)

### Team owners:
- **b15merger**: go-live gate, resolved store, overlay build
- **b7nonhtimes**: ASR on Sol, NONH segmentation, downstream timing
- **b7i**: catalog publish to live site
- **b10**: rendering
- **b15A**: data reconciliation
- **b9**: ytdow backup, video staging to teal16
- **b15M**: archive cleanup sign-off (conflict file)
- **B27**: archive cleanup worker (I manage)

---

## GOTCHAS + DEAD ENDS RULED OUT

1. **Famous-song drift**: On old/fringe videos, the song-text matcher (Path A) produces ~half wrong titles - it matches famous songs, not what was actually sung. Performers are much more reliable. Path C (performer-in-DB match) is the safer publish path for these videos.

2. **Do NOT hit YouTube for metadata** - 691 video resolves would violate block rules + ytdow is running. Use `channel_inventory.json` for upload dates/titles (already populated by b9's enumeration).

3. **Human remap is ALREADY live** - don't try to re-push it. The dry-run confirmed it. Only the NONH gate (newly identified songs) remains to deploy.

4. **b15merger's publish needs backing up first** - the one real hazard is clobbering existing live data. The publish script (`publish_catalog.py`) is gated and reversible, but back up the live catalog JSON before any deploy.

5. **ASR on Sol is CPU-bound, not GPU** - ~9 min per video, 82 videos ? overnight grind. Don't expect fast results; verify the process is alive, not done.

6. **First-line cells in the handover table are often spoken intro, not sung line** - boundary bleed from the segmenter. The LLM review flagged this. Multi-pass vetting should strip/fix these.

7. **B27's archive plan has one real conflict** - `_batch_aligner_v01.py`: documentation says it's runtime-active, but grep shows zero live imports. b15M (who wrote it) needs to resolve the doc-vs-reality gap before that file moves.

8. **Handover table not yet merge-able to the live Google Sheet** - it's a TSV matching the format of one concert tab. Max needs to confirm the columns before it becomes the weekly standard, and multi-pass LLM vetting is still required.

9. **Autonomous watch timer**: armed at ~4 min (`ScheduleWakeup` with sentinel `<<autonomous-loop-dynamic>>`), re-arms every tick. If ASR is grinding and publish is deployed, scale back to wider intervals to be economical.

10. **Identity slipped once** - one post went out as "b6" instead of B26juniorconnector. I corrected it immediately. Watch that `whoami` sticks on future ticks.
