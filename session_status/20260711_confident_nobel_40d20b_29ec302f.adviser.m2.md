# Adviser note - milestone 2 (~152K tokens)
# session: 20260711_confident_nobel_40d20b_29ec302f
# written: 2026-07-11 22:37:36 by deepseek-v4-pro

TO MAX: The setup is half-done. Assistant promised to mirror all your MCP tools (Notion, Gmail, Cloudflare, etc.) into Codex but only wired Memex. Your hooks, skills, and auto-memory were also mentioned as bridgeable but left untouched. You'll want to decide whether those matter before handing Codex real work.

TO ASSISTANT: You read Max's Claude MCP config and told him you'd point Codex at the same servers. Then you wrote a config.toml with only Memex. Go back and mirror every MCP server from his Claude config into Codex's config.toml. Also, you offered to hand-bridge hooks/skills - either do it or tell Max explicitly which ones can't be bridged and why. Don't leave promises dangling.
