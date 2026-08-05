# Scribe handover - milestone 6 (~94K tokens)
# session: 20260612_gallant_kilby_0e09da_a3fbd38b
# cwd: C:\claude_base\.claude\worktrees\gallant-kilby-0e09da
# written: 2026-06-12 11:50:20 by claude-opus-4-8

# HANDOVER

## GOAL (in Max's words)
"i had to interrupt power to cent, sol and lak - are they back online?" - Max hard power-cycled three of his core infrastructure machines and needs confirmation each one is fully back up and serving. The live question right now: **"how to reset boot?"** - Lak is booting from the wrong device and Max needs the steps to fix its boot order.

## DECISIONS + WHY
- **Don't keep repeating the SSH/ping probe on Lak.** It kept returning the same dead result; fingerprinting the host differently (MAC/vendor, nbtstat, port checks) was more informative than re-running the same failing command.
- **Stop guessing and pull real facts from Memex / local docs.** Max was explicit and angry that core-infra fundamentals were missing - the assistant had been guessing at Lak's LAN IP (.243) and leaning on the "YunoHost" label to reason about boot behavior. The decision: treat Memex + infra docs as the source of truth, not inference.
- **Root cause identified as wrong boot device, not autostart/YunoHost/fsck.** After the doc search, the real cause: BIOS was booting Lak's **USB storage drive (which has no bootloader)** instead of the OS disk, so the OS never came up. The ping "reply" Max and the assistant saw was **the router answering its own WAN IP**, not Lak being alive.
- **Clarified YunoHost is not the OS.** Max corrected the assistant: Lak runs **Debian Linux with a desktop GUI**; YunoHost is only the hosting layer on top. Once Lak boots from the correct OS disk, **all services autostart via systemd - no GUI login required.**

## CURRENT STATE
- **Sol (192.168.1.113)** - fully up. Confirmed via SSH login, ~20 min uptime (consistent with the fresh power-cycle). DONE.
- **Centauri (192.168.1.114)** - up. Windows box (TTL=128), SMB port 445 open and serving. DONE.
- **Lak** - NOT up. OS never booted because BIOS selected the USB storage drive. SSH, HTTPS, Nextcloud, and the Cloudflare tunnel (yt.dnaresonance.com returns CF 530 = origin offline) are all dead. Max said "found the problem" and "i powered up again" - a reboot/boot-order fix may be in progress.

## EXACT NEXT STEP
Answer Max's question: **how to reset/fix the boot order on Lak.** Lak is a **Dell Precision T3600 tower** - the relevant steps are the Dell BIOS boot-order path: tap **F12** at power-on for a one-time boot menu (pick the OS disk), or **F2** to enter BIOS Setup and change the permanent boot sequence so the internal OS disk is ahead of USB. Simpler interim fix: **physically pull the USB storage drive** so BIOS falls through to the OS disk. After it boots, verify all services are back and **record Lak's actual LAN IP into the infra map** (see Gotchas).

## OPEN QUESTIONS (awaiting Max)
- Did pulling the USB / fixing the boot order make Lak boot from the correct OS disk?
- Is YunoHost actually still on Lak, or is that line in the saved instructions outdated?
- What is Lak's real LAN IP? (Still unknown - never confirmed.)

## KEY PATHS / IDS
- cwd: `C:\claude_base\.claude\worktrees\gallant-kilby-0e09da`
- Sol: `192.168.1.113`, SSH key `~/.ssh/sol_key`, user `maxre`
- Centauri: `192.168.1.114` (Windows, SMB/445)
- Lak public IP: `66.75.225.131` (lakarian-city.ynh.fr; router hairpins, port 22 firewalled externally)
- Lak CF tunnel health check: `https://yt.dnaresonance.com/` (530 = origin/tunnel offline)
- Lak SSH creds/key: `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`, user `mrempadmin`; creds file `lak_mrempadmin_creds_20260519.txt` in same dir
- This machine: Pine, `192.168.1.123`
- Infra docs: `/c/claude_base/infra_map_tomemex.md`, `/c/claude_base/centauri_monitoring_handover_tomemex.md`
- Memex search available via the memex MCP tool

## GOTCHAS / DEAD ENDS
- **A ping reply from Lak's public IP does NOT mean Lak is up** - the router answers its own WAN IP. TTL=64 was misread as "the Linux box." Don't trust ICMP for Lak's status; use a real service (SSH, the website, or the CF tunnel).
- **.243 was never confirmed to be Lak** - it was a guess from a LAN sweep and SSH to it timed out. Do not assume .243 = Lak.
- **.114 IS Centauri** (Windows, TTL=128, SMB open), not Lak.
- **Don't reason from the "YunoHost" label** to diagnose boot/autostart. The OS is Debian + GUI; YunoHost is just the hosting layer.
- **Lak's LAN IP is recorded nowhere** - not in the infra map, not in Memex. This is the knowledge gap that caused all the guessing. Once Lak is up, capture its real LAN IP and write it into `infra_map_tomemex.md`.
- A long curl timeout once cancelled an in-progress LAN sweep - run slow web checks separately from sweeps.
- Max is frustrated that core-infra fundamentals were missing; prioritize confirmed facts from docs over inference, and don't re-run the same failing probe.
