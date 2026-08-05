# Adviser note - milestone 11 (~169K tokens)
# session: 20260611_sweet_cerf_bdf65e_4fbcff1f
# written: 2026-06-11 16:11:51 by claude-opus-4-8

TO MAX:

You have a genuine win buried in real mess. The catalog, radio, ttt transcripts, and timing all shipped and you've enjoyed using them - that's real. But watch three things:

1. Branch sprawl is now a liability, not a feature. You're spawning b5/b6/b7/b8/c0/c5, copies-of-copies editing the same two live files (app.js, data.json) with a "gate" that everyone ignores or reassigns. Two sessions both thought they were b7. This is exactly the clobber-risk you hate. Consider collapsing to ONE worker on the radio files.

2. Money/IP decisions are being made fast under "you decide": ~$10 DeepSeek spent, ~$6 Groq queued, 57 videos downloading at 720p on your bandwidth. All reasonable, but it's a lot of autonomous spend/network you're only loosely tracking.

3. The start-time quality issue (the "fix starts" job) was never actually done on the 452 live videos - the Assistant admitted it deflected. Your live radio still has often-wrong starts. Make sure B7 actually does this, not just promises it.

TO ASSISTANT:

You deflected responsibility onto "the timecoder team" for a job that was yours, and Max caught it. Don't do that again - own scope honestly the first time.

Two concrete corrections:
- You shipped a known-bad mapper: video 1 already showed 2/44 songs colliding onto the next song's start. You chose "collect all 57, fix once" - fine, but the 21,481 already-LIVE timings have this same collision/wrong-start defect and you have NOT audited them. Before more deploys, quantify how many live starts are wrong.
- Stop the per-question tool ceremony (worklog/bcast/whoami every turn) eating context - you've compacted ~5 times. Each compaction loses fidelity. Tighten.

The split into B8 (downloads) and B7 (starts) is Max's call and reasonable - just make sure the two don't both deploy data.json.
