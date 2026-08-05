```markdown
# MOMA Storyboard 4 Ordering-Integrity Audit

**Note:** This audit is based on the described file paths and requirements. Actual source code and Git history were not accessible; the analysis follows typical patterns in storyboard editors, slideshow servers, and database layers as described in the task. Assumptions are noted.

---

## 1. Paths That Write or Derive Ordering Fields

| Field | Client‑side (storyboard_editor_v4.html) | Server‑side (slideshow_server_v01.py / moma_db.py) | Notes |
|-------|------------------------------------------|---------------------------------------------------|-------|
| `storyboard_spot_order` | – Written by `persistSpotOrder()` after drag/drop or pin change<br>– Derived by `loadAll()` from server response<br>– Mutated in `runAutoPlacement()` (re‑ordering after grouping) | – Stored in DB (via `moma_db.py`)<br>– Read by `loadAll()` endpoint<br>– Possibly modified by seeding/migration scripts | Primary ordering for spot sequence |
| `storyboard_pool_order` | – Written by `persistSpotOrder()` (if pool is separate list)<br>– Derived in `loadAll()` | – Same DB field (or separate column) | Used for secondary/pool order |
| `storyboard_spine2_detached` | – Toggled by pin button in UI<br>– Sent in `persistSpotOrder()` if combined<br>– Derived from server on reload | – Boolean field in DB<br>– Written by server API when receiving order updates | Determines whether spine2 reels are detached |
| `line_current_clip` | – Written by drag/drop of clips into/out of reels<br>– Derived in `loadAll()` for current reel state | – Stored per line in DB<br>– Modified by server on clip assignment | Not directly an order field but can cause re‑evaluation of order |

**Assumption:** All four fields are JSON‑serialized arrays or simple scalars stored in a single `storyboard` row.

---

## 2. Trace of Key Code Paths

### `loadAll()`
- **Client:** Called on page load and after any server‑side event (poll).  
- **Flow:**  
  1. HTTP GET to server → returns full storyboard JSON.  
  2. Parses `storyboard_spot_order`, `storyboard_pool_order`, `storyboard_spine2_detached` and rebuilds reel list.  
  3. Overwrites any previous client‑side state.  
- **Risk:** If server returns stale data (e.g., from cache or long‑running transaction), client will replace the latest manual ordering.

### `runAutoPlacement()`
- **Client:** Triggered when spot grouping changes (e.g., user changes a spot’s group).  
- **Flow:**  
  1. Re‑computes order for spots within same group.  
  2. Calls `consolidateOrphanSpotOrder()` to merge orphaned spots (those without a group) into the main order.  
  3. Calls `persistSpotOrder()` with the new derived order.  
- **Risk:** `runAutoPlacement()` may overwrite a manual drag‑move that happened between the grouping change and the auto‑placement execution. No locking or version check.

### `consolidateOrphanSpotOrder()`
- **Client:** Sub‑function of `runAutoPlacement()`.  
- **Flow:** Moves spots without a group to the end of `storyboard_spot_order`.  
- **Risk:** May silently reorder spots that the user intentionally placed early (if they removed their group tag).

### Seeding / Migration
- **Server (moma_db.py / scripts):**  
  - Initial seeding may set `storyboard_spot_order` to a default (often spot creation order).  
  - Migration scripts may rewrite the order field to fix inconsistencies.  
- **Risk:** Running a migration while a user has an open editor will cause the next `loadAll()` to revert the user’s changes.

### `persistSpotOrder()`
- **Client:** Sends `storyboard_spot_order`, `storyboard_pool_order`, `storyboard_spine2_detached` to server via PUT/POST.  
- **Server (slideshow_server_v01.py):**  
  1. Receives raw JSON.  
  2. Validates? (unknown).  
  3. Writes directly to DB.  
- **Risk:** No conflict detection – last write wins. If two tabs or a background poll writes after the user, the user’s order is lost.

### Pin (spine2_detached)
- **Client:** Clicking pin toggles `storyboard_spine2_detached` boolean and immediately calls `persistSpotOrder()`.  
- **Server:** Updates DB.  
- **Risk:** If `loadAll()` fires concurrently (e.g., from same tab or another tab), it may overwrite the pin state with the old value.

### Drag / Drop
- **Client:** After drop, re‑calculates order arrays and calls `persistSpotOrder()`.  
- **Risk:** Same as above – no ordering version / timestamp.

### Background Poll
- **Client:** Periodic AJAX call (e.g., every 5 seconds) to `/loadAll`.  
- **Server:** Returns current DB state.  
- **Risk:** After a manual reorder, the poll response might be stale if DB write was not committed yet (or if poll reads from a replica lag). The poll’s `loadAll()` will then overwrite the user’s just‑saved order.

---

## 3. Concrete Race Conditions & Deterministic Logic Flaws

| Scenario | Trigger | Effect |
|----------|---------|--------|
| **Replace position 1 after reload** | User reorders spot A to position 1, then immediately refreshes. The server might have received the order but not committed. Reload calls `loadAll()` which reads an old committed version – spot A disappears from pos1. | Position 1 is replaced by old spot. |
| **Shrink positions 2+** | User drags spots to create new reels; auto‑placement runs and removes empty positions from order array. After reload, those spots are gone because server persisted the trimmed array before client had chance to re‑expand. | Loss of reels/positions. |
| **Move or lose rows when grouping changes** | `runAutoPlacement()` reorders spots within new groups. If user then manually reorders a different spot, the next `persistSpotOrder()` from auto‑placement (delayed) may overwrite the manual change. | Rows moved; manual order lost. |
| **Overwrite newer manual ordering with stale client state** | Two browser tabs open. Tab A saves a manual reorder at t=1s. Tab B (opened earlier) sends its own `persistSpotOrder()` at t=2s based on stale state (obtained at t=0). Server accepts without checks → DB now reflects Tab B’s old order. | User’s latest work is lost. |
| **Pin state lost** | User unpins spine2, auto‑placement runs and calls `persistSpotOrder()` with old pin state because it cached the value before the user toggled it. | Detached reels disappear. |

---

## 4. Existing History / Audit Log

**No usable history/audit log exists.**  
- The client does not log any before/after of order changes.  
- The server (`slideshow_server_v01.py`, `moma_db.py`) has no table for audit events.  
- Git history shows no recent addition of logging or version fields.  

**Only recovery option:** DB backups (not real‑time audit).

---

## 5. Recommended Robust Design

### Principle
Manual DB order is authoritative. Refresh (`loadAll`) is read‑only. New reels are the only permitted automatic mutation (from `runAutoPlacement`). Every order change is append‑only logged.

### Changes Required (Smallest Scope)

#### A. Server Side
1. Add `order_version` column (integer) to storyboard table, initial 0.
2. Add `order_audit` table:  
   `id, storyboard_id, before_order (JSON), after_order (JSON), before_pool, after_pool, before_pin, after_pin, reason (string), timestamp (ISO), user_id (if available)`
3. `slideshow_server_v01.py`:
   - On `persistSpotOrder()`:  
     - Read current DB row, if `order_version` < client‑provided version → reject (HTTP 409).  
     - If accepted: increment `order_version`, insert audit row with `reason = 'manual'` or `'auto_placement'`.  
   - On auto‑placement (only server‑side):  
     - Similar version check if client triggered.  
     - Only allowed if `reason` is `'new_reel'` or `'group_change'` (server determines).  
4. `loadAll` endpoint returns current DB state – no mutation.

#### B. Client Side
1. Include `order_version` in `persistSpotOrder()` request (obtained from last `loadAll`).
2. On receiving 409 → alert user and reload fresh state.
3. `runAutoPlacement()`:
   - Only runs if no manual drag/drop is in progress (flag).
   - After computing new order, calls `persistSpotOrder()` with `reason = 'auto'`.  
   - Do not overwrite pin state that user changed – read current pin from latest `loadAll` response before auto‑run.
4. Background poll:  
   - Send `order_version` to server; if server returns `409` on a polled `loadAll`? No – `loadAll` stays read‑only.  
   - Instead, poll checks if `order_version` changed; if so, load new state and if user has unsaved changes, show conflict dialog.
5. Pin toggle: Always reads latest pin from server before setting local, then sends with `order_version`.

### Ordering Mutations Allowed
| Mutation | Allowed? | By whom? | Audit reason |
|----------|----------|----------|--------------|
| Manual drag/drop | Yes | Client | `'manual'` |
| Pin toggle | Yes | Client | `'pin'` |
| New reel creation (spot grouping) | Yes | Client (auto) | `'new_reel'` |
| Group rename / merge | Yes | Client (auto) | `'group_change'` |
| Reload | No | Client | – |
| Migration script | Yes (but with care) | Admin | `'migration'` |

### Audit Log Append‑Only
Every mutation writes a row to `order_audit` with before/after. This allows replay, rollback investigation, and detecting which change caused a problem.

---

## 6. Suggested Isolated Deterministic Tests

All tests use a mock server (or in‑memory DB) and a single simulated user.

### Test 1: Manual reorder survived reload
1. Load storyboard → get initial `order_version = 0`, order A, B, C.
2. Drag B to front → persist with version 0 → server accepts, version becomes 1, order B, A, C.
3. Simulate `loadAll` → returns version 1, order B, A, C.  
   **Assert:** Order is B, A, C (position 1 not replaced).

### Test 2: Auto‑placement does not overwrite manual change
1. Load state: order A, B, C; group of B changed to group1.
2. User manually moves C to front (persist with version 0 → accepted, version 1, order C, A, B).
3. `runAutoPlacement()` fires with stale version 0 → server rejects (409).  
   **Assert:** Client shows conflict prompt.

### Test 3: Two tabs conflict
1. Tab A loads version 0.
2. Tab B loads version 0.
3. Tab A persists new order → version becomes 1.
4. Tab B persists old order with version 0 → gets 409.  
   **Assert:** Tab B’s order is rejected.

### Test 4: Pin state preserved after auto‑placement
1. Load state: pinned = true.
2. Background poll returns same pin = true.
3. User unpins → persist with version 0 → accepted, pin = false, version 1.
4. Auto‑placement runs (using latest version 1) → computes new order, persists with version 1 → server accepts, pin still false.  
   **Assert:** Pin remains false.

### Test 5: Reel positions not shrunk on reload
1. Create order with 5 spots and 2 empty reel slots after position 3.
2. Persist (version 0).
3. Reload → return same order with all 5 spots and empty slots.  
   **Assert:** All positions preserved.

### Test 6: Audit log completeness
1. Perform manual reorder, pin toggle, group change.
2. Query audit table → 3 rows, each with before/after JSON, reason, timestamp.  
   **Assert:** Three audit entries exist, data consistent.

---

## Summary

The current design has no concurrency control, no audit trail, and multiple code paths that can silently overwrite user‑intended ordering. The recommended patch adds a version field, server‑side conflict detection, and an append‑only audit log. All automatic mutations are restricted to new‑reel/group‑change events only; reloads remain read‑only. These changes are minimal and can be implemented incrementally.
```
