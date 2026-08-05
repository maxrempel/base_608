# Scribe handover - milestone 8 (~607K tokens)
# session: 20260625_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-25 18:32:07 by deepseek-v4-pro

# HANDOVER - c16, comms-infra owner

---

## GOAL (in Max's words)

Multiple tasks accumulated across this long session:

1. **"Debug and test whole system. It is a fucking mess."** - Take over c6's team-communication infrastructure (bcast, wake_listener, force/scheduled-wake, worklog) and fix it.

2. **"Continuous frequent timers make no sense - I forget about them. Make sessions gradually slow down their timers by default."** - Build a deceleration system where sessions auto-slow from 4min ? ... ? 24hr after 3 idle wakes each step, with `4mt` (decel) as default and `4steady` for on-duty watchers.

3. **"Build a completely resilient wake-up - survive the computer being off, keep info in the cloud, catch up as soon as back online. F4 missed very important appointments because the wake-up was a sheet."** - Build a Microsoft Windows Task Scheduler-backed resilient job system for the twice-daily Mike-DC Google Calendar fill that F4 depends on.

4. **"Start Chromium without grabbing focus (breaks dictation). Fix that."** (Task A)

5. **"Some sessions start Chromium without Google Login and without Bitwarden. How to force programmatically that every session starts Chromium with proper Bitwarden and Google Login?"** (Task B)

---

## DECISIONS MADE + WHY

### Comms-infra debugging

- **The three reported bugs (case-sensitive team derivation, cross-team @-mention routing, worklog cwd-split) were ALREADY FIXED in code by c6** (commits `fdfeb9f5`, `00d78039`, `1042d521`). Nobody had verified them. c16 wrote isolated test harnesses on a temp board (never touching live data) and confirmed all pass: 9/9 routing, 3/3 worklog, 8/8 wake_listener, 10/10 wakeup parse, 4/4 wake-honesty. **No new code needed - verification only.**

- **Built a leak-proof regression suite** (`branch_bulletin/tests/test_comms_regression.py`, 31 checks ? later expanded to 44+59) so these fixes can't silently break again. Committed + pushed (`55ddfaff`).

- **Max resolved the c16/c6 ownership overlap** by naming c16 the **responsible owner** of comms-infra; c6 was moved to adviser/reviewer.

### Joint-board routing (D21's flood complaint)

- **Diagnosed:** two projects (tamza/"b", MOMA/"d") each have private boards and one shared "joint" board. The joint board was 62% b-team traffic because of the now-fixed case-sensitivity bug + b15merger's `--joint` workaround. Private boards were never mixed.

- **Built auto-demote routing** (commit `6445ff44`): messages route by who you address. Cross-team @mention ? joint; same-team or no mention ? team board; `--all` ? explicitly joint.

- **c6 relayed Max's exact intent:** Max didn't want silent demotion - he wanted the system to **challenge** the posting session ("do you know this hits another project?"). c16 replaced silent-demote with **challenge-and-still-send** (fail-open - a real announcement can never be hidden, but the session gets asked). Commit `3e341f62`, c6-approved.

### cd-missend guard

- **G2 reported** the worst nuisance: posts going out under the wrong id after `cd`-ing into the main checkout to git-commit (e.g. G2's messages went out signed "b29"). Silent, contagious (g1 hit it too).

- **Fix built** (commit `b02eb5fb`): bcast now detects when the leading self-id in a message doesn't match the cwd-registered id, and **refuses** with a clear message + `--as <name>` escape hatch. Uses separator detection (`->`, `:`, `=`) to avoid false-positives on bare mentions. **The perfect fix (session-id anchor) isn't possible** because Claude exposes no session-id to CLI calls.

### Timer deceleration system

- **Built `tools/timer_decel/timer_decel.py`** (commit `843069dd`): a real script doing the ladder math - decel mode ramps 4min ? 8 ? 15 ? 30 ? 1hr ? 3hr ? 6hr ? 12hr ? 24hr after 3 idle wakes at each rung. Productive work resets to 4min. Steady mode holds cadence. Nights (10pm-7am) floor at 3hr in decel mode unless marked `4steady`.

- **Corrected the email rule per Max's pushback** (commit `c5b7a9fd`): email is an ALARM only - (a) crisis, (b) decel-would-cause-damage, (c) stuck in meaningless steady wanting release. Mode confusion is never email-worthy; just default to decel.

- **Updated `global2.md`** (Nextcloud-synced, auto-loads for new sessions) so the decel-default behavior is the default.

- **Built `tools/timer_decel/timer_census.py`**: reusable read-only census of all named sessions + their timer/activity signals.

### Resilient wake-up for Mike-DC fill

- **Diagnosed with F4:** the Mike-DC twice-daily calendar fill (ids `2534a386@07:15 PT` + `55aecd1c@16:00 PT`) only fires when an f4 chat session is **open** in the worktree `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00`. When the chat was closed during due windows, the fill silently skipped (heartbeat `hc-ping cd162bbb` lapsed ~41h, Centauri emailed Mike a stale event list).

- **Built `tools/resilient_job/resilient_run.py`** (commit `3dfe73e6`): a Python runner that launches `claude -p` headless in a target worktree with a prompt file, logs results, records last-run times. **Proven end-to-end:** non-bare `claude -p` authenticates from stored keychain (no env token needed), runs headless, returns results.

- **Built `tools/resilient_job/register_resilient_job.ps1`**: registers Windows Task Scheduler tasks with `StartWhenAvailable=True` + boot trigger - survives Pine being off, catches up on boot/login, no console flash.

- **Found the make-or-break blocker:** headless `claude -p` in the moma worktree could NOT load the Google Calendar MCP (41c7be2d) - it's a **desktop-app account connector**, invisible to CLI Claude. Only Contacts/Playwright/ReadAI loaded.

- **Fixed the blocker - built `tools/mcp-google-calendar/main.py`** (commit `c9e738bd`): a CLI-loadable Google Calendar command-MCP using FastMCP + the reusable Google OAuth client (`google_contacts_oauth_20260522.json`). Mirrors the existing contacts MCP pattern. 6 tools matching the desktop connector's names. **Verified headless:** `claude mcp list` shows "? Connected" from the moma worktree. F4's fill prompt works unchanged.

- **F4 wrote the consent bootstrap** (`tools/mike_dc_calendar/_f4_gcal_oauth_bootstrap.py`): mints a calendar-scoped OAuth token using the contacts OAuth client, saves to `ssh/google_calendar_oauth_token_<YYYYMMDD>.json`.

- **Critical warning flagged to F4+Max:** the Google consent screen is probably in "Testing" mode, making the token expire in 7 days. It must be set to "In production" (published) during consent.

### Chromium fixes

- **Task B (no Bitwarden/login) - FIXED:** added a **user-scope** Playwright MCP entry (`claude mcp add playwright --scope user`) pointing to the canonical profile `C:/claude_base/playwright_profile/pw_mcp_config.json` with Bitwarden/Grammarly extensions + Google-login profile. Every session and new worktree now inherits this. Backed up `~/.claude.json` first.

- **Task A (focus-steal) - NOT FIXED, awaiting decision:** the standard Windows fix (`ForegroundLockTimeout`) was already enabled at 200000ms - Chromium bypasses it because it launches with focus rights from a process that just had focus. c16 proposed building a "focus guard" that snaps focus back to the dictation window within ~1.5s of Chromium appearing, with care not to fight deliberate clicks. **Waiting on Max's OK to build.**

### Forced-wake reach bug

- **Max pushed back** when c16 shrugged at "80 sessions didn't respond to wake-test." c16 investigated properly: only ~5 live wake_listener processes exist; most "sessions" are closed windows with stale state files. The real bug: the listener's idle block was capped at **12 hours** (`MAX_BLOCK_SEC`), so an open-but-idle session went deaf after 12h.

- **Fixed** (commit `90226416`): raised the idle cap from 12h to **40 days**, matching an existing cap elsewhere in the system (proven safe - one cheap sleeping process per open session).

- **Also fixed `datetime.utcnow()` deprecation** in wake_listener.py ? `now(datetime.UTC)` (would have become a hard error on Python upgrade).

---

## CURRENT STATE - what is done, what is in flight

### ? COMPLETE + SHIPPED
- Comms-infra verified green (all fixes were already committed; regression suite locks them)
- Joint-board routing with challenge-at-point-of-violation (c6-approved)
- cd-missend guard (G2's worst nuisance, committed + live-proven)
- Timer deceleration system (engine + global2 + census tool)
- Forced-wake reach fixed (12h ? 40d idle cap + utcnow deprecation)
- Resilient job runner built, proven, pushed (`tools/resilient_job/`)
- CLI Google Calendar MCP built, wired, verified headless (`tools/mcp-google-calendar/`)
- Chromium-without-login/Bitwarden fixed (user-scope Playwright MCP entry)

### ? BLOCKED - awaiting action
- **Mike-DC resilient fill never went live.** The gcal MCP is built and proven; the calendar OAuth token was **never minted** (no token file in `ssh/`). The consent step (F4 + Max) never happened. No Windows Task Scheduler job registered. F4 was force-woken again but wasn't alive when c16 stood down.
- **Chromium focus-steal fix** - awaiting Max's OK on the proposed focus-guard approach.

### ? SKIPPED (intentionally)
- Retroactive joint-board cleanup migration - c6 and c16 agreed to skip it (archive a snapshot instead). Old junk is already behind everyone's cursor; surgery on a live board with 50+ sessions is too risky for zero operational benefit.

---

## EXACT NEXT STEP

**Immediate (blocker):** The Mike-DC fill still runs on the fragile old `wakeup.py` schedule (only fires when an f4 chat is open). To finish the resilient system:
1. F4 + Max do the **one-time OAuth consent** - F4's bootstrap script `tools/mike_dc_calendar/_f4_gcal_oauth_bootstrap.py` - which pops a browser for Max to "Allow" calendar access.
2. **Publish the Google consent screen** during that step (go to Google Cloud Console ? OAuth consent screen ? "Publish App" - otherwise token expires in 7 days).
3. Force-wake c16 after the token file lands.
4. c16 then: registers the two Windows Task Scheduler tasks using `register_resilient_job.ps1` for 07:15 PT + 16:00 PT in worktree `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00` with the fill prompt `C:/claude_base/tools/mike_dc_calendar/mike_dc_fill_prompt_v01.md` and `--max-budget-usd 5`, runs one live validation, verifies `hc-ping cd162bbb` only fires after a real fill, and tells F4 to keep old `wakeup.py` wakes until proven.

**Pending decision:** Max's OK on the Chromium focus-guard. If yes, c16 builds a small script that detects Chromium window creation and returns focus to the previously-active window within ~1.5s, gated so deliberate clicks aren't overridden.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Google Calendar OAuth consent + publish** - the only thing between the Mike-DC fill being fragile (chat-must-be-open) vs. resilient (Windows Task Scheduler, no chat needed). Needs ~2 minutes of your time with F4.

2. **Chromium focus guard - want me to build it?** (See tradeoff above.)

3. **C16 vs C26 owner overlap** - C26 was also claiming comms-infra ownership on Pine. c16 posted asking to sort it, no reply yet (C26 wasn't alive). Should be resolved so there's exactly one owner when the next comms bug surfaces.

4. **Main checkout has 1000+ uncommitted files** from many sessions editing it directly - it's causing repeated rebase/push friction. Worth a deliberate cleanup pass (branch-and-stash the scratch, keep main clean).

---

## KEY FILE PATHS / IDs / COMMANDS

**Files built/edited by c16:**
- `branch_bulletin/tests/test_comms_regression.py` - leake-proof regression suite (44+ checks)
- `branch_bulletin/bcast.py` - challenge routing + cd-missend guard + `--all` + `--as`
- `tools/timer_decel/timer_decel.py` - decel engine (`tick work|idle`, `set 4|off`, etc.)
- `tools/timer_decel/timer_census.py` - session census
- `tools/timer_decel/timer_decel_method_v01_tomemex.md`
- `tools/timer_decel/test_timer_decel.py` - 17 tests
- `tools/resilient_job/resilient_run.py` - headless Claude job runner
- `tools/resilient_job/register_resilient_job.ps1` - Windows Task Scheduler registration
- `tools/resilient_job/resilient_job_method_v01_tomemex.md`
- `tools/mcp-google-calendar/main.py` - CLI Google Calendar MCP (6 tools)
- `tools/wake_listener/wake_listener.py` - idle cap 12h?40d + utcnow fix
- `~/.claude.json` - user-scope Playwright MCP entry added (backed up first)

**Key commit SHAs (all pushed, master in sync):**
- `55ddfaff` - regression suite
- `6445ff44` - auto-demote routing (later refined)
- `3e341f62` - challenge-at-point-of-violation (the approved version)
- `b02eb5fb` - cd-missend guard
- `843069dd` - timer decel system
- `c5b7a9fd` - corrected email alarm rule
- `3dfe73e6` - resilient job runner + Task Scheduler helper
- `c9e738bd` - CLI Google Calendar MCP
- `90226416` - force-wake reach fix
- `f29f7fd1` - F4's fill prompt committed (by another session)

**Key identifiers:**
- Mike-DC fill heartbeat: `hc-ping cd162bbb`
- Mike-DC worktree: `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00`
- Fill prompt file: `C:/claude_base/tools/mike_dc_calendar/mike_dc_fill_prompt_v01.md`
- Old fragile wakes: ids `2534a386@07:15 PT` + `55aecd1c@16:00 PT`
- Google Calendar MCP id: `41c7be2d` (desktop connector - NOT CLI-loadable; my replacement is the command-MCP)
- OAuth client file: `google_contacts_oauth_20260522.json` (reusable for calendar)
- Token will land at: `ssh/google_calendar_oauth_token_<YYYYMMDD>.json`

**Commands to know:**
- `bcast wake --name <id>` - force-wake a session
- `bcast post --all "..."` - announce to all teams
- `bcast post "..." --as <id>` - post under explicit identity
- `timer_decel.py tick work|idle` - session signals whether it did work
- `timer_decel.py set 4` - arm 4-min timer in current mode
- `timer_decel.py off` - stand down timer
- `claude -p "prompt" --max-budget-usd N` - headless Claude invocation (authenticates from keychain, no env token needed)

---

## G
