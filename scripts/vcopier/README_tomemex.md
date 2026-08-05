# Vcopier - YouTube to VK copier

One command: paste a YouTube URL, get it re-uploaded to the configured
VK community with the YouTube title copied automatically. Originally
built for mirroring the Tamza YouTube channel to the VK group.

## Usage
```
python vcopier.py <youtube_url>
```

Optional flags:
- `--no-wall`         do NOT post to the community wall
- `--no-source-link`  do NOT include "Source: <url>" in the description
- `--keep-days N`     change cache retention (default 30 days)

## What it does on every run
1. Prunes cached video files older than `--keep-days` (default 30) from
   `C:\Users\maxre\Downloads\vcopier_cache\`. Only this folder is touched.
2. Probes the YouTube URL for id, title, upload_date (no download yet,
   uses `--dump-json` so Cyrillic titles survive Windows cp1251 stdout).
3. If `yt_<date>_<id>_*.mp4` already exists in the cache, reuses it.
   Otherwise downloads with `yt-dlp -f bv*+ba/b --merge-output-format mp4`.
4. Calls VK `video.save` with the YouTube title as the VK title and
   "Source: <url>" in the description.
5. Uploads the merged .mp4 multipart to the returned upload URL.
6. Prints the public `https://vk.com/video<owner>_<id>` link.

## Config files (one line each, no quotes)
- `C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_user_token.txt` - VK access
  token with scopes `video,groups,offline`. See
  `..\vk_upload\GET_TOKEN_tomemex.md` for how to mint one (never expires).
- `C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_group_id.txt` - positive
  community id. For clubtamza this is `200032154`.

## Requirements
- yt-dlp nightly with EJS solver:
  ```
  python -m pip install -U --pre "yt-dlp[default]"
  ```
- ffmpeg on PATH (already installed via Gyan.FFmpeg winget package).

## Where to run
Developed and tested on Pine. For production batch backfills the natural
home is Centauri (home network, big disk, runs 24/7) or Sol (Ubuntu home
server). Migration: copy this folder, install yt-dlp nightly + ffmpeg,
drop the same two config files in the equivalent ssh folder, done.

## Exit codes
0 ok / 2 bad args/missing config / 3 yt-dlp error
4 VK API error / 5 VK upload server error
