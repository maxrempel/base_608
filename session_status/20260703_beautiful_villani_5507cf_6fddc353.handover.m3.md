# Scribe handover - milestone 3 (~244K tokens)
# session: 20260703_beautiful_villani_5507cf_6fddc353
# cwd: C:\claude_base\.claude\worktrees\beautiful-villani-5507cf
# written: 2026-07-03 17:49:00 by deepseek-v4-pro

# HANDOVER - g4 (beautiful-villani-5507cf, Pine)

## GOAL (Max's words, final task)

> "Just fix it. I know what needs to be done and fix it in the most elegant way. The teams should be able to post on global when it is a global question."

The **Pollution Watcher** - stop X/XG1 teams (and anyone else) from polluting the global/joint board with team-specific chatter, clean up old junk automatically, and make the watcher actually enforce (not just whisper "your call" and get ignored). But teams must still be able to genuinely address all teams when needed.

---

## DECISIONS + WHY

### 1. Root cause of joint-board pollution (NOT defiance)
Max asked "why would teams ignore the local board?" Session x1 diagnosed the actual cause, and g4 reproduced it live: **bcast's router auto-promoted plain team posts to global whenever the message contained any bare token matching a live ID from another team.** Genomics text like `F_ROH`, `F1`, `F2`, `chrX` matched team-f/X ids ? router forced the post to global. The nag then told teams to "move" a post they never chose to send to global and cannot move (append-only). An impossible, misattributed request ? rationally ignored. That's the whole mystery - the tool was the polluter, not the teams.

### 2. Fix the matcher, not the people
The prior fix (last turn's `--joint` reroute for no-cross-team-posts) blocked genuine global questions, violating Max's explicit requirement. The elegant fix is at the **addressing level**: require `@`-prefix to treat a token as addressing another team. Bare `F1` never promotes; only `@f4` does. Plain `post` = your own team board. `--all`/`--joint` = trusted explicit global. Cross-team `@mention` = auto-promote (the original intent). This is structural, needs no LLM, and can't accidentally punish innocents.

### 3. Five-day archive cleanup
Max: "five days cleanup of the boards... the script should just move it to archive." Retention changed from 7?5 days in `bcast.py` (`RETENTION_DAYS = 5`). The watcher now calls `cmd_rolloff()` every 10 min - entries are **moved (not deleted)** to `branch_bulletin/archive/bulletin_<team>.archive.jsonl`, cursor-adjusted, recoverable via `bcast.py archive`. Verified live: joint went 372?233, all archived.

### 4. Stronger watcher message with WHY
Max wanted the message to explain: (a) it distracts other teams and blocks their communication, (b) it buries genuine cross-team messages. Implemented. Also: the watcher was itself a top polluter (it posted its suggestions TO joint). Now nudge posts go to the **offending team's own board** + force-wakes their live sessions. The watcher no longer writes to joint at all.

### 5. Source-mtime guard REVERTED (commit a3a2a7d1)
The guard added in 7c60bc45 (listener exits on code change) was caught by D59: on Windows, `sys.exit(0)` kills the listener, and a truly-idle session never re-arms (no hook fires). `os.execv` on Windows is CRT spawn-and-exit (same problem). So the guard was reverted. The honest answer: there's no in-place code refresh on Windows. Stale listeners are harmless (they keep serving wake), and a periodic OS-level sweep handles zombies.

### 6. Auto-wake-on-post SHIPPED (commit 251c8d9e)
Every board post now wakes every live wakeable session on that board, throttled to once per 2 minutes per target so post bursts don't re-wake. Joint posts fan out to all teams. 1-on-1 (exactly one @-mention) skips the broadcast. Fail-open: any error in auto-wake never breaks the post itself. This feature already proved itself - it woke g4 from a sibling's post this very session.

### 7. D02A uniqueness - no fix needed
Max asked if trailing letters (the A in D02A) count as a unique id. Direct test proved they already do: `_id_eq('D02','D02A') ? False`, case-insensitive match, distinct wake targets, distinct visual signatures. System was already correct.

### 8. Cross-machine wake cursor persist FIXED (commit 2685305b)
Before: listener baselined cursor to newest fleetcomm record at startup, silently skipping wakes posted while the target's listener wasn't armed (the F4 bug). After: cursor persisted per worktree (not per session_id - survives app restart), no age cap (wake fires whenever target next comes online, off-3-days included). One wake per listener cycle, queue drains in order.

---

## CURRENT STATE

### Done and shipped (all pushed to claude_base master)
- **Pollution fix v2 (14a64083):** @-only addressing, trust explicit global verb, RETENTION_DAYS=5, watcher posts to team boards + force-wakes, watcher self-clean (no longer pollutes joint)
- **Auto-wake-on-post (251c8d9e):** 2-min throttle per target, 1-on-1 skip, fail-open
- **Wake cursor persist (2685305b+2685305b):** durable per-worktree cursor, no age cap
- **Source-mtime guard REVERTED (a3a2a7d1):** cleanly backed out
- **7 E04 Mike-Correspondence wakes cancelled on Centauri** - f4 is sole Mike contact
- **37 zombie listeners swept** (32 Pine + 5 Cent) - active sessions re-arm on next prompt with fresh code
- **Mike-DC heartbeat gap diagnosed** - handed to F4 (its owner): doc contradiction, not an infra failure
- **5-day auto-cleanup wired** - runs every 10 min via the watcher

### In flight
- Nothing active. Pollution Watcher runs on its own schedule (every 10 min, bcast_watcher task). The bcast identity redesign (C12A's thread) has consensus but is owned by C12A, not g4.

### The 5-day cleanup
- Verified live: joint 372?233 entries, all archived to `branch_bulletin/archive/bulletin_joint.archive.jsonl`
- All board files (`bulletin_*.jsonl`) are now gitignored (g4 caught itself accidentally committing one and fixed it)

---

## EXACT NEXT STEP

**None - g4's tasks are complete.** The Pollution Watcher is self-running. If Max returns angry about joint-board clutter, the structural fix (matcher requiring `@`) prevents new pollution, and the 5-day cleanup removes old. The only open item is:

---

## OPEN QUESTIONS (awaiting Max)

1. **DeepSeek API is 402 Payment Required.** The *semantic* pass of the Pollution Watcher (AI content-check backstop) can't run. The structural fix (matcher + trust-verb) works without it, so nothing is broken - but the smart backstop is dark until DeepSeek billing is refilled. Max needs to top it up or decide to drop the AI pass entirely.

2. **FedEx sender-side ack-and-retry** - the one gap in cross-machine wake that hasn't been closed: receiver advances cursor on delivery, but if Claude eats the system-reminder (compaction mid-fire, etc.), the sender never knows. Proper fix = receiver posts `wake_ack` on actual session turn; sender re-knocks unacked wakes (1h cadence, Telegram escalation after 24h). Max acknowledged the idea but hasn't said "build it."

3. **Centauri's GitHub HTTPS credentials** - git pull fails non-interactively (no /dev/tty). Workaround (scp) used throughout this session. A spawned task exists for the permanent fix but hasn't been actioned.

---

## KEY PATHS / IDS / COMMANDS

### This session's identity
- **Session ID:** g4
- **Worktree:** `C:\claude_base\.claude\worktrees\beautiful-villani-5507cf`
- **Team board:** `branch_bulletin/bulletin_g.jsonl` (g team = cross-machine comms)

### Files edited this session
- `C:/claude_base/branch_bulletin/bcast.py` - matcher @-only, trust-verb routing, RETENTION_DAYS=5, auto-wake-on-post
- `C:/claude_base/branch_bulletin/watcher.py` - renamed Pollution Watcher, strong-rationale enforcement, posts to team boards, 5-day cleanup wired
- `C:/claude_base/tools/wake_listener/wake_listener.py` - cursor persist (committed 2685305b), mtime guard added then reverted (a3a2a7d1), current state = clean revert + diagnostic anchors only

### Important paths
- `C:/claude_base/branch_bulletin/archive/` - archived board entries (moved, not deleted)
- `C:/claude_base/branch_bulletin/wake/auto_wake_throttle/` - per-target throttle stamps for auto-wake
- `C:/claude_base/branch_bulletin/wake/fleet_cursors/` - persisted cursors keyed by worktree_safe_key
- `C:/claude_base/branch_bulletin/wake/locks_purged_g4_20260626_154954/` - backup of purged stale locks on Cent
- `C:/claude_base/branch_bulletin/wake/schedules/claude_base_15c30882f7.json` (Centauri) - cleaned of 7 E04 wakes, only E05 health-watch remains. Backup at `.bak_g4_20260626`

### Key IDs
- **D59, C40, C41, E16** - teammates actively working on wake-persistence / identity-redesign
- **C12A** - owns the bcast identity redesign thread (worktree=identity consensus reached, not yet deployed)
- **x1, X7A, X9A, X10A** - X/XG1 team sessions (live, notified about pollution)
- **f4** - owns Mike-DC calendar; sole Mike contact now (7 E04 wakes cancelled on Cent)

### Key commits (all on master, all pushed)
- `14a64083` - Pollution fix v2 (@-only addressing, 5-day cleanup, stronger watcher)
- `251c8d9e` - auto-wake-on-post (2-min throttle)
- `a3a2a7d1` - reverted mtime guard (D59 caught it broke wake-at-will on Windows)
- `2685305b` - wake cursor persist (FedEx-grade, no age cap)

### SSH to Centauri
```
ssh -i ~/.ssh/sol_key -o StrictHostKeyChecking=no maxre@192.168.1.176
```
(LAN IPv4 only, no /dev/tty ? git pull fails, use scp for file transfers)

### fleetcomm
```
python C:/claude_base/tools/fleetcomm/fleetcomm.py post "msg" --session <label>
python C:/claude_base/tools/fleetcomm/fleetcomm.py read
```
Worker: `https://fleetcomm.max-rempel2.workers.dev`, key: `fleetcomm_claymem2026`

### timer_decel
```
python C:/claude_base/tools/timer_decel/timer_decel.py set <N>   # set decel rung
python C:/claude_base/tools/timer_decel/timer_decel.py tick work|idle
```

---

## GOTCHAS / DEAD ENDS

1. **Windows `os.execv` does NOT preserve the PID.** It uses CRT spawn-and-exit - caller PID dies, Claude's hook engine sees exit, drops wake-grid slot. Same net result as `sys.exit(0)`. This is why in-place code refresh on Windows is structurally impossible for the wake-listener. **Do not re-attempt execv-based refresh.** The correct approach for zombie listeners is an OS-level periodic sweep (kill listeners >24h old ? next prompt re-arms fresh).

2. **DeepSeek 402 means the watcher's semantic pollution pass is dark.** The structural fix (matcher) works without it, but if you see pollution increasing, check DeepSeek billing first - the AI backstop can't run.

3. **`bulletin_*.jsonl` files are gitignored (2026-07-03).** They're live, per-machine, append-constantly files. Tracking them guarantees merge conflicts. **Do not `git add` them.** The archive files (`archive/bulletin_*.archive.jsonl`) are also untracked for the same reason.

4. **Centauri's git pull is broken** - no /dev/tty ? "could not read Username for github.com." If you deploy bcast.py or watcher.py changes to Centauri, use `scp -i ~/.ssh/sol_key <source> maxre@192.168.1.176:<dest>`. The spawned permanent-fix task is still open.

5. **The auto-wake throttle stamps are in `wake/auto_wake_throttle/<lowercased_id>.ts`.** If auto-wake seems to not fire, check that dir isn't full of stale stamps. The feature is fail-open - if the throttle dir can't be written, it still fires the wake (it just skips the throttle check).

6. **The original cause of joint-board pollution was the matcher, not defiance.** When diagnosing future pollution complaints: check whether the offending session's message contained bare technical tokens matching live short IDs (F1, F2, chrX, etc.). The @-requirement fix should prevent this, but if it recurs, re-check the regex.
