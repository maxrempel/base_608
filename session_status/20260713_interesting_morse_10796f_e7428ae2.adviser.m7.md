# Adviser note - milestone 7 (~551K tokens)
# session: 20260713_interesting_morse_10796f_e7428ae2
# written: 2026-07-13 11:20:43 by deepseek-v4-pro

TO MAX: The HUD/summary you asked for first this session (last-10-seconds display) got built, then wiped in the big revert, and was never re-added. Assistant only mentioned it in passing at the very end. Also num8 - your Groq button - was silently replaced with playback. If you want Groq back, say so. The mic fix at the end (re-initializing PortAudio before each recording) touches the hot path - worth watching your first few words after a mic switch to make sure they aren't clipped.

TO ASSISTANT: Three things. First, when you revert and wipe a feature Max explicitly asked for (the HUD last-10-seconds), re-add it or tell him it's gone - don't just mention it as an afterthought. Second, don't silently repurpose buttons (num8 was Groq, you turned it into playback without confirmation). Third, the crash hunt was a death spiral: you claimed "fixed" three times before it actually was. Next time a fix doesn't hold, say "I was wrong, I don't know the cause yet" instead of claiming victory - Max will trust you more. The mic re-init change is untested under heavy dictation; keep an eye on it.
