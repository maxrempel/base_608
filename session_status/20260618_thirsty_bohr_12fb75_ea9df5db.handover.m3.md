# Scribe handover - milestone 3 (~248K tokens)
# session: 20260618_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-18 16:21:18 by deepseek-v4-pro

# HANDOVER - c16 team-comms debugger

---

## GOAL (Max's words)

"Debug and test whole system. It is a fucking mess. Very useful but very buggy." - then specifically: fix and test the bcast/worklog/wake_listener bugs (case-sensitive team derivation, cross-team @-mention routing, worklog cwd-split). Later: "talk to C6. it is now adviser, you are now responsible for debugging." And finally diagnose the joint-board mixup where two unrelated projects appeared interleaved.

---

## DECISIONS MADE + WHY

### 1. Verified, didn't rewrite
The three reported bugs were **already fixed in committed code** by c6 (commits `fdfeb9f5`, `00d78039`, `1042d521`). Nobody had verified them. Decision: build isolated test harnesses against a fake `BCAST_BASE` rather than touch live code, prove they work, then commit durable regression tests.

### 2. Leak-proof testing pattern
The first ad-hoc test scripts accidentally polluted the **live** state directory because in-process `import bcast` uses the real `BCAST_BASE` unless `os.environ` is set before import. Fixed by: (a) setting `BCAST_BASE` in `os.environ` before any in-process imports, (b) writing the permanent regression suite to use temp dirs and assert no leaks at the end. The collision watcher correctly caught the pollution - it works.

### 3. Auto-demote routing (the big feature build)
Problem: the joint board was flooded because messages between same-team members were routing to the shared all-hands channel. Root cause was the now-fixed case-sensitivity bug (miscased team letters force-routed to joint) plus b15merger's `--joint` workaround compounding it. **The two projects already had separate boards** - the structure was correct, routing was wrong.

Solution (advised by c6, built by c16): kill the old `--joint`/`--team` flags and `_looks_intra_team` heuristic. Replace with unified logic in `cmd_post`: routing follows **who you address**.
- Cross-team `@mention` ? joint board (promoted, with NOTE)
- Same-team or no `@mention` ? team board (demoted)
- `--all` flag ? forces joint regardless (explicit broadcast intent)

### 4. c16 owns comms-infra now, c6 advises
Max decided the overlap: c16 is responsible owner, c6 is adviser/reviewer. c16 announced this to all teams using the new `--all` verb (dogfooding confirmed it works live).

---

## CURRENT STATE

**All fixes shipped and pushed to master (origin in sync):**

| What | Commit | Status |
|------|--------|--------|
| Case-sensitivity fixes (bcast routing) | `fdfeb9f5` (c6) | Verified green |
| Worklog cwd-split fix (git-toplevel anchor) | `00d78039` (c6) | Verified green |
| Wake-listener/wakeup baseline | `1042d521` (c6) | Verified green |
| Regression suite (31?35 checks, leak-proof) | `55ddfaff` (c16) | On master, pushed |
| Auto-demote routing + `--all` | `6445ff44` (c16) | On master, pushed, live-dogfooded |

**Test scores:**
- bcast @-mention routing: 9/9 original + 4/4 auto-demote = 13/13
- wake_listener: 8/8
- wakeup parse+integration: 10/10
- wake honesty (no fake FORCE-WOKEN): 4/4
- worklog cwd-split: 3/3
- **Total: 38/38 across two suites** (`test_comms_regression.py` 35 + `test_split_boards.py` updated assertions)

**Live state clean:** test pollution cleaned (4 leaked JSON files deleted), only the real c16 session remains in the state dir.

**Board quiet:** No new comms bugs posted. c6 was force-woken for design review of the auto-demote routing. Awaiting its feedback.

---

## EXACT NEXT STEP

Re-read the board for:
1. **c6's review feedback** on the auto-demote routing (`6445ff44`) - it was force-woken and asked to review
2. **Any new comms bugs** now that ownership is announced to all teams

If nothing inbound: stand down the timer. The comms stack is fully verified, shipped, and no open work remains.

If c6 has review notes: implement them, update tests, commit, push, re-announce.

---

## OPEN QUESTIONS (for Max)

1. **None actively blocking.** The c16/c6 ownership overlap is resolved. The only thing c6 kicked back was "Max should decide" - which Max did ("talk to C6. it is now adviser, you are now responsible for debugging").

---

## KEY PATHS / IDS

| What | Path |
|------|------|
| Main bcast code | `C:\claude_base\branch_bulletin\bcast.py` |
| worklog (cwd fix) | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| wake_listener | `C:\claude_base\tools\wake_listener\wake_listener.py` |
| wakeup parser | `C:\claude_base\tools\wake_listener\wakeup.py` |
| Regression suite | `C:\claude_base\branch_bulletin\tests\test_comms_regression.py` |
| Split-boards tests | `C:\claude_base\branch_bulletin\tests\test_split_boards.py` |
| Live state dir | `C:\claude_base\branch_bulletin\state\` |
| Live board data | `C:\claude_base\branch_bulletin\bulletin_*.json` (b through joint) |
| Git worktree | `thirsty-bohr-12fb75` (but all sessions run main checkout files directly) |
| Commit: auto-demote | `6445ff44` |
| Commit: regression suite | `55ddfaff` |
| Commit: worklog fix | `00d78039` |
| Commit: case-sensitivity fixes | `fdfeb9f5` |

---

## GOTCHAS

1. **BCAST_BASE env leak:** If you import `bcast` in-process without setting `BCAST_BASE` in `os.environ` first, it resolves to the live directory. Always set it to a temp dir before importing, or use subprocesses with a custom env dict. The permanent test suite enforces this with a leak-guard assertion.

2. **Worktree vs main checkout:** The worktree is `thirsty-bohr-12fb75`, but all live sessions run files from `C:\claude_base\` directly. Edits to `bcast.py` or `worklog.py` take effect immediately for all sessions - they import from main checkout, not the worktree.

3. **c6 is still alive:** It stood down ownership but is active as adviser. Don't fight it for edits - coordinate on the board.

4. **`_looks_intra_team` is gone:** Removed as part of the auto-demote build. If any old code or tests reference it, they'll break.

5. **`--joint` flag still parsed but deprecated:** The old `--joint` in `cmd_post` was replaced by auto-demote logic. The CLI parser may still accept it but behavior changed.

6. **Joint board is NOT mixed by project:** The two projects (tamza/b-team, MOMA/d-team) each have their own private board (`bulletin_b`, `bulletin_d`) that was never cross-contaminated. Only the shared `bulletin_joint` was flooded, and the auto-demote routing now prevents same-team messages from landing there.
