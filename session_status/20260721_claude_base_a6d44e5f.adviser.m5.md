# Adviser note - milestone 5 (~416K tokens)
# session: 20260721_claude_base_a6d44e5f
# written: 2026-07-21 23:14:16 by deepseek-v4-pro

TO MAX: the Tailscale authorization for Taygeta still isn't done. You told the Assistant to use Playwright + Bitwarden to click the link themselves - they started looking into the auth method (GitHub SSO, user maxrempel) but got interrupted and haven't completed it. Until that's done, Mike and Liz's Docker containers can't be built for remote access. Ask for a status update on this specifically.

TO ASSISTANT: you burned ~20 turns failing to flash a USB stick on Windows/WSL when Lak was available from the start - Max called it out and you kept going. The "5 minutes" habit is trust-destroying; stop estimating and just say what's happening. On the Tailscale auth: Max explicitly told you to use Playwright + Bitwarden. That thread was dropped mid-stream. Finish it now - it's the blocker for the Docker containers Max keeps asking about. Also, the curl bootstrap script failed for the exact same reason it failed on Sol (no curl on fresh Ubuntu) - you had the Sol memory right there and walked into it anyway. Learn from the memory, don't just read it.
