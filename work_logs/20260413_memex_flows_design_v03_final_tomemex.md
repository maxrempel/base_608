# SUPERSEDED 2026-05-31 by 20260531_memex_babel_flows_design_v04_tomemex.md
# The DAX migration below was NOT adopted -- the live pipeline runs on SOL.
# Read v04 for the current system. This file is history only.
#
# Memex Flows Design v03 -- Final (post-audit, post-dialogue)
# Author: Opus 4.6, Pine, Claude Code, 2026-04-13
# Supersedes: v01 (20260413_memex_flows_design_tomemex.md)
#             v02 addendum (20260413_memex_flows_design_v02_addendum_tomemex.md)
# This is the design to execute. Read v01 + v02 only for history.

## Decision summary (all approved by Max in dialogue)

- B: everything runs on DAX (Pine is laptop, goes down).
- Patch pusher prefix logic: hard-code nc_/ws_ per root, stop using "Nextcloud"-in-path trick.
- Luminous ingest STAYS at zSyncMain/z_luminous_fixed/ingest/ on Nextcloud
  (do NOT move -- Luminous system likely has active writers; risk of
  breaking Luminous outweighs cleanliness benefit). Instead, give it its
  own Syncthing folder Pine/Lakarian -> DAX. Revises original B2 plan
  while keeping the same end state on DAX. Decision made by Opus during
  doit22 implementation 2026-04-13 after discovering Luminous folder
  layout on Pine.
- Move 10 Sol-local workspace files into 00_clawy_kb/memories/workspace_from_sol/.
- Each DAX-writing stream gets its own Syncthing folder, own direction. Not one pipe.
- Pusher SKIPS the reclaim folder (disk-backup insurance only).
- On migration day: wipe Memex, one-shot catch-up push of reclaim folder, then pusher takes over with empty state. D1 backup dump kept locally as rollback.

## Streams (5)

Stream 1 -- Manual files.
  Hand-placed .md files into 00_clawy_kb/memories/ tree.
  No automation.

Stream 2 -- Notion to DAX.
  Script: S310v01_notion_to_memex.py (Sol-rescued, retarget paths).
  Runs on DAX, cron every 10 min.
  Writes notion_*.md into DAX-local /home/bitnami/notion_to_dax/.
  Syncthing: DAX send-only -> Lakarian/Nextcloud receive (so Pine sees Notion
  pages too).
  Pusher also walks this folder.
  Needs notion_client pip package and Notion token copied to DAX.

Stream 3 -- Pine collector.
  Script: C:\cloud_base\scripts\mdindex_sync.py v04 (already live).
  Pine-resident, scans *_tomemex.md, writes local_*.md into
  00_clawy_kb/memories/ via Nextcloud. Unchanged by migration.

Stream 4 -- Pusher (files to Memex).
  Script: sync_memories.py (Sol-rescued, Apr 7 version, NOT the _v3 file).
  Runs on DAX, cron every 5 min.
  Walks FOUR local DAX folders:
    /home/bitnami/memex_memories/         (Syncthing-received canonical tree)
    /home/bitnami/luminous_ingest/        (Syncthing-received Luminous tree)
    /home/bitnami/notion_to_dax/          (Stream 2 output)
    /home/bitnami/reclaim_to_dax/         (Stream 5 output)
  SKIPS:
    - reclaim_sync_from_memex/ subtree (prevents duplicating direct-MCP writes;
      reclaim files are disk-only insurance).
    - any archive/ subtree(s) within memex_memories (archives are not for Memex).
      Exact paths TBD -- inventory required before first run (see open items).
  Patches needed:
    - Replace path-based nc_/ws_ prefix detection with explicit per-root mapping.
    - Add skip rules for reclaim_sync_from_memex/ and archive subtree(s).
  POSTs to https://claude-memory.max-rempel2.workers.dev/write
  with X-Auth-Key: claymem2026.

Stream 5 -- Reclaim (Memex direct-MCP writes back to disk).
  Script: reclaim_memex.py (Sol-rescued).
  Runs on DAX, cron `2-57/5 * * * *` (every 5 min starting min 2).
  Queries D1 for entries where source NOT IN
  ('clawy-nextcloud-sync','clawy-workspace-sync').
  Writes reclaim_<slug>_<shortid>.md into DAX-local
  /home/bitnami/reclaim_to_dax/.
  Syncthing: DAX send-only -> Lakarian/Nextcloud receive (so a file copy
  lands in the canonical tree at 00_clawy_kb/memories/reclaim_sync_from_memex/
  for disk-backup insurance).
  Pusher does NOT re-push these (skip rule above).
  State file may start empty; on first run it reclaims everything and
  populates reclaim_state.json.

## Folder layout on DAX

    /home/bitnami/
      memex_memories/           (Syncthing receive-only from Lakarian)
        [all of 00_clawy_kb/memories/ mirrored here]
        reclaim_sync_from_memex/   (pusher skips this subtree)
        workspace_from_sol/        (the 10 rescued files, now in-Nextcloud)
        luminous_ingest/           (the 91 Luminous files, folded in)
      notion_to_dax/            (Syncthing send-only to Lakarian)
      reclaim_to_dax/           (Syncthing send-only to Lakarian)

## Syncthing folders (3)

1. memex_memories
   Lakarian send-only -> DAX receive-only.
   Direction: canonical -> DAX.

2. notion_to_dax
   DAX send-only -> Lakarian receive.
   Direction: DAX -> canonical. Lakarian path under
   00_clawy_kb/memories_upstream/notion/ (or similar -- keeps Notion output
   out of the main pusher-walked tree on DAX, but visible on Pine for search).

3. reclaim_to_dax
   DAX send-only -> Lakarian receive.
   Direction: DAX -> canonical. Lakarian path under
   00_clawy_kb/memories/reclaim_sync_from_memex/ (the existing path -- pusher
   skips this subtree so there is no loop).

## Deploy order (migration day)

0. All code patches committed to claude_base repo, reviewed.
1. Take Memex D1 backup dump:
   C:\claude_base\memex_backups\memex_full_dump_YYYYMMDD_HHMM.json
   (text + source + tags + id for every row in memories table)
2. On Nextcloud (Pine or Lakarian):
   - Move Luminous ingest tree into 00_clawy_kb/memories/luminous_ingest/
   - Move the 10 Sol-local files into 00_clawy_kb/memories/workspace_from_sol/
3. Wait for Syncthing to propagate to DAX (verify file counts).
4. On DAX: add the two new Syncthing folders (notion_to_dax, reclaim_to_dax).
5. Install notion_client on DAX. Copy Notion token file to DAX.
6. Copy patched pusher, reclaim, and S310 scripts to DAX. Install cron entries.
   Do NOT enable cron yet.
7. Wipe Memex: DELETE every row from D1 memories table + Vectorize index.
8. One-shot catch-up push: run a script that POSTs every file in the
   reclaim_sync_from_memex/ folder to Memex as a normal entry (source =
   clawy-nextcloud-sync so reclaim does not re-reclaim). Verify count.
9. Enable Stream 2 cron (Notion) -- populates notion_to_dax/.
10. Enable Stream 4 cron (pusher) -- walks all three roots, pushes fresh.
11. Enable Stream 5 cron (reclaim) -- starts clean.
12. Monitor for 1 hour:
    - pusher log: sync/delete counts should settle to 0 after first full run.
    - Memex search returns sane results for 3-5 known queries.
    - Watchdog does not fire.

If anything goes sideways: re-POST every entry from the D1 backup dump to
restore Memex.

## Rollback procedure

Script: restore_from_dump.py (to be written).
Input: memex_full_dump_YYYYMMDD_HHMM.json.
For each row: POST /write with same text/tags/source. New IDs will differ
(cosmetic -- semantic content restored).

## Open items still not covered

- Exact layout of D1 backup dump script (trivial, write during deploy).
- One-shot catch-up push script (trivial).
- Watchdog thresholds: current 200 MB WARN / 300 MB KILL. Review after first
  full run to confirm sane.
- Cron user on DAX: bitnami. Confirm Python3 path and file perms.
- Archive folder inventory: Notion archive pages are already excluded at
  source by S310v01 (4 known archive page IDs). But the Nextcloud tree may
  contain hand-placed archive folders (historical zips, old exports) that
  should not reach Memex. Before first pusher run, inventory subfolders of
  00_clawy_kb/memories/, identify archive-type folders (names or
  README-tagged), and add their relative paths to the pusher skip list.

## What is NOT changing

- Memex Worker, D1, Vectorize, R2: all Cloudflare, healthy, unchanged.
- Pine collector (Stream 3): unchanged.
- Restic backup of canonical KB on Lakarian: unchanged.
- Watchdog on DAX: already deployed (memex_watchdog_v02.py), unchanged.
- Syncthing Lakarian->DAX send of memex_memories: already live.

## Files in use

Source scripts (from C:\claude_base\sol_scripts_retrieved\):
- sync_memories.py        -> needs prefix patch + reclaim-skip patch
- reclaim_memex.py        -> deploy as-is
- S310v01_notion_to_memex.py -> update output path to notion_to_dax/

State to preserve:
- (none, wipe-and-reload design)

State to discard:
- sync_state.json (Sol-rescued) -- keep as reference only, not deployed.
- reclaim_state.json (corrupt from Sol crash) -- discard.
- sync_state_notion.json -- keep, deploy to DAX so Notion sync resumes
  incrementally instead of re-fetching all 220 pages.
