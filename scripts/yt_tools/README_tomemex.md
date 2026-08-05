# yt_tools — list and download YouTube channel videos

Two CLI tools backed by yt-dlp.

## Tool 1a: yt_list.py
List recent videos from a YouTube channel.

```
python yt_list.py https://www.youtube.com/@Tamza --limit 50
```

Prints `# | id | date | dur | title` and saves the same as JSON to `./logs/list_<ts>.json` plus `./logs/latest_list.json`.

## Tool 1b: yt_get.py
Download one video to `C:\Users\maxre\Downloads\`.

```
python yt_get.py 7        # 7th row from last yt_list.py run
python yt_get.py dQw4w9WgXcQ
python yt_get.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Default rate cap: `12.5M` (~100 Mbps), override with `--rate`.
Filename: `yt_<upload_date>_<id>_<title80>.mp4`.

## Requirements
- yt-dlp on PATH (already installed Pine-side)
- ffmpeg on PATH (for merging video+audio streams)
- Python 3.x

## Keeping it working
YouTube changes its player signature and "n-challenge" every few weeks.
When that happens, yt-dlp's stable release lags behind and downloads
silently fall back to slow 720p formats (f136+f251) that throttle and
often fail. Symptom: `.f136.mp4.part` files that never finish, plus
warnings like "Signature solving failed" / "n challenge solving failed".

Fix (takes 30 seconds):
```
python -m pip install -U --pre "yt-dlp[default]"
```
The `[default]` extra pulls `yt-dlp-ejs` (the JS challenge solver) and
`--pre` pulls the nightly that has the current YouTube player decoded.
Re-run the download from scratch after updating; partial files from the
old run are the wrong format and should be deleted first.

If you see "Signature solving failed" in the log, that is THE signal to
update. Do not try to resume the old .part files — wipe and restart.

## Exit codes
0 ok / 2 bad args / 3 yt-dlp error
