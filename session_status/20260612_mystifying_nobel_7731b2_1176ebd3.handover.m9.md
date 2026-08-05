# Scribe handover - milestone 9 (~144K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# cwd: C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2
# written: 2026-06-12 12:34:18 by claude-opus-4-8

# HANDOVER - Lak Power-Loss Recovery & Server-Doc Resilience

## GOAL (in Max's words)
Max interrupted power to three servers (cent, sol, lak) and wanted to know if they came back online. The work then expanded into: "i need resilience, not booting is a major flaw" and "make everything resilient." His final question, still unanswered: **"So you are saying all monitors and everything is resilient?"**

## CURRENT STATE - all three servers are UP
- **Sol** (192.168.1.113) - fully up, confirmed via SSH, fresh boot.
- **Centauri** (192.168.1.114) - Windows box, up, SMB (445) live.
- **Lak** (192.168.1.199) - fully up. Real LAN IP is **.199** (NOT .243, which was an earlier wrong guess). Tailscale IP **100.110.225.89**. All YunoHost services autostart via systemd. The Cloudflare tunnel + d3 app + yt-transcript run as **user services with linger enabled**, so they ALSO autostart on boot with no login. **yt.dnaresonance.com returns HTTP 200** - serving fine.

Max has **already changed the BIOS boot order**, and the current successful boot happened **with the USB drives still plugged in** - meaning the fix is confirmed working (it boots the OS disk now, not the USB).

## DECISIONS + WHY
- **Root cause of "Lak not booting" was the BIOS booting the USB storage drive** (which has no bootloader) instead of the internal OS disk. The "ping replies" seen early were the router answering its own WAN IP, not Lak. This was NOT a YunoHost issue, NOT fsck, NOT a missing autostart. Max found this himself.
- **Lak is a Dell Precision T3600**, running **Debian** with a desktop GUI; **YunoHost is just the hosting layer on top of Debian, not the OS.** (Max was annoyed that earlier reasoning leaned on YunoHost - correct his framing if it recurs.)
- **An earlier note claiming "the tunnel is fragile / not a real service" was WRONG and has been corrected** in both docs. The tunnel is `sizzler-d3-tunnel.service`, a user service, enabled, with linger on - it IS resilient.

## DOCS UPDATED & VERIFIED
- **Notion "Servers" page** (id `2ee0316f-5560-8161-a6bb-e69c1c41be80`), under Claude Documents ? Instructions ? Infrastructure Essentials. Updated: fixed Dax to current box (**35.80.203.42**, Debian 12, Docker; old WordPress Dax **34.210.86.92** is dead), added Lak Tailscale IP + hardware + resilience notes, added Centauri (was missing entirely), pointer to infra_map. All changes verified live by re-fetching.
- **Global instructions:** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - added a "Reaching Lak" block (LAN IP .199, Tailscale, lakarian-python MCP as the working access path) and corrected the tunnel note.

## EXACT NEXT STEP
**Answer Max's final question directly and honestly.** The honest answer:
- **Boot resilience: now solid** - he fixed the boot order; it booted with USBs plugged and chose the OS disk.
- **Service resilience: solid** - all system + user services autostart on boot, no login needed.
- **Still genuinely open: AC Power Recovery.** Recommend he set **AC Power Recovery = ON** in the T3600 BIOS (Power Management) so Lak self-powers-on after a power cut instead of sitting dead. This is the one remaining hands-on gap.
- **"All monitors" part:** be careful - the word "monitors" hasn't been pinned down. It may mean monitoring/alerting, or the other servers. Do NOT overclaim. Verify before asserting that monitoring is resilient - there is no confirmed monitoring/alerting layer discussed yet.

## OPEN QUESTIONS AWAITING MAX
- What does Max mean by "all monitors" - monitoring/alerting tooling, or the servers collectively? Clarify before answering.
- Has he set AC Power Recovery ON, or only boot order?

## KEY PATHS / IDS / COMMANDS
- **lakarian-python MCP** = the working SSH bridge / access path to Lak (use `ping`, `run_python_code`). This is the blessed way in.
- Lak SSH key: `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`, user `mrempadmin`. Public-IP SSH (66.75.225.131) is firewalled externally - don't rely on it.
- Sol SSH: `~/.ssh/sol_key`, user `maxre`, 192.168.1.113.
- Lak public IP 66.75.225.131; CF tunnel public service: yt.dnaresonance.com.
- Infra docs: `C:\claude_base\infra_map_tomemex.md` (living cron/backup source), `centauri_monitoring_handover_tomemex.md`.
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` and `session_status.py report "..."` - both already used to log this milestone.

## GOTCHAS / DEAD ENDS RULED OUT
- **Don't re-fire identical probes** - a hook blocks repeated identical checks. To watch a booting box, use ONE wait-loop (`until <check>; do sleep 20; done`) which is exempt, NOT three separate curls. This was a real friction point; Max noted the hook "must be negotiable" - it fails open and the poll-loop pattern is the sanctioned approach.
- **.243 was a wrong guess for Lak** - real IP is .199.
- **Don't invoke YunoHost to diagnose OS/boot behavior** - it's the Debian/systemd layer that matters; Max pushed back hard on this.
- **AWS Lightsail blocks ICMP** - use a TCP port-22 check, not ping, to confirm Dax is alive.
- The agent cannot touch BIOS - all BIOS changes are hands-on at the box by Max only.
