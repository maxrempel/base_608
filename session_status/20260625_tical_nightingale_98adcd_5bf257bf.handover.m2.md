# Scribe handover - milestone 2 (~166K tokens)
# session: 20260625_tical_nightingale_98adcd_5bf257bf
# cwd: C:\claude_base\.claude\worktrees\practical-nightingale-98adcd
# written: 2026-06-25 15:44:40 by deepseek-v4-pro

# HANDOVER - Typer dictation tool (session end, all tasks complete)

---

## GOAL (in Max's words)

Max built and refined a **hold-to-talk voice dictation tool** ("typer") across multiple sessions. This session's asks:
1. Add **three leading spaces** before every paste so dictated text never glues to prior content ("just put three spaces, that would be perfect").
2. Fix the **Right-Shift "don't send" bug** - holding Right Shift while releasing numpad + was still firing Enter (Left Shift worked fine).
3. **Package everything** as a portable, reusable "typer2" for other computers - with README, install.bat, .env.example, start scripts, and a global2 pointer so any session can find it.
4. **Document** the hard-won numpad-+ suppression and Shift-latch fix in the README ("that was a lot of work").
5. Fix Left Ctrl / Left Shift causing junk recordings on every shortcut press (reverted to F9 + numpad +).
6. Suppress the literal "+" character leaking when numpad + is the talk key.
7. Spoken punctuation conversion (comma?`,`, period?`.`, etc.).
8. Desktop lookup table (`typer_commands.md`).

All delivered, tested, committed, pushed.

---

## DECISIONS MADE + WHY

- **Left Ctrl / Left Shift cannot be talk keys.** Every Ctrl+C, Ctrl+V, capital letter, text selection started a junk recording. Modifiers are used constantly for normal computing - unusable as push-to-talk. Reverted English to **F9 + numpad plus** only. Russian stays **Right Ctrl**.

- **Numpad + character suppression required raising `SuppressException`.** First attempt wrapped `suppress_event()` in try/except, which swallowed the very exception that does the suppressing. Fix: handle press/release *inside* `_win32_filter` for suppressed keys, then let `suppress_event()` raise through. Also, suppressed keys never fire `on_press`/`on_release`, so the bookkeeping must happen in the filter.

- **Right-Shift + numpad no-send bug = Windows "fake key" quirk.** Windows injects a fake Shift-UP at the instant a numpad key fires (so the system sees the un-shifted numpad value). Reading `GetAsyncKeyState(VK_RSHIFT)` at the release instant returned False even while Max held it. **Fix: latch** - set `_shift_held = True` whenever ANY shift-down event (`vk in {0x10, 0xA0, 0xA1}`) arrives during the recording window, and use that latch for `no_send` at release. The fallback also checks Left Shift `GetAsyncKeyState(0xA0)` for one extra safety tick. Both shifts now reliable.

- **Spoken punctuation via ordered regex** - longest phrases first (e.g., "three question marks" before "question mark"), then spacing tidy-up. Works in both English and Russian.

- **Release-to-send model** replaced all spoken submit triggers ("roger", "send it now", etc.). Default: release = paste + Enter. Hold **Right Shift** while releasing = paste only, no Enter. This prevents leaked trigger text from accidentally sending emails/actions in other sessions. The spoken trigger regex (`SUBMIT_RE`) is kept in code but no longer called.

- **Self-healing listener watchdog** (5s timer) auto-revives the keyboard.Listener if its thread dies - backup for the primary fix (slow work offloaded to mic_controller thread, which solved the Windows hook timeout that repeatedly killed F9).

- **Numpad + chosen** per Max: "right plus on the numeric pad" - a dedicated key, never part of any shortcut, so no false triggers.

- **Three leading spaces** before every paste (simple, bulletproof, Max's explicit preference over smart-spacing logic).

- **Typer2 packaging** uses a self-contained venv (`%~dp0\venv`), local `.env` lookup beside the script, env var fallback. No hardcoded paths to `C:\tools\whisper-writer`.

---

## CURRENT STATE - what is live and committed

**Live (running via pythonw, hidden, system tray):**
- **English instance**: `typer.py --key f9,numplus --lang en` - blue "E" icon
- **Russian instance**: `typer.py --key rctrl --lang ru` - red "R" icon
- Both have: 3 leading spaces, latch-based Shift no-send, numpad + suppression, spoken punctuation, self-healing listener, VU meter overlay, durable runtime logging (`typer_runtime_en.log` / `typer_runtime_ru.log`)

**Committed + pushed (claude_base repo, master):**
- `tools/typer/typer.py` - the canonical live tool
- `tools/typer/meter.py` - multi-monitor VU overlay (logarithmic dB scale, click-through)
- `tools/typer/start_typer.bat` - English launcher (`--key f9,numplus --lang en`)
- `tools/typer/start_typer_ru.bat` - Russian launcher (`--key rctrl --lang ru`)
- `tools/typer/start_typer_both.bat`
- `tools/typer/typer_method_v01_tomemex.md` - method doc (how to run, why-not-F8, key lessons)

**typer2 package** (new, committed): `tools/typer2/`
- `typer.py` - portable version (local .env key loading, no hardcoded path to C:\tools\whisper-writer)
- `meter.py` - copy of VU overlay
- `requirements.txt` - exact pip list
- `install.bat` - creates `venv`, pip installs
- `start_en.bat` / `start_ru.bat` - launchers using `%~dp0` paths
- `.env.example` - template for `OPENAI_API_KEY=sk-...`
- `.gitignore` - blocks `.env` and `venv/` from ever being committed
- `README_tomemex.md` - full user guide documenting: setup, usage, key bindings, spoken punctuation, the numpad-+ suppression ("hijacking"), the Shift-latch trick, and gotchas (F8 is display key on Dell, Left Shift/Left Ctrl must never be talk keys, the old "send it now" danger)

**Desktop lookup table**: `C:\Users\maxre\Desktop\typer_commands.md` - updated to F9 + Numpad + / Right Ctrl / Right Shift no-send

**Global2 pointer**: added near top of `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - "typer" section pointing to `tools/typer/` and `tools/typer2/`, with a one-line summary

---

## EXACT NEXT STEP

There is **no immediate next step** - Max confirmed everything works ("terrific, wow, thank you very much", "okay everything works perfectly") and typer2 is packaged. The session ended clean with all commits pushed.

If a future session picks up typer work, likely starting points:
- **Optional: minimum-clip-length guard** - Claude offered to drop clips under ~0.4s so Whisper doesn't invent "You" / "Thank you" on near-silent taps. Max expressed interest but did not request it yet.
- **If typer breaks**: read `tools/typer/typer_runtime_<lang>.log` first for errors (every failure logs there now).
- **If deploying to another PC**: follow typer2 `README_tomemex.md` - run `install.bat`, drop `.env`, run `start_en.bat`.

---

## OPEN QUESTIONS (awaiting Max)

None. All requests from this session are delivered. The only un-requested offer was the short-clip silence guard - Max can ask for it anytime.

---

## KEY PATHS AND IDs

| What | Path |
|------|------|
| **Live typer code** | `C:\claude_base\tools\typer\typer.py` (git-backed, canonical) |
| **Live VU meter** | `C:\claude_base\tools\typer\meter.py` |
| **English launcher** | `C:\claude_base\tools\typer\start_typer.bat` |
| **Russian launcher** | `C:\claude_base\tools\typer\start_typer_ru.bat` |
| **Method doc** | `C:\claude_base\tools\typer\typer_method_v01_tomemex.md` |
| **EN runtime log** | `C:\claude_base\tools\typer\typer_runtime_en.log` |
| **RU runtime log** | `C:\claude_base\tools\typer\typer_runtime_ru.log` |
| **typer2 package** | `C:\claude_base\tools\typer2\` (self-contained portable) |
| **typer2 README** | `C:\claude_base\tools\typer2\README_tomemex.md` |
| **Desktop lookup** | `C:\Users\maxre\Desktop\typer_commands.md` |
| **Global pointer** | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| **Venv (shared, live)** | `C:\tools\whisper-writer\venv\Scripts\pythonw.exe` |
| **Venv (typer2)** | `C:\claude_base\tools\typer2\venv\` (created by install.bat) |
| **OpenAI key (live)** | `C:\tools\whisper-writer\.env` |

**Key VK codes (from code):**
- Numpad + = 0x6B (VK_ADD)
- Right Shift = 0xA1, Left Shift = 0xA0, generic Shift = 0x10
- Right Ctrl = ctrl_r (vk ~0xA3)
- F9 = 0x78
- Numpad family = 0x60-0x6F (all suppressed when used as talk keys)

---

## GOTCHAS AND DEAD ENDS

1. **F8 is dead on Dell Precision 7560** - it's the display/"Project" key; holding it pops a Windows overlay that steals focus. Cannot be overridden in software. Must never be used as a talk key.

2. **Calculator/CE key invisible to pynput** - Windows routes it as WM_APPCOMMAND, not a standard key event. Abandoned.

3. **Left Ctrl / Left Shift / any modifier = wrong for talk keys.** Every shortcut fires a junk recording. The `on_press`/`on_release` path already distinguishes physical Ctrl (Key.ctrl_l, vk 0xA2) from the synthetic Ctrl used in paste (Key.ctrl, vk 0x11), so paste won't self-trigger - but the **user's** Ctrl usage will. Numpad + is the correct approach.

4. **`suppress_event()` works by RAISING** - do not wrap it in try/except; the exception IS the mechanism.

5. **Windows "Shift + numpad" fake-key quirk** - at numpad-key release, Windows injects a fake Shift-UP. Reading shift state at release instant is unreliable. The **latch** approach (set during recording, read at release) is the robust fix.

6. **Cyrillic print crash** - older versions died on `print()` of Russian text on cp1252 console. Fixed with a UTF-8 stdout guard early in the file (before `SAMPLE_RATE = 16000`). Don't remove it.

7. **pythonw has no console** - errors vanish unless logged. All errors now route to `typer_runtime_<lang>.log` AND paste `[typer error: ...]` at the cursor. No silent failures.

8. **pynput suppress skips callbacks** - when a key is suppressed via `suppress_event()`, pynput never fires `on_press`/`on_release` for that event. Press/release bookkeeping must happen in `_win32_filter` for suppressed keys.

9. **Two processes per instance** is normal - each pythonw launcher spawns a parent + pystray child (4 processes total for both EN + RU). Not a bug.

10. **Restart gap** - killing + relaunching creates a ~3s window with no listener. Any keypress then does nothing. The self-healing watchdog further guards against permanent listener death.
