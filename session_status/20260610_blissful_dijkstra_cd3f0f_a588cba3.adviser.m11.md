# Adviser note - milestone 11 (~167K tokens)
# session: 20260610_blissful_dijkstra_cd3f0f_a588cba3
# written: 2026-06-10 17:05:37 by claude-opus-4-8

TO MAX:
Verify your MOMA tabs actually work right now. The Assistant killed the live 8790 server to load its change, the relaunch broke once and threw a Windows popup, then a background restart task also failed (the failure notice is the last thing in the log). It claims 8790 is back up and serving 200, but a second relaunch attempt failed after that claim - so the current state is genuinely ambiguous. If anything is dead, the safe fix is a clean full restart via start_moma.bat.

TO ASSISTANT:
You hit the exact server-relaunch quoting bug TWICE this session and it took the live server down both times. Stop hand-rolling `start /B pythonw` from git-bash. Use start_moma.bat as your own notes say. Right now: confirm the true state of 8790 - the trailing task-notification says your relaunch task FAILED exit 1, which contradicts your "back UP, 200" claim. Re-check with a fresh netstat + curl and tell Max the real status before doing anything else. Also: you took the live 8790 server down to ship a visualization-only feature - that restart should have been the last, carefully-staged step, not a mid-flow gamble. Otherwise the core work (sidecar timings, shading lane, tested on scene 9) looks sound and the rebase/merge was handled cleanly.
