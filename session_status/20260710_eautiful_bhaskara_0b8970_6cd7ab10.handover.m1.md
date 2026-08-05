# Scribe handover - milestone 1 (~139K tokens)
# session: 20260710_eautiful_bhaskara_0b8970_6cd7ab10
# cwd: C:\claude_base\.claude\worktrees\beautiful-bhaskara-0b8970
# written: 2026-07-10 13:54:53 by deepseek-v4-pro

# HANDOVER: Bitwarden-per-session fix for Playwright/Chromium

## GOAL (Max's words)
> Again, same problem, the sessions keep opening Chromium without Bitwarden. You have to make it possible for multiple sessions to open Chromium through Playwright with Bitwarden, and prevent them from opening sessions without Bitwarden. That's very annoying. Tons of sessions promise to solve that, and it's still happening.

Max wants **every parallel Claude session** that uses Playwright to launch Chromium with the real Bitwarden extension **logged-in** (account present, ready to unlock with master password). The existing design gave only the first session the real state; all others got a logged-out Bitwarden (useless). He wants that gone.

## DECISIONS MADE + WHY

- **Root cause**: The old `pw_mcp_launch.py` used a **single** profile (`C:/claude_base/playwright_profile`) with a lock mechanism: first session claims it and gets real Bitwarden; subsequent sessions get `--isolated` which creates a fresh empty extension environment, so Bitwarden appears **logged-out** (no account). That's the "without Bitwarden" he kept seeing.

- **New design**: **Clone-per-session** using a **seed profile** that contains the logged-in Bitwarden state. Every session copies that seed (46 MB) into its own temporary directory, launches with that clone, and deletes it on exit. No shared lock, no owner/loser split.

- **Seed creation**: Created `build_seed.py` that takes the existing master profile (`C:/claude_base/playwright_profile`) and copies only the essential logged-in state: the `Default/Local Extension Settings/nngceckbapebfimnlniiiahkandclblb` folder (Bitwarden vault, ~26 MB), plus `Default/Local Storage` and `Default/Sessions` (required for extension context). It skips ~1.1 GB of cache (Cache, Code Cache, Service Worker, etc.). The seed lives at `C:/claude_base/playwright_profile_seed` (46.3 MB).

- **New launcher**: Replaced `pw_mcp_launch.py` with version that:
  1. Copies seed ? `C:/claude_base/playwright_profile_sessions/s<pid>_<timestamp>`.
  2. Launches Chromium with `--user-data-dir=<clone>` and explicit `--load-extension=<bw_ext_path>`.
  3. On shutdown, deletes the clone (catches normal + signal exits).
  4. **No fallback to `--isolated`** - if seed missing, script fails with clear error.

- **Verification**:
  - Ran `build_seed.py` successfully.
  - Inspected vault leveldb: found `global_account_accounts` and `_email` strings ? confirms authenticated account marker is in seed.
  - Tested launcher manually: creates clone, logs "logged-in Bitwarden," cleans up on exit.
  - An existing stray clone from a live process (pid 17220) shows it works in parallel.

- **Documentation updates**:
  - Edited `global2.md` (Nextcloud synced) to replace old lock scheme description with new clone approach, including notes about seed rebuild if Bitwarden updates.
  - Edited `bitwarden_persistent_setup_v01_tomemex.md` to add warning not to revert to old lock scheme.

- **Commit & push**: All changes committed with message about fixing the recurring "without Bitwarden" bug, pushed to master.

## CURRENT STATE

- **Code deployed**: New `build_seed.py` and `pw_mcp_launch.py` are on disk and in git (`C:/claude_base/tools/playwright_bitwarden/`). Seed exists at `C:/claude_base/playwright_profile_seed` (~46 MB).
- **Behavior for new sessions**: Any new Claude session spawned after this commit will use the new launcher ? clone seed ? gets logged-in Bitwarden.
- **Sessions already running** (including current one) still use old launcher until Claude Code restarts.
- **Bitwarden extension ID**: `nngceckbapebfimnlniiiahkandclblb` (unchanged).
- **Master profile** (`playwright_profile`) still contains original large folder (1.2 GB) but is now only used as source for seed rebuilds; launcher no longer touches it.

## EXACT NEXT STEP

Max should **restart Claude Code** (or any session using Playwright) to pick up the new launcher. After restart, opening a browser via Playwright should show Bitwarden with the unlock screen (i.e., account present), not the login screen (no account). No further action required unless the problem recurs - in that case, the first check would be whether `playwright_profile_seed` exists and contains the vault.

## OPEN QUESTIONS (awaiting Max)

- None. Claude explicitly asked if he wanted to review the exact wording in global2, but that was not answered (the question was in the transcript but no response). However, the fix is done, so no blocker.

## KEY FILE PATHS / IDs / COMMANDS

- **Seed**: `C:/claude_base/playwright_profile_seed` (46.3 MB, never deleted)
- **Clone directory**: `C:/claude_base/playwright_profile_sessions/s<pid>_<timestamp>` per session
- **New launcher**: `C:/claude_base/tools/playwright_bitwarden/pw_mcp_launch.py`
- **Seed builder**: `C:/claude_base/tools/playwright_bitwarden/build_seed.py` (run if Bitwarden account changes)
- **Docs updated**: `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` and `C:/claude_base/tools/playwright_bitwarden/bitwarden_persistent_setup_v01_tomemex.md`
- **Extension ID**: `nngceckbapebfimnlniiiahkandclblb`
- **Chromium binary**: `C:/Users/maxre/AppData/Local/ms-playwright/chromium-1224/chrome-win64/chrome.exe`
- **Python**: `C:/Users/maxre/AppData/Local/Python/pythoncore-3.14-64/python.exe`

## GOTCHAS / DEAD ENDS ALREADY RULED OUT

- **Do NOT revert to old lock scheme**: The old single-profile with exclusive lock is what caused the bug. If someone tries to "re-optimize" by making sessions share one profile, they will reintroduce the problem. Seed cloning is the only design that works for parallel sessions.
- **MV3 popup in headless**: The session attempted to verify via opening a browser window to check Bitwarden popup, but headless mode can't show extension popups (known issue). Verification was done via leveldb string search instead, which is reliable.
- **No need to copy full profile**: The seed skips cache folders intentionally (1.1 GB). Copying only `Local Extension Settings`, `Local Storage`, and `Sessions` is enough for Bitwarden's logged-in state.
- **Master password still required**: The clone carries the encrypted vault, not an unlocked session. Max must enter master password each time to unlock. That's expected.
- **Seed rebuild**: If Bitwarden updates/rotates its extension data keys, or Max adds a new account, run `build_seed.py` again. The current seed was built from today's state.
- **Parallel clones coexist**: The transcript confirmed a live clone from pid 17220 when cleaning up, showing multiple sessions can run at once-each with its own clone - no conflict.
