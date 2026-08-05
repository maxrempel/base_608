# Scribe handover - milestone 3 (~242K tokens)
# session: 20260617_serene_pasteur_eed5fd_5f143530
# cwd: C:\claude_base\.claude\worktrees\serene-pasteur-eed5fd
# written: 2026-06-17 23:16:53 by deepseek-v4-pro

# HANDOVER - E5 Sol Health-Watch (2026-06-17 ~21:40 PDT)

---

## GOAL (Max's words)

**"I start actual work on sol with fan, you watch for signs of trouble. You are now in charge of trouble watching."**

Max is doing real work on Sol (fan-ON config) and wants E5 to be the trouble-watcher - catch freezes, overheating, or unreachability and alert him. The watch must be **off Sol's own logs** (probe live `/proc/uptime` + sensors from outside) so a Sol freeze can't hide itself.

---

## DECISIONS MADE + WHY

### 1. Retired the bespoke watcher - Sol is already monitored
**Why:** Max pointed out his existing Healthchecks.io monitors already cover Sol fully (`sol-host heartbeat`, `sol-cpu-temp`, `fleet-deepseek-monitor`). They ping the same Telegram bot (@MMMMonitorMaxBot) and ship readings off-box (temp to Lak). Building a parallel system was redundant and wrong.

**What was torn down:**
- Windows scheduled task `sol_health_watch_guard` (DELETED - this was the popping terminal Max hated).
- `sol_health_watch.sh` and `sol_health_guard.sh` ? moved to `C:\claude_base\worklog\archive_e5_bespoke_solwatch\`.
- Leftover `sol_thermal_monitor.sh` from earlier RAM soak - killed.

### 2. Telegram alarms go through existing monitors, not a bespoke path
**Why:** The infrastructure map (`C:\claude_base\infra_map_tomemex.md`) already describes Sol monitors wired to Healthchecks.io ? Telegram. No need for E5's script to also curl Telegram directly. The existing `sol-cpu-temp` monitor alarms at 85?C and ships each reading off-box.

### 3. E5's role reduced to a light periodic in-chat check
**Why:** The real alarm path is independent (Healthchecks.io). E5's session should just verify the existing monitors are still green every ~30 min, not re-implement the watch. Context is expensive.

### 4. The thermal verdict from the RAM experiment
During the session, a clean finding emerged: **2-stick GREEN config (slots 1+3, 32GB @ 27GB load) is rock-solid ONLY when Sol has active DIMM airflow (case open or extra fan on).** With the cover closed + extra fan off, it froze 4 times and corrupted data twice in under an hour (temps climbed to 73?C). This is a strong thermal/airflow signal, not a RAM-config fault.

---

## CURRENT STATE

- **Sol is up, fan ON** - Max is doing real work on it.
- **Existing monitors are green** (verified via Healthchecks.io API - all four Sol checks `status=up`, pings fresh).
- **No E5 processes running** - bespoke watcher killed, scheduled task deleted, scripts archived. Nothing will pop a terminal.
- **E5's last armed self-wake** was re-pointed to check the existing Healthchecks monitors (not the retired digest file), but the session transcript shows a *later* wakeup prompt that still references the OLD `sol_health_digest.txt` path - this is stale and was sent before the teardown was fully reflected in the wakeup chain.

---

## EXACT NEXT STEP

**At the start of the next session, the cold handover recipient should:**

1. **Verify no bespoke watcher is running** - check no `sol_health_watch.sh` or `sol_thermal_monitor.sh` process exists (PowerShell: `Get-CimInstance Win32_Process -Filter "Name='bash.exe'" | Where-Object { $_.CommandLine -match 'sol_health_watch|sol_thermal_monitor' }`). If found, kill it.

2. **Verify the Windows scheduled task is gone**: `schtasks /Query /TN "sol_health_watch_guard"` - should return "ERROR: The system cannot find the file".

3. **Check existing monitors are green**: 
   ```
   curl -s -H "X-Api-Key: hcw_FURiOSiC9Vszzf2OWydsJumrkNj9" https://healthchecks.io/api/v3/checks/
   ```
   Look for `sol-host heartbeat`, `sol-cpu-temp`, `fleet-deepseek-monitor` with `status=up`.

4. **Report in-chat**: Sol's current uptime + temp (via a quick SSH: `ssh -i ~/.ssh/sol_key -o ConnectTimeout=10 maxre@192.168.1.113 "echo uptime=$(uptime -p); sensors 2>/dev/null | grep 'Package id'"`) and that monitors are green.

5. **Re-arm a 30-min light check** - NOT the old digest-peek prompt that references the retired watcher. Use Healthchecks API instead.

6. **Stop only when Max says work is done or says stop.**

---

## OPEN QUESTIONS (awaiting Max)

- **How long is the real work session on Sol?** (E5 keeps watching until told to stop.)
- **Should E5 also monitor Sol's load/memory during Max's work, or just freeze/overheat/unreachable?** (Currently scoped to trouble only.)

---

## KEY PATHS / IDs / COMMANDS

| Item | Value |
|---|---|
| **Sol host** | 192.168.1.113, user `maxre`, key `~/.ssh/sol_key` |
| **Healthchecks API key** | `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\healthchecks_io_creds_20260604.txt`) |
| **Telegram bot** | @MMMMonitorMaxBot, token in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\telegram_critical_alarms_bot_token_20260604.txt` |
| **Archived bespoke scripts** | `C:\claude_base\worklog\archive_e5_bespoke_solwatch\` |
| **Infra map** | `C:\claude_base\infra_map_tomemex.md` |
| **RAM experiment history** | `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` |
| **Bcast board** | `C:\claude_base\branch_bulletin\bcast.py` |

---

## GOTCHAS

1. **The last wakeup prompt in the transcript references a DIGEST FILE (`sol_health_digest.txt`) AND WATCHER that NO LONGER EXIST.** That prompt was a stale artifact - the watcher was retired BEFORE that wakeup fired, but the wakeup text wasn't updated. A cold session MUST NOT try to read `sol_health_digest.txt` or relaunch `sol_health_watch.sh`. Use the Healthchecks.io API instead.

2. **`pkill` is NOT available in Git Bash.** The earlier `pkill -f sol_thermal_monitor.sh` silently failed. To kill bash processes from Pine, use PowerShell: `Get-CimInstance Win32_Process -Filter "Name='bash.exe'" | Where-Object { $_.CommandLine -match 'sol_thermal_monitor' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }`.

3. **PATH fragility in daemonized bash scripts.** When launching bash scripts detached (via `setsid`, `Start-Process`, or Windows scheduled tasks), `PATH` is often empty. The cure: hardcode `export PATH="/usr/bin:/bin:/c/Program Files/Git/usr/bin:..."` at the top of any script that might run detached, OR always launch as a login shell (`bash -lc`). The scheduled task used `bash -lc`, which works.

4. **The 2-stick GREEN RAM config (slots 1+3) is clean ONLY with active DIMM cooling.** Max knows this; the fan is ON during his real work session. But if the fan gets accidentally turned off or the cover closed with no extra airflow, Sol will eventually freeze at load. This is important context for interpreting any trouble alarms.

5. **The `campaign.run` flag auto-restarts ramscan on reboot via `@reboot` cron.** If Sol reboots for any reason during Max's work, the old RAM soak might relaunch alongside his work. E5 should be aware of this but Max likely disabled it before starting real work. Worth a quick check on first connect.
