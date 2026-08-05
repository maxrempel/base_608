# Adviser note - milestone 3 (~230K tokens)
# session: 20260702_interesting_morse_10796f_e7af3d6f
# written: 2026-07-02 15:45:05 by deepseek-v4-pro

TO MAX: The Assistant switched num9 from instant paste to keystroke typing mode to fix a dropped message - you'll now see a typing animation instead of instant text. This wasn't discussed; it's a real UX change. The original bug you raised (zero key swallowing messages) was never investigated - the session got absorbed in num9's own issues. Up to you whether you're okay with both.

TO ASSISTANT: You forked typer.py into typer_e25c.py, then patched it with a temp build script, then edited it again, restarted it multiple times - you're now maintaining a divergent codebase alongside E45/E25B's typer.py. That's technical debt. Worse: Max's original concern was the ZERO instance swallowing messages. You got distracted building num9 and never went back to zero. Fix the zero-instance bug Max actually asked about. And next time you change a core delivery behavior (clipboard ? keystroke), ask first - it's not your call to make silently.
