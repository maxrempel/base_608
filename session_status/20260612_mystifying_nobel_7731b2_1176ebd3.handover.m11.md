# Scribe handover - milestone 11 (~166K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# cwd: C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2
# written: 2026-06-12 12:59:47 by claude-opus-4-8

# HANDOVER - Lak Power-Loss Recovery & Resilience Job

## GOAL (in Max's words)
- Opening: "i had to interrupt power to cent, sol and lak - are they back online?"
- Escalated to: "i need resilience, not booting is a major flaw."
- Then: "Yes, make everything resilient" ? narrowed to "yes, all things on lak - test and fix resilience."
- Final standing request (the live one): **"Steps in bios please."** - Max wants the exact step-by-step to set the BIOS resilience option on Lak's Dell Precision T3600.

Underlying theme Max hammered repeatedly: **do NOT guess on core infrastructure.** He was angry that basic facts (Lak's LAN IP) weren't documented anywhere ("the basic fundamental knowledge is not available to you. Super bad"). Always pull facts from Memex/Notion FIRST before probing.

## DECISIONS + WHY
- **Root cause of Lak not booting was BIOS boot order** - it was booting the USB storage drive (no bootloader) instead of the OS disk. Max found this himself; Max fixed it; this last successful boot (with drives plugged in) proves the fix.
- **Stopped network-guessing, switched to fact-finding from Memex/Notion** - after Max's rebuke and a rejected tool call. This is the standing lesson.
- **Did NOT touch anything on Lak** - the resilience job turned out to need zero fixes; everything was already correct. Play-safe, read-only was the mandate.
- **Corrected a wrong doc note** - I had written "Cloudflare tunnel is fragile / not a systemd service." That was wrong (I checked system scope only). It IS resilient: a USER service with linger enabled. Corrected in both Notion and global2.md.
- **Did NOT touch Centauri** - out of scope; only flagged.

## CURRENT STATE
- **Sol (.113), Centauri (.114), Lak (.199): all online.** Verified.
- **Lak fully resilient, verified end-to-end:** all system services enabled+active (nginx, php8.3-fpm, postgresql, mysql, slapd, cron, ssh, tailscaled); 3 user services active with linger=yes (autostarted unattended on the cold boot); cron proven live; yt.dnaresonance.com = HTTP 200; ALL lak-* Healthchecks monitors green.
- **Docs updated + verified:** Notion "Servers" page and global2.md now carry Lak's real LAN IP, Tailscale IP, hardware, and the corrected tunnel note.
- **Autonomous timer: DISARMED.** The job was declared complete. The stability pass passed clean.
- Max then asked the AC Recovery setting was real ? confirmed real via web search.
- Max's last message asks for the **BIOS steps**. This is the only open action.

## EXACT NEXT STEP
Answer "Steps in bios please." with the T3600 procedure to set **AC Recovery = On** (and optionally re-confirm boot order). Plain English, no tools needed:
1. Power on, tap **F2** repeatedly at the Dell logo ? enters System Setup (BIOS).
2. Go to **Power Management** ? find **AC Recovery** (options: On / Off / Last).
3. Set it to **On** (server should auto-power-on when AC returns; default is Off - that's why Lak stayed dark after the cut).
4. Optionally verify **Boot Sequence**: internal OS disk first, USB below/disabled (Max says he already fixed this).
5. Press **F10** to Save and Exit.
(F12 at logo = one-time boot menu, for reference.)

## OPEN QUESTIONS
- None awaiting Max for the BIOS answer - just deliver the steps.
- Flagged-but-not-asked: does Max want Centauri's two down monitors fixed (separate job)?

## KEY PATHS / IDs
- **Lak:** Dell Precision T3600, Debian + GUI, YunoHost is a LAYER (not the OS). LAN **192.168.1.199**, Tailscale **100.110.225.89**, public **66.75.225.131** (OpenWrt port-forward; public SSH NOT reachable from inside LAN).
- **Access path to Lak:** the **lakarian-python MCP** (tools `mcp__lakarian-python__ping` / `run_python_code`) - the working bridge. Use this, not public SSH.
- **Lak user services:** `sizzler-d3-tunnel.service`, `sizzler-d3.service`, `yt-transcript.service` - manage with `systemctl --user` (NOT system scope). Linger via `loginctl enable-linger mrempadmin`.
- **CF tunnel:** `d3-sizzler-lakarian`, tunnel_id ba4f6187-71bc-4924-880f-d48bab050eac, binary at /home/mrempadmin/00HA1py/sizzler/cloudflared, serves yt.dnaresonance.com.
- **Dax:** current = 35.80.203.42 (Debian 12, Docker, us-west-2). Legacy WordPress 34.210.86.92 is DEAD.
- **Notion "Servers" page:** id `2ee0316f-5560-8161-a6bb-e69c1c41be80` (Claude Documents > Instructions > Infrastructure Essentials).
- **global2.md:** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (LAK section ~line 513).
- **Healthchecks API key:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/healthchecks_io_creds_20260604.txt`; API https://healthchecks.io/api/v3/checks/ with X-Api-Key header.
- **infra_map_tomemex.md** = living cron/backup source (local, C:\claude_base).
- **Worklog:** `C:\claude_base\worklog\mystifying_nobel_7731b2_6cbd77f5a7.md` (worklog.py to append).

## GOTCHAS / DEAD ENDS RULED OUT
- **`systemctl is-active cloudflared` (system scope) returns "not found" - this does NOT mean it's down.** The tunnel is a USER service. Check with `systemctl --user`.
- **.243 was a phantom guess** - never confirmed as Lak. Lak's real IP is .199.
- **Public-IP ping can be the router answering, not the box** - don't trust ICMP on 66.75.225.131 as proof Lak is up.
- **Suicide-prevention hook** (block_death_spiral.py) blocks repeated identical Bash calls across turns. To poll a booting box, use ONE wait-loop (`until <check>; do sleep 20; done`) - that's exempt. Don't fire the same curl 3x.
- **AC Recovery default is Off** on the T3600 - confirmed via web search; exact BIOS label is "AC Recovery" (not "AC Power Recovery").
- **MCP run_python_code times out on heavy recursive greps** over ~/00HA1py - keep commands light, set short per-command timeouts.
- Communication style: pingpong, purple-circle TLDR markers, plain English (no code dumps), ASCII-only except sanctioned circle markers, verify Notion writes loudly.
