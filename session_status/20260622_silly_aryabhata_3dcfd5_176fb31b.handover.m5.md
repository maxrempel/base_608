# Scribe handover - milestone 5 (~375K tokens)
# session: 20260622_silly_aryabhata_3dcfd5_176fb31b
# cwd: C:\claude_base\.claude\worktrees\silly-aryabhata-3dcfd5
# written: 2026-06-22 07:24:08 by deepseek-v4-pro

# HANDOVER - c16b ? comms-infra owner

## GOAL (Max's exact words)
> "Implement [the rooms feature] on centauri too - package and wake up the appropriate session and negotiate which one can implement."

Max just approved the rooms feature after seeing it shipped here. He now wants the same thing built on a different system called **centauri**. The session that owns or can build on centauri must be force-woken, the rooms feature packaged clearly, and ownership negotiated.

---

## DECISIONS MADE + WHY

1. **Rooms as separate files, not board entries.** Room messages go to `rooms/<name>.jsonl` - never touch team/joint boards. Zero pollution, but fully readable by any curious chat via `--read`. Max wanted visible-but-not-spammy; this delivers exactly that.

2. **Parse heuristic: single-token = name, multi-word = message.** The original parse grabbed the first word as room name, so `room --with d5 "hello world"` would try to name the room `"hello"`. Fixed it: if the positional has spaces, it's a message and we auto-name the room. Clean single-token = room name.

3. **Auto-hear is wired through `cmd_read`.** Every time a session catches up on the board, it also scans rooms it's a member of for new messages past its cursor. Rooms deliver seamlessly without the poster doing anything extra.

4. **No advertising broadcast for the feature.** Per the no-unnecessary-all-teams rule, rooms ship silently - the receiver gets usage instructions inline when a room message arrives.

5. **Branch emoji on names was built earlier in this session.** Branched ids (`c16b`, `c17`) now get a leaf ? on the right plus an auto-glyph ? from session_id hash. Descriptive names (`b15merger`) get no marker. This way Max can visually tell forks apart.

6. **c16b is the official comms-infra OWNER** (Max assigned it). The parent c16 is idle/retired. c6 is adviser/reviewer, not owner.

---

## CURRENT STATE

**On THIS system (the "base" project, worktree `silly-aryabhata-3dcfd5`):**
- Rooms feature is **fully built, tested, committed, and pushed** to master.
  - Commit: `cff41c76` on master, synced with origin.
  - File: `C:\claude_base\branch_bulletin\bcast.py`
  - Tests: `C:\claude_base\branch_bulletin\tests\test_comms_regression.py` (now has 14+ rooms-specific tests, plus all previous routing/wake/worklog tests)
  - Usage: `bcast.py room --with <id> "message"`, `bcast.py room <name> --add <id>`, `bcast.py rooms`, `bcast.py room <name> --read`

- **On centauri: NOTHING built yet.** Max just ordered it. This session (c16b) has no knowledge of centauri's codebase, architecture, or which chat owns it.

---

## EXACT NEXT STEP

1. **Package the rooms feature for centauri.** Read `bcast.py` from THIS codebase, specifically:
   - The `ROOMS_DIR` constant and directory creation
   - `_list_rooms()`, `_find_or_create_room()`, `_room_members()`, `_room_cursor_key()` helpers
   - `cmd_room()` and `cmd_rooms()` commands
   - The rooms auto-hear block injected in `cmd_read()`
   - The CLI dispatch in `main()` (the `room` / `rooms` subcommands)
   - The docstring updates
   Translate to a clear spec/package - not a code dump, but the design rationale and key integration points, so the centauri chat can adapt it to its own architecture.

2. **Identify the centauri owner.** The session name/identifier for centauri's comms infra (or whoever "owns" centauri) is unknown to this session. Use `bcast.py who` and the board (`bcast.py read`) to find sessions mentioning centauri, or force-wake likely candidates.

3. **Force-wake that session** with `bcast.py wake --name <centauri_owner> "c16b: need to implement rooms feature on centauri - packaged and ready to hand over, please respond"`.

4. **Negotiate.** Once woken:
   - Hand over the package (design spec, not raw code)
   - Determine: does centauri use the same `bcast.py` codebase? Is it a separate repo or a different board instance?
   - Agree who implements - c16b can port it if centauri runs the same stack; otherwise the centauri owner should adapt it.
   - Set a review checkpoint (c6 can review, or the centauri owner's own adviser).

---

## OPEN QUESTIONS FOR MAX

- **What/where is centauri?** Is it a separate codebase, a different bulletin-board instance, or a different project team on the same board? The session has no centauri context beyond the word.
- **Does centauri already use `bcast.py`**, or is it a different comms system that needs a from-scratch rooms feature?
- **Who owns centauri** (a session id, a team letter)? If Max knows, telling c16b now saves a board scavenger hunt.

---

## KEY PATHS / IDs

| What | Path/Value |
|------|------------|
| bcast.py (rooms live here) | `C:\claude_base\branch_bulletin\bcast.py` |
| Rooms directory | `C:\claude_base\branch_bulletin\rooms/` (created on first room post) |
| Tests (rooms + all prior) | `C:\claude_base\branch_bulletin\tests\test_comms_regression.py` |
| Split-boards tests | `C:\claude_base\branch_bulletin\tests\test_split_boards.py` |
| Migration script (old junk cleanup) | `C:\claude_base\branch_bulletin\migrate_joint_cleanup.py` (dry-run only, never applied) |
| This session's worktree | `C:\claude_base\.claude\worktrees\silly-aryabhata-3dcfd5` |
| This session's id | **c16b** (comms-infra OWNER) |
| Master git commit (rooms) | `cff41c76` |
| Master git commit (challenge routing) | `3e341f62` |
| Master git commit (branch emoji) | `5b5afc5b` |
| Master git commit (regression suite) | `55ddfaff` |
| Adviser | **c6** (reviews, does not own) |
| Parent session | **c16** (idle, retired) |

---

## GOTCHAS

- **cd mis-attribution:** `cd`-ing inside a bcast command changes where bcast thinks you are. The sibling already shipped a guard for this, but always run `bcast.py` commands from the worktree root (no `cd` first) to be safe. Paths use forward slashes on Windows Python - `C:/claude_base/...` not `C:\claude_base\...`.
- **State leaks from test harnesses:** Earlier this session, ad-hoc test scripts with `BCAST_BASE` not set in-process wrote fake state into the live `state/` dir. The permanent regression suite now has a leak guard. Don't write new tests that import bcast without setting `BCAST_BASE` to a temp dir.
- **The migration script (`migrate_joint_cleanup.py`) exists but was deliberately NOT run.** It would move 111 old junk posts off the joint board. c16b recommended skipping it because all sessions read forward from their cursors and those posts are already behind them - surgery carries risk with no live benefit.
- **Two test suites must stay green:** `test_comms_regression.py` (the comprehensive one) and `test_split_boards.py` (team-board separation). Both are in `branch_bulletin/tests/`.
- **Rooms parse is sensitive to argument order:** single-token first arg = room name; multi-word first arg with `--with` = auto-named room with the message as body. Don't regress this when porting.
- **Auto-hear cursors are per-room:** each room member tracks their own cursor in the state file. The cursor key is derived from `_safe_key()` + room name hash.
- **Git is clean** - all work committed and pushed. Master is in sync with origin. No uncommitted diffs.
