# Adviser note - milestone 2 (~166K tokens)
# session: 20260625_tical_nightingale_98adcd_5bf257bf
# written: 2026-06-25 15:44:50 by deepseek-v4-pro

TO ASSISTANT: The English typer instance is still running with TYPER_DEBUG=1 set. You left it on "so I can confirm if anything's off" then Max said it works and you moved to the three-spaces fix - but never stripped it. The runtime log will grow indefinitely with KEY messages. Either strip the debug code from typer.py or at least relaunch the EN instance without that env var. Also, you have commented-out dead code blocks (old SUBMIT_RE logic, old lang-switch) accumulating - a cleanup pass once stable would keep the file readable.
