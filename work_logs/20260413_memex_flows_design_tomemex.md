# Memex Flows Design Document
# Author: Opus 4.6, Pine, Claude Code, 2026-04-13
# Purpose: Document all data flows into and out of Memex for migration from Sol to DAX

## What is Memex

Semantic memory for Claude across all platforms (desktop, phone, browser). Stores text with vector embeddings. Searchable via MCP tools (memex_search, memex_read, memex_write). Used daily.

## Architecture

- Cloudflare Worker: claude-memory (MCP + REST API)
- Cloudflare D1: claude-memory-db (text storage)
- Cloudflare Vectorize: claude-memory (768 dim, cosine, bge-base-en-v1.5)
- Cloudflare R2: memex-files (backup)
- Worker URL: https://claude-memory.max-rempel2.workers.dev
- Auth: X-Auth-Key: claymem2026
- Cloudflare Plan: Workers Paid ($5/mo)

All of the above is on Cloudflare and healthy. What died with Sol is the cron scripts that fed data in and reclaimed data out.

## Canonical Source of Truth

The folder: /home/maxre/Nextcloud/00_clawy_kb/memories/ (on Sol/Nextcloud).
Windows path: C:\Users\maxre\Nextcloud\00_clawy_kb\memories\
Lakarian path: /home/yunohost.app/nextcloud/data/mremp/files/00_clawy_kb/memories/

If Memex is wiped, it can be fully rebuilt by re-ingesting this folder. Memex is an index, not a source.

## Folder Structure

    00_clawy_kb/
      memories/                          THE INGEST FOLDER
        [root level, 232 files]
          notion_*.md (202 files)        Flow 2 output (Notion downloader)
          local_*.md (19 files)          Flow 3 output (Pine collector)
          hand-placed .md (~11 files)    Flow 1 (manual)
        kazarian_assembly/               Flow 1 (hand-placed audio scripts, raw scenes)
        proj_knowledge/                  Flow 1 (hand-placed Notion zip exports, 157 files)
        reclaim_sync_from_memex/         Flow 5 output (96 files reclaimed from Claude MCP writes)
        worklogs/                        Flow 1 (hand-placed chat logs)
      notion/                            Unused/empty tree
      temp/                              4 misc files

## Flow 1 -- Manual Files

What: .md files placed by hand into memories/ or its subfolders.
Who: Max or Clawy.
Where: Directly into the folder tree on any Nextcloud-connected machine.
Examples: finance-biotron.md, archive.md, proj_knowledge/ zip exports, kazarian_assembly/ scripts.
No automation needed. Files appear in Nextcloud, sync to Lakarian, get pushed to Memex by Flow 4.

## Flow 2 -- Notion Downloader

What: Pulls pages from the Claude Documents Notion tree, saves as notion_<page_id>.md.
Excludes: Archive pages (to keep junk out of Memex).
Script: S310v01_notion_to_memex.py (was on Sol at /home/maxre/00HA1py/scripts/).
Schedule: Every 10 min on Sol cron.
Output: 202 notion_*.md files into memories/ root.
Status: DEAD (Sol is down). Needs to move to DAX.
Dependency: Notion internal integration token (stored in Nextcloud/zSyncMain/ssh/).

## Flow 3 -- Pine Collector

What: Scans registered folders on Pine for *_tomemex.md files, copies them into memories/ with local_ prefix.
Script: C:\cloud_base\scripts\mdindex_sync.py (v04).
Config: C:\cloud_base\scripts\folder_registry.txt (roots: Nextcloud, moma, cloud_base, claude_base).
Schedule: Persistent process, runs every 10 min. Starts on Windows boot via VBS in Startup folder.
Output: 19 local_*.md files into memories/ root. Also builds C:\cloud_base\mdindex.md as index.
Status: RUNNING (fixed 2026-04-13, was stopped since Apr 10).
Also handles cleanup: if a _tomemex.md file is deleted from source, removes matching local_* from memories/.

## Flow 4 -- Pusher (memories folder to Memex Worker)

What: Walks memories/ recursively, reads each .md file, POSTs new/changed ones to Memex Worker /write endpoint. Deletes Memex entries for removed files.
Script: sync_memories.py v3 (was on Sol at /home/maxre/.openclaw/skills/memex-memory/scripts/).
State tracking: sync_state.json (maps filename to SHA256 hash + memex_id).
Schedule: Every 5 min on Sol cron.
API: POST https://claude-memory.max-rempel2.workers.dev/write, header X-Auth-Key: claymem2026, body {text, tags, source}.
Status: DEAD (Sol is down). Needs to move to DAX. This is the most critical piece.

## Flow 5 -- Reclaim (Claude MCP writes back to folder)

What: Queries Memex D1 for entries written directly by Claude (via phone/browser MCP), saves them as .md files into memories/reclaim_sync_from_memex/.
Why: If Memex is wiped, direct MCP writes would be lost unless they exist in the canonical folder. Reclaim ensures every Memex entry has a file-system copy.
Script: reclaim_memex.py (was on Sol at /home/maxre/.openclaw/skills/memex-memory/scripts/).
State tracking: reclaim_state.json (tracks reclaimed IDs).
Output folder: memories/reclaim_sync_from_memex/ -- SEPARATE from other flows to prevent amplification (pusher would re-push reclaimed files, creating duplicates).
D1 query token: Hp0RcvNVzktIZj64vVgW7gWyseZ3wguEXfdM2cwR
Schedule: Every 5 min offset 2 min on Sol cron.
Status: DEAD (Sol is down). Needs to move to DAX.

## Cleanup Flow

To remove junk from Memex: delete the file from the memories/ folder. Next pusher run (Flow 4) detects the deletion and removes the corresponding Memex entry. This is why sync_memories.py tracks file-to-memex-id mapping in sync_state.json.

## Migration Plan (Sol to DAX)

What needs to happen:
1. Syncthing shares memories/ folder from Lakarian to DAX (receive-only on DAX, deletions propagate downstream, never upstream to Nextcloud). Lakarian side DONE (2026-04-13). DAX side needs to accept.
2. Deploy sync_memories.py (Flow 4) on DAX. Script exists on Sol NVMe drive (extractable via WSL on Pine). Cron every 5-15 min.
3. Deploy S310v01_notion_to_memex.py (Flow 2) on DAX. Needs Notion token. Cron every 10 min. Output goes to memories/ which Syncthing sends back... WAIT -- this is a problem. DAX receives memories/ as receive-only. Notion downloader output needs to go INTO memories/. Options: (a) run Notion downloader on Pine instead, output lands in Nextcloud directly, or (b) make a separate notion_sync/ folder on DAX that the pusher also walks.
4. Deploy reclaim_memex.py (Flow 5) on DAX. Same folder problem -- reclaim output needs to land in reclaim_sync_from_memex/ which is inside the receive-only Syncthing folder. Options: (a) run reclaim on Pine, or (b) reclaim writes to a separate DAX-local folder that pusher also walks.
5. Pine collector (Flow 3) already running.

## Open Design Decision

Flows 2 and 5 write INTO the memories/ folder. If DAX receives memories/ as receive-only via Syncthing, those scripts cannot write there. Three options:

Option A: Run Flows 2 and 5 on Pine (or any Nextcloud machine). Output lands in Nextcloud, syncs to Lakarian, Syncthing sends to DAX. Clean but adds load to Pine.

Option B: On DAX, have separate ingest folders (e.g. notion_ingest/, reclaim_ingest/) outside the Syncthing folder. Modify the pusher to walk multiple roots.

Option C: Make the Syncthing folder send-receive (not receive-only) so DAX can write back. Risky -- could create sync conflicts.

Recommendation: Option A for reclaim (it is lightweight, runs every 5 min, tiny files). Option B for Notion downloader (heavier, 202 files, better to run close to the Memex Worker on DAX).

## Credentials Reference

- Memex Worker REST auth: X-Auth-Key: claymem2026
- D1 query token: Hp0RcvNVzktIZj64vVgW7gWyseZ3wguEXfdM2cwR
- Notion internal integration token: stored in Nextcloud/zSyncMain/ssh/
- Worker deploy token: cloudflare_vectorize_token_20260304.txt (value: 0_HFJaVkI0VShTyuH9TRlsiSvEige2lwzqDbUfx9)
- All credential files: C:\Users\maxre\Nextcloud\zSyncMain\ssh\

## API Reference

POST /write - {text, tags, source} - stores with embedding
POST /search - {query, top_k} - semantic search
GET /read/:id - full entry by ID
DELETE /delete/:id - remove entry
/mcp - OAuth MCP endpoint for Claude connector
