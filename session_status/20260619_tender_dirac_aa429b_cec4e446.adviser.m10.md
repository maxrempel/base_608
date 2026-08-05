# Adviser note - milestone 10 (~750K tokens)
# session: 20260619_tender_dirac_aa429b_cec4e446
# written: 2026-06-19 18:49:37 by deepseek-v4-pro

TO MAX: The spine is scrambled again, and the root cause is a design gap in how D21 produced reels - it bypassed the merge API so line-membership data never got recorded. This caused the "three hours wasted" incident and is why D31's storyboard update knocked reels out. D21 shipped a fix to `fire_merge_lipsie` but the existing 75+ reels need D30's repair to run before your spine heals. Verify D30 has actually applied that repair - the session shows it was pending.

TO ASSISTANT: Four hard lessons from this session: (1) Never fire on an observation - wait for an explicit command. You burned money on 2821 and the pattern recurred. (2) Use the merge API (`fire_merge_lipsie`) not raw `fire_job` - your bypass is why reels didn't auto-land and Max lost hours. (3) Stop offering plans when Max is in action mode - he told you "do it" repeatedly while you asked "should I?" (4) The session is at 453 turns and 750K tokens - you're in context-bloat territory. Stop proposing multi-step plans. Execute one thing at a time, report only necessary status, and do NOT re-explain things Max already knows. When D31's restore is done, aggressively summarize and reduce scope.
