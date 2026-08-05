
## [2026-06-20 11:50] ? 6fddc353
- DID: fleetcomm cross-machine channel fully wired Pine<->Centauri. Centauri auto-loads same synced global rules (symlink to D:\Nextcloud\claude_md_synced) so fleetcomm pointer already present; CLI placed at canonical repo path on both machines; stray C:\fleetcomm removed; global2 unified to one path.
- STATE: LIVE + in use - Max's pasted Centauri session already posted to the board. Worker fleetcomm.max-rempel2.workers.dev, KV-backed durable.
- NEXT: Optional only: throttled auto-hear hook for true teams feel - ask Max first

## [2026-06-22 07:19] g4 6fddc353
- DID: Built noflash_watch: scanner + SessionStart hook on Pine+Centauri
- STATE: Pine task hourly (next 7:07), Centauri task hourly (next 7:17), scanner already caught CF Workers KV Backup on Pine (live flasher), Centauri 0 violations
- NEXT: Optional: fix CF Workers KV Backup .bat with the same hidden-VBS pattern
- LESSON: Centauri's git push/pull is broken (no GitHub HTTPS credentials cached); scp over SSH works as a workaround. File a separate housekeeping item to fix Centauri git auth.

## [2026-06-26 15:49] g4 6fddc353
- DID: Killed 7 E04 Mike-correspondence wakes on Centauri (g4 owns cross-machine comms). Then probed why Cent's asyncRewake-while-idle is broken.
- STATE: On Cent: 5 wake_listener processes actively heartbeating BUT running pre-deploy code (no _dbg instrumentation, likely no fleetcomm-wake polling). Plus 20 stale-lock zombies from 6/24-6/25 dead listeners. Smoking gun for m04's 'wakes arrive batched' report: the live in-RAM listeners on Cent pre-date the fleetcomm wake-poll feature, so they never poll fleetcomm. They only deliver wakes via the UserPromptSubmit auto-surface hook when session next takes a turn.
- NEXT: Hand findings to E16 (Pine owns wake_listener investigation). Propose durable fix: listener self-terminates when source mtime > its own start time (cycle old code automatically).

## [2026-06-26 18:56] g4 6fddc353
- DID: Shipped the source-mtime self-terminate guard on wake_listener.py + swept zombie listeners fleet-wide. Max ordered the fix - this is the 'wake-at-will trick' restored.
- STATE: Commit 7c60bc45 pushed to master. Cent has the new file (scp'd, git auth failed). Killed 5 stale Cent listeners (7824/6576/8960/20800/20172) + 32 stale Pine listeners (>1h old). All active sessions will re-arm with the new guarded code on their next prompt. Going forward: any wake_listener.py update auto-cycles stale in-RAM listeners within ~60s of the file settling.
- NEXT: Wait + verify: when sessions take their next prompts, new listeners spawn with guard code. Watch for debug log entries on Cent (wake_listener_debug.log) to confirm new code is running. Next: f4/team can also test fleetcomm wake to a Cent session that has re-armed.

## [2026-06-26 19:06] g4 6fddc353
- DID: Reverted wake_listener mtime-guard (7c60bc45->a3a2a7d1) after D59 caught it breaks wake-at-will on Windows (sys.exit(0) drops hook grid slot; os.execv on Windows detaches new process from parent wait semantics = same result). Posted revert to joint board, force-woke D59.
- STATE: Master pushed a3a2a7d1. Joint board notified D59/C40/E16. Worktree clean. Decel timer at 15m (ticked work). Listeners on fleet running 7c60bc45 code will see updated mtime on next git-pull and exit(0) - last suffering of the bug they fix, then re-arm on next prompt with reverted code.
- NEXT: Watch for D59/C40 acknowledgement. Listener forensics will keep arriving via diagnostic anchors. If Max wants OS-level periodic sweep scripted, scope that next.
- LESSON: On Windows fleet: neither sys.exit(0) nor os.execv preserves Claude Code hook wake-grid membership. Any in-place refresh of an async+asyncRewake hook is structurally impossible on Windows. Mitigate via OS-level zombie sweep instead.

## [2026-06-27 15:11] g4 6fddc353
- DID: Max: 'consult C40 on persistence of wakeability across restart/sleep. C40 stuck. wakeability must be persistent.' Did: (1) decel timer set 30 (was 15m, Max asked slow flexible ~30min) -> DELAY_SECONDS=1800. (2) Posted three concrete consult questions to C40 on joint board (Q1: does ScheduleWakeup persist across Claude Code app restart? Q2: does SessionStart fire automatically on tab restore or only on click? Q3: are listeners in parent's Job Object?). Offered to run tests in sacrificial worktree.
- STATE: Decel armed at 30m. Joint board posted, C40 force-woken. No code edits this turn. Revert a3a2a7d1 still standing.
- NEXT: Wait for C40 reply or for Max to greenlight me running Q1/Q2 tests myself. If C40 wants tests, run them and report back. Don't ship any code until Q1/Q2 answered - design would be blind otherwise.

## [2026-07-02 12:21] ? 6fddc353
- DID: Shipped auto-wake-on-post in bcast.py (commit 251c8d9e): posts now ping every live wakeable session on the board via _drop_signal, 2-min per-target throttle, 1-on-1 skips broadcast, fail-open. Verified live (8 peers woken on joint post). Replied to C12A identity-redesign consensus (+1 worktree=identity, keep session-id fallback). Flagged safety's mike-dc heartbeat fix as WRONG (Centauri must not ping per method doc line 166; real owner = Pine MikeDC-Fill task).
- STATE: auto-wake DONE+pushed. Investigating whether Pine MikeDC-Fill scheduled task exists/pings hc cd162bbb (heartbeat gap since Jun20).
- NEXT: Report MikeDC-Fill task state to g board; F4 owns the actual fill. Then idle - Max's explicit task (auto-wake) complete.

## [2026-07-03 10:31] ? 6fddc353
- DID: Pollution fix v2 shipped (bcast.py+watcher.py, commit 14a64083). Root cause: router auto-promoted plain single-team posts to joint on bare-token id matches (F1/F2/chrX/F_ROH). Fixed: _mentioned_ids requires @-prefix; cmd_post trusts --all/--joint as global verb (teams CAN post global questions); watcher move-orders+dup-nudges now go to offending team's OWN board not joint; RETENTION_DAYS 7->5 with watcher running cmd_rolloff each 10-min run (archives, not deletes). 6-case routing matrix passes. Verified cleanup live (joint 372->233 archived).
- STATE: DONE+pushed. Structural fix needs no LLM. DeepSeek semantic pass is DOWN (HTTP 402 Payment Required - billing). 12 phantom dup collisions detected (C12A's session-id-churn domain, not mine).
- NEXT: Flag DeepSeek 402 to Max. Otherwise complete; idle.
- LESSON: Joint 'pollution' was mostly a tooling false-positive (bare token id-match auto-promote), not willful; fix the matcher not the people.

## [2026-07-04 11:12] ? 6fddc353
- DID: Pollution GATE shipped (bcast.py commit dd30e3d5): --all/--joint posts with no cross-team @mention now pass a fast DeepSeek 'is this genuinely global?' check at POST TIME; single-team work (postmortems/status/handoffs) reroutes to team board before landing on joint. Fail-open (missing key/error/timeout/disable-flag -> allow). Plain posts + @cross-team skip the check. Verified: X5 postmortem->team board, 'master frozen'->joint, '@f4'->joint. Moved the already-leaked X5 postmortem off joint to x board.
- STATE: DONE+pushed+announced. Gate is the prevention-at-write layer atop the @-only matcher fix + trust-verb + 5-day archive + semantic watcher.
- NEXT: Complete. Idle.
- LESSON: Trusting an explicit --all/--joint verb is exploitable by self-certification ('genuinely global, trust me'); a cheap post-time content gate on ONLY the rare explicit-global posts closes it without taxing normal traffic.

## [2026-07-04 17:18] ? 6fddc353
- DID: As manager, briefed fresh session G22B to fix the wake-listener orphan-guard false-kill (the DEAD-LISTENER root cause: listener self-exits ORPHAN_EXIT0 when one transient claude.exe helper ends, mistaking helper churn for an app restart; proven from debug log). Wrote durable handover: tools/wake_listener/orphan_guard_falsekill_handover_20260704_v01_tomemex.md. Posted brief to board.
- STATE: G22B not yet registered (brand-new, needs its first turn to run whoami G22B + catchup). Brief is on the board + handover on disk; it will catch both on onboarding. My stale-sid fix cec1e5ce already shipped; G22B owns the deeper dead-listener fix; told it to coordinate with C12A.
- NEXT: Wait for G22B to register + report back on g board; answer its questions as manager.
