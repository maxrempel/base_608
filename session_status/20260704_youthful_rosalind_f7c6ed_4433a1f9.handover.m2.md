# Scribe handover - milestone 2 (~154K tokens)
# session: 20260704_youthful_rosalind_f7c6ed_4433a1f9
# cwd: C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed
# written: 2026-07-04 22:24:46 by deepseek-v4-pro

## GOAL (Max's own words)
Create a tool called **facer** inside MoMA, invoked from the image popup (usually opened from the imager tab). In the tool, you click a numbered person button (1-6, but usually only four), then draw a box on the image with the mouse to mark that person's face. The box automatically saves and stays visible. Nothing else in this part - just labeling. The face positions are stored per image in the database.

## DECISIONS + WHY
- **Tool name**: `facer` - user's choice.
- **Invocation point**: Inside the image popup (`shared_ui/popup.js`) as an action button added to the plate and photo-shot action rows. This makes it available from imager or anywhere that opens the popup, exactly as requested.
- **Number of persons**: Supports up to 6 (user said "program the sixth, but normally only four"). Implemented all six for future proofing; each gets a distinct colour for easy visual differentiation.
- **Immediate auto-save**: After the user draws a box, it is sent to the backend and saved instantly. No separate "approve" step - user explicitly rejected an approve button.
- **Storage**: A new `face_boxes` table in the MoMA D1 database (`moma-v2`), with columns: `image_id` (text), `person` (int), `x, y, w, h` (real numbers). One row per labelled face per image.
- **Backend structure**: Added GET and POST endpoints under `/api/faces/<image_id>` (to load all boxes for an image), `/api/faces/<image_id>/save` (to upsert a single person's box), and `/api/faces/<image_id>/delete` (to delete a single person's box). Chose upsert for simplicity - no need to check if a box already exists before saving.
- **Frontend state model**: Within the popup's module scope, a `_facer` object holds the current person number, whether the mode is active, the loaded face boxes, and HTML overlays (SVG/canvas? used `position:absolute` divs for person buttons and the image overlay with mouse drag). Used a `pointerdown`/`pointermove`/`pointerup` approach for box drawing.
- **Cleanup**: The facer mode is exited when the popup closes or a new image is loaded, handled by the existing popup `close()` and content-loading functions. A `_clearFacer()` helper removes overlays.
- **File changes**:
  - `sc10/shared_ui/popup.js` - added facer button HTML injection, facer logic, cleanup hooks.
  - `sc10/combo_runner/code/combo_gui.py` - added GET/POST routes and D1 table setup.
- **Testing**: Performed live endpoint round-trip tests (GET empty, POST save, GET verify, DELETE, GET empty again) against the running server (port 8779) and cleaned up test rows.
- **Deployment**: Committed to `master` branch of the local MoMA git repository and pushed.

## CURRENT STATE
- All code is written, syntax-checked (both JS and Python pass), and tested round-trip.
- The `face_boxes` table exists and is ready.
- The facer button and full label-save functionality are live on the server.
- The user has been instructed to hard-refresh the imager tab to load the updated frontend code.
- **No further work has been done beyond the labelling (Part 1 as described).**

## EXACT NEXT STEP
The immediate next step is for the user (or another session) to **test the tool in the browser**:
1. Ensure the MoMA server is running (on port 8779).
2. Hard-refresh the imager tab (Ctrl+F5) to pick up the new popup.js.
3. Open any image from imager.
4. Click the pink "facer" button in the popup.
5. Test labelling persons 1, 2, etc., and verify that boxes persist when closing and reopening the popup on the same image.
6. Confirm that "clear all" removes all boxes.

After successful testing, the user indicated a possible "second part" (using the labeled positions for something). This is **not defined yet** - an open question.

## OPEN QUESTIONS (awaiting user)
- What should be done with the saved face positions after labelling? (Part 2 - not specified.)
- Any desired changes to the box-drawing behaviour (e.g., minimum size, ability to move a box without redrawing)?
- Should there be any visual feedback beyond the colour-coded rectangles (e.g., person number label on the box)?
- Should the facer tool be available on video popups too? (It's currently only present on image popups; the code only added the button for plate and photo-shot contexts.)

## KEY PATHS / IDS
- **MoMA repository root**: `C:\moma` (working directory used: `/c/moma/sc10`)
- **Frontend file**: `sc10/shared_ui/popup.js`
- **Backend file**: `sc10/combo_runner/code/combo_gui.py`
- **Git branch**: `master`
- **Server port**: 8779 (auto-reloads combos)
- **D1 database**: `moma-v2` (UUID `3a1326e3-07f5-4e7e-a30a-087164ad37ef`)
- **New table**: `face_boxes` with columns `image_id TEXT, person INTEGER, x REAL, y REAL, w REAL, h REAL`
- **API endpoints**:
  - `GET /api/faces/<image_id>` ? returns JSON array of face objects `[{person, x, y, w, h}, ...]`
  - `POST /api/faces/<image_id>/save` ? body: `{person, x, y, w, h}` ? upserts single box
  - `POST /api/faces/<image_id>/delete` ? body: `{person}` ? deletes box for that person

## GOTCHAS
- The user initially said check in as "D03B" but immediately corrected to **D05B**. Correct branch bulletin name is D05B.
- The server auto-reloads `combo_gui.py` changes, but the browser **must be hard-refreshed** (Ctrl+F5) to get the updated popup.js because the static files may be cached.
- The facer button is only injected for plate and photo-shot image popups (not video popups). If the user tries to open an image via a different popup type, the button may not appear.
- The box coordinates are relative to the displayed image's natural dimensions (the overlay scales with the image). If the image is resized or has CSS applied, coordinates might not align exactly with pixel space - but since the popup uses `naturalWidth`/`naturalHeight` and scales proportionally, it should be correct as long as the overlay is correctly sized.
- The database schema was created manually via the D1 MCP tool before the backend code was written; the backend doesn't automatically create the table on first run. Future fresh deployments would need to ensure the table exists.
