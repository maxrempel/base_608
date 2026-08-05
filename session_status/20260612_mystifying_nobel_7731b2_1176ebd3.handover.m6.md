# Scribe handover - milestone 6 (~102K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# cwd: C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2
# written: 2026-06-12 11:59:25 by claude-opus-4-8

# HANDOVER - Lakarian (Lak) Post-Power-Cut Recovery

## GOAL (in Max's words)
Max interrupted power to three machines - **Cent, Sol, and Lak** - and wants to confirm they're "back online." As the session evolved, his real concern sharpened to: **"i need resilience, not booting is a major flaw."** He's frustrated that core infrastructure facts about Lak (his main box) were missing from available docs ("That's my core infrastructure - you guys dropped key facts"). The immediate ask at the end: **"check lak now."**

## DECISIONS + WHY
- **Don't weaken the repeat-probe hook; fix the pattern instead.** The hook blocked repeated identical curl/SSH probes. Max asked if the hook was excessive. Conclusion reached together: the hook was right that fired-the-same-probe-3x is wrong, BUT polling a genuinely-changing booting box is legitimate. The correct, hook-friendly approach is **a single wait-loop** (`until <check>; do sleep 20; done`) which counts as ONE call and is explicitly exempt from the repeat rule. Max seemed to accept this.
- **The root cause of Lak being down was identified by Max himself** (he "found the problem"): Lak's BIOS was booting from a **USB storage drive that has no bootloader**, so the OS never started. The ICMP ping replies were the **router answering its own WAN IP**, NOT Lak being alive. This overturned all earlier theories (autostart misconfig, YunoHost issue, fsck stall).
- **YunoHost is NOT the OS** - Max corrected this firmly. Lak runs **Debian Linux with a desktop GUI**; YunoHost is just a hosting layer on top. Services (nginx, postgres, cloudflared) are normal systemd services that **autostart on boot, no GUI login needed**. So once it boots the correct disk, everything should come back on its own.

## CURRENT STATE
- **Sol (192.168.1.113)** - fully up. Confirmed via SSH, ~20 min uptime (fresh boot). DONE.
- **Centauri (192.168.1.114)** - up. Windows box (TTL=128), SMB port 445 open. DONE. (Note: "Cent" = Centauri.)
- **Lak** - still NOT confirmed healthy as of last check. After Max edited the BIOS and powered up again, the last probe showed: **CF tunnel (yt.dnaresonance.com) = HTTP 530 (origin offline), Nextcloud = no connection, public SSH = timeout.** May still be mid-boot, OR the BIOS fix didn't take.
- Max has just said **"check lak now"** - this is the pending action.

## EXACT NEXT STEP
Run **ONE wait-loop** (not repeated separate probes - that trips the hook) that polls Lak's Cloudflare tunnel every ~20s until it comes up, then report. Suggested check target: `https://yt.dnaresonance.com/` returning a non-530 code, OR `https://lakarian-city.ynh.fr/` responding. The moment services come up, notify Max. If after a reasonable window it's still 530, report that the BIOS boot-order fix may not have worked.

## OPEN QUESTIONS (awaiting Max)
1. Is YunoHost actually still on Lak, or is that doc line outdated? (Asked, not answered.)
2. **What is Lak's real LAN IP?** Never confirmed - this is a recorded knowledge gap. Guessed at .243 but SSH timed out so it was never verified as Lak.
3. Resilience follow-ups Max should set in BIOS (raised, not confirmed done): **AC Power Recovery = ON** (auto power-on after power cut - the big one for an always-on server), and **boot order = internal OS disk first, USB below/disabled**.

## KEY PATHS / IDs / COMMANDS
- **Sol:** 192.168.1.113, SSH `maxre@` with key `~/.ssh/sol_key`
- **Centauri:** 192.168.1.114, Windows, SMB/445
- **Lak public IP:** 66.75.225.131 (router hairpins LAN?WAN, which caused the misleading pings)
- **Lak hostnames:** lakarian-city.ynh.fr; CF-tunnel service at yt.dnaresonance.com (origin = Lak)
- **Lak hardware:** Dell Precision T3600 tower, Debian + GUI, hostname/label "RempelServer"
- **Lak SSH key:** `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`, user `mrempadmin`
- **Lak creds file:** `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lak_mrempadmin_creds_20260519.txt`
- **Nextcloud path on Lak:** /home/yunohost.app/
- **Infra docs:** `/c/claude_base/infra_map_tomemex.md`, `/c/claude_base/centauri_monitoring_handover_tomemex.md`
- **Memex search** is available (MCP tool) and was used to find the USB-boot fact - use it for Lak fundamentals.
- BIOS keys for the T3600: **F12** = one-time boot menu, **F2** = setup, **F10** = save/exit.

## GOTCHAS / DEAD ENDS RULED OUT
- **Ping replies from Lak are unreliable** - the router answers ICMP on the public IP even when Lak's OS is dead. Don't treat ping as "Lak is up." Use the CF tunnel / actual services as the truth signal.
- **Public SSH (port 22 on 66.75.225.131) is firewalled externally** - repeatedly timed out. Not a usable remote login path. There is currently **no confirmed working remote login to Lak** even when healthy; this is an unclosed access-resilience gap.
- **Don't fire repeated identical probes** - the hook blocks it (fails open, just nudges). Use a single wait-loop instead.
- **Lak's LAN IP is recorded nowhere** (not infra map, not Memex). .243 was a guess, unverified. Once Lak is up, **capture its real LAN IP and write it into the infra map** so future sessions don't fly blind.
- Ruled out as causes of the outage: missing autostart, YunoHost fault, fsck stall. The real cause was **wrong BIOS boot device (USB without bootloader)** - Max edited the BIOS to fix it.
- Tone note: Max was visibly frustrated about missing core-infra knowledge. Lead with facts pulled from Memex/docs, not guesses.
