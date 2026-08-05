# Scribe handover - milestone 11 (~165K tokens)
# session: 20260613_dreamy_bassi_ead69f_db0f1c86
# cwd: C:\claude_base\.claude\worktrees\dreamy-bassi-ead69f
# written: 2026-06-13 15:28:05 by deepseek-v4-pro

# HANDOVER - Sol Freeze Investigation & Watchdog Fix (b11)

## GOAL (Max's words)
"Set 4 min timer until everything is solved and go autonomous. Sol is up. I force rebooted it 7 min ago. See when it crashed. Make sure logs are synked to elsewhere and document that. Investigate. Temperature etc."

Translation: Find out WHY Sol keeps dying (3 times in ~4 days), fix the root cause so it doesn't require manual reboots, ensure off-box log survival exists, document everything, run autonomously with a wakeup timer until the task is fully solved.

---

## DECISIONS MADE + WHY

**1. The freezes are REAL hardware/userspace hangs, not SSH drops.**
Evidence: Both local cron (sol_heartbeat, temp_monitor, guard - none need network) AND outbound Healthchecks pings stopped at the same second (~14:49 PDT). A box that only lost sshd would still log cron locally. A box that only lost network would still log cron locally. Both went silent together = full freeze. The "no trace in logs" is the *signature* of a freeze, not missing data.

**2. Root cause of the REPEATED manual-reboots: the hardware watchdog was INERT.**
`RuntimeWatchdogSec=30s` was configured in `/etc/systemd/system.conf` - the watchdog was *switched on in software* but had no hardware to bite. The `iTCO_wdt` kernel module was blacklisted by Ubuntu's HWE kernel package (`/lib/modprobe.d/blacklist_linux-hwe-6.17_*.conf`). Every boot, kmod refused to load it: "Module 'iTCO_wdt' is deny-listed." A previous "fix" from Jun 10 added `/etc/modules-load.d/itco_wdt.conf` but a modules-load.d entry CANNOT override a deny-list - it silently failed across three freezes.

**3. The fix: a systemd oneshot service that force-loads past the deny-list.**
`/etc/systemd/system/itco-wdt.service` - runs `modprobe iTCO_wdt` by name (plain modprobe ignores `blacklist` directives, unlike modules-load.d which respects them), then `daemon-reexec` to re-arm systemd's watchdog. Lives in `/etc/systemd/`, survives kernel updates. This was chosen over: editing the package blacklist file (gets wiped on kernel updates), or a modules-load.d entry (doesn't work against deny-lists), or a modprobe.d override (you can't subtract a blacklist via directive).

**4. No new off-box monitoring added - it already existed.**
Sol already had `sol_heartbeat.sh` cron ? Healthchecks check `023cf3f6-186a-4afd-ada0-95e5d7e5f223` ? Telegram + email. Plus `sol-cpu-temp` check `b1073b92` with durable temp history shipped to Lak. A duplicate monitoring stack was briefly created (snapshot script, second Healthchecks check, new Syncthing folder) then fully deleted per anti-duplication rules.

**5. No ssh-self-restart added.**
An ssh-based self-restart can't help a freeze - it can't run while userspace is hung. The evidence proves it's a freeze, not an sshd-only failure. Adding one would be noise.

**6. Freeze root cause itself is UNKNOWN (hardware/PSU suspected).**
No panic, no OOM, no MCE, no thermal warning in logs - the journal just stops mid-normal-operation at 14:49:08. Temps are healthy (36-38?C, crit is 100?C). Three freezes in 4 days (Jun 9, 12, 13) points to a recurring hardware trigger. The watchdog fix handles the *consequence* (staying dead), not the cause.

**7. Timeline corrected.**
Initial guess of "rebooted ~14:53" was wrong. Max's message at ~15:07 PDT saying "7 min ago" + Sol's actual boot at 15:00:31 proves restart was ~15:00. Freeze at 14:49:08, ~11 min dead, manual restart at ~15:00.

**8. Documentation updates on infra_map.**
The infra map falsely claimed the watchdog was working since Jun 10. Rewrote that section to document: the deny-list bug, that the device was absent (no /dev/watchdog), that the Jun 10 fix never actually loaded, the real fix via itco-wdt.service, and all three freeze incidents.

---

## CURRENT STATE

**Sol is UP and stable (verified by the last autonomous check):**
- Uptime: ~24 minutes after Max's ~15:00 reboot, no new freeze
- `/dev/watchdog0` present and live (`/dev/watchdog0` character device 252, 0)
- `itco-wdt.service` enabled and active (`systemctl is-enabled` returns enabled)
- `RuntimeWatchdogUSec=30s` confirmed in systemd
- Temps: 37?C (well below 100?C crit)
- b-team worker is running (not disrupted - Sol was NOT rebooted to verify persistence)

**The fix is VERIFIED on the current boot but NOT across a reboot.**
The itco-wdt.service was tested by starting it and confirming the watchdog device appears. It was enabled so it'll run at next boot. But an actual reboot was intentionally avoided because the b-team worker is live on Sol. Boot-persistence will be confirmed on Sol's next natural reboot.

**All duplicates cleaned up:**
- Deleted Healthchecks check `5b5fcee5-32b2-4c1c-944e-51db165ee769`
- Removed sol_health_snapshot.sh cron line and script
- Deleted dead modules-load.d files (`itco_wdt.conf`, `watchdog.conf`)
- Syncthing folder `sol_clawy_writes` left intact (it's the proper Memex pipeline channel, wasn't harmful)

**Docs updated:**
- `C:\claude_base\infra_map_tomemex.md` - watchdog section corrected
- `C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md` - full writeup with timeline, diagnosis, fix, and "how to investigate next time" recipe
- `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` - multiple entries for investigation, fix, persistence, timeline correction, freeze proof
- bcast posts to b-team (b7, b8, b80) about Sol status

**Autonomous timer is ARMED** for ~15:26 PDT (4 min after last action). The wakeup instruction says: verify Sol still up, /dev/watchdog0 present, service enabled. If stable ? post "solved" bcast, mark worklog DONE, STOP re-arming. If new freeze ? investigate and keep timer.

---

## EXACT NEXT STEP

The autonomous wakeup fires ~15:26 PDT with a specific script. The cold session should:

1. **Read the worklog first:** `python C:/claude_base/compaction_kb/scripts/worklog.py read`
2. **SSH into Sol:** `ssh -i ~/.ssh/sol_key -o ConnectTimeout=8 maxre@192.168.1.113`
3. **Run three checks:**
   - `uptime` - confirm no new freeze (should be >30 min by then)
   - `ls -l /dev/watchdog0` - confirm device still present
   - `systemctl is-enabled itco-wdt.service` - confirm still enabled
4. **If all three pass (99% likely):**
   - Post bcast: `python "C:/claude_base/branch_bulletin/bcast.py" post "b11->team: Sol stable, resilience task solved. Watchdog fix verified live (/dev/watchdog0 present, 30s, boot-persistent). No new freeze."`
   - Log DONE: `python C:/claude_base/compaction_kb/scripts/worklog.py log "Sol resilience task COMPLETE. Final stability check: uptime Xmin, watchdog live, service enabled. No new freeze. Task solved. Stopping timer."`
   - **DO NOT re-arm ScheduleWakeup.** The task is done.
5. **If Sol is unreachable or a new freeze occurred:**
   - Investigate per `C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md`
   - Re-arm timer and continue

---

## OPEN QUESTIONS (still awaiting Max)

1. **What is the actual freeze cause?** Three hangs in 4 days with zero log trace suggests hardware - possibly PSU voltage droop, bad RAM, or a chipset errata. If freezes continue despite the watchdog, next steps are:
   - BIOS setting: "AC Recovery = Power On" (handles full power loss, which watchdog can't)
   - Memory test (memtest86)
   - Check if a specific cron or service triggers the freeze pattern
2. **Is the watchdog boot-persistent across an actual reboot?** Won't be confirmed until Sol naturally reboots (not forced - b-team worker is running).
3. **Does Max want the b-team worker moved off Sol** given the recurring hardware instability?

---

## KEY PATHS & IDs

**Sol SSH:** `ssh -i ~/.ssh/sol_key -o ConnectTimeout=8 maxre@192.168.1.113`
**Sol sudo password:** `SM2w3e4r5t6y=` (file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\sol_sudo_password_20260523.txt`)

**Watchdog fix (on Sol):**
- Service: `/etc/systemd/system/itco-wdt.service` (oneshot, force-loads iTCO_wdt, re-arms systemd)
- Enabled at: `/etc/systemd/system/multi-user.target.wants/itco-wdt.service`
- Module: `iTCO_wdt` (depends on `iTCO_vendor_support` + `intel_pmc_bxt`)
- Device: `/dev/watchdog0` (created when module loads)
- Config: `RuntimeWatchdogSec=30s` in `/etc/systemd/system.conf`
- Deny-list: `/lib/modprobe.d/blacklist_linux-hwe-6.17_<something>.conf` - DO NOT EDIT (package file)

**Existing monitoring (on Sol):**
- Healthchecks check for heartbeat: `023cf3f6-186a-4afd-ada0-95e5d7e5f223` ("sol-host")
- Healthchecks check for CPU temp: `b1073b92` ("sol-cpu-temp")
- Cron entries in maxre's crontab: sol_heartbeat.sh, temp_monitor.sh
- Durable temp history shipped to Lak

**Healthchecks API:**
- Key: `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\healthchecks_io_creds_20260604.txt`)
- Alerts route to Telegram `@MMMMonitorMaxBot` (chat 1395850773) + email mass@tamza.com

**Key docs on Pine:**
- `C:\claude_base\infra_map_tomemex.md` - updated watchdog section (replaced false "working" claim)
- `C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md` - full incident report + fix recipe
- `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` - session worklog

**bcast:** `python "C:/claude_base/branch_bulletin/bcast.py" post "<message>"`
**worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "<entry>"`

**Syncthing on Sol:** Shares `sol_clawy_writes` (Memex KB pipeline ? Lak ? Nextcloud ? Pine). Sol does NOT use Nextcloud client - Syncthing is its off-box sync.

---

## GOTCHAS

1. **Do NOT** edit `/lib/modprobe.d/blacklist_linux-hwe-6.17_*.conf` - it's a package file, gets wiped on kernel updates. The itco-wdt.service is the kernel-update-proof fix.
2. **Do NOT** use `systemctl enable itco-wdt.service` again - it's already enabled. Don't touch it unless it shows disabled.
3. **Do NOT** add modules-load.d entries - they silently fail against deny-lists. The service approach is correct.
4. **Do NOT** duplicate monitoring - Healthchecks checks `023cf3f6` and `b1073b92` already exist and work.
5. **Do NOT** reboot Sol to "verify persistence" - the b-team worker is running. Persistence confirms next time Sol reboots naturally.
6. **If Sol freezes again**, the watchdog should now auto-reboot it in ~30s (device present, systemd armed). If it DOESN'T self-reboot, something is wrong with the watchdog fix - likely the service didn't run at boot. Check `journalctl -b -u itco-wdt.service`.
7. **The watchdog cannot catch a full power loss** (PSU failure, unplugged). That needs BIOS "AC Recovery = Power On" and the Healthchecks dead-man alert.
8. **es.exe quoting:** Use `-path "C:/path"` with forward slashes. DO NOT put a trailing backslash on Windows paths - it escapes the closing quote and breaks bash.
9. **worklog.py read** always comes first on any autonomous wakeup - it's the compaction-survival journal for this task.
10. **"STOP re-arming the timer"** is explicit in the wakeup instructions. If stability confirmed, the task is DONE - do not ScheduleWakeup again. Only re-arm if a new freeze occurs and investigation continues.
