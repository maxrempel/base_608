---
title: Sol Migration Progress Report
date: 2026-04-13
author: Opus 4.6 on Pine
status: in progress
---

# Sol Drive Extraction and Migration Progress

## Background

Sol (Lenovo ThinkCentre M720s) died. Max ordered a UGREEN M.2 NVMe USB
enclosure to extract Sol's drive. The drive arrived and was connected to
Pine (Dell Precision 7560).

## What was accomplished 2026-04-13

### 1. WSL installed on Pine

- Installed WSL2 with Ubuntu 24.04 on Pine.
- Had to enable virtualization in BIOS (turned out it was already enabled).
- OOBE (first-run user setup) hung; fixed by killing zombie wsl.exe
  processes, rebooting, then creating the user manually via root.
- User: maxre, password: formality-only local password.

### 2. Sol NVMe drive successfully mounted

- Sol drive: Micron 2300 NVMe 1024GB, detected as PHYSICALDRIVE1.
- Partition table: GPT, partition 1 = EFI (1 GB), partition 2 = ext4 (1023 GB).
- Mounted read-only via `wsl --mount \\.\PHYSICALDRIVE1 --bare` (admin),
  then `mount -o ro /dev/sde2 /mnt/sol` inside WSL.
- Full filesystem readable.

### 3. Sol drive contents confirmed

Key directories in /home/maxre on Sol:
- 00HA1py -- working directory, contains luminous_deploy/
- qdrant_storage -- Qdrant vector DB data (Noeticus/Luminous)
- Nextcloud -- Sol Nextcloud sync folder
- memex-backup-20260309-130519 -- Memex backup from March
- dialog -- dialog trainer data
- kokoro-tts-venv -- Kokoro TTS virtual environment
- backups_maxrempel_site -- old site backups

### 4. DAX-Medium checked via SSH

- DAX-Medium (35.80.203.42) is alive, up 248 days, load 0.00.
- RAM: 3.8 GB total, 686 MB used, 3.2 GB available.
- Disk: 79 GB total, 19 GB used (25%), 57 GB free.
- Running 4 Docker containers (nginx-proxy-manager, MariaDB, two static
  nginx for tamza and colony sites -- all likely obsolete since sites
  moved to Cloudflare).
- Candidate for repurposing as Riga (Noeticus host).

## Next steps

1. SSH into DAX-Medium and verify what is actually needed there vs obsolete.
2. If safe: stop old containers, install Qdrant Docker + cloudflared +
   Syncthing on DAX-Medium (rename conceptually to Riga).
3. Copy luminous_deploy/ and qdrant_storage/ from Sol drive to Pine,
   then deploy to Riga.
4. Set up Syncthing one-way sync: Pine/Nextcloud -> Lakarian -> Riga.
5. Verify Noeticus API works on Riga via cloudflared tunnel.
6. Wipe Sol, reinstall fresh for genomics-only use.

## Infrastructure notes

- Old "DAX" instance (35.166.146.39, micro, $10/mo) status unknown --
  likely dead, needs checking and killing to stop billing.
- Memex is safe on Cloudflare (D1 + Vectorize + R2 + Worker). Not on Sol.
- Sol was only running the cron indexer that fed source files into Memex.
