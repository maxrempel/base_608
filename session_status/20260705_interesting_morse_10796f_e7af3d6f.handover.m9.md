# Scribe handover - milestone 9 (~676K tokens)
# session: 20260705_interesting_morse_10796f_e7af3d6f
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-05 22:31:19 by deepseek-v4-pro

# ? Session Handover - Typer E25C (Max's dictation tool)

## GOAL (in Max's words)
Max wanted a reliable, fast voice-dictation tool that "just works." He wanted English and Russian, click?to?start / click?to?stop (double-click), a chime that plays on all speakers but follows the Windows volume slider, cross?instance coordination so pressing any key stops the current recording, and a global recall of the last dictation from any key. By the end he said "??? works fine" and the last fix was to make the chime follow the volume control.

## DECISIONS MADE AND WHY
1. **Local GPU beats cloud** - After testing Groq, Deepgram, and OpenAI on the same day, all cloud providers had unpredictable server?queue delays (0.3s - 13s). Moving to Whisper large?v3 on Pine's own NVIDIA T1200 GPU gave consistent ~2?6s transcription. Russian stayed on asto (CPU) or OpenAI for speed when asto was busy.
2. **Double?click over hold?to?talk** - Max trained himself on click?to?start / click?to?stop. All 7 instances now use double?click except F9 (intentionally kept as hold for legacy). This eliminated the "phase reversal" confusion.
3. **One mic at a time** - Because all instances run from the same code, multiple talk keys could conflict. The fix uses a shared owner file (`typer_recording_owner.txt` in TEMP) so that pressing a different talk key stops the previous recording without starting a new one. This solved the "plus intercepts" problem.
4. **Global recall** - Double?tap Numpad `.` (or Alt+key) now reads a shared global?last file (`typer_global_last.txt`) rather than per?instance memory. This ensures the last dictation from *any* key can be recalled. Only one instance (the English one) listens for the dot, to avoid duplicate pasting.
5. **Chime evolution** - After many failures (simultaneous playback, sampling?rate mismatches), the final solution uses the SoundCard library to enumerate physical speakers, plays sequentially, and scales the audio by the system master volume read via `pycaw`. It now follows the Windows volume slider.
6. **Escape cancels transcription too** - Previously only stopped recording; now also aborts in?flight STT tasks (via an `_transcribing` counter and epoch?based discard).
7. **Mic hot?swap resilience** - On each recording start, the script compares the current default device name to the one the stream was opened with. If they differ, it closes the old stream and opens the new one. This prevents a total wedge when the mic is unplugged or switched.
8. **Instant paste (spit)** - Switched from keystroke animation to clipboard paste via `--paste`, with Win+V history exclusion and prior clipboard restoration. Instant, no speed issue.
9. **No 90?second cap** - The old runaway safety cut off dictations at 90s; raised to 30 minutes (virtually unlimited for normal speech).

## CURRENT STATE
All code is committed and pushed to master. 7 instances are running on Pine from the canonical launch script `start_typer_all.bat`:

| Key | Language / Engine | Mode |
|---|---|---|
| **F9** (hold), **Numpad+** (double) | English, local large?v3 GPU | hold / double |
| **Numpad 1** | English, OpenAI whisper?1 | double |
| **Numpad 2** | English, Deepgram nova?3 | double |
| **Numpad 9** | English, Groq whisper?large?v3 | double |
| **Numpad 0 / Insert** | **Russian, OpenAI whisper?1** | double |
| **Numpad 3** | Russian, asto CPU large?v3 | double |
| **Right Ctrl** | Russian, asto CPU large?v3 | double |

All share: instant paste, chime (system?volume?aware), mic name on green bar, 20?min mic warm, cross?instance coordination, global recall, Escape cancels everything.

GPU: ~2255 MiB used of 4096 MiB (plenty free). ASTO server is up (IP `100.83.187.123:8123`), running large?v3 via `typer_stt_server.py`.

Startup is reboot?safe. A desktop "Restart Typer" shortcut runs `restart_typer.py`, which snapshots live instances and re?launches them; if none are alive it falls back to `start_typer_all.bat`.

The `typer_dictation_log.txt` file in Downloads records every utterance with timestamps.

## EXACT NEXT STEP (awaiting you, no action needed now)
Everything is stable. There are no urgent pending tasks. When you return:
- Confirm the chime volume is good (the last change scaled it to master volume).
- If the intermittent GPU slowness (one call every ~15 minutes) reappears, the log will now dump `SLOW?LOCAL diagnosis:` with the guilty process. That instrumentation is armed.
- You may want to settle on an English "winner" among the cloud/local buttons - currently local large?v3 is the primary, but all four are live for easy A/B comparison.

## OPEN QUESTIONS STILL AWAITING YOU
1. Is the chime volume on the laptop speaker acceptable now that it follows the system slider?
2. Which English engine do you want as the default for daily driving? (Local is already on your main keys.)
3. Do you want to retire any of the cloud backup buttons (now that they're rarely used) or keep the full set?

## KEY FILE PATHS, IDs, COMMANDS
- **Main code:** `C:\claude_base\tools\typer\typer_e25c.py`
- **Meter UI:** `C:\claude_base\tools\typer\meter_e25c.py`
- **Startup launcher:** `C:\claude_base\tools\typer\start_typer_all.bat`
- **Restart script:** `C:\claude_base\tools\typer\restart_typer.py` (and desktop shortcut `C:\Users\maxre\Desktop\Restart Typer.lnk`)
- **Dictation log:** `C:\Users\maxre\Downloads\typer_dictation_log.txt`
- **Desktop cheat sheet:** `C:\Users\maxre\Desktop\my_keys.html` (also `typer_commands.md`)
- **Chime audio file:** `C:\claude_base\tools\typer\sounds\chime_done.wav`
- **ASTO server:** `http://100.83.187.123:8123`, service `typer-stt.service`, model at `/home/rempel/typer_stt/models/large-v3`
- **API key files:**
  - Groq: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/groq_api_key_20260611.txt`
  - Deepgram: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/deepgram_key_20260515.txt`
  - OpenAI: `.env` file next to `typer_e25c.py` (contains `OPENAI_API_KEY=sk-proj-...`)
- **Recording coordination temp file:** `%TEMP%\typer_recording_owner.txt`
- **Global recall temp file:** `%TEMP%\typer_global_last.txt`
- **GPU diagnostics:** `pynvml` used within `typer_e25c.py`; slow?call logging is triggered when >8s.

## GOTCHAS AND DEAD ENDS ALREADY RULED OUT
- **Phase?reversal / focus theft** - Fixed with Escape hard reset and improved watchdog (disabled for suppressed keys).
- **Double?Delete misfire** - Main?keyboard Delete accidentally triggered recall. Fixed by checking the extended?key flag to distinguish numpad dot.
- **Chime not on laptop speaker** - Multiple attempts: simultaneous playback overloaded audio subsystem; WASAPI sample?rate mismatch; auto?mute not our problem. Final solution: SoundCard sequential fan?out with pycaw volume scaling works.
- **90?second dictation cutoff** - Removed; now effectively unlimited.
- **Hold?to?talk chopped after 300ms** - The "any?key?stops?toggle" rule was accidentally active during holds. Fixed by gating to double?click mode only.
- **Cross?instance recording conflict** - Solved with a shared owner file; pressing any talk key stops the running one.
- **History rewrite from accidental large file** - A `git add -A` pulled in 570MB of throwaway wheels. Cleaned safely with filter?branch after stashing other sessions' WIP, preserving all commits.

---

*Everything is committed, pushed, and running. Enjoy.*
