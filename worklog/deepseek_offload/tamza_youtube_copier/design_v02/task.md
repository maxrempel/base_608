# Tamza weekly video copier — design draft

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Design a reliable Python system that copies completed weekly livestream recordings
from source `https://www.youtube.com/@prostoproverka/streams` to destination
`https://youtube.com/@Tamza`.

## Infrastructure and constraints

- The only allowed downloader is the existing `ytdow` pipeline.
- It runs on always-on Linux server Lak and deposits verified MKV files on the
  Centauri Windows storage machine under its Tamza backup area.
- The source channel must be integrated into ytdow, not fetched by a competing
  downloader.
- Centauri is appropriate for a hidden Windows Scheduled Task.
- All authorization material remains external to source code and logs.
- YouTube previously removed related channels after unwanted material appeared in
  unattended streams. Each future recording therefore needs human approval before
  it can reach the main channel.

## Required behavior

1. Every Tuesday at 01:00 America/Los_Angeles, discover new completed source streams.
2. Consider all unprocessed candidates in the weekly window.
3. Preserve title and description exactly; preserve useful tags and category.
4. Send Max a Telegram approval request with source link, title, date, duration, and
   candidate count. Require explicit approval for each candidate or batch.
5. After approval, use the verified ytdow file on Centauri, validate it with ffprobe,
   and upload with the official YouTube Data API resumable protocol.
6. Upload as unlisted first, verify processing and metadata, then require a second
   explicit approval before making it public.
7. Notify Max when transfer begins, when it finishes, and when it fails.
8. Use a crash-safe SQLite ledger keyed by source video ID. Retries must never create
   duplicates.
9. The job must be hidden, resumable, bandwidth-conscious, and safe across reboots.
10. Include dry-run mode: discovery, metadata, ledger, and local-file verification
    without upload or notification.

## Requested result

Write `result.md` with:

- concise architecture and state machine;
- exact file tree;
- Python module boundaries and command-line interfaces;
- failure and idempotency rules;
- dependency list;
- practical implementation draft and tests;
- pilot and deployment checklist.

Do not perform network actions or publication. Do not propose browser-cookie downloads
or policy bypasses.
