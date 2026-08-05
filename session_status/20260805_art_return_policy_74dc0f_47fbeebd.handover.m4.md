# Scribe handover - milestone 4 (~304K tokens)
# session: 20260805_art_return_policy_74dc0f_47fbeebd
# cwd: C:\claude_base\.claude\worktrees\walmart-return-policy-74dc0f
# written: 2026-08-05 00:57:03 by deepseek-v4-pro

## Handover: Claude Task Panel - Board Parity Session

### GOAL (in Max's words)
"First reproduce all the features of codex board. ... codex has tons more features, catch up with it."

Pair the Claude Task Panel with the existing Codex Session Board, feature-for-feature, inside its own tight, frameless window.

### DECISIONS + WHY

**Window delivery**
- We needed a standalone window without browser chrome. The Codex board gets one from its Electron host; the panel doesn't have that.  
- **Decision:** Chrome application mode (`chrome.exe --app=http://localhost:4747`). It strips tabs, address bar, bookmarks-just a title bar.  
- Launcher is a VBS script (starts server if needed, opens Chrome, never flashes a console). A Desktop shortcut was created.  

**Open button fix**
- The deep?link launcher fired PowerShell with `detached:true`. On Windows a detached process owns no console; PowerShell died before forwarding the `claude://resume?session=...` link.  
- The link itself is real-confirmed inside the desktop app's own code and against the app log.  
- **Decision:** spawn PowerShell non?detached, wait ~0.7s, and return the real exit code + stderr to the UI. The button now works and tells the truth.

**Density & layout**
- The old panel had column?driven layout and generous cards (~85px). The board uses a workspace model with a fixed left rail and free?position tiles on the right, cards at ~28px.  
- **Decision:** full rewrite of the UI to match the board's workspace model: a fixed Recent rail, fixed Unassigned rail, free?position tiles, draggable by their header, with drop?zone indicator and insertion line.

**Feature parity**
- The board's feature list from its v21 (layout, dragging, Explorer?style clicks, rename, right?click menus, Undo/Redo, search, Recent slider, recency borders, manual ordering, archive, Focus Sets, Compact mode) was checked off.  
- **Decision:** implement all of them, no shortcuts. Undo/Redo persists across restarts. Archive only hides the card; transcripts are never touched.

**Shortcut placement**
- The first Desktop shortcut went to `$env:USERPROFILE\Desktop`, but Max's real Desktop is OneDrive?redirected.  
- **Decision:** resolved actual Desktop path via registry `User Shell Folders`. Shortcut now sits next to the Codex++ Session Board icon.

### CURRENT STATE
- **Board parity is built and committed** (commit message: *Panel v04: full Codex board parity built and verified*). Pushed to branch `codex/beautification-selector-v02` in `maxrempel/claude_base`.
- Server is running on `http://localhost:4747` (Node background process).
- All unit tests (15) and the smoke test pass.
- The Desktop shortcut works now; Max confirmed "it worked!" for the Open button and then the shortcut placement.
- Max has **not yet tested the new board**. The last interaction was about finding the shortcut. He was told to close the old panel window and open from the shortcut.

### EXACT NEXT STEP
**Max opens the panel from the Desktop shortcut and validates the board.**
- Close any old panel window.
- Double?click "Claude Task Panel" on the real Desktop.
- Try core board interactions:
  1. Drag free tiles by their header - landing frame and insertion line appear.
  2. Single?click a card to select; double?click to open the session via `claude://`.
  3. Pause?then?click a tile's title to rename.
  4. Right?click cards, tiles, and empty space to see context menus.
  5. Use Ctrl+Z / Ctrl+Y for undo/redo across moves, assignments, renames.
  6. Type in the search box; the list filters in real time.
  7. Open the Recent slider (top?left), move the stops, see the card list update.
  8. Collapse/expand the rails with the chevrons.
  9. Toggle Compact mode.
- Report anything that feels wrong or missing.

### OPEN QUESTIONS (awaiting Max)
- **"Plus" features**: Max mentioned ideas about timing and archives, but not yet finalized. He said "first reproduce all the features" - so these are on hold.
- **"Expanded a bit more"**: earlier he said the board was "tight" and wanted the panel to copy it but also to be "expanded a bit more." He hasn't decided what extra falls outside the strict board parity.

### KEY FILES / PATHS / IDS
- **Project root**: `C:\claude_base\tools\claude_task_panel`
- **Key sources**:
  - `src/public/app.js` - the full board UI logic (workspace model, dragging, clicks, menus, undo, search, sliders)
  - `src/public/style.css` - dense board?style cards
  - `src/public/index.html` - minimal DOM
  - `src/server.js` - Node Express server (port 4747)
  - `src/sessionStore.js` - data store with persistent undo/redo, archive, Focus Sets
  - `src/launcher.js` - Node subprocess that fires the `claude://` deep link
- **Launcher scripts**:
  - `launch/Start Claude Task Panel.vbs` - hidden VBS entry point
  - `launch/Start Claude Task Panel.ps1` - helper that starts Node and opens Chrome
- **Tests**: `tests/launcher.test.js`, `tests/session-store.test.js`, `tests/smoke-api.js`
- **Desktop shortcut**: `Claude Task Panel.lnk` on the OneDrive?redirected Desktop
- **Chrome path**: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- **Branch**: `codex/beautification-selector-v02` in repository `maxrempel/claude_base`
- **Real session count**: 287 sessions parsed from your actual Claude sessions directory

### GOTCHAS
- **Never use `detached:true` with `execFile` on Windows** for launching something that depends on a console or output. It silently fails.
- **Desktop path is not `$env:USERPROFILE\Desktop`** on this machine - use registry key `User Shell Folders` (OneDrive redirect).
- **Archive in the panel does not delete or move any transcript**; it only hides the card. Undo brings it back instantly.
- **The server must be running** for the shortcut to work; the launcher checks and starts it if needed.
- If the panel window is already open from a previous version (pre?v04), it must be closed before launching from the shortcut, or the old UI will remain.

---

This should be enough for a cold session to immediately resume testing the board parity.
