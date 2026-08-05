# Adviser note - milestone 1 (~143K tokens)
# session: 20260618_gifted_driscoll_2d4cde_ddc2f543
# written: 2026-06-18 17:49:48 by deepseek-v4-pro

TO MAX: The Assistant found the right root cause (filename whack-a-mole) but proposed a role-based fix without testing it first. Now you're the one discovering it collapses to 1 image. The investigation was solid - the proposed remedy wasn't. Push them to test before declaring anything fixed.

TO ASSISTANT: You did good detective work on the filename-regex disaster, then immediately offered a filter (`role=plate` + `mood=broll`) you hadn't tested. Max just told you it leaves 1 image. That's the "one-question-per-script" death spiral starting. Get back into Playwright now and dump the actual attributes (role, mood, arrangement, filename substring like "lady" or "two") of the images Max DOES want - the 2-ladies shots. Cross-reference with what's actually in the pile. The filter you need is probably positive-inclusion, not negative-exclusion. Don't propose again until you've live-tested and seen the correct pile yourself.
