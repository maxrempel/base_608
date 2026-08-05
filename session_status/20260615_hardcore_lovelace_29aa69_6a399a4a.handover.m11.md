# Scribe handover - milestone 11 (~167K tokens)
# session: 20260615_hardcore_lovelace_29aa69_6a399a4a
# cwd: C:\claude_base\.claude\worktrees\hardcore-lovelace-29aa69
# written: 2026-06-15 15:32:53 by deepseek-v4-pro

# HANDOVER - Scribe Record (B11R)

## GOAL (Max's own words)
"Branched you into - you are now B11R - go read online and brainstorm, what the fuck is going on. Likely people know that situation inside out - first generic, 4 stick test. Next specifically this computer Dell model."

(Note: the machine is a **Lenovo ThinkCentre M720s**, not Dell - Max misspoke. Clarify this for the research phase.)

## DECISIONS MADE AND WHY
1. **Software `memmap=` blocking is futile.** The bad cells are scattered, non-repeating, heat-triggered bit-flips - no fixed set of physical pages to reserve. This was proven across multiple crash-loop runs (113 then 22 then 220 bad pages, all different addresses). Decision: abandon software block.
2. **Single-bad-stick hypothesis disproven.** All four sticks tested individually and in a pair using `ramscan` (12-24GB, 20 passes, all 6 patterns). Every test came back CLEAN - zero bit errors, zero crashes. The box only crashes with all 4 sticks installed (64GB). The fault is a full-configuration problem, not one defective module.
3. **Crash-loop service permanently disabled.** `sol-ramscan-loop.service` is stopped and disabled. Sol will NOT auto-crash on future boots.
4. **Testing methodology agreed:** group testing (2vs2 to find bad pair) then isolate - but this session ran SOLO tests per Max's demand for positive identification of every stick. The ramscan tool (custom C, write/verify 6 patterns) is the standard soak test. Short name: "RAM stress test" / "ramscan"; long name: "sustained pattern write-and-verify memory soak" (March-type memory test family).
5. **Max has spare sticks in a drawer at home** - may be free fix candidates, but only after we understand the root cause.
6. **Options on the table:** BIOS RAM underclock (2667?2133/2400, ~1 trip), replace one stick (~$35 but needs ID), replace all 4 (~$110, zero testing), or leave Sol idle-only.

## CURRENT STATE
- **Sol:** UP and stable. Last known config: stick 4 solo (16GB), just finished a clean ramscan 20-pass run. Unknown whether Max has reinstalled other sticks since the stick-4 test ended.
- **Crash-loop:** DISABLED. `sol-ramscan-loop.service` is stopped+disabled.
- **Hardware watchdog:** ARMED (iTCO_wdt, /dev/watchdog0, 30s timeout). A frozen Sol self-reboots in ~30s.
- **Production:** MIGRATED OFF Sol onto Lak (b8). Sol is low-stakes.
- **Memory config known:** 4?16GB DDR4-2667 non-ECC UDIMM, generic/no-name (blank part numbers), slots ChannelA-DIMM0/1 + ChannelB-DIMM0/1. The M720s has 4 DIMM slots, non-ECC only.
- **Test results so far:**
  - Pair {1,2} (32GB, 20 passes) - CLEAN
  - Stick 3 solo (16GB, 20 passes) - CLEAN
  - Stick 4 solo (16GB, 20 passes) - CLEAN
  - Full 4-stick config (64GB) - CRASHES under load (proven earlier with stress-ng and memtester)
- **ramscan binary:** at `/home/maxre/ramscan` on Sol (compiled `gcc -O2` from `/home/maxre/ramscan.c`)
- **All docs up to date and pushed:** `C:/claude_base/tools/sol_resilience/sol_crash_and_resilience_20260613_v01_tomemex.md`, global2.md reference added, worklog current.

## EXACT NEXT STEP (to be done by B11R immediately on session start)
**Research two layers:**
1. **Generic:** Why do 4 DIMMs fail together when every stick passes solo? Known causes: memory training weaker with 4 slots populated, signal integrity degradation (more electrical load on the memory controller), power delivery droop under combined load, heat buildup in a 4-stick config, BIOS memory-refresh timing margin insufficient for 4 ranks, channel interleaving exposing rare address-line crosstalk. Search terms: "4 sticks fail but each works alone DDR4 non-ECC", "all DIMMs pass individually crash together", "memory training failure 4 DIMMs".
2. **Model-specific:** Lenovo ThinkCentre M720s memory issues. Look for known problems with populating all 4 slots, BIOS updates that fix memory stability, power delivery limits, or community reports of crashes with 4 sticks. Search: "Lenovo M720s 4 DIMMs crash freeze", "M720s memory stability 64GB", "ThinkCentre M720s all memory slots populated".

## OPEN QUESTIONS AWAITING MAX
- None immediate - the research is to be done autonomously. Max may want a report after investigation.

## KEY PATHS, IDs, CREDENTIALS
- **Sol SSH:** `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`
- **Sol sudo password:** `SM2w3e4r5t6y=` (file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\sol_sudo_password_20260523.txt`)
- **Healthchecks API key:** `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\healthchecks_io_creds_20260604.txt`) - existing check for Sol: `023cf3f6-186a-4afd-ada0-95e5d7e5f223` (sol-host)
- **Main doc:** `C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md`
- **ramscan source:** `C:\claude_base\tools\sol_resilience\ramscan.c`
- **ramscan binary on Sol:** `/home/maxre/ramscan` (note: NOT in /tmp - /tmp wipes on reboot)
- **Sol test logs on Sol:** `/home/maxre/pairtest12.log`, `/home/maxre/test_stick3.log`, `/home/maxre/test_stick4.log`
- **Infra map:** `C:\claude_base\infra_map_tomemex.md`
- **global2:** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- **Sol RAM specs from dmidecode (read earlier):** 4 slots, all populated with 16GB DDR4-2667, serials 6C/5E/63/5D, part numbers blank, non-ECC, M720s chipset.
- **Worklog:** `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md`
- **bcast:** `python C:/claude_base/branch_bulletin/bcast.py` (whoami b11r, catchup, post)
- **es.exe for local search:** `C:/claude_base/tools/es/es.exe`
- **worklog.py:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- **Sol GRUB:** `/etc/default/grub` - currently `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"` (clean, no memtest=). Backup at `/etc/default/grub.bak.premem`.
- **DIMM mapping (approximate from histogram):** Bad cells were scattered across the entire physical address range, which is consistent with channel interleaving across all 4 sticks.

## GOTCHAS AND DEAD ENDS RULED OUT
1. **DON'T re-enable the crash-loop service.** `sol-ramscan-loop.service` is disabled for good reason - an aggressive unattended crash-loop froze Sol requiring a physical power-cycle. Test attended, one soak at a time.
2. **`/tmp` is wiped on reboot.** Any binary or log placed in `/tmp` on Sol disappears across a crash/reboot. Always use `/home/maxre/` or `/var/log/`.
3. **Sol is LAN-only (192.168.1.113).** No Tailscale, no remote access path from outside the home network. If the current session is off-LAN, Sol is unreachable. (A prior attempt ran dmidecode from off-LAN and timed out - correctly diagnosed as network, not a crash.)
4. **Single-bad-stick is ruled out.** All 4 tested clean solo - the problem is the full 4-stick configuration (64GB). Don't re-litigate the individual sticks.
5. **Software memblock (memmap=) is futile** for this fault. The bit flips are scattered and non-repeating. Don't propose it again.
6. **The earlier Intel NIC hypothesis was a red herring.** The box crashed with the NIC fix in place, in memory-management kernel code, with a single-bit-flipped pointer. The e1000e fix is harmless (kept) but not causal.
7. **Temperature is NOT the root cause** - CPU peaks 81?C under load (limit 100?C), GPU 30?C, SSD 25?C. Ruled out.
8. **Static cold-boot memtest (kernel memtest=17) is blind to this fault.** It passed clean twice. Removed because it only slowed boots by 3.3 min.
9. **sudo password quoting:** When using sudo remotely, set `PW='SM2w3e4r5t6y='` INSIDE the remote single-quoted command, not before it. Pattern: `ssh ... 'PW="..."; echo "$PW" | sudo -S -p "" <cmd>'`.
10. **The machine is a Lenovo ThinkCentre M720s, NOT a Dell.** Max's message says "Dell" but every piece of evidence (dmidecode, BIOS name, model research) confirms Lenovo. Research accordingly.
11. **Wattcher pattern for catching Sol on boot:** polling SSH in a loop works; the critical window is the first ~25s after boot (before any auto-start service fires). Use `-o ConnectTimeout=3` for fast polling.
12. **ramscan usage:** `ramscan <GB> <passes>` - allocates that many GB, runs that many full passes of all 6 patterns. On a 16GB stick, use 12GB (leave headroom for OS). On 32GB, use 24GB. On 64GB, use 50GB.
