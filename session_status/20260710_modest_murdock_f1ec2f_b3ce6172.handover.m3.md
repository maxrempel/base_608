# Scribe handover - milestone 3 (~227K tokens)
# session: 20260710_modest_murdock_f1ec2f_b3ce6172
# cwd: C:\claude_base\.claude\worktrees\modest-murdock-f1ec2f
# written: 2026-07-10 13:49:18 by deepseek-v4-pro

# Handover for continuing work on bcast.py - chat rooms and board management

Max wanted a third communication layer under the board: **chat rooms**, for smaller subsets of a team to talk privately, with a deliberate "knock" to enter (not auto-loaded). He then asked to **remove the emoji-per-session** feature (painful for audio playback), then to **move entire teams into rooms** and **add a barrier** so roomed sessions can't post on the team/global board without confirming a whole-board reason. Finally he wanted the ability to **remove members from rooms** (self and others). This handover captures the implementation that was built, tested, and merged to master across those steps.

---

## GOAL (in Max's words)
- Implement "chat rooms" (sub?boards), three layers: global ? team board ? chat room.
- A chat room is like a board for a smaller subset. It must not be loaded automatically; members must "knock in" / "open the door" (explicit --read) to see content. There should be resistance, not default loading.
- Strip the emoji generator that assigns a visual icon to each session on registration - no emoji at all.
- A command to grab a whole team and move it into a room, runnable by anyone.
- A barrier: once sessions are in rooms, posting to the team or global board must be resisted unless it's a genuine whole-board item (shared resource, danger, or Max announcement). Un-roomed sessions still post freely.
- Room member removal - both removing others and leaving.

---

## DECISIONS MADE (and why)

### 1. Rooms already existed - changed to "knock-only"
- **Why:** The original `room` command auto?pushed the full message body into every member's per?turn context. That violated Max's rule "not loaded automatically, you knock in, with resistance".
- **What was done:** The per?turn injection now sends only a **knock** line, e.g. `room p1: 2 unread - open with --read`. The count persists until the member explicitly uses `--read`. This is the "resistance". Non?members get nothing.
- **Technical note:** The knock is cleared when the member reads (the tool writes a per?user last?read marker).

### 2. Emoji signatures stripped completely
- **Why:** Audio playback struggles with emoticons. Max wanted "nothing, just no emoticon whatsoever, just kill that whole little program".
- **What was done:** Removed the `SIG_POOL` (emoji characters) and the `_signature()` function from `bcast.py`. Also removed the "YOUR VISUAL SIGNATURE" line at registration and the per?turn "lead your reply with this emoji" reminder. Sessions now carry only their plain id (e.g. `G1B`).

### 3. `moveteam` command
- **Why:** Move an entire team into a room with a single command, from inside or outside the team.
- **Implementation:** `python bcast.py moveteam <team>` (alias `herd`). It reads all registered sessions for that team letter, creates the room (or adds to existing), logs a move?in announcement, and deletes the old team file to prevent future board auto?hearing for that team (though they still can listen if they explicitly re?register). Anyone can run it.

### 4. Board posting barrier for roomed sessions
- **Why:** Once roomed, sessions shouldn't casually post on the team/global board; they need a "genuine whole?board" reason (resource, danger, Max announcement).
- **Implementation:** In `cmd_post`, after the usual dust?gate and pollution checks, there's a new check: if the posting session belongs to any room, the post is **refused** with a question listing the three valid reasons. The session must re?post with `--announce` (a flag added to post) to override. Sessions **not** in any room post freely (the "1-2 sessions, no rooms" case). This effectively pushes small?group chatter into rooms.
- **Note:** The `--announce` flag is parsed only when the barrier fires; otherwise ignored.

### 5. Room member removal
- **Why:** Max wanted cleanup after rooms were created - stray members, session renames, and the developer's own presence.
- **Implementation:** Added `--remove <id>` (also `--rm`/`--kick`) and `--leave` to the `room` command. Works case?insensitively. For `--leave`, the current session's id is used from `whoami`. Updates the room's `members.json` and posts a removal notice.

### 6. Project rooms p1, p2, p3 populated
- **Why:** Max specified to put P1, P2, P3 team members into proper chat rooms.
- **Membership from board screenshot + live renames:**
  - **p1 (KENEFICK):** x5, X7A, X8A, X10A, x15b, X1D, X9A (the last was present from a sibling's previous creation; not removed because not definitely wrong).
  - **p2 (NPA):** X12B, X11B, X12C.
  - **p3 (OMEGA):** X21B (now 1P3), X21F, x1, X21C, X21D (now QP3), X21G.
- **Stray members cleaned:** Removed X21D (OMEGA) from p1, removed stale ids from p3. Developer G1B left all three rooms.

---

## CURRENT STATE
- **All features are implemented, tested (in isolated BCAST_BASE), and merged to `origin/master`** (commits `3c8d3a75` and `20e68535`).
- The live board at `C:\claude_base\branch_bulletin` now has:
  - Knock?only rooms (third layer).
  - No emoji on registration or in replies.
  - `moveteam` command available.
  - Board posting barrier for roomed sessions (with `--announce` override).
  - Room member removal (`--remove`, `--leave`).
- Project rooms p1, p2, p3 are populated and cleaned.
- Tests were updated (`test_comms_regression.py`) and pass for the new features (the 7-8 pre?existing routing failures are due to flaky DeepSeek pollution checks - unrelated).

---

## EXACT NEXT STEP
The immediate work (removal and cleanup) is **done**. However, two small loose ends remain that Max might want addressed:

1. **p1 has a case?duplicate:** `x5` and `X5` appear as separate entries because the tool treats them as distinct strings. Cosmetic, but could be cleaned up if Max prefers tidy lists.
2. **p1 contains `X9A`**, which wasn't on Max's original board screenshot. It was left because it might be a legitimate P1 helper. Needs a raise with Max to confirm if it should stay or be removed.

Beyond that, Max's last message was non?specific ("removal and other stuff, please continue"). The removal feature itself is built and used. The logical next step is to ask Max about the above two items, or to await further instructions.

---

## OPEN QUESTIONS AWAITING THE USER
- Should we deduplicate case?variations in room membership (x5 vs X5) automatically, or just clean up p1 manually?
- Does `X9A` belong in p1 (KENEFICK) or should it be removed?
- Is there any other "stuff" beyond room removal that Max wants done (e.g., a command to list all rooms, a way for Max to mass?move across projects, refinements to the barrier wording, etc.)?

---

## KEY PATHS, FILES, IDS, COMMANDS
- **Board tool:** `C:\claude_base\branch_bulletin\bcast.py`
- **Tests:** `C:\claude_base\branch_bulletin\tests\test_comms_regression.py`
- **Worktree used for editing:** `C:\claude_base\.claude\worktrees\kind-carson-2cc207\branch_bulletin\bcast.py` (the changes were then merged into the main checkout at `C:\claude_base`)
- **Live board base:** `C:\claude_base\branch_bulletin` (where `bcast.py` runs with default BASE directory, no `BCAST_BASE` override - the real board data)
- **Room commands (as of now):**
  - Create / add members: `python bcast.py room <name> --members <id1 id2 ...> ["welcome message"]`
  - Read room: `python bcast.py room <name> --read` (clears knock)
  - Remove member: `python bcast.py room <name> --remove <id>` (also `--rm`/`--kick`)
  - Leave room: `python bcast.py room <name> --leave`
- **Team move:** `python bcast.py moveteam <team_letter> [room_name]`
  - e.g., `python bcast.py moveteam g chat_g` - moves all registered sessions of team `g` into room `chat_g`
- **Post with announcement override:** `python bcast.py post --announce "message"`
- **Important session ids:** G1B (developer), x5/X5, X7A, X8A, X10A, X12B, X11B, X12C, 1P3, QP3, x1, X21F, X21G (among others)
- **Rooms:** p1, p2, p3 exist with the memberships listed above.

---

## GOTCHAS & DEAD ENDS
- The test suite's 7-8 "routing" failures are **pre?existing flakiness** from a non?deterministic DeepSeek pollution gate. They vary run?to?run with zero code change and are **not caused** by the new features.
- The commit history is slightly messy: the earlier batch of changes was inadvertently swept into a concurrent session's commit (`3c8d3a75`), but the code is intact and matches what was tested.
- When testing new bcast code, **always set `BCAST_BASE` to a temp directory** to avoid touching the live board. For example:
  ```
  export BCAST_BASE=$(mktemp -d)
  python bcast.py whoami
  ```
- The live board is in `C:\claude_base\branch_bulletin` with its data in `C:/claude_base/branch_bulletin/data/` (rooms, teams, global, sessions). Be careful with destructive commands like `moveteam` when connected to the real base - it will delete the team file; that's intentional and part of the design.
- The `room` command's help and the top?of?file docstring have been updated to reflect all new features, but the README might still need a refresh for the barrier and removal flags - the current handover writer didn't update README beyond the initial knock?only layer. It's a minor doc gap to be aware of.
