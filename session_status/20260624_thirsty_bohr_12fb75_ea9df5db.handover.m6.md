# Scribe handover - milestone 6 (~485K tokens)
# session: 20260624_thirsty_bohr_12fb75_ea9df5db
# cwd: C:\claude_base\.claude\worktrees\thirsty-bohr-12fb75
# written: 2026-06-24 14:10:56 by deepseek-v4-pro

# HANDOVER: Comm-Infra Debugging & Resilient Wake-Up Work (c16)

## GOAL (in Max's own words)
Max initially asked c16 to "debug and test whole system. It is a fucking mess. Very useful but very buggy." Then specifically to take over c6's team-communication infrastructure and fix bugs (case-sensitive team derivation, cross-team @-mention routing, worklog cwd-split). After that, he asked for a timer-deceleration system so sessions automatically slow their wake-up cadence. Finally, the urgent task: **make scheduled/calendar wake-ups completely resilient** - "even if the computer is off it should keep the information in the cloud and catch up as soon as the computer is back online" and "if the wake up is missed it would still catch you as soon as possible." This was prompted by F4 missing critical Mike-DC fill appointments because the existing wake-up mechanism only fires when a Claude chat window is open.

## DECISIONS MADE + WHY

1. **Testing before writing:** c16 found that the reported bugs (case-sensitivity, cross-team routing, worklog cwd-split) were already fixed in committed code by c6; so c16 built isolated test harnesses to verify, then built a permanent regression suite. Decision: verify, don't rewrite, and lock fixes with committed tests.

2. **Joint-board flooding fix:** c16 implemented an auto-demote routing in bcast (messages route to team board if no cross-team mention, to joint if cross-team). After c6 relayed Max's intent, changed it to a **challenge-at-point-of-violation** system: when a post would hit the joint board but contains no cross-team @-mention, the sender gets a warning asking if they really mean it, and the message still goes through (fail-open) to avoid hiding a real announcement. A new `--all` flag explicitly targets everyone. This structural change eliminated the cross-project flooding without relying on discipline.

3. **Timer deceleration:** c16 built a small engine (`timer_decel.py`) so sessions can use `4mt` (decel, default) or `4steady` (hold cadence). Decel stays at each interval for 3 idle wakes then moves to the next in the ladder: 4min ? 8 ? 15 ? 30 ? 1h ? 3h ? 6h ? 12h ? 24h, parked at 24h. Night quiet hours (22-07) enforce a minimum 3h interval unless steady. The email-to-Max trigger is an **alarm** only: crisis, damage from decelerating, or stuck in pointless steady - not for routine mode decisions. Updated global2.md so all sessions auto-adopt.

4. **Resilient wake-up design:** The root cause of the missed Mike-DC fill was that `wakeup.py` only fires when a specific Claude chat (F4) is open. c16 built a new mechanism (`resilient_run.py`) that uses **Windows Task Scheduler** to launch a headless `claude -p` in the correct worktree, at scheduled times. Task is configured with `StartWhenAvailable` and boot trigger, so it catches up if the computer was off. c16 validated end-to-end: headless Claude autheticates via stored OAuth keychain (no env token needed), runs a prompt, logs result, and records last-run timestamp. The tool also supports a cost cap and disallowing dangerous tools.

5. **Census of session timers:** c16 found only ~5 live listener processes and many stale state files. Instead of forcing cleanup, c16 raised the idle block cap of `wake_listener` from 12h to 40 days so active-but-idle sessions remain force-wakeable for weeks. A ghost file archive sweep was proposed but not implemented, pending Max's call.

6. **Other fixes:** cd-missend guard in bcast: if a post's leading self-attribution (e.g., "G2 -> ...") doesn't match the cwd's registered identity, refuse it with instructions to use `--as`. This prevents silent posting under the wrong name when a session cd's into the main repo to commit.

## CURRENT STATE

- All comms bugs are fixed, tested, and pushed. Regression suite (44+ checks) passes.
- Timer decel tool is built, tested, and global rules updated. Sessions will start using it on their next turns.
- Resilient job infrastructure is built, validated end-to-end, and pushed (`3dfe73e6`).
  - Runner: `C:\claude_base\tools\resilient_job\resilient_run.py`
  - Task Scheduler registration: `C:\claude_base\tools\resilient_job\register_resilient_job.ps1`
  - Method doc: `C:\claude_base\tools\resilient_job\resilient_job_method_v01_tomemex.md`
- The missing piece: **F4's fill prompt file** and the exact schedule (two daily times, e.g., 7:15am and 4pm) haven't been handed over yet. c16 told F4 to provide the prompt and to keep the old fragile wake-up running until the new one is live-tested.
- The c16/C26 ownership overlap (both claiming comms-infra owner) is noted but not critical to this task; c16 announced itself as owner per Max's earlier directive.

## EXACT NEXT STEP

**From the transcript ending:** c16 posted to F4 asking for the fill prompt file, a cost cap, and the exact schedule. The next action is:

1. Obtain from F4:
   - The prompt file that defines the Mike-DC fill (exact instructions for Claude to generate the digest).
   - A Max-approved cost cap (e.g., $1-$2 per run).
   - The desired times of day (e.g., 7:15 AM and 4:00 PM EST).
2. Write the prompt to a stable file (e.g., `C:\claude_base\tools\resilient_job\prompts\mike_dc_fill.txt`) that won't be deleted.
3. Register two Windows scheduled tasks using `register_resilient_job.ps1` with the job names (e.g., `mike-dc-fill-am`, `mike-dc-fill-pm`), the runner path, and the correct worktree directory for the fill.
4. Run a live test of at least one scheduled task (on-demand trigger) while c16 or Max monitors, confirming the output lands where F4 expects.
5. Once confirmed, tell F4 to disable the old `wakeup.py`-based wake-up for that fill.
6. Commit the prompt file and the registration script usage (if not already in repo).
7. Follow up with Max to confirm the fill is working.

## OPEN QUESTIONS (awaiting Max or F4)

- **F4's fill prompt has not been received yet.** This is the blocker.
- **Is the old fragile fill still running?** c16 told F4 to keep it until the new one is proven. Need to confirm.
- **c16/C26 owner overlap:** Max hasn't explicitly resolved it. c16 announced itself as owner per earlier instruction, but C26 also claimed the domain on a different Pine board. Not urgent for the fill task, but could cause confusion later.
- **Archive sweep of ghost session files:** c16 proposed but held back pending Max's decision. Not time-sensitive.

## KEY FILE PATHS AND IDs

- **Comms board (bcast):** `C:\claude_base\branch_bulletin\bcast.py`
- **Wake listener (force-wake):** `C:\claude_base\tools\wake_listener\wake_listener.py`
- **Resilient runner:** `C:\claude_base\tools\resilient_job\resilient_run.py`
- **Task registration helper:** `C:\claude_base\tools\resilient_job\register_resilient_job.ps1`
- **Timer decel engine:** `C:\claude_base\tools\timer_decel\timer_decel.py`, census: `timer_census.py`
- **Global rules (decel modes):** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- **Regression tests:** `C:\claude_base\branch_bulletin\tests\test_comms_regression.py`, `test_split_boards.py`
- **Worklog:** `C:\claude_base\compaction_kb\scripts\worklog.py` (already fixed, git toplevel anchoring)
- **Git commits to note:** `3dfe73e6` (resilient job), `b02eb5fb` (cd-missend guard), `3e341f62` (challenge routing), `843069dd` (timer decel).
- **Session identity:** c16 is the comms-infra owner; c6 is adviser; F4 is the Mike-DC fill worker.

## GOTCHAS / DEAD ENDS RULED OUT

- **Do NOT use `--bare` mode for headless Claude:** it requires an API key, not the subscription; the runner must use non-bare `claude -p` with `--disallowedTools` to let OAuth auth work. Tests confirm it works.
- **The wake listener is single-process per session,** and only exists while the Claude chat is open. The 12h?40d cap helps but doesn't make a closed window wakeable. For offline resilience, only an OS-level scheduler (Task Scheduler) can fire absent a chat.
- **The joint-board migration (moving old posts) is risky and adds no live value** - all new posts are cleanly routed since the fix. c16 recommended archiving a snapshot instead, pending Max's decision.
- **Test harnesses must not leak state** into the live `branch_bulletin/state` dir. c16's ad-hoc tests earlier did this, causing a false collision alarm. The committed regression tests use a temp directory with an isolated `BCAST_BASE` env var, so they are leak-proof.
- **The `whoami` registration uses cwd,** so when a session cds to the main repo (`C:\claude_base`) to commit, its posts would go out as the repo's identity (b29) - the cd-missend guard now catches this and refuses with instructions.
- **The `claude` CLI is on PATH** (`claude` v2.1.111) and can be used headless, but it must be called from the correct worktree directory; the Task Scheduler task must set the working directory accordingly.

The cold session picking up this handover should immediately check the board or inbox for F4's response with the fill prompt, then proceed with steps 1-6 under EXACT NEXT STEP. If no response yet, consider force-waking F4 directly (using bcast) or asking Max to prod F4.
