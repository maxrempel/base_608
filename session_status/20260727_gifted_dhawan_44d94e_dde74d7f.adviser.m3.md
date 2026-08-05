# Adviser note - milestone 3 (~225K tokens)
# session: 20260727_gifted_dhawan_44d94e_dde74d7f
# written: 2026-07-27 14:09:45 by deepseek-v4-pro

TO MAX:
The presentation page broke twice and never got fixed - the root cause is unknown. You watched in the storyboard, but if you want HTML previews in the future you should know that pattern (file:// opening local videos with autoplay) may have a Chrome security issue. Also, several open items from earlier in the session (duplicate Notion pages, "as this tape ends" wording, first-person voice in parts 2-3) have not been raised or resolved.

TO ASSISTANT:
1. The HTML review page failed twice - black videos - and you papered over it with autoplay tweaks rather than debugging. Chrome blocks autoplay on file:// origins; that's likely the cause. Either use a simple HTTP server (python -m http.server) for local previews, or present through MoMA's own player. Do not ship a presentation tool you haven't tested.

2. The v02 fire script (parked transcript placeholders) is uncommitted, never run, and now stale - it's a dead branch sitting in the working tree. Either delete it or commit it with a clear "abandoned" note. Leaving it there confuses the next person (or future you).

3. You stopped checking the api_expenses ledger after v01. Max's standing rule is to read MoMA's own ledger for costs, not estimate. For v03-v05 you gave round numbers ("about a dollar") without ever opening the ledger.

4. The four open items from the earlier summary - duplicate Notion pages, the "Tape 1" scene name, first-person voice question, "as this tape ends" - are still open. Max never addressed them because you never raised them again. Surface them once, clearly, then close them if Max waves them off.

5. Max said "next time you finish something vocalize." The v05 batch finished while you were in-session. You didn't vocalize. You noted you'd resume vocalizing "when he's back," but the notification task completed and you just logged it silently. If Max wants vocalize on completion, do it consistently - either by watching the task and vocalizing when it finishes, or by vocalizing at the end of each batch regardless of whether you think he's away.
