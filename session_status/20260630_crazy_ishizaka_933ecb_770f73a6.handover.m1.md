# Scribe handover - milestone 1 (~125K tokens)
# session: 20260630_crazy_ishizaka_933ecb_770f73a6
# cwd: C:\claude_base\.claude\worktrees\crazy-ishizaka-933ecb
# written: 2026-06-30 14:51:20 by deepseek-v4-pro

# HANDOVER: Typer Clipboard Bug Fix (Session E35/E125)

---

## GOAL (Max's own words)

"When a computer slows down or busy, it skips sentences. It's still the microphone or green bar still jumping fine, but the sentences are lost on the way and then at the end it might type a sentence in the middle of the phrase and the beginning or the end are lost. So look for the bug and fix it. Check in as E35 and just fix it."

Later clarification: Max initially thought he needed **typer2** fixed, but the live running tool turned out to be **typer** (tools/typer/typer.py). He asked for E25 (the original author session) to be consulted, but E25 is retired and unreachable.

---

## DECISIONS + WHY

**1. Root cause identified: clipboard contention in `paste_via_clipboard`**

- The tool captures audio and transcribes it fully (proven by logs showing e.g. `42.8s -> 469 chars`). The loss happens at the **delivery step**.
- Delivery works by: put text on Windows clipboard ? press Ctrl+V ? restore previous clipboard. Two failure modes on a busy machine:
  - **`OpenClipboard` fails silently**: The old code called it ONCE. If another app held the clipboard, it returned `None` but still fired Ctrl+V - pasting whatever stale text was sitting there. Whole sentence lost.
  - **Fixed restore timing (0.30s)**: After Ctrl+V, the code waited a fixed 0.30s then restored the previous clipboard. On slow apps (browsers, Electron, busy CPU), the app hadn't finished reading the paste yet - so it grabbed the old clipboard mid-paste. Result: "middle of the phrase pastes, start/end lost."

**2. Three-part fix applied**

- **Retry loop** (`_open_clipboard_retry`): tries `OpenClipboard` repeatedly for up to 1.2s with 20ms backoff instead of one-shot.
- **Keystroke fallback**: if clipboard can't be seized even after retry, falls back to `type_unicode` (character-by-character keystroke injection via `SendInput`). Slower but never silent - text always arrives.
- **Adaptive settle**: wait scales with `len(text) / 600.0`, floored at 0.30s, capped at 1.2s. Long sentences get more time before clipboard restore.

**3. Mistaken duplicate-process alarm - DISMISSED**

- E35 initially saw 6 pythonw.exe processes and feared duplicate instances causing contention. On investigation, this was a **false alarm**: the venv launcher pattern means each launch produces a stub `pythonw.exe` that spawns the real interpreter as a child. So 3 launches = 6 processes = exactly ONE clean set of 3 real interpreters. No duplicates. The kill-and-relaunch churn was based on this misdiagnosis. The clipboard code fix is the real fix.

**4. Which typer is which**

- `C:\claude_base\tools\typer\typer.py` - the LIVE tool, running now. All 3 active instances (main EN on f9/numpad+, backup EN on num0/numpad-ins, RU on right-ctrl) load from here. Uses raw Win32 clipboard API via ctypes. **FIXED.**
- `C:\claude_base\tools\typer2\typer.py` - the portable copy. Uses pyperclip library, different paste path. **NOT yet inspected or fixed.** Not currently running.

**5. E25 consultation failed**

- Max asked twice to reach E25 (the original session that built typer). E25 is retired - only appears in old joint-board records, no live session forkable or messageable via the consult/bcast tools. E35 worked the bug from code + logs directly.

---

## CURRENT STATE

- **Fix committed** on master: commit `100fdd47`, pushed to origin (0 ahead/behind).
- **3 live instances** running the patched `tools/typer/typer.py` (confirmed via parent/child process inspection).
- All instances use `--paste` flag ? clipboard delivery path (the fixed path).
- **typer2 is untouched** - still has the old single-shot `OpenClipboard` behavior (or equivalent via pyperclip). This is an acknowledged gap but Max has not yet directed action on it.
- **A g4 wake-system test** interrupted mid-session; E125 ACKed it on the bcast board and returned to Max. Irrelevant to the bug work.

---

## EXACT NEXT STEP

Max's pending question: "Try reaching E25 again." E25 is confirmed unreachable (retired session). The next move depends on Max:

- If he still wants a "second brain": spin up a fresh sibling session to independently review the typer fix.
- If he wants typer2 patched: inspect typer2's delivery path and apply the same hardening (retry, fallback, adaptive timing).

**Do not pre-empt - wait for Max's direction.** The typer-one fix is complete and live.

---

## OPEN QUESTIONS (awaiting Max)

1. **Should typer2 be hardened the same way?** (Noted but not yet acted.)
2. **Is the adaptive settle sufficient?** E125 flagged a residual risk: a *really* slow web app could still beat even 1.2s. The "bulletproof" proposal is to leave dictated text on the clipboard and only restore the old clipboard at the START of the next dictation, eliminating the race entirely. Unanswered.
3. **Does Max want the independent sibling review?** Offered but not confirmed.

---

## KEY PATHS, IDs, COMMANDS

- **Live tool path:** `C:\claude_base\tools\typer\typer.py` (48KB, the fixed file)
- **Portable copy:** `C:\claude_base\tools\typer2\typer.py` (25913 bytes, not fixed)
- **Log evidence:** `C:\claude_base\tools\typer\typer_runtime_en.log` (shows full capture/transcription, proving loss is in delivery)
- **Fix commit:** `100fdd47` on master, pushed
- **Start bats:** `start_typer.bat`, `start_typer_zero.bat`, `start_typer_ru.bat` - all use `--paste` ? clipboard path
- **Broadcast tool:** `python C:/claude_base/branch_bulletin/bcast.py`
- **Consult tool:** `python C:/claude_base/tools/consult/consult.py`
- **3 live instance keys:** f9/numpad+ (main EN), num0/numpad-ins (backup EN), right-ctrl (RU)

---

## GOTCHAS

- **Windows clipboard is a single shared resource** - only one process can hold `OpenClipboard` at a time. This is the root of the bug. Clipboard contention is normal on busy machines, not a defect elsewhere.
- **Venv launcher stub pattern** means each `pythonw.exe` launch shows TWO processes (stub + real child) with the same command line. Do not mistake this for duplicate instances. Process count = launches ? 2. Trust parent/child PID analysis, not naive process counting.
- **E25 is permanently unreachable** - not a temporary glitch. Do not attempt again.
- **The fix is syntax-checked and round-trip tested** (set?capture-prev?set-new?restore passes).
- **Silent `OpenClipboard` failure was the original defect** - it returned `None` to `_set_clipboard_text_no_history`, which the old caller didn't check, so Ctrl+V fired blind. The new code returns a tuple `(prev_text_or_None, ok)` so callers can't ignore failure.
