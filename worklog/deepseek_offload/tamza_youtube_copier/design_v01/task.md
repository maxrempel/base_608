# Tamza YouTube weekly copier — design and implementation draft

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

## Goal

Design a reliable Python system that copies completed weekly livestream recordings
from YouTube source channel `https://www.youtube.com/@prostoproverka/streams` to the
main channel `https://youtube.com/@Tamza`.

## Known infrastructure

- The only sanctioned YouTube downloader is `ytdow`.
- `ytdow` runs on always-on Linux server Lak and deposits verified MKV files on
  Centauri Windows storage at `D:\tamza_yt_full_backup\`.
- The main Tamza channel ID is `UCo-O_aBrW8J3hEGEdow71Iw`.
- Current ytdow watches only Tamza and Hucolo. The source channel must be integrated,
  not downloaded by a second competing process.
- Centauri is reachable and suitable for a hidden Windows Scheduled Task.
- A Telegram alert bot can send to Max from a credential file; secrets must never
  appear in code, logs, task packets, or results.
- Existing history: YouTube terminated Tamza2 and two linked channels on 2026-04-24
  under Circumvention policy after troll pornography appeared in unattended streams.
  Therefore the main channel needs a human approval gate for each future recording.

## Required behavior

1. Every Tuesday at 01:00 America/Los_Angeles, discover newly completed source
   livestream recordings.
2. Consider all unprocessed candidates from the recent weekly window, not just one.
3. Copy original title and description exactly. Preserve relevant tags/category if
   practical.
4. Do not publish automatically. Send Max a Telegram approval request containing the
   source URL, title, date, duration, and candidate count. Require explicit approval
   for each candidate or batch before upload.
5. On approval, obtain the already-downloaded ytdow file from Centauri, verify size
   and media streams with ffprobe, then upload through the official YouTube Data API
   resumable upload to the authorized `@Tamza` channel.
6. Upload as `unlisted` initially. Verify the resulting YouTube video metadata and
   processing state. A separate explicit approval should promote it to `public`, or
   propose a safe alternative if the API cannot reliably perform the final check.
7. Send Telegram notifications when transfer starts, when upload finishes, and on
   failure. Never expose OAuth tokens, bot tokens, or private IDs.
8. Maintain a durable JSON or SQLite ledger keyed by source video ID so retries never
   create duplicates. State transitions must be crash-safe and auditable.
9. The job must be hidden, resumable, bandwidth-conscious, and safe if Centauri
   reboots. No visible terminal windows.
10. Include a dry-run mode that performs discovery, metadata extraction, ledger
    checks, and local file verification without uploading or sending approval.

## Output requested

Produce `result.md` containing:

- concise architecture and state machine;
- exact proposed file tree;
- Python module boundaries and command-line interfaces;
- failure cases and idempotency rules;
- dependency list;
- a practical implementation draft for the central Python script and tests, but do
  not include or invent credentials;
- a pilot and deployment checklist.

Do not recommend bypassing YouTube rules or using browser cookies from the main
account for downloads. Do not perform any network action or publication.
