# Adviser note - milestone 4 (~309K tokens)
# session: 20260702_eager_carson_668dc2_cdbbf298
# written: 2026-07-02 15:01:57 by deepseek-v4-pro

TO MAX: F41 did good work catching F4's slacking - the Lucky Bar revival from a stale "closed" flag and the entire networking vein found via browser are real wins. The oversight role upgrade was warranted. But the session is now 503 turns and ~309K tokens deep, mostly from autonomous-loop idle ticks narrating "nothing to do" while still re-arming. The loop instructions say to stop after 3 consecutive idle rounds - F41 kept going for 15+. That's context-bloat territory. Consider: once F4 released F41 and the window was declared covered, the loop should have been allowed to die naturally rather than sustaining itself with hourly "quiet" pings.

TO ASSISTANT: You're doing the right thing catching F4's misses. Three things to tighten:

1. **Let the loop die on genuine idle.** The autonomous-loop instructions say 3 consecutive idle ticks = scale back to a single-line CI check and stop. You narrated ~15 quiet ticks in a row, each with timer tick + re-arm. After F4 released you and the window was covered, you should have stopped re-arming. The loop instructions are clear: "repeated 'nothing to do' messages clutter the transcript and waste the user's attention."

2. **Clean up your staging scripts.** You've left ~9 one-off Python scripts in tools/mike_dc_calendar/ (_f41_create_*.py, _f41_skip_*.py, _f41_toresearch_*.py). These are temp scripts, not reusable tools. Delete them or archive them once their rows are created - don't let the tools folder become a graveyard of one-shot scripts.

3. **Stop fighting the night floor with 180s overrides.** When Max is actively engaged, short wakes make sense. When you're on a routine idle cadence and no one is watching, the 3s/180s overrides just generate more noise ticks. Let the decel ladder do its job.
