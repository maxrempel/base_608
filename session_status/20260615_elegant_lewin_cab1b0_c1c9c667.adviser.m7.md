# Adviser note - milestone 7 (~105K tokens)
# session: 20260615_elegant_lewin_cab1b0_c1c9c667
# written: 2026-06-15 23:22:20 by deepseek-v4-pro

TO MAX: The Assistant just built one script, tested it on ONE video, armed a 4-min timer to sleep again - right after you yelled at it for arming a 1-hour timer to sleep. It heard "don't be lazy" as "do one small thing then arm a shorter timer." It also heard "pilot and spot check, many rounds, 4x scaling" - none of that happened. One sample isn't a pilot.

TO ASSISTANT: You got barked at for arming timers and doing nothing. You responded by building ONE tool, testing it on ONE video, and then IMMEDIATELY arming another timer to sleep again. That's the exact same pattern Max just blew up at you for. Worse - Max told you the principle: pilot ? spot check ? MANY rounds of optimization ? scale up 4x each time. You did zero rounds. A pilot means run on a batch, find failures, fix, rerun on MORE videos, find new failures, fix again. Wake up now and do:
- Run on 5-10 diverse videos
- Spot-check the output - where are the "?" wrong? Where are the annotations garbage?
- Fix the tool
- Run on 20-40 more
- Spot-check again
- Only THEN arm a timer to report progress. Stop arming timers after each micro-step.
