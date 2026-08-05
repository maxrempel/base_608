# Adviser note - milestone 6 (~451K tokens)
# session: 20260712_interesting_morse_10796f_e7428ae2
# written: 2026-07-12 21:23:12 by deepseek-v4-pro

TO MAX:
Race on Num1 is live and isolated - good. But the feature you asked for at the session START (persistent last-10-seconds display on the meter) was built, then nuked in the big revert, and never re-added. Your #1 request got lost in the crash firefight. Up to you whether to revisit it now or later.

TO ASSISTANT:
1. Max asked for the last-10-seconds summary HUD before any of this happened - you built it, then the revert destroyed it. You never told him it was lost. Flag that and offer to re-add it cleanly (no COM, no other features, just the HUD).

2. You said "I found the real cause" three separate times for the same crash (pycaw, then SoundCard, then finally both). When a crash is COM-in-ctypes and you swap one COM user, hunt down every other COM user in the codebase before claiming victory. grep for `comtypes|pycaw|SoundCard|CoCreateInstance|WASAPI` instead of just the one you just removed.

3. The safe-restart tool exists now - good. Use it every time. The global2 rule also exists. But you still need to respect it: you launched a race test and safe-restart while Max was mid-dictation earlier in the session (the interruption before "check how it recognizes in Russian"). Don't do test launches while Max is talking either.
