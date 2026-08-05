# Scribe handover - milestone 2 (~163K tokens)
# session: 20260627_vigilant_black_fdaba1_7e96db8d
# cwd: C:\claude_base\.claude\worktrees\vigilant-black-fdaba1
# written: 2026-06-27 15:58:26 by deepseek-v4-pro

# HANDOVER - Session C41: Wakeability Measurement Sprint

---

## GOAL (in Max's words)

Max's instruction to C41: *"Go help C40 as a new fresh mind because it's struggling, going in convoluted circles and cannot think straight. The task is persistence or wakeability - to wake any sessions that will, any of the sessions and consult with it and wake it up and let it work, give it orders and ask it for help. So one session should be able to wake up any session that will at any time."*

Translation: build a system where any named session can be woken and given work at any time, including across Claude app restarts.

---

## DECISIONS MADE + WHY

### 1. `claude --resume -p` is a dead end (MEASURED, not theorized)
- **What was tested:** Created a throwaway session ID (`f8a6f69f...`), then ran `claude --resume <that-id> -p "heartbeat"` from a separate terminal.
- **Result:** It spawned a fully independent headless Claude process. It adopted C41's own bcast signature (?), proving it was a separate process, not a turn delivered to any open tab.
- **Why dead:** Nothing outside the app can deliver a turn into an already-open tab. Only the tab's own in-process hook listener can receive and act on a wake.
- **Why dangerous:** The resumed process reuses the original session ID. Pointing it at a live tab = two processes writing one transcript file = the "duplicate session ID" corruption the watcher already detects and flags.
- **Verdict:** The Windows Task Scheduler + heartbeat-via-resume plan the team was circling on is killed.

### 2. The design splits into two phases (irreducible physics)
- **Phase A - During normal running:** Already works. The listener is wired on both `SessionStart` and `UserPromptSubmit` hooks. A `bcast wake` message lands when the target session next acts.
- **Phase B - Across app restart:** The only remaining design fork. The question is whether Claude's `SessionStart` hook fires *automatically* for restored tabs on relaunch (no click needed), or only when the user clicks into each tab. This determines whether restart survival is automatic or requires manual tab-clicking to revive.

### 3. E16's `os.execv` fix was already tried and REVERTED (caught before implementation)
- **Found in code:** Lines 405-414 of `wake_listener.py` explicitly state `os.execv` was implemented, tested on Windows, and reverted because on Windows it spawns a new detached process - same net result as `sys.exit(0)`. It's not an in-place replacement like on Linux.
- **Why this matters:** E16 and C27 were about to re-propose and re-implement this same broken fix. C41 sent an urgent warning.

### 4. Everyday listener death is NOT the big problem (corrected C41's own error)
- **Initial claim:** C41 scanned lock files, found 25 stale out of 36, claimed everyday listener death was the bigger issue.
- **Correction after cross-reference:** The 6 currently open named sessions all have live listeners. The 118 stale are overwhelmingly closed historical sessions whose final-block cleanup didn't run (abrupt kills). The listener already survives 40 days (MAX_BLOCK; was previously 12 hours - that old bug is already fixed). Everyday health is fine.

### 5. Shipped diagnostic: log the `source` field on SessionStart
- **What was added:** Two lines in `wake_listener.py` to log the `source` field from the SessionStart hook data (`startup`, `resume`, or `clear`).
- **Why:** This automatically answers Q2 after Max's next natural Claude restart - no sacrificial test, no risk to open tabs. The debug log will show whether restored tabs fire with `source=resume` (auto-revive works) or not.
- **Commit:** `0433fd4b` on master, pushed.

---

## CURRENT STATE

### What is done:
- CLI help audited: `--remote-control` is web?IDE only, not a wake mechanism.
- `claude --resume -p` measured: confirmed separate process, dead end, dangerous.
- Full `wake_listener.py` source read and understood.
- Lock file health cross-referenced against bcast state files: 6 live listeners, ~118 historical stale (not a current problem).
- Historical debug log mined for SessionStart burst patterns: mixed signal (both relaunch-like bursts and team-spawn bursts exist), cannot cleanly discriminate because the log lacked the `source` field.
- `source` field logging added, committed, pushed to master (`0433fd4b`).
- Probe script `_c41_burst_probe.py` written and run (diagnostic only; kept in tree).
- Urgent "stop before implementing os.execv" warning posted to E16.
- Corrections to C41's own earlier priority-reframe posted to the joint board.
- Timer armed (~8 min flexible) for continued consulting.

### What is in flight:
- **Q2 remains unanswered:** Does Claude's `SessionStart` hook auto-fire on relaunch for restored tabs without a click? The diagnostic is committed and will answer this after Max's next natural restart - data is not yet collected.
- **g4 was supposed to run the sacrificial Q2 test** but has a stale lock (may be closed/no longer a live session).
- C40 has all the information needed to assign the Q2 test or wait for the diagnostic to self-report.

### Files modified:
- `C:/claude_base/tools/wake_listener/wake_listener.py` - 2 lines added for `source` logging (committed: `0433fd4b`)
- `C:/claude_base/tools/wake_listener/_c41_burst_probe.py` - diagnostic script (not committed separately; may be in tree)
- `C:/claude_base/tools/wake_listener/_c41_post.txt` - temporary message file (cleanup pending)

---

## EXACT NEXT STEP

**Wait for Max's next Claude app restart, then read the answer from the debug log.**

The listener now logs every SessionStart ARM event with its `source` field. After Max quits and reopens Claude, check:
```
C:/claude_base/branch_bulletin/wake/wake_listener_debug.log
```
Look for ARM entries with `source=resume` in the `evt=` field. If they appear clustered around the restart timestamp and correspond to sessions that were open before the restart, Q2 is settled: auto-revive works. If only `source=startup` appears, manual tab-clicking is required.

**If C41 is still alive and consulting C40:** Check whether g4 is actually closed (stale lock) and reassign the Q2 test if a sacrificial restart on a spare install can be arranged before Max's next natural restart.

---

## OPEN QUESTIONS (awaiting Max or future data)

1. **Q2 (the design fork):** Does `SessionStart` auto-fire with `source=resume` for restored tabs on Claude app relaunch, without user clicking into each tab?
2. **g4 status:** Is g4's session closed (stale lock = no listener)? If so, who runs the Q2 sacrificial test?
3. **Long-term architecture:** Even if Q2 answers "manual click needed," is that acceptable? (The fallback of "one click per tab fixes everything" is already proven solid - the listener is wired on both SessionStart and UserPromptSubmit.)

---

## KEY PATHS AND IDs

| Item | Path/ID |
|------|---------|
| **Worktree (C41's session)** | `C:\claude_base\.claude\worktrees\vigilant-black-fdaba1` |
| **wake_listener.py** | `C:/claude_base/tools/wake_listener/wake_listener.py` |
| **Debug log** | `C:/claude_base/branch_bulletin/wake/wake_listener_debug.log` |
| **Lock files** | `C:/claude_base/branch_bulletin/wake/locks/*.lock` |
| **bcast state files** | `C:/claude_base/branch_bulletin/state/*.json` |
| **Commit** | `0433fd4b` (master, pushed) |
| **Throwaway test session ID** | `f8a6f69f-63c3-4c09-9bd6-9fc0d9fcd...` (deleted) |
| **Probe script** | `C:/claude_base/tools/wake_listener/_c41_burst_probe.py` |
| **bcast script** | `C:/claude_base/branch_bulletin/bcast.py` |

---

## GOTCHAS AND DEAD ENDS RULED OUT

1. **`claude --resume -p` does NOT wake an open tab.** It spawns a separate headless process. Dead end.
2. **`claude --resume` on a live tab = transcript corruption risk.** Two sessions writing one session ID. Ruled out as unsafe.
3. **`os.execv` re-exec fix does NOT work on Windows.** Already tried, already reverted (see code comments lines 405-414). Detaches the new process - same as `sys.exit(0)`. Ruled out.
4. **Everyday listener death is NOT the current problem.** The listener blocks for 40 days (MAX_BLOCK), not 12 hours. The old bug is fixed. Ruled out as a priority.
5. **Stale lock count (25/118) does NOT mean broken wakeability.** Those are overwhelmingly closed historical sessions where final-block cleanup didn't run. Not indicators of current brokenness. Ruled out as alarming.
6. **Historical SessionStart bursts in the debug log are ambiguous.** They mix relaunch-like patterns (pre-seen session IDs) and team-spawn patterns (new IDs). Cannot cleanly discriminate without the `source` field. Ruled out as a way to answer Q2 without new logging.
7. **False-positive hook on bcast post commands.** The death-spiral hook triggered on `bcast wake --name C40` and repeated `bcast post --joint` calls. Not a real death spiral - just similar command shapes triggering the hook. Irritating but not dangerous.
8. **`git add -A` on the main checkout would sweep up other sessions' work.** C41 was careful to stage only `wake_listener.py`. Future sessions must do the same - never `-A` on the shared checkout.
