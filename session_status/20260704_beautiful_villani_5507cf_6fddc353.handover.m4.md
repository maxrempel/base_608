# Scribe handover - milestone 4 (~309K tokens)
# session: 20260704_beautiful_villani_5507cf_6fddc353
# cwd: C:\claude_base\.claude\worktrees\beautiful-villani-5507cf
# written: 2026-07-04 16:58:10 by deepseek-v4-pro

# HANDOVER: Pine g4 (beautiful-villani) - Cross-Machine Comms & Board Infrastructure

---

## GOAL (Max's own words)

"Think about a way how could cl code sessions from this computer pine, talk to cl code sessions at centauri" - build a reliable cross-machine communication channel, fix the force-wake system so sessions can actually be woken remotely, and stop the global/joint board from being polluted with single-team posts.

---

## DECISIONS MADE + WHY

### 1. Cross-machine channel: fleetcomm (Cloudflare KV worker)
**Choice B (Cloudflare) over A (Nextcloud-synced folder).** Max: "surely B, A is flaky, unreliable, slow."

- Built a dedicated Cloudflare Worker (`fleetcomm.max-rempel2.workers.dev`) with KV backing, not D1 (the Workers-scoped API token lacked D1 admin but had KV permission).
- Auth: weak bearer key `fleetcomm_claymem2026`. 30-day TTL, no auto-retire.
- NOT the existing `claude-wall` (which auto-deletes at 30 min - wrong for async).
- CLI: `C:/claude_base/tools/fleetcomm/fleetcomm.py` (pure stdlib Python). Commands: `post`, `read`, `read --all`, `whoami`. Auto-machine-tagging via HOSTMAP.
- **CRITICAL FIX:** Added `"User-Agent": "fleetcomm/1.0"` header - without it, Cloudflare edge returns 403 for urllib's default UA.
- Deployed to both Pine and Centauri (scp'd to Cent since Centauri can't `git pull` - no GitHub HTTPS creds in non-interactive SSH).
- Centauri's global CLAUDE.md is a symlink to the Nextcloud-synced copy at `D:\Nextcloud\claude_md_synced\`, so the fleetcomm pointer auto-loads on both machines.

### 2. wake_listener - the "force-wake at will" mechanism
The trick: Claude Code `async+asyncRewake` hook, exits code 2 with stderr ? engine wakes idle session and injects stderr as system reminder. Build 2.1.116 supports this.

**Multiple rounds of fixes:**

- **Cursor persistence** (commit 2685305b): The listener's startup baseline was silently dropping wakes posted before the listener armed. Fixed by persisting a per-session fleet cursor in `branch_bulletin/wake/fleet_cursors/<cwd_safe_key>.cursor`. Re-keyed from volatile `session_id` to durable `cwd_safe_key` (survives app restart). **NO age cap** - wakes wait up to 30 days in KV until delivered.

- **Source-mtime guard - REVERTED** (7c60bc45 ? a3a2a7d1): D59 caught that `sys.exit(0)` on code-change kills the listener of every idle session with no way back (truly-idle sessions fire no hook to re-arm). On Windows, `os.execv` also detaches from the hook grid (CRT spawn-and-exit semantics, not image-replace). **Reverted entirely.** The honest position: there is no in-place code refresh on Windows that preserves the wake-grid slot.

- **Worktree-keyed lock for stable wake delivery** (commit cec1e5ce, LATEST FIX): The root cause of force-wake failing for LIVE sessions - a session's `session_id` churns (rotates) faster than the bcast state file gets updated. So `wake --name X9A` resolves to a stale `session_id` whose lock file is dead, drops the signal there, and nobody sees it. **Fix:** the listener now ALSO maintains a stable lock keyed by its worktree path (`wake/locks/wt_<safe_key>.lock`, content = current session_id from stdin). The manager (`_session_id_for` in bcast.py) recovers the live session_id from this worktree lock when the state-file session_id is stale. Both sides compute the identical key via `_safe_key(cwd)`.

### 3. bcast.py - auto-wake on post (commit 251c8d9e)
Max: "Whoever posts on the board should wake up every wakeable session on the board... let's do two minutes."

- After every successful post, `_auto_wake_board_peers()` iterates `_live_wakeable_ids()` for the same board (or all boards if joint post), drops signals to each, throttled at **2 minutes per target** (touch file in `wake/auto_wake_throttle/<id>`). Post bursts within 2 min don't re-wake.
- **1-on-1 detection:** exactly one @-mention ? skip broadcast (target still gets the normal wake).
- **Fail-open** - any error in auto-wake never breaks the post itself.

### 4. Pollution Watcher - stopping single-team posts on the global board

**Problem:** The joint board was flooded with X-team genomics posts. Investigation (credit: x1) found the REAL cause: the router's `_mentioned_ids` matched bare technical tokens like `F1`, `F2`, `F_ROH` as cross-team ids, **auto-promoting** plain team posts to global. Teams never chose global - the tool shipped them there on a false match, then nagged them for something they never did and couldn't undo (board is append-only).

**Fixes shipped (commits 14a64083, dd30e3d5):**

1. **Addressing now requires `@` prefix.** `_mentioned_ids` updated - bare `F1` never promotes; only `@f4` counts. Kills the false auto-promote at the source (zero LLM cost).

2. **Teams CAN still post global questions.** Explicit `--all`/`--joint` or `@`-mentioning another team still routes to joint. Genuine all-teams posts work fine.

3. **Content gate on `--all`/`--joint`** (commit dd30e3d5): When an explicit-global post names no other team, a fast DeepSeek "is this genuinely cross-team?" check runs BEFORE the post lands. Single-team work (postmortem, status, handoff) is rerouted to the team board. Fail-open (DeepSeek down ? posts go through). Rare - only explicit-global posts trigger it, never plain posts.

4. **Watcher got teeth** (watcher.py): Old watcher only whispered "suggestion, your call." Now posts a firm MOVE ORDER to the **offending team's own board** (so the watcher stops polluting joint itself) + force-wakes the team's live sessions. Explains WHY it matters: (a) distracts other teams, blocks their comms; (b) buries genuine cross-team messages.

5. **5-day auto-archive** (RETENTION_DAYS=5 in bcast, wired into watcher's unattended run). Old entries are **archived (moved, not deleted)** to `archive/` subdirs. Verified: joint went 372?233 entries, all saved.

6. **DeepSeek semantic pass** - was down (402 Payment Required), Max refilled, confirmed working again.

### 5. noflash_watch - auto-detect flashing terminal windows
Max: "recently some stupid session on both machines... installed a periodic flashing terminal which is exactly prohibited."

- **Scanner** (`noflash_scan.py`): hourly scheduled task on each machine, enumerates Windows scheduled tasks, flags Interactive ones with console execs (python.exe, cmd.exe, .bat/.cmd, powershell without -WindowStyle Hidden, wscript without //B). Vendors whitelisted. Writes `C:\claude_base\noflash\violations_<host>.json`.
- **SessionStart hook** (`noflash_hook.py`): wired in `~/.claude/settings.json` on both machines, reads violations and injects system-reminder listing offenders + canonical hidden-VBS fix recipe. Fail-open.
- **Fixed actual flashers:** disk-report (both machines - VBS wrapper), safety_watcher.py (CREATE_NO_WINDOW on git subprocess), CF Workers KV Backup (VBS wrapper).

---

## CURRENT STATE - WHAT IS DONE

- **fleetcomm:** Live, both directions Pine?Centauri confirmed, durable (30-day KV), per-session cursors, no age cap.
- **force-wake:** Worktree-keyed lock fix shipped (cec1e5ce), untested in the wild (takes effect as each session re-arms its listener on next turn). The older fixes (cursor persistence, per-worktree cursor keying) are all pushed.
- **auto-wake-on-post:** Live, proven (C12A's board post auto-woke g4 this session). 2-min throttle per target.
- **Pollution Watcher:** Full stack live - @-only matcher, content gate on explicit-global, enforcement watcher (posts to team board + force-wakes), 5-day archive. DeepSeek semantic pass confirmed working after refill.
- **noflash_watch:** Scanner + hook live on Pine and Centauri, 0 current violations.
- **Mike-DC cleanup:** 7 E04 wakes cancelled on Centauri (f4 is sole Mike contact now). MikeDC-Fill Windows task confirmed healthy (Ready, last run 0x0).
- **Zombie listener sweep:** 5 Cent + 32 Pine stale listeners killed. Active sessions re-arm fresh on next prompt.

### Session identity
- This session = **g4** on the bcast board (team g = cross-machine comms)
- Worktree: `beautiful-villani-5507cf` under `C:\claude_base\.claude\worktrees\`
- Decel timer: 30m (via `timer_decel.py`), but this session is effectively done.

---

## EXACT NEXT STEP

**The worktree-keyed lock fix (cec1e5ce) needs validation in the wild.** When a Centauri or Pine session re-arms its listener on its next turn, the new worktree lock code kicks in. Then a force-wake to a session whose state-file session_id is stale should still succeed - the manager recovers the live session_id from the worktree lock.

To verify:
1. Wait for a session that had a stale id (like X9A) to take a turn (or prompt it manually).
2. From ANOTHER session, `wake --name <that_id>`.
3. Confirm the signal is consumed (not "queued" with no armed listener).

Also: **Centauri's git pull is still broken** (no GitHub HTTPS creds in non-interactive SSH). To deploy files to Centauri, you must `scp -i ~/.ssh/sol_key <file> maxre@192.168.1.176:<path>`. A permanent fix (SSH key or credential helper) was flagged as a chip but never addressed.

---

## OPEN QUESTIONS (awaiting Max)

1. **FedEx sender-side ack-and-retry** - the receiver-side cursor fix works, but there's no sender-side "did it actually fire?" tracking. Proposed receiver posts `wake_ack` on real turn; sender re-posts unacked wakes. Max hasn't approved this yet. Mentioned but deferred.

2. **C12A's identity redesign** - worktree=identity to kill the "phantom duplicate id" alarms at the root. Consensus reached (g4 +1), C12A leading, g4 noted compatibility requirement (keep session-id fallback). Not yet deployed.

3. **bcast ID number recycling** - Max asked about reusing 0-50. g4 recommended jumping to C100+ or rotating team letter. No decision made.

---

## KEY PATHS, IDs, COMMANDS

### File paths
- `C:/claude_base/branch_bulletin/bcast.py` - the board system (edited this session)
- `C:/claude_base/branch_bulletin/watcher.py` - Pollution Watcher (edited)
- `C:/claude_base/tools/wake_listener/wake_listener.py` - force-wake listener (edited)
- `C:/claude_base/tools/fleetcomm/fleetcomm.py` - cross-machine CLI
- `C:/claude_base/tools/fleetcomm/worker/index.js` - Cloudflare worker source
- `C:/claude_base/tools/noflash_watch/noflash_scan.py` - flashing terminal scanner
- `C:/claude_base/tools/noflash_watch/noflash_hook.py` - SessionStart hook for violations
- `C:/claude_base/tools/timer_decel/timer_decel.py` - decel timer (set 30, tick work/idle)
- `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` - synced instructions (symlinked to `~/.claude/CLAUDE.md` on both machines)
- `C:/claude_base/branch_bulletin/wake/` - locks, signals, fleet_cursors, auto_wake_throttle
- `C:/claude_base/branch_bulletin/bulletin_joint.jsonl` - the joint/global board (live, gitignored)
- `C:/Users/maxre/.claude/settings.json` - hooks configuration

### SSH to Centauri
```
ssh -i ~/.ssh/sol_key -o StrictHostKeyChecking=no maxre@192.168.1.176
```
(LAN IPv4 only. Centauri Windows box, always-on, `D:\Nextcloud` for synced files.)

### Cloudflare
- Worker URL: `https://fleetcomm.max-rempel2.workers.dev`
- Auth key: `fleetcomm_claymem2026`
- API token (Workers/KV scope, NOT D1): `ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b`
- Account ID: `e4dc2224d6baa721873dca77dc6f057d`
- KV namespace: `4639fd2da50044a09ec5bb42ecc97247`

### bcast commands (from worktree root)
- `python C:/claude_base/branch_bulletin/bcast.py whoami <id>` - check in
- `python C:/claude_base/branch_bulletin/bcast.py post "<msg>"` - post to team board
- `python C:/claude_base/branch_bulletin/bcast.py post --all "<msg>"` - post to global/joint
- `python C:/claude_base/branch_bulletin/bcast.py read` - read team board
- `python C:/claude_base/branch_bulletin/bcast.py read --joint` - read global board
- `python C:/claude_base/branch_bulletin/bcast.py wake --name <id> "<msg>"` - force-wake
- `python C:/claude_base/branch_bulletin/bcast.py catchup` - full history

### fleetcomm commands
- `python C:/claude_base/tools/fleetcomm/fleetcomm.py post "<msg>" --session <label>`
- `python C:/claude_base/tools/fleetcomm/fleetcomm.py read`
- `python C:/claude_base/tools/fleetcomm/fleetcomm.py read --all`

### Recent git commits (most recent first)
- `cec1e5ce` - worktree-keyed lock for stable force-wake delivery (LATEST)
- `dd30e3d5` - pollution content gate on --all/--joint
- `14a64083` - @-only addressing + 5-day archive + watcher teeth
- `251c8d9e` - auto-wake-on-post
- `a3a2a7d1` - revert broken mtime-guard
- `2685305b` - FedEx-grade cursor (no age cap, per-worktree)
- `489dbf19` - CF Workers KV Backup VBS hidden launcher
- `01de2cf7` - safety_watcher CREATE_NO_WINDOW
- `d3c20652` - noflash_watch tool
- `3699e435` - wake confirmation by signal-consumption

---

## GOTCHAS AND DEAD ENDS

### DO NOT REPEAT
1. **Do NOT add any age cap to wake delivery.** Max explicitly demanded FedEx resilience - "even if the machine was completely turned off, the wake should be kept... and shoot and wake up as
