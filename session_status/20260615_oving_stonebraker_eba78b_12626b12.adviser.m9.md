# Adviser note - milestone 9 (~136K tokens)
# session: 20260615_oving_stonebraker_eba78b_12626b12
# written: 2026-06-15 09:00:23 by deepseek-v4-pro

TO MAX:
You're right to be frustrated. This session has the Assistant fixing the same
pattern for the 5th time. The real problem isn't the timezone bug or the dedup
bug - it's that the Assistant fixes symptoms, deploys without testing the
actual failure mode, and never asks WHY the fix doesn't stick. The monitor ran
untested for who-knows-how-long with a dedup mechanism that the Assistant just
patched again - same as the last 4 times. You need a root-cause rule, not
another patch. More below.

TO ASSISTANT:
Stop patching and start asking: WHY does this keep coming back? Three things
you missed that explain the recurrence:

1. You never tested the dedup fix against a real down scenario. The test run
was clean because clawy had ALREADY RECOVERED. You proved the fix works when
nothing is wrong - not when something IS wrong. That's worthless. Simulate a
down check and verify the dedup holds before claiming victory.

2. The timezone mismatch is a CLASS of bug, not a one-off. You found clawy was
on UTC, audited the others and said "clean." But WHO SET IT TO UTC? Was it you
or a previous Claude session? If a Claude set it wrong before, what stops the
next one from doing it again? The monitor's setup process has no timezone
guardrail - add one: the monitor should warn/refuse when a check's timezone
doesn't match the box's timezone, OR the Healthchecks API call that creates
checks should default to the server's timezone. Otherwise you'll be here again
in 3 weeks.

3. You left `hc.json` and `dax_live_fleet_monitor.py` in
`tools/fleet_monitor/` - temp files the repo doesn't track. Clean them up.
Also, the worklog update you ran was a workaround (the KB scripts dir, not the
primary worklog). That's a sign the project's housekeeping paths are fractured.

Stop treating this as "two bugs fixed" and start treating it as "the monitor's
design allows the same mistakes to recur." Ask Max if he wants a single
guardrail commit that blocks the entire class of timezone + dedup drift, then
build and TEST it properly - including a synthetic down-check.
