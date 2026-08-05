# Adviser note - milestone 4 (~302K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# written: 2026-06-17 21:26:04 by deepseek-v4-pro

TO ASSISTANT:
Stop iterating. You have a working template (2774), Max approved it. Use it exactly - same tone, same "eyes on each other, minimal nods, film grain" boilerplate, same Left/Right line-labeling format. No more experiments unless Max asks.

Before firing ANY job:
- Trace the still through the spine: clip ? still ID ? confirm it shows both characters in the correct layout for that location (Anna-left/Ishtab-right or window reversed).
- For alcove/doorway, extract a frame directly from the existing approved clip for those lines (the spine gives you the clip_id). Do not guess or reuse hall/window.
- Verify merged audio fits ?15s and all line hashes resolve.

Do not block on polling. Fire, log the job IDs and lipser links, and move on. When you finish the batch, present a single clean summary with links per arrangement.

TO MAX:
The assistant is now re-firing arr02-11 after many wrong attempts. The main risk remaining is that the alcove/doorway two-shots must be pulled from existing clip frames - if that extraction fails, more fires will be wasted. You'll see the results when you return.
