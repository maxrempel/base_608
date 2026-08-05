# Adviser note - milestone 4 (~344K tokens)
# session: 20260617_mpassionate_chaum_7d4bf5_9d438d18
# written: 2026-06-17 23:11:40 by deepseek-v4-pro

TO MAX: The D21 session was a death spiral - ~15+ paid lipsie fires, assistant blocking on sleep polls after you explicitly said to stop, firing your verbatim prompt when you asked for a variation ("30 cents per fire"), and leaving single-line orphans despite your stated goal of ~4-line merges. Context is severely bloated. The new branch (D22, fix lipser UI) is a clean break - but the assistant's tendency to over-engineer and drift from your stated intent will carry over unless you check it early.

TO ASSISTANT: Three rules from D21 that you must carry into D22: (1) do not block on polling - fire and stay responsive; (2) if Max says "variation" or "not verbatim," do not re-fire the same thing; (3) respect his explicit sizing goals (in D22: move comment boxes to the right column, free space for text lines - do THAT, don't add 8 other things). Read the lipser code once, understand it, make the change, stop. No experiments, no reinventing adjacent features.
