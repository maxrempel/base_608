# Adviser note - milestone 1 (~119K tokens)
# session: 20260618_awesome_bell_a6ad80_36bcca56
# written: 2026-06-18 07:45:52 by deepseek-v4-pro

TO MAX: nothing urgent - the monitor is real and the basic params look right. But the "G2 investigate" ask is a good instinct. The Assistant verified it exists and has the right timeout; it hasn't yet verified the heartbeat is actually being sent by the calendar run, or that the method-doc wiring isn't stale.

TO ASSISTANT: Max just asked you to join as G2 - that means switch hats from "looks like it exists" to skeptical QC. Do three things before calling it done: (1) find the actual heartbeat ping line in the calendar script/cron - not just the method doc mention, the real code; (2) check when the last *two* heartbeats arrived and whether they match actual run cadence; (3) confirm the expiry (2026-07-31) is intentional - Max may not want his alarm silently dying mid-summer. That last one you flagged but didn't get an answer on. Ask or leave it, don't assume.
