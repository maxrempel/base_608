# Scribe handover - milestone 2 (~166K tokens)
# session: 20260627_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-06-27 09:25:47 by deepseek-v4-pro

# HANDOVER - Typer Session E25

---

## GOAL (Max's words)

"I want typer to type clean text that never swallows the beginning of my dictation. Streaming/garbled-duplicates is rejected. I want two redundant copies - production plus for clean typing, num0 dev for experiments - so I'm never left without dictation when you tinker."

Secondary goals accomplished this session: clipboard-free typing (no Win+V pollution), spoken punctuation, release-to-send with Shift-hold = no-send, self-healing listener, Russian instance, VU meter overlay, typer2 portable package, WhisperWriter uninstalled.

---

## DECISIONS MADE + WHY

### 1. Streaming experiments REVERTED on production
- v1 (overlapping windows) typed seam words twice - unacceptable for messages to real humans.
- v2 (LocalAgreement-2, re-transcribe whole clip every 3s) was clean but cost ~5x more in Whisper API calls. Max: "too wasteful, I just feel bad about increasing the load."
- v3 (overlapping segments, drop last ~12% of each, merge) - cheap (~1.4x) but produced garbled/duplicated/mixed-up text in real use. Max: "it is garbled there is some weird ketchup catch up miss positions and weird mix-ups."
- **Decision:** Production plus + Russian reverted to pre-streaming one-shot typing (transcribe-on-release, no streaming). Reason: clean text is non-negotiable. Streaming experiments continue ONLY on num0 dev.

### 2. Swallowed-beginning bug is a KEYSTROKE DELIVERY DROP, not transcription
- History log showed FULL text was transcribed and dispatched - the first part was never landing on screen.
- Root cause: `SendInput` silently delivers fewer keys than asked when the target window's input queue is cold (right during key-release/focus switch).
- Old code was "fire and forget" - never checked SendInput's return count.
- **Fix (live on production now):** `_send_batch()` verifies the count, re-sends refused events (up to 4 retries with 20ms sleep), and logs any unrecoverable drop. `type_unicode` also uses gentle mode (smaller 40-char batches, 12ms gaps) for the first chunk.
- This fix was already proven on num0 dev; ported to one-shot production path only.

### 3. Clipboard eliminated entirely
- Old method: clipboard copy ? Ctrl+V paste caused Win+V history pollution and Shift+V false trigger (synthetic Ctrl+V collided with held Shift).
- **Fix (proven, live):** Unicode SendInput keystroke injection directly to the cursor. Zero clipboard touch.
- Key technical detail: the Win32 INPUT struct MUST be 40 bytes (padded union with `ctypes.c_ubyte * 32`), not 24. No argtypes on SendInput, pass `ctypes.byref(arr)`.

### 4. "Send it now" / "Roger" replaced by physical key
- "Send it now" leaked as literal text into another session and triggered a real email send - DANGEROUS.
- Solution: release the talk key = send (types + Enter); hold Shift while releasing = type only, no Enter.
- "Send it now" / "submit it now" / "roger" all retired as triggers; they type as plain text now.
- A note was added to global2.md so future sessions know "roger" / "end of message" is just a benign voice end-marker.

### 5. Redundancy pattern (Max's design)
- Two independent files & processes: `typer.py` (production, keys f9/numplus EN + rctrl RU) and `typer_stream_test.py` (dev, key num0 EN).
- Separate log files, separate history files - they never collide.
- Production stays stable; experiments happen on num0 first. Only after Max confirms does a feature migrate to production.

### 6. Keys settled
- English: **F9** or **numpad-plus** (numpad + is the preferred key - easy to hold, no shortcut collisions).
- Russian: **Right Ctrl**.
- No-send modifier: **either Shift** (reliable latch-based detection for both left and right, fixing the Windows shift+numpad fake-key quirk).
- Repeat/last-message: **Ctrl + numpad-plus** (on production), **Ctrl + numpad-0** (on dev).
- F8 was tried and rejected (Dell display/"Project" key steals focus). Left Ctrl/Left Shift were tried and rejected (trigger junk recordings on every shortcut/capital letter). The CE/calculator key was invisible to pynput.

---

## CURRENT STATE

**Production (plus) - LIVE AND WORKING:**
- File: `C:\claude_base\tools\typer\typer.py`
- Two instances running: English (F9 / numpad +, blue E tray icon) and Russian (Right Ctrl, red R tray icon).
- Behavior: hold key ? mic records ? release ? transcribe entire clip ONCE ? deliver via Unicode SendInput with verify+retry + gentle first chunk ? press Enter (unless Shift held at release).
- Has: spoken punctuation (comma ? `,`, period ? `.`, question mark ? `?`, etc. in EN and RU), VU meter overlay (logarithmic dB scale), self-healing keyboard listener (5s watchdog), durable runtime log, transcript history log, Clipboard-repeat buffer (Ctrl+numpad-plus re-types last - rapid presses walk older messages).
- Commit: `8fe233dc` (just committed with the swallowed-beginning delivery fix), pushed to master.

**Dev (num0) - EXPERIMENTING, UNTOUCHED THIS RESTART:**
- File: `C:\claude_base\tools\typer\typer_stream_test.py`
- Key: numpad 0 (English only).
- Has: v3 streaming + keystroke delivery fix (proven on this file).
- Used for experiments; Max uses it when production needs work.
- Own log: `typer_streamtest_en.log`, own history: `typer_history_streamtest_en.md`.

**Russian - WORKING:**
- Same `typer.py` binary, `--key rctrl --lang ru`.
- Confirmed dictating Cyrillic cleanly.
- Has spoken punctuation, release-to-send, all delivery fixes.

**Autostart:** Startup shortcut `typer_dictation.lnk` ? `start_typer_all.bat` ? launches both EN + RU on boot. Boot-simulation tested, confirmed working.

**Archived:** Pre-streaming clean version at `C:\claude_base\tools\typer\archive\archive_typer_pre_streaming_20260625_161713.py.bak`. Superseded v3 at `archive/superseded_typer_v3stream_<timestamp>.py.bak`.

**typer2 portable package:** Built at `C:\claude_base\tools\typer2\` - self-contained install, README documenting numpad+ hijacking + shift latch, pointed from global2.md.

**WhisperWriter:** Fully uninstalled (Startup shortcut deleted, 840 MB `C:\tools\whisper-writer` folder deleted). typer uses its OWN local venv (`C:\claude_base\tools\typer\venv`) and OWN `.env` (OpenAI key). No dependency.

---

## EXACT NEXT STEP

**None pending - Max confirmed working.** The swallowed-beginning fix was the last thing deployed. Max needs to test production plus with long dictations and confirm the beginning no longer drops. If it still drops occasionally, the next escalation is a stronger "window-ready wait" before the first SendInput batch (e.g., wait 60ms for focus to settle, try an empty space + backspace as a "wake-up" probe).

If Max reports it's clean, log the completion and wait for his next idea.

**Dev experimentation (deferred):** Max may want to revisit streaming on num0 later. The v3 is still there for refinement.

---

## OPEN QUESTIONS (awaiting Max)

None currently. Max was testing the swallowed-beginning fix on plus at transcript end.

---

## KEY PATHS

| What | Path |
|---|---|
| Production typer.py | `C:\claude_base\tools\typer\typer.py` |
| Dev typer (num0, streaming) | `C:\claude_base\tools\typer\typer_stream_test.py` |
| Meter (VU overlay) | `C:\claude_base\tools\typer\meter.py` |
| English launcher | `C:\claude_base\tools\typer\start_typer.bat` |
| Russian launcher | `C:\claude_base\tools\typer\start_typer_ru.bat` |
| Both launcher (for autostart) | `C:\claude_base\tools\typer\start_typer_all.bat` |
| Autostart shortcut | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\typer_dictation.lnk` |
| typer's own venv | `C:\claude_base\tools\typer\venv\` |
| typer's own .env (OpenAI key) | `C:\claude_base\tools\typer\.env` (gitignored) |
| Runtime log (EN) | `C:\claude_base\tools\typer\typer_runtime_en.log` |
| Runtime log (RU) | `C:\claude_base\tools\typer\typer_runtime_ru.log` |
| History log (EN) | `C:\claude_base\tools\typer\typer_history_en.md` |
| History log (RU) | `C:\claude_base\tools\typer\typer_history_ru.md` |
| Dev runtime log | `C:\claude_base\tools\typer\typer_streamtest_en.log` |
| Dev history | `C:\claude_base\tools\typer\typer_history_streamtest_en.md` |
| Pre-streaming backup | `C:\claude_base\tools\typer\archive\archive_typer_pre_streaming_20260625_161713.py.bak` |
| typer2 portable package | `C:\claude_base\tools\typer2\` |
| Desktop lookup table | `C:\Users\maxre\Desktop\typer_commands.md` |
| global2 pointer | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| Git repo | `C:\claude_base` (master branch) |
| Vocalize/attention tool | `python C:/claude_base/tools/attention/attention.py --session "E25 typer" --msg "..."` |

---

## GOTCHAS & DEAD ENDS

1. **CE/Calculator key invisible** - Windows routes it as WM_APPCOMMAND, pynput can never see it. Do not try to bind it.

2. **F8 = Dell Project key** - steals focus, cursor vanishes on hold. Never bind it.

3. **Left Ctrl / Left Shift as talk keys** - triggers junk recordings on every Ctrl+C/Ctrl+V/capital/selection. Modifier keys are fundamentally unusable as push-to-talk. Numpad keys (+, 0) are the right picks.

4. **Numpad keys must be suppressed** - they emit literal characters (+, 0, etc.) that must be swallowed via pynput's `suppress_event()`. This raises an exception internally - do NOT wrap it in try/except or suppression breaks. Press/release bookkeeping for suppressed keys must happen inside `win32_event_filter` because suppression skips `on_press`/`on_release`.

5. **Windows SendInput INPUT struct = 40 bytes** - the union must be padded with `ctypes.c_ubyte * 32` (sized by MOUSEINPUT) or SendInput silently returns 0. No argtypes set; call with `ctypes.byref(arr)`.

6. **SendInput silently drops events** - cold input queue (right after focus/key-release) can refuse the first batch. Must verify return count and retry dropped events. The `_send_batch()` retry loop (up to 4 retries, 20ms sleep) is critical.

7. **Windows Shift + numpad fake-key quirk** - with NumLock on, Windows injects a FAKE Shift-UP at numpad key events, so `GetAsyncKeyState` reads False at the release instant. Latch-based no-send (detect real Shift-down during recording) is the reliable fix - do not rely on reading shift only at release time.

8. **Streaming = garbled text for Max** - v1 duplicated seam words, v3 garbled and mixed up text. Production must stay on one-shot transcribe-on-release until a streaming approach is proven clean on num0 and approved by Max.

9. **pythonw has no console** - all errors go to the runtime log (`typer_runtime_<LANG>.log`), not stdout. The tool has a `log_event()` function for durable logging; always check the log before diagnosing "dead" behavior.

10. **Each typer instance = 2 pythonw processes** (parent launcher + child pystray thread). That's normal. A "duplicate EN" with 4 processes is actually one pair - don't kill both thinking it's two instances.

11. **`.bat` launchers sometimes drop processes** - the reliable launch path is PowerShell `Start-Process -FilePath pythonw -ArgumentList "script.py --args" -WindowStyle Hidden`. The `.bat` files are fine for double-click but flaky when invoked from a non-interactive shell.

12. **Do NOT edit production typer.py while Max is using it** - the redundancy pattern (num0 dev + plus production) exists precisely so experiments stay separate. Only touch production after Max confirms a fix on num0 and explicitly says "push to plus."

13. **WhisperWriter venv is GONE** - typer has its own venv and own `.env` at `C:\claude_base\tools\typer\`. Do not look for whisper-writer.

14. **"Roger" / "end of message" / "send it now" are NOT triggers anymore** - they type as plain text. Release-to-send is the only send mechanism now (Shift-hold = no-send).
