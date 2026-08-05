# Scribe handover - milestone 2 (~151K tokens)
# session: 20260619_awesome_bell_a6ad80_36bcca56
# cwd: C:\moma\.claude\worktrees\awesome-bell-a6ad80
# written: 2026-06-19 07:57:54 by deepseek-v4-pro

# HANDOVER - Mike DC Calendar Monitor QC (G3 session)

---

## GOAL (Max's words)
"Setup a monitor. Using a monitor system to alarm me when the update is missed by 1.5 days. Possibly that monitor already exists."

The monitor was then found to already exist, so the session pivoted to QC: verify it's live, verify the daily run that feeds it actually fires, and confirm the full end-to-end loop works.

---

## DECISIONS + WHY

1. **No new monitor built** - a prior session ("G2monitor", 2026-06-17) had already created `mike-dc-calendar-daily` on Healthchecks.io. It matched the spec exactly (1.5-day alarm, Telegram + email alerts). No point rebuilding.

2. **QC focused on the feed side** - the monitor's config was trivially verifiable via API. The real risk was whether the daily Mike-DC calendar run *actually fires and pings it*. That's what the 180-minute self-wake timer was for: wait for today's 09:00 run to land a real heartbeat.

3. **Doc fix committed** - the method doc (`mike_dc_calendar_method_v01_tomemex.md`) had a stale wake ID. Wakes regenerate IDs each time they're re-armed, and the schedule lives in a different worktree (`sweet_kepler`), so hardcoding the ID was misleading. Updated the doc to say "look it up live."

4. **Self-wake hops (60-min caps)** - the wake tool enforces a 60-minute max, so the 180-minute timer was split into three 60-min hops with re-arm instructions.

---

## CURRENT STATE

**Everything works. QC passed.**

- **Monitor:** `mike-dc-calendar-daily` on Healthchecks.io - check ID `cd162bbb-59b9-4736-aee3-3ccd4740736b`
- **Config:** 1-day timeout + 12h grace = alarms at 1.5 days of silence
- **Alert channels:** Telegram (@MMMMonitorMaxBot) + email (mass@tamza.com) - both confirmed attached
- **Status:** `up` - went from 1 ping (setup) to 4 pings (real runs), last ping 2026-06-19 04:34 UTC
- **Feed mechanism:** A daily self-wake (09:00, repeats) in the `sweet_kepler` worktree re-runs the calendar fill. On success it pings the monitor; on error it pings `/fail`. Both paths alert Max.
- **Expiry:** Auto-stops after 2026-07-31 (end of calendar autopilot season)
- **Doc fix:** Committed to `claude_base` (updated stale wake ID reference)

---

## EXACT NEXT STEP

**None - the session is complete.** The monitor is live, verified end-to-end, and the doc fix is pushed. Max was informed. The 180-min self-wake timer was stopped early (success confirmed on hop 1).

If Max wants to act on the open question below, that's the only remaining item.

---

## OPEN QUESTIONS

**One question asked twice, still unanswered by Max:**

> Keep the alarm's 2026-07-31 auto-expiry, or extend/remove it?

The monitor self-destructs when the calendar autopilot season ends. If Max wants alerts to persist past summer, the expiry needs removal.

---

## KEY PATHS, IDs, COMMANDS

| What | Path/ID |
|---|---|
| Healthchecks check ID | `cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| Healthchecks API key | `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (in `C:/Users/maxre/Nextcloud/zSyncMain/ssh/healthchecks_io_creds_20260604.txt`) |
| Monitor API URL | `https://healthchecks.io/api/v3/checks/cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| Method doc | `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` |
| Wake schedule (where the daily run is armed) | `C:/claude_base/branch_bulletin/wake/schedules/sweet_kepler_a528fd_901f468ea7.json` |
| Wake ID (live, may drift) | `ba98305c` (as of session) |
| Worktree this session ran in | `awesome-bell-a6ad80` (bcast) |
| Worktree the schedule lives in | `sweet_kepler_a528fd` |
| Quick API check command | `curl -s -H "X-Api-Key: hcw_FURiOSiC9Vszzf2OWydsJumrkNj9" "https://healthchecks.io/api/v3/checks/cd162bbb-59b9-4736-aee3-3ccd4740736b" \| python -c "import sys,json; d=json.load(sys.stdin); print(d['n_pings'], d['last_ping'], d['status'])"` |

---

## GOTCHAS

1. **Wake IDs are ephemeral** - they regenerate every time a wake is re-armed. Never hardcode them; always look up the live ID from the schedule JSON in `C:/claude_base/branch_bulletin/wake/schedules/`.

2. **Wake schedules are per-worktree** - running `wakeup.py list` in `awesome-bell` showed nothing because the Mike-DC schedule lives in the `sweet_kepler` worktree. Always check the right worktree or grep the full schedules directory.

3. **The heartbeat ping wiring lives in the wake message itself** (a curl one-liner in the schedule JSON) - there is no separate monitoring script. The success path pings the check; the error path pings `/fail`. Both are one-liners baked into the wake payload.

4. **The doc was stale but the system wasn't** - the method doc had an old wake ID, but the actual armed wake was correct and firing. The discrepancy was cosmetic only.
