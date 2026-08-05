# Scribe handover - milestone 11 (~167K tokens)
# session: 20260617_jovial_chaum_26dd4b_bb5c7df0
# cwd: C:\claude_base\.claude\worktrees\jovial-chaum-26dd4b
# written: 2026-06-17 13:20:38 by deepseek-v4-pro

# HANDOVER - Sol RAM Diagnosis Session (E1sol, worktree jovial-chaum-26dd4b)

---

## GOAL (Max's words)

Diagnose why Sol (Lenovo ThinkCentre M720s, 192.168.1.113) keeps freezing. Root-caused as RAM instability, but Max rejects single-factor explanations: there are four entangled factors (sticks, slots/positions, stick pairing/channel topology, CPU memory controller). Max wants to isolate which factor causes the freezes via systematic slot/stick swap experiments, running 100%-load RAM stress tests (20 rounds each), with per-round bad-word reporting and crash counting. Ultimately: find a stable configuration without buying new hardware.

---

## DECISIONS MADE + WHY

**1. Rejected "bad stick" as sole explanation**
Earlier testing showed all 4 sticks pass solo at low load, but fail together at high load. Max insists on multifactor thinking - position, slots, sticks, and processor are all live suspects. No single component is convicted.

**2. Test protocol settled**
- Tool: `/home/maxre/ramscan <GB> <passes>` (custom March-type C memory tester, 8 passes per run, reports `bad_words=N`)
- "100% load" = max safe load that won't trigger Linux OOM-killer (~85-90% of installed RAM; leaves ~2GB OS headroom)
- Each test = 20 rounds, reboot-survivable (guard cron relaunches after crash, boot logger counts freezes)
- Per-round reporting of bad_words and crashes

**3. Phase A ? Phase B switch**
Early tests varied which STICKS were installed. After stick 1+4 proved disastrous (11 crashes), Max shifted to fixing known-good sticks 2+3 and varying SLOTS to isolate bad slots.

**4. Load matters - not just "bad" vs "good"**
Fault only appears above ~27GB load. A clean result at low load (12-13GB) is inconclusive - it may just be below the trigger threshold. This is why solo-stick tests (16GB ? only ~12GB loadable) can't clear a stick or slot.

**5. OOM trap learned**
First 48GB test used 45GB load ? OOM-killer fired, contaminated the test. Now load is always sized with OS headroom. Max's theory that a concurrent transcription-software install ate headroom and caused the v1 freeze is plausible and supported.

**6. Web research validated**
- Bit-flips (bad_words measured by a March test) are real memory corruption, not an overload artifact
- memtest86+ (boot-level, no OS) is the gold-standard confound-free test; our Linux-based ramscan is a stress probe
- Pros combine MemTest86 with real-workload stress (Prime95 Blend, stressapptest, or actual genomics jobs)

**7. History now saved**
Full experiment table saved to `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` (committed + pushed). Survives compaction.

---

## CURRENT STATE

**Slot 3+4 test (sticks 2+3, 32GB box, 27GB load, 20 rounds) is RUNNING RIGHT NOW on Sol.**
- Launched at ~13:06 PDT via `/home/maxre/relaunch34.sh`
- Round 1 in progress, 0 crashes
- Monitor watcher (`sol_mon34_watch.sh`, background ID pending) logging to `C:\claude_base\worklog\sol_mon34_watch.log` every 90s, auto-disarms on crash
- Sol is up, stable, watchdog armed

**Full experiment history (hard facts only - Max's framing):**

| Config | Load | Result |
|---|---|---|
| All 4 sticks, 64GB | 50GB soak | Froze at pass 16 |
| 3 sticks (1,2,4), 48GB | 36GB/75% | Flip scale R3=391, no freeze |
| Each stick SOLO, 16GB | 12GB | All 4 clean (inconclusive - low load) |
| Sticks 1+2, slots 1+2 | 24GB/75% | **CLEAN 20/20** |
| Sticks 2+3, slots 1+2 | 40/75% | Marginal (~2 crashes, some flips) |
| **Sticks 1+4, slots 1+4** | 40/75% | **DISASTER - 11 crashes, flips nearly every run** |
| Sticks 2+3+4, slots 1+2+3, 48GB | 42GB | R2=52, R3=84 flips, **FROZE R4** |
| Sticks 2+3, slots 1+3 (green) | 27GB | **CLEAN 20/20** |
| Sticks 2+3, slots 2+4 | 27GB | R3=4, R4=2 flips, **FROZE R5** |
| Sticks 2+3, **slots 3+4 (RUNNING)** | 27GB | Round 1 in progress |

**Key pattern:** same sticks 2+3 at same 27GB load - slots 1+3 perfect, slots 2+4 failed. This implicates slot 2 (or slot 4, or the pairing topology) as the fault, not the sticks. Slots 3+4 is the decider.

---

## EXACT NEXT STEP

The **slots 3+4 test** is already running. The immediate next actions for the cold session:

1. **Read `C:\claude_base\worklog\sol_mon34_watch.log`** to see current round, bad_words per round, and crash count.
2. **If test is still running:** continue reporting each round's bad_words sum to Max. Re-arm the per-round timer (~3-4 min per 27GB round).
3. **If test completed (20/20):**
   - **Clean (0 flips, 0 crashes):** slot 2 is the confirmed culprit (slots 1+3 clean, slots 3+4 clean - only slot 2 in the failed configs 1+2+3 and 2+4). Stable config found: slots 3+4 or 1+3 at 32GB. Report to Max.
   - **Flips/freeze:** slot 4 is also bad (or the pairing/slot topology matters more than one bad slot). Max will decide next swap.
4. **If Sol froze:** the watcher auto-disarms (removes campaign.run, kills ramscan). When Sol comes back (watchdog or Max power-cycle), confirm it's idle, then report crash round + bad_words at death.

**Whatever the result, update the experiment history table doc** at `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` and the durable worklog.

---

## OPEN QUESTIONS AWAITING MAX

- **None actively pending** - Max is driving the swap decisions in real time. The only unasked question is what he wants to do after the slots-3+4 verdict (likely: if clean, settle on a stable config; if bad, further swaps).
- The **memtest86+** option (boot-level, no OS confound) has been surfaced repeatedly but Max hasn't chosen to do it - it requires him at Sol's console for ~2 min.

---

## KEY PATHS, IDs, COMMANDS

**Sol:**
- SSH: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`
- Sudo password: `SM2w3e4r5t6y=` (file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\sol_sudo_password_20260523.txt`)
- Remote sudo pattern: `ssh ... 'PW="SM2w3e4r5t6y="; echo "$PW" | sudo -S -p "" <cmd>'` (PW set INSIDE remote quotes)

**Test infrastructure on Sol:**
- `/home/maxre/ramscan` - the C memory tester binary
- `/home/maxre/campaign.sh` - the test loop (loads via `for gb in <N>; do`, reads cap from `campaign_maxrounds`, increments `campaign_round.cnt`, logs to `campaign32.log`)
- `/home/maxre/campaign.run` - flag file (test runs while this exists)
- `/home/maxre/campaign_guard.sh` - cron-launched relauncher
- `/home/maxre/campaign32.log` - RESULT lines: `RESULT ROUND n LOAD xGB bad_words=N HH:MM:SS`
- `/home/maxre/campaign_boots.log` - crash log: `BOOT <timestamp>` lines; `grep -c "^BOOT"` = crash count
- Campaign crons (Sol crontab): `@reboot sleep 30; /home/maxre/campaign_guard.sh`, `*/2 * * * * /home/maxre/campaign_guard.sh`, `@reboot date... | xargs -I{} echo BOOT {} >> campaign_boots.log`
- `/home/maxre/relaunch34.sh` - last used clean-launch script for the slots 3+4 test

**Poll command (one-liner for status):**
```
ssh -i ~/.ssh/sol_key -o ConnectTimeout=20 maxre@192.168.1.113 'echo -n "crashes="; grep -c "^BOOT" campaign_boots.log; echo -n " round="; cat campaign_round.cnt; echo -n " flips_nonzero="; grep RESULT campaign32.log | grep -vc "bad_words=0 "; pgrep -f "bash /home/maxre/campaign.sh" >/dev/null && echo " ALIVE" || echo " DEAD"'
```

**Current monitor watcher (may still be running):**
- Script: `C:\claude_base\worklog\sol_mon34_watch.sh`
- Log: `C:\claude_base\worklog\sol_mon34_watch.log`
- Background task ID: check `TaskList` for the most recent watcher

**Local files:**
- Worklog: `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` (durable, survives compaction)
- Experiment history table: `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` (committed + pushed)
- Watch logs: `C:\claude_base\worklog\sol_*_watch*.log`
- ramscan source: `C:\claude_base\tools\sol_resilience\ramscan.c`
- bcast identity: **E1sol** (E team, off B board)
- Worktree: `C:\claude_base\.claude\worktrees\jovial-chaum-26dd4b`

---

## GOTCHAS

1. **SSH exit 255 doesn't always mean Sol froze.** During heavy load, SSH starves and drops. Also, `pkill` commands race the connection. Always re-verify with a fresh SSH before concluding "frozen." If Sol is truly frozen, SSH times out repeatedly.

2. **OOM-killer trap:** Never set ramscan load closer than ~2GB to MemTotal. On 32GB, max safe = 27GB. On 16GB, max = 12GB. On 48GB, max = 42GB. The OOM-killer kills ramscan and contaminates the test.

3. **Post-reboot garbage rounds:** If the campaign relaunches after a freeze, the round counter may increment to garbage values (rounds completing instantly with bad_words=NA). These are artifacts - only the pre-freeze rounds are real data.

4. **Watcher false-crash on swap-reboot:** The boot logger stamps a BOOT line on every boot (including Max's manual power-cycle for a swap). Watchers that compare crash-count to detect freezes will false-trip on a swap-reboot. Always check uptime and context before disarming.

5. **Solo-stick tests are inconclusive if clean:** 16GB ? only ~12GB loadable, below the ~27GB+ where flips appear. A clean solo test doesn't clear a stick or slot.

6. **Compaction kills the timer:** The ScheduleWakeup dynamic loop requires re-arming each turn. After compaction, the session forgets to re-arm. The durable worklog contains the state to resume from.

7. **Max reads short, leads with TLDR:** All responses to Max should be ~100-300 chars, TLDR first with `# ? **tldr** ?` markers. Plain English, no code dumps. But he wants precise, honest answers - never gloss over errors or overclaim.
