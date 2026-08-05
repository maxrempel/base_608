### Implementation Design: Reel Selection & Batch Actions

**Assumptions from existing code** (based on typical MoMA ReelMaker structure):
- `runner_core.js` contains main application logic, probably a `ReelGrid` class or object managing reel elements.
- Each reel has a video ID accessible via `data-video-id` attribute or similar.
- `runner_core.css` styles the grid and reel cards.
- `runner_page.html` contains the HTML structure, likely a container like `#reel-grid` and action buttons.

**New interaction layer** (to be added in a separate file or within `runner_core.js`):
1. **Each reel card** (`.reel-item`) gets a checkbox (`.reel-select`) added to its top-left or overlay.
2. **Controls bar** (below grid or alongside existing buttons):  
   - “Select All Visible” / “Deselect All” toggle  
   - “Approve Selected” / “Junk Selected”  
   - “Approve All Visible” / “Junk All Visible” (affects currently displayed reels, respecting any filter/sort)
3. **State management**: a simple `Set<videoId>` for selected IDs.  
   - On scroll/pagination, clear selection by default (or persist per page if requested).
4. **Batch approval/junk flow**:  
   - Show confirmation dialog (optional)  
   - Disable buttons during operation  
   - For each selected ID, POST to `/api/video/approve/<id>` or `/api/video/junk/<id>`  
   - Use `Promise.allSettled()` to run requests concurrently (limit to ~10 at a time to avoid server overload)  
   - On success, update the reel card CSS class (`.approved`, `.junked`) and remove from selection.  
   - On partial failure, show summary toast (e.g., “5 approved, 1 failed”).

**Preserving Imager grid selection**:  
- Imager likely has its own selection (e.g., highlight‑or‑compare mode). Our checkboxes use a different CSS class (`.reel-selected`) and a separate data attribute (`data-selected`). No interaction with imager’s click events – checkbox click stops propagation.  
- “Approve All Visible” does not affect imager’s selection; it only loops over visible `.reel-item` elements.

**Code location** (hypothetical additions to `runner_core.js`):
```javascript
// In initialization:
this.bindSelectionEvents();
this.bindBatchActions();

// Reusable helpers
selectAllVisible() { ... }
clearSelection() { ... }
batchApprove(ids) { ... }
batchJunk(ids) { ... }
```

### Likely Edge Cases

| Edge Case | Mitigation |
|-----------|------------|
| User clicks checkbox while a batch action is pending | Disable checkboxes and all action buttons during execution (set `disabled = true`) |
| No reels visible (empty grid) | Hide batch action buttons via CSS or JS check |
| Mix of already‑approved and unapproved | Allow selection of any reel; batch action will update regardless. Server returns 200/400 – handle gracefully |
| Network failure / timeout for some requests | `allSettled` – show final summary with failed IDs. Option to retry failed with one click |
| Reels loaded via infinite scroll or pagination | “Select All Visible” selects only currently visible items (those in DOM). On page change, selection is cleared (or we can keep a persistent filter across pages – decide based on UX requirement) |
| Duplicate IDs (e.g., reel appears twice due to bug) | Use a `Set` – duplicates ignored |
| User presses browser back/forward during batch | Poll for navigation; abort ongoing requests via `AbortController` (optional) |
| Imager selection conflicts (e.g., both imager and our checkboxes react to click) | Checkbox uses `event.stopPropagation()` to prevent imager’s `click` handler from firing |
| Reel is dynamically added/removed (e.g., after approve) | After each batch update, refresh the reels list or mark DOM elements accordingly. Selection set is cleared after batch action to avoid stale references |

### Focused Tests

**Unit (JavaScript)**
- `selectAllVisible()`: after adding three `.reel-item` elements with distinct IDs, assert that `selectedIds` contains all three.
- `clearSelection()`: after selecting two, call clear, assert empty.
- `batchApprove([])` / `batchJunk([])`: should show warning or do nothing (test that no POST is sent).
- `batchApprove` with one ID: verify fetch called with correct URL and method POST.
- `onCheckboxChange`: toggling a checkbox adds/removes ID from set; ensure class `.reel-selected` is added/removed.

**Integration (using a mock server)**
- Load page with 3 reels. Click “Select All” → checkboxes become checked. Click “Approve Selected” → mock receives 3 POSTs. Assert UI shows success feedback.
- Try to approve when no reel selected → button is disabled or shows tooltip.
- Mix of selected and unselected: batch approve selected only, verify unselected reels are not touched.
- Approve all visible when no filter: verify all visible POSTs.
- Junk all visible when one reel already junked: verify that reel is not junked again (server may return 400 – handle by skipping or showing error).

**UI (optional with Playwright/Cypress)**
- Checkbox appears on each reel card.
- “Select All” toggles “Deselect All” label.
- After batch action, checkboxes are cleared and disabled briefly.
- Imager selection (e.g., clicking the reel background) does not affect checkbox state.

### Acceptance Criteria
- User can efficiently select & approve/junk multiple reels at once.
- No regression in existing imager click behavior.
- Server is not overloaded (concurrency limit).
- Clear feedback on success/failure.
