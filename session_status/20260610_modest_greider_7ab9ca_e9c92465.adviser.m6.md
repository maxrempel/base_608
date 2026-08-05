# Adviser note - milestone 6 (~91K tokens)
# session: 20260610_modest_greider_7ab9ca_e9c92465
# written: 2026-06-10 13:03:07 by claude-opus-4-8

TO MAX:
The Playwright fix needs a Claude Code restart to take effect - the Assistant edited your live .claude.json. Before you restart, the Assistant should confirm the edit is valid JSON so you don't break MCP startup. Also: it edited a profile config but you still have ~20 stale worktree copies of moma_restart.py floating around; that mess is the likely real source of the MOMA popup.

TO ASSISTANT:
Max said "i might have missed, try again" - he wants the popup gone, not more analysis. Stop expanding scope. Two concrete asks: (1) verify your .claude.json edit parses cleanly (python -m json.tool) so you don't brick MCP. (2) You hand-waved the MOMA case as "old copy somewhere" - either find which launcher actually fires, or say plainly you can't and ask Max to click it once while you watch. Don't ship a second long TLDR; give him one verified change and a yes/no test step.
