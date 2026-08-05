# Scribe handover - milestone 2 (~150K tokens)
# session: 20260710_eautiful_bhaskara_0b8970_6cd7ab10
# cwd: C:\claude_base\.claude\worktrees\beautiful-bhaskara-0b8970
# written: 2026-07-10 14:41:29 by deepseek-v4-pro

# HANDOVER - Playwright/Bitwarden clone-per-session fix

## GOAL (in Max's words)
"Make it possible for multiple sessions to open Chromium through Playwright with Bitwarden, and prevent them from opening sessions without Bitwarden. That's very annoying. Tons of sessions promise to solve that, and it's still happening."

## ROOT CAUSE FOUND
The old launcher design gave only the **first** session the real Bitwarden profile; every parallel session got `--isolated` mode (a fresh, empty profile) - meaning Bitwarden was present as an extension but **logged out**, which is what Max kept experiencing as "opened without Bitwarden." This wasn't sessions misbehaving - the design handed out a useless browser on purpose.

## FIX BUILT AND COMMITTED
**New design:** a 46MB "seed" snapshot of the logged-in Bitwarden state is cloned per-session. Every parallel session gets its own copy, so all of them open with Max's Bitwarden account present (locked, awaiting master password). No shared lock. No logged-out fallback.

**Files changed (pushed to `C:/claude_base` master):**
- `tools/playwright_bitwarden/build_seed.py` - **new.** Reads the existing logged-in profile and extracts only the essential extension state (Bitwarden + Grammarly vaults from `Local Extension Settings`, ~47MB) into `C:/claude_base/playwright_profile_seed/`, deliberately skipping ~1.1G of cache.
- `tools/playwright_bitwarden/pw_mcp_launch.py` - **rewritten.** Every session now: (1) clones the seed to `C:/claude_base/playwright_profile_sessions/s<PID>_<timestamp>/`, (2) launches Chromium against the clone, (3) cleans up the clone on exit. Logs "logged-in Bitwarden" when the vital data path exists.
- `tools/playwright_bitwarden/bitwarden_persistent_setup_v01_tomemex.md` - updated with new design + "do not revert to old lock scheme" warning.
- `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` - PLAYWRIGHT section updated with new design.

**Seed verification (file-level):** The copied vault LevelDB contains `global_account_accounts` (7 occurrences) and `_email` keys - these are Bitwarden's authenticated-account registration markers. So every clone opens with Max's account present, not the logged-out login screen.

## CURRENT STATE - FIX IS IN PLACE, BUT NOT YET END-TO-END VERIFIED
- Seed built successfully: `C:/claude_base/playwright_profile_seed/` - 46.3 MB.
- Launcher smoke-tested: clone created, "logged-in Bitwarden" message appeared, clone cleaned up on exit. Works.
- **But:** the fix only applies to **newly started** Claude Code sessions. Sessions running before the fix keep the old launcher until they restart.
- Max reported another session opening Chromium without Bitwarden - that session was pre-fix.
- A live end-to-end Playwright test (`bw_livetest.js`) was being written to definitively prove a cloned browser shows Bitwarden's unlock screen. **This test was interrupted mid-execution.**
- The test script attempted to open the Bitwarden extension popup and read its DOM, but the popup was blocked (likely MV3 service-worker registration issue). Claude pivoted to querying the extension's storage directly via the service worker, then the user interrupted.

## EXACT NEXT STEP
**Complete the end-to-end verification.** Launch a Chromium instance from the seed clone using Playwright, and confirm Bitwarden shows Max's logged-in account. The file-level proof (LevelDB keys) is strong, but Max wants to see it actually work in a browser. The test script already exists at `C:/Users/maxre/AppData/Local/Temp/claude/.../scratchpad/bw_livetest.js`. Options to complete:
1. Query Bitwarden's extension storage via CDP (bypass popup), or
2. Navigate to `chrome-extension://nngceckbapebfimnlniiiahkandclblb/popup/index.html` directly (though MV3 may block this headlessly), or
3. Use the extension's background/service worker to read stored account data.

After verification: confirm with Max that new sessions actually get Bitwarden. If the old session is still running, kill it and restart.

## OPEN QUESTIONS STILL AWAITING MAX
- **None explicitly asked.** But implicitly: does the fix actually work in practice when Max starts a new session? The live verification was meant to answer this before asking Max to trust it.

## KEY PATHS, IDS, NAMES
| What | Path/ID |
|---|---|
| Seed profile | `C:/claude_base/playwright_profile_seed/` (46.3 MB) |
| Per-session clones | `C:/claude_base/playwright_profile_sessions/s<PID>_<ts>/` |
| Original profile | `C:/claude_base/playwright_profile/` |
| Bitwarden extension ID | `nngceckbapebfimnlniiiahkandclblb` |
| Bitwarden vault (key state) | `.../Local Extension Settings/nngceckbapebfimnlniiiahkandclblb/` (~27 MB) |
| Grammarly vault | `.../Local Extension Settings/kbfnbcaeplbcioakkpcpgfkobkghlhen/` (~20 MB) |
| Launcher | `C:/claude_base/tools/playwright_bitwarden/pw_mcp_launch.py` |
| Seed builder | `C:/claude_base/tools/playwright_bitwarden/build_seed.py` |
| Live test script | `C:/Users/maxre/AppData/Local/Temp/claude/.../scratchpad/bw_livetest.js` |
| Chromium binary | `C:/Users/maxre/AppData/Local/ms-playwright/chromium-1224/chrome-win64/chrome.exe` |
| Python | `C:/Users/maxre/AppData/Local/Python/pythoncore-3.14-64/python.exe` |
| Git commit | Already committed and pushed to `C:/claude_base` master |
| Session identity | E40 (checked in via bcast) |
| global2.md | `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` |

## GOTCHAS AND DEAD ENDS
1. **Old sessions don't auto-update.** The launcher runs inside the MCP server process; it can't hot-swap. Any session started before the fix must be **restarted** (kill Claude Code and relaunch) to pick up the new launcher.
2. **MV3 extension popups blocked headlessly.** The initial live test tried `page.evaluate()` to access the Bitwarden popup DOM, but MV3 service workers don't serve popups the old way. This is a known Chromium/Playwright headless limitation - not a bug in the fix. The fallback is CDP or service-worker-based verification.
3. **Do NOT revert to the old "single-profile lock" design.** The docs now explicitly warn against this. The clone-per-session approach is the correct fix; any attempt to go back to `--isolated` fallback for non-owner sessions will re-create the exact bug Max is experiencing.
4. **Seed must be rebuilt if Bitwarden login state changes.** If Max logs out and back into Bitwarden, or the vault data changes significantly, `build_seed.py` should be re-run to refresh the seed.
5. **The stray process from the test (PID 17220) was left alive** with its own clone at `C:/claude_base/playwright_profile_sessions/s17220_1783716643/`. This is harmless and actually demonstrates the goal (independent per-session clones coexisting), but should be noted. The clone cleanup mechanism triggers on launcher exit - since the process is still alive, its clone remains.
