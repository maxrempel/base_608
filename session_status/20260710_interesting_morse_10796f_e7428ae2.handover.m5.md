# Scribe handover - milestone 5 (~378K tokens)
# session: 20260710_interesting_morse_10796f_e7428ae2
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-10 11:36:42 by deepseek-v4-pro

# HANDOVER: typer - Claude Code Session Continuation

---

## GOAL (in Max's own words)

Max is building his personal multi-button voice-dictation tool ("typer"). The most recent active direction:

1. **The indicator bar (meter overlay) is gone on both screens** - this is the current problem to fix. The safe-restart is already queued and waiting for 40s of dictation-idle before rebuilding it.

2. **Earlier completed work:** Max wanted a "universal button" that auto-detects Russian vs English (clamped to only those two, never random 3rd languages) and races local large-v3 against OpenAI whisper-1. This was built, worked for ~15 minutes, then caused crashes. It was fully reverted to the clean pre-experiment working version. Max wants to bring back auto-language-detection later on a **separate, free key** (Num5 suggested) without breaking working buttons.

3. **The big crash hunt:** All typer buttons were dying after ~1 hour of use, and restarts didn't help. The root cause was identified and appears fixed - the COM audio path (SoundCard WASAPI chime) was replaced with pure Win32 winsound. The fix has survived ~2 days with zero crashes.

---

## DECISIONS MADE + WHY

### 1. Race/universal button - REVERTED (commit `c2d076d8` restored)
- **What it was:** F9/Num+ became a "race" button - auto-detect RU/EN (clamped to those 2 only), then fire local large-v3 + OpenAI whisper-1 in parallel, land the fastest result.
- **Why reverted:** It caused frequent crashes (COM-related), and Max was losing working dictation time. Max explicitly demanded: "Return to the previous working version and stop breaking what works."
- **Reverted to:** Separate language buttons - F9/Num+ = English local, Num0 = Russian asto, Num2/4/8 = English cloud, Num6 = Russian OpenAI, Right Ctrl = Russian asto. No race, no universal.
- **Max still wants auto-language-detection back** but on a separate free key (Num5), NOT by modifying working buttons.

### 2. COM removed entirely - THE crash fix
- **The crash:** Every dead instance showed `_ctypes.pyd` fault offset `0x91bd` - a native COM access violation that Python can't catch, so the process silently vanishes.
- **Two COM sources were removed:**
  - **pycaw (master volume read):** Was reading Windows master volume via COM to scale chime loudness. Removed - chime now plays at fixed level 0.35 (which Max wanted - "quieter").
  - **SoundCard (WASAPI playback):** The multi-speaker chime fanout used SoundCard's WASAPI via COM. Replaced entirely with `winsound` - pure Win32, zero COM.
- **Why this was hard to find:** The crash was rare-per-chime, so light use killed only heavily-used buttons; heavy use across all buttons made them all die. Both COM paths contributed. Max was told "fixed" twice before it actually was, because the first fix (pycaw) still left SoundCard COM in place.
- **Proof it's fixed:** Crash-recorder (`faulthandler`) was added. Buttons have run ~2 days (since 07-08 13:17) with ZERO faults. All 7 instances still alive.

### 3. Safe-restart tool built (`restart_typer_safe.py`)
- Max's rule: **never restart while he's dictating.** Built into a tool, not left to memory.
- Behavior: if instances are **dead** ? restart immediately; if **alive** ? poll for 40 seconds of dictation-idle, then restart.
- Shows a **tiny non-blocking corner toast** ("typer updating...") during restart - NOT a full-screen flash (Max hated the full-screen version: "don't block the screen, don't take over focus").
- The safe tool is what Claude should always use to restart typer.

### 4. Auto-deploy daemon - KILLED
- The daemon (`typer_auto_deploy.py`) that watched for code changes broke Num0 before. Max hated it. It's permanently disabled in `start_typer_all.bat`.

### 5. Chime volume - halved
- Max asked: "?????? ???? ? ??? ???? ????." Fixed level reduced to ~0.35.
- Chime plays on default device only (winsound limitation). Max noticed it doesn't play on laptop speakers (Realtek rejects the format), but plays on dock speakers + mixer - he said "?????? ?????????."

### 6. Meter summary panel - built and reverted
- A 5-second post-dictation summary HUD was built showing last-10 transcription durations (big font, right=newest) and race-winner history (L/O letters). It was **reverted** along with the race code. Max still wants this feature brought back.

### 7. Whisper anti-hallucination - `condition_on_previous_text=False`
- Max explicitly forbade silence trimming - "???????? ????????? ?????? ? ?? ????????."
- Hallucination fix is only `condition_on_previous_text=False`, no audio modification.

### 8. Git discipline
- **Never `git add -A`** - a ~600MB CUDA wheels commit blocked all pushes before. Stage files by name only.

---

## CURRENT STATE

### What's alive and working (7 buttons, all running since 07-08 13:17):
| Key | Engine | Language |
|-----|--------|----------|
| F9 | local large-v3 | English |
| Num+ | local large-v3 | English |
| Num0 | remote asto | Russian |
| Num2 | Deepgram | English |
| Num4 | OpenAI | English |
| Num6 | OpenAI | Russian |
| Num8 | Groq | English |
| Right Ctrl | remote asto | Russian |

- Daemon: OFF
- Chime: winsound, quiet (~0.35 fixed level), default device only
- All instances: 2 days uptime, zero crashes
- Crash-recorder: armed (faulthandler writing to `%TEMP%\typer_crash_*.log`)

### What's currently broken:
- **The indicator bar (meter overlay) is gone on both screens.** Not a crash - the overlay windows were created 2 days ago and got orphaned when monitors slept/reconnected. Instances are healthy.
- The **safe-restart is already queued** - it's waiting for 40s of dictation-idle before rebuilding the bar.

### What was reverted (not present in current code):
- Race mode (local + OpenAI parallel)
- Universal/auto-language button
- 5-second summary HUD on the meter
- pycaw volume-following
- SoundCard multi-speaker fanout
- Auto-deploy daemon

---

## EXACT NEXT STEP

The safe-restart is already launched and polling. **When Max pauses dictating for 40 seconds**, it will:
1. Flash the tiny "typer updating..." corner toast
2. Kill all instances
3. Relaunch all 7 from `start_typer_all.bat`
4. The meter overlay bar should reappear on both screens

If the bar does NOT come back after the restart, the meter itself needs debugging (check `meter_e25c.py` overlay window creation).

After the bar is back, **the pending user request is:** bring back auto-language-detection on a **separate free key** (Max suggested Num5). This means:
- Add a new instance for Num5 with the clamped auto-detect (RU/EN only) + race (local + OpenAI)
- Do NOT modify the existing working buttons
- Test in isolation
- Only if stable, consider making it a replacement

---

## OPEN QUESTIONS (awaiting Max)

1. **Does Max want the auto-language + race on Num5 now**, or wait until after more testing?
2. **Should the summary HUD (last-10 seconds + race winners) come back** when the race returns?
3. **Chime volume** - is 0.35 quiet enough, or adjust further?
4. **What to do with the now-redundant Russian buttons** (Num0, Num6, Right Ctrl) if the universal button can handle both languages? Max called them "????????? ??????" but they're still running as backup.
5. **Chime on laptop speakers** - Max noticed it doesn't play on the Realtek built-in speakers. Worth fixing or fine as-is?

---

## KEY PATHS, IDS, NAMES

### Files:
- **`C:\claude_base\tools\typer\typer_e25c.py`** - the core tool (~2000 lines), all logic
- **`C:\claude_base\tools\typer\meter_e25c.py`** - Tkinter canvas overlay (indicator bar)
- **`C:\claude_base\tools\typer\start_typer_all.bat`** - canonical launcher (7 instances, no daemon)
- **`C:\claude_base\tools\typer\restart_typer_safe.py`** - safe restart tool (40s idle wait + toast)
- **`C:\claude_base\tools\typer\tiny_toast.py`** - non-blocking corner toast window
- **`C:\Users\maxre\my_keys.html`** - desktop cheat sheet
- **`C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`** - persistent rules loaded every session (contains the typer restart rule)
- **`C:\claude_base\tools\typer\venv\Scripts\pythonw.exe`** - Python runtime for instances

### Commits:
- `c2d076d8` - the clean pre-experiment working version (07-06 12:03)
- Latest commits reverted back to c2d076d8 base + COM removal + crash-recorder

### Instance identification:
- Each instance has `--key <name>` (e.g., `numplus`, `num0`, `f9`)
- Coordination via `%TEMP%\typer_recording_owner.txt` (prevents multiple instances recording simultaneously)
- Global last dictation: `%TEMP%\typer_last_dictation.txt`

### Crash forensics:
- Crash logs: `%TEMP%\typer_crash_<id>_<pid>.log`
- The fault was always `_ctypes.pyd` offset `0x91bd` = COM access violation
- Faulthandler is now armed in every instance (writes stack trace on SIGSEGV)

---

## GOTCHAS AND DEAD ENDS

1. **Never restart typer instances directly** - always use `restart_typer_safe.py` which waits for dictation-idle. Not a polite suggestion; it's enforced. The safe tool already handles the "dead vs alive" branching.

2. **COM is toxic in typer.** Both pycaw (volume) and SoundCard (WASAPI) caused hard crashes that Python can't catch. Any future audio feature must use pure Win32 (winsound) or a process-isolated approach, never COM from the main process.

3. **Auto-language detection works but has a cold-start cost.** The local large-v3 model takes ~15 seconds to load on first use after startup. The startup warm-up was set to 5 minutes idle-delayed (Max: "The start needs computer resources"). This needs to be brought back when auto-detect returns.

4. **NumLock state silently kills numpad buttons.** When NumLock is OFF, numpad digit keys send nav codes (arrows, Home, etc.) instead of digit codes. Typer only listens for digit codes, so buttons appear dead. NumLocker is supposed to hold NumLock ON. If numpad buttons "die" in the future, check NumLock state first.

5. **Whisper hallucination on short clips** - Max explicitly forbids silence trimming. The only anti-hallucination measure is `condition_on_previous_text=False`. Do NOT re-trim silence.

6. **Numpad-dot (recall) vs main Delete key** - both are VK 0x2E. The extended-key flag (bit 0x01) distinguishes them: main Delete has the flag, numpad decimal does not. This is already handled correctly, but it's fragile - don't change the dot-recall key detection.

7. **Auto-deploy daemon must stay OFF.** It broke Num0 silently before and Max explicitly rejected it.

8. **Chime doesn't reach laptop speakers** - Realtek rejects the winsound format (error 0x88890004). It plays on dock speakers and USB mixer. Not currently a problem per Max.

9. **Git: `git add -A` ruined a previous push** (600MB in sol_wheels/). Always stage by explicit file name.

10. **The meter overlay can orphan** after ~2 days of uptime (monitor sleep/reconnect). Rebuilding = a restart. This is a known minor issue, not a crash.
