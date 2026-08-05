# Scribe handover - milestone 10 (~161K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# cwd: C:\claude_base\.claude\worktrees\mystifying-nobel-7731b2
# written: 2026-06-12 12:41:50 by claude-opus-4-8

# HANDOVER - Lak Power-Loss Recovery & Resilience Audit

## GOAL (in Max's words)
Started as: "i had to interrupt power to cent, sol and lak - are they back online?" Evolved into: "make everything resilient" ? narrowed to "all things on lak - test and fix resilience." The current live question: **"is [Confirm BIOS 'AC Power Recovery = ON'] = real or wishful thinking? Check laks' model and bios online."**

Max cares deeply about resilience for his **core infrastructure** and was visibly frustrated that basic facts about his core box (Lak) were missing from the docs. He wants accuracy, not guesses - and he wants to know whether an instruction I gave him is actually real for his specific hardware.

## DECISIONS + WHY
- **Don't weaken the anti-repeat hook** - it correctly flagged that repeated identical probes were a death-spiral pattern. The fix was to use a single wait-loop (`until <check>; do sleep 20; done`, which counts as ONE call and is exempt) instead of firing separate identical curls. The hook fails open and is already negotiable.
- **Stopped guessing Lak's IP and pulled real facts** - after Max called out the missing fundamentals, I used Memex + Grep + the lakarian-python MCP to get ground truth instead of inferring.
- **Verify every write, never assume** - re-fetched the Notion page after each update to confirm changes landed.
- **Corrected my own earlier wrong note** - I initially wrote that Lak's CF tunnel was "fragile / not a real service." That was WRONG. It IS a proper user systemd service with linger enabled, so it autostarts on boot with no login. I corrected this in both docs.

## CURRENT STATE
All three servers are **online and verified**:
- **Sol** - 192.168.1.113, up (fresh boot confirmed via SSH).
- **Centauri** - 192.168.1.114, Windows, up (SMB live). NOTE: its `centauri-host` and `centauri-odysee-sync` Healthchecks monitors are DOWN despite the box being online - flagged to Max, NOT touched (out of scope).
- **Lak** - 192.168.1.199 (real LAN IP, finally confirmed), Tailscale 100.110.225.89. Dell Precision T3600 tower, Debian + GUI, YunoHost is the hosting layer on top (NOT the OS).

**Root cause of the whole incident:** Lak's BIOS was booting a plugged-in USB *storage* drive (no bootloader) instead of the internal OS disk. The "ping replies" I saw early were the router answering its own WAN IP, not Lak. Max found this and fixed the boot order in BIOS. This current boot succeeded **with drives plugged in**, proving the boot-order fix works.

**Lak resilience: fully tested end-to-end, all green:**
- All system services (nginx, php8.3-fpm, postgres, Nextcloud, mail/LDAP) enabled + active, autostart via systemd.
- User services (`sizzler-d3-tunnel`, the d3 app, `yt-transcript`) are systemd USER services with **linger enabled** ? autostart on boot, no login needed.
- yt.dnaresonance.com serves HTTP 200.
- All Lak Healthchecks monitors GREEN post-reboot: lak-host, lak-cpu-temp, both backups, restic backup.

**Docs updated and verified:** Notion "Servers" page (fixed Dax, added Lak Tailscale+hardware+resilience notes, added missing Centauri) and global2.md (added "Reaching Lak" block + corrected the tunnel note).

**Autonomous timer:** A 240s wake was armed for a single read-only stability re-check during Max's break. That may have fired or be pending.

## EXACT NEXT STEP
Answer Max's actual question: **Does the Dell Precision T3600 actually have an "AC Power Recovery" BIOS setting, or did I invent it?** Research the real T3600 BIOS online (web search) - confirm the exact setting name, where it lives in the menu, and its options. Dell typically calls this "AC Recovery" or "AC Power Recovery" under Power Management with options Off / On / Last (Last State). Report honestly whether my instruction was real or wishful thinking. Do NOT pad - give Max the verified truth.

## OPEN QUESTIONS AWAITING MAX
1. The BIOS "AC Power Recovery = ON" confirmation - this is the live question; he's asking me to verify it's real first.
2. (Flagged, no rush) Centauri's two down monitors - when he's back.

## KEY PATHS / IDS / COMMANDS
- **Lak access:** lakarian-python MCP (working SSH bridge - the blessed access path). LAN 192.168.1.199, Tailscale 100.110.225.89, public 66.75.225.131 (public SSH port 22 is firewalled externally - do NOT rely on it).
- **Lak SSH key:** `/c/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`, user `mrempadmin`.
- **Notion master doc:** "Servers" page, id `2ee0316f-5560-8161-a6bb-e69c1c41be80` (Claude Documents ? Instructions ? Infrastructure Essentials).
- **Global instructions:** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` ("LAK = LAKARIAN" + new "Reaching Lak" block).
- **Living cron/backup source:** `C:\claude_base\infra_map_tomemex.md`.
- **Healthchecks creds:** `/c/Users/maxre/Nextcloud/zSyncMain/ssh/healthchecks_io_creds_20260604.txt`.
- **Worklog/status scripts:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` and `.../session_status.py report "..."`.
- **Dax (cloud):** current = 35.80.203.42 (Debian 12, Docker, SSH:22 open). DEAD/legacy = 34.210.86.92 (old WordPress, stale in old docs).

## GOTCHAS / DEAD ENDS RULED OUT
- **YunoHost is NOT the OS** - it's a hosting layer on Debian. Max was angry I leaned on it to diagnose a boot issue. Don't repeat.
- **The .243 IP guess was WRONG** - Lak is .199. Never guess Lak's IP again; it's now recorded.
- **Public ping to Lak is unreliable** - router hairpins/answers its own WAN IP, giving false "alive" signals. Use the MCP or LAN/Tailscale IP.
- **The CF tunnel is NOT fragile** - I wrongly claimed this early; it's a proper linger-enabled user service. Already corrected in docs.
- **fsck / missing-autostart theories were both wrong** - the only real failure was USB boot order.
- **Don't fire repeated identical probes** - use a single wait-loop to poll a booting box (hook-exempt).
- **AC Power Recovery / BIOS is hands-on only** - I cannot edit BIOS. Max does it physically. Boot order is already fixed and proven.
- **Sol and Centauri monitoring was never fully rolled out** (per infra map) - only Lak and Dax. Don't claim those two are monitored.
- Context was near the ~169K compaction threshold at session end.
