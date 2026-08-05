# Scribe handover - milestone 6 (~453K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-07-02 14:22:47 by deepseek-v4-pro

# TYPER SESSION HANDOVER - SESSION E25B

---

## GOAL (Max's words)
Max is building and maintaining **typer**, his all-day hold-to-talk voice dictation tool. Three instances run simultaneously: **English Plus** (F9 / numpad+), **English Zero backup** (numpad 0 / Insert), and **Russian** (Right Ctrl). Hold the key ? record mic ? Whisper transcribes ? text appears at cursor + Enter to send. Hold **Shift** on release = type only, no Enter. **Left Alt + numpad+** re-sends the last dictation (recall).

This session's primary goal evolved from fixing bugs (swallowed sentences, clipboard races, 404 errors) into a major performance investigation: dictation was taking **5-14 seconds** instead of the normal ~1s. Max wanted speed back, and wanted to experiment with Groq (a faster/cheaper Whisper provider) without breaking his daily tool.

---

## DECISIONS MADE + WHY

### 1. Groq STT engine switch (then REVERTED)
- **Decision:** Switched transcription from OpenAI's `whisper-1` to Groq's `whisper-large-v3` (same model family, 200x faster on their hardware, OpenAI-compatible API).
- **Why:** Max complained dictation was taking ~10s for 200 characters. Groq offered sub-second warm latency. We already had a Groq API key on disk.
- **Problemp:** Groq's free tier has aggressive rate-limiting. The `warm_keeper` (a 20s heartbeat to keep the connection warm) combined with orphaned duplicate processes (22 pythonw instances from repeated broken restarts) hammered the rate limit ? the SDK silently retried with exponential backoff ? 1s calls ballooned to 5-14s. E45 (a watching diagnostic session) proved the round-trip was length-independent ? rate-limiting, not network.
- **Also:** The `turbo` Groq model mis-recognized simple words for Max's accent. FLAC vs MP3 experiments consumed time but file size proved irrelevant (server latency dominated).
- **Outcome:** Reverted back to OpenAI `whisper-1` (the months-stable ~1s path). Groq experiment is parked in a separate file for later testing.

### 2. Normalization / volume boost
- **Decision:** Added a normalize step: every recorded clip is boosted to a healthy ?20 dBFS target level (with a limiter to prevent clipping from stray clicks).
- **Why:** Max complained the saved audio sample was "super quiet and distorted." Investigation proved his Windows mic input level is genuinely low (?30 to ?35 dBFS speech), and the low-quality MP3 default (~33 kbps, lossy) made quiet audio sound distorted on playback. The VU meter was misleading (scale floors at ?55 dB, making ?35 dB look mid-range). Normalization fixes both playback quality and likely sharpens recognition.
- **Status:** The normalization code was written and tested (proven with a ~25 dB boost on a quiet clip), BUT it lives in the experimental `typer.py` - not in the live stable version Max is currently running.

### 3. MP3 quality
- **Decision:** Bumped MP3 encoding from the default ~33 kbps to `compression_level=0.0` (best quality).
- **Why:** File size proven irrelevant for speed (16x size reduction only saved ~350ms, while Groq/OpenAI server variance was 500-2000ms). Best quality costs nothing in speed and sounds better.
- **Status:** Also in the experimental version only.

### 4. Recall key (Left Alt + numpad+)
- **Decision:** Built a "recall" feature: hold Left Alt, tap numpad+ ? re-pastes and re-sends the last dictation. This frees Ctrl+numpad+ for Chrome zoom (which collided with the old talk-key binding).
- **Why:** Max explicitly asked for this: "left alt plus numpad to paste what was already dictated previously."
- **Bug fixed:** Held Left Alt was corrupting Ctrl+V (turning it into Ctrl+Alt+V ? no paste) and Enter (turning it into Alt+Enter). Fixed by adding Alt vks (0x12, 0xA4, 0xA5) to the modifier-clear list in `_send_ctrl_v` and `press_enter`.
- **Status:** This fix IS in the current stable version (commit 100fdd47).

### 5. Resilient warm-pool recorder
- **Decision:** The mic stream opens on first press, stays warm between phrases, auto-releases after 120s idle. `latency="high"` big buffer, 2.0s pre-roll ring buffer (catches lead-in words), 0.35s tail-drain (catches final buffered words).
- **Why:** Kills the "swallowed beginning" bug (per-press cold mic open lag) and the "swallowed end" bug (buffered audio discarded on immediate close).
- **Status:** In the stable version (74bfdf56).

### 6. No-silent-failures + stopwatch instrumentation
- Every dictation logs: encode ms | api ms | paste ms | total ms. Empty clips under 3s type nothing at cursor. Quick taps under 0.45s are silently dropped (no phantom sentence).
- **Status:** Timing instrumentation is in the experimental version; the basic empty/hush guards are in stable.

### 7. Clipboard paste race fix
- A 2.5s clipboard-restore delay (added by mistake earlier) caused the "disaster" where back-to-back dictations stomped each other ? stale/wrong paste. Fixed to synchronous race-free paste (set ? Ctrl+V ? 0.30s ? restore, inline, no thread).
- **Status:** In stable.

### 8. 404 "Invalid URL" fix
- Root cause: some instances inherited a polluted launch environment (`OPENAI_BASE_URL` pointing at DeepSeek proxy). Hard-pinned `base_url="https://api.openai.com/v1"` and made the API key load prefer `.env` file over environment.
- **Status:** In stable.

### 9. Session ownership / E45 collision
- Two Claude sessions (E25B and E45) were editing the same `typer.py` file simultaneously ? code clobbering, duplicated restarts, orphaned processes. Resolved by telling E45 to stand down (board + force-wake); this session (E25B) now owns typer.

### 10. The "revert to stable, experiment on numpad 7/8/9" plan (Max's most recent architecture decision)
- **Decision:** Keep the main keys (Plus, Zero, Russian) on yesterday's stable OpenAI version. Wire experimental improvements (normalization, MP3 quality, timing, Groq) onto isolated test buttons - numpad **7**, **8**, **9** - so Max can A/B test safely without his daily dictation ever breaking.
- **Why:** "I hate when the typing is broken because there are many windows that require my attention." Today proved that editing the live tool breaks it repeatedly.
- **Status:** The stable version was exported from commit `74bfdf56` and saved as `typer_stable.py`. The computer was rebooted and the stable instances were relaunched. Max was mid-test ("Restarted the computer, testing, testing...") when the session hit the context limit. The numpad 7/8/9 experiment buttons are NOT yet built.

---

## CURRENT STATE

- **Computer:** Freshly rebooted (Max initiated the reboot to clear orphaned processes and machine load).
- **Live instances:** `typer_stable.py` was launched via `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py` - 3 instances (Plus EN, Zero EN backup, Russian RU), 6 pythonw processes total.
- **Code version running:** Yesterday's stable commit `74bfdf56` - OpenAI `whisper-1`, resilient warm-pool recorder, recall fix, clipboard race fix, 404 fix. NO Groq, NO warm-keeper, NO normalization, NO MP3 quality bump.
- **Experimental code:** The day's improvements (normalization, best-MP3, timing instrumentation, Groq-switchable engine) live in `C:\claude_base\tools\typer\typer.py` but are NOT running. The stable version is the separate `typer_stable.py`.
- **Max reported just before the reboot:** "english died again" and "russian dead too and f9 dead" - but this was under the old messy state with orphaned processes. The reboot + clean single launch should have fixed it.
- **OpenAI key test:** Was initiated but interrupted. The stable version uses the key from `C:\claude_base\tools\typer\.env` (sk-proj-...), hard-pinned to `api.openai.com`. Should work.
- **Max's last words:** "Restarted the computer, testing, testing..." - he was about to test dictation.
- **E45:** Was told to stand down. Should no longer be editing typer.

---

## EXACT NEXT STEPS

1. **Verify typer is working after the reboot.** Ask Max to dictate a test line on his Plus key (F9 / numpad+). If it transcribes and pastes within ~1s, the stable version is alive and well. If not, check:
   - Are 6 pythonw processes running with `typer_stable.py` in their command line?
   - Does the OpenAI key still work? (Test a quick transcription: a 1s sine wave via the same `api.openai.com` endpoint.)
   - If dead, relaunch using `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py` (make sure ALL old typer processes are killed first via psutil).

2. **Build the numpad 7/8/9 experiment buttons** - this is the architecture Max explicitly approved:
   - Create a separate `typer_experiments.py` that loads the experimental version (normalization, best-MP3, timing, Groq-switchable engine).
   - Wire **numpad 7, 8, 9** as independent talk keys, each possibly testing a different config (e.g., 7 = OpenAI + normalize, 8 = Groq large-v3 + normalize, 9 = Groq turbo + normalize).
   - Launch these as SEPARATE processes so they never touch the stable keys (Plus/Zero/Russian).
   - This way Max can A/B test speed and quality safely while his daily tool works.

3. **Once the normalization is proven on test buttons,** promote it to the stable version. (The normalization is the single most impactful improvement: it fixes the quiet audio quality and likely improves recognition.)

4. **Document every key binding** on the Desktop `typer_commands.md` so Max (and any future session) knows what each button does.

---

## OPEN QUESTIONS AWAITING MAX

- **Is typer working after the reboot?** (Max was mid-test when the session ended.)
- **Does the stable OpenAI version feel fast enough?** (Before all the Groq experiments, it was ~1s - the normal baseline.)
- **Which experiments does he want on numpad 7, 8, 9?** Specifically: should one test Groq large-v3 (accurate but rate-limited), one test the normalization, one test both? Or just start with normalization on one button?
- **Does he still want the "hold text until I click back to the original field" feature?** (The deferred-paste to prevent wrong-window disasters - was discussed but deferred behind speed/quality.)
- **The slowness investigation proved it was Groq rate-limiting + orphaned processes, not network congestion.** But the machine was genuinely loaded (22 pythonw instances, multiple Claude sessions, possible video rendering). Worth checking: after the reboot, is the machine snappy again?

---

## KEY FILE PATHS

| What | Path |
|------|------|
| **Stable typer (LIVE, running)** | `C:\claude_base\tools\typer\typer_stable.py` |
| **Experimental typer (NOT running)** | `C:\claude_base\tools\typer\typer.py` |
| **Stable launcher script** | `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py` |
| **Kill-all helper** | `C:\Users\maxre\AppData\Local\Temp\typer_kill_all.py` |
| **VU meter overlay** | `C:\claude_base\tools\typer\meter.py` |
| **API key (.env)** | `C:\claude_base\tools\typer\.env` |
| **Groq key** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| **Runtime log (English)** | `C:\claude_base\tools\typer\typer_runtime_en.log` |
| **Desktop command table** | `C:\Users\maxre\Desktop\typer_commands.md` |
| **Method doc** | `C:\claude_base\tools\typer\typer_method_v01_tomemex.md` |
| **typer2 portable copy** | `C:\claude_base\tools\typer2\` (NOT running - dormant installer kit) |
| **Startup shortcut** | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\typer_dictation.lnk` |
| **Raw voice probe** | `C:\claude_base\tools\typer\probe\raw_lossless.wav` |
| **Bcast board** | `C:\claude_base\branch_bulletin\bcast.py` |
| **Stable commit** | `74bfdf56` (2026-07-01) in the claude_base repo |
| **Repo** | `C:\claude_base` (main branch = master) |

---

## GOTCHAS + DEAD ENDS

### Gotchas
- **Never edit the live typer file while Max is dictating.** The file change is harmless (in-memory process doesn't see it), but the RESTART kills his dictation mid-sentence. Always warn, test on an isolated key first, and restart during a known pause.
- **Use `Start-Process pythonw.exe -WindowStyle Hidden` to launch, never `cmd /c start ...bat`.** The bat flashes a black console window, which Max explicitly prohibited.
- **Never bind Ctrl or Shift as solo talk keys.** Max uses them constantly for shortcuts, and every press triggers a junk recording that pastes "[typer: no speech recognized - please repeat]" into his active field. He learned this painfully with Left Ctrl / Left Shift.
- **Numpad keys with NumLock OFF:** numpad 0 sends VK_INSERT (0x2D), not VK_NUMPAD0 (0x60). If binding numpad keys for experiments, map BOTH vk codes so they work regardless of NumLock state.
- **The clipboard restore race is deadly for back-to-back dictations.** The fix (synchronous, 0.30s delay) is in stable. Never reintroduce a background thread or long delay there.
- **22 orphaned pythonw processes** happened because repeated broken restarts left old copies alive. Always kill ALL typer processes before launching fresh ones, and verify exactly 6 remain (3 instances ? 2 processes each).
- **E45 was simultaneously editing typer** - the two-manager collision caused code clobbering. Resolved by telling E45 to stand down. Before making future changes, confirm E45 is not also touching the file.
- **Max rejects "always-on mic"** - the warm-pool recorder is the compromise (warm during active use, releases after 120s). Do not propose a permanently-open stream.
- **Max's microphone level is genuinely low** (~?35 dBFS speech). The VU meter misleads because its scale floors at ?55 dB. The normalization fix compensates, but raising the Windows mic input level would fix it at the true source. Max says he checked it and it's "perfect" - but the raw probe proved otherwise. Tread carefully: he may reject a Windows setting change.

### Dead ends already ruled out
- **Compression/file size is NOT the speed lever.** Proven with interleaved tests: 16x file size reduction saved ~350ms; server latency swung 500-2000ms. Don't chase
