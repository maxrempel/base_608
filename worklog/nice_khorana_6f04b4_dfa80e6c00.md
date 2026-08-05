
## [2026-07-13 13:01] ? faa85602
- DID: Downloaded UEI launch video (1080p), cut Max's talk (1:01:38-1:19:50), ran retake_cleaner transcribe + custom assemble: proper intro/outro trim + shortened 11 long pauses
- STATE: Final clip done: 'Max Rempel talk UEI launch 20260711 v02_clean.mp4' 16:27, verified by QC frames (host intro / Max mid / host outro)
- NEXT: Awaiting Max feedback; can tweak pause aggressiveness or endpoints if wanted

## [2026-07-13 16:35] ? faa85602
- DID: Uploaded cleaned UEI talk (v03) to Hucolo TV YouTube channel via Max's Chrome (claude-in-chrome); set title, description+17 chapters, unlisted
- STATE: Published UNLISTED at youtu.be/jyMh4KBv-RU on Hucolo TV; file drag-dropped by Max (sandbox blocked auto file attach)
- NEXT: Awaiting Max review; flip to Public when he approves

## [2026-07-18 00:58] ? 2eb1eb83
- DID: Built noeticus-qbot: on-demand verbatim recent visitor questions to Max via Telegram (text+voice), plus 'elaborate N' DeepSeek expansion. Deployed to Dax as systemd service noeticus-qbot (long-poll getUpdates on critical-alarms bot, serves only Max chat 1395850773). Script: tools/noeticus_usage_report/noeticus_question_bot.py; state /home/bitnami/noeticus/logs/qbot_state.json.
- STATE: LIVE + enabled on Dax; --once drained clean, no webhook conflict. List works now; elaborate needs DeepSeek balance (Max topping up).
- NEXT: Await Max's live test of 'questions'; tune default N (60) if needed.

## [2026-07-18 16:09] ? 2eb1eb83
- DID: Found yesterday's (Jul17) YT-summary failures: 9 videos hit DeepSeek 'Insufficient Balance' (transcript cached OK, summary+audio step died). Balance restored ($19.16). Wrote reprocess_failed_summaries_20260718.py on Lak importing yt_transcript_app and replaying cached transcripts through live _summarize_and_push_audio.
- STATE: Reprocess running in bg on Lak; first vids confirmed DeepSeek+FishAudio+Telegram OK. 9 vids: NmQzRMMlCcY 8dg4o8HFY70 HFLBDi87888 kt7F4nnITAQ LASqAqOi8Z0 p1KhXOhpPCQ CSFDEM2uiDY mXRPi3XD2zk sgtd-Asp334.
- NEXT: Confirm all 9 posted; log noeticus-qbot still live.
