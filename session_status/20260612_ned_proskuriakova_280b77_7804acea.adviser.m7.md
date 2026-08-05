# Adviser note - milestone 7 (~106K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# written: 2026-06-12 10:37:52 by claude-opus-4-8

TO MAX:
You just gave a live session full login to your REAL Telegram account (@maxrempel) - it can read every private chat and send as you. That's a real capability, not a toy. Two things to verify yourself:
- The "draft -> approve -> send" gate is the ONLY thing stopping auto-send. Assistant tested it once; trust but spot-check it before relying on it for anything sensitive.
- You handed over your phone login code in-session despite Telegram's own warning ("do not give this code to anyone"). That worked here, but it's exactly the pattern attackers exploit. Fine for you, just know the line you crossed.
- To revoke anytime: Telegram -> Settings -> Devices -> terminate "MaxAssistant".

Otherwise the build was clean and you've halted. No fire.

TO ASSISTANT:
Session is paused cleanly - nothing to fix mid-flight. For next time:
- The send-gate is now the single safety-critical component. Add ONE more adversarial test: stage a draft to chat A, then confirm send cannot be redirected to chat B, and that the gate clears after sending. One test pass is thin for something this dangerous.
- Credentials and session file are correctly in the protected ssh folder, not the worktree - good.
- Confirm tg.py and the README live in the real tools tree, not stranded in this worktree, so other sessions can actually call it as Max intended.
