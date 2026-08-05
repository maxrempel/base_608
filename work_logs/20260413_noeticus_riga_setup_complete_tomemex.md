---
title: Noeticus Riga Setup -- Complete Configuration
date: 2026-04-13
author: Opus 4.6 on Pine
status: LIVE
---

# Noeticus is Live on Riga (DAX-Medium)

## URLs (all working)

- https://ai.maxrempel.com -- main access point
- Frontend: Cloudflare Worker (maxrempel-site, unchanged)
- Backend: DAX-Medium (35.80.203.42) via Cloudflare Tunnel

## Host: DAX-Medium (Riga)

- AWS Lightsail, IP 35.80.203.42 (static: DAX-StaticIP)
- 4 GB RAM, 2 vCPU, 80 GB SSD, $20/mo
- Debian 12, user: bitnami
- SSH key on Pine: C:\Users\maxre\.ssh\dax_lightsail_max_id_rsa.pem

## Services running (all systemd, all restart=always)

1. **qdrant** (Docker) -- vector DB, port 6333
   - Data: /home/bitnami/noeticus/qdrant_storage/
   - Collection: luminous, 3734 vectors, text-embedding-3-small
2. **noeticus.service** -- FastAPI backend, port 8080
   - Script: /home/bitnami/noeticus/scripts/noeticus_api_v6_riga_20260413.py
   - Venv: /home/bitnami/noeticus/venv/
   - Version: v6.0.0
3. **cloudflared.service** -- Cloudflare Tunnel
   - Tunnel: riga-noeticus (960bc2bd-9ba9-479c-be3c-ce923d5d45e8)
   - Routes: ai.maxrempel.com -> localhost:8080
4. **syncthing-bitnami.service** -- Syncthing file sync
   - Device ID: 6ZLZ2KT-W6C4QDB-OITA7CY-RMMDXGV-RGA6JYR-U5Z5O2P-FYRFKW6-Z5OBXQO
   - Paired with Lakarian (DHQ36WQ-...)
   - Shared folder: z_luminous_kb (receive-only)
5. **colony-static-nginx** (Docker) -- humancolony.org static site, port 8082
6. **nginx-proxy-manager** (Docker) -- reverse proxy for humancolony.org
7. **npm-db** (Docker) -- MariaDB for nginx-proxy-manager

## Cron

- Every 15 min: autoingest v3 checks /home/bitnami/noeticus/kb/ for new .md files
  and ingests them into Qdrant

## Content update flow

Pine/Vega -> edit .md files in Nextcloud/z_luminous_kb/
    -> Nextcloud syncs to Lakarian
    -> Syncthing (send-only from Lakarian, receive-only on Riga)
    -> /home/bitnami/noeticus/kb/
    -> cron autoingest every 15 min
    -> Qdrant luminous collection updated
    -> Noeticus serves new content

## File layout on Riga

/home/bitnami/noeticus/
  keys/           -- API keys (OpenAI, Anthropic, DeepSeek)
  scripts/        -- API script, autoingest script
  kb/             -- Syncthing receive folder (from Lakarian)
  qdrant_storage/ -- Qdrant data (Docker mount)
  logs/           -- API log, ingest log, syncthing log
  venv/           -- Python virtual environment

## API keys on Riga

- /home/bitnami/noeticus/keys/openai_api_key_20260216.txt
- /home/bitnami/noeticus/keys/anthropic_api_key_ant_max2_60218.txt
- /home/bitnami/noeticus/keys/deepseek_api_key_20260226.txt

## Cloudflare Tunnel details

- Tunnel name: riga-noeticus
- Tunnel ID: 960bc2bd-9ba9-479c-be3c-ce923d5d45e8
- DNS: ai.maxrempel.com CNAME -> 960bc2bd-9ba9-479c-be3c-ce923d5d45e8.cfargotunnel.com
- Old Sol tunnel (sol-openclaw, 48c75755-eba3-4cfc-867b-66291e976b66) is now unused

## Syncthing pairing

Lakarian (send-only):
- Device ID: DHQ36WQ-UFNKSWA-WGQMOJ4-ZBUJIF7-LXZCRLK-LAYC6RB-66AVQ3U-A5ZCHA7
- Source: /home/yunohost.app/nextcloud/data/mremp/files/z_luminous_kb
- syncthing user added to nextcloud group for read access
- Runs as system service (YunoHost install)

Riga/DAX (receive-only):
- Device ID: 6ZLZ2KT-W6C4QDB-OITA7CY-RMMDXGV-RGA6JYR-U5Z5O2P-FYRFKW6-Z5OBXQO
- Destination: /home/bitnami/noeticus/kb
- Runs as syncthing-bitnami.service

## What migrated from Sol

- qdrant_storage/ (94 MB compressed, 689 MB tar) -- copied via SCP through Pine
- luminous_api_v5 -> adapted to v6 with Riga paths
- luminous_autoingest_v2 -> adapted to v3 with Riga paths
- starseedai_chat.html -- fallback HTML for direct API access
- Visitor logs archived to Pine (starseedai_visitors.jsonl, starseedai_stats.json)

## Also on this host

- humancolony.org -- static site via nginx + nginx-proxy-manager
- Old WordPress backup cron (can be removed)

## WSL installed on Pine

As part of this migration, WSL2 (Ubuntu 24.04) was installed on Pine
to mount Sol's ext4 NVMe drive via USB enclosure. WSL is useful for
future Linux disk access and local testing.
