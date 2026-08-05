## Implementation Analysis: Player Enhancements for Storyboard Editor v2

### 1. Key Files and Locations
- **Player launch HTML**: `sc10/sound_assembly/code/storyboard_editor_v2.html`
- **Player view (likely a separate page/overlay)**: `C:\moma\player.html` or `C:\moma\js\player.js` (infer from typical structure; also possibly `storyboard_player.html`)
- **Shared MomaPopup**: `C:\moma\js\moma_popup.js` (the same popup used by Storyboard 2 for reel editing/annotations)
- **CSS**: `C:\moma\css\player.css` or inline in player HTML
- **API endpoints** (assumed RESTful):
  - `POST /api/reel/approve` (body: `{reelId}`)
  - `POST /api/reel/junk` (body: `{reelId}`)
  - `POST /api/reel/done` (body: `{reelId}`)
  - `GET /api/storyboard/{id}` or `GET /api/spot/{spotId}` to fetch current SPOT number

### 2. Data Mapping for Current Job and Spot
- **Current job**: Typically available from the parent storyboard context (e.g., `window.storyboard.jobId` or a global `currentJobId` set in `storyboard_editor_v2.js`).
- **Current spot number**: The storyboard contains multiple spots (e.g., `spots[]` array). The player is launched for a specific reel within a specific spot. The SPOT number should be retrieved from the storyboard’s current active spot index (e.g., `currentSpotIndex + 1`) or directly from the spot object (`spot.spotNumber`). Must be passed to the player during launch (e.g., via query string `?spotNumber=3` or `?spotId=xyz`).
- **Reel ID**: The currently playing reel is identified by the player’s internal `currentReelId`. This must be propagated to the MomaPopup and to the Approve/Junk/Done endpoints.

### 3. Functions & Endpoints to Modify/Create
| File | Function/Area | Change |
|------|---------------|--------|
| `player.js` (or equivalent) | `initPlayer(spotNumber, reelId)` | Accept `spotNumber` param; display it prominently in the player UI (e.g., a `#spot-number` element). |
| `player.js` | `openPopup(reelId)` | Call the shared `MomaPopup.open(reelId)` (or `window.openMomaPopup(reelId)`) directly, ensuring the same popup component is reused. |
| `player.js` | `handleApprove()`, `handleJunk()`, `handleDone()` | Add click handlers that call the respective API endpoints with `reelId` and possibly `spotId`. |
| `player.css` | Player text size | Increase base font size to ~14px (e.g., `body { font-size: 14px; }`) or target specific text elements. |
| `storyboard_editor_v2.html` | Player launch script | Add `spotNumber` to the URL/params passed to the player when opening it (e.g., `player.html?spotNumber=${currentSpot.spotNumber}&reelId=${currentReelId}`). |
| `moma_popup.js` | Ensure it can be called from the player (if not already) | Verify it’s a global function (e.g., `window.MomaPopup = {...}`) or accessible via `parent.MomaPopup` if player is in an iframe. |

*Note: The shared MomaPopup is already used by Storyboard 2 – the player must open it in the **same context** (same window/tab or iframe) so that annotations, editing, and state are consistent. If the player is in an iframe, `parent.MomaPopup` or `window.opener.MomaPopup` may be needed.*

### 4. Edge Cases
- **No reel playing**: Disable Approve/Junk/Done buttons or show a message. The SPOT number should still display but indicate “no reel”.
- **Reel already in a completed state** (approved/junked/done): Buttons should reflect current status (e.g., if already approved, the Approve button could be styled as applied or disabled). The user specifically asked not to add Unapprove, so once done, buttons may remain but could be reconsidered.
- **Multiple spots**: Each reel belongs to exactly one spot. Ensure the correct spot number is passed and displayed even if the player is reused across spots.
- **Popup already open**: The shared `MomaPopup` might have a singleton pattern. If open for a different reel, should close current and open new, or prompt user.
- **Permissions/roles**: The Approve/Junk/Done actions may be restricted to certain users. The player should handle 401/403 responses gracefully.
- **Race conditions**: Rapid button clicks could send multiple API requests. Implement debouncing or disable button until response.
- **Player launch from different contexts**: If the player is launched not just from storyboard_editor_v2, the SPOT number may be missing. Default to “N/A” or require the parameter.

### 5. Recommended Patch Plan
1. **Update `storyboard_editor_v2.html`**  
   - When opening the player, pass `spotNumber` from the current storyboard spot (e.g., `player.html?spotNumber=${spot.spotNumber}&reelId=${reelId}`).  
   - Ensure the player is opened in the same window/tab (or an overlay) so that `MomaPopup` is accessible in the same JavaScript context.

2. **Modify the Player HTML (e.g., `player.html`)**  
   - Add a prominent `<div id="spot-number">` to display the SPOT number (e.g., “SPOT 3”).  
   - Add three buttons: `#approve-btn`, `#junk-btn`, `#done-btn`.  
   - Adjust overall body font-size to 14px (or use a CSS class).

3. **Edit the Player JavaScript (e.g., `player.js`)**  
   - In initialization, parse `spotNumber` from the URL and set it in the DOM.  
   - Create handler functions for each button: call `POST /api/reel/approve` etc. with the current `reelId`.  
   - Implement a function `openInMomaPopup()` that invokes the shared popup: `window.MomaPopup.open(currentReelId)` or `parent.MomaPopup.open(currentReelId)` if in an iframe. Add this action to a double-click or a “Edit in Popup” link/button (it is implied that clicking the reel name/thumbnail does this).  
   - Handle edge cases: check `currentReelId` is defined before enabling buttons; disable buttons while API call is in flight.

4. **Adjust CSS**  
   - Set `font-size: 14px` on the player container or `body` to increase all text proportionally. For the SPOT number, use a larger/bolder style (e.g., `font-size: 18px; font-weight: bold; color: #333;`).

5. **Verify the Shared MomaPopup API**  
   - Check that `window.MomaPopup` (or similar) is globally accessible. If the player is in a separate window/iframe, ensure the popup is opened in the same window to allow annotations. If necessary, refactor the player to open the popup via `window.opener.MomaPopup` (if launched via `window.open`) or via `parent` if launched as an iframe.

6. **API Integration**  
   - Ensure the backend endpoints `/api/reel/approve`, `/junk`, `/done` exist and accept `reelId` (and optionally `spotId`). If not, create them or map to existing ones.

### Summary of Changes
- **3 files** primarily: `storyboard_editor_v2.html` (or its JS), `player.html`, `player.js`.  
- **1 CSS** modification.  
- **API consistency** check.  
- **No new popup** – reuse existing `MomaPopup`.  
- **No Unapprove** button as requested.

All changes should be made in the context of `C:\moma` with the given starting point. No secrets or unrelated material included.
