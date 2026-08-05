# Scribe handover - milestone 8 (~129K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# cwd: C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2
# written: 2026-06-12 12:23:04 by claude-opus-4-8

# HANDOVER - Lak Recovery & Infrastructure Resilience

## GOAL (in Max's words)
"i need resilience, not booting is a major flaw" ? "Yes, make everything resilient."

Max had to interrupt power to three core servers (Cent, Sol, Lak). The immediate goal was confirming they came back online. That expanded into a broader mandate: make the infrastructure resilient so a power cut never leaves a box stranded, and fix the documentation gaps that left this session guessing at core-infra facts (which frustrated Max - "that's my core infrastructure - you guys dropped key facts").

## DECISIONS + WHY
- **Don't weaken the repeat-probe hook.** It fired because identical curls/SSH probes were repeated. Max asked if it was excessive; conclusion reached together: the hook was right about the shape of the error. The correct way to wait on a booting box is a single wait-loop (`until <check>; do sleep 20; done`) which counts as ONE call and is explicitly exempt. Use that pattern, not repeated discrete probes.
- **Master server doc lives in Notion, not local files.** The local `infra_map_tomemex.md` and Memex lacked Lak's LAN IP - that's why .243 was guessed wrongly (real IP is .199). Notion "Servers" page already had .199; the gap was local only.
- **Verify writes, never assume.** Every Notion update was re-fetched to confirm it landed. Continue this.
- **Verify IPs before writing them.** Dax confirmed via SSH port-22 reachability (ICMP blocked on AWS Lightsail, so ping is inconclusive).

## CURRENT STATE
All three servers ONLINE and verified:
- **Sol** - 192.168.1.113, up, SSH confirmed.
- **Centauri** - 192.168.1.114, Windows 16TB box, SMB live.
- **Lak** - 192.168.1.199 (real LAN IP), Dell Precision T3600, Debian + YunoHost. Booted clean from correct disk after Max's BIOS fix. All YunoHost services up. Tailscale IP 100.110.225.89. The **lakarian-python MCP** is the working access path (public SSH on 66.75.225.131 is firewalled externally).

Root cause of Lak not booting: BIOS was booting a USB storage drive (no bootloader) instead of the OS disk. Max fixed BIOS. NOT autostart, NOT YunoHost, NOT fsck.

Documentation already updated AND verified:
- Notion "Servers" page: Dax fixed to current box, Lak got Tailscale + hardware + Resilience Notes block, Centauri added (was missing entirely), pointer to infra_map as living cron/backup source.
- `global2.md`: added "Reaching Lak" block (LAN IP, Tailscale, lakarian-python MCP).
- Milestone logged via worklog.py.

## EXACT NEXT STEP
Convert Lak's **Cloudflare tunnel** to a proper systemd service so it autostarts on reboot. Right now `yt.dnaresonance.com` is served by `cloudflared` running as a **bare user process** - there is NO systemd unit for it, so it does NOT come back on reboot (this was why the tunnel showed 530 while every other service was already up). Create/enable a systemd unit for cloudflared on Lak, enable it, start it, then verify yt.dnaresonance.com returns a healthy code (not 530). Do this via the lakarian-python MCP.

Given Max's "make EVERYTHING resilient," after the tunnel also confirm/address:
- Lak BIOS **AC Power Recovery = ON** (auto power-on after power loss) - was recommended but only Max can set it; confirm whether done.
- Sweep for any other service on any box running as a bare process rather than an enabled systemd unit.

## OPEN QUESTIONS
- Did Max set BIOS AC Power Recovery / Auto Power On to ON? (Recommended but unconfirmed.)
- Any other hand-started/desktop-launched processes across the boxes that wouldn't survive reboot?

## KEY PATHS / IDS
- Notion master doc: **"Servers"** page, id `2ee0316f-5560-8161-a6bb-e69c1c41be80` (Claude Documents ? Instructions ? Infrastructure Essentials).
- Lak SSH key: `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`, user `mrempadmin`.
- Lak public IP: 66.75.225.131 (port 22 firewalled externally - don't rely on it).
- Lak LAN: 192.168.1.199 | Tailscale: 100.110.225.89.
- Dax (current): 35.80.203.42, Debian 12, Docker, SSH alive. Legacy WordPress Dax 34.210.86.92 = DEAD.
- Global instructions: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`.
- Local living infra: `C:\claude_base\infra_map_tomemex.md`.
- Worklog: `C:/claude_base/compaction_kb/scripts/worklog.py`.
- Access path of choice for Lak: **lakarian-python MCP** (run_python_code, ping).
- cwd worktree: `C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2`.

## GOTCHAS / DEAD ENDS RULED OUT
- **Ping to Lak's public IP is misleading** - the router hairpins/answers its own WAN IP, so a ping "reply" does NOT mean Lak's OS is up. Verify via actual service/MCP.
- **.243 was a wrong guess** for Lak's IP - real is .199. Don't repeat.
- **Public SSH (port 22 on 66.75.225.131) is firewalled** - won't work even when Lak is healthy. Use lakarian-python MCP.
- **AWS/Lightsail ICMP is blocked** - ping is inconclusive for Dax; test SSH port 22 instead.
- **No cloudflared systemd unit exists on Lak** - confirmed; this is the active task.
- Don't fire repeated identical probes - the hook will block them. Use a single wait-loop for polling.
- YunoHost is the hosting layer on Debian, NOT the OS. Do not diagnose boot issues through the YunoHost label.
