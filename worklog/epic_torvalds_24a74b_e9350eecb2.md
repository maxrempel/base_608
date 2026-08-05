
## [2026-06-19 14:09] ? 99f5f77c
- DID: Set up WhisperWriter (C:\tools\whisper-writer) end-to-end: OpenAI whisper-1 dictation, hold F9 to talk. Fixed key delivery (.env), RU/EN auto-detect + bilingual bias prompt, UTF-8 config fix in utils.py, BT headset (HomeSpot JY508-AV) set as default mic via AudioDeviceCmdlets, added Windows Startup shortcut.
- STATE: All working, tested by Max in EN+RU from BT headset.
- NEXT: Optional: investigate google-contacts MCP process leak (~24 stray main.py seen earlier).

## [2026-06-20 14:55] ? 99f5f77c
- DID: Built 'typer' dictation tool at C:/tools/typer (F9 hold-to-talk, OpenAI whisper-1, instant clipboard paste, 'submit now'->Enter, pystray tray w/ Quit). Reuses whisper-writer venv + .env key.
- STATE: Running detached (pythonw). Fixed submit-now to suffix-match on API text. Awaiting Max test.
- NEXT: Confirm submit-now fires Enter; consider auto-start on login if Max wants.

## [2026-06-21 08:01] ? 99f5f77c
- DID: Built+pushed cross-machine fleetcomm WAKE (Task 1+2): aliasing, per-session read cursor, cmd_wake, wake_listener fleet-poll. Committed ec68f739+d6f9a134, global2+method doc updated.
- STATE: Both tasks done/tested/pushed on Pine. Centauri RECEIVER side NOT wired yet (needs git pull + wire_hooks.py + restart + bcast-named sessions). Polling fleetcomm as E12 every 20min for Centauri A01 typer reply + wake-setup confirm; all cycles silent.
- NEXT: On Max's word: optionally SSH-wire Centauri myself; route the two flagged waiting requests (E03 Nextcloud-propagation confirm; mikedc double-email risk). Keep polling otherwise.
