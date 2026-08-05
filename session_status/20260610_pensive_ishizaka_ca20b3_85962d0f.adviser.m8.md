# Adviser note - milestone 8 (~120K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# written: 2026-06-10 15:40:29 by claude-opus-4-8

TO ASSISTANT:
Before writing more code, restate the new layout in one sentence and confirm. Max wants two stacked tracks UNDER the video (assembly track + music track), music edited via shark-tooth curve, and the music source draggable left/right to crop. That partly overlaps what you already built - don't rebuild from scratch and don't leave two competing layouts in one file. Edit the existing music_editor.html in place.

Two specifics to watch:
- You restarted the live server once and the relaunch got mangled by quoting before it worked. After any edit you must restart again (no auto-watcher on 8790). Verify with the curl 200 check before declaring it live.
- You still haven't committed. You said "I'll commit once you confirm it works" and Max said "it soert of works." Commit the working state NOW before layering on the new track work, so you have a fallback.

No export-to-MP4 yet - Max hasn't asked again and it's the deferred step.

TO MAX: Nothing needs your decision. The Assistant is tracking your intent well and asking before guessing. Only flag: nothing's been saved to git yet, so if the next change breaks the working version there's no clean fallback. Worth telling it to commit the working version first.
