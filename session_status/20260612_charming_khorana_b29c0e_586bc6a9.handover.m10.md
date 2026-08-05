# Scribe handover - milestone 10 (~152K tokens)
# session: 20260612_charming_khorana_b29c0e_586bc6a9
# cwd: C:\claude_base\.claude\worktrees\charming-khorana-b29c0e
# written: 2026-06-12 07:30:03 by claude-opus-4-8

# HANDOVER

## GOAL (in Max's words)
Max started with two concrete jobs but pivoted to a capability test. His own words: *"i am not interested in result, i am interested in your ability to control remote computer."* He wants to know **how an agent can actually control a remote Windows machine**, and specifically how the "remote thing" gets set up in the first place when the target has no remote access yet. His underlying frustration: the slow back-and-forth, the assistant being "impotent"/"miserable" at driving RustDesk, and wanting it to just *act* instead of asking questions.

The two original tasks (now backgrounded, but still real):
1. Fix guitar sound in Zoom on his friend **Igor's** Win11 PC. Max insists he already knows the "Original Sound for Musicians" fix inside out - it is NOT that; it's a "super fancy other problem" he hasn't fully described. He wants to run Windows settings/driver-level changes on Igor's machine remotely without manual back-and-forth.
2. Set up a remote shared drive on **Centauri** (his ~14.9TB backup box) so he/friends can reach it. This was being used as the "practice run."

## DECISIONS + WHY
- **SSH is the real control method, not pixel-driving a screen-share.** The assistant controls the Linux fleet (Sol, Lak, Dax) cleanly over SSH and demonstrated it this session. Pixel-pushing RustDesk was declared the worst, last-resort method.
- **For remote Windows control, the chosen path is: bootstrap OpenSSH once, then SSH in forever.** Researched alternatives: SSH-MCP bridges (standard), `agent-rdp` (CLI built for AI agents to drive Windows RDP via the accessibility tree, not pixels), `mcp-vnc`, and Tailscale as the network connector. agent-rdp was flagged as the proper tool for the "control a remote Windows GUI" case but was NOT installed or tried.
- **The irreducible truth established for Max:** you cannot remotely set up remote access on a machine that has none - that first foothold always needs one human touch at the machine, once. After that, everything is remote/clean.
- **Tailscale was proposed** for the Sol?Centauri network gap (and as the long-term "drive from anywhere" answer) but not acted on.

## CURRENT STATE
- Centauri IS up and reachable - Max has it open in RustDesk full-screen on **monitor 2 (LG)**. (Earlier ping-sweep wrongly concluded Centauri was off; corrected - Windows blocks ICMP by default.)
- **Hard wall hit:** computer-use **masks the RustDesk remote-desktop window as solid black** - tried full-screen, windowed, and re-granting the process name; always black. This is by design (agent safety: can't see inside a remote-control window). The assistant therefore refuses to type admin commands blind into it.
- Separately, screenshotting/acting keeps knocking RustDesk's full-screen view down (inferred focus-stealing) and `open_application("RustDesk")` activated the wrong (main) window on monitor 1.
- Sol scanned the whole LAN for SMB/RDP and saw **zero Windows hosts** - so Sol and Centauri currently cannot see each other on the network (different subnet, or Centauri firewall on "Public"). RustDesk works only because it dials outbound.
- Last exchange: Max just laughing ("hahaha") after the assistant conceded the RustDesk route is a dead end by design.

## EXACT NEXT STEP
Nothing is mid-flight requiring a tool call. The ball is with Max. The proposed concrete move on the table: Max pastes the 4 PowerShell commands (below) into Centauri's PowerShell as Admin himself, once. Then SSH into Centauri from this machine and demonstrate real control like Sol. Do NOT re-attempt to screenshot/drive the RustDesk window - that's settled as a dead end.

## OPEN QUESTIONS (awaiting Max)
- Will he run the 4 commands manually on Centauri, or does he want a different approach (e.g., try agent-rdp, set up Tailscale)?
- What is the actual "super fancy" guitar problem on Igor's PC? Never described. Is the guitar via a USB audio interface (Focusrite etc.) or the laptop's built-in mic? Unknown - changes which driver to target.
- Has the RustDesk Telegram message been sent to Igor yet, and is Igor on Windows? (Confirmed Igor's machine is Win11 generally.)

## KEY PATHS / IDS / COMMANDS
- **Sol:** Ubuntu, `192.168.1.113`, user `maxre`, SSH key `~/.ssh/sol_key`. Fully controllable, works well.
- **Lak / RempelServer:** `192.168.1.199`. **AstolfoDebian:** `192.168.1.243`. Router: `192.168.1.1`.
- **Centauri:** Windows 11 Pro. The 14.9TB drive = **D:** ("16tbRaid", NTFS mirror). No SSH currently; Max normally reaches it via RDP/RustDesk. IP not yet confirmed.
- **The 4 OpenSSH-on-Windows commands (run as Admin):** install OpenSSH.Server capability; start the sshd service; set sshd startup to Automatic; add an inbound firewall rule allowing TCP port 22.
- Centauri notes: `C:\Users\maxre\Nextcloud\claude_md_synced\memory_claude_base\project_centauri_setup.md`; `C:\claude_base\centauri_monitoring_handover_tomemex.md`; server export folder under `C:\Users\maxre\Nextcloud\00_clawy_kb\memories\proj_knowledge\SERVERS...\Centauri_Backup_Computer`.
- This machine is "Pine" (Windows, dual-monitor; LG = monitor 2). RustDesk 1.4.7 finished downloading here ~6:40 AM.
- Telegram message for Igor (non-techie): download RustDesk portable from rustdesk.com ? double-click (no install, "Run anyway") ? read back 9-digit ID + password.

## GOTCHAS / DEAD ENDS RULED OUT
- **DEAD END: driving Centauri through the RustDesk window via computer-use.** The remote view renders as black to the agent by design - confirmed across windowed/fullscreen/re-grant. Don't retry.
- ICMP ping-sweep is blind to Windows hosts (they block ping) - don't conclude a Windows box is off from ping alone; TCP-probe 445/3389/139 instead.
- Full-screen RustDesk collapses when it loses focus; agent screenshots steal focus. `open_application("RustDesk")` grabs the wrong window.
- The Zoom fix is NOT "Original Sound for Musicians" - Max knows that cold; don't suggest it again.
- Zoom's own in-app audio toggles aren't scriptable; only Windows driver/device/registry-level changes are scriptable over SSH.
- Early wrong claim that the assistant couldn't drive RustDesk at all was walked back, then re-narrowed to: it CAN drive native windows, but CANNOT see inside a remote-desktop window.

## TONE NOTE
Max is impatient, sweary, and testing capability - he wants action and blunt honesty, not strings of clarifying questions or repeated caveats. Keep it short, act first where possible, admit limits plainly.
