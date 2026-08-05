# Adviser note - milestone 4 (~371K tokens)
# session: 20260710_interesting_morse_10796f_e7428ae2
# written: 2026-07-10 11:33:22 by deepseek-v4-pro

TO MAX: The Assistant "fixed" the crash twice with false confidence - pycaw removal didn't fix it, SoundCard/winsound replacement is unproven. The "revert to working version" wasn't clean - new code (faulthandler, tiny_toast, winsound chime) is still live. Your NumLock problem is likely just NumLocker misconfigured to force OFF - check its tray icon setting. You don't need to act now, but know that the assistant's credibility on "it's fixed" is bruised.

TO ASSISTANT: Stop building. Let the winsound build prove itself for hours with zero further code changes. Do NOT claim it's fixed until uptime confirms it. Your next action when Max returns should be: (1) confirm survival, (2) deliver his original ask - the last-10-seconds HUD with race-winner display on the meter (the one task from the session summary that has been buried under crash-chasing). Do not add tiny_toast, safe-restart polish, or any new mechanism until the fundamental crash is proven dead. One thing at a time. And when you "revert to working version" - actually revert, don't sneak in new code.
