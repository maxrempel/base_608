# Scribe handover - milestone 5 (~379K tokens)
# session: 20260622_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-22 07:37:03 by deepseek-v4-pro

# HANDOVER - c16, comms-infra + timer-decel owner

## GOAL (Max's words)
> "ok, next, identify sessions with armed timers and see if any of them are just forgotten. There should be some on duty and likely many forgotten."

The meta-ask: audit the live session ecosystem, find which sessions still have active self-wake timers, classify each as genuinely on-duty vs. abandoned/forgotten, and (presumably) release or decel the dead ones so they stop burning cycles and context.

---

## WHAT WAS COMPLETED BEFORE THIS (for context - this work is DONE)
c16 started as a takeover from c6, became the **owner** of the comms-infra domain (c6 ? adviser). Every bug Max cited was either already fixed by c6 in code, or c16 shipped a fix for it. The stack is proven-green via a 44-check regression suite.

**Verified/shipped:**
- bcast case-sensitivity routing (phantom-team, cross-team bugs) - c6's fix, tested 9/9
- worklog cwd-split keying (git-toplevel anchor) - c6's fix, tested 3/3
- wake_listener + wakeup + scheduled-wake - 18/18 tests
- wake honesty (no fake "FORCE-WOKEN" when listener absent) - 4/4
- 31-check leak-proof regression suite committed, later expanded to 44

**Built + shipped by c16:**
- Challenge-at-point-of-violation routing on the joint board (replaced silent auto-demote): if a session posts without `--all` and without addressing another team, the board ASKS "do you know this hits everyone?" - but still sends it (fail-open). `--all` is now the explicit broadcast verb.
- Cd-misattribution guard: a session chaining `cd /c/claude_base && git commit ; bcast post` would silently post under the wrong id (b29). Now bcast detects a self-declared id prefix (`G2 -> ...`) mismatching the cwd's registered id and REFUSES the post with a clear fix (`--as <name>` override available).
- Timer deceleration system (`tools/timer_decel/timer_decel.py`): a script-backed ladder. Default = "4mt" (decel), which auto-slows after 3 idle wakes per rung: 4min ? 8 ? 15 ? 30 ? 1hr ? 3hr ? 6hr ? 12hr ? 24hr, parks there. Productive wake resets to 4min. Night floor = 3hr unless steady. Steady = "4steady" (holds cadence for on-duty watchers/doers). Email Max only as an alarm: crisis, decel-would-cause-damage, or stuck-in-meaningless-steady asking for release. Global2 updated so new sessions auto-adopt decel.

**Recommended but NOT executed (gated):**
- Retroactive joint-board junk migration: dry-run script exists (`migrate_joint_cleanup.py`), 111 posts would move. c6 concurred with c16's recommendation to SKIP the live migration (old junk is behind everyone's cursor, surgery is risky, zero operational benefit). Archive a dated snapshot instead if you want a clean record. **Still awaiting Max's ruling.**

---

## EXACT NEXT STEP
Read the live session state (`C:/claude_base/branch_bulletin/state/`) and/or the wake_listener's timer tracking, enumerate every session with an armed timer, and classify each one:

1. **Genuinely on duty** - watcher, overnight worker, continuous production ? should be on steady
2. **Forgotten / dead** - timer still firing but session abandoned its task or the chat is gone ? release or decel to prevent noise
3. **Unknown** - session hasn't stated its intent ? flag for Max or email

The timer-decel engine c16 wrote can help here (sessions already using "4mt" will be self-decelerating), but sessions that predate the new system or use raw `ScheduleWakeup` timers may still be churning at fixed cadences.

**How to approach it:** read all `.json` files in `C:/claude_base/branch_bulletin/state/`, cross-reference with any timer-registration files the wake_listener maintains, check which worktrees/chats still exist on disk, and produce a report. Then either force-wake the forgotten ones with a release message, or demote their timers directly if the engine supports it, or flag them to Max.

---

## KEY PATHS, IDS, COMMANDS
| What | Path / Value |
|---|---|
| **Live session state** | `C:\claude_base\branch_bulletin\state\*.json` (each file = one session's cwd?id mapping) |
| **c16's worktree** | `C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75` |
| **G2's worktree** (example of cd-missend victim) | `C:\claude_base\.claude\worktrees\hungry-mayer-737e63` |
| **Main checkout** (shared, causes cd-missend) | `C:\claude_base` (registered id = b29) |
| **bcast board file** | `C:\claude_base\branch_bulletin\bcast.py` (also `bulletin_b`, `bulletin_d`, `bulletin_joint` etc.) |
| **Regression suite** | `C:\claude_base\branch_bulletin\tests\test_comms_regression.py` (44 checks, leak-proof) |
| **Split-boards tests** | `C:\claude_base\branch_bulletin\tests\test_split_boards.py` |
| **Timer decel engine** | `C:\claude_base\tools\timer_decel\timer_decel.py` (CLI: `set 4` or `set steady 4`) |
| **Timer decel tests** | `C:\claude_base\tools\timer_decel\test_timer_decel.py` (17 pass) |
| **Timer method doc** | `C:\claude_base\tools\timer_decel\timer_decel_method_v01_tomemex.md` |
| **Global rules (auto-loads)** | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| **Joint migration script (dry-run ready)** | `C:\claude_base\branch_bulletin\migrate_joint_cleanup.py` |
| **Wake listener** | `C:\claude_base\tools\wake_listener\wake_listener.py` |
| **Wakeup parser** | `C:\claude_base\tools\wake_listener\wakeup.py` |
| **Worklog** | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| **Pushed commits (all on master, in sync with origin)** | `c5b7a9fd` (timer-decel, latest), `b02eb5fb` (cd-misattrib guard), `3e341f62` (challenge routing), `55ddfaff` (regression suite), `00d78039` (c6's worklog fix), `fdfeb9f5` (c6's bcast fix), `6445ff44` (auto-demote - superseded by 3e341f62), `1042d521` (c6 fix) |
| **Register / whoami** | `python C:/claude_base/branch_bulletin/bcast.py whoami <id>` |
| **Read board** | `python C:/claude_base/branch_bulletin/bcast.py read` |
| **Post to teams** | `python C:/claude_base/branch_bulletin/bcast.py post --all "c16 -> ..."` |
| **Force-wake a session** | `python C:/claude_base/branch_bulletin/bcast.py wake --name <id> "message"` |
| **Worklog** | `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"` |
| **Set decel timer** | `SET TIMER_DECEL_BASE=<dir> python C:/claude_base/tools/timer_decel/timer_decel.py set 4` |
| **Set steady timer** | `SET TIMER_DECEL_BASE=<dir> python C:/claude_base/tools/timer_decel/timer_decel.py set steady 4` |

---

## OPEN QUESTIONS AWAITING MAX
1. **Retroactive joint-board cleanup** - skip live migration + archive a snapshot, or do the surgery? (c16 and c6 recommend skip. Script is built and dry-run-tested.)
2. **G2/G3 duplicate-id churn** - two sessions built the same monitor independently; c16 flagged this as NOT a code/infra bug but an owner-assignment / task-management fix for whoever manages those sessions. No resolution yet.

---

## GOTCHAS + RULED-OUT APPROACHES
- **Test harnesses leak state if BCAST_BASE not set before in-process import** - the regression suite in `tests/test_comms_regression.py` uses a leak-guard pattern (asserts no files touched under the live state dir). Always use that pattern or set `BCAST_BASE` in `os.environ` before importing bcast.
- **True session-id anchoring is impossible** - Claude exposes no session-id to CLI subprocesses (verified: no `CLAUDE_SESSION_ID` or similar env var). The cd-misattrib guard works by catching the self-declared id prefix mismatch instead.
- **Cd into `C:\claude_base` (main checkout) changes bcast identity to b29** - the main checkout is a legitimate git root with its own registered identity. Git-worktree-root keying alone won't fix this; the guard is the right layer.
- **Multiple sessions edit main checkout files concurrently** - c16 hit an edit collision mid-session (another session was fixing worklog at the same time). Always re-read before editing. The tree sometimes has uncommitted changes from other sessions.
- **`git push` can non-fast-forward** (a remote "Mike-DC" commit landed) - resolved via `git rebase --autostash origin/master`. The autostash reapply was safe because no uncommitted changes touched the same files.
- **The `_looks_intra_team` function was removed** when c16 built the challenge routing. Any old code or tests referencing it will fail; the tests were updated accordingly.
- **The `--all` flag exists now** - it's the explicit, intentional broadcast to the JOINT board. Without it, posts that don't address another team stay on the poster's own team board.
- **Self-attribution separator required**: bcast now looks for `id ->`, `id:`, or `id =` at the start of a message body to detect self-declared identity. Bare `"b1 freeze please"` (addressing b1 without @) is NOT mistaken for a self-claim because there's no separator.
