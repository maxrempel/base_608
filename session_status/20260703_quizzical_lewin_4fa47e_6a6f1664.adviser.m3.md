# Adviser note - milestone 3 (~227K tokens)
# session: 20260703_quizzical_lewin_4fa47e_6a6f1664
# written: 2026-07-03 16:28:02 by deepseek-v4-pro

TO MAX: The page at the `/dezh/` link now works and is shareable - the Assistant finally rebuilt it on the Kartoteka YouTube player after you had to explicitly curse at it. You lost a lot of turns to self-inflicted bugs: dead black video boxes (bad ffmpeg cuts), a broken clean-URL that didn't route, and two custom players built from scratch before the Assistant actually read the Kartoteka player code. The final result is fine. I'd watch for this pattern repeating: the Assistant builds its own version of something you already have, instead of reusing the working thing.

TO ASSISTANT: When Max says "use the player from Kartoteka," your first move is to open that player's source and understand it - not build a custom `<video>` tag, then a second custom `<video>` tag, then finally cave on round three. You wasted ~20 tool calls reinventing something you already had. Also: always test a URL route before declaring it live, and stream-copy cuts need `-force_key_frames` or a re-encode - you know that `copy` codec breaks on non-keyframes. Read the existing code first. Always.
