# Scribe handover - milestone 2 (~152K tokens)
# session: 20260711_confident_nobel_40d20b_29ec302f
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-11 22:37:19 by deepseek-v4-pro

# Handover: Setting up Codex alongside Claude Code for token-saving cooperation

## Max's Goal (in his own words)
"I want to transfer same instructions and functionality to codex from cl code desktop and run them in cooperation to save on token limits." He wants a "humanized interface" for Codex, like Claude Desktop - not just raw terminal. He hates coding and wants to interact in plain English, same as with Claude Code Desktop.

## Decisions Made & Why
1. **Codex CLI installed first** (OpenAI's terminal tool, v0.144.1). It works, but Max wanted a friendlier window.
2. **VS Code + Codex extension chosen** as the humanized interface: no standalone Codex Desktop exists; the VS Code chat panel is the next best thing. It's an editor sidebar where you type plain English and Codex edits files - similar feel to Claude Desktop's file-handling, just inside a code editor that Max can largely ignore.
3. **Global instructions transferred in principle:** Created a `C:\Users\maxre\.codex\AGENTS.md` file that *references* his real Claude rules (global CLAUDE.md, global2, personal profile, project rules) - but this is a placeholder. The real rules should be *inlined* into that file so Codex loads them at startup. (See Open Questions.)
4. **One MCP tool connected to Codex:** Memex (his local knowledge?base tool). Wired via `~/.codex/config.toml` pointing to `C:\Users\maxre\bin\local-memex.exe`. The other Claude MCP servers (Notion, Gmail, Cloudflare, etc.) have **not** been mirrored yet - that's still on the to?do list.
5. **Windows Update service left disabled/stopped** (already as he wanted). It was not the cause of any install issue; Codex installs via npm, not dependent on Windows Update.

## Current State
- **Codex CLI** working (`codex --version` ? 0.144.1).
- **VS Code** installed and launched, pointed at `C:\claude_base`. Codex extension installed and visible as a panel on the **right side** of the window (the assistant confirmed via screenshots that the CODEX tab was open and looked signed in, but Max couldn't find it at first; the assistant clicked the tab to bring it into focus).
- **Sign?in status:** Possibly already signed in (the panel appeared to be ready), but Max's last message was "I logged into Visual something but I can't find codecs yet." Then he was interrupted. It's possible he's logged into the Codex extension but still can't locate the panel.
- **Rules file** `C:\Users\maxre\.codex\AGENTS.md` exists but is a stub - it tells Codex to go read the Claude files on each session. That won't work reliably; the file should contain the actual merged rules.
- **Codex config** `C:\Users\maxre\.codex\config.toml` contains:
  - Default model: `gpt-4o`
  - Tool `memex` referencing the local Memex executable, auto?approved.
- **No cooperation mechanism set up** yet - both Claude and Codex run on the same folder but do not talk to each other automatically.

## Exact Next Step
When Max returns, first confirm he can open VS Code and activate the Codex chat panel:
- Open VS Code (likely still running or pinned). If not, launch from Start menu or `code C:\claude_base`.
- Look for the **CODEX** tab on the right side of the window (or possibly in the left activity bar - the assistant found it on the right). If it's not visible, click the "ChatGPT/Codex" icon (a circle/spiral) in the left vertical bar. The assistant can screen?share again if needed.
- Verify the panel is signed in: the chat box should be ready to accept input. If not, sign in with ChatGPT account.

Once he's in, immediately tackle:
1. **Populate `AGENTS.md` with his full rules.** Read his existing files:
   - `C:\Users\maxre\.claude\CLAUDE.md`
   - `C:\Users\maxre\.claude\global2.md`
   - `C:\Users\maxre\.claude\personal_profile.md`
   - Any project?level `CLAUDE.md` in `C:\claude_base`
   ...and concatenate the **actionable rules** (short answers, no code dumps, no emoji, memory housekeeping, dictation preferences, version discipline, no touching Windows updates, etc.) into `C:\Users\maxre\.codex\AGENTS.md` as a single document that Codex will load on every session. (The stub strategy will likely fail.)
2. **Mirror all other MCP tools** from Claude's `claude_desktop_config.json` (Notion, Gmail, Cloudflare, etc.) into Codex's `config.toml`. This requires deciding which are safe to auto?approve and adjusting the config accordingly. This is the bulk work to achieve "functionality transfer."
3. **Design a simple cooperation/handoff file** (e.g., `C:\claude_base\COOP.md` or `.handoff.txt`) that both agents can read and write, so Max can instruct Codex to take heavy work while Claude handles judgment without burning tokens. Explain the workflow to Max.

## Open Questions Awaiting Max
- **Confirm he can see and use the Codex panel.** This is the immediate blocker.
- **Does he want Codex to be a full clone of Claude's toolset?** (He said "same instructions and functionality" - I took this to mean all MCP tools too. He hasn't explicitly said yes or no, but it's strongly implied.)
- **How does he envision the "cooperation"?** E.g., "Codex, write the scaffold; Claude, review and refine," or "use Codex to run long regex jobs so I don't burn Claude's limit." He hasn't defined the split yet. The simplest first step is a shared handoff file.
- **Should hooks/skills/auto?memory be ported?** The assistant already noted they don't copy over; does he want manual workarounds (e.g., a shared memory file, or a skill?like instruction block in AGENTS.md)? No answer yet.
- **Will he accept VS Code as the interface, or does he want to explore cursor/Windsurf?** He hasn't reported back on comfort after the panel?finding hiccup.

## Key Paths & IDs
- **Codex global rules:** `C:\Users\maxre\.codex\AGENTS.md` (to be filled with merged rules)
- **Codex config:** `C:\Users\maxre\.codex\config.toml`
- **Claude global rules:** `C:\Users\maxre\.claude\CLAUDE.md`, `~/.claude/global2.md`, `~/.claude/personal_profile.md`
- **Project root:** `C:\claude_base` (his main workspace)
- **Memex executable:** `C:\Users\maxre\bin\local-memex.exe`
- **Claude MCP config:** `C:\Users\maxre\AppData\Roaming\Claude\claude_desktop_config.json` (read?only, source of truth)
- **Codex CLI:** installed globally, version `0.144.1`, executable `codex`
- **VS Code:** installed at `C:\Users\maxre\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd`; extension ID `chatgpt.codex`

## Gotchas & Dead Ends Already Ruled Out
- **Windows Update was not the cause of any install failure** - it was already disabled, and Codex didn't need it.
- **The "rules stub" approach won't work.** Codex does not automatically re?read external instructions from a pointer in AGENTS.md; we must inline the actual rules.
- **Codex's UI may still be unfamiliar.** The panel appeared on the right side in the assistant's screenshot; the left?bar icon is for the Activity Bar's "ChatGPT/Codex" entry. If the panel is hidden, a second click on that icon may show it. Max might need explicit click?by?click guidance.
- **Sign?in state ambiguous.** The panel looked signed in, but Max's statement suggests he may have signed into VS Code itself (via Microsoft account) but not the Codex extension. Watch for an additional "Sign in" button inside the panel.
- **No automatic sync between agents.** They share the filesystem but do not automatically "hand off" - all coordination is manual until we set up a shared file.
- **Hooks, skills, and the memory watcher are Claude?specific** and will require explicit bridge instructions if Max wants them in Codex too (likely not yet).

This handover should allow the next session to resume immediately: guide Max to the panel, then focus on rules population, MCP mirroring, and a handoff file.
