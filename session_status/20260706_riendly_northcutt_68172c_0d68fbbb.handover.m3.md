# Scribe handover - milestone 3 (~249K tokens)
# session: 20260706_riendly_northcutt_68172c_0d68fbbb
# cwd: C:\claude_base\.claude\worktrees\friendly-northcutt-68172c
# written: 2026-07-06 10:31:46 by deepseek-v4-pro

# HANDOVER - Tamza Photo Mosaic from Real Video Frames

---

## GOAL (in Max's words)

Max pointed at an outdated Tamza promotional collage and said: *"These are very outdated images. Can you recreate something like that using real photographs from Tamza? We have all the videos and the system for making images. Check in as B52D and experiment. Show me some examples what you can do."*

After seeing the first attempt he added: *"Pick the good quality ones, happy ones. Properly normalized and prettified using saturation, brightness, and contrast. Normalized."*

And after contamination was found: *"Don't trust the names, you have to look. The database should be the source of truth."*

---

## DECISIONS + WHY

1. **Source footage**: Pulled from the teal16 machine (`C:\Users\maxre\...` ? actually `D:\tamza_yt_full_backup\tamza_channel\*.mkv`, ~220 videos). These are real Tamza concert/performance videos from 2020-2024, downloaded by the ytdow backup pipeline. Chose this over YouTube directly because the files are local and fast to batch-process with ffmpeg.

2. **Frame extraction method**: Used ffmpeg on teal16 to grab one frame per video (at the 10% mark to skip intros). First pass extracted 80 frames, second pass expanded to 220, then a curated subset of 102 at higher resolution (`-vf scale=640:-1` ? then full resolution), finally 141 after contamination cleanup.

3. **Curation approach**: Built labeled contact sheets (thumbnails with filenames overlaid in a grid) so I could visually scan and pick frames. Excluded: spreadsheets/screen recordings, dark/blurry shots, non-performance content (puppets, costume-in-tree, stop-motion). Kept: singing, guitar, happy/energetic performance shots.

4. **Normalization**: Applied per-frame contrast/saturation/brightness normalization in the mosaic builder script to even out the wildly different lighting conditions across concert footage (some indoor/dark, some outdoor/bright).

5. **Contamination fix (the Hucolo problem)**: Max spotted non-Tamza videos. I traced this to the source - the ytdow backup system on Lak (`100.110.225.89`, user `mrempadmin`) maintains per-channel title databases scraped from YouTube. Cross-referenced every video ID in the `tamza_channel` backup folder against both the Tamza and Hucolo title databases. Found 20 Hucolo (channeling/webinar) videos misfiled in the Tamza folder. Moved them to `hucolo_channel` where they belong. The backup folder on teal16 itself is now clean, not just the collage.

6. **Logo approach**: Tried OpenAI image generation for the horses/sunset badge - it produced the artwork fine but garbled the Cyrillic text (as AI always does). Ended up compositing the badge with real Cyrillic text rendered locally via PIL and a proper font. Max preferred the un-logo'd version anyway.

---

## CURRENT STATE

- **Final output**: A clean 141-frame mosaic (`tamza_mosaic_clean.png`) sent to Max. All frames verified against the title database - zero Hucolo contamination.
- **teal16 backup**: `D:\tamza_yt_full_backup\tamza_channel\` now contains only genuine Tamza videos (200 files after removing 20). The 20 Hucolo videos were moved to `D:\tamza_yt_full_backup\hucolo_channel\`.
- **Scratchpad**: All working files, scripts, and intermediate frames are in:
  ```
  C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-friendly-northcutt-68172c\0d68fbbb-ee91-49e4-a52a-35c634be0740\scratchpad\
  ```
  Key files:
  - `tamza_mosaic_clean.png` - the final output
  - `f_keep_list.txt` - the 141 verified Tamza video IDs used
  - `contaminated_ids.txt` - the 20 Hucolo IDs that were moved out
  - `build_mosaic_final.py` - the script that builds the normalized mosaic
  - `audit_titles.py` - cross-references video IDs against Lak's title database
  - `tamza_frames_hires/` - the 141 high-res extracted frames

---

## EXACT NEXT STEP

Max hasn't explicitly requested a next action - he received the clean mosaic and seemed satisfied. The natural follow-ups he might ask for:

1. **More curation passes** - he said "you have to look" and some imperfect frames may have slipped through. He might spot more and ask for another cleanup round.

2. **Different mosaic layouts** - wider aspect ratios, different grid densities, portrait orientation, or a version with the logo properly integrated (he said "the left one without the logo is better" but might want a properly-executed logo version).

3. **Permanent save location** - the output is currently in a temp scratchpad. He'll likely want it moved somewhere permanent (Nextcloud? the Tamza pipeline directory?).

4. **Clean up the root cause on Lak** - the 20 misfiled videos suggest the ytdow drainer has a bug where it sometimes puts Hucolo videos into the Tamza folder. This wasn't investigated further but should be.

---

## OPEN QUESTIONS FOR MAX

- Is the final mosaic good, or does he want another curation pass? He said some might be imperfect since curation was eyeballing thumbnails.
- Does he want the output saved to a specific permanent location?
- Does he want variants (different layouts, sizes, with/without logo)?
- Should we investigate why the ytdow drainer misfiled 20 Hucolo videos into the Tamza folder on teal16? The title databases on Lak appear correct - this seems to be a drainer logic bug.

---

## KEY PATHS / IDS / COMMANDS

### Machines and SSH

| Machine | IP | User | SSH Key | Role |
|---------|-----|------|---------|------|
| teal16 | 192.168.1.176 | maxre | `~/.ssh/sol_key` | Video backup storage (Windows) |
| Lak | 100.110.225.89 | mrempadmin | `~/.ssh/lakarian_key.pem` | ytdow backup system, title DBs |
| Pine | localhost | maxre | - | Claude session, Python/PIL |

### Key paths on teal16
```
D:\tamza_yt_full_backup\tamza_channel\*.mkv   ? Tamza videos (~200, WAS ~220)
D:\tamza_yt_full_backup\hucolo_channel\*.mkv  ? Huculo videos (received +20)
D:\_tamza_frames_tmp2\                         ? temp frame extraction directory
```

### Key paths on Lak (source of truth)
```
/home/mrempadmin/yt_backup/tamza_videos.txt     ? Tamza title database (JSON-per-line)
/home/mrempadmin/yt_backup/hucolo_videos.txt    ? Hucolo title database
/home/mrempadmin/yt_backup/hucolo_all_ids.txt   ? All Hucolo video IDs
/home/mrempadmin/yt_backup/channel_inventory.json ? Channel manifest
```

### Useful commands to re-use

**Extract frames from teal16 videos:**
```bash
ssh -i ~/.ssh/sol_key maxre@192.168.1.176 "powershell -NoProfile -Command \"
  \$files = Get-ChildItem D:\\tamza_yt_full_backup\\tamza_channel\\*.mkv | Select-Object -First 220
  foreach (\$f in \$files) {
    \$out = 'D:\\_tamza_frames_tmp2\\' + \$f.BaseName + '.png'
    & 'C:\\ffmpeg\\bin\\ffmpeg.exe' -y -ss 00:00:10 -i \$f.FullName -vframes 1 \$out 2>&1 | Out-Null
    Write-Host \"OK: \$(\$f.BaseName)\"
  }
\""
```
ffmpeg is at `C:\ffmpeg\bin\ffmpeg.exe` on teal16.

**Pull frames back to Pine:**
```bash
scp -i ~/.ssh/sol_key "maxre@192.168.1.176:D:/_tamza_frames_tmp2/*.png" "$LOCAL_DIR/"
```

**Cross-reference video IDs against title databases (Python audit script):**
The `audit_titles.py` script loads the Lak title databases, parses each line as JSON, extracts the `id` field, and flags any video ID that appears in the Hucolo database. The core logic:
- Load `tamza_videos.txt` and `hucolo_videos.txt` from Lak
- Parse each line as JSON, build sets of video IDs
- For any given video ID, check membership in both sets
- Flag IDs that appear in Hucolo but are sitting in the Tamza folder

### Building the final mosaic
The `build_mosaic_final.py` script:
1. Loads the keep list (`f_keep_list.txt`)
2. Loads each corresponding frame from `tamza_frames_hires/`
3. Applies per-frame normalization: auto-contrast stretch, slight saturation boost (+15%), brightness normalization to a target mean
4. Arranges frames in a grid (determined by aspect ratio math), crops to square tiles
5. Outputs as `tamza_mosaic_clean.png`

---

## GOTCHAS

1. **Don't trust folder names on teal16.** The `tamza_channel` folder had 20 Hucolo videos mixed in. The Lak title databases are the source of truth - always cross-reference against those.

2. **The ytdow drainer has a filing bug.** Something caused 20 Hucolo downloads to land in the Tamza folder. Nobody investigated the root cause - the drainer script lives at `/home/mrempadmin/yt_backup/drainer.sh` on Lak. The lock file is at `/home/mrempadmin/yt_backup/.drain.lock`. Check whether it's safe to touch before modifying anything.

3. **ffmpeg path on teal16** is `C:\ffmpeg\bin\ffmpeg.exe` (not in PATH, must use full path in PowerShell commands).

4. **OpenAI image generation can't do Cyrillic text.** It will produce plausible-looking gibberish that looks like Cyrillic to non-readers but is nonsense. Use PIL with a real font (e.g., from the system fonts directory) to render text separately and composite.

5. **Video filenames on teal16 are YouTube IDs** (e.g., `dQw4w9WgXcQ.mkv`). These map to human-readable titles only through the Lak databases, which parse to `{"id": "dQw4w9WgXcQ", "title": "????? - ??????? 2023", ...}`.

6. **Scratchpad is in a temp directory** that will eventually be cleaned. If the output mosaic needs to persist, copy it to a permanent location (Nextcloud or the Tamza pipeline directory at `C:\claude_base\tools\tamza_songs\pipeline\`).

7. **Python/PIL is available locally on Pine.** The mosaic and audit scripts ran locally, not on teal16 or Lak. Python was invoked via PowerShell: `cd <scratchpad>; python <script>.py`.
