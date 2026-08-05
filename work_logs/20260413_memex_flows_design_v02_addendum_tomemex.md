# Memex Flows Design — Addendum v02 (corrections from Sol script audit)
# Author: Opus 4.6, Pine, Claude Code, 2026-04-13
# Supersedes: selected sections of 20260413_memex_flows_design_tomemex.md
# Source of truth: actual Sol scripts at C:\claude_base\sol_scripts_retrieved\

## Why this addendum exists

The original flows design doc was written without reading the Sol scripts.
The handover pointed next chat at Sol scripts for a reason -- they contain
facts the design doc guessed wrong about. This addendum lists every
correction. The 5-flow model itself is still correct; paths and details
are not.

## Correction 1 -- Flow 4 (Pusher) walks THREE roots, not one

The original design said Flow 4 walks memories/ only. Actual script
(sync_memories.py, Apr 7 mtime, was the live cron) walks:

    /home/maxre/Nextcloud/zSyncMain/z_luminous_fixed/ingest/   (91 .md files)
    /home/maxre/Nextcloud/00_clawy_kb/memories/                (~500 .md files)
    /home/maxre/.openclaw/workspace/memory/                    (10 .md files, Sol-LOCAL)

Sync state file confirms: 574 total keys (564 nc_*, 10 ws_*).

Implications for migration:
- If Flow 4 moves to DAX and only sees Syncthing-received
  /home/bitnami/memex_memories/ (= 00_clawy_kb/memories/), it will fail to
  find the other ~101 entries in its state file and DELETE them from
  Memex on the first run. THIS IS A CATASTROPHIC DATA-LOSS RISK.
- The z_luminous_fixed/ingest/ tree is inside Nextcloud and is available
  on Pine and Lakarian. It just needs a second Syncthing folder to reach
  DAX, OR pusher runs on Pine.
- The .openclaw/workspace/memory/ tree was Sol-LOCAL (not Nextcloud-
  synced). Rescued to C:\claude_base\sol_scripts_retrieved\
  workspace_memory_local_only\ (10 files). Decision needed: relocate
  under Nextcloud (e.g. 00_clawy_kb/memories/workspace_from_sol/) so
  they are covered by normal pusher+Syncthing going forward.

## Correction 2 -- Pusher version

Original said "sync_memories.py v3". The file actually labeled
sync_memories_v3.py (Mar 20 mtime) is NOT the prod file. Prod is
sync_memories.py (Apr 7 mtime). The Apr 7 file's docstring says
"v3 fixes" so the v3 behavior is included, but deploy sync_memories.py,
not sync_memories_v3.py.

## Correction 3 -- Key naming / dedup is sensitive to path

sync_memories.py line 112:
    base_prefix = "nc_" if "Nextcloud" in mdir else "ws_"

Then key = base_prefix + subprefix + filename. This drives:
- sync_state.json key
- memex tags
- source field ("clawy-nextcloud-sync" vs "clawy-workspace-sync")

If DAX mounts the Syncthing folder at a path WITHOUT "Nextcloud" in it
(current: /home/bitnami/memex_memories/), every file gets "ws_" prefix
instead of "nc_", producing different keys from the Sol state file and:
- Every existing file gets re-pushed as a new Memex entry (duplicates
  all 564 nc_* entries).
- Original nc_* entries never get updated, and eventually get deleted
  on the next run because they are not in current_files.

Fix options (pick one before deploying pusher to DAX):
a) Patch sync_memories.py to use explicit per-root prefixes instead of
   path-string matching. Cleanest.
b) Mount/symlink the Syncthing folder at a path containing "Nextcloud",
   e.g. /home/bitnami/Nextcloud/00_clawy_kb/memories/.
c) Run pusher on Pine where the canonical Nextcloud path is native.

## Correction 4 -- Flow 5 (Reclaim) source filter

Reclaim SQL filter excludes BOTH clawy-nextcloud-sync AND
clawy-workspace-sync. Design doc only mentioned the former. Fine -- both
match what pusher writes. Just document it.

D1 IDs in reclaim_memex.py (hardcoded):
- CF_ACCOUNT = e4dc2224d6baa721873dca77dc6f057d
- D1_ID = ced548a2-e647-4547-9ae3-7606b08b6e16
- Token = Hp0RcvNVzktIZj64vVgW7gWyseZ3wguEXfdM2cwR

## Correction 5 -- Flow 2 (Notion) path resolution

Handover said script at /home/maxre/00HA1py/scripts/S310v01_notion_to_memex.py.
Actual: that path is a SYMLINK -> /home/maxre/Nextcloud/sol_00HA1_scripts/.
Single physical copy under Nextcloud. Cron invoked the symlink target.
When deploying to DAX, deploy the Nextcloud-side physical file and update
cron to its real deploy path on DAX.

Dependencies: python3 notion_client package. Token at
/home/maxre/Nextcloud/zSyncMain/ssh/notion_internal_token_20260319.txt
(same path on Pine; different on DAX -- needs copying).

## Correction 6 -- Flow 2 schedule

Design doc: "every 10 min". Actual cron: `*/10 * * * *`. Matches.
Log shows runs taking 120-140s with 220 Notion pages, 0 new/updated in
steady state. Safe to keep 10-min cadence on DAX.

## Correction 7 -- Flow 5 schedule

Design doc: "Every 5 min offset 2 min". Actual cron: `2-57/5 * * * *`
(every 5 min starting at minute 2). Matches.

## Open design decision -- REVISED recommendation

Original open question: where to run Flows 2 and 5 given receive-only
Syncthing on DAX.

Given Correction 1, Flow 4 itself has the same problem: it needs read
access to three roots. Real options now:

A) Everything on Pine. Pine has Nextcloud (covers 2 of 3 roots); the
   workspace_memory root moves into Nextcloud. Flow 2 writes Notion-sourced
   files into Nextcloud. Flow 5 writes reclaims into Nextcloud. Flow 4
   pushes from Nextcloud to Memex Worker. Everything flows down to
   Lakarian and DAX by Syncthing for backup, not for function.
   Pro: Memex is fed while Pine is online; no DAX infra needed for this.
   Con: If Pine is off, flows stall. DAX becomes unused for Memex.

B) Pusher on DAX, Flows 2 and 5 on DAX, Syncthing sends all three roots
   (add 2 Syncthing folders for z_luminous_fixed/ingest and a relocated
   workspace memory). Patch sync_memories.py to stop using "Nextcloud"
   string for prefix discrimination.
   Pro: DAX is always-on, independent of Pine uptime.
   Con: More Syncthing config, needs the sync_memories.py patch.

Recommendation pending Max decision. B is more robust long-term. A is
faster to deploy today and resurrects Memex feeding sooner.

## Things still correct in original design doc

- 5-flow model
- Memex Worker URL, auth key
- Cleanup flow (delete file -> next pusher run deletes from Memex)
- Amplification concern with reclaim_sync_from_memex/ separate subfolder
- Recommendation not to flatten reclaim folder

## Files rescued from Sol (2026-04-13)

C:\claude_base\sol_scripts_retrieved\
    sync_memories.py            -- Flow 4 prod (deploy this one)
    sync_memories_v3.py         -- older branch, reference only
    reclaim_memex.py            -- Flow 5 prod
    S310v01_notion_to_memex.py  -- Flow 2 prod
    state\sync_state.json            -- 574 keys, preserves Memex IDs
    state\reclaim_state.json
    state\sync_state_notion.json
    workspace_memory_local_only\     -- 10 Sol-local .md files to relocate

## Next step (unchanged from handover, but now informed)

Decide A vs B with Max. Either way, preserve sync_state.json when
deploying pusher so existing Memex entries are not duplicated or
deleted.
