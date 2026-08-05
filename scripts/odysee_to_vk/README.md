# odysee_to_vk

Manual weekly sync: download a video from Odysee, upload it to a VK community.

## Usage (Max paste-and-go)

Paste the Odysee URL to Claude. Claude will:
1. Run `download_odysee.py <url>` — saves MP4 to `downloads/`.
2. Open VK in Playwright. First run: Max logs in by hand once; session persists.
3. Navigate to https://vk.com/clubtamza and upload the MP4.

## Files
- `download_odysee.py` — yt-dlp wrapper, writes to downloads/
- `vk_upload_notes.md` — Playwright walkthrough notes for next chat
- `downloads/` — MP4 output (gitignored / heavy)
- `logs/` — run logs

## Target
- Source: Odysee (URL pasted each week)
- Destination: https://vk.com/clubtamza
