# SUPERSEDED 2026-05-31 (evening) by 20260531_memex_babel_flows_design_v05_tomemex.md
# WRONG IN THIS DOC: it says "the whole pipeline runs on SOL" and "the DAX
# migration was never adopted; DAX is not in this pipeline." Both false -- DAX
# was a SECOND active pusher, and that two-writer setup is what doubled every
# entry. v05 records the corrected single-writer (DAX-primary) state. History only.
#
# Memex + Babel flows design v04 (current state)
# Author: Claude Opus 4.8, Pine, Claude Code, 2026-05-31
# Supersedes: v03 final (20260413_memex_flows_design_v03_final_tomemex.md)
# v03 described a DAX-based plan that was NOT fully realized. Reality:
# the whole pipeline runs on SOL (home server, 192.168.1.113, user maxre).
# Read v01/v02/v03 for history only. THIS doc is the live system.

## Big picture (what changed since v03)

Two separate semantic-search databases now exist, by deliberate split
(2026-05-31):

- MEMEX  = Max's OWN material (books, notes, Notion, worklogs, todos).
- BABEL  = OTHERS' YouTube transcripts (the "listening trail").

Why the split: YT transcripts were burying Max's own content in Memex
search. Each YT listen dumped a long transcript; over time they out-massed
his books. So the YT trail was moved to its own DB (Babel) and purged from
Memex. Now a Memex search surfaces Max's own writing; Babel is queried
separately when he wants "what did that video say".

Both are Cloudflare Workers (Worker + D1 + Vectorize 768-dim bge-base-en +
R2), same code shape, each with its own MCP connector on Max's Claude
account, both queryable from the phone.

## MEMEX -- Max's own knowledge base

Worker:   https://claude-memory.max-rempel2.workers.dev
D1:       claude-memory-db
Auth:     X-Auth-Key: claymem2026
Write cap: /write truncates text > 8000 chars (this is why whole-book
           entries were broken -- see Books below).
Endpoints: /search /write /read/<id> /list /delete/<id> (DELETE method)
           /changes /authorize /mcp

Canonical source tree (the ONE folder the pusher watches):
  /home/maxre/Nextcloud/00_clawy_kb/memories/   (on Sol; Nextcloud-synced,
  so the same tree is visible on Pine at C:\Users\maxre\Nextcloud\00_clawy_kb\
  memories\, pinned always-local).

### Cron jobs on Sol (all user maxre)

Stream 4 -- PUSHER (the heart).
  /home/maxre/.openclaw/skills/memex-memory/scripts/sync_memories.py
  cron */5. Walks ONE root (memories/, prefix nc_, source
  clawy-nextcloud-sync). Hash-incremental: only changed files re-push.
  Each file keyed prefix + subpath_ + filename; unique Memex tag
  "clawy-sync,{key-without-.md}". Deletes Memex entries whose source file
  vanished (reconcile pass). SKIPS subfolders: reclaim_sync_from_memex
  (disk-insurance only) and archive.
  State: .../memex-memory/state/sync_state.json ; log: .../state/sync.log.
  DEDUP FIX (2026-05-31): before writing a file it now deletes EVERY
  existing Memex entry carrying that file's exact tag (replace-by-tag),
  not just the one id in state. This kills state-loss orphan duplicates on
  re-push. Backup of pre-fix script: .prededup_20260531_134711.bak.

Stream 5 -- RECLAIM (direct-MCP writes -> disk insurance).
  .../memex-memory/scripts/reclaim_memex.py  cron 2-59/5.
  Pulls D1 rows whose source is NOT clawy-nextcloud-sync / clawy-workspace-sync
  (i.e. things Claude wrote straight to Memex via MCP) and saves a .md copy
  into 00_clawy_kb/memories/reclaim_sync_from_memex/ so they survive on disk.
  Pusher skips that subfolder, so no loop.

Stream 2 -- NOTION -> Memex.
  /home/maxre/00HA1py/scripts/S310v01_notion_to_memex.py  cron */10.
  Pulls Notion pages, writes .md into 00_clawy_kb/memories/from_notion/.
  Pusher then ingests them (tag nc_from_notion_...). Notion stays the
  source-of-truth for full docs; Memex is the semantic index.

Extra -- Notion task sync.
  /home/maxre/00HA1py/scripts/S201v03_notion_clawy_task_sync.py  cron */15.
  Round-trips Max's todo list between Notion and todo.md.

Stream 3 -- PINE collector (off-Sol).
  Pine: C:\claude_base\scripts\mdindex_sync.py. Scans registered folders for
  *_tomemex.md, copies them into 00_clawy_kb/memories/from_tomemex/ via
  Nextcloud. That is how instruction/method docs become Memex-searchable.

Stream 1 -- Manual files. Hand-placed .md anywhere under memories/.

## BABEL -- others' YouTube transcripts

Worker:   https://babel.max-rempel2.workers.dev
D1:       babel-db
Auth:     X-Auth-Key: babelmem2026
Source tag: clawy-yt-transcript
Rows:     2054 (migrated from Memex 2026-05-31, then purged from Memex).

Fed by the YT transcript service on Lak (home server, yt.dnaresonance.com):
  yt_transcript_app.py. On every YouTube share from Max's phone it pulls the
  transcript (Whisper fallback if captions blocked), makes a DeepSeek summary,
  FishAudio TTS (Anna voice) -> Telegram audio, AND writes the transcript to
  Babel. Config vars renamed MEMEX_* -> BABEL_* on 2026-05-31 for clarity.

Design note (2026-05-31, confirmed by Max): the nextcloud-sync source is
"wipe-and-reingest by design" -- exact-duplicate rows are expected and NOT
to be retro-dedup'd. The fix for staleness is wipe + reingest, not per-row
deletion. FUTURE dups are prevented by the pusher's replace-by-tag fix above.

## BOOKS -- fixed 2026-05-31

Problem: Max's 5 books lived as single whole-book .md entries, so the /write
8000-char cap truncated each to its first ~8000 chars; only the opening of
each book was ever searchable, and Celestial Science was missing entirely.

Fix: each book was split into per-chapter .md files (564 total, every chapter
under 8000 chars) and placed under the live feed at
  00_clawy_kb/memories/maxs_publications/books/<slug>/
so the pusher ingests each chapter as its own Memex entry. The 4 old
truncated whole-book entries were deleted directly from Memex (orphans: their
source files no longer existed anywhere the pusher watches, so they would
never self-reconcile).
  bogi_o_nas (book2 ts6 GLAVNYJ, Russian) 38 | celestial_science 168 |
  from_the_galaxy (Book6) 91 | metaphysics_for_lightworkers 40 |
  welcome_to_earth 227.
Canonical split source: C:\claude_base\scripts\book_format_fix\staging_v01\.
NOTE: an earlier session staged the same split into
zSyncMain\z_luminous_fixed\ -- that "luminous" pipeline feeds NOTHING (0 rows
in CF Memex came from it). It was abandoned to avoid a branch. The Sol pusher
on 00_clawy_kb is the ONE live feed to the phone.

## What is NOT changing

- Both Workers / D1 / Vectorize / R2 on Cloudflare: healthy.
- Reclaim disk-insurance, Notion sync, Pine collector: unchanged.
- The DAX migration in v03 was never adopted; DAX is not in this pipeline.
