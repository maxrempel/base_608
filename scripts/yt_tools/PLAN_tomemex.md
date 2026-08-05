# yt_tools — plan v01 | 2026-05-04

Two CLI tools any Claude Code chat can run. No GUI. Backed by yt-dlp (already installed).

## Tool 1a: yt_list.py
List recent videos from a YouTube channel.

Usage:
```
python yt_list.py <channel_url> [--limit 50]
```

Output: numbered table to stdout — `# | id | upload_date | duration | title`.
Default limit 50. Writes the same list as JSON to `./logs/list_<timestamp>.json` so a follow-up download knows IDs by index.

## Tool 1b: yt_get.py
Download one video to the standard Windows Downloads folder.

Usage:
```
python yt_get.py <video_id | url | index_from_last_list>
```

- Output dir: `C:\Users\maxre\Downloads\`
- Filename template: `yt_<upload_date>_<id>_<title80>.mp4`
- Format: `bv*+ba/b`, merged to mp4
- Throttle: `--limit-rate 12.5M` (≈100 Mbps), overridable with `--rate`
- Resolves `index_from_last_list` against the most recent `logs/list_*.json`
- Writes a log to `./logs/get_<timestamp>.log`
- Exit codes: 0 ok, non-zero on yt-dlp failure

## Defaults / conventions
- Versioned header in every script (v01, v02, ...)
- Backup before edit (git in cloud_base)
- No emojis, plain ASCII
- Hidden subprocess windows on Windows (`CREATE_NO_WINDOW`)

## Target channel
https://www.youtube.com/@Tamza
