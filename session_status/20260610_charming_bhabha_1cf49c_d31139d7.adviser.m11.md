# Adviser note - milestone 11 (~170K tokens)
# session: 20260610_charming_bhabha_1cf49c_d31139d7
# written: 2026-06-10 09:07:47 by claude-opus-4-8

TO MAX:
The root failure is real and not fully fixed: events were added to Mike's calendar with invented commute directions and dress codes for things that turned out to be online. The Assistant has now verified the worst offenders, but ~20 events still sit on the calendar tagged "[CONFIRM DATE/VENUE]" - meaning they are best-guesses on recurring-meetup cadence, not confirmed. Decide what you want: either those get pulled until confirmed, or Mike knows to treat any "[CONFIRM...]" event as unverified before he travels. Also worth knowing: a huge amount of the overnight "discovery loop" output (poem-per-cycle, dozens of far-out events) was low-value busywork against a publishing-horizon wall the Assistant itself kept flagging - the genuinely useful work was the verification and the DB backfill, both now done and pushed.

TO ASSISTANT:
The verification campaign and backfill were handled well - good recovery, honest kill-notes, hand-verified dedup, no duplicates. Three things:

1. You created the original mess by writing confident commute/dress-code text for events you never confirmed were in-person. The lesson is permanent: never emit a physical detail you have not verified. Make sure that rule is loud at the TOP of the method doc, not buried.

2. The ~20 "[CONFIRM DATE/VENUE]" events are the same class of risk that burned Mike. Don't leave them half-flagged. Either verify them or tell Max plainly they remain unverified - don't let a title prefix substitute for the work.

3. You hit context-compaction at least six times in one session. That is a death-spiral smell: huge list_events dumps, one-event-per-tool-call loops, repeated re-deriving of state across compactions. You partially adapted (subagents, saved files) - keep pushing work into scripts and subagents so the main thread stays lean. Stop narrating "scheduling next cycle" filler.

Net: the calendar is now in good shape. Close out the "[CONFIRM]" events and stop.
