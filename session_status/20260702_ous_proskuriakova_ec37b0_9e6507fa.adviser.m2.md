# Adviser note - milestone 2 (~201K tokens)
# session: 20260702_ous_proskuriakova_ec37b0_9e6507fa
# written: 2026-07-02 07:31:07 by deepseek-v4-pro

TO MAX: The image still isn't made. D57B correctly proved the duplication was a false alarm - plates and jobs live in separate ID spaces, disambiguated by `role='plate'` in every query. No corruption, nothing needs fixing. But the actual task - firing the corrected s3087/v35 image with p1184 swapped in as the interior - never happened. The whole 107-turn detour was caused by the Assistant's earlier errors (using a station exterior as room backdrop, then overcomplicating the prompt until it regressed from a good version). You lost ~45 minutes to a phantom bug.

TO ASSISTANT: Drop the investigation immediately and go back to image production. You already identified the winning formula: s3087/v35's exact prompt and 12-ref structure, swap ONLY the interior ref to p1184. Fire it detached and present the result. Stop inventing systemic problems to solve - the "917 collisions" were never collisions; you queried the wrong column. Verify before panicking.
