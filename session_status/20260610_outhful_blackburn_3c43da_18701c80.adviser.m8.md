# Adviser note - milestone 8 (~127K tokens)
# session: 20260610_outhful_blackburn_3c43da_18701c80
# written: 2026-06-10 08:57:27 by claude-opus-4-8

TO ASSISTANT:
The double-menu was a predictable side effect of the iframe-the-whole-site approach, and Max called it "stupid." Max wants ONE menu, his. The iframe embeds noeticusai.com's full chrome - you cannot hide its menu from the parent frame cleanly (cross-origin). Do not hack CSS into someone else's framed page. Two real options: (a) iframe a menu-less/bare version of the noeticus app if one exists or can be served, or (b) embed only the chat widget, not the whole site. Ask Max which before writing code. Verify on mobile too - the prior full-window embed already trapped him once.

Also: you are deep in this worktree (~127K tokens, compaction near 169K). Watch context. The full-site crawl was thorough but heavy; you don't need to re-crawl everything for this small change.

One process note: you've been committing to master from a worktree repeatedly with self-written commit messages. That's been working, but confirm the branching story stays clean - no stray worktree artifacts (.playwright-mcp screenshots) getting committed.
