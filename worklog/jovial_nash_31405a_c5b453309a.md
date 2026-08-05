
## [2026-07-05 11:27] ? 8d105d01
- DID: Fixed imager scene-filter pollution (D06B): /api/plates now honors ?arr= scene scope server-side (combo_gui.py) + loadAll sends it (runner_core.js). Committed b9c5aa3, pushed moma master, bounced 8779 GUI only.
- STATE: VERIFIED: unscoped plates=1184, sc11-scoped=25; client cache 298 scene-11 items, 0 off-scene. Flash structurally impossible now.
- NEXT: Watch for the other chat's handover; confirm with Max the flash is gone on his screen.

## [2026-07-05 23:01] ? 8d105d01
- DID: Storyboard 'ancient image leak' RESOLVED as diagnosis: NOT a filter bug, NOT D06B. Session D52C's script _d52_import_room_history.py (commit 3ebea5b, 2026-07-04 23:49) ran 2026-07-05 06:45-06:48 and created 75 job rows (label=sc11_room_history, scene=bg_sc11_service_desk_room) importing old station_room*.png from interiors/junk+older_obsolete as done jobs -> they flood the sc11 pile. Earlier this session: fixed imager /api/plates scene-scope (committed b9c5aa3, pushed).
- STATE: Posted full evidence + 4 questions to D52C on team-d board and force-woke it (queued, no live listener). Awaiting D52C's account of what command triggered the import. 75 rows NOT yet touched.
- NEXT: Relay D52C reply to Max; on Max's word junk/un-scene the 75 rows (coordinate with D52C + D06C who is editing storyboard_editor_v2.html).
