---
title: Noeticus Migration Design -- Sol to DAX (Riga)
date: 2026-04-13
author: Opus 4.6 on Pine
status: design doc, pre-implementation
---

# Noeticus Migration Design: Sol to DAX (Riga)

## What is Noeticus

Noeticus (public name; internal codename Luminous) is a RAG chatbot serving
Max's publications -- Postcontact book, Celestial Science digest, Acid for
Squares podcast, and related materials. It speaks from a starseed/new age
perspective as a defined AI personality.

Live URLs (all currently DOWN because Sol died):
- www.maxrempel.com/ai (main site route)
- ai.maxrempel.com (standalone subdomain)
- noeticusai.com (registered on Route 53, Cloudflare zone)

## Current architecture (Sol, now dead)

Frontend: Cloudflare Worker (maxrempel-site). One handleLuminous() function
serves the chat HTML for all URLs. Worker source in luminous_deploy/worker.js.

Backend: FastAPI script (luminous_api_v5_20260310.py) on port 8080.
Streaming responses. DeepSeek for free tier, Claude Opus for paid tier.
Rate-limited: 10 req/60s per IP, Max's subnet exempt.

Vector DB: Qdrant in Docker. Collection "luminous". Embeddings via OpenAI
text-embedding-3-small. Storage: 94 MB total.

Tunnel: Cloudflare tunnel "sol-openclaw" routes ai.maxrempel.com to
localhost:8080.

KB ingestion: Auto-ingest cron every 15 min. Reads .md files from
z_luminous_kb/ folder (Nextcloud-synced). MD5 manifest tracks changes.
Script: luminous_autoingest_v2.py.

## Content update flow (was, and will be again)

Pine/Vega -> edit .md files in Nextcloud/z_luminous_kb/ -> Nextcloud syncs
to Sol (was direct) -> cron picks up changes -> ingests into Qdrant.

System prompt lives in Notion (page 3210316f-5560-8112-8b9e-d14210318732).

## New architecture: DAX-Medium becomes Riga

Target host: DAX-Medium (35.80.203.42), AWS Lightsail.
4 GB RAM, 2 vCPU, 80 GB SSD, $20/mo. Currently running obsolete nginx
containers from old WordPress era. 57 GB free disk.

### Components to deploy on Riga

1. Qdrant Docker container (needs ~94 MB data + ~500 MB RAM)
2. FastAPI backend (luminous_api_v5 or newer)
3. cloudflared tunnel (new tunnel, replacing sol-openclaw)
4. Syncthing (receive-only, for content sync from Lakarian)
5. Auto-ingest cron (luminous_autoingest_v2.py, every 15 min)

### Content sync flow (new)

Pine/Vega -- Max edits .md files in Nextcloud/z_luminous_kb/
    |
    v
Lakarian (Nextcloud server) -- syncs normally via Nextcloud
    |
    v (Syncthing, one-way, receive-only on Riga)
Riga (DAX-Medium) -- /home/[user]/z_luminous_kb/
    |
    v (cron every 15 min)
Qdrant on Riga -- luminous collection updated

Key principle: Riga never pushes back. One-way flow. No conflicts possible.
Lakarian is the Nextcloud server. Riga gets Syncthing only (no Nextcloud
server/client on Riga).

### What syncs via Syncthing

- z_luminous_kb/ -- knowledge base .md files (content Max edits)
- zSyncMain/scripts/ -- API script, ingest script (code updates)
- Possibly system prompt config if we externalize it

### What does NOT sync (must be copied once from Sol)

- qdrant_storage/ (94 MB) -- vector DB data, copy from Sol drive
- cloudflared config -- new tunnel, configured fresh on Riga
- systemd units -- written fresh on Riga

## Files confirmed on Sol drive (mounted read-only via WSL on Pine)

Sol drive: Micron 2300 NVMe 1024GB, mounted at /mnt/sol in WSL.

- /home/maxre/00HA1py/luminous_deploy/worker.js + wrangler.toml
  (Cloudflare Worker source -- deployed to Cloudflare, not to Riga)
- /home/maxre/Nextcloud/zSyncMain/scripts/luminous_api_v5_20260310.py
  (also already on Pine via Nextcloud sync)
- /home/maxre/Nextcloud/sol_00HA1_scripts/luminous_autoingest_v2.py
- /home/maxre/qdrant_storage/ (94 MB -- MUST copy to Riga)
- /home/maxre/00HA1py/logs/starseedai_visitors.jsonl (visitor logs, archive)
- /home/maxre/00HA1py/logs/starseedai_stats.json (visitor stats, archive)

## Files already on Pine via Nextcloud

- C:\Users\maxre\Nextcloud\zSyncMain\scripts\luminous_api_v5_20260310.py
- C:\Users\maxre\Nextcloud\z_luminous_kb\ (knowledge base folder)

## Migration steps

1. SSH into DAX-Medium, stop old containers (nginx-proxy-manager,
   MariaDB, colony-nginx, tamza-nginx).
2. Install Qdrant Docker on DAX-Medium.
3. Copy qdrant_storage/ from Sol drive (Pine WSL) to DAX via scp.
4. Copy/deploy luminous_api_v5 script to DAX.
5. Copy luminous_autoingest_v2.py to DAX.
6. Create new cloudflared tunnel on DAX, route ai.maxrempel.com to
   localhost:8080.
7. Update Cloudflare Worker KV if API URL changes.
8. Install Syncthing on DAX, set receive-only, pair with Lakarian.
9. Configure Syncthing folders: z_luminous_kb, zSyncMain/scripts.
10. Set up cron for auto-ingest every 15 min.
11. Set up systemd units for: Qdrant, API, cloudflared, Syncthing.
12. Test all three URLs.
13. Archive Sol visitor logs to Pine.
14. Rename DAX-Medium to Riga conceptually.

## Open questions

- Old "DAX" instance (35.166.146.39, $10/mo) -- check if alive, kill if dead.
- Do we keep nginx-proxy-manager on Riga or go cloudflared-only?
  Recommendation: cloudflared-only, simpler.
- API script version -- is v5 the latest or did Sol have something newer
  running as a detached process? The Memex doc says v5.5 features were
  done but the script filename is still v5. Need to check the actual
  running code.
- Syncthing on Lakarian -- is it already installed? Need to verify.

## Budget

DAX-Medium: $20/mo (already paying)
Lightsail snapshots: ~$0.05/GB/mo (auto daily backups)
Old DAX if killed: saves $10/mo
Net: ~$20/mo for Riga, same as current DAX-Medium cost.
