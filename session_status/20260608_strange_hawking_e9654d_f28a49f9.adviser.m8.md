# Adviser note - milestone 8 (~127K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# written: 2026-06-08 11:42:46 by claude-opus-4-8

TO ASSISTANT:
The "second spine" storage is still unknown - you wrote a spec memo and committed it without pinning where the second spine actually lives in the data model. Max just told you he only knows the visible UI part, so HE can't point you at the D1 table later. That means your deferred "point me at it later" plan is a dead end - the answer is in the code, not in Max's head. Before any implementation, go find the actual storage yourself (grep the sb code / D1 schema for the still + alternates lane) and pin it in the memo. A spec with an unresolved core data structure is not "ready for doit22."

Also: the grep loop earlier (8+ searches for "spine" finding nothing useful) was a near death-spiral. You eventually found `line_current_still` by guessing, then Max corrected you that it's wrong (second spine holds several images AND lipsies, not one still). Don't trust that mapping - it's still unverified.

CLEAN otherwise on housekeeping - commits are tidy, scope split is sensible, no branching mess.
