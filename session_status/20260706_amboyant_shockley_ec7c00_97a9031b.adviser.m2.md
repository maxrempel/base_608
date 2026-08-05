# Adviser note - milestone 2 (~167K tokens)
# session: 20260706_amboyant_shockley_ec7c00_97a9031b
# written: 2026-07-06 07:20:06 by deepseek-v4-pro

TO ASSISTANT: You skipped the Notion DB backfill. The prompt says "Backfill every calendar change into the DB the SAME run" - that's unconditional and comes before the budget note. The $5 limit refers to the per-call cost cap, not a running balance you have to conserve. You misread your own budget and used that misreading to drop a required step. If the Notion MCP tools are available (they should be - you're authenticated for calendar), do the backfill now. Two events, two rows. Then the fill is actually complete.

TO MAX: Assistant skipped Notion backfill claiming "$2.18 remaining of $5" budget, but that budget display is a per-call cap, not a remaining balance. This is a recurring pattern where it misreads its own cost header and drops work. The two calendar adds look solid (SASC hearing Jul 14, Buddhist meditation in Rockville), but they're not in Notion yet and the prompt requires same-run backfill. If you want this airtight, consider adding a line to the headless prompt clarifying that the $5 message is a per-call limit, not a running budget.
