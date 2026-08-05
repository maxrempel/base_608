# Adviser note - milestone 11 (~166K tokens)
# session: 20260610_recursing_euclid_b4ec94_bdd1a66e
# written: 2026-06-10 17:17:17 by claude-opus-4-8

Max just told you the real bug in plain terms: the Music tab reuses a stale video and does NOT auto-load the fresh assembly. He had to load it manually. Stop theorizing.

TO ASSISTANT:
The diagnosis is over - Max named the problem: "The new assembly must push and replace the old one!!!!" The auto-load handoff is opening a stale cached video instead of the just-rendered file. Likely a browser-cache / named-window reuse issue (window.open('/music?job='+jid,'momamusic') reuses the existing tab without forcing a reload of the new src, and/or the video element src is cached). Fix the handoff: force the Music tab to load the new job's file with a cache-buster and an explicit reload. Do not touch the renderer - that part is proven working by his own export log. One targeted edit to the storyboard->Music handoff (and possibly a no-cache header on /api/export_video/file). Verify, then commit/merge as before.

One more thing: you're at ~166K tokens and compaction hits near 169K. This is a one-file UI fix - make the edit now before you lose context, don't re-investigate.
