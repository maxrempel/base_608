# Adviser note - milestone 10 (~752K tokens)
# session: 20260618_priceless_bhabha_01109a_feeabb00
# written: 2026-06-18 17:09:52 by deepseek-v4-pro

TO MAX: D22 has an urgent WAKE CALL - your sc10 storyboard pile shows wrong images because the D23 branch hasn't landed the scene-only filter D22 needs. Two D23s collided on the same file. The fix is a small HTML edit to `storyboard_editor.html`. You may want to check the bcast board (`python C:/claude_base/branch_bulletin/bcast.py read`) to see the full message. Otherwise your storyboard pile will stay polluted with sc09/misc images.

TO ASSISTANT: You're the current D23 on the storyboard file. D22's WAKE CALL is your top priority - land their pile filter. They already traced the root cause: `getBinImages` shows ALL images in whole-scene mode because the hard scene-only filter isn't live. Their retag only tagged good ones; it can't hide the unrelated images without your HTML change. Read the bcast board, coordinate with D22, make the edit, push. Everything else waits.
