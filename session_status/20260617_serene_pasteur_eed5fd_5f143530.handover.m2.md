# Scribe handover - milestone 2 (~153K tokens)
# session: 20260617_serene_pasteur_eed5fd_5f143530
# cwd: C:\claude_base\.claude\worktrees\serene-pasteur-eed5fd
# written: 2026-06-17 21:21:40 by deepseek-v4-pro

# Scribe Handover - E5 Sol RAM Thermal Watch

---

## GOAL (Max's words, distilled)

Max is diagnosing Sol's RAM freezes (Lenovo M720s, i7-9700, 4?16GB DDR4-2667 non-ECC). The 2-stick GREEN config (sticks in slots 1+3, 32GB total, loaded at 27GB) was previously **rock-solid** - 45+ rounds clean, 0 crashes, 0 bit-flips. Max is now testing whether the freezes are **thermal/airflow** by closing the case cover and removing the extra cooling fan. If the same config breaks only when hot, the root cause is heat, not the RAM sticks themselves.

---

## DECISIONS + WHY

### 1. E5 takes over monitoring from E1
**Why:** E1testrunner's self-wake timer broke. Max handed the watch to E5 to keep the 4-hour soak monitored.

### 2. Polling cadence: 2 min ? 7 min ? 12 min, hold at 12
**Why:** Quick initial checks to confirm stability after handover, then widen to avoid noise. Tightened back to 2 min when trouble hit (freeze/corruption).

### 3. Fan removal - safe, no alarm
**Why:** At 2-stick/27GB load with case open, temps were only ~54?C. Stock CPU cooler alone is plenty; critical is 100?C. E5 confirmed post-removal temp was 56?C - negligible change.

### 4. Deliberate reboot rebaselined (bootcount=1 as baseline)
**Why:** Max manually restarted Sol at 20:59 PDT with fan off + cover closed. That's a known boot, not a freeze. E5 set `real_freezes = bootcount - 1` to avoid false alarms.

### 5. Thermal verdict at 21:13 and 21:20
**Why:** The same GREEN stick pair that ran 45 clean rounds with case open (~57?C) froze within ~14 minutes with the cover closed (temps climbed to 69-73?C). Bit corruption (bad_words=2) also appeared for the first time ever on this config. Freezes recurred ~7-8 minutes apart. This is a strong thermal signal - the RAM itself is fine when cool.

### 6. Watching temp, not just boot count
**Why:** With the thermal hypothesis, temp is the leading indicator. E5 escalated alarms to include temp ?80?C and reported temp every tick while hot.

---

## CURRENT STATE

- **Config:** 2-stick GREEN (stick1/slot1 + stick3/slot3, 32GB total), ramscan 27GB load
- **Case:** COVER CLOSED, extra cooling fan REMOVED (stock CPU cooler only)
- **Last known state:** Sol froze at ~21:20:12 PDT (second freeze after the 21:12:54 one), watchdog auto-rebooted. Boot count = 3 (2 real freezes + 1 manual restart). Bit corruption (bad_words=2) appeared in round 51. Temps were climbing (73?C at last clean reading before the second freeze).
- **Uptime at last check:** ~1 minute (fresh reboot, temp ~59?C and climbing)
- **Pattern:** Freeze every ~7-8 minutes as temps climb to ~70-73?C
- **Watch interval:** E5 is armed on a **2-minute** ScheduleWakeup (tight freeze watch)
- **E1 is aware:** E5 posted freeze and corruption findings to the bcast board

---

## EXACT NEXT STEP

1. **Next wakeup is armed** - a 2-minute ScheduleWakeup titled `E5 Sol-soak FREEZE+CORRUPTION watch (cover-closed thermal)`. It will SSH into Sol and check boots, rounds, bad_words, and Package temp.

2. **Max's expected action:** Open the case cover and/or restore the extra cooling fan. This is the key isolation experiment - if the GREEN config goes clean again once cooled, it nails the diagnosis: **Sol's freezes are heat-driven, not a RAM-configuration fault.**

3. **If Max cools the box:** E5 watches for temp dropping below ~60?C and bad_words staying 0 for 2-3 ticks, then reports "cooling fixed it" and widens from 2-min ? 7-min ? 12-min polling.

4. **If Max does NOT cool the box:** Expect more freezes every ~7-8 minutes as temps cycle. E5 will catch them and continue alarming.

---

## OPEN QUESTIONS AWAITING MAX

- **Did Max re-open the cover or restore the fan?** (Not yet at transcript end - the wakeup is still armed waiting for the next tick.)
- **When should the soak be considered done?** Original 4-hour target was ~22:32 PDT (from the 18:32 start), but after the 20:59 restart the new 4-hour target would be ~00:59 PDT. Max hasn't explicitly reset the end condition.
- **Next experiment after thermal verdict?** If cooling fixes it, the endgame is still memtest86+ at Sol's console (needs Max physically there) to fully separate stick-vs-slot-vs-controller.

---

## KEY PATHS / IDs / COMMANDS

| Item | Value |
|---|---|
| Sol SSH | `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` |
| Campaign round | `/home/maxre/campaign_round.cnt` |
| Boot/crash log | `/home/maxre/campaign_boots.log` (`grep -c ^BOOT` = boot count) |
| Results log | `/home/maxre/campaign32.log` (RESULT ROUND lines, bad_words=N) |
| Temp check | `sensors 2>/dev/null | grep 'Package id'` |
| History doc | `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` |
| Monitor log | `C:\claude_base\worklog\sol_soak_2stick_green_4h_monitor.log` |
| bcast post | `python "C:/claude_base/branch_bulletin/bcast.py" post "..."` |
| bcast wake | `python "C:/claude_base/branch_bulletin/bcast.py" wake --name <target>` |
| worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| Worktree | `serene-pasteur-eed5fd` |
| E1's worktree | `dreamy_bassi` |
| Bcast ID | E5 (this session), E1testrunner (the campaign runner) |
| E5 wakeup ID | `d0a92f54` (original), then re-armed multiple times |

---

## GOTCHAS

1. **Boot baseline subtraction:** After Max's deliberate 20:59 reboot, `real_freezes = bootcount - 1`. Any new session MUST check the boot log timestamps to distinguish Max's manual reboots from real crashes.

2. **Downsize load trap (from original handover, not yet triggered here):** After any RAM downsize swap, campaign.sh still holds the PREVIOUS higher load. Fix: lock campaign.sh load in its own SSH call first, then reset+launch. (Not relevant to current 2-stick 27GB soak - but critical for any next-config test.)

3. **No IPMI:** Sol has no remote console. Freezes require physical presence to recover (watchdog auto-reboots in ~2 min, but memtest86+ needs Max at the keyboard).

4. **Thermal vs. contact confounding:** Closing the cover and removing the fan could have physically nudged a DIMM. The cleanest confirmation that it's purely thermal is to cool it again (open cover / re-add fan) and watch it go clean - which hasn't happened yet at transcript end.

5. **ScheduleWakeup continuity:** Each tick re-arms the next. If a new session begins and the last wakeup hasn't fired yet, it will still fire and wake the new session with the armed prompt.

6. **bad_words=2 on GREEN config:** This is the first-ever bit corruption recorded on the 2-stick GREEN pair (all prior rounds = 0). This appeared alongside the thermal spike. If corruption persists even after cooling, it would suggest the DIMMs themselves may have taken damage - but the working hypothesis is that it's purely heat-induced.
