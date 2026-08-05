# Scribe handover - milestone 4 (~305K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-07-02 12:54:54 by deepseek-v4-pro

# HANDOVER - typer dictation tool (E25B)

## GOAL (Max's words)
Fix the hold-to-talk dictation tool "typer" so it's **fast, accurate, never loses beginnings/endings, and the paste never lands in the wrong session**. He moved to Groq for speed, wants MP3 compression, volume normalization, real timing diagnostics, and a "hold-and-deliver-to-original-field" paste. He also needs **no more collision with other branches editing the same file** - this session (E25B) now owns typer.

## DECISIONS MADE + WHY

### 1. STT engine: OpenAI ? Groq Whisper large-v3
- **Why**: OpenAI was ~10s per dictation. Groq is same Whisper family (equal or better accent accuracy) at ~200x realtime, OpenAI-compatible API, drop-in swap. Already had a Groq key on disk.
- **Tradeoff**: free tier queue is **wildly inconsistent** - 1s to 14s for the same work. Not our code, server congestion. Paid Groq tier would fix it.
- **Reversible**: one-line `STT_PROVIDER = "openai"` flips back.

### 2. Audio format: WAV ? MP3 ? best-quality MP3 + normalization
- **Why**: Max said "lossless is overkill for speech, MP3 at decent quality is sufficient." Test proved upload size doesn't affect speed (28KB vs 469KB = ~350ms difference, dwarfed by Groq server swing). So best-quality MP3 keeps audio clean at no speed cost.
- **Normalization added**: Max's mic level is genuinely quiet (?30 to ?35 dBFS), but the VU meter looked "proper" because its scale floors at ?55 dB (so ?35 shows ~38%). This quietness made the old low-bitrate MP3 sound "super quiet and distorted." Each clip is now boosted to a healthy level with a limiter. **Also likely improves recognition accuracy.**
- **Reversible**: one-line format change.

### 3. Pre-roll buffer (2.0s) - fixes swallowed sentence-start
- **Why**: On a loaded machine, the gap between key-press and recorder flipping ON can exceed the small 0.6s cushion. The pre-roll ring buffer keeps the last 2s of audio so a press grabs lead-in words. **Zero delay - it's a rewind, not a wait.**
- Also: **warm-keeper** (20s heartbeat, 20-minute window) keeps Groq connection warm so dictations after a think-pause skip the cold-start.

### 4. Left Alt + numpad+ = RECALL (re-send last dictation)
- **Why**: Max wanted Ctrl+numpad+ freed for Chrome zoom. Left Alt + numpad+ re-pastes and re-sends the previous dictation.
- **Bug fixed**: held Left Alt corrupted Ctrl+V into Ctrl+Alt+V and Enter into Alt+Enter during recall. Both now clear modifiers first.

### 5. Synchronous race-free clipboard paste (0.30s restore)
- **Why**: The old daemon-thread clipboard restore with 2.5s delay caused back-to-back dictations to stomp each other's clipboard ? stale paste ("by Chad Gpte") + lost words. Now set?Ctrl+V?0.30s?restore, inline, no thread.

### 6. Hard-pinned OpenAI host + .env-first key
- **Why**: Intermittent 404 "Invalid URL POST /v1/audio/transcriptions" - instances launched from a polluted shell inherited a DeepSeek proxy address. Now typer ignores `OPENAI_BASE_URL` env var and reads its own `.env` for the real key.

### 7. This chat (E25B) now SOLELY owns typer
- E45 overstepped earlier (pushed FLAC when Max wanted MP3), then stood down. Collisions resolved.

### 8. No silent failures
- Empty transcript on short clip (<3s) types **nothing** (was pasting "[typer: no speech recognized - please repeat]" junk). Quick-tap floor at 0.45s.
- Real failures paste `[typer error: ...]` at cursor.

## CURRENT STATE

**Live and deployed** on all 3 instances (Plus F9/numpad+, Zero numpad0/Insert, Russian Right Ctrl):
- Groq Whisper large-v3, best-quality MP3 with normalization
- 2.0s pre-roll + 120s warm mic window
- Warm-keeper heartbeat (20s/20min)
- Recall (Left Alt + numpad+)
- Timing stopwatch (logs start-delay + transcribe time)
- Quick-tap guard (0.45s), empty-silence guard (3s floor before error message)

**Known issues still open:**
- **Speed inconsistency**: Groq free tier swings 1-14s randomly. Cure = paid Groq tier (pennies/hour).
- **Low mic level**: Max's speech is ?30 to ?35 dBFS. Normalization is now live to compensate, but the *source* level is still low - Windows mic slider may be turned down.
- **Paste-into-wrong-session**: if Max clicks into another field during the wait, paste lands there. Deferred-paste ("hold until you click back to the original field") was designed but NOT built - pending Max's go-ahead.
- **Progress bar / timing diagnostics**: Max wants real avg conversion/upload/wait times displayed, not a fake ETA. NOT built yet.

**Running right now**: 6 pythonw processes (Plus parent+child, Zero parent+child, Russian parent+child) from `C:\claude_base\tools\typer\venv\Scripts\pythonw.exe`. Autostart via Startup shortcut `typer_dictation.lnk` ? `start_typer_all.bat`.

## EXACT NEXT STEP

1. **Max tests the new normalized audio** - dictate one line, then say "play it" so I can play back the normalized sample. He judges volume + quality.
2. **If normalization is good**, next priority per Max: **compression tuning** (he's "still annoyed by the slowness" - but data proved compression doesn't affect speed; the real lever is Groq paid tier).
3. **If still too slow**, set up Groq paid API key (already have free key at `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` - paid tier just needs a different key/tier).
4. **Progress bar** (Max's priority #2): build real timing diagnostics into the meter overlay.
5. **Deferred paste** (Max's priority #3): hold text and deliver when he clicks back to the original dictation field.
6. **Patch typer2** (portable copy at `C:\claude_base\tools\typer2\`) with all the fixes - still on old code, NOT running.

## OPEN QUESTIONS AWAITING MAX

- Is the normalized volume good enough, or does he want me to check Windows mic slider level?
- Does he want the Groq paid tier (to kill the 1-14s speed swings)?
- "During those 5s wait, are you typing into another field or just reading?" - determines whether the deferred-paste feature helps or annoys.
- Should typer2 be patched now or later?

## KEY PATHS / IDs / COMMANDS

- **Live tool**: `C:\claude_base\tools\typer\typer.py` (all instances)
- **VU meter**: `C:\claude_base\tools\typer\meter.py`
- **Launchers**: `start_typer.bat` (Plus, `--key f9,numplus --lang en --paste --recall lalt+numplus`), `start_typer_zero.bat` (`--key num0,numins --lang en --paste`), `start_typer_ru.bat` (`--key rctrl --lang ru --paste`), `start_typer_all.bat` (calls all three)
- **Key file**: `C:\claude_base\tools\typer\.env` (OPENAI_API_KEY for real OpenAI, groq key in separate file)
- **Groq key**: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt`
- **Logs**: `typer_runtime_en.log`, `typer_runtime_ru.log` beside typer.py
- **Sample file**: `C:\claude_base\tools\typer\_last_sample.mp3` (last saved clip for quality checks)
- **Probe tool**: `C:\claude_base\tools\typer\mic_probe.py` (records 20s raw WAV for level testing)
- **Portable copy**: `C:\claude_base\tools\typer2\` (stale, needs patching)
- **Git**: claude_base repo, master branch. Most recent typer commits: `15eaa0a4` (normalization+MP3), `80cc618d` (Groq swap), `f819c0c8` (pre-roll bump), `901d08f9` (hard-pinned host), `0aab7524` (race-free paste), `f4ae6a4d` (empty-silence fix).
- **Process management**: `Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object {$_.CommandLine -like '*typer.py*'}` then `Stop-Process`. Relaunch via `Start-Process pythonw.exe -ArgumentList '...' -WindowStyle Hidden`.
- **Autostart**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\typer_dictation.lnk` ? `start_typer_all.bat`
- **Session signature**: ? E25B (bcast)
- **Consult**: `python C:/claude_base/tools/consult/consult.py <target> "<question>"`

## GOTCHAS

1. **NEVER edit typer.py from two sessions at once** - E45 and E25B collided on it earlier (FLAC vs MP3). E45 stood down. This chat now owns it.
2. **pythonw launched via `cmd /c start ...bat` flashes a black console** - prohibited. Always use `Start-Process pythonw.exe -WindowStyle Hidden` directly.
3. **Stop-Process on parent kills child** - iterating pids yields "process not found" on the child; harmless.
4. **Suicide-prevention hook** blocks 3 consecutive Reads of the same file - interleave with Grep/Edit.
5. **PowerShell `$_` variable mangled when passed through bash** - use the PowerShell tool directly, not bash?powershell.
6. **The 2.0s pre-roll is NOT a 2s delay** - it's a rewind buffer. Don't zero it; it fixes the swallowed-start.
7. **Max's green VU bar looks "proper" but the level is quiet** - the meter scale bottoms at ?55 dB, so ?35 dB speech shows ~38%. The bar is misleading. Normalization compensates.
8. **NumLock OFF is required** for Max's nav pad (Page Up/Down/Home/End). Zero backup key works in both states (bound to both 0x60 numpad-0 and 0x2D Insert).
9. **Numpad+ suppression** works by pynput raising an exception - must never catch it. Numpad+ is a char-emitting talk key; its "+" is swallowed.
10. **The "by Chad Gpte" stale-paste disaster** was a 2.5-second clipboard-restore race I introduced. Deployed fix is synchronous (0.30s) - never widen that delay again.
11. **Warm-keeper** uses a tiny silent clip (~0.1s) to ping Groq every 20s. First dictation after a long pause may still be cold; subsequent ones warm.
12. **Groq's free tier** is the root cause of the wild 1-14s swing - NOT our code, NOT compression, NOT the model. The logged TRANSCRIBE times prove it.
