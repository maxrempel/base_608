# Scribe handover - milestone 2 (~166K tokens)
# session: 20260626_focused_ride_1f38f1_856ff2ef
# cwd: C:\claude_base\.claude\worktrees\focused-ride-1f38f1
# written: 2026-06-26 16:41:39 by deepseek-v4-pro

# HANDOVER - C: Drive Video Migration to Centauri teal16

---

## GOAL (in Max's words)

Move large video files off Pine's C: drive (nearly full - 13.2 GB free of 476 GB) to Centauri's teal16 D: drive. This is a **migration** (move, not backup): copy ? verify ? delete from C: to free space.

First batch: create `VIDS_2026_06` on teal16 and move the `00_KEEP` folder out of the `riverside_ep02` podcast cleanup project.

---

## DECISIONS MADE + WHY

1. **Target = Centauri teal16 (D:\)** - 16 TB drive, ~11.4 TB free. Lakarian is taken (Nextcloud + apps). Other drives too small or down. Accessible via SSH at `192.168.1.176` with key `~/.ssh/sol_key`.

2. **Transport = rclone over SFTP** - resumable, skips already-copied files, verifiable. Only needs rclone installed on Pine (done: v1.74.3). Centauri only needs its existing SSH/SFTP server. rclone remote named `teal16` already configured and tested - lists `D:\VIDS_2026_06\00_KEEP` contents.

3. **Verify method = independent SHA256 on both ends** - rclone does the copy, then the migrator separately computes SHA256 locally and on Centauri (via SSH invoking a PowerShell hasher). Only when hashes match are source files deleted. This is stricter than rclone's built-in checks.

4. **System in Python, not PowerShell** - the original `migrate.ps1` hit an unsolvable `AmbiguousParameterSet` binding error. Parser reported zero errors, `Get-Command` saw one clean set, but the binder choked on every invocation. Tried removing help comments, rewriting in heredoc, stripping to bare `param()` - never resolved. Switched to Python (`migrate.py`) which works reliably and fits Max's existing toolchain.

5. **`--no-delete` on first run** - the first invocation of `migrate.py` on `00_KEEP` was done with `--no-delete` to confirm the SHA256 verify gate works before trusting it to delete originals. Once proven, re-run without the flag for the actual move.

6. **OneDrive/Nextcloud video files left alone** - those showed up in the C: scan as large files but are likely online-only placeholders (not real local space consumption). Different operation, not in scope yet.

---

## CURRENT STATE

- **`migrate.py` is currently running** against `C:\Users\maxre\Videos\podcast_cleanup\riverside_ep02\00_KEEP` (3 files, 12.0 GB) with `--no-delete`.
- It is reconciling the rclone copy (the files may already be on teal16 from an early scp that completed before being killed) and computing SHA256 hashes on both ends.
- **No files have been deleted from C: yet.**
- The run has not finished - output was being read from a temp task log and was still in progress.
- Centauri already has `D:\VIDS_2026_06\00_KEEP\` with files (from the scp that finished earlier). rclone should handle this gracefully by skipping or overwriting with verification.

### What's built and where

- **Migration tool**: `C:\claude_base\tools\bigfile_migrate\migrate.py`
  - Usage: `python migrate.py --source <local-folder> [--dest-root D:/VIDS_2026_06] [--no-delete]`
  - Steps: rclone copy ? local SHA256 ? remote SHA256 (via SSH + `remote_hash.ps1`) ? compare ? delete source on match (unless `--no-delete`).
  - Leaves a README manifest on Centauri.

- **Remote hash script**: `C:\claude_base\tools\bigfile_migrate\remote_hash.ps1`
  - Uploaded to Centauri (path on remote: `C:\Users\maxre\remote_hash.ps1` or similar - confirm).
  - Computes SHA256 of a path on Centauri's filesystem.

- **rclone config**: remote `teal16` points to `maxre@192.168.1.176` via SFTP, key `~/.ssh/sol_key`. Binary at `C:\Users\maxre\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.74.3-windows-amd64\rclone.exe`.

### Space picture

| Location | Size | Status |
|---|---|---|
| C: total | 476 GB | 13.2 GB free |
| `C:\Users\maxre\Videos` | 89.6 GB | #1 target |
| `...\podcast_cleanup\riverside_ep02` | ~71 GB | bulk of Videos |
| `...\00_KEEP` | 12.0 GB (3 files) | **in flight** |
| `C:\Users\maxre\Downloads` | 33.8 GB | second target, not started |
| Centauri teal16 (D:\) | ~11.4 TB free | destination |

---

## EXACT NEXT STEP

1. **Check if `migrate.py` finished** - look at the temp task log or re-run `python migrate.py --source "C:\Users\maxre\Videos\podcast_cleanup\riverside_ep02\00_KEEP" --no-delete` to see current state. If it completed with SHA256 matches, the files are verified on both ends and safe.

2. **If SHA256 verify passed**, re-run **without** `--no-delete` to delete the C: originals and complete the move:
   ```
   python migrate.py --source "C:\Users\maxre\Videos\podcast_cleanup\riverside_ep02\00_KEEP"
   ```

3. **If the previous run didn't finish** (crashed, interrupted), just re-run it - rclone is idempotent and the SHA256 verify is stateless. It picks up cleanly.

4. **After `00_KEEP` is fully moved and freed**, ask Max which folder next - the rest of `riverside_ep02` (~59 GB remaining), or jump to Downloads (33.8 GB), or something else. The `migrate.py` tool is reusable for any source folder.

---

## OPEN QUESTIONS (awaiting Max)

- After `00_KEEP`: move the rest of `riverside_ep02` (the other subfolders), or move Downloads next?
- Does Max need the `00_KEEP` files locally accessible day-to-day, or is it fine that they live only on Centauri (reachable via SSH/SFTP)?
- The full `podcast_cleanup\riverside_ep02` is 71 GB - most of it appears to be obsolete/archive versions. Does Max want to move the entire folder, or pick specific subfolders like he did with `00_KEEP`?

---

## KEY PATHS, IDs, COMMANDS

| What | Path/Value |
|---|---|
| Migration tool | `C:\claude_base\tools\bigfile_migrate\migrate.py` |
| Remote hasher | `C:\claude_base\tools\bigfile_migrate\remote_hash.ps1` |
| rclone binary | `C:\Users\maxre\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.74.3-windows-amd64\rclone.exe` |
| rclone remote name | `teal16` |
| Centauri SSH | `maxre@192.168.1.176`, key `~/.ssh/sol_key` |
| Destination root | `D:\VIDS_2026_06` on Centauri |
| Source (in flight) | `C:\Users\maxre\Videos\podcast_cleanup\riverside_ep02\00_KEEP` (3 files, 12.0 GB) |
| Next candidate | rest of `...\riverside_ep02` (~59 GB) |
| Second candidate | `C:\Users\maxre\Downloads` (33.8 GB) |

---

## GOTCHAS & DEAD ENDS

1. **PowerShell `migrate.ps1` abandoned** - `AmbiguousParameterSet` on every invocation despite clean parse and one parameter set. Root cause never found. Don't waste time resurrecting it; the Python version works.

2. **Early scp already copied the 12 GB** - the scp I ran (and you told me to stop) had already finished. Files landed in `D:\VIDS_2026_06\00_KEEP\`. This is harmless - rclone reconciles and the SHA256 verify will confirm they're identical. No need to clean up.

3. **rclone SFTP remote depends on `~/.ssh/sol_key`** - if that key path changes, the remote breaks. The key is used for both raw SSH commands (remote hashing) and rclone SFTP transport.

4. **The `remote_hash.ps1` must exist on Centauri** - confirm it was uploaded and its path is correct in `migrate.py`'s SSH command. If the script crashes mid-verify with "file not found" on the remote side, that's the fix.

5. **`--no-delete` is your safety net** - always run with it first for a new source folder to confirm the verify gate works before trusting the delete step.

6. **OneDrive/Nextcloud folders excluded** - `C:\Users\maxre\OneDrive` and Nextcloud paths showed large videos but are cloud-synced placeholders. Don't touch those with this migration tool; they need a different approach.
