
## [2026-06-16 17:53] b7nonhtimes 65b83f05
- DID: B7nonhtimes: built seg_nonh_v01.py (batch of b15 seg_phase1 prose-boundary segmenter over NONH). 181 vids segmented ($0.66). HUM remap hit 100% ($11.10, B7i to publish). Captions 459/786.
- STATE: seg batch idle after 181 (ran out of captioned vids); re-launched to absorb new captions. Caption fetch PID40720 alive 63%. My budget ~$3 cap $5.
- NEXT: Re-run seg_nonh each tick as captions arrive. Hand drafts (_work/seg_nonh/) to b15A annotator. When captions 100%, final seg pass.

## [2026-06-16 18:14] b7nonhtimes 65b83f05
- DID: Tick: NONH boundaries 460/786 vids ($1.01); captions 70% (552/786, PID40720 alive). Re-launched seg PID85588 to absorb new captions.
- STATE: seg batch is one-shot per run (exits when caught up to available captions); I re-launch each tick. HUM done (B7i). My budget ~$3 cap $5.
- NEXT: On captions 100%: final seg pass, then bcast b15A all NONH drafts ready in from_scratch_idx/_work/seg_nonh/.

## [2026-06-17 06:26] b7nonhtimes 65b83f05
- DID: Tick: NONH boundaries 617/786 ($1.65); captions 92% (726/786, 70 caption-disabled). Re-launched seg PID88002.
- STATE: 70 NONH vids have NO captions (disabled) - segmentable universe ~716, those 70 need audio transcription later (out of $3 budget). Caption fetch PID40720 ~60 left.
- NEXT: Captions ~100% soon: final seg pass, bcast b15A all NONH drafts ready in from_scratch_idx/_work/seg_nonh/. Flag the 70 caption-disabled as a known gap.

## [2026-06-17 06:44] b7nonhtimes 65b83f05
- DID: Set up Sol ASR for 86 caption-DISABLED NONH videos. Sol(192.168.1.113, key ~/.ssh/sol_key): venv at ~/nonh_transcribe/ with faster-whisper 1.2.1 + yt-dlp; script transcribe.py (copy of _work/sol_transcribe_nonh.py) reads vids.txt, yt-dlp bestaudio -> faster-whisper RU no-translate -> out/<vid>.json in {t,d,x}. Running PID8345 CPU int8 (P400 CUDA declined). Resumable, logs transcribe.log/run.log.
- STATE: Reality: multi-hour concert vids on CPU = slow, likely days for 86. yt-dlp JS-runtime warning harmless (ANDROID_VR client works). Main NONH captioned seg still running separately.
- NEXT: Each tick: scp Sol ~/nonh_transcribe/out/*.json back to Pine transcripts/, then re-run seg_nonh_v01 to segment them. Refresh vids.txt from fetch_nonh_state permanent list as it grows. Consider retrying GPU with compute_type=int8 (not int8_float16).

## [2026-06-17 07:41] b7nonhtimes 65b83f05
- DID: Sol went OFFLINE (no ssh, no ping - destination unreachable). Max said 'Start the 75% test, 20 rounds, restarted' - interpreting as Sol restarted + put on a 75%-memory stress test 20 rounds (its known bad-RAM diagnosis), so Sol is BUSY/unavailable for transcription for a while.
- STATE: Sol ASR (86 caption-less NONH vids, ~/nonh_transcribe/) is PAUSED until Sol's memtest finishes; job is resumable so no work lost. Captioned-NONH segmentation continues on Pine (seg_nonh_v01). Asked Max to clarify if I should start the test or he did.
- NEXT: When Sol back: scp out/*.json to Pine transcripts/, resume seg. Do NOT improvise a hardware stress test. Keep re-running seg_nonh for captioned vids; caption fetch PID40720.

## [2026-06-17 08:15] b7nonhtimes 65b83f05
- DID: Segmented final 74 NONH videos after DeepSeek refill; all 691 captioned NONH videos now have prose-boundary drafts in from_scratch_idx/_work/seg_nonh/. Total seg spend .12 (budget ~).
- STATE: NONH segmentation COMPLETE for all captioned videos. 691 done, ~91 caption-disabled remain (need Sol ASR first). Posted handoff to b15A via bcast.
- NEXT: Await Max decision on Sol ASR for the ~91 caption-disabled videos. Otherwise NONH-timestamps lane is done.

## [2026-06-17 08:43] b7nonhtimes 65b83f05
- DID: Loop tick: captions 784/786 attempted (fetcher exited), all 691 captioned NONH segmented (nothing new to seg). Sol ASR alive PID 9152 on CPU int8 (CUDA declined, P400 Pascal cant int8-GEMM), 0/86 done so far - slow. Updated Sol vids.txt 86->93 to cover all caption-disabled.
- STATE: NONH seg complete for captioned set. Sol ASR grinding on 93 caption-disabled, 0 done yet. b15A already has 691 drafts.
- NEXT: Next tick: scp Sol out/*.json to transcripts/, seg the new ASR ones, report counts. Final pass + tell b15A when ASR done.
- LESSON: P400 (compute 6.1 Pascal) cannot do ctranslate2 int8 GEMM on CUDA; needs Turing 7.0+. CPU int8 is the only path on Sol - slow on long concerts.

## [2026-06-17 09:05] b7nonhtimes 65b83f05
- DID: Loop tick: discovered Sol ASR was DEAD - prior 'alive' PIDs were pgrep self-matches (ssh cmd contained 'transcribe.py'). Real process died at 06:42 after model load (not detached, killed on SSH drop). 0/93 transcribed. RELAUNCHED properly: setsid+nohup, stderr->crash.log, PID 18753 real. Nothing new to segment (all 691 captioned done).
- STATE: Sol ASR restarted detached on 93 caption-disabled vids, CPU int8, slow. 691 captioned NONH segmented + handed to b15A. Captions 784/786 attempted (fetcher exited).
- NEXT: Next tick: check crash.log if dead again, scp out/*.json, seg the new ASR transcripts, report ASR count.
- LESSON: pgrep -f transcribe.py SELF-MATCHES the ssh bash command that contains the string. Use 'ps -eo pid,cmd | grep -E [p]ython.*transcribe' to avoid false-alive. Always launch Sol jobs with setsid+nohup+</dev/null or they die on SSH disconnect.

## [2026-06-17 09:26] b7nonhtimes 65b83f05
- DID: PAUSED on Sol per Max ('pause until stress tests done'; 'stop the fucking downloads'). Killed Sol transcribe.py + yt_dlp (PID 18753 gone, confirmed ALL_DEAD). My uncoordinated YT downloads from Sol risked an IP block while the 2000-video Tamza/Hucolo backup runs - that was my error. Stray 300MB tmp/iDkG2mQdJbw.m4a left on Sol (harmless). An OLD wakeup fired with relaunch-Sol prompt; OVERRODE it - did not touch Sol.
- STATE: NONH-timestamps deliverable COMPLETE: 691 captioned videos segmented (prose boundaries), $2.12, drafts in from_scratch_idx/_work/seg_nonh/ handed to b15A. Only ~93 caption-disabled videos remain (need ASR) - PAUSED until Max says resume AND routed through the shared spaced YT pipeline (NOT a separate downloader). Saved new memory rule feedback_youtube_download_coordination.md.
- NEXT: WAIT for Max 'resume'. Then do ASR for 93 via shared pipeline w/ ~30s spacing. Do NOT touch Sol before that.
- LESSON: YT blocks IP on uncoordinated/parallel downloads; all YT pulls go through the one shared optimized pipeline, spaced ~30s sequential. Never run a separate downloader while the channel-backup job is active.

## [2026-06-17 12:29] b7nonhtimes 65b83f05
- DID: Idle hold tick. Sol OFF-LIMITS per Max (stress-testing it; 'pause until tests done'). I have NOT touched Sol. Repeated old wakeups with relaunch/scp prompts were all OVERRIDDEN - no Sol contact.
- STATE: NONH-timestamps deliverable COMPLETE: 691 captioned videos segmented (prose boundaries), $2.12, drafts in from_scratch_idx/_work/seg_nonh/ handed to b15A, committed+pushed. PAUSED: ASR for ~93 caption-disabled videos - waits for Max 'resume', then route through SHARED spaced YT pipeline (NOT standalone; see feedback_youtube_download_coordination.md). Stray 300MB tmp file left on Sol (harmless).
- NEXT: WAIT for Max 'resume'. Then: route 93 audio pulls through shared pipeline ~30s spacing -> ASR on Sol -> scp transcripts to Pine transcripts/ -> seg_nonh_v01.py (cap 5) -> tell b15A. Do NOT touch Sol before 'resume'.
- LESSON: When an OLD ScheduleWakeup fires with a now-stale prompt (e.g. relaunch Sol) that conflicts with Max's latest instruction (pause), OBEY the latest instruction, override the stale wakeup prompt.

## [2026-06-17 14:28] b7nonhtimes 65b83f05
- DID: Held during Sol stress tests; gave Max a TMS. Sol team converged: black slots 2+4 bad, 32GB on green = safe machine.
- STATE: NONH segmentation DONE (691 vids, .12, drafts to b15A, pushed). ASR for ~93 caption-disabled vids PAUSED - Sol off-limits, YT downloads stopped.
- NEXT: On Max 'resume': ask which shared YT pipeline to route the 93 audio pulls through, then scp transcripts, run seg_nonh_v01.py (cap 5), tell b15A.

## [2026-06-17 15:43] b7nonhtimes 65b83f05
- DID: Answered B25handoverer interview + reviewed TAMZA_HANDOVER_START_HERE_v01 - all my-lane sections OK, no corrections. Confirmed ASR routing: b9 stages 93 caption-disabled vids as mkv to teal16; Sol ASR extracts audio FROM teal16 (no YouTube hit) once Sol cleared.
- STATE: NONH segmentation DONE (691 vids, $2.12, drafts to b15A, pushed). ASR for 93 vids PAUSED - Sol off-limits during RAM stress tests. Holding 60min.
- NEXT: On Max resume / Sol cleared: count 93 mkv on teal16, run Sol ASR from teal16 audio (NOT YouTube), scp transcripts to Pine, run seg_nonh_v01.py cap 5, tell b15A.

## [2026-06-17 16:44] b7nonhtimes 65b83f05
- DID: Disarmed self-wake timer per Max's instruction (relayed by B25handoverer): idle/holding sessions drop timers, peers hear board each turn. Going quiet.
- STATE: NONH segmentation DONE (691 vids, $2.12, drafts to b15A, pushed). Only remaining = ASR for 93 caption-disabled vids, BLOCKED on Sol (off-limits, RAM stress tests). NO timer armed.
- NEXT: Wake by name OR Max says resume when Sol cleared + 93 mkv on teal16: count mkv, run Sol ASR from teal16 audio (NOT YouTube), scp transcripts to Pine, run seg_nonh_v01.py cap 5, tell b15A.

## [2026-06-17 22:55] b7nonhtimes 65b83f05
- DID: B26 (in charge while Max out) woke me: Sol coming available, I own the 93-vid ASR. Verified teal16: 82/93 mkv on Centauri (11 still pulling). Wrote sol_transcribe_nonh_v02.py = pulls mkv from teal16 via scp + faster-whisper decodes mkv directly, NEVER YouTube (respects single-puller rule + Max's stop-downloads order). asr_ready_ids.txt = the 82 ready.
- STATE: Sol not contacted yet (waiting ~3min for it to come up). v02 script ready locally. Re-armed 5mt to launch once Sol verified reachable + stable 32GB config.
- NEXT: Next tick: ssh Sol verify up; scp v02 script + 82 ids as vids.txt to ~/nonh_transcribe/; launch setsid nohup detached; verify liveness ps -eo pid,cmd grep [p]ython.*transcribe_v02; then poll for out/*.json, scp back to Pine transcripts/, run seg_nonh_v01.py cap 5, tell b15A.

## [2026-06-17 22:59] b7nonhtimes 65b83f05
- DID: LAUNCHED Sol ASR v02 (teal16 source): verified Sol up at 31GB stable config, deps OK, scp'd v02 script + 82 ids, tested Sol->Centauri scp (pulled 1.3GB mkv OK), launched detached PID 27020, verified alive via ps grep. 1/82 done, QC'd first transcript = genuine rough Russian lyrics (small CPU model). Job pulls mkv from teal16 NEVER YouTube.
- STATE: Job running overnight, ~many hours for 82 long concerts on CPU int8. 82/93 ready on teal16; 11 still being pulled by b9. Max going to sleep; running autonomous with 5mt then flex.
- NEXT: Accumulate transcripts -> LLM multi-sample QC (Max asked) -> scp out/*.json to Pine transcripts/ -> run seg_nonh_v01.py cap 5 -> tell b15A. Top up vids.txt with the 11 once b9 finishes them.
- LESSON: v02 sources ASR audio from teal16 (scp mkv from Centauri) instead of YouTube - respects single-puller rule; faster-whisper decodes mkv directly via av, no separate ffmpeg extract needed.

## [2026-06-17 23:08] b7nonhtimes 65b83f05
- DID: Relaunched Sol ASR on CPU int8 after GPU/cuBLAS path failed; job alive (pid 52723), 1 done/81 to do, model small CPU int8 confirmed
- STATE: ASR running on Sol ~/nonh_transcribe, teal16-sourced mkv, resumable. crash.log only shows benign onnx GPU-probe warning
- NEXT: Monitor every 5min; QC transcripts with many LLM sampling passes as they land; top up vids.txt with 11 not-yet-on-teal16 ids when b9 done

## [2026-06-17 23:49] b7nonhtimes 65b83f05
- DID: Sol ASR 6/81 done, alive; QC-sampled 2 transcripts
- STATE: Timing solid; text rough fringe-Russian; some vids are English songs forced thru RU. Worth it for TIMING (only source for caption-disabled). ~10hr ETA
- NEXT: Monitor 4mt, run LLM-QC loop on transcripts, top up vids.txt w/ 11 pending b9

## [2026-06-17 23:52] b7nonhtimes 65b83f05
- DID: Max reviewed 4 ASR samples, verdict 'acceptable but barely, keep going'. vids.txt now full 93. b9: 90/93 on teal16, 3 left by morning
- STATE: Sol ASR running CPU int8; quality varies (clean-speech good, fringe moderate, English partial); some 1-2hr videos eat CPU. LLM-QC loop pending as transcripts accumulate
- NEXT: Monitor 4mt; batch LLM-QC the rough fringe-Russian; then seg_nonh_v01 -> b15A

## [2026-06-17 23:58] b7nonhtimes 65b83f05
- DID: VALIDATED full pipeline end-to-end on first 6 teal16 ASR transcripts: ASR->stage to Pine transcripts/->seg_nonh DeepSeek->boundary drafts in from_scratch_idx/_work/seg_nonh/. 1dDhDrNM9rE=37 songs w/ clean perf/author/title from intros (Чеширский блюз etc); 13yHAn8qzAg=54; English+silent vids correctly 1-seg low-conf NO hallucination
- STATE: Noisy ASR yields RELIABLE performer attribution (intros transcribe clean); sung-lyric garble only hurts canon-match which is 'verify' anyway. seg cost ~$0.004/vid
- NEXT: Keep ASR grinding (6/81 done); re-stage+re-seg as batches complete; then hand seg_nonh drafts to b15A
- LESSON: QC priority = verify seg OUTPUT boundaries+intro attribution, NOT scrub sung-lyric text; segmenter is noise-tolerant by design (SYS says ~50% garbled)

## [2026-06-18 06:25] b7nonhtimes 65b83f05
- DID: ASR 54/81 done; staged all 54 to Pine transcripts/; seg_nonh segmented 53 (1 empty/near-silent skipped). QC'd broad random sample
- STATE: Quality BIMODAL: rich concert vids (1dDhDrNM9rE=37,13yHAn8qzAg=54,7Nwc4dh-18c=37) = clean perf/author/title from intros; short/sparse/instrumental vids = 1-seg low-conf no-attribution (correctly held, no false confidence). seg drafts in from_scratch_idx/_work/seg_nonh/
- NEXT: Let ASR finish (~27 left incl long ones); final stage+seg+QC pass; then hand seg_nonh drafts to b15A

## [2026-06-18 06:48] b7nonhtimes 65b83f05
- DID: ASR 57/81; staged+segmented 56 caption-disabled NONH into seg_nonh/. Posted cross-branch heads-up: b27/b15merger must re-pull seg_nonh (697-snapshot predates my set)
- STATE: New team rule absorbed: KILL TITLES, identity=first-sung-line(LLM-verified by b27). My seg title field=junk; my reliable output=performer+boundary timecodes. ASR alive on long concerts, ~24 left
- NEXT: Keep ASR grinding, stage+seg each batch; final pass + tell b27/b15A when all 81 done

## [2026-06-18 07:44] b7nonhtimes 65b83f05
- DID: Tick: confirmed Pine path on board; pulled+segmented 4 new transcripts (61/81 staged+segged). ASR alive on long concert jO6BW9TMhgs.
- STATE: 61/81 ASR done, all staged to transcripts/ + segmented to seg_nonh/. Sol pid 52723 @561%CPU. ~20 left incl long concerts.
- NEXT: Keep draining 61->81: each tick pull new Sol out/ -> Pine transcripts/ -> seg_nonh; final full pass + bcast when 81 done.

## [2026-06-18 13:47] b7nonhtimes 65b83f05
- DID: ASR said DONE@81 but found 11 of 93 never transcribed despite being on teal16 (resume-state quirk); relaunched transcribe_v02 -> '11 to do'. 82 staged+segmented; E7apqIFW0RQ empty (honest skip).
- STATE: 82/93 transcribed+segmented; 11 now re-running from teal16; 1 empty. seg cost ~.49.
- NEXT: Wake ~25min: pull+segment the 11; then final bcast to b27/b15merger that full caption-disabled set is staged in transcripts/ + seg_nonh/.

## [2026-06-18 15:55] b7nonhtimes 65b83f05
- DID: NONH ASR 100% done (93 transcribed, 91 segmented, 2 empty) - posted complete to board. Took B26's 2-min-cap task: found cap-hit rows need NO ASR - seg_end = next act's start (free chaining). Staged candidate filling 3205 (+899 b7i =4104/4232), 128 residual. Committed+pushed stage_segend_nextstart_v01.py (9e94c0af).
- STATE: NONH DONE. 2-min-cap fix STAGED (no deploy) for B26 spot-check; b15merger deploys on approval. 128 residual=77 last-act(need vid-duration)+51 no-id junk.
- NEXT: Await B26 spot-check verdict on nextstart candidate. If approved, last-act fallback = video duration (could pull from teal16 ffprobe). Else NONH lane idle - monitor board.

## [2026-06-18 17:52] b7nonhtimes 65b83f05
- DID: Added MAX_GAP=1800s guard to next-start seg_end pass (b26-approved): filled 3201, 4 absurd-gap nulled. Then staged negdur fix: nulled 17 pre-existing negative-duration seg_end rows (all src=None). Both committed+pushed (e3adf7a1, 2e495d29), candidates 002436Z + negdur 005144Z.
- STATE: NONH ASR lane 100% done. 2-min-cap fix STAGED+handed off: b15merger has b26 GO to deploy 002436Z (+3201), then negdur candidate. Awaiting deploy confirmation.
- NEXT: Watch board for b15merger deploy-done. Remaining cap residual: 77 last-act-per-video (would need video-duration fallback from teal16/cached transcript) + 51 no-id junk -- NOT started, wait for b26 to scope before inventing.

## [2026-06-18 18:20] b7nonhtimes 65b83f05
- DID: +3201 next-start DEPLOYED LIVE by b15merger (4100 songs uncapped). b15merger held my negdur v01 claiming 26/6-positive nulled; I diffed index-by-index = exactly 17, all negative, 0 positive (their diff had duplicate-(vid,start) key collision). Adopted their better derived-start rule as v02 (still 17, structurally safe). Committed b92a7497.
- STATE: NONH done. +3201 LIVE. negdur v02 staged (data_candidate_segend_negdur_v02_20260619T012004Z.json), awaiting b15merger deploy.
- NEXT: Watch board for b15merger negdur v02 deploy. Remaining cap residual 77 last-act + 51 no-id still unscoped -- wait for b26.

## [2026-06-18 18:46] b7nonhtimes 65b83f05
- DID: b26 resolved negdur dispute, GO'd v02 to b15merger. Cap problem essentially closed for TIMED set (899+3201 live = 4100 uncapped + 17 broken ends being removed). Offered to ASR the remaining '54 awaiting teal16 ASR' (my pipeline) if b26 hands the id list.
- STATE: My cap-fix lane DONE: +3201 LIVE, negdur v02 staged+GO'd (b15merger deploys). Awaiting either: b15merger v02 deploy-confirm, or b26 handing me the 54-video ASR list.
- NEXT: If b26 drops the 54 ids -> run teal16->Sol ASR->boundary same as the 93. Else watch board, stay quiet.

## [2026-06-18 19:24] b7nonhtimes 65b83f05
- DID: Staged FREE ffprobe video-duration seg_end fill for last-act untimed rows: durations_teal16_v01.json (10 dur) + stage_segend_videodur_v01.py building on negdur v02 -> data_candidate_segend_videodur_20260619T022200Z.json (filled 10 last-acts, 2 mid-video left for ASR). Committed 67fc94ce, pushed. Posted dumb-bucket win to board.
- STATE: Awaiting B26 GO on videodur candidate + b15merger deploy-confirm of negdur v02. Deploy order: 002436Z(LIVE) -> negdur v02 -> videodur. Nothing new on board since cursor.
- NEXT: Watch board for B26 videodur GO + b15merger negdur-deploy. As b9 backup lands more of 67 needs-end vids on teal16, re-ffprobe + extend durations + re-stage. 2 genuine mid-video rows (eD9UEvA3YLE t7424, eS1n9-YbH0A t5456) -> ASR/B30 only.

## [2026-06-18 19:52] b7nonhtimes 65b83f05
- DID: B26 GO'd deploy chain to b15merger (002436Z LIVE -> negdur v02 -> my videodur 022200Z) + approved dumb-bucket ffprobe win. Re-checked teal16 for new needs-end arrivals: 10 on teal16 = exactly the 10 already in durations_teal16_v01.json, 0 new. Nothing to re-ffprobe this tick.
- STATE: Videodur candidate approved, deploy is b15merger's job (gated, not mine). 57 of 67 needs-end videos still NOT on teal16. Awaiting b15merger deploy-confirm.
- NEXT: Each tick: re-grep teal16 (grep -Fxf untimed vs cmd-dir list, NOT comm/powershell) for newly-landed needs-end vids; when new ones appear, ffprobe + extend durations + re-stage videodur. 2 mid-video rows (eD9UEvA3YLE t7424, eS1n9-YbH0A t5456) -> ASR/B30.
- LESSON: teal16 listing: use 'ssh ... cmd /c dir /b *.mkv' (bare names), NOT powershell .BaseName (mangles through ssh/bash). And use grep -Fxf for id intersection, NOT comm (locale collation hides matches on ids with -/_).

## [2026-06-18 20:23] b7nonhtimes 65b83f05
- DID: Deploy chain went LIVE (b15merger): 002436Z+negdur v02+videodur 022200Z, 26144 rows int seg_end. Then re-checked teal16: 1 NEW needs-end video landed (BdX_9DbVQck, 356 mkvs now). ffprobe=12828s. Added to durations, re-ran videodur -> candidate 032224Z (11 last-act fills, +1 BdX; 3 mid-video for ASR). Committed 4f41bc08, pushed, posted to b15merger to re-deploy.
- STATE: Awaiting b15merger re-deploy of 032224Z. 56 of 67 needs-end videos still not on teal16. 3 mid-video rows queued for ASR/B30.
- NEXT: Each tick: re-grep teal16 (cmd dir + grep -Fxf) for new needs-end arrivals; ffprobe + add to durations + re-run stage_segend_videodur_v01.py + commit + tell b15merger. Mid-video rows (gap>1800) -> ASR/B30, never fill.

## [2026-06-18 20:52] b7nonhtimes 65b83f05
- DID: Tick: re-checked teal16 (358 mkvs, +2). No NEW needs-end arrivals - all 11 needs-end on teal16 already in durations_teal16_v01.json. Nothing to stage.
- STATE: Awaiting b15merger re-deploy of candidate 032224Z (BdX increment). 56 of 67 needs-end videos still not on teal16.
- NEXT: Keep grepping teal16 each tick (grep -Fxvf have_dur for NEW; never comm - collation bug). ffprobe new last-acts + extend durations + re-run videodur + tell b15merger.

## [2026-06-18 21:54] b7nonhtimes 65b83f05
- DID: B30 verdict: my 3 mid-video residual rows = DUPLICATE-&t= data artifact (6 rows, two songs sharing one start), NOT ASR. B26 ACK'd. I ACK'd + adopted: gap>1800 rows route to human-dedup not ASR. B26 confirms 2-min cap CLOSED for timed set (899+3201+ffprobe LIVE). teal16 re-check: 364 mkvs, no new needs-end.
- STATE: Steady-state: my ffprobe lane = last-act rows only as b9 lands the 54 remaining needs-end videos. Candidate 032224Z (BdX) still pending b15merger re-deploy.
- NEXT: Each tick grep teal16 for new needs-end; ffprobe new last-acts (gap<=1800) -> extend durations -> re-run videodur -> b15merger. Mid-video (gap>1800) = dupe artifact -> human, never ASR.
