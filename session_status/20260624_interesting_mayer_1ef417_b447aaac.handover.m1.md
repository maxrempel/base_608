# Scribe handover - milestone 1 (~147K tokens)
# session: 20260624_interesting_mayer_1ef417_b447aaac
# cwd: C:\claude_base\.claude\worktrees\interesting-mayer-1ef417
# written: 2026-06-24 15:10:29 by deepseek-v4-pro

# HANDOVER: Brother Printer (Centauri) Setup & Remote Printer Access for Oksana

## GOAL (in Max's own words)
*   "I just plugged in a Brother printer to Cent. Set it up so you could print from anywhere-ideally I want it as a printer on the GUI on Pine, and on other computers at home."
*   Later: "Just tell me the instructions how to set it up on my wife's computer ... send a link to Oksana's Gmail from Anna for Max" (so that the SSH enabler can be run, then Claude finishes the printer setup remotely).
*   Final: "Update Global 2 with instructions on how to print on the Centauri printer, brother."

## DECISIONS MADE + WHY
1.  **Printer kept on Cent (USB) and shared over SMB** - Cent is the always?on box, printer was already installed there as a local USB device. Sharing it as `\\192.168.1.176\Brother-Cent` makes it available to any Windows PC on the home LAN without cloud dependency.
2.  **Printer renamed to "Brother-Cent"** to avoid confusions with an old dead local twin on Pine (that old entry was removed).
3.  **IP pinned via DHCP reservation on the router** - The router (OpenWRT at 192.168.1.1) now permanently assigns `192.168.1.176` to Cent's MAC `E4-54-E8-57-EE-E7`. Without this the IP could change and break the printer path.
    *   *Why not hostname?* `Centauri` and `Centauri.local` didn't resolve from Pine (mDNS not active), so the only reliable path was the IP-hence the reservation.
4.  **No password?free guest printer sharing** - Dropped. Modern Win11 refuses anonymous network printer connections anyway, so it wouldn't save Oksana a step, and it required messing with Group Policy on Cent. Instead, the standard one?time credential entry (maxre / L2w3e4r5t=) with "Remember" is simpler and safer.
5.  **For Oksana's PC: send an SSH?enabler via email instead of walking Max through GUI steps** - Max preferred to run a one?click installer that turns on SSH and drops the `sol_key` so Claude can finish everything remotely. The email was sent to `opolesskaya@gmail.com` from Anna, addressed to Max, with the raw link to the enabler batch file.
6.  **Document the whole setup in `global2.md`** - Added a "HOME PRINTER - BROTHER ON CENTAURI" section so future sessions can recall the printer name, path, credentials, and how to add it to new PCs.

## CURRENT STATE
*   **Brother HL-L2300D** is connected via USB to **Centauri** (Windows, 192.168.1.176). Cent must be powered on to print.
*   **Printer shared**: Share name `Brother-Cent`, path `\\192.168.1.176\Brother-Cent`.
*   **Pine (Max's Win11)**: Printer added, test page printed successfully. Only the correct one exists now (dead local twin removed).
*   **Sirius & Vega**: Not added yet. Max said they will be done later when those machines are on.
*   **Router**: DHCP reservation for Cent is committed and live.
*   **Oksana's PC**: The SSH enabler email was sent to her Gmail account (`opolesskaya@gmail.com`). Max has not yet run it as of the last transcript. We are **waiting** for the `REMOTE_READY.txt` line (Computer / User / IP) after he runs it.
*   **global2.md**: Updated with the printer section.

## EXACT NEXT STEP
Wait for Max to run the SSH enabler on Oksana's PC and send the one?line output from `REMOTE_READY.txt`.  
Once received:
1.  SSH into that PC using `sol_key`.
2.  Run `Add-Printer -ConnectionName "\\192.168.1.176\Brother-Cent"` (the credentials are cached with `cmdkey` if needed).
3.  Verify the printer appears in the list and, optionally, send a test page.
4.  Confirm to Max that it's done.

If Max decides to add it manually instead, the 4?click steps are:
- Settings ? Bluetooth & devices ? Printers & scanners ? Add device ? "The printer that I want isn't listed" ? Select a shared printer by name ? `\\192.168.1.176\Brother-Cent` ? Next. If asked for credentials, use `maxre` / `L2w3e4r5t=` and check Remember.

## OPEN QUESTIONS
*   Still waiting for Oksana's PC to be SSH?enabled. No reply received yet.
*   Sirius/Vega printer setup pending when those machines are next powered on (Max will ask).

## KEY PATHS, IDs & COMMANDS
*   **Printer**: Brother HL?L2300D series, driver already installed on Cent.
*   **Share path**: `\\192.168.1.176\Brother-Cent`
*   **Cent credentials for printer share**: `maxre` / `L2w3e4r5t=` (from Nextcloud zSyncMain/ssh/shared_logins_frequent.txt)
*   **Cent static IP**: 192.168.1.176 (MAC `E4-54-E8-57-EE-E7`, reserved on OpenWRT at 192.168.1.1)
*   **SSH key**: `~/.ssh/sol_key` (public at `~/.ssh/sol_key.pub`). Used for all remote access.
*   **SSH enabler script**: `C:\claude_base\tools\remote_access_setup\enable_ssh_for_max.bat`  
    Raw download link (Gist): `https://gist.githubusercontent.com/maxrempel/d9f2075e13895ad83399b3a6d5bc6da3/raw/enable_ssh_for_max.bat`
*   **global2.md**: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (synced across machines). Contains the full printer setup instructions now.
*   **Router access**: OpenWRT at 192.168.1.1, root / `0y32dnkh40rj7hub1y` (LuCI). Session token and ubus calls were used to add the DHCP reservation; the apply endpoint is `https://192.168.1.1/cgi-bin/luci/admin/network/dhcp/apply/`.
*   **Email sending**: tool `C:\claude_base\tools\mxmail\mxmail_v01.py`. The mail was sent "from Anna" to the target address, with Max BCC'd.

## GOTCHAS / DEAD ENDS RULED OUT
*   **Name resolution doesn't work for Cent**. Do **not** try `\\Centauri\Brother-Cent` from other PCs-it won't resolve. Use the IP.
*   **Do not try to make the printer password?free** - it won't work on modern Win11 without extra group policy changes on each client, and the effort isn't justified.
*   **The old dead "Brother HL?L2300D series" local printer on Pine** (USB001, no device) was removed. There should be no confusion now.
*   **Router commit failure**: When adding the DHCP reservation via ubus, direct commit gave an ACL error. The correct way was to use the LuCI `apply` endpoint with the session cookie. That worked and the reservation is live.
