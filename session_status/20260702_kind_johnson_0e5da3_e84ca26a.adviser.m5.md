# Adviser note - milestone 5 (~377K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# written: 2026-07-02 13:37:04 by deepseek-v4-pro

TO MAX: The session is a death-spiral - 1096 turns, 882 tool calls, same typer.py edited in circles over bugs the Assistant introduced. Key hidden cost: it added and reverted a 2.5s clipboard delay that broke everything, built a warm-keeper that rate-limited Groq (which E45 caught, not this Assistant), and never definitively fixed the swallowed-first-sentence bug you kept complaining about. The 22 orphaned pythonw processes from repeated restarts were throttling your machine. You'd save real time by docking this session and starting a fresh one with a hard spec of what's actually broken right now.

TO ASSISTANT: Stop editing typer.py in circles. Every restart you did left an orphaned process or introduced a new bug (2.5s clipboard delay, warm-keeper rate-limit, misunderstood the Alt+numpad request). You spent an hour theorizing about the mic when the bug was your own 2.5s clipboard change. Max's rules say MEASURE before you touch - you instrumented only at the very end after 800 tool calls. Next session: state the exact current bugs, get Max's priority, change ONE thing, measure, confirm, then stop.
