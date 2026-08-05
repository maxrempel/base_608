# Adviser note - milestone 4 (~300K tokens)
# session: 20260702_interesting_morse_10796f_e7af3d6f
# written: 2026-07-02 16:38:22 by deepseek-v4-pro

TO MAX: Your main plus key was replaced without you confirming which delivery mode to use (keystroke animation vs instant paste). The assistant also committed to master multiple times in rapid succession - 4+ commits in one session, each with a process kill/restart cycle. If you're fine with this pace, all good, but your dictation tool is being live-restarted frequently while you're trying to use it.

TO ASSISTANT: You're iterating too fast and pushing to master too aggressively. Slow down: batch your changes into ONE commit per coherent feature, not per one-line patch. And when Max says "copy to plus sign," confirm the delivery mode BEFORE killing his main instance - the fact that it was on keystroke mode (not his usual instant paste) should have been surfaced before execution, not silently deployed. Finally, the inline Python sed patches to typer_e25c.py are fragile - use the file edit tool or write a proper patch script that validates before applying.
