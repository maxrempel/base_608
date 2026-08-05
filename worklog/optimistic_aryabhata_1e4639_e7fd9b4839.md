
## [2026-06-27 15:52] E16 2954c44e
- DID: Confirmed cwd-key fix is clean: verified shipped wake_listener.py has NO os.execv re-exec (only revert comments); responded to C41's URGENT wake-call - I never touched exit/re-exec logic, fix is orthogonal key-resolution only.
- STATE: cwd-key fix DONE: shipped master e301ac3, deployed to Centauri, 9/9 tests pass both machines. Re-exec branch confirmed dead/untouched. cwd-key item CLOSEABLE per board.
- NEXT: g4 owns remaining surface: Q2 restart-respawn test (grep wake_listener_debug.log for src=resume after Max's next natural relaunch). Cent live listeners re-arm fresh on next turn.
- LESSON: C41 measured: claude --resume CLI heartbeat is a dead end (spawns parallel headless process keyed to cwd, never delivers a turn to an open tab, risks 2-procs-1-transcript corruption). os.execv re-exec also dead on Windows (detaches, loses wake-grid slot). Only real wake path = hook exit-2/asyncRewake from a listener the session spawned via its own SessionStart/UserPromptSubmit lifecycle.
