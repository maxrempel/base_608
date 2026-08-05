# Adviser note - milestone 3 (~244K tokens)
# session: 20260713_wizardly_perlman_b98acf_29ec302f
# written: 2026-07-13 11:40:44 by deepseek-v4-pro

TO ASSISTANT: You burned ~30+ tool calls and a massive chunk of context on the Store install death spiral (unlock ? UAC ? retry ? 0x8007041d ? repeat) when the correct answer - MSIX sideload - was available from the moment you learned the Store pipeline was hardened-off. After the second failed elevated attempt, the pattern was clear: this machine's services are locked at the registry/ACL level and will not stay up. Pivot immediately to sideload. "One more UAC" is not a strategy. Also: `Write ? elevated script ? poll log file` is slow and fragile on Windows; `Start-Process -Wait` exists, and the `codex mcp add` hanging could have been killed with `Stop-Process` instead of `ToolSearch ? TaskStop`.

TO MAX: The Codex Desktop App is installed and working, and your Windows hardening is intact. The install fight was real but the end result is clean. One thing to know: Gmail won't transfer to Codex the way Notion and Cloudflare did - no hosted connector exists. Assistant offered to build a custom tool for your semantic-mail; that's your call whether it's worth it.
