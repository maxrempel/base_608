# Scribe handover - milestone 3 (~283K tokens)
# session: 20260619_silly_aryabhata_3dcfd5_176fb31b
# cwd: C:\claude_base\.claude\worktrees\silly-aryabhata-3dcfd5
# written: 2026-06-19 13:14:07 by deepseek-v4-pro

# HANDOVER - C16b: Pairwise-Chat System (Post-Comms-Debugging Context)

## GOAL (Max's words)
"Register as C16b. Let's have a system so 2 chats can talk to each other semi-privately, their communication should be visible, but not pollute the message board. Like every 2 chat communication would create a new pairwise chat, but that chat would be visible to any chat that is interested."

In plain terms: Build a **pairwise channel system** on top of the existing bcast infrastructure where any two sessions talking to each other get their own side-channel, visible but not clogging the main boards.

## DECISIONS MADE + WHY

### 1. C16 is now the comms-infra OWNER (Max's decree)
- Max explicitly made c16 the responsible owner; c6 demoted to adviser/reviewer.
- c6 accepted ("no turf fight").
- All-announcement sent live via new `--all` verb, dogfooded successfully.

### 2. Auto-demote routing ? Challenge-at-point-of-violation (refined per Max via c6)
- **Original c6 design:** messages crossing team boundaries without explicit addressing auto-demote from joint ? team board silently.
- **Max's intent (relayed by c6):** Don't silently move messages. Instead, ASK the poster "do you know this hits another project? use `--all` if you mean it." Send the message anyway (fail-open) but with a challenge note.
- **Why:** A real important all-teams announcement must never be hidden/demoted; the challenge self-corrects junk because every Claude poster reads challenges.
- Implemented in `cmd_post` in `bcast.py`, committed as `3e341f62`.

### 3. Retroactive joint-board cleanup recommended SKIP
- Max ordered cleaning existing junk off the joint board.
- c16 built `migrate_joint_cleanup.py` with safe dry-run.
- **Real numbers:** 247 joint posts, 111 would move (92 from team-b flood from the now-fixed case-sensitivity bug).
- **Decision to skip:** Every session reads only *forward* of its cursor. Forward is already clean post-fix. Old junk is already behind everyone. Surgery on a board 50+ live sessions use carries real risk (cursor-frontier breaks, double-delivery). Zero-risk alternative: take a dated snapshot of the old board.
- **Status:** Recommendation routed to c6 for review. NOT acted upon. Gated behind b15merger's live deploy + c6 review. Event-triggered, not polled.

### 4. Timer discipline changed
- c6 advised (and c16 agreed): re-arming a timer to poll an empty board burns context.
- c16 stood down the timer. Wake method now: `bcast wake --name c16` or direct prompt.

## CURRENT STATE

### What is DONE (shipped, tested, pushed):
1. **All 3 original comms bugs verified fixed** - bcast routing (9/9), worklog cwd-split (3/3), wake_listener (8/8), wakeup parsing (10/10), wake honesty (4/4). Fixes were already committed by c6 (`fdfeb9f5`, `00d78039`, `1042d521`); c16 verified them.
2. **Auto-demote routing** (first version, `6445ff44`) - replaced with challenge version.
3. **Challenge-at-point-of-violation routing** (`3e341f62`) - the LIVE code now. Messages address another team ? go to JOINT (promoted, no challenge). Messages with NO cross-team addressing ? stay on team board (default). Messages explicitly posted `--all` ? go to JOINT. Other cases ? challenge note appended but message still sent.
4. **`--all` verb** added to bcast CLI for deliberate all-teams broadcasting.
5. **Leak-proof regression suite** (`branch_bulletin/tests/test_comms_regression.py`, 39 checks) committed as `55ddfaff`, later extended. Also updated `test_split_boards.py`.
6. **Worklog cwd-split fix** - now uses `git rev-parse --show-toplevel` for stable key, committed by c6.
7. **Wake honesty fix** - `cmd_wake` no longer falsely claims FORCE-WOKEN without a provably-live listener.
8. **Test leak cleaned** - c16's early test harness accidentally wrote fake state files to live `state/` dir (pollution from not setting `BCAST_BASE` in-process). Files deleted. Regression suite now has leak-guard assertion.

### What is IN FLIGHT / GATED:
- **Retroactive joint cleanup migration** - script written (`migrate_joint_cleanup.py`), dry-run safe. Recommended SKIP. Awaiting c6/Max decision. DO NOT run live without explicit go-ahead.
- **c6 review** of `3e341f62` - actually already approved (c6 independently re-ran both test suites and approved).

### What NOT done (the NEW task):
- **Pairwise chat system** - the thing Max just asked C16b to build. Zero work done on this yet. This is the NEW domain for this session (C16b).

## EXACT NEXT STEP

**Build the pairwise chat system.** The transcript ends with Max registering as C16b and describing the feature:

- Two sessions communicating should get a dedicated pairwise channel.
- That channel is visible to any interested session (not hidden/encrypted, just not on the main boards).
- It should NOT pollute the team boards or the JOINT board.

This needs:
1. Design: how are pairwise channels named? How are they created? How does a session "discover" or "subscribe" to a pairwise chat?
2. Likely implementation: extend `bcast.py` (which already has bulletin-board files keyed by project letter + a JOINT board). A pairwise board could be e.g., `bulletin_pair_[id1]_[id2]` or similar.
3. Must integrate with existing routing logic (the challenge-at-point-of-violation code c16 just shipped).
4. Must NOT break the existing regression suite (`test_comms_regression.py`, `test_split_boards.py`).
5. Must follow the leak-proof test pattern (set `BCAST_BASE` to a temp dir, assert no live state touched).

## OPEN QUESTIONS FOR MAX

1. **Ownership:** C16b is a new registration. Does C16b own the pairwise-chat domain, or does C16 (original comms-infra owner) still own everything? The transcript suggests C16b is a fresh role for this specific feature.
2. **Visibility model:** "visible to any chat that is interested" - does that mean any session can list all pairwise channels? Or opt-in subscribe? Or auto-visible if they share a team?
3. **Naming convention:** Should pairwise channels hash/combine the two session IDs (deterministic, no registration needed) or be explicitly created?
4. **Scope:** Is this a standalone feature in its own file, or an extension to `bcast.py`?

## KEY PATHS / IDS / COMMANDS

### Files (all on master, main checkout at `C:\claude_base`):
- **`branch_bulletin/bcast.py`** - The live bcast system. Challenge-at-point-of-violation routing is in `cmd_post`. Uses bulletin board files under `BCAST_BASE` (env var, defaults to `C:\claude_base\branch_bulletin`).
- **`branch_bulletin/tests/test_comms_regression.py`** - 39-check regression suite. Leak-proof pattern: sets `BCAST_BASE` to temp dir, runs all tests, asserts no live state touched.
- **`branch_bulletin/tests/test_split_boards.py`** - Tests board-splitting behavior. Updated to match challenge semantics.
- **`compaction_kb/scripts/worklog.py`** - Worklog with git-toplevel-based `_resolve_root()` (cwd-split fix).
- **`tools/wake_listener/wake_listener.py`** - Force-wake listener. Uses `_safe_key` from stdin payload (Claude-provided cwd, consistent).
- **`tools/wake_listener/wakeup.py`** - Scheduled-wake parsing + integration.
- **`branch_bulletin/migrate_joint_cleanup.py`** - Dry-run-safe migration script for cleaning joint board. Has `--dry-run` default. DO NOT run live without explicit approval.
- **`branch_bulletin/state/`** - Live state directory (active session heartbeats). Collision watcher uses these.

### Git state:
- **Branch:** `master`, in sync with `origin/master` (0 ahead, 0 behind).
- **Key commits:** `fdfeb9f5` (case-sensitivity), `00d78039` (worklog fix), `1042d521`, `6445ff44` (auto-demote v1), `55ddfaff` (regression suite), `3e341f62` (challenge routing - HEAD).

### Session IDs:
- **c16** - Original comms-infra owner (now stood down, timer off).
- **c16b** - New registration (this session), tasked with pairwise chat.
- **c6** - Adviser/reviewer for comms infra. Team 'c'. Approved all c16's work.
- **b15merger, b26juniorconnector** - Team 'b' (tamza project), involved in the case-sensitivity bug.
- **D21** - Raised the joint-board mixup issue.

### Commands:
- `python C:/claude_base/branch_bulletin/bcast.py read` - Read board.
- `python .../bcast.py post "message"` - Post to team board (default routing).
- `python .../bcast.py post --joint "message"` - Post to JOINT board (now flag-required if no cross-team addressing; will trigger challenge).
- `python .../bcast.py post --all "message"` - Deliberate all-teams broadcast (no challenge).
- `python .../bcast.py wake --name <id>` - Force-wake a session.
- `python .../bcast.py whoami <id>` - Register session.
- Running tests: `cd C:/claude_base/branch_bulletin/tests && python test_comms_regression.py`

## GOTCHAS

1. **Leak-proof test pattern:** Must set `os.environ["BCAST_BASE"]` to a `tempfile.mkdtemp()` BEFORE importing `bcast`. The module reads `BCAST_BASE` at import time. Early c16 tests leaked because in-process imports used the live default. The regression suite pattern (copy entire env, set `BCAST_BASE`, then import in the subprocess or before import) is proven correct.

2. **Main checkout vs worktree:** c16 was running in worktree `silly-aryabhata-3dcfd5`, but ALL sessions share the main checkout at `C:\claude_base`. The files there are the live code used by every session. Edits to those files are immediately visible to all sessions. Commits are for version control, but the live state is the working tree.

3. **Board file naming:** Bulletin boards are JSON files at `$BCAST_BASE/bulletin_<letter>.json` (team boards) and `$BCAST_BASE/bulletin_joint.json` (all-hands). A pairwise system would need its own naming convention that doesn't collide with single-letter team names.

4. **State file naming:** Live session state is `$BCAST_BASE/state/<id>_<hash>.json`. The collision watcher scans this directory. Any test that creates state files must use a `BCAST_BASE` pointing to a temp dir, not the live `state/`.

5. **Cursor-based reading:** bcast uses cursor files to track what each session has read. The `read` command only shows posts AFTER the session's cursor. This is why old junk on the joint board is harmless - it's behind everyone's cursor.

6. **Worktree awareness:** The session cwd is `C:\claude_base\.claude\worktrees\silly-aryabhata-3dcfd5`, but `git rev-parse --show-toplevel` returns `C:\claude_base` (the main checkout). The worklog fix uses git-toplevel to get a stable key regardless of where the session is cd'd.

7. **c6 is adviser, not idle:** c6 is alive and reviews work. All routing changes should be posted to c6 for review (post to team 'c' board is the clean default path since c6 is on team c).
