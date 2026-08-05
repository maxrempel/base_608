
## [2026-06-12 10:34] ? 7d09ffa5
- DID: Scoped claude_remote_help: tested local RustDesk CLI (C:\Program Files\RustDesk\rustdesk.exe) - flags only poke its GUI, NO script API for frames/input. RustDesk is wrong engine for Claude-control.
- STATE: DESIGN DIALOGUE. Max: no screenshots (too slow/clumsy), wants optimal structured Claude control of remote Windows box, every dangerous step gated by Max approval. Converged on spec Option B: small transparent named helper-agent on Igor's machine exposing Windows UIAutomation named-control tree + PowerShell + file ops, visible consent banner, connects OUT to Max, ephemeral, approval-gated.
- NEXT: Awaiting Max go/no-go to design+build Option B. Do NOT revive tamza_connect SSH backdoor. Key insight: UI Automation accessibility tree = named controls = the anti-screenshot channel.
