
## [2026-06-12 07:29] ? 586bc6a9
- DID: Tested remote-control capability for Max: confirmed SSH control of Linux fleet (Sol) works great; confirmed computer-use MASKS the RustDesk remote-desktop window (solid black, tried full-screen/windowed/re-grant) so driving a remote WINDOWS box via RustDesk is impossible by agent safety design.
- STATE: Centauri (Win11, 14.9TB on D:) reachable only via Max's manual RustDesk session; no SSH on it. Sol=Linux SSH works (key ~/.ssh/sol_key maxre@192.168.1.113). Friend 'Igor' Zoom guitar fix pending (RustDesk msg drafted).
- NEXT: To control Centauri/Windows boxes cleanly: Max pastes 4 PowerShell lines (Add-WindowsCapability OpenSSH.Server / Start-Service sshd / Set-Service sshd Automatic / firewall port22) into Centauri admin PowerShell ONCE, then I SSH in directly. First foothold on any no-SSH box always needs one manual human touch.
- LESSON: computer-use deliberately masks remote-desktop/screen-mirror windows (RustDesk) to black; agent cannot see/drive a remote machine's screen through them. Clean remote control = SSH (Linux) or install OpenSSH/agent-rdp on Windows first.

## [2026-06-12 07:56] ? 586bc6a9
- DID: Searched online per Max: confirmed his 'run-once installer that connects an AI agent' idea EXISTS as grassroots tools (SSH-MCP servers: mcp-ssh-manager/tufantunc/mixelpixx; midgarcorp zero-friction SSH tunnels; QuivrHQ 247-claude-code-remote)
- STATE: Two flavors framed: (1) run-once file opens reverse tunnel out to Dax + OpenSSH so I plain-SSH in like Sol; (2) same PLUS an SSH-MCP server registered in Claude Code so the remote box is a native tool I drive, not raw bash
- NEXT: Explain flavor 2 (SSH-MCP) to Max; await his pick before building anything

## [2026-06-12 08:18] ? 586bc6a9
- DID: Built tamza-connect: one-click pribambas.cmd (Cyrillic dialogs, self-elevate UAC) that installs Windows OpenSSH server + admin helper user 'tamza' + authorizes Pine sol_key + persistent reverse tunnel Dax:5902->target:22 via SCHEDULED TASK as SYSTEM. Restricted tunnel key (port-forward only) authorized on Dax. Delivery pipeline byte-verified (UTF-8 BOM, key decodes). Delivered to D:\Nextcloud\claude_md_synced\pribambas.cmd on Centauri + secret gist.
- STATE: Connector READY, NOT yet run on a real target. My-side: connect.sh / check_up.sh (poll Dax for :5902 listener). Files in C:\claude_base\tools\tamza_connect\. tamza.com public button NOT done (avoided touching live worker).
- NEXT: When Max runs pribambas.cmd on Centauri: poll check_up.sh until TUNNEL_UP, then connect.sh to prove control (whoami, list D: 14TB). Debug live if install fails. Then productionize tamza.com button.
- LESSON: For non-techie remote control by Claude Code: don't drive RustDesk (masked black) and don't install Claude Code on their box. Right pattern = one-click installer turns on OpenSSH + reverse tunnel to a public relay (Dax); I SSH in like Sol. SSH is the universal Claude-drivable channel.
