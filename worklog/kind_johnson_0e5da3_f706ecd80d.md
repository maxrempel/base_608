
## [2026-06-27 15:03] ? e84ca26a
- DID: Built instant clipboard-paste mode for typer (--paste): set CF_UNICODETEXT + Ctrl+V, Windows clipboard-history excluded (3 special formats DWORD 0), prev clipboard restored. Tested clean on zero, Max confirmed much faster, promoted to plus + RU. Added --paste to autostart bats + new start_typer_zero.bat backup launcher.
- STATE: All 3 typer instances running instant: plus(f9,numplus), zero backup(num0,numins), RU(rctrl) - all --paste. Commits e65ca0e8 swallow-fix, 599db406 quick-tap+zero, plus 2 today: clipboard feature + bat autostart. The 'choose a device' phantom was Max reading his screen aloud, NOT a hallucination.
- NEXT: Watch for any clipboard-restore or history-leak issues in real use; keystroke mode still available as fallback if instant ever misbehaves.

## [2026-06-30 13:57] ? e84ca26a
- DID: Fixed typer recall paste: held Left Alt corrupted Ctrl+V->Ctrl+Alt+V and Enter->Alt+Enter. _send_ctrl_v and press_enter now drop held Alt/Shift/Ctrl first. Restarted Plus hidden, committed+pushed (100fdd47). Max confirmed recall works.
- STATE: typer fully working: numpad+ talk, Left Alt+numpad+ recall re-sends last dictation, Ctrl+numpad+ free for Chrome zoom. Method doc updated earlier (8a9ff113).
- NEXT: None - task complete unless Max reports more.

## [2026-06-30 17:26] ? e84ca26a
- DID: Reconciled typer.py collision with session E125. Git truth: my commit 100fdd47 accidentally co-committed E125's uncommitted clipboard fix (_open_clipboard_retry + keystroke fallback + adaptive settle) along with my Left-Alt-clear recall fix. Both live+pushed, nothing lost. Force-woke E125 (signal consumed) + fleetcomm post: told it to stand down, don't re-commit typer.py (already on master = would branch), stop hunting nonexistent 'E25'.
- STATE: typer fully working on Plus (recall + clipboard fix). Live tool = C:/claude_base/tools/typer/ (typer1); typer2 portable copy still unpatched. Max actively USING the tool - NO restart allowed. Zero/RU pick up clipboard fix on next natural restart.
- NEXT: typer2 clipboard patch = separate low-priority later task. Nothing pending now.

## [2026-07-01 12:59] ? e84ca26a
- DID: Fixed recurring typer 404 'Invalid URL POST /v1/audio/transcriptions'. Root cause: instances launched from a polluted shell captured OPENAI_API_KEY(DeepSeek)/OPENAI_BASE_URL(proxy) at start -> Whisper hit a host with no transcription route. Fix in commit 901d08f9: hard-pin base_url=https://api.openai.com/v1 + load_api_key reads typer .env FIRST (not env var). Verified live transcription 200. Restarted all 3 instances hidden with hardened code.
- STATE: typer1 all 3 instances (Plus/Zero/RU) running hardened + clean. Now env-independent - no launch shell can redirect Whisper. Recall + clipboard fixes also live.
- NEXT: Watch for any further 404; if gone, done. typer2 portable copy still needs same hardening later.

## [2026-07-02 07:55] ? e84ca26a
- DID: Fixed typer swallowing sentence-start on loaded CPU (commit f819c0c8). Root cause: pre-roll ring buffer only 0.6s; on a busy machine the key-press -> recording-on gap exceeds 0.6s so the beginning ages out of the ring (NOT a driver drop - zero overflow in log). Fix: PREROLL_SECONDS 0.6->2.0, IDLE_CLOSE_S 45->120 (fewer cold re-opens, still not always-on). Restarted all 3 instances hidden.
- STATE: typer all 3 live with 2.0s pre-roll cushion + 120s warm window. Also live: base_url pin (no 404), recall+clipboard fixes. Slower transcription today = cloud/CPU load, outside our code.
- NEXT: Watch if beginning-loss recurs; if it still happens the start-delay exceeds 2s (would need to reduce start latency or keep mic warmer).
