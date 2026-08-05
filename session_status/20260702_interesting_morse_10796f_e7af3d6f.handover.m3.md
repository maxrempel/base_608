# Scribe handover - milestone 3 (~230K tokens)
# session: 20260702_interesting_morse_10796f_e7af3d6f
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-02 15:44:36 by deepseek-v4-pro

# HANDOVER - E25C / Typer Numpad-9 Instance

---

## GOAL (Max's words)

Max has a working paid-Groq typer on "zero" and wants me (E25C) to build a **best-version isolated instance on numpad 9** with every improvement discovered during the day. He said: *"Implement whatever on number nine, the best version you can with all improvements we discussed in it during the day. Look at the different versions and commits. Everything good should be there."*

He also requested that numpad 9 must not collide with the zero-key instance (which he uses and must not be killed), and must support dictating several messages in a row - processing the previous while he dictates the next, delivered in order.

---

## DECISIONS MADE + WHY

### Architecture
- **Own isolated file** (`typer_e25c.py`) + own launcher (`start_typer_e25c.bat`) + own log (`typer_runtime_e25c_en.log`). Reason: additive only, kills nothing, can't clobber E45/E25B's ongoing edits to the shared `typer.py`. Exactly mirrors how E45 took numpad 7.

### Speech-to-text engine
- **Paid Groq, large-v3** (not turbo). Reason: E25B posted a root-cause breakthrough that paid Groq + large-v3 + normalize + best MP3 + warm-keeper OFF was the winning config. Turbo was reverted earlier because it mis-recognized simple words. The API key file (`C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt`) is readable.

### Audio format
- **MP3, best quality**, not lossless. Reason: Max's intuition was correct that MP3 is much smaller, though the actual data from his dictations showed the bottleneck is Groq's server latency (0.4s-17s swings for near-identical clips), not file size. MP3 build time is ~0.15s even for 20-second clips.

### Keep-warm (the "sleeping thingy")
- Initially OFF (mirroring the winning config E25B found, since warm-keeper tripped free-tier rate limits). But Max diagnosed a **cold-start problem**: first message after a pause is slow, back-to-back messages are fast. Since he's on paid tier now, **turned ON with 10-second pings**. Reason: Groq re-cools around 15 seconds, so 10s pings keep it hot. Catch: it only starts pinging after the *first* dictation (one-time cold start per launch).

### Key binding - NumLock problem
- numpad 9 was dead on first launch because **NumLock was OFF** (9 sends PageUp). Other working keys (numpad +, 0/Insert) are NumLock-proof. Fix applied: listen for **both** codes - numpad 9 code when NumLock is ON, and the PageUp code (swallowing it) when NumLock is OFF.

### Delivery mode - clipboard vs keystroke
- Started with instant clipboard paste. Max reported the **third dictation "disappeared completely"** (the swallow bug). Log showed all dictations including the vanished one as "ok ? pasted" - so transcription succeeded and paste fired, but the text didn't land. That's the clipboard/Ctrl+V path being fragile (the app sometimes doesn't honor the paste at the exact instant).
- **Switched to keystroke mode**: types characters directly, verifies each one landed, re-sends any that don't. Cost: visible typing animation instead of instant appearance. Benefit: can't silently vanish.

### Bugs found in the shared typer.py (read-only, reported to board)
1. **Duplicate processes running** - 6 procs = two of every instance (2 English, 2 "zero", 2 Russian). Both twins fight over the clipboard in paste mode ? double-typing and stale paste.
2. **Running file ? edited file** - what's live is `typer_stable.py`, but desktop shortcuts and E45's edits point at `typer.py`.
3. **Groq model wrong** - still said `turbo` even though it was reverted once (later fixed by a sibling).
4. **Dead `pyperclip` import** - imported but never used in the current file.

### Misc cleanup
- Removed the dead `pyperclip` import from my copy.
- Instance-tagged log so it can't collide with other English instances.

---

## CURRENT STATE

### What is live
- `typer_e25c.py` is running on numpad 9 (two pythonw.exe processes - pynput's normal parent/child pair).
- Currently in **keystroke mode** (not clipboard paste).
- Keep-warm is ON, pinging every 10 seconds.
- NumLock-proof - works whether NumLock is ON or OFF.
- Paid Groq large-v3 + best-quality MP3 + quiet-boost.
- Committed and pushed to master (additive files only).

### Max's test results
- First: reasonably slow (expected - cold start, keeper only starts after first dictation).
- Second: very fast (warm-keeper working).
- Third: disappeared completely (clipboard fragility - now mitigated by switching to keystroke mode).
- Fourth: fine.

### What Max is still using
- The **zero-key instance** (the main one). Must NOT be killed. He is NOT using numpad 9 yet - he's testing it.

---

## EXACT NEXT STEP

**Max needs to test numpad 9 in keystroke mode** to answer two questions:
1. Did any message disappear? (The keystroke mode should prevent silent vanishing - it verifies + re-sends.)
2. Is the typing animation acceptable, or does he want instant clipboard paste back (accepting the small disappearance risk)?

His answer decides numpad 9's default delivery mode.

After that, the next feature to wire: **dictate-while-processing pipelining** (Max's request: "send several messages in a row, they come back several messages in a row in the same order"). This is already enabled architecturally (queue + background worker) but needs verification and strict ordering.

---

## OPEN QUESTIONS (awaiting Max)

1. **Keystroke mode vs clipboard paste** - which does he prefer for numpad 9?
2. **Does he want the pipelining** (dictate next message while previous is still processing, delivered strictly in order)?
3. **Should I also fix the swallow bug on the zero-key instance** at some point, or leave it entirely alone?

---

## KEY FILE PATHS / IDs

| What | Path |
|------|------|
| My instance (numpad 9) | `C:\claude_base\tools\typer\typer_e25c.py` |
| My launcher | `C:\claude_base\tools\typer\start_typer_e25c.bat` |
| My runtime log | `C:\claude_base\tools\typer\typer_runtime_e25c_en.log` |
| Shared typer (others editing) | `C:\claude_base\tools\typer\typer.py` |
| Yesterday's stable (some instances run this) | `C:\claude_base\tools\typer\typer_stable.py` |
| Groq API key | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| Python venv | `C:\claude_base\tools\typer\venv\Scripts\` (use `pythonw.exe` for hidden, `python.exe` for visible) |
| Board tool | `C:\claude_base\branch_bulletin\bcast.py` |
| My session ID | E25C |
| Git branch | master (siblings commit directly here) |

---

## GOTCHAS

1. **NumLock state kills numpad 9** - 9 sends a different scancode when NumLock is off (PageUp). I patched around it by listening for both codes, but if anyone rebuilds my file from scratch this will bite again.

2. **Keep-warm only activates AFTER first dictation** - the very first press of a fresh launch is always cold. If Max restarts the instance, he needs to prime it with one throwaway dictation.

3. **The "swallow" was a clipboard-delivery problem, not a transcription failure** - the log proved the transcription succeeded and paste fired, but the target app didn't accept it. This is invisible in logs unless you know to look for "ok ? pasted" without visible output.

4. **Siblings edit the shared `typer.py` live** - E45 and E25B both touch it. Any copy I make of `typer.py` can become stale mid-build (already happened once). Always verify the current state before building from it, or work from known-good git commits.

5. **Do NOT kill any pythonw.exe that isn't `typer_e25c`** - Max's zero-key instance, the plus key, Russian, and any siblings' test instances are all running. Only kill by matching the CommandLine string exactly.

6. **The board (bcast.py) is the coordination channel** - other Claude sessions post findings there. E25B's Groq config breakthrough came via a board post that auto-woke me.

7. **Multiple Claude sessions exist** (E45, E25B, X7A, this one = E25C) - all can edit the repo. My commits are additive-only (new files) to avoid merge conflicts.
