
## [2026-06-27 17:00] C42 b02b594e
- DID: Proved wakeup.py timer FIRES on restart but a zombie listener (detached child of dead app) consumes+deletes the due entry and cannot wake the restored tab -> wake lost. B9 survives restarts because its tab gets reloaded (fresh live listener delivers); an unclicked passive tab loses the wake to the zombie.
- STATE: Max on ~4h break; armed 15-min steady self-wake; tasked to fix zombie-eats-wake bug in wake_listener.py + test + consult peers.
- NEXT: Add orphan check: listener must not fire/consume a schedule entry if its parent Claude app pid is dead; leave overdue entry on disk so the reloaded tab fires it. Then re-run restart test.
- LESSON: A surviving detached hook listener from a prior app instance can race-win and consume a scheduled wake without delivering it; only a listener whose parent app is alive should fire/consume schedule entries.

## [2026-06-27 17:14] C42 b02b594e
- DID: Built+tested reliable zombie_sweep.py via arm-files after measuring that parent-chain orphan detection is UNSAFE (intermediate bash dies, chain dead-ends while app alive -> would kill live tabs). Listeners now drop arm-files recording captured app pid; sweep kills only provable orphans. Committed 033fd1a5.
- STATE: Orphan self-guard (e88b7f54) + reliable external sweep (033fd1a5) both shipped+pushed. Sweep is dry-run default, --apply opt-in, NOT yet wired as scheduled task (pending Max review - kill tool, asymmetric risk). 20+ old-code zombies have no arm-file so are left alone; they die naturally on restart.
- NEXT: On Max return: live restart-test of orphan guard (preserve wake on disk vs eaten). Decide whether to wire zombie_sweep as periodic task. Re-arm 15min loop meanwhile.
- LESSON: Process-parent-chain walking is unreliable for orphan detection on Windows: intermediate wrappers die and break the chain even when the real ancestor app is alive. Capture identity (pid+create_time) at spawn while the chain is intact, persist it, and check THAT later.

## [2026-06-27 17:18] C42 b02b594e
- DID: Post-compaction wake: verified shipped work intact (e88b7f54 guard, 033fd1a5 sweep). Documented zombie-eats-wake hazard+fix in C41's wakeable_grid method doc (pushed 6a65c137). Posted track-2-DONE + flagged that C41's proposed stream-json headless-worker track conflicts with Max's explicit no-headless rule.
- STATE: Wakeability hardening on the GRID path (ScheduleWakeup = the real mechanism, confirmed by C41 vs B9) is essentially complete on my side. On-demand force-wake now reliable across restart via orphan-guard. Waiting: Max return for live restart test + decision on wiring zombie_sweep as periodic task.
- NEXT: Each 15m wake: check board for C41 reply, respond to Max if back, re-arm 900s. Do NOT build headless worker; do NOT auto-wire kill-sweep; do NOT restart while Max away.
- LESSON: Don't accept a manager track assignment that violates a standing Max directive - flag the conflict instead of silently building the rejected thing.

## [2026-07-02 08:10] ? b02b594e
- DID: Shipped bcast+watcher dedup fix (commit 1bc5cffc): phantom 'two live <id>' alarm killed by keying identity to physical tab (worktree cwd) not churned session_id
- STATE: pushed to master, verified 0 phantom dups live
- NEXT: keep auditing bcast/wake system for bugs+improvements per Max
