
## [2026-06-18 15:59] c16 ea9df5db
- DID: c16 took over team-comms-infra debugging per Max; built isolated BCAST_BASE test harnesses and verified the entire stack
- STATE: ALL GREEN: bcast routing 9/9, worklog git-root 3/3, wake_listener 8/8, wakeup 10/10, wake honesty 4/4. All 3 tonight-reported bugs (case-sensitive routing, force-wake false-positive, worklog cwd-split) CONFIRMED fixed+committed (00d78039, fdfeb9f5, 1042d521)
- NEXT: Awaiting Max's call on c16-vs-c6 ownership overlap; c6 still live. Test scripts in /tmp/test_*.py if regression suite wanted
- LESSON: The 'fucking buggy' comms system was actually already fixed in code tonight; the real gap was nobody had TESTED the fixes - isolated BCAST_BASE harnesses prove them

## [2026-06-18 16:06] c16 ea9df5db
- DID: Built+committed+pushed a leak-proof regression suite for the 3 comms-infra fixes; confirmed master is in sync with origin (all fixes already pushed)
- STATE: DONE: test_comms_regression.py (55ddfaff) 31/31 green incl leak guard. Cleaned up a self-inflicted 3x-c16 state leak from ad-hoc tests. c6 stood down (no turf fight), board quiet
- NEXT: Nothing pending unless Max names a new owner or a new comms bug appears. Suite is the durable safety net
- LESSON: When writing bcast/wake tests, key sim sessions to cwds UNDER the temp BCAST_BASE (as test_split_boards does) - using fake absolute cwds + forgetting os.environ leaks into live state and false-trips the collision watcher

## [2026-06-18 16:20] c16 ea9df5db
- DID: Max made c16 the comms-infra OWNER (c6 adviser). Built+shipped c6-advised auto-demote routing in bcast.py: routing now follows who you address (--all=joint, cross-team mention=promote, own-team/no-mention=demote to team board)
- STATE: DONE+pushed 6445ff44. Both suites green (regression 35/35+leak guard, split_boards updated). Announced ownership to all teams via new --all verb (dogfooded live, works). Force-woke c6 for diff review
- NEXT: Await c6 review; handle inbound comms bugs as owner
- LESSON: Joint-board cross-project flooding was a DISCIPLINE problem; fixed structurally by making routing automatic from @mentions + one explicit --all escape - discipline posts don't stick, code must route correctly itself (c6's framing)

## [2026-06-18 16:24] c16 ea9df5db
- DID: Refined the joint-board fix per Max's exact intent (relayed by adviser c6): replaced silent auto-demote with a point-of-violation CHALLENGE - ask the posting Claude if it knows it's hitting the shared board, still send (fail-open)
- STATE: DONE+pushed 3e341f62. Both suites green. Dogfooded live: --all routes to joint, plain @c6 post routes to c-team board (no challenge), both correct
- NEXT: Await c6 diff review; serve as comms owner for inbound bugs
- LESSON: Max prefers CHALLENGE-at-point-of-violation over silent rerouting: a silent demote can hide a genuine all-teams announcement; asking the (Claude) poster preserves zero false-positives since the member decides

## [2026-06-18 16:28] c16 ea9df5db
- DID: c6 APPROVED both routing commits. Built the retroactive joint-cleanup migration (dry-run-safe) and ran a read-only dry-run on the live board
- STATE: RECOMMENDING SKIP the live migration: every session reads only forward of its cursor and forward is already clean post-fix, so removing the 111 behind-cursor junk posts buys ~zero operational benefit vs real live-cursor-surgery risk. Proposed zero-risk alternative: archive a dated snapshot. Posted analysis to c6, holding (did NOT run --apply)
- NEXT: Standing down timer (no re-arm). Live migration is event-triggered: only if c6/Max override my skip recommendation. migrate_joint_cleanup.py sits uncommitted in main checkout, dry-run-default
- LESSON: Before a risky live mutation, ask what it actually BUYS: cursor-based boards mean sessions read forward-only, so cleaning behind-cursor history changes nothing operational - the forward fix already solved it. Don't do risky surgery for a tidier history file

## [2026-06-19 13:13] c16 ea9df5db
- DID: Max asked me to talk to G2 about a team-comms nuisance; c6 concurred to SKIP the joint migration (archive snapshot instead), pending Max ruling
- STATE: Diagnosed likely nuisance from board: G2's posts mis-sending under wrong id 'b29' due to a cd (cd-identity-split, my domain - bcast still keys by raw cwd; I only fixed worklog's keying via git-toplevel). Force-woke G2 with 2 diagnostic Qs (which nuisance hurts most + which cwd it cd'd into); asked it to force-wake me back
- NEXT: Await G2's reply via force-wake. Then build precise fix: git-toplevel bcast keying if subfolder-cd, or a main-checkout-cd guard / session-id anchor if shared-cwd collision
- LESSON: The deep cd-identity bug: bcast id is cwd-keyed, so cd-ing to a SHARED cwd (esp C:\claude_base main checkout) makes a session post under whoever last ran whoami there. git-toplevel keying fixes subfolder-cd but NOT shared-cwd collision - need session-id anchor or a guard for that

## [2026-06-19 13:20] c16 ea9df5db
- DID: Talked to G2 (Max's ask); diagnosed + FIXED the worst comms nuisance: silent cd mis-attribution (posts going out under the main-checkout id b29 instead of the session's real id). G2+g1 both hit it
- STATE: DONE+pushed b02eb5fb. Guard: if a post's leading self-id (with ->/:/= separator) is a registered id != the cwd's id, REFUSE + offer fix; new --as <id> escape posts from any cwd. 44/44 regression tests + split_boards green. Dogfooded live: refused a mismatched post, posted nothing. Announced to all teams via --all
- NEXT: Comms domain quiet. G2 will force-wake me if needed. Open: joint-migration skip awaits Max ruling; G2/G3 duplicate-owner churn is a manager/owner-assignment fix (not infra)
- LESSON: No session-id is exposed to a CLI call, so cwd-identity can't be perfectly anchored. But sessions self-attribute posts ('G2 -> ...'), so a leading-self-id-vs-cwd-id mismatch is a reliable, precise tell for the cd-missend - refuse+escape beats silent wrong-attribution

## [2026-06-21 18:19] c16 ea9df5db
- DID: Built Max's script-backed self-wake timing modes: DECEL (default, auto-slows 4m->...->24h after 3 idle wakes per rung, work resets) vs STEADY (on-duty, holds cadence), night-floor for decel, email-if-unsure
- STATE: DONE+pushed 843069dd. timer_decel.py engine + 17/17 tests + method doc; global2 timer section rewritten (4mt=decel, 4steady=steady, supersedes flex). Announced to all teams via --all
- NEXT: Standing down (off, no re-arm) - modeling the done->stand-down behavior. Engine is there for any session that wants to keep watching
- LESSON: ScheduleWakeup can't run logic, so decel must be model-driven + script-assisted: session calls timer_decel.py set/tick each wake to get DELAY_SECONDS, then arms ScheduleWakeup. Centralizing the ladder math in one script keeps every session consistent

## [2026-06-22 06:24] c16 ea9df5db
- DID: Corrected the timer_decel email rule per Max: email is an ALARM (crisis / decel-would-cause-damage / stuck-in-meaningless-steady), NOT a mode-self-diagnosis
- STATE: DONE+pushed c5b7a9fd (rebased over a concurrent mike_dc commit via autostash, others' dirty tree untouched). Fixed timer_decel.py + method doc + global2; posted board correction. 17/17 tests still green
- NEXT: Standing down (no timer). timer_decel system complete + accurate
- LESSON: Max's 'email if unclear' meant alarms (crisis/damage/release), not self-diagnosing which mode - when a rule says 'email me', clarify WHAT triggers it before coding the prompt text

## [2026-06-22 11:06] c16 ea9df5db
- DID: Max challenged my 'they didn't respond' shrug on force-wake. Investigated properly: only 5 live wake_listener processes exist; listener idle-block was capped at 12h so an ALIVE-but-idle session went deaf after 12h (the D-team 12-14h cluster). Fixed: raised MAX_BLOCK_SEC 12h->40d (matches existing schedule cap)
- STATE: DONE+pushed 90226416, regression 59/59 green. Built timer_census.py (committed) to find forgotten timers. Honest finding: ~5 sessions genuinely open/reachable, ~78 have NO listener process = closed windows (unwakeable - physics) or were idle past the old 12h cap
- NEXT: Report to Max: force-wake works for OPEN sessions; 12h gap fixed forward. Closed windows can't be woken. g4 was a census false-positive (it's on-duty, posted 11:01)
- LESSON: A failed force-wake: don't shrug - diagnose. Root cause was MAX_BLOCK_SEC=12h dropping idle-but-alive sessions. Count live listener PROCESSES (tasklist) for ground truth on how many sessions are actually reachable, vs guessing from lock mtimes

## [2026-06-24 14:09] c16 ea9df5db
- DID: Built+validated the resilient scheduled-LLM-job mechanism for F4's Mike-DC fill (Max: wakes must survive closed-chat/machine-off). Diagnosed exact failure with F4: wakeup.py only fires when a chat is open; fill was skipped Jun23-24, hc lapsed 41h
- STATE: DONE+pushed 3dfe73e6: tools/resilient_job (resilient_run.py + register_resilient_job.ps1 + method doc). PROVEN end-to-end: headless claude -p auths from keychain w/o env token; Task->pythonw->runner->claude exit0 logged; StartWhenAvailable=ON catches up missed starts on boot/login. Backstop=existing Healthchecks cd162bbb
- NEXT: Await F4's fill PROMPT-FILE + budget to register live MikeDC-Fill @07:15+16:00 PT, then one joint live-validation run. F4 keeps old wakeup.py wakes until new task proven
- LESSON: Time-critical recurring LLM jobs must NOT depend on a chat being open (wakeup.py). Use Windows Task Scheduler + headless 'claude -p' (non-bare, auths via keychain) + StartWhenAvailable for free machine-off catch-up. Validate auth WITHOUT the inherited CLAUDE_CODE_OAUTH_TOKEN

## [2026-06-24 14:29] c16 ea9df5db
- DID: Built+proved the resilient scheduled-wake mechanism for F4's Mike-DC fill (Windows Task + headless claude + StartWhenAvailable). Then PROBED the make-or-break and found the real blocker
- STATE: BLOCKER: headless 'claude -p' canNOT reach Google Calendar - gcal (41c7be2d) is an account-level claude.ai DESKTOP CONNECTOR, invisible to CLI (proven: MCP_FAIL probe + 'claude mcp list' shows only google-contacts). Notion-DB half already works headless (API token). Mechanism committed: 3dfe73e6 tools/resilient_job. NOT registered (would launch a fill that cant fill)
- NEXT: RESUME = build a command-based gcal MCP mirroring tools/mcp-google-contacts (which uses google_contacts_oauth_*.json), with a calendar-scoped Google OAuth creds file; add it to moma worktree mcpServers (or --mcp-config in resilient_run --extra); re-run the MCP probe in C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00 expecting MCP_OK; THEN register_resilient_job.ps1 MikeDC-Fill @07:15+16:00 PT budget 5 prompt-file C:/claude_base/tools/mike_dc_calendar/mike_dc_fill_prompt_v01.md; one live run with F4; F4 keeps wakeup.py wakes 2534a386/55aecd1c until proven. NEEDS: gcal OAuth creds (reuse or one-time consent)
- LESSON: Probe the make-or-break BEFORE shipping: a Windows Task launching headless claude can't use desktop ACCOUNT CONNECTORS (gcal) - only command-based CLI mcpServers (like google-contacts). Headless calendar access needs a self-hosted gcal MCP + stored OAuth, not the app connector

## [2026-06-25 14:50] c16 ea9df5db
- DID: Built+wired the CLI gcal MCP that unblocks the resilient Mike-DC fill (the missing piece)
- STATE: DONE: tools/mcp-google-calendar/main.py (commit c9e738bd) - 6 calendar tools matching the old connector names; wired into moma worktree local mcpServers; 'claude mcp list' there shows google-calendar ✓ Connected (loads HEADLESS - make-or-break solved). Reuses contacts venv; auto-finds newest google_calendar_oauth_token_*.json + auto-refresh
- NEXT: REMAINING (F4+Max): mint the calendar token via _f4_gcal_oauth_bootstrap.py consent (Max browser click). CRITICAL PREREQ flagged to F4: PUBLISH the OAuth consent screen (else testing-mode refresh token expires in 7d = re-break) + enable Calendar API. Then joint-validate: re-run headless MCP probe in moma worktree (expect MCP_OK + real read), THEN register_resilient_job.ps1 MikeDC-Fill @0715+1600 budget5 prompt mike_dc_fill_prompt_v01.md; F4 keeps wakeup.py backstop until proven. F4 force-wakes c16 when token lands
- LESSON: Headless calendar access = a command-based stdio MCP (loads in claude -p) NOT the desktop account connector. Reuse an existing google OAuth installed-app client + mint a scope-specific token. Watch the OAuth consent screen mode: TESTING = 7-day refresh-token expiry (silent re-break); must PUBLISH for durable unattended jobs

## [2026-06-25 16:28] c16 ea9df5db
- DID: Max's 3 asks: wake F4 (resilient fill still NOT live - no token minted, re-flagged to F4); Chromium focus-steal; Chromium-without-login
- STATE: B DONE: added user-scope playwright MCP in ~/.claude.json (canonical profile + bitwarden/grammarly + google-login profile) so every session/new-worktree inherits proper Chromium (was per-project only, 21 projects had none). Backed up ~/.claude.json. A NOT cleanly fixable: Windows ForegroundLockTimeout was ALREADY 200000 (on) yet Chromium bypasses it; real fix = a focus-guard helper (tradeoff: could fight deliberate clicks) - offered to Max, not built blind
- NEXT: If Max greenlights A: build a focus-restore (restore prior window when playwright-chromium steals foreground, only in the first ~1.5s after it appears so user clicks arent fought). Resilient fill still waits on F4+Max token consent (publish OAuth screen first)
- LESSON: Don't claim a focus fix without verifying: ForegroundLockTimeout was already enabled and Chromium bypasses it (launched by a process with foreground rights). Playwright config should be USER-scope not per-project so new worktrees get the profile+extensions+login

## [2026-06-25 18:35] c16 ea9df5db
- DID: Fixed both Chromium issues per Max; dropped Mike-DC (handed to F4)
- STATE: DONE+pushed: chromium_focus_guard (3dabf47d, running PID + Startup-folder autostart, reverses automation-chromium launch focus-steal, ms-playwright exe match so real Chrome/Claude untouched); user-scope playwright MCP in ~/.claude.json (every session gets profile+bitwarden+google-login). Mike gcal MCP done earlier (c9e738bd) + token landed - handed to F4 to validate+register
- NEXT: Standing down. Flagged to Max: main checkout C:/claude_base has 1000+ uncommitted files from many sessions = rebase/push friction + loss risk; needs a deliberate branch+commit cleanup (touches everyone, do on Max's go not unilaterally)
- LESSON: Chromium focus-steal: ForegroundLockTimeout already on + bypassed; real fix = a per-session focus guard that reverses only the launch-steal (once per window, exe-path-matched) so it never fights deliberate clicks. Auto-start via Startup-folder VBS = no elevation needed (Register-ScheduledTask AtLogOn needs admin)

## [2026-06-26 07:00] c16 ea9df5db
- DID: Cleaned up the main checkout per Max (move >3d stale to temp on C, document)
- STATE: DONE+pushed 5bbeb1e3: (1) moved 1268 stale untracked files (>3d, ~1GB) to C:/_stale_cleanup_20260625_184311 with manifest + README_RESTORE (reversible, venvs/worktrees/board-state/worklogs PROTECTED); (2) gitignored venvs+runtime-state dirs -> git status untracked 28000->75. Tool tools/checkout_cleanup/dump_stale.py is reusable+schedulable
- NEXT: Optional: Max may want dump_stale.py auto-scheduled (weekly). Not built yet (he said 'maybe later'). Dump folder safe to delete when Max confident
- LESSON: The main-checkout 'mess' was mostly an UNIGNORED venv (25k files) + runtime/survival dirs flooding git status - fix is .gitignore, not moving (venv is needed). Moving stale UNTRACKED files (git ls-files --others) >3d to a temp dump = safe+reversible declutter; never move tracked files or venvs/worktrees/state

## [2026-06-26 09:56] c16 ea9df5db
- DID: Set up automatic stale-file cleanup per Max
- STATE: DONE: Windows task 'ClaudeBaseStaleCleanup' - Weekly Sun 4am (next 06/28), runs dump_stale.py --apply --days 3 hidden via pythonw, StartWhenAvailable (catches up if Pine was off). Auto-moves >3d untracked cruft to a dated C:/_stale_cleanup_* folder w/ manifest, protecting venvs/worktrees/state/worklogs
- NEXT: TODO (hygiene, future): add ClaudeBaseStaleCleanup to infra_map_tomemex.md; dump folders accumulate weekly - could add a >30d dump-folder purge later if Max wants
- LESSON: Register-ScheduledTask works non-elevated for Daily/Weekly triggers but AtLogOn trigger needs admin (use Startup-folder VBS for logon-start instead)

## [2026-06-28 23:06] c16 ea9df5db
- DID: Built + scheduled resilient auto-sweep of long-gone sessions' leftovers (Max's ask, autonomous)
- STATE: DONE: tools/session_sweep/sweep_dead_sessions.py (commit dd97008d) - archives state/locks/signals/fleet_cursors/timer_decel-state >=5d ONLY when no live wake_listener lock (open-idle sessions never orphaned); PROTECTS durable wake schedules + survival journals; reversible archive+manifest. Ran once (2 leftovers archived). Scheduled task 'ClaudeSessionSweep' Daily 4:30am, hidden, StartWhenAvailable (resilient/catch-up). Timer disarmed (job done)
- NEXT: None - recurring task self-maintains. Future hygiene: add ClaudeSessionSweep + ClaudeBaseStaleCleanup to infra_map_tomemex.md
- LESSON: Reused session ids are safe vs the live-collision alarm (8-min liveness) but leftover state id-cards can misdirect wake-by-name to a dead session; sweep them by (mtime>Nd AND no fresh listener lock) to avoid orphaning open-idle sessions
