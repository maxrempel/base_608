# Scribe handover - milestone 2 (~152K tokens)
# session: 20260703_quizzical_lewin_4fa47e_6a6f1664
# cwd: C:\claude_base\.claude\worktrees\quizzical-lewin-4fa47e
# written: 2026-07-03 15:04:59 by deepseek-v4-pro

# HANDOVER - Quizzical Lewin (B11B)

## GOAL (Max's words, summarized)
Max wants a **weekly practice page** for his vocal quartet (???????? ?? ??????). Each batch of 5-6 songs should have **video clips of the group's own performances** (or his solo versions where the group hasn't sung it) because the key and arrangement matter for practice. The clips need to be roughly cut from the original full videos stored on the local TEAL16 drive (Centauri), then hosted on **Cloudflare R2** (under tamza.com) with a simple webpage containing playable MP4s and YouTube links. The English song (sixth) may be just a YouTube link to the author's most popular performance. The page URL should be shareable within the group. The process is intended to be repeated weekly with new song batches in the same folder structure under a `practice_batches` directory.

## DECISIONS MADE + WHY
- **Use Tamza catalog database** (`C:/claude_base/tools/tamza_songs/pipeline/output/data.json`): contains all recorded songs with performer, date, YouTube ID, timecodes.
- **Source videos from TEAL16** (`D:\tamza_yt_full_backup\tamza_channel` on Centauri at 192.168.1.176, accessed via SSH with key `~/.ssh/sol_key`): these are already downloaded, so no re-downloading from YouTube.
- **Cut clips with ffmpeg on Centauri** to keep the large video files local; then pull the small clips to Pine (the Windows machine) via SCP.
- **Host via Cloudflare R2** using existing bucket `tamza-media` with credentials from `deploy_catalog.py`; public URL prefix: `https://tamza.com/wp-content/kartoteka/`. Practice folder: `practice/2026-07-03/`.
- **Page structure**: one HTML file per batch, with an inline `<video>` player per clip and a linked YouTube timecode.
- **Song ordering**: prioritized performances by "???????? ?? ??????" first, then ???? ??????? solo, then other performers if no group/solo versions exist (flagged as ??). This was a mid-session correction from Max.
- **Song labels**: use the **first line** of the song as identified by Max (e.g., "??? ?????? ? ??????????" not "?????? ??????"). This was corrected after initial generic title guess.
- **English song**: original line was garbled ("It takes a to make .docx - Google Docs"). Max asked not to guess, but to think - he didn't provide the correct lyrics yet. We are stuck on identification.

## CURRENT STATE (as of session end)
- 5 Russian songs are **cut and online** on the Cloudflare page. The page is live at:  
  **https://tamza.com/wp-content/kartoteka/practice/2026-07-03/index.html**
- Song assignments on that page:
  1. **???????????? ???????** - 2 versions by ???????? ?? ?????? (Jun 7 & May 25, 2025)
  2. **???? ???? ????? ????** - 2 ? ???????? ?? ?????? + 1 ? ???? ??????? solo (3 options)
  3. **?????-?????? ? ???????** - 2 ? ???? ??????? solo (no group version)
  4. **?????? ? ??????? ?????** - ?? Only ???????? ???????? (2021) exists; no group/solo version
  5. **??? ?????? ? ?????????? (?????? ??????)** - ?? Only ?????? ??????????? (2024) exists; no group/solo version
  6. **English song** - **missing entirely**; title/lyrics unknown.
- All local Windows files are in: `C:/claude_base/tools/tamza_songs/practice_batches/batch_2026-07-03/` (index.html + .mp4 clips)
- Centauri temp clips: `D:\tamza_practice_clips\batch_2026-07-03\` (already pulled)
- Cloudflare upload script: `C:/.../scratchpad/upload_r2.py` (reuses bucket credentials from `deploy_catalog.py`)

## EXACT NEXT STEP
1. **Resolve English song identity** - ask Max for a few more words of the lyric (he said not to guess). If he confirms a title, either:
   - Link to the author's most popular YouTube video (no cut/download), or
   - If he wants a cut, locate it in catalog, cut from TEAL16, upload, embed.
2. **Decision on songs 4 & 5 references** - Max needs to confirm whether to keep the other-performer reference clips or drop them.
3. **If Max provides a new song list for next batch**, repeat the find-cut-upload cycle in a new folder `practice_batches/batch_YYYY-MM-DD`.

## OPEN QUESTIONS (awaiting Max)
- **What is the English song?** Currently unknown. Provide actual title or a few recognizable words.
- **For songs 4 & 5**: keep the non-group/non-solo reference performances, or remove them?
- **Is the group name "???????? ?? ??????" exactly?** (Used in catalog search, worked.)
- **Should future batches be numbered by week, or does Max want a specific naming convention?** (Currently using date string.)

## KEY PATHS, IDs, COMMANDS
- Catalog DB: `C:/claude_base/tools/tamza_songs/pipeline/output/data.json`
- Batch local root: `C:/claude_base/tools/tamza_songs/practice_batches/batch_2026-07-03/`
- Centauri videos: `//192.168.1.176/D:/tamza_yt_full_backup/tamza_channel/`
- SSH key: `~/.ssh/sol_key` (user maxre)
- ffmpeg usage: copy video stream, convert audio to AAC for browser mp4:  
  `ffmpeg -ss START -i INPUT -to END -c:v copy -c:a aac -b:a 128k -movflags +faststart OUTPUT.mp4`
- Cloudflare upload script pattern: Python using boto3, endpoint `https://9cd7b8fb6aef9a697e60bfdd57e2cf13.r2.cloudflarestorage.com/tamza-media`, key/secret from `deploy_catalog.py`.
- Public URL pattern: `https://tamza.com/wp-content/kartoteka/practice/BATCH/index.html`

## GOTCHAS / DEAD ENDS RULED OUT
- **Don't guess song titles from vague clues** - Max was annoyed when the assistant guessed "?????? ??????" for "??? ??????...". He wants careful thought based on first lines.
- **Performer key matters**: Max initially accepted the newest performance by any singer, but then corrected that the group's version is essential for practice key. Do NOT use non-group versions if a group/solo version exists.
- **English song is not Dylan's "It Takes a Lot to Laugh"** - that was a guess, and Max didn't confirm, but said not to randomly search. He hasn't given the correct title.
- **Authorization**: R2 bucket is private-write but public-read via Cloudflare's custom domain mapping; you must use the boto3 S3 client with endpoint URL.
- **Centauri SSH**: sometimes times out; keep a 20-second timeout. The Windows PowerShell commands must escape `$` with backtick in SSH command strings.
- **Cyrillic handling**: always use `PYTHONUTF8=1` on Windows Python invocations to avoid encoding issues.
- **Video format**: source videos are mostly h264+opus; when cutting with `-c:v copy`, audio must be re-encoded to AAC for browser compatibility; use `-c:a aac -b:a 128k` with `-movflags +faststart` for web playback.
