# Memex System Status Report -- Post-Migration
# Author: Opus 4.6, Claude Code on Pine, 2026-04-14
# Supersedes: 20260413_memex_deploy_checklist_tomemex.md (historical)

## Executive summary

The Memex feed infrastructure has been migrated from the dead Sol box to
the always-on DAX Lightsail instance. D1 was wiped and reloaded from a
clean source. Three crons feed Memex; a watchdog guards it. The system
is running stable as of 2026-04-14 afternoon.

## Current system

### Memex core (unchanged by migration)
- Cloudflare Worker: claude-memory.max-rempel2.workers.dev
- D1 database: memories table (text + tags + source + timestamps)
- Vectorize index: 768-dim, bge-base-en-v1.5 embeddings
- R2 bucket: nightly backup
- Auth key: claymem2026 (header X-Auth-Key)

### Feed streams (all run on DAX)

1. Pusher -- `/home/bitnami/memex_scripts/sync_memories.py`, cron */5 min.
   Walks three roots and POSTs changed .md files to Memex:
   - /home/bitnami/memex_memories/   (Nextcloud KB, via Syncthing from Lakarian)
   - /home/bitnami/luminous_ingest/  (Luminous, via Syncthing)
   - /home/bitnami/notion_to_dax/    (Notion downloader output, local)
   State: sync_state.json (hash + memex_id per file key).
   Skip subtrees: reclaim_sync_from_memex, archive.
   Key prefix is explicit per-tuple; no path-string heuristic.

2. Notion downloader -- `S310v01_notion_to_memex.py`, cron */10 min.
   Pulls Notion pages into /home/bitnami/notion_to_dax/ as notion_<id>.md.
   Runs in venv. 222 pages tracked.

3. Reclaim -- `reclaim_memex.py`, cron 2-57/5 min.
   Pulls Memex entries whose source is NOT clawy-nextcloud-sync into
   /home/bitnami/reclaim_to_dax/, which Syncthing propagates back to
   Nextcloud as disk-insurance. The `reclaim_sync_from_memex` subfolder
   is explicitly skipped by the pusher (see "loop prevention" below).

4. Watchdog -- `memex_watchdog_v02.py`, cron every 5 min.
   WARN at 200 MB / 1500 rows (Telegram). KILL at 300 MB / 3000 rows
   (disables crons). Thresholds to review after first full week.

### Transport (Syncthing, unchanged GUI config by Max)
- Lakarian -> DAX: memex_memories/ receive-only on DAX.
- Lakarian -> DAX: luminous_ingest/ receive-only on DAX (one-shot rsync
  used for initial backfill; GUI folder to finalize).
- DAX -> Lakarian: notion_to_dax/ send-only, reclaim_to_dax/ send-only.

### Backups / rollback
- D1 dump: `C:\claude_base\memex_backups\memex_full_dump_20260413_2310.json`
  (1324 rows, 5.8 MB). Captured pre-wipe.
- Restore script: `scripts/memex_d1_restore_from_dump_v01.py`.
- Old Notion files archived from Nextcloud (duplicate risk, see below):
  `memex_backups/old_notion_from_nextcloud_memories_20260414/` (202 files).
- Lakarian restic snapshot: daily 3 AM, 30d / 12m retention.

### Git restore point (the version to roll scripts back to)

If the Memex sync pipeline goes wrong and needs restoring to a known-good
state, check out this commit of the `claude_base` repo:

    Repo:    https://github.com/maxrempel/claude_base
    Branch:  master
    Commit:  028d5738a0890bc94ba8957ea1c8c1724e2cf330
    Short:   028d573
    Date:    2026-04-14 10:38:42 -0700
    Title:   Add post-migration system status report

This is the first commit after the migration was fully engaged and
observed to be stable (pusher, Notion cron, reclaim all running; D1
wipe+reload complete; 202-file notion duplicate risk resolved; Memex
search verified sane).

Restore procedure:

    cd C:\claude_base
    git fetch origin
    git checkout 028d573 -- scripts/ sol_scripts_retrieved/

Then redeploy the three scripts to DAX at `/home/bitnami/memex_scripts/`:
- sync_memories.py  (from sol_scripts_retrieved/sync_memories_patched_v01.py)
- S310v01_notion_to_memex.py
- reclaim_memex.py

If D1 content also needs restoring (not just scripts), use the Apr 13
pre-wipe dump plus `scripts/memex_d1_restore_from_dump_v01.py --execute`.
That replays 1324 rows with new ids but preserved text/tags/source.

Previous commit points (for reference):
- `ebb16c4` -- wipe/restore scripts added; pusher patch committed.
- `9d63b58` -- deploy prep: patched pusher, D1 backup, DAX staging.
- Earlier commits predate the migration and are not valid restore points.

## Troubles met on the way (and lessons)

### 1. Dead Sol drive, non-persistent WSL mount
Sol's NVMe was plugged physically via USB, but WSL ext4 mounts do not
persist. Every `wsl --shutdown` and every reboot requires a re-mount
with admin UAC. The prior handover said "mounted" without clarifying
this. Lesson: handover docs must state whether state is persistent or
ephemeral.

### 2. Handover misread the pusher
The original flows design doc was written before the Sol scripts were
retrieved. It claimed pusher walked one root with a nc_/ws_ prefix
guessed from the path. Reality: three roots, and the "nc_" guess keyed
off the substring "Nextcloud" being in the path -- which would fail on
DAX (`/home/bitnami/...`) and re-push every file as a new entry. Lesson:
read the actual code before designing migrations.

### 3. reclaim_state.json was corrupt
Sol crashed uncleanly 2026-04-11; reclaim_state.json contained x86
binary garbage. Unrecoverable. Accepted as one of the reasons to do a
clean wipe-and-reload rather than state-preserve.

### 4. PEP 668 on Debian bitnami
`pip install notion-client` refused on system Python. Fixed by creating
`/home/bitnami/memex_scripts/venv/`. Notion cron runs via that venv.

### 5. Cron wipe
An awk expression in the migration helper accidentally truncated
bitnami's crontab. Restored from /tmp/crontab.before_migration.bak.
Lesson: always snapshot crontab before editing; prefer `crontab -l > bak`
then edit-and-install pattern over in-place awk.

### 6. Notion duplicate risk (caught and fixed this session)
Pre-migration, the Nextcloud KB contained 202 `notion_*.md` files copied
from Sol-era direct sync. Post-migration, the Notion cron on DAX writes
fresh copies of the same pages into `notion_to_dax/`. Both roots are
walked by the pusher. Same filename under different roots maps to the
SAME state key (`nc_notion_<id>.md`) -- second write wins, but either
tree changing silently would toggle the entry. Fixed by archiving the
202 old files out of Nextcloud (`memex_backups/old_notion_from_nextcloud_memories_20260414/`).
Syncthing will propagate the deletion to DAX's memex_memories/; the
pusher will delete those Memex entries on the next cycle; notion_to_dax/
becomes the sole canonical source.

## No amplification. No overlap. No duplication.

This is the single most important operational property of the system.
Every stream must have ONE canonical source per entry. If two streams
can produce the same entry, we get either:

- **Amplification**: a file flips state back and forth and the pusher
  re-POSTs on every tick, burning Worker CPU and doubling Vectorize
  inserts. Watchdog catches mass runaway, but a slow drip is invisible.
- **Duplication**: two Memex entries for the same text. Search returns
  both. Over time, recall gets noisier and the D1 row count inflates
  past what the watchdog expects.
- **Loops**: reclaim writes files that the pusher picks up and re-sends,
  which reclaim pulls down again. Unbounded growth within hours.

Concrete rules now enforced:

1. **Reclaim output is pusher-skipped.** `reclaim_sync_from_memex/` is
   in SKIP_SUBTREES. Reclaim files exist on disk ONLY as insurance;
   the pusher must never walk them. Break this and you get an unbounded
   loop within the first hour.

2. **notion_to_dax/ is the only notion source.** The 202 pre-migration
   notion files in Nextcloud have been archived. Any manual notion
   file additions to the KB memories root will recreate the duplicate
   hazard -- don't put notion_*.md there.

3. **reclaim_to_dax/ is not in the pusher walk list.** It is a send-only
   destination for reclaim output. Adding it to MEMORIES_DIRS would
   re-push every MCP-direct-write back to Memex as a "clawy-nextcloud-sync"
   entry, which reclaim would then pick up again because the source tag
   is wrong. Same loop shape as above.

4. **Explicit per-root source tags.** `MEMORIES_DIRS` is a list of
   (path, prefix, source_tag) tuples. No heuristic inference. If you
   add a new feed root, you set its tag deliberately; the watchdog and
   reclaim SQL depend on these tags.

5. **archive/ is also pusher-skipped.** Placeholder; extend as archive
   folders are inventoried. Never let the pusher walk an archive.

## Open items

- Luminous Syncthing folder is not yet finalized in the GUI (used a
  manual rsync for the first load). Max to add the folder in Syncthing
  web UI when convenient.
- Syncthing propagation of the 202 notion archive deletion has not yet
  reached DAX as of writing; next few pusher ticks will show a large
  "deleted" count in sync.log. That is expected.
- Watchdog thresholds (200/300 MB, 1500/3000 rows) should be reviewed
  after one week of stable data.
- Embedded git worktree at `claude_base/.claude/worktrees/pedantic-golick`
  is untracked; clean up after merge.

## File index

Canonical scripts:
- DAX:   `/home/bitnami/memex_scripts/sync_memories.py`
- DAX:   `/home/bitnami/memex_scripts/S310v01_notion_to_memex.py`
- DAX:   `/home/bitnami/memex_scripts/reclaim_memex.py`
- DAX:   `/home/bitnami/memex_watchdog_v02.py`
- Repo:  `C:\claude_base\sol_scripts_retrieved\sync_memories_patched_v01.py`
- Repo:  `C:\claude_base\scripts\memex_d1_backup_dump_v01.py`
- Repo:  `C:\claude_base\scripts\memex_wipe_via_worker_v01.py`
- Repo:  `C:\claude_base\scripts\memex_d1_restore_from_dump_v01.py`
- Repo:  `C:\claude_base\scripts\memex_reclaim_oneshot_push_v01.py`

Backups:
- `C:\claude_base\memex_backups\memex_full_dump_20260413_2310.json`
- `C:\claude_base\memex_backups\old_notion_from_nextcloud_memories_20260414\`

Design / history:
- `20260413_memex_flows_design_v03_final_tomemex.md` (design)
- `20260413_memex_deploy_checklist_tomemex.md` (historical, pre-engage state)
- THIS FILE (current system state)
