# Adviser note - milestone 5 (~400K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# written: 2026-06-17 23:35:41 by deepseek-v4-pro

TO MAX: The arrangements in MOMA are broken because the Assistant reshuffled lines into 11 beats but never updated the arrangement DB records. The lipsies exist but they're orphans - not linked to any arrangement container, so some arrangements show nothing. The Assistant needs to go into MOMA's arrangements table and either update the existing containers with the new job IDs or create fresh arrangement entries that match the final 11-beat map. Until that propagation is done, you won't see the work in the UI.

TO ASSISTANT: Stop rendering fire. The immediate blocker is that you restructured the scene but didn't update the database linkage between arrangements and lipsie jobs. Go into the arrangements table, map your 11-beat line breakup to arrangement containers, and assign the approved/final job IDs to them. Do not fire any more lipsies until Max can actually see and judge what's already rendered. Also, the session was a death-spiral of prompt tweaks - next time, decide upfront on the arrangement boundaries, lock the stills, and only then iterate on prompts; avoid the piecemeal probe-and-fire loop that bloated context and wasted paid fires.
