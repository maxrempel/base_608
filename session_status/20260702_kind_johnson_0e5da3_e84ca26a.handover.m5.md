# Scribe handover - milestone 5 (~377K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-07-02 13:36:19 by deepseek-v4-pro

# HANDOVER - Typer Dictation Tool (Session E25/E25B)

## GOAL (in Max's own words)

Max wants a **fast, reliable, hold-to-talk voice dictation tool** that never loses sentences, never pastes into the wrong window, transcribes accurately with his accent in both English and Russian, and doesn't pollute his clipboard history. He uses it all day, every day, on Pine (his main Windows machine). He iterates on it constantly and expects fixes to be tested on a "dev" key first (numpad-0) before touching his "production" keys (F9/numpad+ and Right Ctrl).

---

## DECISIONS MADE + WHY

### 1. STT Engine: OpenAI ? Groq Whisper large-v3
**Why:** OpenAI's whisper-1 was taking ~10-14s per dictation. Max demanded speed AND accuracy. Groq runs the same Whisper family at ~200x realtime, OpenAI-compatible API, identical accuracy for his accent.
**Caveat:** Groq's free tier has rate limits and variable server latency (1-14s). The warm-keeper heartbeat was exacerbating rate-limiting (see Gotchas).
**Reversible:** One constant change (`STT_PROVIDER = "openai"`) reverts to OpenAI instantly.

### 2. Encoding format: Raw WAV ? MP3 (best quality, ~33-42 kbps)
**Why:** Max insisted speed matters more than lossless audio. MP3 is 3-16x smaller than WAV, reducing upload time. Tests proved further compression (28KB vs 469KB) does NOT meaningfully improve speed because Groq's server latency dominates.
**Note:** Max briefly tested FLAC (lossless) via another session (E45); he rejected it - MP3 is the settled choice.

### 3. Clipboard paste with Win+V history exclusion (instant, no animation)
**Why:** Max hated the char-by-char "typing animation" of the Unicode SendInput method. Clipboard paste is instant. Windows clipboard history is excluded via registered formats, so Win+V stays clean. Previous clipboard contents are restored after 0.3s.
**Critical race fixed:** The restore was once a background thread with a 2.5s delay - that caused back-to-back dictations to paste stale text. Now it's synchronous (set?Ctrl+V?0.3s?restore, in the same call), race-free.

### 4. Resilient warm-pool recorder (pre-roll buffer + latency="high")
**Why:** Per-press cold mic open was losing the first 0.5-2s of speech (maximally after hibernate). The fix opens a persistent `sd.InputStream` with a 2s rolling pre-roll buffer, so any press grabs the audio from slightly *before* the key registered. Stream auto-releases after 120s idle (NOT always-on). Tail-drain of 0.35s captures the ending.

### 5. Recall key: Left Alt + numpad+ re-sends previous dictation
**Why:** When focus is stolen during the transcription delay, the text lands nowhere. Max wanted a way to re-send it. Holding Left Alt and tapping numpad+ re-pastes and re-sends the last completed dictation. This freed Ctrl+numpad+ for Chrome zoom (his explicit request).
**Held-modifier bug fixed:** Recall requires Left Alt to be physically held, which corrupted Ctrl+V into Ctrl+Alt+V and Enter into Alt+Enter - both are now cleared before synthetic keys.

### 6. No-send: hold Right Shift while releasing the talk key = type-only, no Enter
**Latch-based:** Windows' NumLock injects a fake Shift-UP at numpad key events, making a release-instant shift read unreliable. The code latches any real (non-injected) shift-down during the recording window.

### 7. Quick-tap floor (0.45s) + empty-clip silence
**Why:** Whisper hallucinates phantom sentences on near-empty audio from accidental key bumps. Clips under 0.45s are discarded. Empty transcripts for clips under 3s type nothing at the cursor (no "[typer: no speech recognized]" junk).

### 8. Spoken punctuation (English + Russian)
"comma", "period", "question mark", "exclamation mark", "three question marks", "quote"/"end quote", etc. - plus Russian equivalents. Applied by regex before delivery.

### 9. OpenAPI key hardened against environment pollution
**Root cause of 404 "Invalid URL":** When instances were launched from a shell with a DeepSeek proxy's `OPENAI_API_KEY` and `OPENAI_BASE_URL` set, Whisper calls went to a server with no transcription endpoint. Fix: key always read from typer's own `.env` first, and `base_url` hard-pinned to `https://api.openai.com/v1`.

### 10. Normalization + best-quality MP3 encoding
**Issue:** Max's microphone input level was found to be ~20 dB below normal speech (?35 dBFS vs expected ?15). He insisted the green VU bar "jumps properly" - but the bar's scale bottoms out at ?55 dB, so ?35 dB shows ~38% fill and *looks* healthy. His raw, unconverted voice measurement confirmed the quiet is at the source (mic/Windows input gain), not in the encoding. Normalization boosts each clip to ?20 dBFS with a limiter to handle plosives. Best-quality MP3 was chosen to avoid lossy-artifact distortion.

### 11. Warm-keeper KILLED (was causing rate-limiting)
**Why:** The warm-keeper pinged Groq every 20s to keep the connection warm. With orphaned instances stacked up (22 pythonw processes), this hammered Groq's free tier past its rate limit. The SDK silently retried with backoff, ballooning 1s calls to 14s - which Max experienced as "very slow." Warm-keeper removed. Rate-limit visibility added.

### 12. Russian instance on OpenAI, English on Groq
**Why:** Groq's free tier has rate limits; Russian dictation was randomly failing. Russian now uses `--provider openai` so it talks to stable OpenAI whisper-1, while English uses the faster Groq.

---

## CURRENT STATE

**Tool:** `C:\claude_base\tools\typer\typer.py` (commit `15eaa0a4` + additional uncommitted edits for timing instrumentation, warm-keeper removal, per-instance provider)
**Live instances (should be 3 pair = 6 pythonw processes):**
- Plus (English): F9 + numpad+ ? talk, Groq large-v3, `--paste --lang en`
- Zero backup (English): numpad-0/Insert ? talk, Groq large-v3, `--paste --lang en`
- Russian: Right Ctrl ? talk, OpenAI whisper-1, `--paste --provider openai --lang ru`

**Launchers:**
- `start_typer.bat`: Plus English
- `start_typer_zero.bat`: Zero backup
- `start_typer_ru.bat`: Russian
- `start_typer_all.bat`: calls all three

**Autostart:** `typer_dictation.lnk` in Startup folder ? `start_typer_all.bat`

**Active features:**
- Instant clipboard paste (Win+V excluded, 0.3s restore)
- Normalization + best-quality MP3
- Resilient warm-pool recorder (2s pre-roll, tail-drain, 120s idle close)
- Quick-tap floor (0.45s), empty-clip silence (3s threshold)
- No-send via Right Shift (latch-based)
- Recall: Left Alt + numpad+ re-sends last dictation
- Spoken punctuation (EN + RU)
- Timing instrumentation: every dictation logs `encode ms | api ms | paste ms | total ms`
- Rate-limit visibility: OpenAI client has `max_retries=1` so 429s surface as errors instead of silent retries

**What's NOT running:** The warm-keeper is dead. No background pings to Groq.

**typer2:** `C:\claude_base\tools\typer2\` - portable installer kit (NOT running on Pine). Has its own `.env`, `install.bat`, `README_tomemex.md`. NOT affected by this session's changes - needs patching separately.

**Session ownership:** This chat (E25/E25B) **owns** typer. E45 (another Claude session) was also editing typer.py - that collision was resolved; E45 stood down. Do not let another session re-commit typer.py from a stale worktree.

---

## EXACT NEXT STEP

1. **Verify only 6 pythonw processes** remain (3 instances ? 2 processes each). If there are more, kill orphans. The machine may still have leftover copies from repeated restarts.
2. **Get Max to test dictation on Plus (English) and Right Ctrl (Russian).** Both should transcribe accurately.
3. **Evaluate the timing log:** after Max dictates a few lines, read `typer_runtime_en.log` for the new timing breakdown (`TIMING: encode=Xms api=Yms paste=Zms total=Wms`). This will show whether the slowness is API, network, or paste.
4. **If speed still unacceptable:** the real lever is a cheap paid Groq tier (skips free queue), OR revert English to OpenAI (slower but unbounded). Max's call.
5. **If Russian Groq errors recur:** Russian is already on OpenAI. If it still fails, check the `.env` key and OpenAPI base URL pinning.
6. **Commit the currently uncommitted changes** (timing instrumentation, warm-keeper removal, per-instance `--provider` flag) once confirmed stable.

---

## OPEN QUESTIONS (awaiting Max)

1. **Does Max want a paid Groq tier** to eliminate the free-tier latency swings? (Pennies per hour of audio.)
2. **The quiet microphone:** Max insists his Windows mic level is correct and the green bar jumps properly. The raw probe measurement shows ?35 dBFS (quiet). He may want the Windows input level actually raised, or may be satisfied with software normalization. Unresolved conversation.
3. **Deferred-paste (hold text until user returns to the original field)** was discussed as a fix for "text landing in the wrong window" - Max liked it, but priority was speed/compression first. Not built.
4. **Progress bar improvement** (show real encoding/upload/wait phases instead of fake ETA) was requested but deferred behind speed work.
5. **typer2 portable copy** needs the same fixes (normalization, MP3 encoding, recall key, hard-pinned base URL) - not yet patched.

---

## KEY PATHS / IDS

| Item | Path / Value |
|------|-------------|
| Live tool | `C:\claude_base\tools\typer\typer.py` |
| VU meter | `C:\claude_base\tools\typer\meter.py` |
| English log | `C:\claude_base\tools\typer\typer_runtime_en.log` |
| Russian log | `C:\claude_base\tools\typer\typer_runtime_ru.log` |
| Venv | `C:\claude_base\tools\typer\venv\` |
| OpenAI key | `C:\claude_base\tools\typer\.env` (gitignored) |
| Groq key | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| Autostart shortcut | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\typer_dictation.lnk` |
| typer2 (portable) | `C:\claude_base\tools\typer2\` |
| Backup (pre-streaming) | `C:\claude_base\tools\typer\archive\` |
| Probe recordings | `C:\claude_base\tools\typer\probe\` |
| Sample MP3 | `C:\claude_base\tools\typer\_last_sample.mp3` |
| This session's worktree | `C:\claude_base\.claude\worktrees\kind-johnson-0e5da3` |
| E45 (collision resolved) | Other Claude session - stood down, does NOT own typer |

---

## GOTCHAS & DEAD ENDS

1. **Do NOT restart typer while Max is mid-sentence** - it drops that one clip. Warn him first and pick a quiet moment.

2. **Modifier keys (Shift, Ctrl, Alt) are unusable as talk keys.** They get used constantly for other things, triggering junk recordings. Don't try it again.

3. **The `suppress_event()` call works by RAISING an exception.** If you wrap it in try/except, suppression silently breaks. Must propagate.

4. **The 40-byte INPUT struct** - if you ever touch the SendInput code, the union MUST be padded `("_pad", ctypes.c_ubyte * 32)` or it silently no-ops. Proven the hard way.

5. **Held Alt corrupts synthetic Ctrl+V and Enter** during recall. The fix clears Alt vks (0x12, 0xA4, 0xA5) before synthetic keystrokes.

6. **Windows fakes Shift-up at numpad key events** (NumLock quirk). Do NOT read shift state at the release instant - use the latch pattern (catch real shift-down during the recording window).

7. **22 orphaned pythonw processes** from repeated restarts were the likely cause of "glitchy" feel AND the warm-keeper rate-limiting. Always verify exactly 6 after restarting (3 instances ? parent+child).

8. **Two Claude sessions editing typer.py = guaranteed collision.** E45 stood down; this chat owns it. If you see fresh commits to typer.py from another session, reconcile before touching anything.

9. **The green VU bar's scale bottoms out at ?55 dB,** so a ?35 dB signal looks healthy (~38% fill) even though it's 15-20 dB below normal dictation. Don't trust it as a true loudness gauge.

10. **`cmd /c start ...bat` opens black console windows** - Max prohibits this. Always launch with `Start-Process pythonw.exe -ArgumentList ... -WindowStyle Hidden`.

11. **The stopwatch showed zero start-delay** (lag=0ms) on recent dictations, confirming the pre-roll buffer captures the beginning. If beginnings are still being lost, check that instances are actually running the new code (not old orphaned copies).

12. **Pushing untested code to master is forbidden** - Max's plus key got broken once by an untested deploy. Test on Zero (numpad-0) first.
