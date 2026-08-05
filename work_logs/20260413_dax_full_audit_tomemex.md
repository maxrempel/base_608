# DAX Server Full Audit -- 2026-04-13
# Author: Opus 4.6, Pine, Claude Code
# Purpose: Complete state of DAX-Medium (Riga) after Noeticus migration and humancolony.org fix

## Server

- Name: DAX-Medium (Riga)
- IP: 35.80.203.42
- Provider: AWS Lightsail, $20/mo
- OS: Debian 12
- User: bitnami
- SSH key: C:\Users\maxre\.ssh\dax_lightsail_max_id_rsa.pem
- Disk: 79GB total, 20GB used, 57GB free (26%)
- Python: 3.11.2

## Docker Containers (4 running)

1. nginx-proxy-manager -- ports 80, 81 (admin), 443. Reverse proxy for all sites. MariaDB backend (npm-db container).
2. npm-db -- MariaDB 10. Database for NPM.
3. colony-static-nginx -- port 8082. Serves humancolony.org static export from /home/bitnami/colony_static/.
4. qdrant -- ports 6333-6334. Vector DB for Noeticus.

## Systemd Services

- noeticus.service -- FastAPI v6 on port 8080. Noeticus RAG chatbot.
- cloudflared -- Cloudflare tunnel "riga-noeticus". Routes ai.maxrempel.com to localhost:8080.
- syncthing-bitnami -- Syncthing for KB sync from Lakarian.
- bitnami.service -- legacy Bitnami stack, includes local MySQL on 3306.
- docker.service

## Syncthing

- GUI: 127.0.0.1:8384
- Paired with: Lakarian only
- Shared folders:
  - "Default Folder" at /home/bitnami/Sync (send-receive, empty)
  - "Luminous KB" (z_luminous_kb) at /home/bitnami/noeticus/kb (receive-only from Lakarian)
  - "Memex Memories" (memex_memories) -- PENDING acceptance on DAX side. Added on Lakarian 2026-04-13.

## Websites

- humancolony.org -- LIVE. Static nginx on port 8082, SSL via NPM (Let's Encrypt, expires 2026-07-12).
- bhaktitemple.org -- NOT on DAX. Lives on Lakarian (66.75.229.142). NPM had old proxy entry, now gone.
- dnaresonance.org, localizedtherapeutics.com, tamza.com -- NPM proxy entries were lost when NPM was reset 2026-04-13. WordPress containers for these are NOT running. Docker images still on disk but no active containers. Status unclear -- may have been moved elsewhere or deprecated.

## NPM (Nginx Proxy Manager)

- WARNING: Database was reset on 2026-04-13 22:52 UTC during Noeticus setup session. All previous proxy hosts and SSL certs were lost.
- Currently only humancolony.org proxy host is configured (restored this session).
- Admin: admin@example.com / changeme (DEFAULT -- should be changed).
- Old NPM MySQL backup exists: /home/bitnami/npm_full_backup_20250807_221105.sql (36KB, from Aug 2025).

## Cron Jobs (bitnami)

1. Daily 9:00 UTC -- backup_wordpress_daily.sh (restic backup of bhaktitemple to Lakarian via SFTP). Running successfully.
2. Every 15 min -- noeticus_autoingest_v3_riga_20260413.py. Scans /home/bitnami/noeticus/kb/ for new files, indexes into Qdrant.

Root crontab: empty.

## Ports Listening

22 (SSH), 80/81/443 (NPM), 3306 (MySQL localhost), 6333-6334 (Qdrant), 8080 (Noeticus), 8082 (colony static), 8384 (Syncthing GUI localhost), 22000 (Syncthing data)

## Disk Usage (notable)

- /home/bitnami/docker-sites/ -- 5.3GB total (colony 2.8GB, tamza 949MB, dnaresonance 580MB, lt 501MB, bhaktitemple 480MB). WordPress files, containers NOT running.
- /home/bitnami/noeticus/ -- 521MB (kb, scripts, qdrant_storage, venv)
- /home/bitnami/qdrant_storage_sol.tar -- 689MB. Qdrant backup from Sol migration. Can be deleted if migration verified.
- /home/bitnami/wordpress_transfers/ -- 246MB. Migration artifacts.

## Stale / Cleanup Candidates

- qdrant_storage_sol.tar (689MB) -- Sol migration artifact
- wordpress_transfers/ (246MB) -- migration artifacts
- docker-sites/ WordPress files (5.3GB) -- containers not running, sites may be deprecated
- Unused Docker images: duplicati (2 versions), mysql:8.0, old wordpress images -- ~2.5GB reclaimable
- NPM admin password is default (changeme)

## Backup Status

- Only bhaktitemple has automated backup (daily restic to Lakarian)
- humancolony.org static files have NO backup
- Noeticus data has NO backup on DAX (Qdrant vectors could be re-ingested from KB)

## Actions Taken This Session (2026-04-13)

1. Fixed humancolony.org: recreated colony-static-nginx with correct mount (/home/bitnami/colony_static/ instead of /home/bitnami/static-sites/colony/)
2. Restored NPM proxy host for humancolony.org with SSL (Let's Encrypt)
3. Added "Memex Memories" Syncthing folder on Lakarian side (pending DAX acceptance)
