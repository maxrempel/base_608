# Adviser note - milestone 6 (~93K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# written: 2026-06-10 14:01:28 by claude-opus-4-8

TO ASSISTANT:
Max just resolved your export-vs-preview question, but read it carefully - he did NOT say "build the full export pipeline now." He said: this tab is for postprocessing on an ALREADY-exported assembled video; bringing the mixed result back into MOMA is a LATER phase. So the scope right now is: a new tab that loads an existing exported video + its clip-soundtrack, drop a music file, align it, draw a shark-tooth volume curve, scrub and play. Preview/tune only. Do not start wiring ffmpeg re-import or final-render-back yet.

No code yet - confirm that scope in one line, then build the tab. Keep it as a new isolated tab; don't disturb existing sound-server functionality.
