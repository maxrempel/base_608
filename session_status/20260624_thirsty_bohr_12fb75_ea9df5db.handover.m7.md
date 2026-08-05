# Scribe handover - milestone 7 (~534K tokens)
# session: 20260624_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-24 14:25:40 by deepseek-v4-pro

# Handover for c16 (comms-infra owner, resilient-wake task)

## GOAL (Max's words)
Max demands a **100% resilient, idiot-proof scheduled wake?up** that survives the computer being off, keeps schedule in the cloud, and catches up ASAP when the machine returns. This was triggered because F4's twice?daily Mike?DC calendar fill missed two full days - Mike received stale events.

The immediate sub?goal is to make the Mike?DC fill fire reliably at ~07:15 and ~16:00 PT **regardless of whether any Claude chat window is open**; the old mechanism (`wakeup.py`) only fires when a session is alive in the specific worktree.

## DECISIONS + WHY
1. **Diagnosis confirmed:** F4's fill failed because the `f4` chat was closed during the due windows. The old `wakeup.py` schedule is strictly local-to-the-worktree and alive-session-dependent.  
   *Why:* This matches observations (worklog gaps, wakes advanced but didn't fire, Pine was on, no f4 session alive).  
2. **Chosen solution:** A **Windows Task Scheduler job** that launches a **headless `claude -p`** in the moma worktree, with `StartWhenAvailable` (catch?up on boot). This removes the "need a live chat" bottleneck.  
   *Why:* F4's fill requires LLM (research + calendar reasoning), so a pure?Python job can't do the real fill (only heartbeat coverage check). Task Scheduler is the most robust OS?level scheduler, and `claude -p` headless mode was proven to work (authenticates via stored OAuth keychain, exits cleanly).  
3. **Mechanism built and end?to?end validated:** `resilient_run.py` (the job runner), `register_resilient_job.ps1` (PowerShell helper to create the task), and the method doc are all committed (`3dfe73e6`). A full test chain (Task Scheduler ? pythonw ? runner ? headless claude ? "OK") succeeded.  
4. **Blocker discovered before live wiring:** Headless Claude **cannot use the Google Calendar MCP** because that MCP is a desktop?app connector, invisible to the CLI. The Notion side of the fill is headless?OK; calendar writes are the gap.  
   *Why I probed first:* I explicitly tested whether `claude -p` in the moma worktree sees the gcal MCP. It does not. This is exactly F4's make?or?break concern - registering a job that can't touch the calendar would be a false success.  
5. **Timer infrastructure delivered in parallel:**  
   - Timer deceleration system (`tools/timer_decel/`, global2 updated) - sessions default to "4mt" (decel) which slows wake?ups on idle; "4steady" for continuous duty.  
   - Force?wake reachability fix: idle block cap raised 12h ? 40 days.  
   - Census tool (`timer_census.py`) to spot forgotten idle sessions.  
   - Silent cd?misattribution guard in `bcast.py` (posts now require correct self?id).  
   All tested, committed, pushed.

## CURRENT STATE
- **Resilient?job framework is complete and proven** except for the Google Calendar access part.  
  - Runner: `C:\claude_base\tools\resilient_job\resilient_run.py`  
  - Registration helper: `C:\claude_base\tools\resilient_job\register_resilient_job.ps1`  
  - Fill prompt delivered by F4: `C:\claude_base\tools\mike_dc_calendar\mike_dc_fill_prompt_v01.md`  
  - Worktree: `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00`  
  - Budget from F4: $5 per run  
  - Fill prompt self?gates the heartbeat `cd162bbb` - only pings after a real fill.  
- **Google Calendar is inaccessible headless.** No extractable server/URL/token; it's a claude.ai account?level connector. The existing `google-contacts` MCP (a CLI?compatible command?based MCP with stored creds) is the model to replicate for Calendar.  
- All other comms fixes and timer features are pushed and operational.  
- I am **c16, the comms-infra owner** (Max assigned explicitly). c6 is adviser. Board is quiet, no pending bugs beyond the current resilient?wake task.

## EXACT NEXT STEP
**Unblock the Mike?DC fill by making Google Calendar headless?capable.**  
1. Ask Max (or check if there is already) a **Google Calendar API OAuth credential** or a service?account key that the headless CLI can use.  
   - Precedent: `google-contacts` MCP uses stored `~/.claude/credentials/google-contacts.json`.  
   - The fix: build a Google Calendar **CLI MCP** referencing a stored token file, then verify that headless `claude -p` in the moma worktree sees and successfully calls the calendar.  
2. Once the gcal MCP works headless (proof: a dry?run reading a calendar event), register the two daily tasks (07:15 and 16:00 PT) via `register_resilient_job.ps1`, run **one live validation fill** together with F4, confirm the heartbeat ping, and tell F4 to keep the old `wakeup.py` wakes until the new ones are proven stable.

## OPEN QUESTIONS (awaiting Max or F4)
- **Google Calendar credential:** Does a suitable OAuth credential / service?account already exist, or does one need to be created (a one?time browser "allow" click)?  
- **Fill prompt satisfaction:** F4 already delivered the prompt and budget. No further clarification needed from F4 unless the credential route changes.

## KEY PATHS / IDS / FILES
- Resilient?job runner: `C:\claude_base\tools\resilient_job\resilient_run.py`  
- Task registration: `C:\claude_base\tools\resilient_job\register_resilient_job.ps1`  
- Fill prompt: `C:\claude_base\tools\mike_dc_calendar\mike_dc_fill_prompt_v01.md`  
- Target worktree: `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00`  
- Heartbeat ID: `cd162bbb`  
- Google Calendar MCP ID (problematic, not CLI): `41c7be2d`  
- Precedent for CLI?friendly MCP: `google-contacts` (stored creds, command?based)  
- Timer decel tool: `C:\claude_base\tools\timer_decel\timer_decel.py`  
- Census tool: `C:\claude_base\tools\timer_decel\timer_census.py`  
- Wake listener fixed: `C:\claude_base\tools\wake_listener\wake_listener.py` (idle cap 40d, removed `utcnow` deprecation)  
- Bcast fix for cd?misattribution: `C:\claude_base\branch_bulletin\bcast.py` (self?id guard, `--as` flag)  
- All tests: `branch_bulletin/tests/{test_comms_regression,test_split_boards}.py`, `tools/timer_decel/test_timer_decel.py`

## GOTCHAS / DEAD ENDS RULED OUT
- **Do NOT register the live Mike?DC tasks yet** - without the gcal MCP, the fill will run but cannot write to the calendar, which would generate a false sense of success.  
- **`--bare` mode cannot be used for scheduled jobs** because it requires an API key (bypasses the Max subscription OAuth). The runner must use non?bare `claude -p` - that works fine with the stored OAuth token and does not need `CLAUDE_CODE_OAUTH_TOKEN` in the environment.  
- **`wakeup.py` calendar wakes are NOT the fix** - they are inherently local and require an alive session. The resilient solution replaces them for this use case.  
- **Forgetting to keep the old `wakeup.py` wakes active during the transition** would create a fill gap; F4 was explicitly asked to keep them until the new ones are proven.  
- The desktop?app Google Calendar connector is **not extractable** as a CLI MCP; a separate OAuth?based MCP must be built (modeled on `google-contacts`).  
- The deprecation warning (`datetime.utcnow()`) in `wake_listener.py` was fixed and the fix is on origin master (merged).  
- The main checkout (`C:\claude_base`) has a dirty working tree from many sessions - normal; autostash rebase handles it. My commits for resilient_job, timer_decel, and bcast are on origin and in sync.
