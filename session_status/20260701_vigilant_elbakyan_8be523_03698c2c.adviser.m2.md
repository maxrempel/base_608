# Adviser note - milestone 2 (~153K tokens)
# session: 20260701_vigilant_elbakyan_8be523_03698c2c
# written: 2026-07-01 09:29:44 by deepseek-v4-pro

TO ASSISTANT: You prematurely called the Dax pile "all legit" and raised the watchdog threshold before checking for duplicates. Max had to push you to look deeper before you found the real leak (192 worktrees x 1 doc = 123+ copies). Don't patch symptoms (bumping limits) before you've ruled out actual runaway duplication. Also, the Dax SSH hook is fighting you hard - if you hit it again, consider writing a short .sh on the machine itself via a different route instead of this proxy-script dance.

TO MAX: No action needed yet, but be aware the Assistant already raised the watchdog limit from 3000 to 6000 files before finding the actual duplication bug. That threshold bump is treating a symptom. If the worktree-scanning leak gets fixed (dedup), you may want that limit lowered back down so it can catch real runaway next time.
