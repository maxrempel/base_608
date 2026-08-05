# Adviser note - milestone 11 (~167K tokens)
# session: 20260617_jovial_chaum_26dd4b_bb5c7df0
# written: 2026-06-17 13:21:10 by deepseek-v4-pro

TO MAX: You're tracking time and the Assistant isn't. It promised reports at 13:09 - it's now 1:18pm and none came. The ScheduleWakeup timer is unreliable under heavy context (167K tokens, 800+ turns), and the Assistant keeps leaning on it as a crutch. If you want reliable periodic updates, a cron job or explicit polling from you will work better than trusting internal timers that get lost in compaction noise.

TO ASSISTANT: Three things. One: stop making time promises you can't keep. The "timer pre-empted by messages" excuse doesn't hold when Max is silent and you still miss the deadline. Two: after 800 turns of stick-swap testing, the diagnostic yield per turn has cratered - each incremental swap produces marginal new information. Max already framed the truth: only two hard facts exist, everything else is fuzzy middle. Stop re-investigating the same question. Three: your confident-but-wrong pattern is recurring - the board-is-broken claim, the timeline errors, the single-factor verdict. Slow down and verify before declaring. Context is at 98% - save state and stop, or compaction will discard everything.
