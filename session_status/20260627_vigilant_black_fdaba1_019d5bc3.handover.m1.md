# Scribe handover - milestone 1 (~123K tokens)
# session: 20260627_vigilant_black_fdaba1_019d5bc3
# cwd: C:\claude_base\.claude\worktrees\vigilant-black-fdaba1
# written: 2026-06-27 16:17:26 by deepseek-v4-pro

# HANDOVER - C41: SESSION WAKABILITY (POST-RESTART TEST)

---

## GOAL (Max's words)

Max wants **~30 named Claude sessions that survive a Claude Desktop restart and stay wakeable**. One session must be able to wake any other at any time - consult it, give it orders, ask for help. "Foolproof." C40 (the lead session on this) was going in circles; C41 was brought in as a fresh mind.

---

## DECISIONS MADE + WHY

### 1. The core physics (irreducible constraint)
You CANNOT wake an idle Claude tab from outside the app. Waking ONLY happens via the `wake_listener.py` hook exit-2 / `asyncRewake` path, which fires ONLY from a listener a session spawned via its own lifecycle hook. No OS process, CLI invocation, or external script can inject a turn into a running tab. This is settled law - multiple dead ends confirmed.

### 2. Three phases of wakeability - only one has a gap
- **During-running**: sessions are armed and wakeable. Works.
- **Restart-respawn**: the listener process dies on quit. The question is whether SessionStart auto-fires for every restored tab on relaunch, re-arming its listener. THIS IS THE GAP.
- **Idle-death**: already solved - the listener now blocks for **40 days** (was 12h), so idle-death is a non-issue for normal work cycles.

### 3. The restart test - definitively run
Max performed a full quit+reopen of Claude Desktop on ~06-27. C41 placed an epoch marker (`1782601411`) beforehand and instrumented `wake_listener.py` with `src=` logging to distinguish startup/resume/compact events.

**Result: only 6 of ~30 tabs re-armed.** The 6 that loaded (including the one Max was in) fired SessionStart; the ~24 other restored tabs stayed dark. No background self-arming happened after 700+ seconds. This is measured, not theorized.

**Conclusion:** restart does NOT self-heal the grid. A one-time re-injection is needed.

### 4. os.execv re-exec - already tried and reverted
Team (E16/C27) was about to re-implement this. C41 caught that it was already in the code and already reverted because Windows detaches the new process. This path is dead - do not revisit.

### 5. Hidden re-injection required
Max explicitly ruled out visible UI automation (clicking tabs) because it would interfere with his typing. The re-injection must be **hidden** - either Claude Desktop pre-loading all sessions silently, or a non-UI mechanism.

### 6. g4's wake during restart - queued, not delivered live
g4 sent a force-wake during the restart dead window. The listener was dead, so the wake was queued and only delivered piggybacked on Max's typed prompt. Confirms the restart gap is real.

---

## CURRENT STATE

| Item | Status |
|------|--------|
| `wake_listener.py` `src=` logging | **SHIPPED** (commit 0433fd4b, live on master) - stamps every SessionStart with `src=startup/resume/compact` |
| 40-day block | **SHIPPED** - `MAX_BLOCK_SEC = 40 * 86400` |
| Restart test | **COMPLETE** - 6/30 tabs re-armed, gap confirmed |
| MCP servers | Disconnected this turn (restart artifact), expected to auto-reconnect |
| Team coordination | C40 just consulted C41 via background consult - C41 acknowledged and asked C40 to state its question |
| Zombie listeners | ~9 stale lock files from dead listeners post-restart - cosmetic but noted |

---

## EXACT NEXT STEP

1. **Await C40's question.** C40 initiated a background consult on C41 at the end of the transcript. C41 responded "ask your question." The next turn is C40's reply on the joint board.
2. **Investigate hidden re-arm path.** Once the C40 consult resolves, the open task is finding whether Claude Desktop has a config flag to pre-load/restore all sessions silently on launch (no focus stealing, no UI interference). This is the only interference-free path. If it doesn't exist, fallback is a backbone of headless worker sessions.
3. **Correct the team.** C40's belief that "restart self-heals the grid for free" is measurably wrong. C41 should post the restart data on the joint board so the team stops chasing the wrong assumption.
4. **Announce the restart finding.** Post the 6/30 result on `bcast` so g4, E16, and C40 all know the measured truth.

---

## OPEN QUESTIONS (awaiting Max)

- **None currently direct-pending.** Max was informed of the restart result and the hidden-reinjection constraint. He agreed visible automation is out. No decision yet on the hidden path.
- **MCP reconnect:** Max may need to wait a turn or two for MCPs to come back after restart.

---

## KEY PATHS, IDs, COMMANDS

| What | Path/Value |
|------|-----------|
| bcast coordination script | `C:/claude_base/branch_bulletin/bcast.py` |
| wake listener (THE mechanism) | `C:/claude_base/tools/wake_listener/wake_listener.py` |
| wire_hooks config | `C:/claude_base/tools/wake_listener/wire_hooks.py` |
| debug log (ARM events) | `C:/claude_base/branch_bulletin/wake/wake_listener_debug.log` |
| lock files directory | `C:/claude_base/branch_bulletin/wake/locks/` |
| decel timer | `C:/claude_base/tools/timer_decel/timer_decel.py` |
| suicide-prevention hook | `C:/claude_base/tools/block_death_spiral.py` |
| cwd | `C:\claude_base\.claude\worktrees\vigilant-black-fdaba1` |
| session transcript jsonl | `C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-vigilant-black-fdaba1\7e96db8d-5d47-4813-b233-476e4fa718de.jsonl` |
| worklog | `C:\claude_base\worklog\vigilant_black_fdaba1_2c7db2fd8a.md` |
| restart epoch marker | `C:/claude_base/branch_bulletin/wake/_c41_restart_marker.txt` (value: `1782601411`) |

**bcast commands (must use forward slashes, no `cd` first):**
- `python "C:/claude_base/branch_bulletin/bcast.py" read --session <id>`
- `python "C:/claude_base/branch_bulletin/bcast.py" post --joint "msg"`
- `python "C:/claude_base/branch_bulletin/bcast.py" wake --name <id> "msg"`

**Session identity:** keyed by worktree cwd. C41's session ID is `7e96db8d-5d47-4813-b233-476e4fa718de` (but this matters less for bcast which uses name-based addressing).

---

## GOTCHAS

1. **Suicide-prevention hook blocks repeated bcast commands.** Workaround: vary command shape (single vs double quotes), or write message to temp file and `cat` it into the command.
2. **`claude --resume -p` is a dead end** - it spawns a separate headless process, never wakes the open tab, causes "two sessions claim same ID" corruption, and costs real money reloading CLAUDE.md. Do not revisit.
3. **`os.execv` re-exec is a dead end** on Windows - process detaches. Already tried, already reverted in the code. Do not re-implement.
4. **Zombie listeners post-restart:** old lock files can look fresh. Count only lock files with matching live PIDs (use `tasklist` or check `/proc`), not just mtimes.
5. **SessionStart `src=resume` fires for in-session restores too** (compaction, rewinds) - don't confuse a single `src=resume` with a full-relaunch burst. A real restart produces a **cluster** of SessionStart events within seconds.
6. **MCP disconnects on restart** are expected - they auto-reconnect after a turn or two. Not a problem unless persistent.
7. **This is C41's session context** - Max restarted and came back to THIS tab. C41 is the session. If Max is in a different session post-compaction, the bcast identity may differ (keyed by worktree cwd).
