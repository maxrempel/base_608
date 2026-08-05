# Scribe handover - milestone 7 (~551K tokens)
# session: 20260713_interesting_morse_10796f_e7428ae2
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-13 11:20:19 by deepseek-v4-pro

# HANDOVER - typer voice-dictation tool (E25C)

---

## GOAL (in Max's words)

Max is continuously refining his personal multi-button voice-dictation tool. This session was the aftermath of a long crash-hunt. The transcript covers: (a) diagnosing and fixing native COM crashes that killed all buttons after ~1 hour, (b) a full revert to the stable pre-experiment version, (c) selectively re-adding features on isolated buttons so nothing breaks what works, (d) making numpad buttons independent of NumLock state, (e) adding a playback/mic-monitor button, (f) fixing the mic to follow the current Windows default, and (g) adding hallucination cleanup for Russian subtitles. The one feature that was **built then wiped in the revert and never re-added** is the persistent big-font last-10-seconds display on the meter overlay.

---

## DECISIONS MADE + WHY

### 1. COM eliminated entirely (the crash fix)
- **What**: Replaced both pycaw (master-volume read) and SoundCard (WASAPI multi-speaker chime) with `winsound` - pure Win32, zero COM.
- **Why**: Every dead instance logged `_ctypes.pyd 0x91bd` - a native access violation inside Python's COM bridge. It was a low-frequency-per-chime crash, so heavy dictation across buttons made every instance accumulate enough calls to hit it within an hour. Two prior "fixes" (reducing pycaw frequency, then removing pycaw) still crashed because SoundCard's WASAPI playback also drove COM hundreds of times per hour. The only definitive fix was removing COM entirely.
- **Trade-off**: Chime plays only on the default audio device at a fixed quiet level (~0.35 gain). No longer follows the Windows volume slider, no multi-speaker fanout. Max accepted this.

### 2. Full revert to stable pre-experiment version (c2d076d8)
- **Why**: The crash-churn + race + auto-language + HUD churn broke working buttons and wasted Max's dictation time. He ordered: "Return to the previous working version and stop breaking what works."
- **What was reverted**: Everything - race mode, universal/auto-language button, summary HUD overlay, all of it. Reverted to separate language-per-button layout.

### 3. Race re-added ISOLATED on num4 only
- **Why**: Max wanted the race back ("fast on cold start") but NOT on his primary button (Num+). Placed on num4 so if it ever breaks, his main buttons are untouched.
- **Race**: local large-v3 + OpenAI whisper-1 in parallel, fastest wins. English only, no auto-language. No HUD.
- **Race winner data** (from earlier testing, 37 dictations): local won 23x (62%), OpenAI won 14x (38%) - proving the race is genuinely useful (each wins different scenarios).

### 4. NumLock independence (numpad buttons work with NumLock OFF)
- **Why**: NumLocker was unreliable and kept forcing NumLock OFF. Max uses numpad 1/7/9/3 as Home/End/PgUp/PgDn navigation keys in nav mode, so NumLock should stay OFF permanently. But typer's numpad talk keys (2/4/6/8/0) need to work regardless.
- **Fix**: Disabled NumLocker (moved autostart shortcut to .disabled). NumLock stays OFF permanently. Typer's hook now catches **numpad nav codes** (Down=0x28, Left=0x25, Right=0x27, Up=0x26, Insert=0x2D) but applies `is_extended` bit-flag filtering so **non-extended** numpad nav keys route to typer while real dedicated arrow keys (extended flag set) pass through untouched.
- Race moved from num1 to num4 because num1=End (Max uses it).

### 5. num8 = playback/mic-monitor button (replaced Groq)
- **Why**: Max wanted to hear his own recordings without transcription - record, stop, play back, hear the mic quality.
- **Implementation**: Click to record, click to stop ? plays via winsound. No transcription, no model loading. Escape stops playback mid-play.
- Groq was rarely used so it was displaced.

### 6. Mic now follows Windows default (not stuck on one mic)
- **Why**: Max switched mics and typer stayed on the old one. Root cause: PortAudio caches the device list at init and never re-checks when Windows default changes.
- **Fix**: Added `_maybe_refresh_mic()` - after ~3s of recording-idle, calls `sd._terminate()` + `sd._initialize()` to pick up the new Windows default device. Opening-words are preserved (pre-roll data is dropped on a re-init). Rapid back-to-back dictation doesn't refresh (stays fast). The meter bar's mic-name label updates to show the new device.

### 7. Escape stops playback
- **Why**: Max wanted Escape to halt the num8 playback while it's playing.
- **Fix**: Added `_PLAYING` global flag. Escape block checks it: if `_PLAYING`, aborts the playback thread. If nothing's playing, Escape passes through normally.

### 8. Hallucination cleaner for Russian (??????????? ??????? etc.)
- **Why**: Whisper large-v3 hallucinates trailing Russian subtitle phrases (trained on YouTube/TV subtitles). Max kept seeing "??????????? ???????...", "??????? ?? ????????", etc. even with zero trailing silence.
- **Fix**: Two-tier cleaning: (a) **trailing strips** - removes known subtitle phrases from the END of the text (regex: ??????????? ???????, ??????? ?? ????????, ???????? ??????..., thanks for watching, subscribe, etc.); (b) **whole-text removal** - if the entire transcription is a single hallucination word ("???????", "you", "thank you"), it returns empty. Does NOT remove these phrases mid-text (real uses are preserved).

### 9. Safe restart tool (`restart_typer_safe.py`) - the restart rule is BUILT IN, not remembered
- **Why**: Max ordered: "You should not rely on your memory, you should build it into the script." KILL live instances => wait 40s idle => flash tiny toast => restart. If instances are ALREADY DEAD, restart immediately (no idle wait). The tool is the ONLY way to restart typer.
- **Toast**: Small bottom-right corner label "typer updating..." - does NOT steal focus, does NOT block the screen (Max rejected the full-screen amber flash).
- **Rule saved to global2.md** so every future session enforces it.

### 10. Chime volume halved (?0.35 fixed)
- **Why**: Max said it was too loud. Removing COM also removes the ability to follow the Windows volume slider, so the chime plays at a fixed quiet level (0.35 gain). Winsound plays on the default device only.

---

## CURRENT STATE - what is live and working

All committed and deployed via safe restart. **7 instances running** (no daemon - the auto-deploy daemon was disabled and stays off):

| Key | Function | Engine | Language |
|-----|----------|--------|----------|
| **F9** | English | local large-v3 | EN |
| **Num+** | English | local large-v3 | EN |
| **Num4** | Race (fast) | local + OpenAI, fastest wins | EN |
| **Num2** | English cloud | Deepgram | EN |
| **Num6** | Russian cloud | OpenAI | RU |
| **Num8** | Playback/mic-monitor | (record+play, no transcription) | - |
| **Num0** | Russian remote | Asto server | RU |
| **Right Ctrl** | Russian remote | Asto server | RU |

**NumLock state**: OFF permanently (nav mode). NumLocker disabled. Numpad 1/7/9/3/5 are Max's navigation keys (End/Home/PgUp/PgDn).

**Key mechanics**: All numpad buttons fire from numpad nav codes (non-extended), so they work regardless of NumLock. Real dedicated arrow/home/end keys pass through.

**Crash status**: Proven fixed - 2 days of uptime with zero crashes after COM removal (winsound chime).

---

## EXACT NEXT STEP

The **persistent big-font last-10-seconds display on the meter overlay** - this was Max's ORIGINAL top-priority request at the very start of the session (before all the crash drama). It was built and tested (the preview flashed on screen for Max to see), then **wiped out in the big revert**, and never re-added. Max was told about this at the end: "Your very first request - the persistent last-10-seconds display on the meter bar - got built, then wiped out in the big revert, and I never re-added it or told you. It's gone right now."

The feature spec (from the original build that was wiped):
- Module-level deque in `meter_e25c.py` holding the last 10 transcription durations (whole seconds)
- Space-separated display, right = most recent
- Big font, top-center overlay (separate from the thin green progress bar)
- Also shows race winners as colored letters: L (local, teal) / O (OpenAI, orange), right = most recent
- Stays visible for 5 seconds after each dictation, then fades

This should be re-implemented in `meter_e25c.py` and wired to `typer_e25c.py` (worker feeds duration + race winner to the meter on each successful delivery). No COM. No touching the chime. No universal/auto-language. Just the display.

---

## OPEN QUESTIONS AWAITING MAX

- **Num5 is free** - Max mentioned it as a candidate for a test button earlier. Could host something experimental.
- **Grok and Asta in the race** - Max explicitly deferred: "???????? ? ??????... ????? ??????????? ??????? ??????? ???????, ?????? ?? ???????????. ????? ????????????, ????? ??? ?????." So adding Groq/Asta to the race is paused until the current race proves stable.
- **E35C coordination** - another session (LightShot print screen hotkeys) was coordinating with this one via the branch bulletin board. E35C's root cause was Windows Snipping Tool hijacking Print Screen - no conflict with typer. This handover session replied to E35C confirming no conflict. No further action needed unless E35C posts again.

---

## KEY FILE PATHS

- `C:\claude_base\tools\typer\typer_e25c.py` - **THE core tool (~2400 lines).** All logic lives here.
- `C:\claude_base\tools\typer\meter_e25c.py` - Tkinter canvas overlay (thin green bar + the-to-be-re-added summary panel).
- `C:\claude_base\tools\typer\start_typer_all.bat` - Canonical launcher (7 instances, no daemon).
- `C:\claude_base\tools\typer\restart_typer_safe.py` - Safe restart tool (waits 40s idle, shows tiny toast, THEN kills+relaunches). **ALWAYS use this to restart typer - never Stop-Process directly.**
- `C:\claude_base\tools\typer\tiny_toast.py` - Tiny bottom-right corner toast ("typer updating...") used during safe restart.
- `C:\Users\maxre\my_keys.html` - Desktop cheat sheet (kept in sync).
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - Auto-loaded session rules (contains the restart-typer-idle rule).
- `C:\claude_base\branch_bulletin` - Cross-session coordination board (used for E35C messaging).
- Runtime logs: `C:\claude_base\tools\typer\typer_runtime_e25c_*.log`
- Crash logs: `%TEMP%\typer_crash_*.log` (faulthandler writes exact crash line here)
- Dictation log: `C:\Users\maxre\Downloads\typer_dictation_log.txt`
- Env file for API keys: `C:\claude_base\tools\typer\.env`
- Venv: `C:\claude_base\tools\typer\venv\Scripts\pythonw.exe`
- Worklog: `C:\claude_base\compaction_kb\scripts\worklog.py log "..."` (used to persist checkpoints)

---

## GOTCHAS AND DEAD ENDS RULED OUT

### RULED OUT (do not repeat)
- **Any COM whatsoever** - pycaw, SoundCard/WASAPI, CoCreateInstance. All cause `_ctypes.pyd 0x91bd` crashes. Use winsound for audio, no COM for anything.
- **Silence trimming in Whisper** - Max FORBADE it ("???????? ????????? ?????? ? ?? ????????"). Use `condition_on_previous_text=False` only.
- **Full-screen flashes** - Max rejected them ("flashing on screen is idiotic, I want to keep doing other work"). Use the tiny corner toast or just the meter indicator.
- **Auto-deploy daemon** - disabled and stays off. It silently broke buttons (Num0).
- **Race on Num+ or any primary button** - keep experiments isolated to dedicated keys (num4).
- **Universal/auto-language on a live button** - the clamped en-vs-ru auto-detect worked but caused confusion (mixed-language sentences got the wrong language locked in by the first word). Not re-added; would need separate testing.
- **NumLock dependency** - permanently solved by binding to numpad nav codes with extended-key filtering.
- **Restarting typer mid-dictation** - the safe restart tool enforces 40s idle wait. Never `Stop-Process` typer instances directly.
- **`git add -A`** - Max was burned by a ~600MB accidental commit earlier. Always stage files by name.
- **NumLocker** - disabled (autostart shortcut renamed to `.disabled`).

### CURRENT GOTCHAS
- **Cold start on local-only buttons (F9/Num+)**: ~15 seconds on first press after a restart while large-v3 loads into GPU memory. Max knows and accepts this ("?????????, ???????? ?????? ??? ?????? ????? ??? ?????? ?????? ??????"). The pre-warm now defers 5 minutes after idle rather than at startup.
- **Whisper hallucination**: The cleaner strips known subtitle phrases, but there may be new ones that appear. Max should report exact text when it happens so the cleaner's regex can be expanded.
- **NumLock state**: System is designed for NumLock OFF permanently. If NumLock somehow gets turned ON (e.g., BIOS reset, Windows update), the numpad digit codes will conflict with the nav-code bindings and buttons may misbehave. The fix handles both states, but it's designed for OFF.
- **Meter bar disappearing after long uptime**: The overlay windows can get orphaned by monitor sleep/reconnect (happened after ~2 days). A restart rebuilds them. This is a known Tkinter limitation, not a crash.
- **Chime doesn't play on laptop speakers**: Only on the dock speaker and USB mixer. The Realtek audio device rejects the winsound format (error 0x88890004). Max accepted this.
- **Race winner HUD was part of the wiped feature**: The summary panel (durations + race-winner letters) was part of the reverted HUD. When re-adding the last-10-seconds display, remember to also restore the race-winner letters (L/O).

---

## BUTTON LAYOUT (current, NumLock OFF = nav mode)

```
numpad:
  Home(7)  Up(8?playback)  PgUp(9)
  Left(4?race)   5(free)   Right(6?Russian)
  End(1)   Down(2?Deepgram)  PgDn(3)
           Ins(0?Russian-asto
