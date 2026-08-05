# Scribe handover - milestone 6 (~451K tokens)
# session: 20260712_interesting_morse_10796f_e7428ae2
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-12 21:22:38 by deepseek-v4-pro

# HANDOVER - typer voice-dictation tool (Max's multi-button system)

## GOAL (in Max's own words)
"????? ?????? ????? ????? ?? ?????-?? ?????? ??????. ?? ????, ?? ?????? 1 ??? 3. ???????... 1, 7, 3 ???????."
Max wants a **race** (local large-v3 vs. OpenAI whisper-1, fastest wins) on a **separate key** (Num1) so that the crash-prone experiment does **NOT** affect his working buttons (Num+, F9, Num0, etc.). Earlier, a universal/race attempt broke everything and was fully reverted. Now that the crash root cause (COM in chime) is definitively removed, he's willing to test the race again, but **isolated**.

## DECISIONS MADE + WHY

1. **All COM removed from typer (the definitive crash fix)**
   - **Problem:** All typer instances silently died after ~1 hour (hard crash in `_ctypes.pyd`, offset `0x91bd`). Restarting didn't help because the faulting code remained.
   - **Diagnosis:** Two COM paths: `pycaw` (reading Windows master volume for chime) and `SoundCard` (WASAPI playback for multi-speaker chime fanout). Both triggered access violations.
   - **Fix:** Replaced the chime entirely with `winsound` (pure Win32, zero COM). Removed all `pycaw`/`SoundCard`/COM calls.
   - **Proof:** 2+ days of uptime with zero crashes after the fix. Crash recorder (`faulthandler`) is armed and confirmed no further faults.

2. **Safe restart discipline built into a tool (not relying on memory)**
   - **Rule:** Never kill/relaunch typer while Max is dictating. If processes are alive ? wait **40 seconds of dictation-idle** before restarting; if dead ? restart immediately.
   - **Implementation:** `restart_typer_safe.py` polls `_last_use_ts` from the owner file; waits for 40s silence; flashes a **tiny non?blocking toast** ("typer updating...") for ~12s during the restart; then relaunches all. The tool is used by all future sessions. No full?screen flash (Max found it intrusive - he watches the indicator bar).
   - **Persisted in** `global2.md` so every session knows.

3. **Hallucination stripping (subtitle-filler)**
   - **Problem:** Russian transcripts ended with "??????????? ???????...", "??????? ?? ????????", "???????? ?????? DimaTorzok" etc. English ones got "thank you", "you".
   - **Fix:** Added `_strip_hallucinations(text)`:
     - **Trailing only** (anywhere at the end of the string): a list of filler patterns (Russian and English).
     - **Whole?string only** (if the entire transcript is just one word/phrase): "???????", "you", "thank you" ? replaced with empty.
   - **Tested with real examples**, verified not to touch genuine mid-text usage.

4. **Race re-added on Num1 only (isolated experiment)**
   - Minimal re?add of the race engine (`"race"` provider in `STT_ENGINES`, `_race_transcribe` function that fires local and OpenAI in parallel, returns the first result). No auto-language, no HUD, no other changes.
   - Attached to **numpad 1** (`--key num1 --provider race --lang en`). It fires only when NumLock is ON (standard digit code `0x61`).
   - **Commit** contains the code + launcher line + cheat sheet update. It is **NOT yet deployed** - the safe restart tool will deploy it on the next 40?second idle.

5. **NumPlus (your main button) stays local-only, no race**
   - The crash?era revert turned NumPlus back to pure local (large-v3 English). Max explicitly forbids re?adding the race to NumPlus because he associates it with the prior breakage. That's final.

6. **Chime loudness halved**
   - After the COM fix, the chime still played too loud. Reduced the fixed gain from `0.35` to half (`0.175`) or similar - now quiet. User still may want it even quieter; value is in code comment.

## CURRENT STATE

- **All 7 instances running:**
  - F9 / Num+ ? English local large-v3
  - Num0 ? Russian asto (remote, dual?binding to survive NumLock state)
  - Num2/4/8 ? English cloud (Deepgram/OpenAI/Groq)
  - Num6 ? Russian OpenAI
  - Right Ctrl ? Russian asto
  - (Num1 race is **not running** - waiting for idle restart.)

- **Crash-free for 2+ days**, zero faults since the winsound fix.

- **Meter/indicator bar** may be missing because monitor sleep/reconnect orphaned the overlay (processes alive). A restart will rebuild it.

- **NumLock:** The user reported that NumLocker works fine now; no further action.

- **Cheat sheet (`my_keys.html`)** is updated for the race on Num1; Num+ is correctly labeled as English local.

- **All code committed and pushed**, clean git history (no `git add -A`).

## EXACT NEXT STEP

1. **Wait for the safe restart to complete** (triggered after 40s idle). It will flash "typer updating..." as a tiny toast, then relaunch with the race on Num1.
2. **Test Num1** after the restart: should be fast (OpenAI wins on first press, local takes over later). Confirm it works during the session.
3. **Check indicator bar** reappears on both screens after restart. If not, investigate meter overlay window creation.
4. **Observe** whether "??????????? ???????" ever slips through again on Russian buttons (the cleaner should strip it). If seen, capture the exact text and extend the pattern list.

## OPEN QUESTIONS (awaiting Max)

- If Num1 race works well, should we add a similar race for **Russian** (local + OpenAI Russian, or asto?) or keep it only English?
- Should the race include **more than two engines** in the future (Groq, asto)? Currently agreed to keep it simple for testing.
- Should the chime volume be further reduced or tuned?
- Should the NumLock dependency be removed entirely by adding dual?bindings (digit + nav code) to all numpad buttons, so NumLock state never matters? (Max can decide later.)

## KEY FILE PATHS

- `C:\claude_base\tools\typer\typer_e25c.py` - core tool (all transcription logic, race, hallucination cleaner, winsound chime, safe?restart?aware).
- `C:\claude_base\tools\typer\start_typer_all.bat` - launcher (instances with flags). Line for Num1 race added.
- `C:\claude_base\tools\typer\restart_typer_safe.py` - the idle?waiting restart discipline tool. Must always be used.
- `C:\claude_base\tools\typer\meter_e25c.py` - overlay meter (thin bar, not yet showing last?10 seconds; that feature was lost in revert).
- `C:\Users\maxre\my_keys.html` - desktop cheat sheet.
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - contains the persistent rule for restart only when idle.
- Crash logs per instance: `%TEMP%\typer_crash_*.txt` (armored with `faulthandler` - only grow if a fault occurs).
- Owner file: `%TEMP%\typer_recording_owner.txt`

## GOTCHAS / DEAD ENDS

- **Never use COM in the tool.** `pycaw`, `SoundCard`, any COM audio API cause the `_ctypes.pyd 0x91bd` crash. Chime is now `winsound` only.
- **Never restart typer while user is dictating.** Always use `restart_typer_safe.py`; it enforces the 40?second idle wait. Do NOT `Stop-Process` directly.
- **Never `git add -A`** - stage files by name.
- **Auto-deploy daemon** is permanently OFF (it broke Num0 and was hated). Do not revive.
- **Silence trimming** is forbidden (Whisper hallucination fix must never touch audio).
- **Extended key flag** distinguishes main Delete vs. Numpad decimal - do not confuse them.
- Num1 and all numpad digits require **NumLock ON** to work. If user reports button dead, first check NumLock state.
- **Race was reverted earlier** not because it caused crashes but because the whole experimental branch was rolled back. The crash cause was COM, not race. So race is safe now (zero COM).
- The **persistent big?font display of last-10 durations** was lost in revert; user mentioned it but then other issues took over. It's not currently implemented; may be revisited later.
