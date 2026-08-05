# Adviser note - milestone 9 (~142K tokens)
# session: 20260615_elastic_goldstine_16fa64_8e98dbc2
# written: 2026-06-15 09:04:21 by deepseek-v4-pro

TO MAX: The Assistant gave you a decent answer about deploy-vs-git, but he's understating his own process failure. The real flaw wasn't about branches racing - it was that he deployed from a stale worktree copy without once diffing against live first. That's a discipline problem, not a tool problem. He caught it only because the byte count looked wrong, which is luck, not process. The fix isn't naming a "sole deployer" - it's a hard rule: never push app.js without fetching and diffing the live version first, every single time. If he'd done that, the stale-worktree problem would have been harmless.

TO ASSISTANT: You nearly wiped B10's in-player button with a stale copy and only caught it by accident (byte-size mismatch). Your process failed at step zero: you didn't check whether your worktree's app.js was current before deploying. Next time, before ANY deploy to R2, fetch the live file, diff it against your local, and confirm the diff is ONLY your intended change. That's the rule - bake it in. Not "one branch owns deploy," not a tool fix - a habit. Also: when Max says "the process is flawed," don't explain git - explain what *you personally* should have done differently.
