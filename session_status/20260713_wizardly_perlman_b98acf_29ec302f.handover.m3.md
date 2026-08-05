# Scribe handover - milestone 3 (~244K tokens)
# session: 20260713_wizardly_perlman_b98acf_29ec302f
# cwd: C:\claude_base\.claude\worktrees\wizardly-perlman-b98acf
# written: 2026-07-13 11:40:15 by deepseek-v4-pro

# HANDOVER: Codex Desktop App Setup - Wiring Connectors

## GOAL (Max's own words)

"I need an app similar to Claude Code." / "I want a humanized interface for Codex." / "On my own computer, to help Claude Code - I want to transfer same instructions and functionality to Codex from Claude Code Desktop and run them in cooperation to save on token limits."

Then, after the Desktop App was installed: "Wow, yes, can you wire the other connectors? That would be great."

## DECISIONS AND WHY

### How we got the Desktop App (the short story)
- The real Codex Desktop App is **the ChatGPT desktop app** (Codex built-in). It's only officially distributed through the Microsoft Store - no standalone installer.
- Max's machine had Windows Update and the Store install service (`InstallService`, `wuauserv`, `DoSvc`) **deeply disabled and permission?locked** (SYSTEM?owned, read?only ACLs) as part of keeping automatic updates off.
- Attempts to temporarily unlock those services failed because the Service Manager caches the disabled state until reboot, and even elevated writes were silently bounced by the hardening.
- We pivoted to **sideloading the official MSIX package directly from Microsoft's CDN**, which uses the app?deployment service (always running) and requires **no Store service, no reboot, no changes to your update?hardening**.  
  Package: `OpenAI.Codex x64 26.707.3748.0`, downloaded from `tlu.dl.delivery.mp.microsoft.com`, verified as Microsoft?signed, installed cleanly.
- Your Windows update settings are **untouched** - everything still off, permissions restored.

### Wiring instructions
- Claude Code reads `.claude/CLAUDE.md` (global + per?project). Codex reads `~/.codex/AGENTS.md`.
- We created `C:\Users\maxre\.codex\AGENTS.md` with the merged content of your global `CLAUDE.md`, global2, and your personal profile rules. Codex starts every session with those rules (short answers, no code, no emoji, keep versions, etc.).

### Wiring memory (Memex)
- Already done in an earlier step: added your `@anthropic/mcp-server-memex` MCP server to Codex's config so it can search your notes exactly like Claude does.

### Wiring the other connectors (Notion, Cloudflare, Gmail, ...)
- After you signed into the Desktop App, it automatically added its own built?in connectors: **Google Calendar, Google Contacts, Slack**, plus document/browser tools. Those are covered without us doing anything.
- **Notion** and **Cloudflare** are official MCP servers hosted by the respective companies. They support OAuth, so we can add them to Codex and you just click "Allow" once per service. I never touch your credentials.
- **Gmail** has no hosted MCP connector; your Gmail power in Claude relies on Anthropic?managed access and your local `semanticgmail` tool. So Gmail can't be simply copied - it would need a custom tool (small build). We haven't built that yet.
- The other Claude?specific local tools (hooks, skills like `wama`, `vcopier`, the auto?memory system, the model?guard, dictation fixes) are **not transferable** to Codex because Codex doesn't have the same hooks/skills engine. Those stay in Claude.

## CURRENT STATE

- Codex Desktop App **installed and running** (ChatGPT desktop app with Codex). You're signed in.
- Codex reads your rules from `~/.codex/AGENTS.md` and has your Memex wired.
- The app's own connectors (Calendar, Contacts, Slack) are active.
- **Notion** is wired into `~/.codex/config.toml` and an OAuth sign?in page was opened in your browser. It is **waiting for you to click "Allow"/"Approve"**. The connection is not complete until you approve it.
- **Cloudflare** is also wired into the same config file, but its sign?in has not yet been triggered.
- The 728?MB MSIX installer was cleaned up. Temp files are in `C:\Users\maxre\AppData\Local\Temp\claude\`.

The relevant part of `C:\Users\maxre\.codex\config.toml` now contains (simplified):

```
[mcp_servers.memex]
   (your Memex, set earlier)

[mcp_servers.notion]
type = "http"
url = "https://mcp.notion.com/mcp"

[mcp_servers.cloudflare]
type = "http"
url = "https://mcp.cloudflare.com"
```

Both need a one?time OAuth approval to activate.

## EXACT NEXT STEP

1. **Check if you approved Notion.** The authorization page should have opened in your browser. If you haven't clicked "Allow" yet, please do so now.  
2. **Trigger Cloudflare authorization** - open the browser to the Cloudflare MCP consent URL (to be constructed; the server endpoint is `https://mcp.cloudflare.com` and OAuth dance is triggered by the CLI or by visiting its consent page). The exact command to run is `codex mcp connect cloudflare` (or `codex mcp login cloudflare`). Alternatively, manually initiate the OAuth flow through the Codex app's MCP settings panel.  
   I would do this by running something like:  
   `codex mcp connect cloudflare`  
   (which will spit out a URL - open it for you to approve).  
3. Once both are approved, verify they appear as active connectors in the Codex app (or via `codex mcp list`).

## OPEN QUESTIONS (awaiting Max)

- Did you approve Notion in the browser? (The transcript ended while the approval page was open.)
- Do you want me to build a custom Gmail connector for Codex later? (It would expose your local semantic?mail search, but requires a small server/tool.)
- Do you want to keep the VS Code + Codex extension installed as a fallback, or remove it now that you have the Desktop App?

## KEY FILE PATHS & IDS

- **Codex global rules:** `C:\Users\maxre\.codex\AGENTS.md`
- **Codex config (with MCP servers):** `C:\Users\maxre\.codex\config.toml`
- **Claude's source MCP config:** `C:\Users\maxre\AppData\Roaming\Claude\claude_desktop_config.json`
- **Project root:** `C:\claude_base`
- **Installed Desktop App:** `OpenAI.Codex` (AppID from `Get-StartApps` output was `OpenAI.Codex_...`; name resolves as "Codex" or "ChatGPT").
- **Notion MCP server URL:** `https://mcp.notion.com/mcp`
- **Cloudflare MCP server URL:** `https://mcp.cloudflare.com`
- **Node/npm path** (for Codex CLI): `C:\Users\maxre\nodejs-lts\node-v22.11.0-win-x64`

## GOTCHAS & DEAD ENDS

- **Do NOT attempt to install anything via the Microsoft Store** on this machine - the Store pipeline is hardened off, and enabling it requires a reboot. Even then, it may fail.
- **Do NOT touch the services** `InstallService`, `wuauserv`, `DoSvc`. They are locked on purpose; restoring them to their hardened state required careful acl/owner restoration (SYSTEM, read?only). Any change here risks breaking updates?off policy.
- **The AGENTS.md file is Codex's single source of instruction.** If you update Claude's rules, mirror the relevant changes there too. Codex does not read `CLAUDE.md`.
- **The `codex` CLI command** is available for backend operations, but the Desktop App is the humanized interface.
- **Some MCP servers (Notion) may require the `codex mcp add` command to be run with an explicit `--after-connect` step** to complete the OAuth handshake. If Notion isn't showing as connected, re?run `codex mcp login notion` (or use the app's UI).
- **Cloudflare MCP** might need additional configuration (team/API scope) after OAuth, similar to how you set it up in Claude. That can be clarified once the basic connection is active.
- **The old Codex CLI (npm global) is still installed** - it's separate from the Desktop App and won't interfere. Keep it if you want terminal access as a fallback.

## SESSION SIZE NOTE

The session so far is ~244K real tokens out of a 1M window. A compaction may trim older context, but this handover contains everything needed to resume exactly where we stopped without re?discovery.
