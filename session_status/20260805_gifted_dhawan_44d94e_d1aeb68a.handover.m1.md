# Scribe handover - milestone 1 (~96K tokens)
# session: 20260805_gifted_dhawan_44d94e_d1aeb68a
# cwd: C:\claude_base\.claude\worktrees\gifted-dhawan-44d94e
# written: 2026-08-05 09:16:56 by deepseek-v4-pro

# HANDOVER - Codex Session Communication Research

## GOAL (in Max's words)
"Thoroughly search online. How is communication between Codex sessions works? Codex sessions talk to each other very nicely, and every session knows what's going on. And one can easily take over the management of the other sessions. And this is pretty recent. So search online, find out the answers. I use DeepSeek, Smart DeepSeek to save on tokens."

## DECISIONS + WHY
- Searched for official OpenAI Codex CLI documentation, configuration details, and recent release notes about session communication.
- The user mentioned "pretty recent" and "take over the management" of other sessions - this aligns with Agents V2 (parent/child tree) introduced in Codex 0.145.0.
- Covered three real mechanisms, plus a VS Code extension update. No dead ends; all searches productive.

## CURRENT STATE
Research completed. A concise TLDR was delivered covering:
1. **Agents V2** (Codex 0.145.0, off by default) - root agent can spawn named children, use `list_agents`, `send_message`, `followup_task`, `interrupt_agent` tools. Context inheritance via `fork_turns`. Shared filesystem, risk of collisions.
2. **Codex CLI as MCP server** - another agent can invoke it as a sandboxed worker with handoffs.
3. **Durable shared files** (AGENTS.md, handoff docs) - simple, cross-agent, no special tooling needed.
4. **VS Code agent host** (1.129) - gives Codex/Claude/Copilot multi-window session management, sub-task delegation.

Sources gathered:
- https://exsesx.dev/blog/en/codex-agents-v2
- https://codex.danielvaughan.com/2026/05/12/codex-cli-agents-sdk-mcp-server-multi-agent-workflows/
- https://codex.danielvaughan.com/2026/05/19/codex-cli-cross-repository-development-multi-repo-sessions-coordination-patterns/
- https://codex.danielvaughan.com/2026/05/14/codex-cli-inside-vscode-multi-agent-architecture-agent-sessions-unified-development/
- https://github.com/openai/codex/discussions/26148
- https://openai.com/index/introducing-the-codex-app/

## EXACT NEXT STEP
The immediate task (research) is done. No further steps mandated by Max. The only follow-up offered was: "Want me to check whether your Codex config already has V2 on?" - awaiting user choice. If resumed, likely action: check `~/.codex/config.toml` for `multi_agent_v2 = true`.

## OPEN QUESTIONS
- Does Max want to verify their local Codex configuration for V2?
- Any deeper dive into one of the mechanisms (MCP server, V2, VS Code agent host)?

## KEY PATHS / IDS
- Codex config: `~/.codex/config.toml` (key: `multi_agent_v2`)
- Agents V2 canonical paths: `/root/research/api`, etc.
- Tools: `list_agents`, `send_message`, `followup_task`, `interrupt_agent`
- Config: `fork_turns` (history sharing control)

## GOTCHAS
- Agents V2 is off by default (0.145.0); must be manually enabled.
- Shared filesystem means agents can step on each other's files unless you assign separate target files.
- The "recent" feeling Max described is almost certainly Agents V2, not older workarounds.
- Codex sessions are isolated by default; there is no automatic telepathy-shared state must be explicitly designed via one of the above mechanisms.
