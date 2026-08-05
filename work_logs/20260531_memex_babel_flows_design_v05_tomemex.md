# Memex + Babel flows design v05 (current, verified)
# Author: Claude Opus 4.8, Pine, Claude Code, 2026-05-31 (evening)
# Supersedes: v04 (20260531_memex_babel_flows_design_v04_tomemex.md), same day.
# WHY v05: v04 claimed "the whole pipeline runs on SOL" and "the DAX migration
# was never adopted; DAX is not in this pipeline." BOTH WRONG. In reality TWO
# pushers (Sol AND DAX) were both writing to the one Memex worker, which is what
# doubled every entry. This doc records the corrected, verified single-writer
# state after the 2026-05-31 evening cleanup. Read v01-v04 for history only.

## TL;DR of the 2026-05-31 evening fix

- Root cause of the long-standing "everything shows up twice" problem: TWO
  pushers writing to the same Memex worker -- Sol's cron AND DAX's cron. Same
  code, same canonical tree, so each file got written once by each = uniform 2x.
- Decision (Max): DAX (AWS Lightsail, stabler than the residential-IP home
  server) becomes the SINGLE primary writer. Sol's Memex crons turned off.
- Cleaned up: dropped DAX's stale second source ("luminous_ingest"), moved the
  unique content out of it first, added the replace-by-tag dedup fix to DAX,
  then wiped DAX's push-state and reingested fresh so every file collapsed to
  exactly one entry.
- Verified after: Memex = 1539 entries, 0 duplicate tags (was 2813 with ~1274
  redundant copies). All 5 books at full chapter counts, 13 DNA papers present,
  YouTube transcripts gone from Memex (they live in Babel).

## The two databases (unchanged from v04)

- MEMEX = Max's OWN material (books, notes, Notion, worklogs, todos, papers).
  Worker https://claude-memory.max-rempel2.workers.dev ; D1 claude-memory-db ;
  auth X-Auth-Key: claymem2026 ; /write truncates text > 8000 chars.
  Endpoints: /search /write /read/<id> /list (POST) /delete/<id> (DELETE) /changes /mcp.
- BABEL = OTHERS' YouTube transcripts ("listening trail").
  Worker https://babel.max-rempel2.workers.dev ; D1 babel-db ; auth babelmem2026 ;
  source tag clawy-yt-transcript. Fed by the Lak transcript service
  (yt.dnaresonance.com / yt_transcript_app.py). Split out so YT transcripts stop
  burying Max's own writing in Memex search.

## WHO WRITES TO MEMEX NOW (the important correction)

PRIMARY PUSHER = DAX (AWS Lightsail, bitnami@35.80.203.42, UTC clock).
  Script:  /home/bitnami/memex_scripts/sync_memories.py
  Cron:    */5  (plus reclaim 2-57/5, notion S310 */10, watchdog */5)
  State:   /home/bitnami/memex_scripts/state/sync_state.json (+ sync.log)
  Walks TWO roots now (luminous_ingest DROPPED 2026-05-31):
    /home/bitnami/memex_memories/   (Syncthing receive-only from Lak canonical)
    /home/bitnami/notion_to_dax/    (Stream 2 Notion output, DAX-local)
  Skips subfolders: reclaim_sync_from_memex, archive.
  Has the replace-by-tag DEDUP fix (deletes EVERY existing entry carrying a
  file's exact tag before writing -- kills state-loss orphans and any second
  writer's copy). Backup of pre-cleanup script:
    sync_memories.py.preDAXprimary_20260531.bak
  Pre-reingest state backup: state/sync_state.json.preReingest_20260531.bak

SOL (home server, maxre@192.168.1.113) -- Memex crons DISABLED 2026-05-31.
  crontab lines for sync_memories.py, reclaim_memex.py, S310 notion are
  commented "# DISABLED 20260531 DAX-primary:". Sol still has the scripts and
  the newer dedup patch, so it's a warm standby -- but DO NOT re-enable its
  Memex crons while DAX runs, or doubling returns.
  Sol KEEPS one cron: S201v03_notion_clawy_task_sync.py (*/15) -- the todo-list
  round-trip between Notion and todo.md. That is a Sol-only function, unrelated
  to the Memex pusher, and must keep running.

## Streams feeding the canonical tree (00_clawy_kb/memories/)

Canonical tree = /home/maxre/Nextcloud/00_clawy_kb/memories/ on the Nextcloud
account (synced Lak <-> Pine <-> Sol; Lak -> DAX via Syncthing into
memex_memories/). This is the ONE source of truth. Everything searchable in
Memex should live here.

- Stream 1 Manual: hand-placed .md anywhere under memories/.
- Stream 2 Notion->Memex: S310v01_notion_to_memex.py writes from_notion/ .md;
  runs on DAX (*/10) into notion_to_dax/, and the pusher ingests them.
- Stream 3 Pine collector: C:\claude_base\scripts\mdindex_sync.py scans for
  *_tomemex.md and copies into from_tomemex/. Unchanged.
- Stream 4 Pusher: now DAX only (see above).
- Stream 5 Reclaim: reclaim_memex.py (DAX, 2-57/5) pulls direct-MCP writes
  (source not clawy-nextcloud-sync) to disk insurance at
  reclaim_sync_from_memex/. Pusher skips that subfolder, so no loop.

## What "luminous_ingest" was, and why it was dropped

DAX had a SECOND source root /home/bitnami/luminous_ingest/ (Syncthing-fed from
Pine's zSyncMain\z_luminous_fixed\ingest\). It bypassed the canonical tree and
re-injected ~96 files: the 4 OLD truncated whole-book entries (already replaced
by the per-chapter split), ~60 YouTube transcripts (now in Babel), old Feb-2026
Kazarian movie drafts, and -- the one thing of real value -- 13 of Max's DNA /
consciousness science papers (.md) that lived nowhere else in the KB.

Cleanup done 2026-05-31:
- Copied the 13 DNA papers into the canonical tree at
  00_clawy_kb/memories/maxs_publications/DNA_resonance/ so they stay searchable
  under the single clean feed. (The 5 "bad_convert" backup copies were skipped;
  PDF originals are preserved under published_public_keep\ and on Google Drive.)
- Dropped the luminous_ingest root from DAX's MEMORIES_DIRS.
- The reconcile pass then deleted the ~91 stale luminous-keyed entries from
  Memex automatically.
- Old Feb Kazarian drafts intentionally let go from Memex search (the movie now
  lives in C:\moma; the 4 current ones were already in the canonical tree).

## Wipe-and-reingest done this session (how the 2x was cleared)

Max's standing rule: nextcloud-sync dups are wipe-and-reingest by design; don't
pick off rows one by one. Executed the spirit of that safely WITHOUT a search
blackout:
1. Backed up the 2 direct-MCP entries' full text (cloudflare_sites_overview,
   Liz/Siegen handover) to C:\claude_base\memex_backups\, and saved an id/tag
   manifest of all 2813 pre-clean entries.
2. Backed up + cleared DAX's sync_state.json (so the pusher re-pushes every
   file instead of skipping on unchanged hash).
3. Ran the patched DAX pusher once. With empty state + the replace-by-tag dedup,
   each file: fetch its tag's existing ids (the two old copies, incl Sol's
   orphan) -> delete them all -> write ONE fresh. The 2 direct entries have
   different tags so were never touched.
Result verified: 1539 total, 0 duplicate tags.

## What is NOT changing

- Both Workers / D1 / Vectorize / R2 on Cloudflare: healthy.
- Babel pipeline (Lak transcript service): unchanged.
- Pine collector (Stream 3), reclaim disk-insurance, Notion sync: unchanged.
- Sol's S201 todo-sync cron: keeps running.

## Guardrails / do-not-trip

- Do NOT re-enable Sol's sync_memories / reclaim_memex / S310 crons while DAX
  is primary. Two writers = doubling again.
- If DAX is ever rebuilt or the home server must take over, enable ONE machine's
  Memex crons, never both. Whichever takes over should clear its state and
  reingest once so the dedup collapses anything stale.
- The replace-by-tag dedup now on DAX is the permanent prevention of future
  duplicates from state loss.
