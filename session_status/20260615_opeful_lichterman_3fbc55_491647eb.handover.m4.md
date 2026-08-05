# Scribe handover - milestone 4 (~72K tokens)
# session: 20260615_opeful_lichterman_3fbc55_491647eb
# cwd: C:\claude_base\.claude\worktrees\hopeful-lichterman-3fbc55
# written: 2026-06-15 09:17:46 by deepseek-v4-pro

# HANDOVER: Playwright Browser Reaper with Heartbeat

## GOAL (Max's words)
Prevent orphaned Playwright browsers from piling up. Sessions sometimes open Playwright and forget to close it. The next session shouldn't have to guess whether to kill. Force every session to close on a timer - if idle/stale for a period, go kill it. The timeout should be 15 minutes (not 10).

Max's final word: implement this as a "hook" (heartbeat pattern), with a 15-minute threshold.

## DECISIONS + WHY

1. **Heartbeat + reaper pattern chosen (not blind timer kill).**
   - A blind timer that kills after N minutes would nuke browsers that are legitimately idle - e.g., waiting for the user to solve a captcha or the user stepped away temporarily.
   - Solution: the *active* session touches a heartbeat file whenever it's genuinely using Playwright. The reaper only kills browsers whose heartbeat is older than the threshold. A session parked on a captcha keeps refreshing its heartbeat and survives.

2. **Timeout: 15 minutes (per Max).**
   - Initial suggestion was 10 min. Max bumped it to 15 min ("maybe even longer - say 15 min"). This is the final number.

3. **Precedent: bcast already uses this pattern.**
   - bcast has an 8-minute liveness window using the same heartbeat trick. This implementation should follow the same approach but with a 15-minute window for Playwright sessions.

4. **Terminology: Max said "like a hook."**
   - He's endorsing the heartbeat-as-hook design. The reaper should be event/timer-driven, not a manual cleanup step.

## CURRENT STATE
- **Nothing built yet.** This was a design discussion only (2 turns, zero tool calls).
- Agreement reached on the approach (heartbeat + 15-min reaper).
- The concept is fully specified and ready to build.

## EXACT NEXT STEP
Build the mechanism:
1. **Heartbeat side:** When a session is actively using Playwright, it writes/touches a heartbeat file (e.g., `<tempdir>/playwright-session-<id>.heartbeat`) periodically (e.g., every 30-60 seconds).
2. **Reaper side:** A timer or daemon that scans for heartbeat files, checks their age, and if a heartbeat is older than 15 minutes, kills the corresponding Playwright browser process and cleans up the heartbeat file.
3. Follow the existing bcast liveness pattern for consistency.

## OPEN QUESTIONS
- None. Max approved the design and specified the 15-minute timeout. Build is ready to proceed.

## KEY PATHS / IDS
- bcast liveness mechanism (existing code to reference): uses an 8-minute window
- Heartbeat file location: likely in whatever temp directory the sessions use (same neighborhood as bcast)
- Playwright session identification: session IDs used to name heartbeat files

## GOTCHAS
- **The captcha/idle case is the whole point of the heartbeat.** Don't use a simple wall-clock timer that ignores liveness, or you'll kill browsers the user is actively looking at.
- **Reaper must be resilient:** if a browser process is already dead (crashed, killed manually), the reaper should clean up the orphaned heartbeat file without erroring.
- **Match bcast's existing heartbeat format/location conventions** to avoid reinventing the wheel inconsistently.
