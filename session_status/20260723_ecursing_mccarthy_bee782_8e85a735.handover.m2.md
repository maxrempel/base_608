# Scribe handover - milestone 2 (~180K tokens)
# session: 20260723_ecursing_mccarthy_bee782_8e85a735
# cwd: C:\claude_base\.claude\worktrees\recursing-mccarthy-bee782
# written: 2026-07-23 07:29:49 by deepseek-v4-pro

# Handover: Player 2 (Selection Player)

## GOAL (as Max stated it)
Max wants a "player 2" - a tool that does one thing: whatever text he selects on screen with mouse or keyboard, when he presses **Numpad 5**, that text is sent to FishAudio and read aloud in the default FishAudio male voice. It must be integrated with Typer 2's button family so Numpad 5 shares the same launcher and hotkey ecosystem as all the other typer buttons.

## DECISIONS MADE + WHY

1. **Standalone process, not inside typer_e25c.py**
   - Reason: The typer engine is huge, fragile, and Max hates restarting dictation. Adding any code there risked destabilising voice dictation. Instead, Player 2 is a small independent Python script that grabs Numpad 5 globally and never touches the typer engine.

2. **Button binding: Numpad 5**
   - Chosen because Max said button 5 was available and it would be "coupled to Typer 2". We verified no other button in the typer family uses Numpad 5.

3. **Startup integration: added to `start_typer_all.bat`**
   - That batch file already launches every typer process (dictation engine, extra buttons, etc.). Adding Player 2 there means it starts automatically on reboot and is conceptually part of the Typer 2 button set without needing a separate launcher.

4. **Audio pipeline: FishAudio HTTP API ? WAV ? sounddevice**
   - Reused the exact FishAudio endpoint and default male narrator voice (`reference_id` = `efc2f515-...`, the stock male voice from previous projects) that were already present in `yt_transcript_app.py`.
   - Requested WAV format so no ffmpeg is needed for playback. The raw audio bytes are read with soundfile and played with sounddevice, identical to how typer's Num8 playback button works.

5. **Behaviour: press to read, press again to stop**
   - First press of Numpad 5 sends the clipboard selection to FishAudio and plays it. If playback is active, a second press stops it immediately. This avoids needing a separate stop button and matches Max's preference for simple toggles.

6. **Tray icon**
   - A small orange "P2" system-tray icon is shown while Player 2 is running. Right-click offers Quit. This gives visibility and a clean exit path without hunting processes.

7. **No restart required**
   - The edit to start_typer_all.bat was made while the typer engine was live, so no dictation was interrupted. Player 2 is a separate process and its launch won't disrupt anything.

## CURRENT STATE

- **Player 2 is running right now** (launched during the session via `pythonw.exe`). It has a tray icon and is listening for Numpad 5 globally.
- The FishAudio call was tested in isolation: a short phrase was converted to WAV and saved successfully. The male voice rendered correctly.
- Playback (sounddevice) was tested and works. The audio path is proven.
- The startup batch (`start_typer_all.bat`) now includes a line to launch Player 2. On next reboot, it will start automatically.
- Code committed and pushed as `player2 v01: selection player (Numpad 5 -> FishAudio male voice)`.

## EXACT NEXT STEP

**Max needs to test it manually and give feedback:**
- Highlight some text in any application, press Numpad 5. The male voice should read it aloud.
- Press Numpad 5 again while it's speaking - it should stop.
- Tell the assistant:
  - Is the male voice acceptable or does he want a different FishAudio male voice?
  - Does the toggle-stop behaviour feel right?
  - Any problems with button responsiveness or tray icon?

Based on his answer, the very next actions could be:
- Swap the voice reference ID if he wants a different male voice.
- Adjust stop logic if the toggle feels off.
- Add a visual/audio cue (e.g., a beep) if desired.

## OPEN QUESTIONS (awaiting Max)

- Is the **default male narrator voice** final, or does he want a specific FishAudio male voice instead?
- Does the **second-press-to-stop** mechanic work exactly as he wants, or should it be something else (e.g., always play, no stop)?
- Any issues with the tray icon (color, label, quit behaviour)?

## KEY PATHS, IDs, AND NAMES

- **Player 2 script:** `C:\claude_base\tools\player2\player2.py`
- **Startup batch (modified):** `C:\claude_base\tools\typer\start_typer_all.bat`
- **Python environment:** uses the typer venv at `C:\claude_base\tools\typer\venv\` (contains numpy, sounddevice, soundfile, pyperclip, pynput, pystray, PIL)
- **FishAudio API details:**
  - Endpoint: `https://api.fish.audio/v1/tts`
  - Voice reference_id: `efc2f5151e24421c8f6b4ccc5b2d04f0` (the default male narrator)
  - API key file: located under `C:/Users/maxre/Nextcloud/zSyncMain/ssh/` (a file whose name includes "fishaudio_api")
- **Commit:** `player2 v01` on branch `main` (or wherever the working tree points) - only added `tools/player2/player2.py` and modified `tools/typer/start_typer_all.bat`

## GOTCHAS & DEAD ENDS RULED OUT

- **Do not modify `typer_e25c.py`:** This was explicitly avoided. That engine is fragile and restarting dictation mid-session is heavily disliked.
- **The voice reference ID** was taken from an existing working project (`yt_transcript_app.py`). It's known good. If Max wants a different male voice, only the reference_id needs swapping in `player2.py`.
- **No ffmpeg needed:** Because WAV is requested from FishAudio directly, playback uses soundfile (libsndfile) which is already in the venv. This avoids a hidden ffmpeg dependency.
- **Global hotkey conflicts:** Numpad 5 was confirmed free in the typer button mapping. No other process claims it. If another app later grabs it, pynput will silently fail to register, and Player 2 would appear running but non-responsive. Diagnose by checking if the hotkey registration succeeded (currently it logs to console, but since pythonw runs without console, that's lost - something to note for debugging).
- **Clipboard dependency:** Player 2 reads the current selection by copying it to clipboard (pyperclip). If clipboard is locked or empty, it will silently do nothing. No error toast is shown. That might confuse a user - if feedback is needed later, we can add a short beep or tray notification.
- **Test WAV file:** The test temporarily created `test_out.wav` in the player2 folder and was deleted. No leftover test artefacts.
