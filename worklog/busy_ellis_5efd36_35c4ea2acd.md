
## [2026-06-23 15:51] D32 d66d6c70
- DID: Built reel-worker death/hang watchdog (commit b77d6f9): heartbeat + crash-proof loop + stderr crashlogs + moma_worker_watch.py scheduled every 3min, alarms via Telegram @MMMMonitorMaxBot + on-screen attention flash. Diagnosed the 22:xx stall = worker hung silently (stderr was DEVNULL). New reel worker restarted w/ heartbeat live.
- STATE: Watchdog live + scheduled task 'moma_worker_watch' every 3min. Telegram+attention both verified by Max.
- NEXT: Optionally extend watchdog table to other workers (combo_worker, lipsync ds/bb). Back to L23 gesture reel iteration if Max wants.

## [2026-06-23 16:18] D32 d66d6c70
- DID: Shipped atomic job-claim (CAS) + orphan-recovery in wan26au worker (d210247) so two workers can't double-bill one reel; added effective_status->'stalled' badge in ReelMaker when reel worker heartbeat is stale. Crashlog capture (b77d6f9) instantly caught WHY 8779 was down: combo_gui crashed on startup makedirs over a transient Nextcloud VFS error - fixed + tolerant now (8e4220c). Restarted combo_gui (8779 up 200) + worker (heartbeat live).
- STATE: All committed+pushed to master. 8779 up, worker live w/ atomic claim+heartbeat, watchdog scheduled every 3min.
- NEXT: Tell Max to hard-refresh ReelMaker. Optionally extend watchdog+heartbeat to other workers.

## [2026-06-23 16:57] D32 d66d6c70
- DID: DONE: shipped full worker-resilience suite for moma (commits b77d6f9,d210247,8e4220c,dfb98a5,49ea7e9,12ffe73): death/hang watchdog every 3min w/ Telegram+screen alarm; heartbeats in all 5 workers; atomic job-claim+orphan-recovery (no double-bill); ReelMaker shows 'stalled' when worker down; moved image/clip/kling pids OFF Nextcloud (data/ VFS OSError22 root cause); combo_gui makedirs tolerant. All workers up+beating, 8779 up.
- STATE: Complete + pushed to master. Watchdog scheduled task 'moma_worker_watch' live. Nextcloud data/ folder still in VFS-limbo (only bookkeeping; outputs fine) - Max may restart Nextcloud client.
- NEXT: Optional: investigate why data/ specifically wedges; or move worker logs off Nextcloud too. Else idle.
