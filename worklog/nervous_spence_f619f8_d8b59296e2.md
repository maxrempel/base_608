
## [2026-06-22 10:40] C26 36bd0e2c
- DID: C26 built+deployed the global task log (tasklog) on Pine+Cent; Max: 'Amazing'
- STATE: COMPLETE: tasklog.py (set/find/list/who) indexes bcast state + work-logs, no new watcher/DS4. Live Pine (83 sessions) + Centauri (2); enforcement nudge hook wired+validated both. Pushed 03e7a16e
- NEXT: Idle, standing by. No timer armed. This session also shipped: comms routing+challenge, rooms feature, branch-emoji
- LESSON: Run worklog/bcast/tasklog with NO cd (full path) - cd resolves git-toplevel to the shared main checkout and misattributes the entry

## [2026-06-22 14:03] C26 36bd0e2c
- DID: Investigated the Pine<->Cent Mike-DC comms failure Max flagged; probed fleetcomm (round-tripped fine) and found root cause
- STATE: FIXED: fleetcomm had no per-turn auto-surface UserPromptSubmit hook like bcast, so cross-machine posts were invisible until manually read. Cent/m05 built fleetcomm_hook.py (pushed 5280296) + wired Cent; I wired it on PINE too (settings.json validated+backed up). Tested hook fires; cross-machine wake to m05 sent. Told both teams
- NEXT: Residual: running sessions must restart/​reload to load the new hook (new sessions auto-get it). DURABILITY GAP to flag Max: settings.json isn't synced, so every machine hand-wires hooks - a unified installer would prevent recurrence
- LESSON: Cross-machine comms needs the SAME auto-surface-every-turn hook that same-machine bcast has; without it, posts sit invisible and teams 'can't reach' each other even though the channel works

## [2026-06-26 09:25] C26 36bd0e2c
- DID: Checked if the hook-wiring durability gap was already fixed (it wasn't - wire_hooks.py only did wake_listener); built the unified installer per Max
- STATE: DONE+pushed 9d7d9f2d: tools/fleet_hooks/wire_all_hooks.py wires the COMPLETE standard hook set (wake_listener, noflash, bcast, fleetcomm, worklog, tasklog, session_status, user_verbatim, ctx_gauge, block_death_spiral) idempotent+BOM-tolerant+self-healing-dedup. Pine 11/11 clean. Centauri was MISSING 9/11 - wired them; hit+fixed a no-matcher-group duplicate bug, healed Cent to 1 clean group of 8 UPS hooks
- NEXT: Durability gap closed: one command hardens any machine. Note: Cent had NO survival hooks (worklog/ctx_gauge/user_verbatim) and NO death-spiral guard until now
- LESSON: settings.json hook drift is the root class behind cross-machine failures; a single idempotent+self-healing installer (matcher absent==empty) prevents it. Cent's UPS group had no matcher key - match by normalized matcher
