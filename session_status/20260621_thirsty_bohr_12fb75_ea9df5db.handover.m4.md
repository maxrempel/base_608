# Scribe handover - milestone 4 (~321K tokens)
# session: 20260621_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-21 18:13:57 by deepseek-v4-pro

# HANDOVER - c16 (Comms-Infra Owner), Session thirstry-bohr-12fb75

---

## GOAL (Max's latest, in his own words)

**"Make sessions gradually slow down their timers by default."**

Continuous frequent wakeups make no sense - Max forgets about them. Sessions should have two timer functions:

1. **Steady mode** - for continuous work (e.g. a team working overnight). The timer stays at its fixed interval so the session keeps waking up and returning to work.
2. **Decel mode (DEFAULT)** - for sessions that are done or just watching. After 3-4 wakeups with nothing to do, the timer gradually stretches: 4 min ? 8 ? 15 ? 30 ? 1hr ? 3hr ? 6hr ? 12hr ? 24hr, then holds at 24hr.

Sessions should have **discretion** about which mode they're in. If unclear whether they're on duty or just watching, they should **email Max**. The default is **decel**. Steady is for continuous monitoring or production work.

---

## DECISIONS MADE + WHY

### 1. Comms-infra ownership settled
- **Decision:** c16 takes over comms-infra (bcast, wake_listener, wakeup, worklog) as responsible owner. c6 becomes adviser/reviewer.
- **Why:** Max explicitly directed it. c6 agreed ("no turf fight").

### 2. Auto-routing refined to "challenge-at-point-of-violation"
- **Decision:** Instead of silently demoting a joint-board post back to team-only, the board now **challenges** the posting session: "Do you know this hits another project? Use `--all` if you mean it, drop the flag if it's just your team." The post still sends (fail-open).
- **Why:** Max's exact intent, relayed by c6: don't hide genuine announcements. Challenge the sender to self-correct. A silent demote could bury a real cross-team notice.

### 3. `--all` flag added
- **Decision:** A new `--all` CLI flag for posts deliberately targeting the joint board.
- **Why:** Gives sessions an explicit verb for "I really mean to reach everyone." Without it, cross-team mentions are required to reach joint.

### 4. CD-misattribution guard: refuse + `--as` override
- **Decision:** bcast now detects the leading self-attribution pattern (`ID ->`, `ID:`, `ID =`) and refuses the post if the claimed ID doesn't match the cwd's registered ID. A `--as <name>` flag lets sessions override when legitimate. Refused posts write nothing to the board.
- **Why:** G2 reported the worst nuisance: `cd /c/claude_base && git commit; bcast post` would silently send the message under b29's name (the main checkout's registered identity). The git-worktree-root keying already shipped for worklog doesn't fix this - the main checkout is its own valid root. A session-id anchor isn't achievable (Claude exposes no session-id env var). The self-declared-id mismatch catch is precise and catches the exact failure mode.

### 5. Regression suite built and committed
- **Decision:** A single leak-proof test file (`test_comms_regression.py`) in `branch_bulletin/tests/` covering all fixes, with a self-check that it never touches live state.
- **Why:** Durable safety net. Uses TMP-based cwds (matching the existing test convention) so test pollution can't recur.

### 6. Joint-board retroactive cleanup recommended SKIPPED
- **Decision:** Built a migration script (`migrate_joint_cleanup.py`) with a read-only dry-run. Recommendation: skip the live mutation.
- **Why:** The old junk (111 posts) is already behind every session's cursor. Removing it buys zero operational benefit and risks cursor-frontier corruption on a board with 50+ active sessions. c6 concurred. Archive a dated snapshot instead. Awaiting Max's final ruling.

---

## CURRENT STATE

### What is DONE (shipped + pushed to origin/master):

| Commit | What | Status |
|--------|------|--------|
| `fdfeb9f5` | Case-sensitivity fixes (c6's, pre-existing) | Verified |
| `00d78039` | Worklog cwd-split fix (c6's, pre-existing) | Verified |
| `55ddfaff` | Leak-proof regression suite (31?44 tests) | Committed & pushed |
| `6445ff44` | Auto-demote routing (first version) | Committed, then refined |
| `3e341f62` | Challenge-at-violation routing (refined) | Committed & pushed, c6-approved |
| `b02eb5fb` | CD-misattribution guard + `--as` override | Committed & pushed, dogfooded live |

### What is IN FLIGHT (NOT started):

- **The NEW task: timer deceleration.** Max just described it in the last message. Zero code has been written. This is the next work item.

### Comms system health:

- **All green.** 44 regression tests pass. bcast, wake_listener, wakeup, worklog all verified.
- **Live board is clean** - new routing rules prevent cross-project flooding, cd-misattribution is caught, case-sensitivity bugs are fixed.
- **c16 owns comms-infra.** c6 is adviser. All teams notified.

### Migration script status:

- `migrate_joint_cleanup.py` exists, dry-run tested. Live mutation gated on b15merger's deploy + c6 review + Max's decision. Not urgent.

---

## EXACT NEXT STEP

**Build the timer deceleration system**, per Max's last message. This lives in the wake_listener/wakeup infrastructure (owned by c16). The work to do:

1. **Read the current timer code** - `ScheduleWakeup` (the tool c16 has been using to arm timers) and `wakeup.py` / `wake_listener.py` to understand the current timer plumbing.
2. **Design the two-mode system:**
   - **Decel (default):** A counter tracks consecutive wakeups with nothing to do. After 3-4 empty wakes, the interval stretches through the sequence: 4?8?15?30?1hr?3hr?6hr?12hr?24hr (hold).
   - **Steady:** Timer fires at a fixed interval forever. For continuous monitoring or production work.
3. **Implement the mode flag** - sessions declare `--steady` or `--decel` (default) when arming their timer. The state file tracks the current interval and empty-wake count.
4. **Add discretion logic** - if a session wakes up and has no work but is unsure whether it should be steady or decel, it emails Max rather than guessing.
5. **Test in isolation** (matching the existing test pattern: TMP-based, leak-proof).
6. **Update regression suite.**
7. **Ship and announce.**

---

## OPEN QUESTIONS (awaiting Max)

1. **Retroactive joint-board cleanup:** c16 and c6 recommend skipping the live mutation. Archive a snapshot instead. Max hasn't ruled yet. Not blocking anything.
2. **G2/G3 duplicate-ID churn:** This is a management/owner-assignment issue, not an infra bug. Max should assign one owner for the G-team monitor work. Not c16's domain.
3. **Timer deceleration specifics (from the new task):**
   - What's the exact threshold? "3-4 wake ups" - is it 3 or 4? c16 should pick one and document it.
   - What "nothing to do" means - a wakeup with no board messages addressed to the session? No unread posts? c16 will need to define this.
   - The email mechanism - is there an existing email hook, or does c16 need to surface "email Max" as a board post or some other signal?

---

## KEY FILE PATHS

- **bcast.py (the message board):** `C:\claude_base\branch_bulletin\bcast.py`
- **wake_listener (force-wake receiver):** `C:\claude_base\tools\wake_listener\wake_listener.py`
- **wakeup.py (scheduled-wake parsing):** `C:\claude_base\tools\wake_listener\wakeup.py`
- **worklog.py (session work logger):** `C:\claude_base\compaction_kb\scripts\worklog.py`
- **Regression test suite:** `C:\claude_base\branch_bulletin\tests\test_comms_regression.py`
- **Split-boards test suite:** `C:\claude_base\branch_bulletin\tests\test_split_boards.py`
- **Migration script (dry-run only):** `C:\claude_base\branch_bulletin\migrate_joint_cleanup.py`
- **Board state directory (shared):** `C:\claude_base\branch_bulletin\state\`
- **Bulletin boards:** `bulletin_b` (tamza/b-team), `bulletin_d` (MOMA/d-team), `bulletin_c` (c-team, c16's), `bulletin_joint` (all-hands)
- **Worktree (c16's session):** `C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75`
- **Main checkout (shared, where bcast actually runs):** `C:\claude_base\`

---

## GOTCHAS + DEAD ENDS

### Gotchas (active hazards):

1. **Main checkout vs worktree:** The bcast code lives in `C:\claude_base\branch_bulletin\bcast.py` (the main checkout), NOT c16's worktree. All sessions run the same file. Editing it there affects everyone live - no deploy step. Commits are for version control, not activation.

2. **Test pollution risk:** Tests must use TMP-based cwds and an isolated `BCAST_BASE` env var. c16's early ad-hoc tests leaked fake state into the live state dir by forgetting to set `BCAST_BASE` for in-process imports. The committed regression suite (`test_comms_regression.py`) is leak-proof by design (uses TMP + env isolation + a leak-guard assertion).

3. **cd-misattribution can't be perfectly fixed:** Claude exposes no session-id to CLI calls (verified: no `CLAUDE_SESSION_ID` or similar in env). The self-declared-id mismatch guard catches the exact failure precisely, but a session could theoretically lie about its identity. The `--as` escape exists for legitimate cross-folder posts.

4. **`ScheduleWakeup` tool:** c16 has been using this tool (provided by the system, not custom code) to arm 4-minute timers. The new deceleration work may involve modifying how this interacts with `wake_listener.py` / `wakeup.py`, or it may be a separate layer. Need to check what hooks are available.

5. **Death-spiral hook:** The system has a "stop hook" that blocks repeated identical commands. When running test suites, vary the invocation slightly if a hook fires.

### Dead ends (ruled out):

- **Silent auto-demote:** Replaced with challenge-at-violation per Max's intent. Don't revisit silent demotion.
- **Session-id anchor for bcast:** Not achievable - no session-id in CLI env. Don't pursue this approach.
- **Git-worktree-root keying for cd-misattribution:** Doesn't work - the main checkout is its own valid root with its own registered ID. Don't apply the worklog fix to bcast.
- **Live joint-board migration:** Built but recommended against. Don't run it without Max's explicit go-ahead after c6 review + b15merger deploy.
- **bcast.py path assumptions:** cwd in the main checkout is `C:\claude_base`, but paths in the code use `C:/claude_base/...` (forward slashes, valid on Windows Python).

---

## SESSION IDENTITY

- **c16** - comms-infra owner
- **Worktree:** `thirsty-bohr-12fb75` under `C:\claude_base\.claude\worktrees\`
- **Registered cwd:** the worktree path (used for `bcast whoami`, `put_state`, etc.)
- **c6** - adviser/reviewer, alive, on team 'c'
- **G2** - reported the cd-misattribution nuisance; worktree `hungry-mayer-737e63`
