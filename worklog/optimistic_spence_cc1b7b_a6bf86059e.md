
## [2026-06-25 14:43] ? b6472802
- DID: Decoupled typer from whisper-writer (own venv+.env, portable key load), added 3-space paste prefix + both-shift no-send fix; committed+pushed (65b48b34). Uninstalled whisper-writer (840MB). Max wanted ZERO autostart -> removed Startup shortcut. Accidentally killed live instances too -> + key went dead -> relaunched EN+RU hidden via pythonw, Max confirmed working.
- STATE: typer EN+RU running on local venv (no console). NO autostart shortcut (Max wants none on boot). Tool intact in C:\claude_base\tools\typer.
- NEXT: Nothing pending. If Max wants boot autostart later, create Startup shortcut to start_typer_all.bat.

## [2026-06-25 15:34] ? b6472802
- DID: typer: tried replacing clipboard-paste with direct Unicode SendInput (to fix clipboard-history pollution + Shift->V bug). First attempt silently typed nothing: Win32 INPUT struct was 32 bytes, must be 40 (union must be padded to MOUSEINPUT size) - SendInput rejects wrong cbSize. Fixed struct (proven: SendInput returns all events). But Max relies on typer live and it had broken twice, so per his 'restore to working copy' I git-checkout'd the committed clipboard version and restarted EN+RU. Max happy.
- STATE: typer EN+RU running the COMMITTED clipboard-paste version (proven working). Uncommitted Unicode rewrite was reverted via git checkout - the working-tree edits are GONE (not saved to sidecar; cp was rejected). The fix is reconstructable from this session: add _pad (c_ubyte*32) to the INPUT union so sizeof==40, set SendInput argtypes, plus force-release Shift/Ctrl before typing. No autostart change. NOT committed.
- NEXT: If Max wants the no-clipboard improvement: re-apply the Unicode-injection rewrite WITH the 40-byte struct fix, test in a throwaway target first (SendInput must return ==event count), only swap live when Max is free.
- LESSON: Win32 INPUT struct via ctypes MUST be 40 bytes on 64-bit (union padded to MOUSEINPUT=32) or SendInput silently does nothing (returns 0). Always verify SendInput's return == number of events before trusting injection.

## [2026-06-25 16:16] E25 b6472802
- DID: Built all 4 typer features (streaming overlapping-window dictation, Ctrl+key repeat buffer, dictation history log, chunked SendInput) into typer_stream_test.py on num0 test key. Streaming confirmed by Max: 434-char long dictation streamed+stitched+logged clean.
- STATE: Test instance running on num0/en (own logs typer_streamtest_en.log + typer_history_en.md). Live EN (f9,numplus) + RU (rctrl) restarted and up. Max testing Ctrl+numpad-0 repeat now.
- NEXT: On Max OK: promote streaming+repeat+history into live typer.py (both EN+RU), wire Ctrl+numplus repeat key, commit+push.
