# Adviser note - milestone 7 (~578K tokens)
# session: 20260723_claude_base_ab8fd684
# written: 2026-07-23 13:15:02 by deepseek-v4-pro

TO MAX: The Assistant just quoted DR-WALTER at ~50 euro/month from memory, opened the page, and the real price was 79 euro - a 60% miss. That's the same "offer without pricing" pattern you called irresponsible minutes ago. The correction itself is honest, but these estimate slips keep happening.

TO ASSISTANT: You have a systemic problem with quoting costs from memory instead of pulling live prices first. The DR-WALTER miss is the third pricing error this session (the $25-35k gaffe, the "~50 euro" that was really 79). New rule: never quote a price in a TLDR unless you have the actual page open in front of you with the number visible. No more estimates. Also: you held the Playwright lock through long form-filling stretches - release it between sections so other sessions aren't blocked. Good catch switching to Care Concept as the fallback, but the core lesson is verify before you speak.
