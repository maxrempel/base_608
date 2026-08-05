# Adviser note - milestone 3 (~244K tokens)
# session: 20260703_beautiful_villani_5507cf_6fddc353
# written: 2026-07-03 17:49:28 by deepseek-v4-pro

TO ASSISTANT: The wake_listener mtime-guard (7c60bc45 shipped, a3a2a7d1 reverted same session) was a regression that touched the exact "excellent stuff" Max forbids breaking - it would have killed every idle listener's wake-grid slot on Windows. You caught the revert fast, but the pattern of shipping before fully reasoning about Windows constraints (os.execv spawn-and-exit, not image-replace) is the quality problem. Before any wake_listener edit, verify: does this break wake-at-will for a truly idle session with no hook event? A "yes" means don't ship it without a compensating path. Also you accidentally committed a live board file (bulletin_joint.jsonl) to git - you cleaned it up, but that's a housekeeping error pattern. Tighten.

TO MAX: Two open items from this session. 1) DeepSeek API is out of credit (HTTP 402) - the semantic Pollution-Watcher backstop is dark. The structural fix (matcher, cleanup) works without it, but the AI content-check pass is dead until billing is refilled. 2) The wake-persistence-across-Claude-restart thread (C41: ~24 of 30 tabs dark after restart) was abandoned when you pivoted to the Pollution Watcher. Nobody solved it. Those are your only action items. Everything else shipped and pushed.
