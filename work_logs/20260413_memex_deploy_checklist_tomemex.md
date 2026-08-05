# Memex Migration -- Deploy Checklist (paused state)
# Author: Opus 4.6, Pine, Claude Code, 2026-04-13
# Status: All safe prep done. Stopped before live cron + Memex wipe.
# These steps require Max present (or an explicit go-ahead).

## What is already done (safe, reversible)

1. Sol scripts retrieved and inspected.
   C:\claude_base\sol_scripts_retrieved\ contains originals + state files.

2. Patched pusher written.
   C:\claude_base\sol_scripts_retrieved\sync_memories_patched_v01.py
   - explicit per-root nc_/ws_ prefix
   - skip subtrees: reclaim_sync_from_memex, archive

3. D1 backup dump captured.
   C:\claude_base\memex_backups\memex_full_dump_20260413_2310.json
   1324 rows, 5.8 MB. Schema + every row preserved. Rollback insurance.

4. One-shot reclaim catch-up push script written.
   C:\claude_base\scripts\memex_reclaim_oneshot_push_v01.py
   Dry-run by default; --execute flag to actually POST. Reads from
   C:\Users\maxre\Nextcloud\00_clawy_kb\memories\reclaim_sync_from_memex.

5. 10 Sol-local workspace files staged in Nextcloud.
   C:\Users\maxre\Nextcloud\00_clawy_kb\memories\workspace_from_sol\
   Will sync to Lakarian via Nextcloud, then to DAX via existing Syncthing.

6. DAX SSH access verified.
   Key: C:\Users\maxre\Nextcloud\zSyncMain\ssh\dax_lightsail_max_id_rsa.pem
   Host: bitnami@35.80.203.42

7. DAX scripts staged at /home/bitnami/memex_scripts/.
   sync_memories.py        (patched, walks 4 roots, paths fixed)
   reclaim_memex.py        (paths fixed for DAX)
   S310v01_notion_to_memex.py (paths fixed for DAX, runs in venv)
   notion_token.txt        (mode 600)
   venv/                   (Python venv with notion-client installed)
   state/                  (empty, ready)
   *.bak files preserved alongside each patched script.
   All 3 scripts pass python3 ast.parse syntax check.

8. DAX folders created (still empty):
   /home/bitnami/luminous_ingest/   (awaits Syncthing)
   /home/bitnami/notion_to_dax/     (awaits Notion script first run)
   /home/bitnami/reclaim_to_dax/    (awaits reclaim script first run)

9. Design doc updated to v03 with all decisions.
   C:\claude_base\work_logs\20260413_memex_flows_design_v03_final_tomemex.md

## What is NOT done -- requires Max approval / manual action

### A. Syncthing folders (manual via GUI)

Three new folders need to be added to Syncthing:

  Folder ID: luminous_ingest
    Pine path:     C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed\ingest\
    Lakarian path: /home/yunohost.app/nextcloud/data/mremp/files/zSyncMain/z_luminous_fixed/ingest/
    DAX path:      /home/bitnami/luminous_ingest/
    Direction:     Pine/Lakarian send -> DAX receive-only

  Folder ID: notion_to_dax
    DAX path:      /home/bitnami/notion_to_dax/
    Lakarian path: /home/yunohost.app/nextcloud/data/mremp/files/00_clawy_kb/memories_upstream/notion/
    (Pine receives via Nextcloud sync from Lakarian)
    Direction:     DAX send-only -> Lakarian receive

  Folder ID: reclaim_to_dax
    DAX path:      /home/bitnami/reclaim_to_dax/
    Lakarian path: /home/yunohost.app/nextcloud/data/mremp/files/00_clawy_kb/memories/reclaim_sync_from_memex/
    Direction:     DAX send-only -> Lakarian receive
    (lands in the existing reclaim folder so Pine sees it via Nextcloud)

### B. WIPE Memex (destructive, MUST confirm with Max)

Backup already captured. After Max's go-ahead:
  - Truncate D1 memories table.
  - Clear Vectorize index (768-dim).
  Done via wrangler or D1 API.

### C. One-shot reclaim catch-up push

After wipe, BEFORE enabling pusher cron:
  python C:\claude_base\scripts\memex_reclaim_oneshot_push_v01.py --execute
Pushes ~97 reclaim files to Memex with source=clawy-nextcloud-sync.
Verify count via Memex search before continuing.

### D. Enable DAX crons (only after A+B+C verified)

Add to bitnami crontab:
  */10 * * * * /home/bitnami/memex_scripts/venv/bin/python /home/bitnami/memex_scripts/S310v01_notion_to_memex.py
  */5 * * * *  /usr/bin/python3 /home/bitnami/memex_scripts/sync_memories.py
  2-57/5 * * * * /usr/bin/python3 /home/bitnami/memex_scripts/reclaim_memex.py

(watchdog cron already live; do not duplicate.)

### E. Monitor first hour

Watch /home/bitnami/memex_scripts/state/sync.log + notion_sync.log + reclaim.log.
Confirm pusher counts settle to "0 synced, 0 deleted".
Sample-test 3-5 Memex search queries.

## If things go wrong: rollback

A restore script will need to be written that re-POSTs every row from
memex_full_dump_20260413_2310.json back to the Worker. New IDs will
differ but content is preserved.

## Open questions for Max

- Confirm Syncthing folder IDs/paths above match your existing scheme.
- Confirm wipe is the right call vs preserve sync_state.json (we chose
  wipe for the 1324->~700 entry cleanup it brings).
- Watchdog thresholds: 200 MB WARN / 300 MB KILL. Review after first
  full pusher run on DAX.

## Sol drive

Still mounted at /mnt/sol via WSL on Pine (per Max's request to keep it).
Will need re-mount after any wsl --shutdown or reboot. Procedure in
C:\claude_base\sol_scripts_retrieved\README_tomemex.md.
