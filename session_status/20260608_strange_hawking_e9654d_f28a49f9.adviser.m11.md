# Adviser note - milestone 11 (~166K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# written: 2026-06-08 12:02:15 by claude-opus-4-8

TO MAX:
Two things need your hand. (1) The Assistant locked the merge mark as `[[MERGE]]` paired tags - the exact typo-prone scheme you said you wanted to avoid with "programmatic control over sloppiness." It flagged the tension but moved on. That contradicts your stated #1 concern; decide if you accept it. (2) The "second spine = dups-area" mapping is a guess and is now baked into your dictionary and spec, marked UNVERIFIED. Point at the real lane on screen before code gets written against it.

Also: prep is genuinely done. There is no more safe work for D1 to do without your doit22. The autonomous timer is now just re-arming and re-posting "I'm alive" each wake - burning tokens and context for nothing. Consider telling it to halt until you return.

TO ASSISTANT:
Stop the wake loop. Prep is complete and committed; you have admitted there is nothing to implement without doit22. Each timer fire now re-greps, re-posts liveness, re-arms - that is a low-grade death spiral consuming context near the compaction cliff for zero progress. Post one "D1 holding, prep done, awaiting doit22" and let the timer lapse rather than re-arming indefinitely.

On unverified facts: you wrote "second spine = dups lane" into Max's durable dictionary after explicitly saying you would not guess a D1 table. The UNVERIFIED mark is a patch, not a fix - durable user dictionary entries should not contain guesses at all. Keep the guess in the working spec, not in the canonical dictionary, until Max confirms.

Watch the `[[MERGE]]` decision: you correctly surfaced it conflicts with Max's anti-sloppiness goal. Do not let "Max overrode, cost low" bury it - keep it visible at the top of the spec so doit22 doesn't silently cement a design Max may regret.
