# Memex Migration Handover (Sol -> DAX)
# Author: Opus 4.6, Claude Code on Pine, 2026-04-13
# Context: Chat filled up mid-migration. This is the baton for the next Opus chat.

# !!! READ FIRST: 20260413_memex_flows_design_v02_addendum_tomemex.md
# The flows design doc was written without reading the Sol scripts and got
# several critical details wrong (Flow 4 walks 3 roots not 1, path-based
# key prefix breaks on DAX, prod pusher file is sync_memories.py not _v3,
# 10 Sol-LOCAL files were not Nextcloud-synced). Addendum corrects these.
# Sol scripts retrieved to C:\claude_base\sol_scripts_retrieved\ on 2026-04-13.
# Mounting Sol drive requires admin UAC each time: see retrieved README.

## TL;DR
Sol is dead. Memex (the Cloudflare semantic memory) is healthy, but the cron scripts that fed it died with Sol. Migration is ~40% done. Flow 1 (Syncthing ingest) and safety (watchdog + restic backup) are live. Flows 2/4/5 still need to be extracted from the Sol drive (now plugged into Pine as /mnt/sol via WSL) and redeployed on DAX.

## What is live now (2026-04-13)
- humancolony.org: back up with SSL (was broken, fixed this session)
- Pine collector (Flow 3): running, added to Windows startup via `C:\cloud_base\scripts\start_mdindex_sync.vbs`. Registry expanded to include cloud_base and claude_base. Script: `C:\cloud_base\scripts\mdindex_sync.py` (v04).
- Syncthing (Flow 1 transport): Lakarian sendonly -> DAX receiveonly. 516 files of `00_clawy_kb/memories/` synced to `/home/bitnami/memex_memories/` on DAX.
- Restic backup of canonical KB on Lakarian: daily 3 AM, 30 daily + 12 monthly retention. Repo `/home/mrempadmin/backups/clawy_kb_restic`, password `clawy2026`. First snapshot: 521 files / 62 MB.
- Watchdog (circuit breaker): `memex_watchdog_v02.py` deployed at `/home/bitnami/` on DAX. Cron every 5 min. WARN at 200 MB / 1500 files (Telegram only). KILL at 300 MB / 3000 files (disables all `memex` crons except watchdog itself, sends Telegram). Reversible with `python3 memex_watchdog_v02.py --restore`.
- Source repos committed: claude_base and cloud_base on github.com/maxrempel.

## What is still dead
- Flow 4 (Pusher): `sync_memories.py` -- walks memories/ and POSTs to Memex Worker. THE critical piece. Not yet on DAX.
- Flow 2 (Notion downloader): `S310v01_notion_to_memex.py`. Not yet on DAX.
- Flow 5 (Reclaim): `reclaim_memex.py` -- pulls MCP-written entries back into `memories/reclaim_sync_from_memex/`. Not yet on DAX.

## Sol drive status
Plugged into Pine. WSL sees it: `/mnt/sol` and `/mnt/sol2` both mount. Scripts to retrieve:
- `/mnt/sol/home/maxre/.openclaw/skills/memex-memory/scripts/sync_memories.py`  (Flow 4)
- `/mnt/sol/home/maxre/.openclaw/skills/memex-memory/scripts/reclaim_memex.py`  (Flow 5)
- `/mnt/sol/home/maxre/00HA1py/scripts/S310v01_notion_to_memex.py`  (Flow 2)

Ubuntu root may be on /mnt/sol2 rather than /mnt/sol -- check both. If empty, `wsl --shutdown` then retry, or confirm drive letter in Windows Disk Management.

## Open design decision (unresolved)
Flows 2 and 5 need to WRITE into the `memories/` tree, but on DAX that tree is Syncthing receive-only. Three options from the design doc:
- A: run Flows 2+5 on Pine. Output lands in Nextcloud, flows back down.
- B: give DAX separate ingest folders (`notion_ingest/`, `reclaim_ingest/`) outside the Syncthing root; modify pusher to walk multiple roots.
- C: make Syncthing send-receive. Risky.
Recommendation in design doc: A for reclaim (light), B for Notion (heavy, closer to Worker).
Decide before deploying Flows 2 and 5.

## Failure modes to watch
1. Duplicate Memex entries (pusher re-pushing same file under different path)
2. False deletions (pusher deletes Memex entries because a sync glitch hid files)
3. Receive-only conflict (Flows 2/5 try to write into receiveonly folder)
4. KB data loss (wider clawy folder -- mitigated by restic)
5. KB contamination (junk re-flowing back upstream)
6. Amplification (reclaim writes file, pusher re-pushes it, MCP writes again... mitigated by separate `reclaim_sync_from_memex/` subfolder -- do NOT flatten this)

## Key paths / creds (do not re-discover)
- Memex Worker: https://claude-memory.max-rempel2.workers.dev  auth header `X-Auth-Key: claymem2026`
- D1 query token: `Hp0RcvNVzktIZj64vVgW7gWyseZ3wguEXfdM2cwR`
- Notion token: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\`
- Telegram: bot `8123222971:AAHaFDwaND04quJ0xiBixElwCDa2fLwLn_4`, chat `1395850773`
- DAX ingest folder: `/home/bitnami/memex_memories/` (user bitnami)
- Canonical folder: Lakarian `/home/yunohost.app/nextcloud/data/mremp/files/00_clawy_kb/memories/` = Pine `C:\Users\maxre\Nextcloud\00_clawy_kb\memories\`

## Reference docs written this session
- `C:\claude_base\work_logs\20260413_memex_flows_design_tomemex.md` -- full 5-flow design, folder layout, API reference
- `C:\claude_base\work_logs\20260413_dax_full_audit_tomemex.md` -- DAX audit (containers, cron, ports)
- `C:\claude_base\memex_watchdog_v02.py` -- deployed watchdog source
- `C:\cloud_base\scripts\mdindex_sync.py` -- Pine collector (v04)

## Next actionable step
Extract the three Sol scripts via WSL, copy into `C:\claude_base\sol_scripts_retrieved\`, READ them (don't rewrite blindly -- these were troubleshooted on Sol), then deploy Flow 4 (pusher) to DAX first. Test on a few files before enabling full cron.
