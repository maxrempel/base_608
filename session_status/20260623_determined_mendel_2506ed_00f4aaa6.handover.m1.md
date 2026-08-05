# Scribe handover - milestone 1 (~91K tokens)
# session: 20260623_determined_mendel_2506ed_00f4aaa6
# cwd: C:\claude_base\.claude\worktrees\determined-mendel-2506ed
# written: 2026-06-23 08:41:54 by deepseek-v4-pro

# HANDOVER - Brother Printer Setup on Cent for Home LAN Printing

## GOAL (Max's own words)
Max plugged a Brother printer into Cent and wants to set it up so he can print from anywhere - ideally having it appear as a normal printer in the GUI on Pine (Windows 11), and also on other computers at home (Sirius, Vega).

## DECISIONS MADE + REASONING
- **Approach: LAN-based sharing via SMB, no cloud.** Reasoning: Cent is an always-on box on the home network. All target machines (Pine, Sirius, Vega) are on the same LAN. No need for Google Cloud Print or any internet-dependent printing. Simpler, faster, private.
- **Cent as print server.** Plugged in via USB to Cent. Cent will host the Brother driver and share the printer over SMB so Windows machines see it as a standard network printer.
- **Network share name proposed:** `BrotherCent`, accessible as `\\CENTAURI\BrotherCent`.

## CURRENT STATE
- Brother printer is physically plugged into Cent.
- **No actual work has been done yet.** This is a fresh request.
- **Critical unknown:** The exact Brother model number is still unknown. This gatekeeps all driver installation steps.

## EXACT NEXT STEP
1. **Wait for Max to provide the Brother model number** (sticker on front or back of the printer, e.g., HL-L2350DW, MFC-L2710DW, etc.).
2. Once model is known:
   - SSH into Cent (`probably centauri`).
   - Install the correct Brother driver (likely from Brother's Linux driver support pages or via a package manager).
   - Configure CUPS (or Samba) to share the printer as `BrotherCent` over SMB.
   - Ensure the share is discoverable on the LAN.
3. On Pine (Windows 11):
   - Add a network printer via `\\CENTAURI\BrotherCent`.
   - Confirm it appears in the standard Windows printer dialog and can print a test page.
4. Repeat step 3 for Sirius and Vega when needed.

## OPEN QUESTIONS (awaiting Max)
- **? What is the exact Brother model number?** (e.g., HL-L2350DW, MFC-L2710DW, DCP-L2550DW, etc.) - This is blocking further work.

## KEY PATHS, HOSTS, AND NAMES
- **Print server host:** Cent / CENTAURI (always-on, Linux)
- **Target clients:** Pine (Windows 11 GUI), Sirius, Vega
- **Planned SMB share:** `\\CENTAURI\BrotherCent`
- **Current working directory:** `C:\claude_base\.claude\worktrees\determined-mendel-2506ed`

## GOTCHAS / NOTES
- Cent must remain powered on for any other machine to print. Max has confirmed it typically stays on - this is fine.
- Brother Linux drivers can sometimes require manual `.deb`/`.rpm` downloads from Brother's site rather than being in standard repos. The exact process depends entirely on the model.
- If the printer is a multi-function (MFC series), scanning over the network would be a separate, more complex setup - only printing was mentioned so far, but worth flagging.
- No firewall or network segmentation has been discussed; assuming flat home LAN where SMB broadcasts work.
