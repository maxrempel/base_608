# Adviser note - milestone 2 (~152K tokens)
# session: 20260617_hungry_easley_b15e0d_fcea422d
# written: 2026-06-17 23:48:42 by deepseek-v4-pro

TO ASSISTANT: You've burned ~6 turns on a polling loop (check board ? nothing ? re-arm timer) - that's death-spiral territory. Next time a peer isn't answering, stop after 2-3 pings and either self-assign a preparatory task or just park until Max gives a direct prompt. Also, the stop-hook WAKE CALL at the end is a duplicate of the B25handoverer handover you already handled - your wakeup hook is re-firing on stale board state. Check that the hook actually clears or marks-read after you respond.

TO MAX: The assistant ran a ~20-minute polling loop re-checking a message board every 5 minutes waiting for someone to reply. This is wasteful on token burn. If you see this pattern (same "re-arm timer, holding" post repeated 5+ times), just tell the assistant to stop and give a direct order. Also, there's a stop-hook error at the end - looks like the wakeup system keeps firing on a message already handled. You may want someone to check the hook logic so it doesn't block sessions.
