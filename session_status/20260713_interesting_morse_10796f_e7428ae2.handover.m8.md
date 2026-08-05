# Scribe handover - milestone 8 (~601K tokens)
# session: 20260713_interesting_morse_10796f_e7428ae2
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-13 11:49:59 by deepseek-v4-pro

# HANDOVER - typer voice-dictation session (E25C)

---

## GOAL (in Max's words)

Build and refine a multi-button voice-dictation tool. Key directions from this session:

1. **Race mode** (local large-v3 vs OpenAI whisper-1, fastest wins) on a dedicated button - currently **Num+/F9**.
2. **Persistent race-comparison HUD** overlay showing the last ~10 dictation times for BOTH engines (local row + OpenAI row), with the **winner boxed**, so you can visually see which engine overtakes which. This was the original "last 10 seconds" request evolved into a two-row race leaderboard.
3. **NumLock-independence** - buttons must work regardless of NumLock state, while preserving Max's nav keys (Home/End/PgUp/PgDn, including num1=End).
4. **Playback/mic-monitor button** on num8 - record, then play back to hear your own mic, no transcription.
5. **Whisper hallucination cleanup** - strip trailing subtitle-stamps ("??????????? ???????", "???????", "subtitle by...") and solo hallucinated words ("???????", "thank you", "you") only when they're the entire output.
6. **Crash-proofing** - the tool kept dying after ~1 hour of use. Root cause was COM audio (pycaw volume-read + SoundCard WASAPI chime). Both ripped out. Chime now uses `winsound` (pure Win32, zero COM).
7. **Safe restart discipline** - never kill/relaunch typer while Max is dictating. Enforced via `restart_typer_safe.py`, which waits **40 seconds** of dictation-idle, then shows a tiny corner toast ("typer updating..."), then swaps the build.
8. **Mic follows Windows default** - each recording after a pause picks up the current Windows default microphone (PortAudio was caching old mic and never re-checking).

---

## DECISIONS + WHY

### Crash fix - COM removal
- **Symptom:** all buttons died after ~1 hour of heavy use. Windows WER log showed `_ctypes.pyd 0x91bd` access violation - a native COM crash that `try/except` can't catch, so the process silently vanished.
- **Diagnosis stages:** First blamed pycaw master-volume read (removed it, crashes continued). Then identified SoundCard's WASAPI chime fanout as the second COM path (removed it, replaced with `winsound`).
- **Result:** Zero crashes for ~2 days straight after the winsound switch. 7 instances alive continuously. Crash proven fixed.
- **Trade-off:** Chime no longer follows the volume knob - plays at a fixed quiet level (~0.35). Max accepted this. Chime also no longer fans out to all speakers - plays on default device only.

### Race button isolation (num4, then swapped to Num+/F9)
- Max wanted the race tested on a **separate, free button** so it couldn't kill his working buttons. Built on num4 (English, local + OpenAI), then later swapped with Num+ at Max's request so his main button gets the fast race.
- **Race logic:** fires local large-v3 and OpenAI whisper-1 in parallel threads. First engine to return **non-empty** text wins - immediately submitted, no waiting for the loser. If the first engine returns empty (hallucination/error), falls back to the slower one.
- **Why no auto-language in the race:** we tried it earlier in the session; the auto-detect adds complexity and the race got reverted during the crash saga. Max hasn't asked to re-add it to the race - currently the race is **English-only**, and auto RU/EN detection lives on **Num4** (plain local, no race).

### NumLock independence
- **Root cause of "buttons dying":** NumLocker was actively holding NumLock OFF. When NumLock is OFF, numpad 2/4/6/8/0 send arrow/nav codes instead of digits, so typer never saw them.
- **Max's preference:** NumLock stays OFF permanently (nav mode) so Home/End/PgUp/PgDn (7/1/9/3) always work - including num1=End which he uses.
- **Fix:** Disabled NumLocker (autostart lnk renamed to `.disabled`, registry `InitialKeyboardIndicators` set to 0 so NumLock boots OFF). Typer now catches **numpad nav codes** (non-extended Down=0x28, Left=0x25, Right=0x27, Up=0x26) and maps them to their digit talk-keys. The extended-key flag distinguishes numpad arrows from dedicated arrow keys - real arrows pass through untouched.
- **Num0 (Russian asto):** needs both NumLock-ON (0x60) and NumLock-OFF (Insert/0x2D) codes - already dual-bound in the launcher.

### Hallucination cleanup
- Two categories of Whisper hallucination:
  1. **Trailing subtitle stamps** (only from the end of text): "??????????? ???????", "??????? ?? ????????", "???????? ??????...", "thanks for watching", "subscribe...", etc.
  2. **Solo hallucination** (only when it's the ENTIRE output): "???????", "you", "thank you" - these appear when Max presses the button for <1 second and the model fills silence with a memorized word.
- Applied in `_clean_hallucinated_text()` before delivery. Does NOT trim silence from audio (Max explicitly forbade this earlier).

### Playback button (num8)
- Replaced Groq on num8. Toggle: first press records, second press stops ? plays the audio back via `winsound` (no COM). No transcription, no typing.
- Escape stops the playback while it's playing.

### Mic refresh
- PortAudio caches the device list at init. Even `_stream_healthy()` only checked the cached index. Now `_refresh_mic()` re-initializes `sounddevice` entirely after 3+ seconds of idle, so it picks up a Windows default-mic switch. Opening words preserved.

### Safe restart tool (`restart_typer_safe.py`)
- Replaces manual `Stop-Process` + relaunch. Logic:
  - Check owner file + process list: if **all dead** ? restart immediately. If **alive** ? wait 40s of dictation-idle (no owner transitions to "rec"), then show tiny Tkinter toast bottom-right ("typer updating..."), kill all, relaunch 7 instances.
  - The toast is non-blocking, no focus steal - Max said the full-screen amber flash was "idiotic" because he's working on other things during updates.
- This is now the **only** way typer restarts. Rule saved in `global2.md` (loaded every session).

### Meter overlay crash-proofing
- The race-comparison panel is rendered inside the meter Tkinter overlay (`meter_e25c.py`). All rendering is wrapped in `try/except` so a panel glitch can never freeze the main meter bar.

---

## CURRENT STATE

### What is deployed and running RIGHT NOW
- **7 typer instances** alive (since ~11:29), stable no-COM build.
- Button layout:
  - **Num+/F9** ? English RACE (local + OpenAI, fastest wins)
  - **Num4** ? auto RU/EN local (language-detect, no race)
  - Num2 ? Deepgram English
  - Num6 ? Russian OpenAI
  - Num8 ? playback/mic-monitor (replaced Groq)
  - Num0 ? Russian asto (remote)
  - Right Ctrl ? Russian asto (remote)
- **NumLocker disabled**, NumLock OFF permanently.
- **Safe-restart tool** alive and enforcing the 40s idle rule.

### What is queued for deploy (safe-restart waiting for 40s idle)
The latest commit includes:
1. **Race-comparison HUD** - two-row panel (local teal / OpenAI orange), last ~10 races, winner boxed per column, appears top-center for 5 seconds after each dictation on the race button.
2. **Per-leg race logging** - each engine now logs its own time + OK/EMPTY status. Empty legs show as e.g. "2.3e" in the table so Max can see when a faster engine returned nothing (this explains why the table "looked like picking slower").
3. **Crash-proof panel guard** - all rendering in try/except.

**The safe-restart has been waiting since ~11:33 but Max has been dictating continuously and never paused for 40 seconds.** Max saw the panel only once - that was a test render of mine. The real panel will appear after his next 40+ second pause, when the toast flashes and the build swaps.

---

## EXACT NEXT STEP

1. **Max pauses dictation for 40+ seconds** - the amber "typer updating..." toast appears, instances reload with the new HUD build.
2. **Max dictates a few times on Num+** - the race-comparison panel should appear top-center for 5 seconds after each dictation.
3. **Max evaluates the panel:** wants it bigger? different colors? more/fewer than 10 races? decimals or whole seconds? The panel is currently whole seconds, no decimals.
4. **Verify the "picked slower" issue:** with the new per-leg logging, if a faster engine returned empty (e.g. "2.3e"), that explains the fallback. Max can see it directly on the panel now.
5. **Open question pending:** does Max want Russian back on his main button (Num+/F9)? Currently the race is English-only. Adding auto-language detection to the race requires re-adding the clamped detect step before the race fires - adds complexity but we proved it worked earlier.

---

## OPEN QUESTIONS (awaiting Max)

1. **Race + auto-language on main button?** Right now Num+/F9 is English-only race; Num4 is auto RU/EN (no race). Max hasn't decided whether to merge them.
2. **Panel styling** - size, colors, decimals, number of columns (currently 10).
3. **Chime level** - currently fixed at ~0.35. Max asked for "2x quieter" and got it, but hasn't confirmed it's right.
4. **Asta in the race?** Max said he wants to add Groq and Asta as third engines later, after the current simple race is tested. Parked.
5. **Groq button** - was on num8, replaced by playback. Does Max want Groq moved somewhere else or dropped entirely? Not asked.

---

## KEY FILE PATHS

| File | Purpose |
|------|---------|
| `C:\claude_base\tools\typer\typer_e25c.py` | Core tool (~2000 lines). All logic: recording, transcribe engines, race, chime, hook, etc. |
| `C:\claude_base\tools\typer\meter_e25c.py` | Tkinter canvas overlay - the green bar + new race-comparison HUD panel |
| `C:\claude_base\tools\typer\start_typer_all.bat` | Canonical launcher. Launches all 7 instances. No auto-deploy daemon. |
| `C:\claude_base\tools\typer\restart_typer_safe.py` | Safe restart tool - waits 40s idle, shows toast, relaunches. THE ONLY way to restart typer. |
| `C:\claude_base\tools\typer\tiny_toast.py` | Small corner toast window - shows "typer updating..." during restarts, never blocks focus |
| `C:\Users\maxre\my_keys.html` | Desktop cheat sheet - kept in sync with current button layout |
| `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` | Always-loaded rules - contains the 40s-idle restart discipline |

**Instances run via:** `C:\claude_base\tools\typer\venv\Scripts\pythonw.exe` (fully detached, no console)

**Crash logs:** `%TEMP%\typer_crash_*.txt` - faulthandler dumps (empty headers mean no crash; actual dump means a hard fault with the exact line).

**Dictation log:** `C:\Users\maxre\Downloads\typer_dictation_log.txt` - delivered text only, timestamps, leaderboard-ready.

---

## GOTCHAS

1. **Never `git add -A`** - a previous session committed ~600MB of CUDA wheels, blocking all pushes. Stage files by name.
2. **Never restart typer directly** - always use `restart_typer_safe.py` or run it through the safe restart. The 40s idle rule is enforced in global2.md and the tool itself.
3. **NumLock must stay OFF** (Max's nav keys depend on it). Typer now catches numpad nav codes, not digits. If someone turns NumLock ON, numpad 2/4/6/8/0 will stop working (the hook maps nav codes, not digit codes).
4. **Race is English-only** - not auto-language. If Max dictates Russian on Num+, it forces translation to English (same as old bug). The auto-language race was reverted. Auto RU/EN is on Num4 (no race).
5. **First dictation after a restart is slow on local** (~15s GPU model load). The race protects against this on Num+ (OpenAI wins while local warms), but Num4 (auto-local) and F9 (plain local) still pay the cold start. There's a deferred warm-up (5 min idle) in the code, but it may not be deployed yet.
6. **Chime is winsound-only** - plays on the default audio device only, fixed volume. Will not fan out to docking station speakers or USB mixer as before.
7. **Hallucination cleanup is regex-based** - if Max sees a new hallucination phrase slip through, the trailing phrase list in `_clean_hallucinated_text()` needs that phrase added.
8. **The race panel HUD is NOT YET DEPLOYED** - it's committed and waiting in the safe-restart queue. Max saw my test render, not the live version. It deploys on his next 40-second pause.
9. **Empty engine fallback** - if the faster race engine returns empty text (hallucination/silence), the slower engine's text is used instead. The new panel marks empty legs with "e" so this is visible.
