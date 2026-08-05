# Scribe handover - milestone 1 (~97K tokens)
# session: 20260623_reverent_volhard_be5d05_f471a92c
# cwd: C:\claude_base\.claude\worktrees\reverent-volhard-be5d05
# written: 2026-06-23 09:12:52 by deepseek-v4-pro

# HANDOVER - Session "Attention Tool" (Screen Flash + TTS Voice)

---

## GOAL (Max's Words)

"Flush a standardized message on both screens. I have two screens, so it should be on both screens visible. Pretty big. And also synthesize TTS, synthesize a voice and announce the name of the session and the number so I can find which session wants my attention. Specifically, it needed me to resolve human capture."

In short: when any Claude Code session needs Max's physical attention (e.g. captcha to solve), it should **visually flash a large message across both monitors** and **speak the session name + number aloud** via Windows TTS. This complements the existing Telegram/email notification system.

---

## DECISIONS + WHY

1. **Python + tkinter for the screen overlay** - Chosen because Python 3.14 is already available on the machine, pythonw allows launching without a console window, and tkinter is bundled with Python on Windows (no extra deps). The overlay uses full-screen borderless windows on each monitor, amber background for high visibility.

2. **Windows built-in SAPI TTS (win32com / pyttsx3)** - Chosen over FishAudio or other cloud TTS because:
   - Zero cost, works offline
   - No API keys or network dependency
   - Immediate response (no latency waiting for synthesis)
   - The voice quality is "good enough" for an alarm/attention-getter

3. **Dual-screen detection via tkinter itself** - The tool queries `winfo_screenwidth()`/`winfo_screenheight()` and iterates all monitors by moving a hidden root window to each screen's geometry. No external dependency on `screeninfo` or similar packages.

4. **Default behavior: stays until dismissed** - The message lingers on screen (with voice repeating up to 3 times at intervals) until Max clicks or presses a key. An optional `--seconds N` flag exists for auto-dismiss testing. This default was chosen because captcha resolution might take variable time, and Max might be away from the desk when it fires.

5. **Tool location: `C:/claude_base/tools/attention/`** - Following the existing pattern of tool directories under `tools/` (like `fleetcomm`).

---

## CURRENT STATE

- **File created:** `C:/claude_base/tools/attention/attention.py` - the full attention tool is written and saved.
- **Test launched:** A 5-second test was triggered with:
  ```
  pythonw C:/claude_base/tools/attention/attention.py --session "attention-test" --number 99 --msg "This is a test of the screen + voice alarm" --seconds 5
  ```
- **Test outcome: UNKNOWN.** The assistant explicitly asked Max whether he saw/heard it: *"Did you SEE the big amber message on both screens AND HEAR the voice say 'Session attention-test number 99'?"* - No response recorded in the transcript.
- **Integration not yet done.** The tool exists standalone but has NOT been wired into the session infrastructure (no hook from the captcha/Human Capture flow into calling this tool).
- **No documentation written yet.**

---

## EXACT NEXT STEP

1. **Get confirmation from Max** that the test worked (saw the amber flash on both screens, heard the voice).
2. If it worked: wire the call into the session attention/captcha pipeline - likely a function that sessions can invoke (like fleetcomm) that calls:
   ```
   pythonw C:/claude_base/tools/attention/attention.py --session "<session_name>" --number <session_number> --msg "Captcha to solve in the browser"
   ```
3. If it did NOT work: debug - most likely issues would be missing `pyttsx3` pip package, SAPI voice not installed/defaulting wrong, or tkinter monitor detection failing on the specific dual-monitor setup. Check `python` vs `pythonw` behavior (pythonw may suppress stderr, making debugging invisible).
4. Document the tool and its usage pattern.

---

## OPEN QUESTIONS (Awaiting Max)

- **Did the 5-second test actually work?** (amber box on both screens + voice announcement)
- **Auto-dismiss or stay-until-dismissed?** Currently defaults to stay-until-dismissed with optional `--seconds` timeout. Max needs to confirm preference for the real captcha use case.
- **Should the voice repeat indefinitely until dismissed**, or is 3 repeats the right cap?

---

## KEY PATHS, FILES, COMMANDS

| What | Path/Command |
|------|-------------|
| Attention tool | `C:/claude_base/tools/attention/attention.py` |
| Base working dir | `C:\claude_base\.claude\worktrees\reverent-volhard-be5d05` |
| Python executable | `python` (console) / `pythonw` (no console), version 3.14 |
| Test command used | `pythonw C:/claude_base/tools/attention/attention.py --session "attention-test" --number 99 --msg "This is a test of the screen + voice alarm" --seconds 5` |
| Intended captcha call | `pythonw C:/claude_base/tools/attention/attention.py --session "b7 grok" --number 7 --msg "Captcha to solve in the browser"` |

---

## GOTCHAS + DEAD ENDS RULED OUT

- **Cloud TTS rejected** - FishAudio and similar were considered but ruled out in favor of Windows built-in SAPI for cost/latency/offline reasons. This decision is recorded and should not be re-litigated unless Max specifically asks.
- **pythonw hides stderr** - If the test failed silently, the problem may be invisible because pythonw swallows console output. Debugging may require running with plain `python` to see tracebacks.
- **pyttsx3 dependency** - The tool likely imports `pyttsx3`. If it's not installed (`pip install pyttsx3`), the TTS portion will fail. Not explicitly confirmed installed in this session.
- **win32com alternative** - The tool may use `win32com.client` for SAPI directly (an alternative to pyttsx3). Either way, `pywin32` needs to be installed if going the win32com route.
- **Dual monitor geometry** - tkinter monitor detection can be flaky if monitors have different DPI scaling or negative coordinates (primary monitor not at 0,0). This works in most setups but is a known fragility point.
- **Session transcript is truncated** - The last turn shows the assistant awaiting feedback. The real session context says this is at ~97K tokens, suggesting more may have happened before compaction, but the transcript provided for this handover only goes up to the test launch + question. If there was further conversation (like test results), it's not captured here.
