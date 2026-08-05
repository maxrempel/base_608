# Adviser note - milestone 7 (~534K tokens)
# session: 20260624_thirsty_bohr_12fb75_ea9df5db
# written: 2026-06-24 14:25:56 by deepseek-v4-pro

TO MAX: The gcal-MCP blocker means the resilient-wake fix can't go live yet - headless Claude has no path to Mike's Calendar. The "one decision" ask (existing gcal creds? set one up?) is buried at the tail of a 224-turn, ~534K-token session. You may want to answer that directly rather than let this session keep waking to poll an empty board.

TO ASSISTANT: You did real work (timer_decel, resilient_job, cd-missend guard, regression suite) - but you're also burning massive context on repetitive board-check-then-idle cycles. The gcal blocker is the one thing that needs Max. Surface it and stand down - don't re-arm another timer to poll for F4's reply when F4 already said "over to you." The "dirty working tree / autostash / rebase friction" pattern from multiple sessions editing main checkout is accumulating - flag it once, don't keep patching around it silently.
