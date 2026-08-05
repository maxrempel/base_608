
## [2026-06-13 15:09] b11 db0f1c86
- DID: Joined b-team as b11; Sol went DOWN (2nd time in ~3 days), Max force-rebooted ~14:53. Now autonomous investigating crash cause + log sync.
- STATE: Sol back up. Need: boot/crash history, temps, ensure watchdog logs sync OFF Sol, document.
- NEXT: SSH Sol: journalctl --list-boots, last -x, sensors, check why it dropped off network. Set up off-box log sync.

## [2026-06-13 15:19] b11 db0f1c86
- DID: Sol crash investig DONE: froze 14:49 Jun13 (3rd freeze: Jun9,12,13), no log cause=hard hang, temps fine. KEY: hw watchdog iTCO_wdt was INERT - DENY-LISTED by kmod so systemd skips it at boot; that's why 06-10 watchdog 'fix' never held + Sol stays dead on freeze. Manually modprobe'd it NOW (live, /dev/watchdog0, RuntimeWatchdogSec=30s). Removed my duplicate monitoring (existing sol_heartbeat.sh+sol-cpu-temp+sol-host 023cf3f6 already live).
- STATE: Watchdog LIVE now but NOT boot-persistent yet - deny-list still blocks it on reboot. Need to find+remove deny-list file (grep iTCO_wdt in /lib /usr/lib /etc modprobe.d).
- NEXT: 1)find deny-list, remove it 2)reboot-test or update-initramfs 3)fix infra_map L104-118 (watchdog was inert+add Jun12/13 incidents) 4)slim doc C:/claude_base/tools/sol_resilience/ 5)bcast 6)verify

## [2026-06-13 15:20] b11 db0f1c86
- DID: Watchdog now BOOT-PERSISTENT: deny-list was Ubuntu HWE /lib/modprobe.d/blacklist_linux-hwe-6.17_*. Fixed via /etc/systemd/system/itco-wdt.service (force-loads iTCO_wdt by name, ignores blacklist, + daemon-reexec to rearm). Enabled+live now (/dev/watchdog0, 30s). Removed dead /etc/modules-load.d/{itco_wdt,watchdog}.conf. Did NOT reboot (b-team worker running) so boot-path unverified but logic proven by manual run.
- STATE: Sol hardened: hw watchdog auto-reboots a freeze in 30s, persists across reboots. Existing monitoring (sol_heartbeat 023cf3f6 + sol-cpu-temp) untouched+healthy.
- NEXT: REMAINING: (1) FIX infra_map L104-118 - currently FALSELY says watchdog works; correct to deny-list story+service+add Jun12&13 freeze incidents. (2) slim doc C:/claude_base/tools/sol_resilience/...v01. (3) next Sol reboot: verify /dev/watchdog0 auto-appears.

## [2026-06-13 15:22] b11 db0f1c86
- DID: TIMELINE CORRECTION: Sol froze 14:49:08 PDT Jun13; Max force-restarted ~15:00 (actual boot 15:00:31, not the ~14:53 I earlier guessed); Max said so ~15:07. Watchdog fix + docs all stand correct.
- STATE: Resilience task done; autonomous timer armed for ~15:26 stability check.
- NEXT: Wake: verify Sol uptime/no new freeze, /dev/watchdog0, itco-wdt.service enabled; if stable, bcast solved + stop timer.

## [2026-06-13 15:27] b11 db0f1c86
- DID: Tested Max's 'Sol just lost ssh, stayed alive' hypothesis -- DISPROVEN. Proven TRUE FREEZE: local cron AND outbound Healthchecks pings both went silent at the same instant 14:49 PDT (last cron 14:45:01, last ping 14:45:02 UTC21:45; gap until force-reboot 15:00:31 / ping resume 15:05). A box that lost only sshd keeps logging cron locally + keeps pinging out; only-net-loss still logs cron locally. Both silent = full userspace hang. Updated resilience doc with the dual-silence proof.
- STATE: Sol up 24min, /dev/watchdog0 present, itco-wdt.service enabled, temp 37C. Watchdog fix is the correct recovery for a freeze (would have reset Sol in ~30s vs 11min dead). ssh-self-restart NOT added: cannot run during a true freeze.
- NEXT: Rearm 4-min timer per Max; on autonomous drive investigate freeze-FREQUENCY root cause (3 hangs in 4 days) -- scan kernel ring across boots for recurring pre-hang signature (i915/ACPI/hung_task/disk-reset). Confirm watchdog boot-persistence on next real reboot.
- LESSON: A true freeze is provable without any panic trace: if BOTH local cron logging and outbound dead-man pings stop at the same second, userspace hung. ssh-only or net-only loss each leaves one of the two still alive.

## [2026-06-13 15:28] b11 db0f1c86
- DID: Autonomous wake: Sol stable (up 27min, watchdog live+enabled, no new freeze). Freeze-frequency scan of 4 boots' kernel rings = NO recurring pre-hang signature (hard hang logs nothing before dying); deno segfaults were unrelated noise 9min prior. Suspects nvidia/PSU/RAM unprovable from logs. Added that to resilience doc; committed+pushed (master 45baf62f). b8 migrated production off Sol to Lak so hardware-trigger chase is low priority.
- STATE: TASK DONE. Sol hardened (hw watchdog auto-reboots a freeze in 30s, boot-persistent via itco-wdt.service), proven a true freeze not ssh-drop, root-cause-of-frequency unprovable from logs + now low-stakes (prod moved to Lak). Docs+infra_map updated, committed, pushed. Existing monitoring untouched.
- NEXT: DONE -- stopping autonomous timer (no more ScheduleWakeup). Only open item, unforceable: confirm /dev/watchdog0 auto-appears on Sol's NEXT real reboot.

## [2026-06-13 15:50] b11 db0f1c86
- DID: Stress test REPRODUCED Sol crash 15:44; armed panic_on_oops caught it. Root cause FOUND = BAD RAM: kernel GPF on single-bit-flipped pointer (0xfeff vs 0xffff) in page-free path, triggered by stress-ng-vm memory stressor on non-ECC RAM. Not NIC/thermal/PSU. Saved panic dmesg evidence (sol_panic_badram_20260613_1545.txt), documented in resilience doc + referenced in global2, committed+pushed (4481bdbf). Cleared apport GUI crash popup remotely.
- STATE: Sol back up on its own (panic=10 auto-reboot worked). Investigation COMPLETE. Only remaining fix needs Max at console.
- NEXT: Wait for Max to answer green-Q (keep stress-testing vs stop). Real fix = memtest86+ at Sol console to pinpoint+pull bad DIMM. Do NOT re-run stress (crashes Sol, no new info).
- LESSON: panic_on_oops=1 + pstore converts a silent freeze into a captured panic on the first crash - the single most valuable diagnostic to arm on any silently-freezing Linux box.

## [2026-06-13 16:15] b11 db0f1c86
- DID: Sequential isolation test COMPLETE + conclusive. RESULTS.txt: cpu SURVIVED (5min full load, no crash), memory CRASHED Sol ~2.5min, combo CRASHED. Service self-disabled, Sol idle (load 0.14), watchdog armed. Verdict = BAD RAM, confirmed 2 ways (single-bit-flip panic + cpu-safe/memory-crashes isolation). Doc updated, committed+pushed bc68cf8d. global2 referenced.
- STATE: Sol idle-stable, investigation DONE. Nothing more actionable remotely - only fix left needs Max at console.
- NEXT: Max back ~16:35. Real fix = boot memtest86+ at Sol console, pinpoint+pull bad DIMM. Until then keep Sol idle/low-stakes (production already on Lak). Keep 4-min timer per Max; ticks now idle no-ops.

## [2026-06-13 16:40] b11 db0f1c86
- DID: Idle-watching post-completion. Sol stress investigation DONE: bad RAM confirmed 2 ways (single-bit-flip kernel panic 15:44 + sequential isolation: cpu SURVIVED, memory CRASHED, combo CRASHED). All committed+pushed (bc68cf8d), global2 referenced, harness self-disabled, Sol idle-stable (up ~25min load 0.05), watchdog armed.
- STATE: Investigation complete; nothing actionable remotely. Sol healthy idle.
- NEXT: ONLY remaining fix = Max boots memtest86+ at Sol console to pinpoint+pull bad DIMM (64GB->fine on 1-2 good sticks). Keep Sol idle/low-stakes meanwhile (production on Lak). Keeping 4-min timer per Max.

## [2026-06-13 17:08] b11 db0f1c86
- DID: Idle-watching, Sol stable up ~55min. Investigation fully DONE: bad RAM confirmed 2 ways (single-bit-flip panic + sequential isolation cpu-survives/memory-crashes). Everything committed+pushed (bc68cf8d), global2 has the SOL FREEZES=BAD RAM pointer, harness self-disabled.
- STATE: Complete. Nothing actionable remotely. Awaiting Max's return.
- NEXT: Only fix left = Max boots memtest86+ at Sol console, pull bad DIMM. Doc: C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md. Keep 4-min timer per Max.

## [2026-06-13 17:33] b11 db0f1c86
- DID: Idle-watching, Sol stable up ~1h15m, load 0.10. Sol freeze investigation COMPLETE: root cause = BAD RAM, confirmed 2 independent ways (1: 15:44 kernel panic with single-bit-flipped pointer 0xfeff vs 0xffff in page-free path under memory stressor on non-ECC RAM; 2: sequential isolation test - CPU-only SURVIVED 5min full load, memory-only CRASHED ~2.5min, combo CRASHED). All pushed (commit bc68cf8d). global2 has 'SOL FREEZES = BAD RAM' pointer block. Stress harness self-disabled. Watchdog armed.
- STATE: DONE. Nothing actionable remotely. Sol idle-stable. Autonomous 4-min timer running per Max.
- NEXT: ONLY remaining fix needs Max at Sol physical console: boot memtest86+ (in GRUB menu), >=2 passes, pull bad DIMM (64GB, fine on 1-2 good sticks). Full doc: C:\claude_base\tools\sol_resilience\sol_crash_and_resilience_20260613_v01_tomemex.md. Keep idle-watch + 4-min timer until Max returns/instructs.

## [2026-06-13 18:08] b11 db0f1c86
- DID: Set memtest=17 in Sol GRUB (/etc/default/grub, backup .bak.premem), update-grub ok, rebooted Sol 18:07:54 to run kernel early_memtest = maps AND reserves bad RAM pages on every boot, no physical pull needed
- STATE: Sol rebooting into memtest scan (offline ~5-30min during single-threaded 64GB x17-pattern scan). After boot: dmesg | grep -i memtest shows reserved bad ranges. Root cause already confirmed = bad DIMM (single-bit-flip panic + memory-stress-only crash). sudo pw file: zSyncMain/ssh/sol_sudo_password_20260523.txt
- NEXT: Autonomous: re-arm ~270s timer, wait for Sol SSH back, capture dmesg early_memtest results, accumulate bad-page map across repeated reboots until stable, keep memtest=17 in GRUB so bad pages stay blocked every boot
- LESSON: ssh remote sudo: set PW INSIDE the remote command (PW=..; echo $PW|sudo -S) - a locally-set var referenced as \ expands empty on the remote and sudo silently fails

## [2026-06-13 18:13] b11 db0f1c86
- DID: memtest pass1 result: CLEAN - kernel early_memtest ran 17 patterns over 64GB (~198s scan visible as gap in dmesg), reserved ZERO bad pages. Rebooted for pass2 18:13.
- STATE: memtest=17 permanent in GRUB. Pass1 clean = fault is intermittent/stress-triggered (matches stress-ng single-bit-flip evidence), NOT a hard stuck bit, so static memtest may never catch it. Honest limitation flagged to Max.
- NEXT: Keep rebooting passes to accumulate (Max said again+again). If still clean after several passes, the surer catches are memtest86+ at console OR physical stick swap - static testing is blind to load/heat-only flips.

## [2026-06-13 18:19] b11 db0f1c86
- DID: memtest static passes 1+2 BOTH CLEAN (confirmed static testing blind to this fault). Installed memtester, EDAC says No ECC (confirms non-ECC). Launched memtester 48G x5 loops as systemd transient unit sol-memtester, log /var/log/sol_memtester.log, capped timeout 3600, locked 48G ok, running.
- STATE: memtester = stress+report tool that prints FAILING ADDRESS (unlike stress-ng which only crashes). It may catch the load-triggered marginal cell OR crash Sol (panic_on_oops auto-reboots, log persists). memtest=17 stays permanent in GRUB to auto-block any hard stuck bit each boot.
- NEXT: Check /var/log/sol_memtester.log for FAILURE lines (= bad address found) or detect a crash/reboot (uptime reset). If found: record addr, that IS the map. If crash w/o find: relaunch. If clean after full run: report static+memtester both clean = remote mapping not feasible, real fix is stick-swap/memtest86+ at console.

## [2026-06-13 18:24] b11 db0f1c86
- DID: *** BAD RAM CAUGHT BY memtester WITHOUT CRASHING SOL *** Findings: (1) Stuck Address FAILURE @ buffer-offset 0x77d0dc2c8; (2) Solid Bits FAILURE 0x0100000000000000 != 0x0 @ offset 0x3645629c8 = single bit stuck high at bit56 = textbook single-bit error matching the kernel-panic fingerprint. Sol stayed UP (load 1.0, unit active), memtester still running its 5 loops.
- STATE: DEFINITIVE: failing DIMM confirmed a 3rd independent way (panic + stress-crash + now memtester reproducible single-bit error). memtester offsets are VIRTUAL (into its mlocked 48G buffer, differ each run via ASLR) so they DON'T give a permanent physical address to memmap-block. Permanent block = memtest=17 in GRUB (hard bits) + real cure = pull stick.
- NEXT: Let memtester finish 5 loops, collect ALL FAILURE lines for the fullest map. Then report to Max: bad RAM proven+partially mapped, but exact physical cell can't be pinned remotely (virtual offsets); fix = stick swap / memtest86+ at console. memtest=17 stays permanent.
- LESSON: memtester (userspace) CATCHES load-triggered marginal cells that kernel early_memtest (static, cold) misses - and reports the failing bit pattern without crashing. For non-ECC intermittent-flip diagnosis, memtester >> static memtest.

## [2026-06-13 18:35] b11 db0f1c86
- DID: Built ramscan.c (C tool, local: C:/claude_base/tools/sol_resilience/ramscan.c, on Sol /tmp/ramscan) = stresses RAM + translates failing virt->PHYSICAL addr via /proc/self/pagemap + per-GB histogram, so bad cells can be permanently reserved with kernel memmap= (software bad-sector remap, fully remote, no stick-pull). memtester earlier found 2.5MB of failures (RAM badly faulty).
- STATE: Sol CRASHED again mid-ramscan ~18:34 (4th confirmation: panic + stress-crash + memtester + now ramscan-crash). Fault is HEAT/TIME-dependent: cool 1-pass scan over 50G with patterns 0x00/ff/55/aa was CLEAN, only 0x01 caught 1 page, then box died. memtest=17 still in GRUB (slows every boot +3.3min, USELESS for this fault - REMOVE it). sudo pw: zSyncMain/ssh/sol_sudo_password_20260523.txt
- NEXT: On reboot: (1) REMOVE memtest=17 from /etc/default/grub (+update-grub) to speed reboots. (2) Run ramscan 50 12 (multi-pass, builds heat) to map full bad region + physical histogram. (3) If bad pages cluster in one stick-sized contiguous range -> memmap= reserve whole range (= disable stick in SW, leaves 48G). If scattered by channel-interleave -> memmap= reserve individual bad pages. Max wants fully-remote, hates stick-pull. memtester evidence in /var/log/sol_memtester.log, ramscan in /var/log/ramscan.log.
- LESSON: Intermittent non-ECC RAM fault is HEAT-dependent: static/cool single-pass tests pass clean; the fault only manifests under sustained load once the DIMM warms. Must run sustained multi-pass stress to map it. memtester caught it (long run, hot); a cool ramscan single pass nearly missed it.

## [2026-06-13 18:40] b11 db0f1c86
- DID: FULLY-AUTOMATIC RAM mapper LIVE on Sol: service sol-ramscan-loop.service (enabled+active). Script /usr/local/sbin/sol_ramscan_loop.sh (src C:/claude_base/tools/sol_resilience/sol_ramscan_loop.sh). Binary /home/maxre/ramscan (src ramscan.c same folder). memtest=17 REMOVED from GRUB (fast reboots restored). DIMMs: 4x16GB DDR4-2667 non-ECC, slots ChannelA/B-DIMM0/1, blank part#s (generic), serials 6C/5E/63/5D.
- STATE: Loop scans 50G x12 hot -> box crashes mid-scan -> panic auto-reboots (~1min) -> loop auto-resumes, harvests BADPAGE physical addrs from prior run logs into deduped master /var/log/sol_ramscan/badpages.txt. Self-disables after 8 runs OR 3 no-growth runs. RESULTS.txt = progress. ~4min/cycle, ~30-40min total to map.
- NEXT: WHEN MAPPING DONE (check: systemctl is-enabled sol-ramscan-loop = disabled, or RESULTS.txt says MAPPING COMPLETE): read /var/log/sol_ramscan/badpages.txt + the per-GB histogram in run logs. If bad pages cluster in one stick-sized contiguous phys range -> memmap=SIZE$ADDR reserve whole range (Max's disable-the-stick idea, leaves 48G). If scattered by channel-interleave -> memmap= each bad page. Apply to /etc/default/grub, update-grub, reboot, verify free shows reduced RAM + stable. I (not Max) apply the block - Max wants fully remote, hates stick-pull. Then optional: order 16GB DDR4-2667 stick as real cure.
- LESSON: Make crash-test harnesses persist their binary OUTSIDE /tmp (/tmp is wiped on reboot) - first ramscan run vanished after a crash-reboot because it was in /tmp. Put on /home or /usr/local.

## [2026-06-13 19:22] b11 db0f1c86
- DID: Mapper running ~30min. Sol UNREACHABLE on 2 consecutive checks ~20min apart - longer than a normal 1-2min crash-reboot. Possibly unlucky timing on fast crash-loop, OR Sol FROZEN (not auto-rebooting). HW watchdog (iTCO_wdt 30s) + panic=10 should self-recover; if those aren't persistent across reboots, a later crash could hang the box.
- STATE: Shortened wake to ~300s to disambiguate stuck-vs-rebooting. badpages.txt count + RESULTS.txt unread (box down). Loop service: sol-ramscan-loop (enabled, autostarts). Did NOT alarm Max (on break) yet - could be normal.
- NEXT: NEXT CHECK: if Sol answers SSH -> read /var/log/sol_ramscan/badpages.txt + RESULTS.txt, that is the map; if mapping COMPLETE (loop disabled) apply memmap= block. If Sol STILL DOWN after 300s -> likely FROZEN, needs Max physical power-cycle (M720s has no IPMI). At that point: tell Max, and consider that the auto-crash-loop may be too aggressive - alternative is stop forcing crashes, just reserve the bad pages already found.

## [2026-06-13 19:28] b11 db0f1c86
- DID: SOL FROZEN (3 checks down ~25min) - auto crash-loop too aggressive, watchdog/panic did NOT self-recover this time. Needs Max to PRESS SOL POWER BUTTON (M720s no IPMI, no remote power). Launched background watcher (bash task) that polls SSH every 5s and the instant Sol returns runs 'systemctl disable --now sol-ramscan-loop' to stop it re-crashing (races the loop's 25s boot-settle window, wins).
- STATE: Background watcher running (catches Sol on power-on, disables crash-loop, dumps badpages count + RESULTS). Map collected so far is preserved in /var/log/sol_ramscan/badpages.txt (survives reboot). Did not send Telegram alarm (Sol non-production, Max on break + knows we're working on it).
- NEXT: NEXT: when Max powers Sol on, watcher auto-disables the loop. THEN do NOT resume forced crashing (it freezes Sol). Instead: read /var/log/sol_ramscan/badpages.txt (the bad physical pages already mapped) + per-GB histogram in run logs, and apply a GENTLE permanent block = memmap= those pages in /etc/default/grub + update-grub + reboot, verify. If too few pages mapped to be confident, run ramscan ONCE manually (not the loop) and watch it, rather than an unattended crash-loop. Tell Max: software-block is viable; mapping showed scale.
- LESSON: Unattended auto-crash-LOOP on a flaky box is dangerous: a freeze the HW watchdog can't catch leaves the box stuck needing a physical power-cycle. For crash-prone diagnosis, prefer ONE attended scan per cycle over a self-rebooting loop, OR confirm panic=10 + watchdog are PERSISTENT (sysctl.d + systemd RuntimeWatchdogSec) before looping.

## [2026-06-13 21:20] b11 db0f1c86
- DID: Sol force-started by Max; re-armed aggressive 2s SSH poll (bg b2iup64hl) to disable sol-ramscan-loop crash-loop within the 25s boot-settle window
- STATE: Sol still booting/unreachable (port 22 timeout). Crash-loop service STILL ENABLED until watcher catches it. badpages map at /var/log/sol_ramscan/badpages.txt not yet read
- NEXT: On catch: disable loop, read badpages.txt + per-GB histogram, apply gentle memmap= block in /etc/default/grub (NO more crash-looping), reboot+verify

## [2026-06-14 07:58] b11 db0f1c86
- DID: Caught Sol on boot, disabled sol-ramscan-loop crash-loop (EXIT=0). Read all run logs: runs found 113/22/220 bad pages but DIFFERENT scattered addresses each run, all single-bit flips -> marginal whole stick, NOT fixed dead cells. badpages.txt master=0 (harvest bookkeeping bug, moot).
- STATE: Sol UP+STABLE 9h+ at idle, crash-loop disabled+inactive. VERDICT: software memmap-block is futile (non-repeating scattered bit-flips + 4-way interleave). Fix needs ONE physical/BIOS visit.
- NEXT: WAITING on Max to pick: (1) BIOS underclock RAM 2667->2133 [my rec], (2) swap-test+pull bad stick, (3) leave Sol idle-only. Do NOT crash-test or memmap further.
- LESSON: Heat-triggered non-ECC failures show as scattered non-repeating single-bit flips, not a fixed bad-page set -> address-mapping + memmap blocking cannot fix them; only hardware (pull/underclock) does.

## [2026-06-14 12:53] b11 db0f1c86
- DID: Discussed fix options w/ Max. Confirmed software memmap-block is futile (scattered non-repeating bit-flips). Priced replace-all: 64GB 4x16 DDR4-2666 non-ECC UDIMM kit ~$110 (Crucial/A-Tech), fits M720s.
- STATE: Sol stable at idle, crash-loop disabled. Max weighing 3 fixes: BIOS underclock (1 quick trip), swap-test+pull (tedious), or replace-all 4 sticks (~$110, 1 trip, permanent, no swap-test). Leaning replace-all.
- NEXT: Await Max pick. If replace-all: tee up a buy link (do NOT purchase). If underclock: BIOS steps given (F1 at Lenovo logo, Memory freq 2667->2133, F10).

## [2026-06-14 13:14] b11 db0f1c86
- DID: Answered Max's logic Qs on identifying 1-of-4 bad sticks: 2 tests by binary pairing (trust passes), 3 by elimination (crashes only), 4 worst-case for positive ID (catch each solo crashing). Max remote on phone tethering, deciding.
- STATE: Sol stable idle, crash-loop off. No remote fix possible (all need physical access at home). Only remote-doable action = order RAM kit now.
- NEXT: Await Max pick: replace-all ~$110 (my rec, order remotely now), BIOS underclock, or swap-test. Offered to tee up buy link (no purchase).

## [2026-06-14 13:35] b11 db0f1c86
- DID: Worked through bad-stick identification combinatorics w/ Max (positive ID of 1-of-4 sticks = 3 tests: 2vs2 to find bad pair, then test stick A solo, then B solo; each ends in a red-handed solo crash). I fumbled it badly across several turns (gave 2, then 4) before adopting Max's correct 3 - flaw noted. Priced RAM: 1 stick ~$35 (needs the 3-boot ID + swap), all-4 kit ~$110 (zero testing, clean swap, matched set).
- STATE: Sol UP+STABLE ~14h at idle, crash-loop disabled. Software fix impossible (scattered non-repeating bit-flips). Max LEANING toward suffering the hands-on route; said 'i will have to suffer'. No purchase made yet.
- NEXT: Max to decide 1-stick vs all-4 and order remotely. If he picks: tee up buy link (DO NOT purchase). Physical swap+test happens later when he's home. Crash-loop must STAY disabled.

## [2026-06-14 13:39] b11 db0f1c86
- DID: Max recalls possibly having 2 spare RAM sticks in a drawer at home (leftovers from a past 2-old->4-new swap). Plan settled: when home, CHECK DRAWER FIRST for good 16GB DDR4-2666 spares = free fix (ID bad stick via 3-test, swap in spare). Only buy if spares are too small (8GB) or flaky.
- STATE: Sol UNREACHABLE right now - this machine is OFF the home LAN (Max tethering remotely); Sol is LAN-only at 192.168.1.113, likely fine just not reachable. Crash-loop stays disabled. No purchase made. dmidecode full read pending home-LAN access.
- NEXT: When home/on-LAN: re-run dmidecode for exact mfr+rank, check drawer sticks. Offered to set up Tailscale on Sol for anywhere-access (Max hasn't answered). Hold all ordering.

## [2026-06-15 10:43] b11 db0f1c86
- DID: Math interlude done (group testing: 3 rounds fully classifies 4 sticks via pos+neg ID; crash test = pattern write/verify RAM soak = March-type memory test). Max going HOME to physically pull/swap a stick, will return and say 'run the test'.
- STATE: Sol off-LAN now (Max remote) but he's heading home = will be on-LAN + reachable at 192.168.1.113. Crash-loop STAYS disabled. ramscan binary at /home/maxre/ramscan; stress-ng also available.
- NEXT: ON MAX'S 'run the test': run ONE attended memory stress pass (e.g. ramscan or 'stress-ng --vm 6 --vm-bytes 7G --verify --timeout 300s') on the CURRENT stick config, watch for crash/bit-flip. Do NOT re-enable sol-ramscan-loop. If it crashes, Max is physically present to power-cycle.

## [2026-06-15 13:51] b11 db0f1c86
- DID: GROUP TEST on pair {1,2} (sticks 3,4 physically pulled by Max, 32GB=2 sticks confirmed): ran ramscan 24GB x20 passes ~9min, ALL CLEAN bad_words=0, NO crash, Sol stayed up. => pair {1,2} is GOOD. Bad stick is in {3,4} (the pulled pair).
- STATE: Sol UP+stable on sticks 1,2. ramscan at /home/maxre/ramscan. Loop disabled. Log /home/maxre/pairtest12.log. Max physically present, swapping sticks on my word.
- NEXT: NEXT: Max inserts stick 3 alongside 1,2 -> I run ramscan on {1,2,3}; CRASH=stick3 bad (positive), CLEAN=stick4 bad. Then confirm by testing the other. Tell Max: pair 1,2 clean, put stick 3 in.

## [2026-06-15 13:54] b11 db0f1c86
- DID: CORRECTION from Max: he wants POSITIVE ID of EVERY stick (each solo), not elimination. So test each remaining stick ALONE. Pair {1,2} already proven good together (their pass = positive good for both).
- STATE: Max physically inserting ONLY stick 3 (solo) now, said 'wait'. Sol on whatever config mid-swap. ramscan /home/maxre/ramscan, loop disabled.
- NEXT: ON MAX GO: run ramscan solo on stick 3 (~14GB x20). CRASH=3 bad(positive), CLEAN=3 good(positive). Then he'll do stick 4 solo likewise. Each result is positive.

## [2026-06-15 14:32] b11 db0f1c86
- DID: STICK 3 SOLO test (16GB confirmed=1 stick): ramscan 12GB x20 ~5min, ALL CLEAN bad_words=0, no crash. => STICK 3 GOOD (positive). Running tally: sticks 1,2 GOOD (pair test), 3 GOOD (solo). So STICK 4 is the culprit by elimination - but Max wants POSITIVE id, so must test 4 solo to catch it crashing.
- STATE: Sol up on stick 3 alone. ramscan /home/maxre/ramscan, loop disabled. Logs in /home/maxre/test_stick3.log, pairtest12.log.
- NEXT: NEXT: Max swaps stick 3 OUT, stick 4 IN (solo); I run ramscan 12 20 solo on stick4 -> expect CRASH = positively bad. That finishes full positive ID of all 4. Then fix: run Sol on the 3 good sticks (48GB) or replace stick 4.

## [2026-06-15 14:53] b11 db0f1c86
- DID: PLAN: Max walking to Sol to swap stick 3 OUT -> stick 4 IN (solo). Armed self-contained bg watcher (3 phases): wait for Sol to drop (=swap), wait for it to return, then AUTO-run ramscan 12x20 on stick4 + monitor. Expect CRASH=stick4 positively BAD.
- STATE: Sticks 1,2,3 all proven GOOD. Stick 4 = prime suspect, confirming positively now. Sol on stick3->being swapped. ramscan /home/maxre/ramscan, loop DISABLED (keep it so). test logs /home/maxre/test_stick4.log.
- NEXT: After stick4 confirmed bad: FIX = run Sol on the 3 good sticks 1+2+3 (48GB, plenty) OR replace stick4. Then re-enable normal use. Report verdict to Max. If compacted, resume.py + this worklog have full state.

## [2026-06-15 15:30] b11 db0f1c86
- DID: All 4 sticks tested CLEAN individually (pair1+2 clean, stick3 clean, stick4 clean) yet box freezes at full 64GB. Single-bad-stick hypothesis DISPROVEN.
- STATE: Sol stable at idle, crash-loop disabled. Max going to brainstorm with other sessions; I am writing the report.
- NEXT: Write report + reference it. Next diagnostic: reinstall all 4, confirm 64GB crash; then try 3 sticks=48GB as possible stable config.

## [2026-06-15 15:59] b11 db0f1c86
- DID: 64GB full soak reproduces FAULT: bad_words 310->2012 climbing, pass 25/30, no freeze yet. All 4 sticks were clean solo/pair=0 errors. Fault is FULL-LOAD dependent, not one dead stick. Posted to board as b11. Report written+pushed.
- STATE: Sol up 21min running soak pid4132 (/home/maxre/full64.log). Buggy first watcher (beq8le666) gives FALSE ssh-fails - ignore. Crash-loop service DISABLED. Autonomous 4min timer armed.
- NEXT: Let 64GB finish (~5 passes), then test 48GB/3-sticks as candidate stable config. ssh -i ~/.ssh/sol_key maxre@192.168.1.113; launch: setsid stdbuf -oL -eL /home/maxre/ramscan <GB> <passes> >log 2>&1 </dev/null &

## [2026-06-15 16:28] b11 db0f1c86
- DID: 64GB RE-TEST after Max BIOS visit: FAULT persists AND now froze Sol hard at pass 16 (bad_words 2->769 from pass0, then unreachable 16:27). BIOS change (if any) did NOT help.
- STATE: Sol HUNG/frozen, needs power-cycle. Config still 64GB/4 sticks. Verdict: 64GB unusable. 32GB(2 sticks) proven clean. Crash-loop service still DISABLED.
- NEXT: Max to power-cycle. Then either run 2 sticks/32GB (done, safe) or I soak-test 48GB/3 sticks. Confirm if Max actually changed a RAM-speed BIOS setting.

## [2026-06-15 17:02] b11 db0f1c86
- DID: 48GB/3-stick(1,2,4) 6-run series: errors scale with population. R1=0 R2=8 R3=391 R4=108 R5=20 bad_words, NO freeze. 32GB(2 sticks)=0 clean, 64GB=heavy+freeze. Root cause = DIMM population/mem-controller load, NOT one bad stick (stick4 clean alone but 1+2+4 errors).
- STATE: Series run6 finishing. Sol up at 48GB. Verdict: only 32GB/2-stick is error-free. Crash-loop DISABLED.
- NEXT: Recommend Max pull one more stick -> run 2 sticks/32GB permanently. Then final verdict + re-enable normal Sol use.

## [2026-06-15 17:06] b11 db0f1c86
- DID: 48GB series FINAL: runs bad_words=0,8,391,108,20,0 -> 4/6 corrupt, no freeze. Locked table: 32GB clean / 48GB intermittent / 64GB freeze. Posted verdict to board.
- STATE: Sol idle at 48GB. VERDICT delivered: use 2 sticks/32GB. Crash-loop DISABLED.
- NEXT: Await Max pulling 1 more stick; optionally run 6x series at 32GB to triple-confirm, then re-enable normal Sol use + close out.

## [2026-06-15 17:27] b11 db0f1c86
- DID: Max pulled another stick -> Sol now at 32GB/2 sticks (the proven-clean safe config). Rebooted 8min ago, some CPU load present (may be in use).
- STATE: Sol at 32GB SCAN-IDLE. Diagnosis CLOSED: 2 sticks=clean, 3=intermittent corrupt, 4=freeze. Crash-loop DISABLED. Team already moving work off Sol per my broadcast.
- NEXT: Optional: run 6x confirm series at 32GB (~24GB soak) IF Max says go and Sol is idle. Else done - re-enable normal low-stakes Sol use.

## [2026-06-15 19:21] b11 db0f1c86
- DID: Sol RAM diagnosis CLOSED + delivered. Final table: 2 sticks/32GB=clean(0 errors), 3/48GB=intermittent corruption(4 of 6 runs, no freeze), 4/64GB=heavy errors+hard freeze. Root cause=mem-controller/DIMM-population load at DDR4-2667, NOT one dead stick (each stick clean solo).
- STATE: Sol running at 32GB/2 sticks (safe config), teammate b15 using it. Crash-loop service DISABLED (must stay). Report+verdict pushed; board informed; team moved work off Sol.
- NEXT: Nothing pending. OPTIONAL only if Max says go: 6x confirm soak (~24GB) at 32GB. Otherwise fully done.

## [2026-06-15 19:57] b11 db0f1c86
- DID: Sol RAM at 32GB/2-stick: launched LONG 80-pass soak (ramscan 24 80, pid in /home/maxre/long32.log) to get a real error RATE (Max: 10x scale). Short 6-run series earlier: runs1-2 clean, run3 had bad_words=1. CONFIRMED TABLE: 32GB~near-zero(1 rare flip), 48GB intermittent(0/8/391/108/20/0), 64GB heavy+freeze. Root cause=mem-controller/DIMM-population signal-integrity at DDR4-2667, NOT one dead stick. Web-confirmed: good RAM=0 errors, intermittent=real fault not cosmic-ray.
- STATE: Sol idle except the 80-pass soak running now. Crash-loop service DISABLED (keep). I am b11 on bcast. Autonomous 4min loop.
- NEXT: 1) Watch long32.log to completion, report error count/rate. 2) THEN run 40%-load test = ramscan 13 80 (Max idea: lighter load may be fully clean/safer). Launch: setsid stdbuf -oL -eL /home/maxre/ramscan 13 80 > /home/maxre/load40.log 2>&1 </dev/null &. 3) Final verdict: pick safe 32GB usage level. ssh -i ~/.ssh/sol_key maxre@192.168.1.113

## [2026-06-15 19:58] b11 db0f1c86
- DID: LAUNCHED alternating-load CAMPAIGN on Sol 32GB (Max: alternate 40%-100% load, crunch until good stats). Script /home/maxre/campaign.sh loops rounds: ramscan 13 8 (40%) then ramscan 29 8 (~100%), logs 'RESULT ROUND n LOAD xGB bad_words=N' to /home/maxre/campaign32.log. ~6min/round.
- STATE: Campaign RUNNING (controlled by flag file /home/maxre/campaign.run). TO STOP: ssh ... 'rm /home/maxre/campaign.run' (finishes current run then exits clean). Sol 32GB/2-stick. Crash-loop DISABLED.
- NEXT: Periodically read campaign32.log, tally bad_words per load level (13 vs 29), report stats to Max. Goal: error rate at 40% vs 100% load -> is 40% fully clean/safer? grep RESULT /home/maxre/campaign32.log

## [2026-06-16 12:11] b11 db0f1c86
- DID: Running 8h unattended campaign on Sol (32GB/2 sticks): alternating ramscan 13GB(40%) vs 24GB(75%), 8 passes each, ~4.5min/cycle, ~100 cycles expected. Reboot-survivable: cron */2 campaign_guard.sh relaunches if dead, @reboot relaunch, @reboot logs BOOT line to campaign_boots.log for crash count. Earlier finding: 32GB froze once during a 29GB(100%) run, watchdog-rebooted.
- STATE: Campaign live since ~12:04. Log=/home/maxre/campaign32.log (RESULT ROUND n LOAD xGB bad_words=N). Crash log=/home/maxre/campaign_boots.log (WINDOW-START 12:11:38, boot 06-15 20:09; any later BOOT line=a crash). Flag=/home/maxre/campaign.run. Window ends ~20:11. b11 on bcast.
- NEXT: Each wake (~270s): grep RESULT to tally bad_words per load (13GB vs 24GB), count BOOT lines after WINDOW-START as crashes, update running table for Max. Stop after 8h via rm /home/maxre/campaign.run (also removes cron guard lines).

## [2026-06-16 12:22] b11 db0f1c86
- DID: AUTONOMOUS TICK 12:21: NEW FINDING - Sol crashed 3x in ~9min. Attribution by timeline: crash1 12:13:50 + crash2 12:16:36 both during 75%/24GB runs; crash3 12:20:43 during a 40%/13GB run. Temps fine (pkg 66C, not thermal). 40% bad_words climbing 0,2,1,6. So current 2-stick pair is unstable EVEN at 40%.
- STATE: Currently installed pair is likely sticks 1+4 (Max pulled 2 then 3); earlier CLEAN 32GB test was sticks 1+2 - so current pair never validated, may contain a marginal stick. Campaign now 40%-ONLY, reboot-survivable, running. Crash log /home/maxre/campaign_boots.log (3 BOOT lines after WINDOW-START 12:11:38).
- NEXT: Tell Max (away, autonomous): 40% also crashes -> his earlier hope that light-load 32GB is safe is wrong for THIS pair. Suggest when he returns: try the OTHER pair (1+2) or single-stick to find which stick is marginal; and the 2x32GB-kit fix still stands. Keep counting crashes/flips.

## [2026-06-16 12:58] b11 db0f1c86
- DID: Heartbeat 12:58: 40%-only campaign on pair 1+4 = 14 runs, 11 CRASHES in ~50min, near-every run flips bits. Verdict locked: this 2-stick pair (1+4) is severely unstable even at 40%, not thermal (66C).
- STATE: Campaign self-running+reboot-survivable on Sol. Logs: /home/maxre/campaign32.log (RESULT lines), /home/maxre/campaign_boots.log (BOOT=crash count). On wide ~25min heartbeat to save context. b11.
- NEXT: When Max back: recommend swap to other pair (sticks 2+3) to test, or single-stick isolation again, or buy 2x32GB kit (1 DIMM/channel) for stable 64GB. Stop run via rm /home/maxre/campaign.run.

## [2026-06-16 14:27] e1sol db0f1c86
- DID: Now bcast id e1sol (E team, was b11). Sol RAM diagnosis: pair 1+4 (current 2 sticks) UNSTABLE even at 40% load - 14 runs/11 crashes in ~50min, flips nearly every run, NOT thermal (66C). 64GB(4 sticks)=fast freeze; 75%/24GB=crashes; 40%/13GB=also crashes on this pair. Campaign STOPPED+cron guard removed. Sol idle-stable (no crash when not loaded).
- STATE: WAITING on Max to physically swap to the OTHER 2 sticks (he'll pull current 1+4, install 2+3, boot). Sol still at 32GB old pair, ~1.5h uptime, no swap yet. ramscan at /home/maxre/ramscan <GB> <passes>. Campaign script /home/maxre/campaign.sh + guard exist (flag /home/maxre/campaign.run removed=stopped). SSH: ssh -i ~/.ssh/sol_key maxre@192.168.1.113.
- NEXT: When Max says 'back up': verify swap via free -g (RAM_GB) + uptime low, then run load test on new pair (ramscan 13 8 repeated, watch bad_words + crashes). If new pair clean->bad stick was in 1+4; if also crashes->slot/controller fault. Fix options: 2x32GB kit (1 DIMM/channel) for stable 64GB, or BIOS underclock.

## [2026-06-16 14:59] e1sol db0f1c86
- DID: PAIR 2+3 TEST RUNNING (Max swapped out suspects 1+4, cover left open=better cooling). Campaign alternates ramscan 13GB(40%) + 24GB(75%), 8 passes, non-stop, reboot-survivable (cron */2 guard + @reboot relaunch + BOOT logger). EARLY RESULT: pair 2+3 = ZERO crashes in 21min vs pair 1+4 = 11 crashes/50min -> strong positive. Reset campaign32.log + campaign_boots.log CLEAN at ~14:44 for unambiguous pair-2+3 data (old log was contaminated w/ 1+4 results).
- STATE: Sol up, 32GB pair 2+3, campaign RUNNING (pid ~5369). Logs CLEAN as of reset: /home/maxre/campaign32.log (RESULT ROUND n LOAD xGB bad_words=N), /home/maxre/campaign_boots.log (BOOT line=crash). Flag /home/maxre/campaign.run. CANNOT verify physical sticks via software (32GB looks same either pair); proof = behavior (clean where 1+4 crashed). Max declined/hasnt given sudo pw for dmidecode serials yet. bcast id=e1sol (E team).
- NEXT: Each wake: grep RESULT campaign32.log -> tally bad_words per load (13GB vs 24GB) + count BOOT crashes, update running table for Max (he wants table accumulated non-stop). If pair 2+3 stays clean/low hours = it is GOOD, bad sticks were 1+4; then Max may test 1 vs 4 separately. Stop via rm /home/maxre/campaign.run. Fix path if all fail: 2x32GB kit.

## [2026-06-16 15:20] e1sol db0f1c86
- DID: Pair 2+3 RAM campaign running on Sol (alternating 40%/75%); reported verified crash attribution (both crashes in-test, not Max restart)
- STATE: campaign RUNNING, 2 crashes in window, 40%=0 flips 75%=1 flip; script=for gb in 13 24
- NEXT: Max wants: wait for 2 MORE crashes (until campaign_boots.log has 4 BOOT lines), THEN sed script to 'for gb in 13' (40% only) and keep looping

## [2026-06-16 15:47] e1sol db0f1c86
- DID: Sol pair 2+3 RAM campaign concluded: box deemed untrusted for genomics (non-ECC, freezes under heavy RAM). Stopped campaign (rm campaign.run + stripped campaign_guard/load_switch crons mid-command); Sol froze during the stop under 75% load
- STATE: Sol UNREACHABLE since ~15:25 (hard freeze, past watchdog window). campaign.run removal likely landed pre-freeze so no auto-relaunch. Verdict: Sol OK only as a LIGHT/non-memory-hungry server
- NEXT: Needs PHYSICAL power-cycle by Max (no remote power). After reboot: confirm STOPPED + no campaign crons remain. Genomics -> run on Lak/ECC cloud, not Sol

## [2026-06-16 17:11] e1sol db0f1c86
- DID: Sol recovered after power-cycle (up 6min). Finished campaign teardown: removed campaign.run flag, stripped all campaign crons (guard/load_switch/boot-logger), killed campaign.sh+ramscan
- STATE: Sol IDLE + STABLE at no load, no relaunch mechanism left. Campaign DONE. Verdict delivered: Sol untrusted for genomics (non-ECC, freezes under heavy RAM); usable only as a LIGHT/non-memory-hungry server
- NEXT: TASK COMPLETE - ending autonomous loop. If genomics needed -> Lak or ECC cloud. If revisiting RAM: 2x32GB 1-DIMM-per-channel kit is the real fix (Max declined buying)

## [2026-06-16 17:57] e1sol db0f1c86
- DID: Max re-swapped sticks to POSITIONS 1+2 (green+blue slots). Rebuilt campaign.sh as a 10-ROUND-capped 40/75 (13GB/24GB) test, reboot-survivable (round counter persists in campaign_round.cnt; guard+@reboot crons re-added; boot logger). Reset logs clean, launched 17:56:43
- STATE: RUNNING pair pos1+2, round1/40% in progress. Window label PAIR=pos1+2-green+blue. Stops + removes campaign.run after round 10
- NEXT: Monitor rounds+crashes; report per cycle; when 10 ROUNDS COMPLETE appears or flag auto-removed, give Max the pos1+2 verdict vs earlier pairs (1+4 bad: 11 crashes; 2+3: 2 crashes)

## [2026-06-16 18:21] e1sol db0f1c86
- DID: pos1+2 (green+blue) 40/75 test: cap raised 10->20 rounds (now file-based /home/maxre/campaign_maxrounds, live-adjustable). Cleaned an orphan-ramscan double-scanner hiccup during the relaunch
- STATE: RUNNING round 4/20. Rounds 1-3 ALL CLEAN (0 flips every load, 0 crashes). pos1+2 looks excellent vs 1+4(11 crashes)/2+3(2 crashes). Sol up >1h. Reboot-survivable; auto-stops+removes campaign.run at round 20
- NEXT: Report every 4 ROUNDS (Max's new cadence). Next report at round 8, then 12/16/20. Watch grep -c BOOT for crashes, grep RESULT for flips. At round 20 give verdict: if all clean -> slot4/its stick is the culprit, pos1+2 = usable stable 32GB

## [2026-06-16 18:42] e1sol db0f1c86
- DID: pos1+2 40/75 test reached round 8/20
- STATE: ALL CLEAN through round 8: 0 flips every load, 0 crashes, Sol up 1h38m. Reboot-survivable, cap=20 (file /home/maxre/campaign_maxrounds), auto-stops at 20. Logs: campaign32.log (RESULT lines), campaign_boots.log (BOOT=crash)
- NEXT: Report every 4 rounds (next: 12, then 16, 20) AND immediately on any crash. Poll: grep -c BOOT campaign_boots.log; cat campaign_round.cnt; grep RESULT | grep -vc 'bad_words=0 '. At round 20 verdict: all-clean => slot4/its stick was culprit, pos1+2 = stable 32GB box

## [2026-06-16 19:04] e1sol db0f1c86
- DID: pos1+2 (green+blue slots) 40/75 RAM test at round 12/20, Sol up 2h
- STATE: ALL CLEAN through round 12: 0 bit-flips on every 40%(13GB) and 75%(24GB) run, 0 crashes. Strongly implicates the position-4 stick/slot as Sol's fault. Earlier: pos1+4=11 crashes(bad), 2+3=2 crashes(marginal), pos1+2=perfect
- NEXT: AUTONOMOUS LOOP active (4min self-wake, sentinel <<autonomous-loop-dynamic>>). Report to Max every 4 ROUNDS (next 16, then 20) + immediately on any crash. POLL CMD: ssh -i ~/.ssh/sol_key maxre@192.168.1.113 then grep -c ^BOOT /home/maxre/campaign_boots.log (crashes); cat /home/maxre/campaign_round.cnt (round); grep RESULT /home/maxre/campaign32.log|grep -vc 'bad_words=0 ' (nonzero flips). Test auto-stops+removes /home/maxre/campaign.run at round 20 (cap in /home/maxre/campaign_maxrounds). Reboot-survivable via campaign_guard.sh cron. AT ROUND 20: give verdict - if all clean, pos1+2 = stable usable 32GB, position-4 is the culprit; Max may then want to test the two suspect sticks individually. Max declined buying 2x32GB kit. Sol untrusted for genomics regardless (non-ECC)

## [2026-06-16 21:08] e1sol db0f1c86
- DID: pos1+2 (green+blue) PASSED full 20-round 40/75 test: 0 flips, 0 crashes, Sol up 2h+. pos1+2 = HEALTHY stable 32GB. History: pos1+4=11crashes(BAD), 2+3=2crashes(marginal), pos1+2=PERFECT
- STATE: Test essentially complete (round 20, auto-stops+removes /home/maxre/campaign.run at round 20). Max now wants NEXT experiment: SLOT-4 test - add one known-good stick into SLOT 4 (keep pos1+2), making 3 sticks/48GB, re-run 40/75. Reading: fails=>slot4 flawed; clean=>slot4 fine, fault was a STICK. Awaiting Max to physically install, then says go
- NEXT: ON GO: re-tune loads for 48GB (40%~19GB, 75%~36GB) - edit /home/maxre/campaign.sh 'for gb in 19 36' (or keep 13 24 as fixed stress), reset campaign_round.cnt=0, set cap in /home/maxre/campaign_maxrounds, clean campaign32.log + campaign_boots.log (WINDOW-START label PAIR=pos1+2+4-slot4test), touch campaign.run, relaunch via setsid, guard cron keeps it reboot-survivable. Report every 4 rounds + on crash. POLL: ssh -i ~/.ssh/sol_key maxre@192.168.1.113; grep -c ^BOOT campaign_boots.log; cat campaign_round.cnt; grep RESULT campaign32.log|grep -vc 'bad_words=0 '. Sol non-ECC => untrusted for genomics regardless. Max declined 2x32GB kit

## [2026-06-17 06:25] e1sol db0f1c86
- DID: Delivered 3-config verdict (pos1+4 BAD=11 crashes / 2+3 marginal / pos1+2 HEALTHY=20 rounds clean). Max chose next test: slots 1+2+3 full, slot 4 BLANK (48GB).
- STATE: Sol idle, waiting on Max to physically install stick in slot 3 + say 'go'. campaign.sh/guard/crons ready to reuse; logs not yet wiped for new window.
- NEXT: On 'go': decide 13/24 vs scaled 19/36 loads, wipe campaign32.log+campaign_boots.log, label window pos123-slot4blank, reset round.cnt=0, cap=20, touch campaign.run, relaunch via setsid. Report every 4 rounds + on crash.

## [2026-06-17 06:37] e1sol db0f1c86
- DID: Confirmed 48GB (49234760 kB, 3 sticks pos1/2/3=sticks2/3/4, slot4 blank). Launched 100pct-load campaign: single 45GB 8-pass scan per round, 20 rounds.
- STATE: RUNNING round 1. Window=pos123-slot4blank-100pct. campaign.sh loads='for gb in 45'; cap=20; crons present; run flag set. Hypothesis: slot4 guilty -> 100pct on 3 good slots stays clean.
- NEXT: Report every 4 rounds + on crash. Poll: grep -c ^BOOT campaign_boots.log (crashes), campaign_round.cnt (round), grep RESULT campaign32.log grep -vc 'bad_words=0' (flips). 45GB chosen as 100pct (3GB OS headroom, avoid OOM-kill).

## [2026-06-17 07:03] e1sol db0f1c86
- DID: Poll #1: rounds 1-2 complete, both bad_words=0; round 3 running. 0 crashes, 0 flips, Sol up 32min. ~5min/round.
- STATE: RUNNING healthy. 100pct 45GB load, 20-round cap, pos123-slot4blank.
- NEXT: Continue 4-round status cadence. Next report ~round 6-7.

## [2026-06-17 07:35] e1sol db0f1c86
- DID: Sol rebooted 07:29 after ~40min freeze. Pulled prev-boot journal: OOM-killer killed ramscan (45GB too big for 48GB box) -> OOM-thrash loop -> hard freeze. pstore EMPTY (no panic, silent hang). My error: 45GB load oversized.
- STATE: Sol BACK, up, DISARMED (campaign.run removed, no scanner, no campaign proc). crashes=1 logged. Slot-4 question INCONCLUSIVE - test contaminated by OOM.
- NEXT: Awaiting Max go to redo 20-round test at SAFE 40GB (heavy, ~8GB headroom, no OOM). Edit campaign.sh 'for gb in 40', reset cnt=0, wipe logs new window pos123-slot4blank-40GB, touch run, relaunch.

## [2026-06-17 07:44] e1sol db0f1c86
- DID: Launched 75pct test: ramscan 36 8 per round, 20 rounds, pos123-slot4blank-75pct. 48GB confirmed, Sol up 14min. Analysis: every load that FIT passed clean (incl 100pct rounds 1-2); only OOM at round3 froze it. Twist: rounds1-2 at 45GB fit, round3 didnt -> concurrent transcription-install likely ate headroom (Max's theory plausible).
- STATE: RUNNING round 1, 36GB=75pct, ~12GB headroom (OOM-immune). Slots1+2+3 NOT condemned - 100pct freeze was OOM-contaminated + concurrent install confound.
- NEXT: Report every 4 rounds + on crash. Later: repeat 100pct in ISOLATION sized to fit (~42GB) for clean max-stress read.

## [2026-06-17 08:06] e1sol db0f1c86
- DID: Killed 75pct test (5 rounds were clean). Relaunched 100pct-v2 ISOLATED: ramscan 42 8/round, 20 rounds, window pos123-slot4blank-100pct-v2. Sized 42GB (avail was 44) to avoid OOM that ruined v1. Sol isolated now (only ~2GB services: invidious/node/gnome).
- STATE: RUNNING round1, 42GB. Tests Max's theory: prior 100pct freeze likely OOM from concurrent transcription-install eating headroom (rounds1-2 at 45GB fit, round3 OOM'd). Clean decider: pass=hardware OK / freeze=real fault.
- NEXT: 2-min status cadence. Report rounds/flips/crashes. On freeze: pull pstore+journal -b -1, disarm run flag. sudo pw in zSyncMain/ssh/sol_sudo_password_20260523.txt.

## [2026-06-17 08:12] e1sol db0f1c86
- DID: Launched background watcher (bg id bnzbkp67p) -> logs to C:/claude_base/worklog/sol_100pct_v2_watch.log every 90s; auto-disarms (rm campaign.run + pkill ramscan) on crash; stops at done=20. Watches 100pct-v2 42GB test.
- STATE: RUNNING. To check: Read the watch log (cheap) instead of SSH. Test = clean decider for slots1+2+3 at full load (isolated, OOM-proof at 42GB).
- NEXT: On compaction: Read sol_100pct_v2_watch.log for live status. If CRASH-DETECTED line -> hardware fault confirmed, pull pstore+journal -b -1 (sudo pw zSyncMain/ssh/sol_sudo_password_20260523.txt). If DONE-20 -> slots1+2+3 GOOD at full load, prior v1 freeze was OOM/contention.

## [2026-06-17 08:22] e1sol db0f1c86
- DID: KEY RESULT: 100pct-v2 42GB isolated -> ROUND1 bad_words=0, ROUND2 bad_words=52. Real memory bit-flips, NO crash, NO OOM. Clean hardware signal.
- STATE: Slots1+2+3 are FAULTY at high load (not slot-4-specific). Load-threshold fault: light=clean, ~42GB=errors. Matches original 64GB pattern. Sol RAM untrustworthy for memory-heavy work, confirmed by measured corruption (not just freezes).
- NEXT: Watcher bnzbkp67p still running, accumulating later rounds. Verdict stands: Sol = light/non-memory server only. Could later try per-stick solo at 14-15GB heavy+long to find WHICH stick, but core answer (bad RAM, load-dependent) is settled.

## [2026-06-17 08:32] e1sol db0f1c86
- DID: DEFINITIVE 48GB result: 42GB isolated -> R1=0, R2=52, R3=84 flips (escalating), R4=FROZE (watchdog rebooted 2min). Rounds5-20=NA garbage post-reboot spin, ignore. Both corruption AND freeze, OOM ruled out. Sol RAM definitively bad, load-dependent.
- STATE: NEW TEST RUNNING: Max swapped to sticks 2+3 in slots 1+3 (both green) = 32GB. Launched 100pct=27GB (max no-OOM on 32GB), 20 rounds, window sticks23-slots13-green-100pct. Watcher bg b0gtn7lb9 -> C:/claude_base/worklog/sol_green23_watch.log, auto-disarms on crash, stops done=20.
- NEXT: CAVEAT: 32GB cant reach the 42GB flip-threshold, so a CLEAN result here is inconclusive (just <threshold), only a freeze/flips is informative. Read sol_green23_watch.log for status. campaign.sh loads now '27'. sudo pw zSyncMain/ssh/sol_sudo_password_20260523.txt.

## [2026-06-17 08:38] e1sol db0f1c86
- DID: CORRECTION (Max pushback): my 'RAM is bad' was flawed single-factor thinking. There are 4 ENTANGLED fuzzy factors: stick, slot, position/channel, CPU memory-controller (controller is ON-DIE in i7-9700, so processor is a live suspect). All only stress at high load, so cannot be cleanly isolated. Every stick passed SOLO -> no single factor convictable.
- STATE: What survives uncertainty: at high memory load Sol's memory SUBSYSTEM is unreliable (flips+freeze), attribution open/multifactor. Practical verdict (no heavy-memory work on Sol) holds regardless of which factor.
- NEXT: Green-23 test still running (watcher b0gtn7lb9). Disentangling factors would need swapping ONE factor while holding trigger-load constant - hard since trigger needs lots of RAM. Frame all future reasoning as multifactor, not 'bad stick'.

## [2026-06-17 08:39] e1sol db0f1c86
- DID: RIGOROUS FRAMING (Max): only 2 hard facts. (1) 3 sticks @100pct/42GB = BAD (flips 52->84 + freeze). (2) slots1+2 @75pct = GREAT (clean). Everything else IN BETWEEN/unknown. No root cause, no convicted component (stick/slot/position/CPU-controller all entangled, only stress at high load, each stick passed solo).
- STATE: Green-23 probe still running (2 sticks=32GB @100pct=27GB, watcher b0gtn7lb9 -> sol_green23_watch.log). It is just ANOTHER mid-range data point, NOT definitive.
- NEXT: Stop drawing big conclusions. Report green-23 result as a data point only. Practical: dont trust Sol for heavy-memory work.

## [2026-06-17 09:10] e1sol db0f1c86
- DID: Delivered 2 web searches on RAM testing methodology (overload vs bad-RAM; synthetic vs real-workload). green-23 test (sticks2+3 slots1+3 green, 32GB box, 27GB load) running clean: R1-3 bad_words=0 no crash. Offered stressapptest real-workload soak.
- STATE: green-23 at round 4, 0 crashes, all clean so far. Watcher b0gtn7lb9 logs to sol_green23_watch.log. Timer was lost in compaction, re-arming now.
- NEXT: Keep pulling per-round sums + report. Await Max yes/no on stressapptest. memtest86+ at console still the clean-confound move.

## [2026-06-17 09:42] e1sol db0f1c86
- DID: green-23 (sticks2+3, slots1+3 both green, 32GB@27GB) FINISHED: 20/20 rounds, ALL bad_words=0, 0 crashes. Clean sweep. Caveat: 27GB below 42GB flip threshold so it proves slots1+3 pair good, not that sticks are cleared at high load.
- STATE: green-23 done clean. Next planned swap (Max's idea): keep sticks 2+3, move to slots 2+4, run 100% 20 rounds -> kills bad-slot theory if also clean. Requires Max physical move.
- NEXT: When Max moves sticks to slots 2+4: launch one-liner (sed for gb in 27; reset counters; touch run; setsid). Then re-arm watcher + ~4.5min timer.

## [2026-06-17 11:44] e1sol db0f1c86
- DID: Max moving sticks 2+3 to slots 2+4. Built auto-launch watcher sol_swap24_watch.sh (background): waits for Sol DOWN(swap)->UP, then auto-launches same 27GB x20 test fresh (resets counters+logs, writes WINDOW-START so swap-reboot BOOT line is cleared), then monitors+auto-disarms on crash.
- STATE: Watcher running in background, logs to C:/claude_base/worklog/sol_swap24_watch.log. Test = sticks2+3 in slots2+4 (other green pair), 100%/27GB, 20 rounds. Goal: if clean, all 4 slots proven good -> bad-slot theory dead.
- NEXT: Watch sol_swap24_watch.log: report when launch fires + per-round sums + any crash. If crash, it's a real data point (slots2+4 bad). Pending bigger swap: stick4 into known-good pair to test bad-stick4.

## [2026-06-17 12:04] e1sol db0f1c86
- DID: SLOTS 2+4 TEST RESULT (sticks2+3, 27GB, 32GB box): R1=0 R2=0 R3=4 R4=2 bad_words, then FROZE round5, watchdog rebooted ~2min. NOT CLEAN. Same sticks+load+box as green-23(slots1+3) which was 20/20 CLEAN -> only slots changed. LOAD CONFOUND REMOVED: identical 27GB, slots1+3 clean vs slots2+4 fail. Bad-slot/channel is REAL.
- STATE: Sol back up, flag=NORUN (no relaunch). Scoreboard: BAD=slots123(3stick,had slot2), slots24(had slot2). GOOD=slots13(no slot2), slots12@75%(had slot2 but lower load 24GB). Slot 2 is common factor in both 27GB+ failures = prime suspect, but 75% slot2-clean keeps load in mix.
- NEXT: NEXT isolating test: slots 1+4 (slot4, NO slot2) sticks2+3 @27GB x20. Clean->slot2 confirmed bad. Bad->slot4 implicated. Requires Max physical swap.

## [2026-06-17 12:44] e1sol db0f1c86
- DID: Max put STICK 3 alone in SLOT 4 (16GB box). Launched 100%=12GB(max-safe solo) 20 rounds, report every round. Watcher bg b385jatmt -> sol_slot4solo_watch.log. Compiled FULL experiment table via Explore agent (Max angry prev report missed params); corrected agent undercount: sticks-1+4 pair = 11 crashes/14 runs (DISASTER), not 3.
- STATE: slot4-solo test running. CAVEAT logged: 12GB low load won't fully clear slot4. Phase B clean story: sticks2+3 slots1+3=CLEAN 20/20, slots2+4=froze R5 (R3=4 R4=2 flips). Slot2or4/channel implicated.
- NEXT: Report every round of slot4-solo. After: to truly test slot4 at load, suggest 2 sticks slots3+4 @27GB. memtest86+ at console = confound-free endgame.

## [2026-06-17 13:01] e1sol db0f1c86
- DID: Slot4-solo (stick3) cleared R1-2 bad_words=0; Max SKIPPED rest, swapping to SLOTS 3+4 (stick2 in slot3 + stick3 in slot4 = 32GB). Sol DOWN mid-swap. Stopped old solo watcher b385jatmt (would misfire on reboot BOOT line). Built+launched sol_swap34_watch.sh (bg) = waits Sol up, kills guard-relaunched old test, reconfigures to 27GB, launches fresh 100% 20-round, monitors+auto-disarm on crash.
- STATE: Watcher running, logs C:/claude_base/worklog/sol_swap34_watch.log. Test=slots3+4 sticks2+3 27GB 20rounds. KEY: slot3 known-good, tests SLOT 4 at real 27GB load excluding suspect slot2. If clean->slot4 good+slot2 is culprit. If froze/flips->slot4 also bad.
- NEXT: Report every round once launched. memtest86+ at console still the confound-free endgame. Phase B so far: slots1+3 CLEAN, slots2+4 BAD(froze R5).

## [2026-06-17 13:05] e1sol db0f1c86
- DID: SLOTS 3+4 (stick2-slot3 + stick3-slot4, 32GB) RELAUNCHED CLEAN at ~13:06 via /home/maxre/relaunch34.sh = 27GB 100% 20 rounds. NOTE: auto-watcher sol_swap34_watch FALSE-tripped (read swap-reboot BOOT line as crash + guard briefly resumed old 12GB test); NOT a real crash. Reset logs fresh, config confirmed 'for gb in 27'. RAM=32GB confirmed (sticks in).
- STATE: Fresh slots3+4 test running from round 1, logs reset clean. campaign32.log=RESULT log, campaign_boots.log fresh (0 BOOT). Launching new monitor watcher sol_mon34_watch.log. Full history table saved+pushed: tools/sol_resilience/sol_ram_experiment_history_20260617_v01_tomemex.md.
- NEXT: Report every round. KEY TEST: slot4 at real 27GB load excluding suspect slot2. Clean->slot2 culprit; froze/flips->slot4 bad too. After: memtest86+ at console = endgame.

## [2026-06-17 13:27] e1sol db0f1c86
- DID: slots3+4 (sticks2+3, 27GB) flips climbing R3=1 R4=2 R5=12, slot4(black) bad. Updated history doc B5 + channel/color theory: GREEN slots(1+3) clean, BLACK slots(2+4) bad - unifies all data, 123-bad explained by black slot 2.
- STATE: 3+4 test still RUNNING (5 rounds, crashes=0). green-23(slots1+3)=CLEAN20/20. slots2+4=froze R5. Conclusion: Sol=2-stick green-slot machine 32GB.
- NEXT: Write thorough handover for fresh session. Decide stop-or-continue 3+4. Optional memtest86+ at console.
- LESSON: On this 4-DIMM board GREEN slots(1+3)=clean, BLACK slots(2+4)=faulty; every bad config includes a black slot.

## [2026-06-17 13:55] E1testrunner db0f1c86
- DID: Relaunched clean: sticks2+4 in GREEN slots1+3, 27GB x20 (testing stick4 in good slot). R1-3 all bad_words=0, crashes=0. PRIOR: slots3+4 (stick4 in black) FROZE round6 after flips R3=1 R4=2 R5=12 = black slot4 bad.
- STATE: sticks2+4 green-slots test RUNNING round4, monitor bdntikrms, log sol_mon_s24g13_watch.log. Clean so far supports stick4 GOOD, black slots fault.
- NEXT: Report rounds to Max; if 20/20 clean = stick4 cleared, fault is black slots 2+4. memtest86+ at console = final convictor.
- LESSON: Stick4 clean in green slot while same stick4 dirty+freeze in black slot4 = slot/channel fault not stick fault.

## [2026-06-17 14:17] E1testrunner db0f1c86
- DID: Switched self-wake from broken ScheduleWakeup (needs /loop mode, dead 4x in plain chat) to wakeup.py (wake_listener hook, fires via exit-code-2, works in any chat). Armed test wake 938ff535 for 14:19:30. 3-stick test (sticks234/slots123, 42GB) R1 clean bad_words=0, round2 running, monitor b1u031t7n.
- STATE: 3-stick 42GB test RUNNING. Real self-wake armed via wakeup.py 14:19:30. Prior: stick4 cleared in green slot (RUN B clean), black slots 2+4 = fault.
- NEXT: Verify wakeup.py self-wake actually fires at 14:19; report 3-stick rounds.
- LESSON: ScheduleWakeup only fires in /loop mode; for self-wake in a normal chat use wakeup.py (wake_listener hook).

## [2026-06-17 14:38] E1testrunner db0f1c86
- DID: 3-stick test (sticks234/slots123, 48GB) at 42GB/100%: rounds 1-6 ALL CLEAN bad_words=0, crashes=0, round 7 running. SURPRISE: B1 (same slots) froze round4 with big flips; this fresh-seated run clean past round6. self-wake via wakeup.py WORKING (fires + auto-reports, re-arm each wake).
- STATE: 3-stick 42GB RUNNING 6/20 clean. Monitor b1u031t7n. Reseating may have fixed contact, OR earlier freeze was stochastic. Watching to 20.
- NEXT: Run to 20; if clean, revise 3-sticks-always-fail read - reseating/contact may be the real variable.
- LESSON: A freeze on a config can be reseating/contact-dependent: same slots1+2+3 froze before, clean after reseat - dont over-conclude from one run.

## [2026-06-17 15:02] E1testrunner db0f1c86
- DID: 3-stick test (sticks2,3,4 / slots1,2,3, SAME as B1) at 42GB: 10/20 CLEAN, crashes=0, round 11. B1 same sticks+slots froze round4; only diff is reseat. self-wake wakeup.py auto-reporting reliably every ~6min.
- STATE: Halfway clean. Reseat-fixed-it hypothesis strong. Monitor b1u031t7n.
- NEXT: Run to 20/20; if clean recommend memtest86+ at console to confirm before trusting 48GB.
- LESSON: Same sticks+slots froze before reseat, clean after = intermittent DIMM seating/contact is a prime cause of Sol freezes.

## [2026-06-17 15:25] E1testrunner db0f1c86
- DID: Relaunched all-4 (64GB) test cleanly after auto-launcher botched it (left old 42GB config, stopped). Now 50GB/30rnd, round1, crashes=0, 62GB visible=4 sticks confirmed.
- STATE: All-4 test running clean. Fresh monitor sol_mon_all4_watch.sh (bg) + wakeup re-armed. 4-crash tolerance then auto-disarm.
- NEXT: Poll rounds/crashes each wake; report to Max. Update experiment-history doc with 3stick-clean-after-reseat + all-4 result when done.

## [2026-06-17 15:48] E1testrunner db0f1c86
- DID: All-4 (64GB) test at 50GB: rounds 1-3 all clean bad_words=0, crashes=0, on round 4/30.
- STATE: Running clean at the exact load (50GB) that froze pre-reseat all-4. Monitor + wakeup active.
- NEXT: Keep polling to 30 rounds; if clean, reseat=confirmed fix, recommend memtest86+ at console before trusting 64GB.

## [2026-06-17 17:33] E1testrunner db0f1c86
- DID: All-4 (64GB) @50GB: rounds 1-13 ALL clean bad_words=0, then froze TWICE (BOOT 16:51, 16:58) ~rounds 14-16. Campaign self-stopped (NORUN), Sol idle. 2 crashes.
- STATE: VERDICT: reseat hugely improved all-4 (13 clean rounds vs froze ~round2/pass16 before) but 50GB still NOT reliable on all-4 -- 2 freezes under sustained near-max load. Matches 2DPC/4-ranks-per-channel marginality theory.
- NEXT: Decide w/Max: pound 50GB to 4-crash limit, or back off to find all-4 safe ceiling (e.g 42GB). memtest86+ at console still the only part-convictor.
- LESSON: All-4 64GB on M720s: clean for ~80min/13 rounds at 50GB post-reseat then freezes -- intermittent, load+time dependent, not instant. Reseat helps a lot but doesn't fix the 4-DIMM marginality.

## [2026-06-17 17:41] E1testrunner db0f1c86
- DID: Max removed stick1 from slot4 -> back to 3-stick (2,3,4 slots1,2,3=48GB). Launched 4h SOAK at 42GB. Guard had relaunched stale all-4 50GB config on 3 sticks (OOM risk); fixed via manual clean relaunch to 42GB. round1 crashes=0.
- STATE: 3-stick 42GB soak running, watcher b4aliwbs9 monitoring 4h, wakeup re-armed 20min flex. Soak auto-relaunches through freezes, counts crashes, no disarm.
- NEXT: Report rounds/crashes over 4h. All-4 verdict (13 clean then 2 freezes at 50GB) already logged.

## [2026-06-17 18:05] E1testrunner db0f1c86
- DID: Max re-inserted all 4 sticks (1-4 slots 1-4) + added COOLING FAN (noticed warm stick). Launched all4 64GB 50GB 4h soak. Guard raced stale 3stick config again; fixed via manual clean relaunch. round1, crashes=0, temp 52-57C.
- STATE: all4+FAN soak running, monitor b76dhs55z (4h, re-arms flag thru reboots), wakeup 5mt. Watching if fan beats pre-fan 13-rounds-then-froze.
- NEXT: Report rounds/crashes/temp. Doc updated w/ Phase C. Recurring gotcha: guard cron relaunches stale campaign.sh config on reboot before watcher -> always manual clean relaunch after a stick swap.

## [2026-06-17 18:21] E1testrunner db0f1c86
- DID: all4+FAN soak: rounds 1-2 clean, ROUND 3 bad_words=54 (first bit-flips this session at 50GB), no freeze, temp 56C, crashes=0.
- STATE: all4+FAN soak running, now showing real bit corruption (not just freeze). Monitor b76dhs55z. Different failure mode than pre-fan (which only froze).
- NEXT: Watch if bad_words climbs / freeze follows. Confirms all-4 64GB genuinely faults under load. 2-stick green = still the only solid config.

## [2026-06-17 18:32] E1testrunner db0f1c86
- DID: Sol froze on all-4+FAN soak; Max removed 2 sticks -> 2-stick GREEN config (stick1 slot1 + stick3 slot3 = 32GB). Guard cron had relaunched stale 50GB on the 32GB box, drove it into swap-thrash/reboot. Killed it, locked campaign.sh to 27GB, reset logs, relaunched clean.
- STATE: 2-stick GREEN 27GB 4h soak running (round 1). Monitor by7wbzwuu polling, re-arms at 27GB if NORUN. Self-wake d0a92f54 in 20min.
- NEXT: At wake: tail monitor log, report rounds/crashes/flips/temp. Known-good config, expect clean. Also pending: add all-4+FAN result (R3 bad_words=54 first corruption, then froze) to experiment history doc.
- LESSON: After any physical swap, campaign.sh still holds the PREVIOUS load; guard/@reboot cron relaunches it immediately. On a downsized box that stale higher load OOM-thrashes Sol before you can fix it. Lock campaign.sh config in its OWN ssh call FIRST (it sticks even if launch SSH drops), then reset+launch.

## [2026-06-17 21:00] E1testrunner db0f1c86
- DID: 2-stick GREEN (s1slot1+s3slot3) 32GB @27GB soak ran 45 ROUNDS CLEAN (bad_words=0, ~2.3h) before Max manually restarted Sol at 20:57 to remove the cooling fan + close the case. Sol auto-resumed at 27GB via guard cron, now round 47, ramscan live.
- STATE: Soak continuing in THIS chat, cover closed/no fan, 27GB. crashes=1 = the manual restart, NOT a freeze. Monitor by7wbzwuu live, self-wake re-armed 20min.
- NEXT: Keep monitoring to 4h. 45 clean rounds already = strongest confirmation yet that 2-stick GREEN is rock-solid. Pending: fold all4+FAN bad_words=54 result into history doc.

## [2026-06-17 22:12] E1testrunner db0f1c86
- DID: Killed both stale Pine monitors (old 18:32 one would've disarmed campaign at 22:32 and killed the new run). Launched ONE fresh monitor bxv44opp8 (clean 4h window, disarms ~02:12). Cover-OPEN no-fan 27GB rerun confirmed running independently on Sol (ramscan live, round 1).
- STATE: Cover-OPEN no-fan 2-stick GREEN 27GB rerun LIVE. Monitor bxv44opp8 sole watcher. Self-wake 91849918 fires ~22:31. THERMAL-CONFIRM run.
- NEXT: Report at wake. KEY THERMAL FINDING (from E5): same green pair = 45 rounds clean cover-OPEN vs 4 freezes+2 bit-flips cover-CLOSED no-fan (hit 73C). This rerun should stay cool+clean. Pending: add thermal finding + all4+FAN bad_words=54 to history doc once this run concludes.

## [2026-06-17 22:51] E1testrunner db0f1c86
- DID: Cover-OPEN no-fan rerun FROZE 2x + 1 bit-flip in 20min (64C) => decisive variable is the DIMM FAN, not the cover (fan-on=45 clean 54C; fan-off cover-closed=4 freezes 73C; fan-off cover-open=2 freezes 64C). Max paused to use Sol for work. Sol was stuck in freeze->reboot->cron-rearm LOOP; broke it by PAUSING the guard cron (commented campaign_guard.sh @reboot + */2 lines as #PAUSED_FOR_MAXWORK, crontab backed up to /tmp/ct_backup_*.bak). Catching leftover ramscan at boot to fully idle Sol.
- STATE: Sol being cleared for Max's work. Guard cron PAUSED (active_guard=0). E5 briefed for safety watch (confirm ramscan stays dead, do not load). Catch-loop bw5udjigf finishing.
- NEXT: When Max says RERUN: re-enable cron (sed 's/^#PAUSED_FOR_MAXWORK //' | crontab -), then clean heredoc relaunch. Pending: write thermal/fan verdict + all4+FAN bad_words=54 into history doc.
- LESSON: Sol's guard cron (@reboot + every-2min campaign_guard.sh) AUTO-RE-ARMS campaign.run, so a freezing load self-perpetuates a freeze->reboot->relaunch loop. rm campaign.run alone is NOT enough - must PAUSE the guard cron lines to truly stop a test. Re-enable them before any rerun.
