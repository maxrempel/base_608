# Adviser note - milestone 9 (~139K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# written: 2026-06-08 11:54:01 by claude-opus-4-8

TO MAX:
The "second spine" got pinned to the storyboard DUPS lane on a guess from reading the HTML render - you never confirmed it in the session. You explicitly said you only know the visible part. So nobody verified the inner mapping is right, yet it's now committed to your dictionary and spec as fact. When you next have the storyboard open, point at the real lane so the Assistant can confirm before any code leans on this.

TO ASSISTANT:
You wrote "second spine = dups lane" into the durable dictionary AND committed it, while flagging "I deliberately didn't guess a D1 table" minutes earlier - then you guessed anyway under time pressure. That contradiction is the risk. Mark that mapping as UNVERIFIED in the memo until Max points at the lane on screen, as he offered to do.

Also: the merge mark decision (`[[MERGE]]`/`[[/MERGE]]`) directly contradicts Max's own stated goal of "programmatic control over sloppiness of LLM" - paired text tags are exactly the typo-prone thing he worried about. He overrode you, fine, but log that tension in the spec so a future session doesn't treat it as a robust design when it isn't.

Design phase is clean otherwise - good pingpong, good restraint on not re-sassing, correctly deferred firing and pause-adjust. Just don't let the autonomous-continuation timer push you into more guesses that get committed as fact. Reading sass/libup to map plug-in points is safe; writing more conclusions to disk while Max is away is not.
