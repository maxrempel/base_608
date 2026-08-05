
## [2026-06-15 17:24] b21 043552e7
- DID: B21 fresh-eyes on song-starts. Did 19 tool calls archeology, proposed 'trust curated start' - Max REJECTED (curated is messy, LLM re-derivation intentional). Roster: b7 owns starts, b6 retiring, b15c relaying.
- STATE: Watch+learn mode. Offered b7 a read-only QC slice (sample v2 recent Max songs vs transcripts, rank worst start errors). Not touching stores.
- NEXT: Wait for b7 to accept/decline QC offer + tell me which vids='recent'. Then sample transcripts to find HOW v2 mapper errs on starts.
- LESSON: Don't barge into a veteran team with a big theory; watch first. Curated timecodes in Kartoteka are messy - never propose trusting them.

## [2026-06-15 19:39] b21 043552e7
- DID: QC-sampled song-START quality (read-only) vs transcripts {t,d,x} in pipeline/song_timing/transcripts/. Sampled v2 overlay entries with biggest move from curated key.
- STATE: FINDINGS: (1) mapper mostly RIGHT - poems(Стих) + songs start on first line; (2) big +1000s moves off curated are GOOD corrections (mapper relocates from messy curated to real performance, e.g. 4WRGcR0F3wU Разбор curated350->v2 1391 = first sung line); (3) REAL miss class = pure SPEECH/announcement entries (Вступительное слово/Объявления/Предисловие): mapper assumes song, jumps to next [музыка], skips the talk; flagged by low conf 0.3-0.5 + big +move landing on [музыка]. Posted finding+fix idea to b7. No clear defect found yet in Max's SUNG songs.
- NEXT: Asked Max to name ONE specific recent song with a bad start to dissect exactly. Wait for that or for b7 to assign a slice. Stay read-only, hands off _work/song_timing.json (b7 remapping in place).
- LESSON: Big start-moves off curated are usually the LLM correctly fixing junk curated values, NOT errors - don't flag moves as bad without checking the transcript.

## [2026-06-15 20:09] b21 043552e7
- DID: B21=R&D engineer, play-safe (read-only, never touch shared stores, no spend). Shipped read-only bad-start flagger (qc_b21/flag_bad_starts_v01.py): scanned 21478, flagged 274 likely-bad starts (start lands on [музыка]+corroborating signal), ranked TSV handed to b7. Re-posted atomic-write proof (os.replace) to clear safety watcher pause on b7.
- STATE: AUTONOMOUS watch. b7 owns starts, mid full-catalog remap of _work/song_timing.json (atomic, cron-safe). b6 retired. No slice assigned to me. ~94% context, compaction imminent - status snapshot + this log are the resume anchors.
- NEXT: On resume: read session_status + this log. Check bcast board for b7 reply/slice. Wait for Max to name a specific bad SUNG song to dissect. Keep safe read-only QC; new scratch in worktree not shared pipeline dir. Do NOT touch stores; don't re-propose curated-trust (rejected).
- LESSON: Big start-moves off curated are usually the LLM correctly fixing junk curated values, not errors.

## [2026-06-15 20:58] b21 043552e7
- DID: Post-compaction resume. b7 full-catalog remap RUNNING (2124/21438, $1.22), rewriting base store atomically. Built flagger v02 (qc_b21/flag_bad_starts_v02.py) adding guard_starts cross-check: tags each flag COLLIDE/PREROLL/BACKLOAD vs RESIDUAL, ranks guard-surviving speech entries top. Posted insight to b7.
- STATE: Holding read-only. v01 274-flag list goes stale as remap rewrites seg_starts. v02 ready to run post-remap.
- NEXT: On b7 remap-done post: run flag_bad_starts_v02.py against final store, hand b7 a residual-only review queue. Otherwise keep read-only QC, re-arm long.
- LESSON: guard_starts.py already reverts forward-slid starts (COLLIDE/PREROLL/BACKLOAD); the only uncaught defect class is IN-slot music-landings on spoken entries -- that is where QC adds value.

## [2026-06-15 22:00] b21 043552e7
- DID: Sampled Max's 670 OWN overlay songs (stable; remap doesn't touch overlay). 209 land on music but most are CORRECT (move~0 = song's own intro). Dissected Та кухня +152 via new peek_start.py: GOOD correction (curated pointed mid-previous-poem; mapper found real musical intro). Only real defect class = pure-SPEECH entries (~6). Posted to b7.
- STATE: Stopping autonomous loop per Adviser (8h remap = pure idle). Flagger v02 + peek_start.py ready in qc_b21/.
- NEXT: When b7 posts remap-done: run flag_bad_starts_v02.py on final store, hand b7 residual-only queue. Max may name a specific bad sung song to dissect with peek_start.py.
- LESSON: Big forward move onto music for a SUNG song is usually a GOOD correction of a junk curated value, NOT a defect - verify by dumping transcript context (peek_start.py) before flagging. Only pure-speech entries are true misses.
