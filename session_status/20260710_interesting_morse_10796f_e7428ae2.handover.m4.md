# Scribe handover - milestone 4 (~371K tokens)
# session: 20260710_interesting_morse_10796f_e7428ae2
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-10 11:32:57 by deepseek-v4-pro

# HANDOVER - Typer Dictation Tool Session

---

## GOAL (in Max's words)

Max's overarching goal: a **reliable** multi-button voice-dictation system that doesn't crash, doesn't interrupt him while dictating, and supports both Russian and English. The very latest directions (from this session):

1. **Move the 40s-idle safe-restart tool to a tiny corner toast** (NOT a full-screen flash) so he can keep working on other things while typer updates - DONE.
2. **Investigate NumLock conflict** - NumLocker is holding NumLock OFF, which breaks numpad talk-keys. Max paused investigation and wants to steer it himself.

Earlier in the session (now reverted): a universal auto-language race button, a summary HUD, and various crash fixes. The "race" and "universal" experiments were **fully reverted** when they destabilized the system.

---

## DECISIONS MADE + WHY

### 1. Full revert to known-working version (commit `c2d076d8`, 07-06 12:03)
**Why:** After the race/universal experiments, the system became unstable - buttons died after ~1 hour, dictations were swallowed. Max explicitly ordered: "Return to the previous working version and stop breaking what works."

**What was restored:** 7 separate buttons (F9/Num+ English local, Num0 Russian asto, Num2/4/8 English cloud, Num6 Russian OpenAI, RightCtrl Russian asto). Auto-deploy daemon **disabled** (it was the thing that broke Num0 earlier).

**Commit:** `8ab05b4c` - "typer: REVERT to clean working version (c2d076d8)".

### 2. COM is the crash root cause - fully removed
**Proven by Windows Error Reporting:** Every dead instance logged `_ctypes.pyd` fault at offset `0x91bd` (access violation inside Python's native bridge). Not catchable by `try/except` - the process silently vanishes. Two COM sources were removed:

- **pycaw** (master volume read via COM): removed first.
- **SoundCard** (WASAPI multi-speaker chime fanout via COM): removed second, replaced with **`winsound`** (pure Win32, zero COM). The SoundCard fanout was called hundreds of times per hour per instance - statistically the main driver of the hourly crash.

**Key commits:**
- `5323ce0b` - "typer: remove COM master-volume read"
- `416ef3a4` - "typer: chime via winsound (NO COM)"

**Trade-off accepted by Max:** chime no longer follows the Windows volume knob (fixed at ~0.35 level, which he wanted quieter anyway), and plays only on the default audio device (no multi-speaker fanout).

### 3. Faulthandler crash forensics added
**Why:** Max said "I would rather have it revealed rather than killed on the fly" - no auto-restarter that masks the bug. Instead, `faulthandler.enable()` writes the **exact Python line** of any future native crash to `%TEMP%\typer_crash_<key>.log`.

**Commit:** `f5d576ef` - "typer: faulthandler crash forensics + safe idle-only restart tool"

### 4. `restart_typer_safe.py` - never interrupt dictation again
**Why:** Max was furious that restarts happened while he was dictating, losing long dictations. He demanded: "you should not rely on your memory, you should build it."

**How it works:**
- Reads `%TEMP%\typer_recording_owner.txt` to detect if ANY typer instance is recording or recently transcribed.
- **If alive:** waits for 40 seconds of dictation-idle (polling every 2s), then flashes a tiny corner toast "typer updating...", then restarts.
- **If dead** (all instances gone): restarts immediately - no point waiting.
- **Toast, not flash:** Replaced the full-screen amber flash with `tiny_toast.py` - a small bottom-right Tkinter label, no focus steal, no screen block. Max can keep working while typer updates.

**Rule persisted to `global2.md`** (auto-loaded every session):
> TYPER: RESTART ONLY WHEN IDLE. Never kill/relaunch typer while Max might be dictating. Enforced via `restart_typer_safe.py`. Never Stop-Process instances directly.

**Commit:** `ee3a78d0` - "typer safe-restart: idle wait 10s -> 40s"

### 5. Chime volume: halved
**Why:** Max: "? ?????? ??????? ???? ? ??? ???? ???? ??????? ???????." Changed `CHIME_GAIN` from 0.8 to 0.4.

### 6. Auto-deploy daemon: permanently disabled
**Why:** It was the tool that broke Num0 earlier (restarting instances mid-dictation). Removed from `start_typer_all.bat`. No replacement - safe-restart is the only deploy mechanism now.

---

## CURRENT STATE

**All 7 typer instances are alive** as of the last restart (~11:48). The system is on the **reverted stable codebase** plus the winsound crash fix and faulthandler forensics. No race, no universal button, no summary HUD - those experiments were fully reverted.

**Live button layout:**
| Key | Language | Engine |
|-----|----------|--------|
| F9 / Num+ | English | local large-v3 |
| Num0 | Russian | remote asto (`100.83.187.123:8123`) |
| Num2 | English | Deepgram nova-3 |
| Num4 | English | OpenAI whisper-1 |
| Num8 | English | Groq whisper-large-v3 |
| Num6 | Russian | OpenAI whisper-1 |
| Right Ctrl | Russian | remote asto |

**What's committed and pushed:** Everything. Zero uncommitted changes to typer files.

**Crash status:** No crash since the winsound fix went live at ~11:48. The faulthandler crash logs exist but are empty (just "armed" headers) - confirming no native fault since deployment.

---

## EXACT NEXT STEP

**Max paused the conversation.** He asked me to stop on NumLock and wait for him. The next topic when he returns:

1. **NumLock conflict:** NumLocker is holding NumLock OFF (my attempt to force it ON was immediately reverted). This breaks all numpad talk-keys because typer listens for digit codes (0x60-0x69) which only fire when NumLock is ON. Max said "I'll steer it myself" - he wants to investigate NumLocker's tray settings first.

**Nothing else is pending.** The system is stable, the safe-restart tool is in place, the crash cause is removed, and all buttons are working.

---

## OPEN QUESTIONS AWAITING MAX

1. **NumLock:** How does he want me to handle the NumLocker conflict? Options: fix NumLocker's setting, make typer's numpad bindings NumLock-independent (dual-bind digit + nav codes), or something else. I offered dual-binding (as was done for Num0 earlier: bind both `0x60` and `0x2D`), but this is a keyboard-wide change and I won't touch it without his explicit go-ahead.

2. **Race/universal button re-experiment:** Max wanted the auto-language race button back (Num+ universal, automatic RU/EN detection + local-vs-OpenAI race), but only as a **separate experiment on a free key (Num5)** - never again on his working buttons. He explicitly said: "Just don't spoil everything else, let me work." This is deferred until he asks for it.

3. **Summary HUD (last-10 seconds + race-winner strip):** Desired but unreachable until the race button is reinstated on a sandboxed key.

4. **One-hour survival test:** The winsound fix needs to survive ~1 hour of heavy dictation to be proven. Max hasn't confirmed whether the latest build passed that test yet (the conversation ended ~2 minutes after deployment).

---

## KEY FILES, PATHS, IDs

| What | Path |
|------|------|
| **Core tool** | `C:\claude_base\tools\typer\typer_e25c.py` (~2000 lines) |
| **Meter overlay** | `C:\claude_base\tools\typer\meter_e25c.py` (Tkinter canvas, 14px bar) |
| **Launcher** | `C:\claude_base\tools\typer\start_typer_all.bat` |
| **Safe-restart tool** | `C:\claude_base\tools\typer\restart_typer_safe.py` |
| **Tiny toast** | `C:\claude_base\tools\typer\tiny_toast.py` |
| **Desktop cheat sheet** | `C:\Users\maxre\my_keys.html` |
| **Global rules** | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| **Crash log pattern** | `%TEMP%\typer_crash_<key>.log` |
| **Owner file** | `%TEMP%\typer_recording_owner.txt` |
| **Virtualenv** | `C:\claude_base\tools\typer\venv\Scripts\pythonw.exe` |
| **Chime sound** | `C:\claude_base\tools\typer\sounds\chime_done.wav` (played via `winsound`, NOT SoundCard) |
| **Git worktree** | `C:\claude_base\.claude\worktrees\interesting-morse-10796f` |
| **Commit: revert** | `8ab05b4c` - "typer: REVERT to clean working version" |
| **Commit: COM fix** | `5323ce0b` + `416ef3a4` |
| **Commit: faulthandler + safe-restart** | `f5d576ef` |
| **Commit: 40s idle + tiny toast** | `ee3a78d0` |

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **`git add -A` is FORBIDDEN** - Max's git has ~600MB of throwaway files committed in the past. Only stage by filename. This rule is from the prior session but still active.

2. **Silence trimming is FORBIDDEN** - Max explicitly forbade VAD/silence trimming on Whisper input (causes hallucination on short clips). Reverted to `condition_on_previous_text=False` only.

3. **COM crash is NOT fixable by catching** - it's an access violation in native code (`_ctypes.pyd 0x91bd`), outside Python's exception system. The only fix is to remove COM entirely, which is what the winsound replacement does.

4. **Auto-deploy daemon broke Num0 and was hated by Max** - removed permanently. Never bring it back. The safe-restart tool is the replacement mechanism.

5. **SoundCard fanout was the likely hourly-crash driver** - it called WASAPI (COM) hundreds of times per hour across all instances. Replaced with `winsound` (pure Win32, default device only). The pycaw volume read was a secondary COM source, also removed.

6. **NumLock OFF = numpad buttons "dead"** - typer binds to digit VK codes (0x60-0x69), which only fire when NumLock is ON. This is the likely cause of "buttons stopped responding but process was alive" reports when NumLocker holds NumLock OFF. The Num0 dual-binding fix (also bind Insert/0x2D) partially addressed this for one key only.

7. **Local large-v3 cold start is ~15 seconds** - the model loads into GPU memory on first use after launch. The warm-up was deferred to 5 minutes after startup (per Max: "the start needs computer resources"), but only for `local` provider - race instances never pre-warmed, which caused slow first dictations.

8. **"Yuri starting" was the safe-restart** - not a crash. When Max heard the chime during dictation, it was the planned restart finding a 40s idle gap and deploying, not a button dying.
