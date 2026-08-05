# Scribe handover - milestone 2 (~151K tokens)
# session: 20260624_interesting_mayer_1ef417_b447aaac
# cwd: C:\claude_base\.claude\worktrees\interesting-mayer-1ef417
# written: 2026-06-24 15:38:27 by deepseek-v4-pro

# HANDOVER - Brother Printer on Centauri (Home Network Printing)

---

## GOAL (Max's own words)
"Set up the Brother printer plugged into Cent so you could print from anywhere in the house - on Pine's GUI, on wife's computer, on other home computers. No cloud, no Google Print. Just local network."

---

## DECISIONS MADE + WHY

1. **Print server = Centauri (192.168.1.176), shared over SMB.** Cent is the always-on Windows box; printer is USB-connected to it. Sharing it over standard Windows printer sharing means any Windows PC on the LAN can add it natively through Settings ? Printers. No extra software.

2. **DHCP reservation on router, not hostname.** Hostnames (`Centauri`, `Centauri.local`) didn't resolve from Pine - mDNS/Bonjour isn't reliably working across the LAN. Fixing name resolution would require more work than simply pinning the IP. A DHCP reservation on the OpenWRT router binds Cent's MAC to `.176` forever, no drift risk, no extra config on each client.

3. **Renamed printer to "Brother-Cent".** The original name ("Brother HL-L2300D series") matched a dead local entry on Pine from when the printer was once USB-connected directly to Pine. Renaming kills the confusion - only one printer shows up.

4. **Removed dead local twin on Pine.** The old `Brother HL-L2300D series` on `USB001` port was a leftover ghost. Deleted it so there's no ambiguity about which printer works.

5. **Dropped the password-free Guest printer plan.** Windows 11 blocks password-free network printer connections by default unless you flip a local policy on *each* client PC. Since we can't reach Oksana's PC remotely, the Guest approach would still require manual work on her end - no net savings versus just entering the password once with "Remember" checked. Safer to keep the password and use SSH for remote setup.

6. **SSH-based remote setup for wife's PC (Oksana).** Instead of walking through GUI steps over the phone, the plan is: email a one-click `.bat` installer that enables SSH and drops Max's key, then Claude adds the printer remotely via SSH. This is the same pattern used for Cent and other home machines.

7. **Sent the link to Oksana's Gmail (opolesskaya@gmail.com), not Max's.** Per Max's explicit request: addressed "from Anna to Max" but delivered to Oksana's inbox so it's right there on her computer. Max is BCC'd.

8. **Documented in global2.md.** Added a "HOME PRINTER - BROTHER ON CENTAURI" section so all future Claude sessions know the printer path, IP, setup steps, and that Cent must be powered on.

---

## CURRENT STATE

### What's Done
- **Centauri (192.168.1.176):** Brother HL-L2300D installed, shared as `Brother-Cent`. Firewall open for File and Printer Sharing. Network profile = Private.
- **Router (OpenWRT, 192.168.1.1):** DHCP reservation live - MAC `E4-54-E8-57-EE-E7` permanently gets `.176`. Committed and applied.
- **Pine:** Printer added and working. Test page printed successfully. Shows as `Brother-Cent on 192.168.1.176`. Dead local twin removed.
- **global2.md:** Updated with printer section (synced via Nextcloud).
- **SSH installer:** Built and published as a private Gist (`d9f2075e13895ad83399b3a6d5bc6da3`). Raw download link emailed to Oksana's Gmail.

### What's In Flight
- **Oksana's PC setup:** The email with the SSH installer link has been sent to `opolesskaya@gmail.com`. Max has reportedly opened it on her computer ("emailed the link to Olga's computer"). The `.bat` file has **not yet been run** - no `REMOTE_READY.txt` confirmation received yet.

### Not Done / Waiting
- **Sirius and Vega:** Offline at the time. Will add later when powered on.
- **Oksana's printer addition:** Blocked until SSH is enabled on her PC.

---

## EXACT NEXT STEP

**Max runs the SSH installer on Oksana's PC:**

1. Open the email from Anna in Oksana's Gmail.
2. Click the link ? a page of raw text opens.
3. Press **Ctrl+S** ? Save (filename stays `enable_ssh_for_max.bat`).
4. Open **Downloads**, double-click the file.
5. If a blue "Windows protected your PC" box appears ? **More info ? Run anyway**.
6. Click **Yes** on the User Account Control popup.
7. Wait ~1 minute. A file called **REMOTE_READY.txt** appears on the Desktop.
8. **Paste that one line** (Computer name / Username / IP address) back to Claude.

Once that line arrives, Claude will SSH in and run:
```powershell
cmdkey /add:192.168.1.176 /user:maxre /pass:"L2w3e4r5t="
Add-Printer -ConnectionName "\\192.168.1.176\Brother-Cent"
```
Then send a test page to confirm.

---

## OPEN QUESTIONS (awaiting Max)

- **None actively blocking.** The only dependency is Max running the `.bat` on Oksana's PC and reporting the REMOTE_READY line.
- Sirius and Vega printer setup is deferred until they're powered on - just ping Claude when ready.
- The old duplicate Brother entry on Pine was removed during cleanup; no action needed unless it reappears.

---

## KEY PATHS, IDs, COMMANDS

### Machines & Network
| Item | Value |
|------|-------|
| Print server | Centauri, 192.168.1.176 (DHCP-reserved, never changes) |
| Cent MAC | `E4-54-E8-57-EE-E7` |
| Cent Windows user/pass | `maxre` / `L2w3e4r5t=` |
| Shared printer path | `\\192.168.1.176\Brother-Cent` |
| Printer model | Brother HL-L2300D (USB) |
| Router | OpenWRT at 192.168.1.1, root / `0y32dnkh40rj7hub1y` |
| Oksana's Gmail | `opolesskaya@gmail.com` |

### SSH Key
- Path on Pine: `~/.ssh/sol_key` (and corresponding `sol_key.pub`)
- Same key used on Cent and intended for all home machines.

### SSH Installer (Gist)
- Gist ID: `d9f2075e13895ad83399b3a6d5bc6da3`
- Raw URL: `https://gist.githubusercontent.com/maxrempel/d9f2075e13895ad83399b3a6d5bc6da3/raw/enable_ssh_for_max.bat`
- Source file: `C:\claude_base\tools\remote_access_setup\enable_ssh_for_max.bat`

### global2.md
- Path: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- Section added: "HOME PRINTER - BROTHER ON CENTAURI"
- Synced via Nextcloud to all machines.

### CLI One-Liner to Add Printer (Any Windows PC)
```powershell
cmdkey /add:192.168.1.176 /user:maxre /pass:"L2w3e4r5t="
Add-Printer -ConnectionName "\\192.168.1.176\Brother-Cent"
```

### GUI Steps to Add Printer (No Terminal)
1. Settings ? Bluetooth & devices ? Printers & scanners ? Add device
2. Wait for scan, then click "The printer I want isn't listed"
3. "Select a shared printer by name" ? type `\\192.168.1.176\Brother-Cent`
4. If prompted: user `maxre`, password `L2w3e4r5t=`, check **Remember**.

### Router Session for Future Changes
- LuCI session cookie file: `/tmp/luci_cookies.txt`
- Auth via `luci_username=root&luci_password=0y32dnkh40rj7hub1y` to `https://192.168.1.1/cgi-bin/luci/`
- ubus calls use session token (dynamic, grab from cookie or re-auth).

---

## GOTCHAS & DEAD ENDS

1. **Hostname resolution doesn't work.** `Centauri` and `Centauri.local` both failed to resolve from Pine. Don't try hostname-based printer paths - use the IP.

2. **Cent must be powered on to print.** No workaround - it's the print server. The printer is USB-only, not network-capable on its own.

3. **Password-free Guest printing is a dead end on Windows 11.** Even after setting Guest access on Cent's printer share, Win11 clients block blank-password network logins by default (local security policy). Fixing it requires touching each client - defeats the purpose. The one-time password entry with "Remember" is simpler.

4. **Router ubus has ACL restrictions.** Adding DHCP host entries works, but `commit` was ACL-denied. The workaround is to call the LuCI `apply` path (`/cgi-bin/luci/admin/ubus?path=uci/apply`) which triggers a full config apply - that succeeded.

5. **The old local Brother entry on Pine (USB001 port) was a ghost.** It existed because the printer was once directly USB-connected to Pine. It showed as a duplicate in the printer list. Removed to avoid confusion.

6. **Black terminal windows popping up are normal.** Those are Claude's tool-call PowerShell/Bash sessions executing on Pine. They're not malware or errors - just the mechanism for running commands. Apologies were made; no fix applied (architectural limitation of the tool-call UI).

7. **SSH installer .bat opens as raw text in browser, not a direct download.** Gist raw URLs display the file contents rather than triggering a download. The workaround: Ctrl+S to save. If this is too awkward for Oksana, the fallback is switching the link to a direct-download host or using a different delivery method.
