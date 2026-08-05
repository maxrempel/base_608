# Scribe handover - milestone 6 (~91K tokens)
# session: 20260610_modest_greider_7ab9ca_e9c92465
# cwd: C:\claude_base\.claude\worktrees\modest-greider-7ab9ca
# written: 2026-06-10 13:03:01 by claude-opus-4-8

# HANDOVER

## GOAL (in Max's words)
"Finally, kill the stupid popup." Max wants to permanently disable Chromium/Chrome's "Restore pages" crash-recovery bubble. Two prior sessions tried and failed. He pasted a generic how-to (launch flag `--hide-crash-restore-bubble`, editing the Preferences file's `exit_type`/`exited_cleanly`) and expects the assistant to **actually do** the fixes, not just explain them. His last message - "hm, i might have missed. try again" - signals that the explanation given so far did not land as a working result for him; he wants it tried again / made to actually work.

## DECISIONS + WHY
- **The popup comes from two separate Chromium installs, not main Chrome.** Investigation showed Max's everyday Chrome profile is fine and should stay fine (he wants page restore there). The popups come from:
  1. **Playwright's Chromium** (the MCP browser Claude Code drives) - launched with a persistent profile, killed uncleanly each run, so it shows the restore bubble "every time Claude Code uses chromium." This had **no** anti-restore flag.
  2. **MOMA's dedicated Chrome profile** - launched by a restart script.
- **Fix Playwright via a config file + flag passthrough.** Decision: give the Playwright MCP a config that injects `--hide-crash-restore-bubble` into its Chromium launch, wired into the Claude config so it loads at startup.
- **Leave main Chrome untouched** - MOMA and Playwright each use their own isolated profile, so the main profile keeps restoring pages as Max wants.
- **Clear the live "Crashed" state now** as belt-and-suspenders so the very next launch is clean, independent of the flag.
- **MOMA's canonical script is already correct.** `C:\moma\sc10\moma_restart.py` already passes `--hide-crash-restore-bubble` AND marks a clean exit. Conclusion: if MOMA still pops, an **older/stale copy** of that script is being launched (there are ~20 stale worktree copies).

## CURRENT STATE
Done:
- Wrote a Playwright MCP config file at `C:\claude_base\playwright_profile\pw_mcp_config.json` containing the `--hide-crash-restore-bubble` flag.
- Edited `C:\Users\maxre\.claude.json` to wire that config into the Playwright MCP server entry (project `C:/claude_base`, profile dir `C:\claude_base\playwright_profile`).
- Ran a Python snippet that cleared the `Crashed`/`exited_cleanly:false` state on **both** the MOMA profile and the Playwright profile.

In flight / not yet confirmed:
- The Playwright fix **only takes effect after Claude Code is restarted** (config read at startup) - not yet verified working.
- The MOMA puzzle is unresolved: which launcher fires the popup is unknown.
- Max's "try again" suggests he is **not satisfied** the popup is dead. It is unclear whether he restarted Claude Code, whether he's still seeing the MOMA popup, or whether the explanation simply didn't read as a completed fix.

## EXACT NEXT STEP
Re-engage on "try again." Do **not** just re-explain. Likely Max either (a) didn't restart Claude Code so the Playwright flag hasn't kicked in, or (b) is still hitting the MOMA popup from a stale launcher. Best move: ask the one disambiguating question (below) OR proactively verify both fixes are live - re-read `C:\Users\maxre\.claude.json` to confirm the config edit survived, confirm `pw_mcp_config.json` still holds the flag, re-check both profiles' Preferences are now clean, and find/fix the stale MOMA launcher. Then state plainly what is fixed and what action Max must take (restart Claude Code).

## OPEN QUESTIONS (awaiting Max)
- When MOMA pops the restore bubble - is it triggered by a **desktop shortcut/icon Max clicks**, or only when **Claude runs the restart script**? This identifies which old launcher to fix.
- (Implicit) Did Max restart Claude Code after the Playwright config change? If not, the Playwright popup will persist until he does.

## KEY PATHS / IDS
- Playwright MCP config (new): `C:\claude_base\playwright_profile\pw_mcp_config.json`
- Playwright persistent profile dir: `C:\claude_base\playwright_profile`
- Claude config (edited): `C:\Users\maxre\.claude.json` - Playwright MCP entry under project `C:/claude_base`
- MOMA canonical restart script (already correct): `C:\moma\sc10\moma_restart.py` (also `moma_refresh.py` in same dir)
- MOMA Chrome profile: `C:\Users\maxre\AppData\Local\moma_chrome_profile\Default`
- Main Chrome profile (do NOT touch): `C:\Users\maxre\AppData\Local\Google\Chrome\User Data\Default`
- The flag: `--hide-crash-restore-bubble`
- Preferences keys to neutralize: `"exit_type": "Crashed"` ? `"None"`; `"exited_cleanly": false` ? `true`

## GOTCHAS / DEAD ENDS
- The popup source was initially mistaken for regular Chrome - it is **not**. It's Playwright Chromium + MOMA's dedicated profile. Main Chrome is unrelated.
- There are **~20 stale worktree copies** of the MOMA scripts. The canonical `C:\moma\sc10\` copy is already fixed, so chasing it is a dead end - the live problem is an older copy somewhere being launched.
- The Playwright config change does **not** apply until Claude Code restarts. Easy to mistake for "didn't work."
- Clearing the `Crashed` state only fixes the *current* next launch; without the flag the bubble returns after the next unclean kill - hence both the flag and the clear were needed.
- Editing/locking Preferences as read-only (Method 2 in Max's paste) was NOT used here; the flag approach was chosen instead.
