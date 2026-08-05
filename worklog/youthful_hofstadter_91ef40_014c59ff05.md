
## [2026-06-18 14:36] B30worker bd87c25d
- DID: B30worker diagnosed the 4233 no-seg_end live rows (the 2-min radio cap). Wrote diag scripts in pipeline/song_timing/_work/ (b30_final_report.py etc.).
- STATE: Buckets: A=900 rows FREE (store already has seg_end; live data.json stale - dry re-enrich proves 22050->22950 with_end). B=2944 rows/61 videos BLOCKED (no cached captions; mapper needs captions; fetch=2nd YT puller vs single-puller rule while ytdow runs). C=~338 rows/11 vids messy edge (key mismatches, 6 vids not in queue). Plus latent youtu.be URL-parse bug in enrich_catalog.video_id (only parses watch?v=). No clean cheap-batch pilot exists - premise of 'time 4232 via DS4' is mostly wrong.
- NEXT: Report findings to B26 + b15merger; 900 free-recovery is already in b15merger's republish path (just needs build_data_overlays+redeploy). Do NOT deploy (b15merger owns gate). 2944 needs a caption-fetch coordination decision from B26/Max. Hold youtu.be parser fix until b15merger acks to avoid mid-publish surprise.

## [2026-06-18 15:16] B30worker bd87c25d
- DID: B30worker: roles locked. b7nonhtimes owns ASR-from-teal16 on Sol for my 7 teal16-ready videos; I'm downstream (seg->seg_end->b15merger). b15merger converged on my youtu.be enrich fix (on master, no pull). Pushed fix 71d3a9f9.
- STATE: Of 61 bucket-B untimed videos: 7 on teal16 now (ASR-able), 54 await b9 backup ~Jun30. Lists in song_timing/_work/b30_bucketB_on_teal16_ASRnow.txt + _pending_b9backup.txt. 899-row FREE recovery staged by b15merger, holding for Max GO. bucket-A=900 free, bucket-B=2944/61vids ASR path, bucket-C=338 messy edge.
- NEXT: Watch song_timing/transcripts/ for the 7 vids (5OY0GaS_krc 6kDV3eUlc9c WUICivWzZnk dyb6RjoJHzA eS1n9-YbH0A fBx49lcJRpE zk25-DXm4i0). When a transcript lands, run seg_phase1_v01/seg_nonh_v01 -> seg_end -> hand b15merger. 54 pending = re-run when b9 backup completes.

## [2026-06-18 19:20] B30worker bd87c25d
- DID: B30worker: handed b7nonhtimes the consolidated 61-video id list (7 teal16-ready + 54 pending) for teal16->Sol ASR. B26 gave full GO. My 899 free recovery is LIVE (b15merger deployed+verified). Parallel: b7nonhtimes's +3201 free recovery also LIVE -> ~4100 songs uncapped, timed-set cap essentially closed.
- STATE: Remaining B30 lane = the 61 genuinely-untimed videos, purely downstream of ASR. 0/7 transcripts landed yet (overnight ASR on Sol). Lists: song_timing/_work/b30_bucketB_on_teal16_ASRnow.txt (7) + _pending_b9backup.txt (54).
- NEXT: Watch song_timing/transcripts/ for the 7 vids. When any lands: seg_phase1_v01/seg_nonh_v01 -> seg_end -> hand b15merger. 54 follow as b9 backup (~Jun30) lands them on teal16.

## [2026-06-18 20:22] B30worker bd87c25d
- DID: B30worker: b7nonhtimes's ffprobe 'dumb-bucket' win - most untimed rows are concert LAST-ACTS (end=video length, free, no ASR); b15merger deployed videodur live (26144 rows timed). My ASR lane shrank to genuine MID-video remainder only. Asked b7nonhtimes to hand me the per-video list of rows ffprobe couldn't solve (they hold live candidates+teal16). My local data.json is ~2000 rows stale vs live, so I won't re-derive from it.
- STATE: Cap essentially closed: 899 + 3201 + videodur all LIVE. My remaining lane = small genuine mid-video set, list pending from b7nonhtimes. 0/7 transcripts landed.
- NEXT: Wait for b7nonhtimes's mid-video ASR list; when it arrives, ASR exactly those from teal16->Sol -> seg -> seg_end -> b15merger. If nil, lane done.

## [2026-06-18 21:25] B30worker bd87c25d
- DID: B30worker probed the 3 mid-video ASR-remainder rows from b7nonhtimes. VERDICT: not a timing task - each is 2 catalog rows sharing one &t= timecode (often different performers), no timed twin = duplicate-timecode data artifact (6 rows). ASR can't fix two songs at one start; needs curated &t= correction. Recorded in _work/b30_dupe_timecode_artifacts_for_human.md, recommended human/dedup pass not ASR.
- STATE: 2-min cap CLOSED for timed set (899+3201+last-act ffprobe all LIVE, 26144 rows). My genuine ASR lane = effectively NIL. 54 pending videos will mostly be last-acts too (ffprobe/b7nonhtimes).
- NEXT: Re-check the 54 as b9 backup lands them (~Jun30); if any genuine mid-video non-dup appears, ASR it. Otherwise lane done. No action needed meanwhile.

## [2026-06-18 22:26] B30worker bd87c25d
- DID: B30worker TASK COMPLETE + acknowledged. My verdict (3 mid-video rows = duplicate-&t= artifact, not ASR) ACKed by B26 + b7nonhtimes. b7nonhtimes adopts: gap>1800 rows route to my dupe_timecode_artifacts_for_human.md (human/dedup), their ffprobe lane = last-acts only; they own the 54-video tail. My youtu.be enrich fix shipped (71d3a9f9). 899-row free recovery LIVE via b15merger.
- STATE: 2-min radio cap CLOSED for the timed set (899+3201+last-act ffprobe LIVE, ~26144 rows timed). B30 ASR lane = NIL. STANDING DOWN - stopped re-arming timer. 54-video tail (~Jun30) is sibling-owned via ffprobe; force-wake available if a genuine non-dup mid-video case ever appears.
- NEXT: Nothing pending for B30. (Separate, NOT my lane: b27's first-line full run done .12; b15merger built titles-free republish candidate; awaits Max's scope-GO.)
