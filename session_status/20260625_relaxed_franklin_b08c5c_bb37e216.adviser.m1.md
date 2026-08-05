# Adviser note - milestone 1 (~134K tokens)
# session: 20260625_relaxed_franklin_b08c5c_bb37e216
# written: 2026-06-25 13:57:54 by deepseek-v4-pro

TO ASSISTANT: You burned ~134K tokens and read the full moma_db.py before even identifying the canonical inputs for that plate. Max explicitly said "start from canonic inputs, not derivatives." Instead of reading source files wholesale, query D1 narrowly: get the arrangement_id for `sc_window_pan_right_v01_B_v01`, then resolve its plates/actors/layout_ids - that's likely 1-2 SQL queries. Don't read source code files unless you have a specific function you need to call and you know its name. The session got interrupted before it spiraled, but the pattern is there - broad sweeps, no narrowing.

TO MAX: Nothing you need to act on - you caught it early. When you re-prompt, consider giving the Assistant the exact arrangement or registry ID if you have it, to skip the DB archaeology.
