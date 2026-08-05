# Scribe handover - milestone 11 (~167K tokens)
# session: 20260616_brave_feynman_abba7a_e1b2e811
# cwd: C:\claude_base\.claude\worktrees\brave-feynman-abba7a
# written: 2026-06-16 17:57:02 by deepseek-v4-pro

# HANDOVER - Sol RAM Diagnosis, Session 2026-06-13 through 2026-06-16

---

## GOAL (Max's own words, closing message)

Max discovered the sticks at **positions 1 and 4** might be the problem. He is now re-running the **40%/75% alternating load test continuously for 10 rounds**, with sticks installed in **positions 1 and 2** (described as "green and blue"). He asks: *"What is the model and what do you know about stick positions. It says 1234."*

---

## DECISIONS MADE + WHY

### Root cause confirmed: non-ECC RAM instability under load
- Sol's freezes were **NOT one dead stick**. Every stick tested clean **alone** and in **clean pairs** - the fault only appears when multiple DIMMs are populated and the memory controller is driven hard.
- The failure signature is **signal-integrity / DIMM-population overload**: the ThinkCentre M720s memory controller cannot cleanly drive multiple DIMMs per channel at DDR4-2667. Errors scale with stick count: 2 sticks ? clean, 3 sticks = intermittent flips, 4 sticks = thousands of errors + hard freeze.
- **Heat/cooling is ruled out** - CPU temps never exceeded 66?C under full load (crit is 100?C).
- **NIC was a red herring** - the Intel I219-V e1000e TSO/GSO fix was applied and the box still froze. That fix was kept as harmless but the real cause is RAM.
- **Sol is untrustworthy for genomics** - Max explicitly stated "no trust" and the box was retired from real computation. It's viable only as a light server (file serving, cron, low-RAM tasks).

### Hardware watchdog fix (kept)
- Ubuntu HWE kernel deny-lists the `iTCO_wdt` module at `/lib/modprobe.d/blacklist_linux-hwe-6.17_*.conf`. A force-load systemd service (`/etc/systemd/system/itco-wdt.service`) was created to bypass this on every boot. `/dev/watchdog0` is live with a 30s timeout. This makes Sol auto-reboot on freeze instead of staying dead. **Boot-persistence NOT yet reboot-verified.**

### Diagnostic tools created
- **ramscan.c** - custom C March-type memory tester. Built because off-the-shelf tools (stress-ng, memtester) either crash without reporting the failing address, or report virtual addresses that can't be mapped to physical pages for the badram/memmap blocking approach. Compiled to `/home/maxre/ramscan` on Sol. Usage: `ramscan <GB> <passes>`. Prints `bad_words=N` per run. Source: `C:\claude_base\tools\sol_resilience\ramscan.c`.

### Software memory-blocking deemed futile
- The bad cells are **scattered and never repeat the same physical addresses**. They're heat/load-triggered, not hard-stuck - so there's no fixed list to block via `memmap=` or `badram`. Max and I both accepted software blocking won't work here.

### Testing methodology
- **Group testing / positive identification**: to isolate a bad stick among 4 requires 3 boots (Max's scheme: 2v2 to find the bad pair, then test each of that pair solo). Positive ID of all sticks = 3 rounds.
- **Alternating-load campaign**: `campaign.sh` on Sol loops `ramscan 13 8` (40% of installed RAM) and `ramscan 24 8` (75% of installed RAM), logs bad-words per run to `/home/maxre/campaign32.log`, counts crashes via `/home/maxre/campaign_boots.log`. Controlled by flag file `/home/maxre/campaign.run` (remove it to stop gracefully).

### Stick position discovery (the key pivot)
- At the very end of the session, Max realized the problem correlates with **physical slot positions**, not just which sticks are installed. Slots are numbered 1-2-3-4 on the M720s board. Positions 1 and 4 "might be a problem." He is now testing sticks in positions **1 and 2** (green and blue sticks). This shifts the diagnosis from "bad sticks" to "bad slots" or "bad slot combinations."

---

## CURRENT STATE

### Sol hardware
- Lenovo ThinkCentre M720s, Intel i7-9700, 4? DDR4 DIMM slots (numbered 1-2-3-4 on the board)
- 4?16GB DDR4-2667 non-ECC UDIMMs (generic, blank part numbers, serials 6C/5E/63/5D)
- **Max's color coding:** at least two sticks are described as "green" and "blue" - these are now in slots 1 and 2
- Cover is **OFF** (left open for slightly better cooling during testing)
- OS: Ubuntu 24.04 HWE, kernel 6.17.0-35-generic
- IP: 192.168.1.113, user maxre, SSH key at `~/.ssh/sol_key`
- Sudo password: `SM2w3e4r5t6y=` (stored in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\sol_sudo_password_20260523.txt`)

### Test campaign
- **STATUS:** Max says it is **RE-RUNNING** - 40%/75% alternating load, 10 rounds, on sticks in positions 1 and 2
- The campaign infrastructure (campaign.sh, campaign.run flag, cron guards) was **stopped and cleaned up** at the end of the prior session, so Max either reinstated it or started a fresh run
- Prior results with pair 2+3 (in unknown positions): 2 crashes, low bit-flips at 75%, clean at 40%
- Prior results with pair 1+4 (in unknown positions): 11 crashes in ~50 min even at 40%

### Sol reliability verdict
- **Dead for genomics.** Max stated "no trust." Box freezes whenever a significant fraction of RAM is in active use.
- **Viable as light server** - file serving, backups, cron, small apps that don't fill RAM.
- **Watchdog armed** - a freeze now auto-reboots in ~30s instead of staying dead.

### Team / identity
- This session is registered as **E1sol** on the E-team bcast board (moved off B-team where siblings were working on unrelated song-catalog tasks).
- Worklog at `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` has all milestones logged for compaction survival.

---

## EXACT NEXT STEP

Max is actively re-running the test on sticks in positions 1 and 2. The immediate task when the cold session picks up:

1. **SSH into Sol** (`ssh -i ~/.ssh/sol_key maxre@192.168.1.113`) and confirm it's up and the test is running. Check `pgrep -af campaign.sh` or `pgrep -af ramscan`.
2. **Read the current running table** from `/home/maxre/campaign32.log` (grep for RESULT lines) and `/home/maxre/campaign_boots.log` (grep for BOOT lines to count crashes).
3. **Report to Max** the per-load results (40% vs 75% bad-words, crash count) for the positions-1+2 configuration.
4. **Answer Max's question about stick positions:** The M720s has 4 DIMM slots on the motherboard, likely labeled 1-2-3-4 physically. In a typical dual-channel layout, slots 1 and 2 are one channel (Channel A), slots 3 and 4 are the other (Channel B). If positions 1 and 4 "are a problem" while 1+2 work, that points to **slot 4 being bad** or a cross-channel issue. The cold session should read the actual slot population via `sudo dmidecode --type memory` (sudo password above) to map which physical slot is ChannelA-DIMM0, ChannelA-DIMM1, ChannelB-DIMM0, ChannelB-DIMM1 - this reveals whether the bad slots share a channel.

---

## OPEN QUESTIONS AWAITING MAX

- Did the **BIOS visit** reveal any memory-speed setting? (M720s BIOS is locked-down; probably no speed control was found.)
- Are there **spare sticks in a drawer** at home? (Max said he might have 2 leftover from a past upgrade - worth checking before any purchase.)
- Should the **cover stay off** (slightly better cooling) during continued testing?
- Does Max want to **order a 2?32GB DDR4-2667 kit** (~$80-120) as the real fix? One DIMM per channel cuts the electrical load that's causing the freezes, and gives stable 64GB. Search term: "64GB (2x32GB) DDR4-2666 UDIMM non-ECC desktop kit."

---

## KEY FILE PATHS AND IDs

### On Sol (192.168.1.113, user maxre)
- `/home/maxre/ramscan` - compiled C memory tester binary
- `/home/maxre/campaign.sh` - alternating-load test loop script
- `/home/maxre/campaign32.log` - per-run RESULT lines (bad_words per load level)
- `/home/maxre/campaign_boots.log` - crash/reboot counter (BOOT timestamps)
- `/home/maxre/campaign.run` - flag file; exists = campaign should run; remove to stop
- `/home/maxre/campaign_guard.sh` - cron-launched wrapper that relaunches campaign if flag present
- `/etc/systemd/system/itco-wdt.service` - force-loads iTCO_wdt watchdog (boot-persistent, enabled)
- `/etc/default/grub` - currently `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"` (memtest=17 was added then removed)
- `/var/log/sol_ramscan/` - archived logs from prior failed mapping attempts (badpages.txt, run logs)

### On Pine (C:\claude_base)
- `C:\claude_base\tools\sol_resilience\ramscan.c` - source of the memory tester
- `C:\claude_base\tools\sol_resilience\sol_ram_stick_isolation_20260615_v01_tomemex.md` - earlier report (all-4-sticks-clean-individually finding)
- `C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md` - canonical resilience doc (watchdog fix, e1000e, crash timeline, temp mapping, sequential isolation results)
- `C:\claude_base\tools\sol_resilience\sol_panic_badram_20260613_1545.txt` - saved kernel panic evidence
- `C:\claude_base\tools\sol_resilience\sol_stress_seq.sh` - earlier sequential stress orchestrator (reboot-survivable)
- `C:\claude_base\tools\sol_resilience\sol-ramscan-loop.service` - earlier aggressive mapper service (**MUST STAY DISABLED**)
- `C:\claude_base\infra_map_tomemex.md` - infra map (updated with watchdog and freeze incident history)
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - has a "SOL FREEZES = BAD RAM" reference block
- `C:\Users\maxre\Nextcloud\zSyncMain\ssh\sol_sudo_password_20260523.txt` - sudo password
- `C:\Users\maxre\Nextcloud\zSyncMain\ssh\healthchecks_io_creds_20260604.txt` - Healthchecks API key
- Worklog: `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md`

### Sol SSH
- Command: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`
- Remote sudo pattern: set PW **inside** the remote single-quoted command: `ssh ... maxre@... 'PW="SM2w3e4r5t6y="; echo "$PW" | sudo -S -p "" <cmd>'`

---

## GOTCHAS AND DEAD ENDS

1. **Static memtest is blind to this fault.** `memtest=17` in GRUB passed clean 2? because the fault is heat/load-triggered, not a hard-stuck cell. It was removed - don't re-add it.

2. **Software memmap/badram blocking is futile.** The bad cells move every run (scattered, non-repeating physical addresses). There's no fixed list to reserve.

3. **ramscan binary must live outside /tmp.** `/tmp` is wiped on every reboot. The binary is at `/home/maxre/ramscan` (persistent). Any new binary deployment must go to `/home/maxre/`, not `/tmp/`.

4. **sol-ramscan-loop.service MUST STAY DISABLED.** That was the aggressive self-rebooting crash-loop mapper that froze Sol hard and needed a physical power-cycle. Do not re-enable it.

5. **Sol has NO remote power control.** No IPMI, no Wake-on-LAN setup. A hard freeze that outlasts the watchdog needs a physical power-button press.

6. **The campaign cron guards were stripped.** If Max is re-running the test now, he may have set up fresh cron entries or a manual launch. Don't assume the old auto-relaunch mechanism is still wired - check.

7. **SSH drops during `pkill` are normal.** Killing ramscan or campaign.sh mid-connection often races the SSH session. Always follow up with a separate verification command to confirm state.

8. **Watcher false-crash bug pattern.** Any background watcher that ends its remote ssh command with `grep -c SOMETHING` will report "SSH-FAIL" when grep finds zero matches (exit code 1). Always end watcher remote commands with `; true` to avoid this.

9. **bcast identity is lost on compaction.** After any context compaction, re-adopt the E-team identity: `python "C:/claude_base/branch_bulletin/bcast.py" whoami e1sol`.

10. **Cover is OFF.** Sol's case is open (Max was lazy to close it). This means
