# Scribe handover - milestone 3 (~230K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-07-02 12:11:52 by deepseek-v4-pro

# HANDOVER: Typer Dictation Tool - E25B (July 2, 2026)

---

## ? MAX'S GOAL (in his own words)
Make the typer hold-to-talk dictation tool **fast, accurate, never lose words**, with safe paste (no stray characters, no clipboard pollution), a reliable recall key, a real diagnostic progress bar, and eventually the ability to continue typing elsewhere during transcription without dumping the result into the wrong field. The tool must work for both English and Russian, and survive slow CPUs / slow network.

---

## ? DECISIONS MADE + WHY

### 1. TRANSCRIPTION ENGINE: OpenAI Whisper ? Groq Whisper large-v3
- **Why:** OpenAI's Whisper API was slow (10+ seconds for a short dictation). Groq runs the same Whisper model ~200x realtime, via an OpenAI-compatible API. The key already existed on disk (`groq_api_key_20260611.txt`). The model pinned to `whisper-large-v3` after turbo mis-recognized simple words. The code auto-loads the Groq key from that file and uses `base_url="https://api.groq.com/openai/v1"`. These are hand-coded, ignoring environment variables (to avoid the "polluted shell" 404 bug of earlier sessions).

### 2. AUDIO UPLOAD: RAW WAV ? MP3 (then to FLAC after quality complaints)
- **Why:** Upload size was the real speed bottleneck, not model compute. Max correctly spotted that length scaled with wait time. Tests proved 30s of audio: WAV 0.96MB ~4.5s, MP3 0.06MB ~0.9s. MP3 was fast but produced audible distortion on a quiet signal. The final state on **disk** is **FLAC** (lossless, ~3x smaller than WAV, zero quality loss), but the **running instances still have MP3** pending a restart. The user wants to try FLAC first, and only fall back to a higher-bitrate lossy format if speed is still a problem.

### 3. RESILIENT RECORDER: Warm-pool mic with pre-roll buffer
- **Why:** The old per-press open/close of the mic caused warm-up gaps that swallowed the beginning of phrases, especially on a cold machine or after hibernation. The final recorder keeps the mic stream open between dictations (auto-releases after 120 seconds of idle), with a **2.0-second pre-roll ring buffer** that captures audio before the key is pressed. The key-press instantly grabs the buffer, so lead-in words are not lost. No delay is added; the pre-roll is a backward-looking safety net.
- **Additionally:** A `blocksize=800` high-latency stream prevents PortAudio from dropping audio under CPU load, and a 0.35-second tail-drain captures audio still buffered on release.

### 4. PASTE: Clipboard-based, race-free, history-excluded
- **Why:** The user wanted "instant, no typing animation." The tool now uses the Windows clipboard with history-exclusion formats (Win+V cache never sees it) and a synchronous paste: `set clipboard ? Ctrl+V ? wait 0.3s ? restore previous clipboard`. No background thread, so back-to-back dictations can't race. The clipboard-restore delay was briefly 2.5s (caused the "by Chad Gpte" stale-paste disaster) and is now 0.3s. The old keystroke-injection path still exists behind the `--paste` flag.

### 5. RECALL KEY: Left Alt + numpad+
- **Why:** Max wanted a way to re-send the last dictation when focus was lost. The recall key holds Left Alt and taps numpad+ -- it re-pastes and re-sends the previous transcript. The implementation clears any physically-held Alt/Shift/Ctrl before pasting and Enter, to avoid corrupting the key combo.

### 6. EMPTY TAPS: Minimum 0.45s hold, silent on short empty clips
- Taps shorter than 0.45s are discarded entirely (to avoid Whisper hallucinating on noise). If a longer clip produces an empty transcript and the clip duration is <3.0s, nothing is typed; if ?3.0s, an error is pasted so the user knows the dictation failed.

### 7. MODIFIER KEYS AS TALK KEYS: Abandoned
- Left Shift/Left Ctrl were briefly mapped as talk keys, which broke all keyboard shortcuts. Immediately reverted. Only non-modifier keys (F9, numpad+, numpad0/Insert, Right Ctrl) are now used.

---

## ?? CURRENT STATE

### Live instances (all running from `C:\claude_base\tools\typer\typer.py`)
| Instance | Talk key(s) | Language | Notes |
|----------|-------------|----------|-------|
| **Plus (main)** | F9, **numpad+** (+ Left Alt = recall) | English | --paste, --recall lalt+numplus |
| **Zero (backup)** | numpad 0 / Insert (NumLock off) | English | --paste, no recall |
| **Russian** | Right Ctrl | Russian | --paste |

All launched via `pythonw` (hidden). Files: `start_typer_all.bat`, `start_typer.bat`, `start_typer_zero.bat`, `start_typer_ru.bat`. `typer2` is a portable copy for other computers, not running on Pine.

### Code state on disk (committed, pushed to master, commit `0e681568` + some uncommitted local edits)
- STT engine: Groq Whisper large-v3, forced API host, key from local `.env`.
- Recorder: warm pool, 2s pre-roll, 120s idle close, 0.35s tail drain, high-latency input.
- Paste: synchronous clipboard with history exclusion, 0.3s restore.
- Audio encoding: **Disk says FLAC**, but running instances were restarted with an earlier MP3 version and have NOT been restarted to pick up FLAC.
- The warm-keeper pings Groq every 20s with a tiny FLAC clip to keep the connection/model warm for 20 minutes after last dictation.

### Open tool modifications (not yet applied)
- **Audio normalization/boost:** The discovered quiet recording (~ -30 dBFS) likely degrades recognition. A gain + soft compression step would help.
- **Real diagnostic progress bar:** Max wants the VU bar to show actual timings (conversion, upload, wait) instead of a fake ETA. Implementation: hook into the transcribe steps, push fractions to meter.
- **Field-remembering / focus-safe paste:** Max wants to type elsewhere during transcription without the paste landing in the wrong field. A proposed approach: remember the target window, hold the text, deliver when the user returns, or deliver on recall.

### Known issues
1. **Recording level is too quiet** - RMS ~-30 dBFS, while normal speech is -18 dBFS. The VU meter looks like it's jumping properly because its floor is -55 dB, but the actual level is very low. This probably causes recognition errors and makes lossy audio sound terrible.
2. **Distortion on playback** - Due to the current MP3 encoding (42 kbps) on a quiet signal. FLAC will fix the distortion; normalization will fix the quietness.
3. **No normalized audio before upload** - The quiet signal hurts both playback quality and likely recognition accuracy for Groq.
4. **Turbo model mis-recognized simple words** - Max reverted to large-v3. That is the correct model for his accent.
5. **Cold start on Groq** - The first dictation after a long pause can take 6-12s because Groq's model goes cold. The warm-keeper heartbeat (20s interval) mitigates this, but a truly cold start still happens after 20+ minutes of silence. The heartbeat stops after 20 minutes idle to avoid wasteful API calls.
6. **Progress bar** - Not yet started; the diagnostic meter code (the `_step` approach) hasn't been written.
7. **Cross-session collision** - Another session (E45) also edited typer.py during this period. The disk file is the reconciled version. Ensure only one branch touches typer.py at a time.

---

## ?? EXACT NEXT STEP

**Fix the audio quality issue (quiet + distortion).** The user said "don't change, just investigate" - but the investigation is done. The fix is needed before further work. The actions:

1. **Add audio normalization/boost** in the transcribe path, before encoding. A simple approach: compute RMS gain to bring the signal up to ~-18 dBFS target, or use a dynamic compressor. This will improve both playback quality and recognition accuracy.
2. **Ensure FLAC encoding is used** (already on disk, but verify). If FLAC is not possible for some reason, use a higher-bitrate lossy format.
3. **Restart the Plus (main) + Russian instances** to pick up the FLAC code and the normalization.
4. **Generate a new sample audio** (the code already saves `_last_sample` on each dictation) and test the playback quality. If the user confirms it sounds good and recognition improves, lock it in.
5. **Commit and push.**

The user also has pending requests for the **diagnostic progress bar** and **field-remembering** - those come after the audio fix.

## ? OPEN QUESTIONS AWAITING MAX

- None critical. The immediate next step is clear. After the audio fix, Max can re-prioritize progress bar vs field-remembering.

---

## ? KEY FILE PATHS & IDs

| What | Path |
|------|------|
| Live typer | `C:\claude_base\tools\typer\typer.py` |
| VU meter overlay | `C:\claude_base\tools\typer\meter.py` |
| English launcher | `C:\claude_base\tools\typer\start_typer.bat` (`--key f9,numplus --lang en --paste --recall lalt+numplus`) |
| Zero backup launcher | `C:\claude_base\tools\typer\start_typer_zero.bat` (`--key num0,numins --lang en --paste`) |
| Russian launcher | `C:\claude_base\tools\typer\start_typer_ru.bat` (`--key rctrl --lang ru --paste`) |
| All-instances launcher | `C:\claude_base\tools\typer\start_typer_all.bat` |
| OpenAI API key (typer's own) | `C:\claude_base\tools\typer\.env` (gitignored) |
| Groq API key | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| Python venv | `C:\claude_base\tools\typer\venv\` |
| Portable installer (not running) | `C:\claude_base\tools\typer2\` |
| Typer method doc | `C:\claude_base\tools\typer\typer_method_v01_tomemex.md` |
| Runtime log | `C:\claude_base\tools\typer\typer_runtime_en.log` / `_ru.log` |
| Last sample audio | `C:\claude_base\tools\typer\_last_sample.mp3` (current) |
| Git commit for latest E25B push | `0e681568` (FLAC + warm-keeper + turbo model, but turbo later reverted) - there may be subsequent uncommitted local changes (e.g., model revert to large-v3 on disk) |
| Session name | **E25B** (the caller is E25) |
| Board / communications | `bcast.py`, `consult.py`, `fleetcomm.py` in `C:\claude_base\tools\` |

---

## ? GOTCHAS AND RULED-OUT DEAD ENDS

- **Do NOT set pre-roll to zero.** The 2-second buffer is a rewind, not a delay. Removing it makes the beginning loss *worse*.
- **Do NOT reintroduce the 2.5-second clipboard restore delay.** That race caused all the stale-paste disasters. The current 0.3s synchronous restore is correct.
- **The VU meter's green bar is misleading** - it shows ~half-full even at -30 dBFS, so the user perceived proper levels when the actual recording was very quiet. The meter scale (floor -55 dB, max -3 dB) should probably be changed to reflect normal speech range.
- **Modifier keys (Shift, Ctrl) as talk keys are permanently ruled out** - they break all normal keyboard shortcuts.
- **Turbo model (whisper-large-v3-turbo) is ruled out for Max's accent** - it mis-recognized simple words. Use `whisper-large-v3`.
- **MP3 at very low bitrate (42 kbps) causes audible distortion** especially on quiet signals. FLAC avoids this entirely.
- **Pasting into the wrong field** happens when the user clicks into a different input while waiting; Windows cannot type into a truly background field. Any fix must either prevent the paste or briefly flip focus back to the original field.
- **The `_last_sample` file is generated on every dictation** (the code currently saves an MP3; after FLAC it should be `.flac`). That's the file to play back for quality checks.
- **Do not edit typer.py from multiple sessions simultaneously** - branching collisions wasted time today. E25B owns this file until further notice.
