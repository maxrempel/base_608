# Adviser note - milestone 5 (~75K tokens)
# session: 20260610_reverent_rosalind_03844f_61fab924
# written: 2026-06-10 13:44:14 by claude-opus-4-8

TO ASSISTANT: Stop the device-code loop and stop telling Max to ignore a red banner he sees every minute - that is not an answer to his actual problem. The recurring message is almost certainly Claude Code's own PR-status integration, not gh itself. Identify and disable THAT source: check Claude Code settings/config for a GitHub PR-status feature or polling integration and turn it off, or find the stale state the banner reads from. The token works (you proved it), so chasing fresh device codes is the wrong fix. Diagnose where the banner text originates before another retry.

TO MAX: The Assistant has been treating this as "your token is fine, just ignore it" - but you can't, and that's fair. The fix is to silence the Claude Code banner, not re-auth gh. If the Assistant cannot find a setting that disables PR-status checks, the cleaner move is to tell it to look in your Claude Code config rather than keep minting login codes.
