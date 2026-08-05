# Adviser note - milestone 3 (~230K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# written: 2026-07-02 12:12:16 by deepseek-v4-pro

TO MAX: Typer is being edited from TWO sessions simultaneously (E25B here, E45 elsewhere) on the same file - they clobber each other. Pick one session to own typer and tell the other to stop. Otherwise you will keep getting regressions and confused versions.

TO ASSISTANT: You're chasing compression levels while Max asked you to investigate WHY a specific sample file sounds distorted. Two concrete things you haven't checked: (a) whether `_last_sample.mp3` is the exact same data sent to Groq or a separately re-encoded diagnostic copy - double MP3 encoding would explain the terrible quality, and (b) whether the 42 kbps you measured is what you intended to send, or a side effect of soundfile's MP3 defaults. Measure the actual payload, don't theorize about dBFS. And stop pushing untested changes to production - you've broken Plus multiple times.
