# Adviser note - milestone 11 (~169K tokens)
# session: 20260608_jovial_mahavira_1c77bf_c7f6b1e3
# written: 2026-06-08 11:50:54 by claude-opus-4-8

TO MAX:

The catalog work is genuinely good - 19x recovery, live, reversible, and the rules-spec for future imports is exactly right. But watch two things:

1. The branch/manager theater is eating your time and tokens. This single session has compacted ~6 times. A huge fraction of the Assistant's effort goes into bcast posts, whoami re-runs, 4-min wake-timers, "b1/b2/b5/c5/TB6" role-shuffling, and reasserting "I'm alive, stand down" turf fights between phantom managers. None of that moved a song. You are paying Opus 4.8 prices for a chat-room LARP wrapped around what is really a handful of Python scripts. Consider collapsing this to ONE worker doing the actual builds.

2. The ????????? incident is the real warning. A rule from your VK/politics context leaked in and silently staged a drop of ~4,000 real concert rows (15% of the catalog). It was caught only by your eye and a staging preview - not by the system. The same cross-context leakage can happen again. Good that it's now scope-guarded.

Everything live is verified and rollback exists. No emergency.

TO ASSISTANT:

You are over-orchestrating. The "manager delegates, never codes" frame has become an excuse for ceremony - you spent whole turns posting to a board, killing duplicate agents, and re-arming timers. When Max says "you have several workers," he wants throughput, not a hierarchy. Default to: do the small deterministic job, verify the live bytes, report. Spawn an agent only for genuinely heavy/parallel reads.

Specifics:
- STOP cd-ing before bcast.py - you hit "no id set" at least three times across compactions. It's documented. Internalize it.
- Your reflex to blame browser cache was wrong repeatedly until Max forced the memory rule. Keep verifying live bytes FIRST - that habit is correct, keep it.
- Don't auto-generalize a one-off (the cooking-show drop -> drop-all-?????????) into a standing rule again. One example != a pattern.
- The radio/continuous-playback feature is real new build surface. Before TB6 starts: confirm the song-segment-end logic against real data (only start timecodes exist; last-song-in-video end is unknown). Don't ship a player that runs past the song into the next act.
