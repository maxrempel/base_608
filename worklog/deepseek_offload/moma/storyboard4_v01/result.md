# result.md

## Audit Limitation
Cannot access the specified files (`storyboard_editor_v2.html`, `storyboard_editor_v3.html`, `slideshow_server_v01.py`) due to environment constraints. The following analysis is based on typical API contracts implied by the descriptions.

## Assumed Data Contract Differences

| Aspect | `/api/approved_images` (assumed) | `/api/sb_pool` (assumed from context) |
|--------|----------------------------------|----------------------------------------|
| **Returned objects** | Flat list of approved still images (e.g., `{id, filename, approved, sort_order}`) | Structured scenes with nested arrangements, roles, junk state, curated bin order |
| **Scene scoping** | Not present | Each item belongs to a scene, with scene metadata (name, order) |
| **Arrangement/role data** | Not present | Each scene contains arrangement variants (e.g., `arrangement_id`, `role_tag`, `position`) |
| **Junk state** | Not present | Items can be flagged as junk (boolean `is_junk`) |
| **Curated bin order** | Simple sort order | Complex ordering per scene/bin (user-defined, auto-placement) |
| **Automatic placement** | Not present | Server-side logic that assigns items to slots based on rules |
| **Quiet polling** | Not present | Endpoint supports polling with `since` timestamp for incremental updates |
| **Completion status** | Not present | Output media (rendered videos, audio) include status fields like `completed`, `progress` |
| **Named projects** | None | Pool items belong to a `project` (named set) |
| **Input stills** | Only approved stills (final) | Pool includes input stills (some not yet approved) and completed output media |

## Required Changes for Storyboard 4 Parity
The goal is a new endpoint `/api/sb_pool_v4` that replicates all current `/api/sb_pool` behavior but moves pile/scene/arrangement/role/junk filtering **server-side** (as Storyboard 3 attempted). Must **not** modify existing endpoints or routes.

### Smallest Safe Implementation
1. **Copy `slideshow_server_v01.py`** → `slideshow_server_v02.py` (or add versioned handler)
2. **Add endpoint** `/api/sb_pool_v4` that:
   - Accepts query parameters: `scene_id`, `arrangement_id`, `role`, `include_junk`, `exclude_completed`
   - Returns the same structure as `/api/sb_pool` but filtered server-side
   - Preserves `since` polling parameter for incremental updates
   - Maintains all existing fields (including completed output media, input stills, project scoping)
3. **Create `storyboard_editor_v4.html`** that:
   - Points all AJAX calls to `/api/sb_pool_v4` instead of `/api/sb_pool`
   - Sends current filter state as query parameters
   - Removes client-side filtering logic that was in v2 (but keep as comment for fallback)
   - Keep all UI features exactly as v2

### Data Contract Preservation Checklist
- [ ] Input stills (approved and unapproved) – same field names
- [ ] Completed output media – same structure
- [ ] Field names/statuses – identical to /api/sb_pool
- [ ] Named projects – include `project` field
- [ ] Scene scoping – `scene` object with `id`, `name`, `order`
- [ ] Arrangements – nested array of `arrangement` objects
- [ ] Junk state – `is_junk` boolean
- [ ] Curated bin order – `bin_order` integer, preserved per scene
- [ ] Automatic placement – server-side logic identical to v2 but now computed before returning
- [ ] Quiet polling – keep `since` parameter support

### Focused Tests
1. **Equivalence test**: For identical filters, `/api/sb_pool_v4` returns same array as client-side filtered `/api/sb_pool`
2. **Filter correctness**: Each query parameter (`scene_id`, `arrangement_id`, `role`, `include_junk`) produces expected subset
3. **Polling**: `since` timestamps return only changed items
4. **Non-regression**: `/api/approved_images` and `/api/sb_pool` still respond exactly as before
5. **UI parity**: Storyboard 4 page looks and behaves identical to Storyboard 2 for all user actions

## Recommendation
Proceed with minimal server-side filtering addition. Do not touch `/api/sb_pool` or v2 HTML. Use v4 as a drop-in replacement that offloads filtering to the server, reducing client complexity while preserving all existing behavior.
