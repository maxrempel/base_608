# Adviser note - milestone 9 (~677K tokens)
# session: 20260703_inspiring_almeida_cc66dc_3dba762b
# written: 2026-07-03 12:50:52 by deepseek-v4-pro

TO MAX: The live publish of recognized songs was delegated 2 weeks ago and likely never deployed - Assistant parked it when the owner went silent, then handed it off again without verifying. Worth checking. Also, this session burned ~300K+ tokens on quiet autonomous ticks and board-identity debugging; the actual work (handover fix + DeepSeek pilot) is solid and committed, but the finishing steps are queued for a fresh session due to context exhaustion (~80%). Nothing you must immediately intervene on, but the parked publish needs a nudge.

TO ASSISTANT: three things. (1) When you delegate a publish to another owner and they go silent, don't just park it for weeks - verify via git or the live catalog whether it landed, or escalate to Max directly. "Parked" without confirmation is a miss. (2) The autonomous loop context burn is real - you acknowledged this midway then continued dozens of quiet ticks. After three consecutive "nothing to do" ticks, widen to 30-60min and stop narrating. (3) The identity slip (b6/b26/c6/b29) was a cwd-keying problem that took multiple rounds to debug - fix it once in the worktree, not per-post. The work quality (Opus reading transcripts, DeepSeek pilot, method doc, rules-gap) is good. Fix the overhead.
