
## [2026-08-04 23:53] ? 47fbeebd
- DID: Fixed Claude Task Panel drag-and-drop, mid-drag refresh, scroll loss, transcript re-read cost and watcher noise; panel v02, commits a092f8a2 + 123e7581 pushed on codex/beautification-selector-v02
- STATE: Panel server restarted hidden on 4747 with the new code; 12 unit tests + smoke test pass; verified live against 286 real sessions with temp groups that were cleaned up; Codex Session Board untouched
- NEXT: Ask Max to try dragging in the panel and confirm; if the Codex board also needs work, get his repro before touching src/index.js

## [2026-08-05 00:17] ? 47fbeebd
- DID: Found and fixed the real Open-button bug: launcher spawned PowerShell with detached:true, which on Windows gets no console and never runs Start-Process, so the claude://resume deep link was dropped. Removed detached, made the endpoint await the dispatch and report failures. Commit 15a07b14 pushed.
- STATE: Panel restarted hidden on 4747; 15/15 unit tests + smoke pass; verified via the desktop app's own main.log (import + startShellPty) and a 400 error on the failure path
- NEXT: Ask Max to click Open and confirm the desktop app comes to the front; if it imports but does not focus, look at the second-instance argv suppression in the app log

## [2026-08-05 00:32] ? 47fbeebd
- DID: Panel v03: own application window (Chrome app mode via hidden VBS launcher + Desktop shortcut, no browser bars) and board-tight density (cards 85px->28px, columns 300->210px, 2-line titles, age in decimal days, hover actions). Wrote PLAN_PARITY_WITH_BOARD_v01_tomemex.md. Commit d0e4e810 pushed.
- STATE: Max confirmed the window works. 15/15 tests + smoke pass. Panel server hidden on 4747.
- NEXT: Phase B of the parity plan: free-position tiles dragged by title with saved positions, fixed Recent and Unassigned rails, collapse chevrons, blue landing frame and insertion line. Then Phase C behaviours. Ask Max what 'expanded a bit more' should mean before building Phase D.

## [2026-08-05 00:51] ? 47fbeebd
- DID: Panel v04: full Codex board parity built and verified - Recent+Unassigned rails, free-position tiles dragged by header with saved x/y, landing frame, insertion line, collapse, Explorer clicks, 3 context menus, 20 pastels, 20-step persisted undo/redo, search, Recent slider (8 stops), recency borders, manual ordering, recoverable archive, Focus Sets, Compact, Ctrl+Z/Y/F. Added PATCH /api/state. Commit 9ab3348e pushed.
- STATE: 15/15 tests + smoke pass; every feature exercised live against 287 real sessions with Max's state captured and restored (back to 287 of 287). Panel hidden on 4747; desktop shortcut opens it in its own window.
- NEXT: Wait for Max to try it and report. The plus features (timing and archives) are not finalized - do not build them until he specifies.

## [2026-08-05 08:18] ? 47fbeebd
- DID: Added Start menu entry for the Claude Task Panel plus launch/Install Shortcuts.ps1 (idempotent, creates Desktop + Start menu shortcuts from the registry's true folder paths). Recorded the OneDrive Desktop redirect in global CLAUDE.md operational facts. Commits d2f35247 + 48891bca pushed.
- STATE: Panel v04 with full board parity is live and Max has tested it happily; server hidden on 4747; both shortcuts verified created.
- NEXT: Wait for Max on the plus features (timing and archives); nothing else pending.
