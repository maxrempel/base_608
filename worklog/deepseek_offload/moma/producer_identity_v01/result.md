# MoMA Producer-Session Provenance Audit – Risk Assessment

## Limitations
Actual file contents could not be accessed (no filesystem available). Risks below are inferred from the described changes and typical implementation patterns for similar systems (JavaScript localStorage, Python workers, SQLite state, HTTP APIs). A real audit would require direct review of each listed file.

---

## Change 1: Shared Permanent Scene/Arrangement Selection

### Correctness Risks
- **Race condition between storage events and app-state polling**: If background polling runs on a timer and overwrites a valid local selection (expected scenario), user changes could be silently reverted. The polling logic must check `localStorage` before writing.
- **Cross-tab propagation**: `localStorage` storage events are only fired in other tabs on the same origin, not the originating tab. The originating tab must update its own state directly after writing.
- **Initial load**: On first visit (no saved selection), a default must be set without erasing a selection that another tab may have just written. A simple "if null set default" is safe; but if the default is computed asynchronously, a lost update could occur.
- **Reset on code update**: If the application rebuilds its state from an in-memory default (e.g., from a server response) on every page load, the saved `localStorage` value may be overwritten if the code does not check for existing saved selection first. The restoration logic must “hydrate” from `localStorage` before any asynchronous fetch.

### Concurrency Risks
- **Tab A writes selection X, tab B writes selection Y**: Both tabs receive storage events and update their views correctly. However, if a third tab is mid-poll when the event fires, it may still overwrite. Need atomic read-compare-write or use `storage` event as authoritative update.
- **Background polling worker (e.g., `combo_sync_worker`)**: If it periodically saves app state, it must not touch `localStorage` for selection without explicit user intent.

### Privacy Risks
- **localStorage is per-origin, not per-tab**: Any extension or site on the same origin could read the selection. No sensitive data, but if selection reveals user’s project preferences, consider clearing on logout.

### Backward Compatibility / Schema Migration
- **No migration needed**: `localStorage` is schema-less. However, if the key format changes (e.g., `sceneSelection_v1` to `v2`), old stored values become stale. A version key or migration logic on first read is recommended.

### Recommended Tests
1. **Cross-tab propagation**: Open two tabs, change selection in Tab A, verify Tab B updates within 100ms. Change in Tab B, verify Tab A updates.
2. **Polling override test**: Simulate background polling that returns a different default. Verify that a valid saved selection is not overwritten.
3. **Code update survival**: Change the selection, simulate a page reload (or ctrl+F5). Verify the selection persists.
4. **Initial empty state**: Clear localStorage, load page, verify default selection appears and is immediately saved.

---

## Change 2: Producer-Session Identity in Job Rows (D1 columns + Tag)

### Correctness Risks
- **`CODEX_THREAD_ID` uniqueness**: If multiple jobs are fired from the same thread (e.g., in a loop), all rows will share the same `producer_session_id`. That may be intentional, but if each job should have a unique session, a counter or UUID must be appended.
- **Fallback to SQLite**: The helper reading `~/.codex/state_5.sqlite` may fail if the file is locked, missing, or in an unexpected format. Must handle exceptions gracefully and fall back to env vars or a default.
- **Override priority**: `MOMA_PRODUCER_*` env vars should override SQLite title, but must not override `CODEX_THREAD_ID` (which is the session ID). Clarify which env var controls which column.
- **Tag truncation**: Display tag ≤10 characters. If the generated tag (e.g., from the agent name) is longer, it must be truncated without corrupting multi-byte UTF-8. Use `String.slice(0, 10)` on byte‑safe strings or use a Unicode-aware truncation.

### Privacy Risks
- **`CODEX_THREAD_ID` exposure**: This identifier may be logged in worker job logs. If it is a trace that can be linked to a user or project, ensure logs are sanitized in non‑debug deployments.
- **`~/.codex/state_5.sqlite`**: Contains potentially sensitive internal state (e.g., project names, user ids). Reading it only for a display title is acceptable, but the worker must not write or propagate its contents beyond the intended columns.

### Concurrency Risks
- **SQLite reads in worker**: Multiple workers may read `state_5.sqlite` simultaneously. SQLite supports concurrent readers via WAL mode, but if the file is locked by another process (e.g., Codex itself), the read may block or timeout. Use a short timeout and fallback.
- **Row insertion contention**: The `fire_job` path must insert a D1 row with the session columns. If D1 is transactional (e.g., Cloudflare D1), ensure retry logic for serialization conflicts.

### Schema Migration & Inheritance
- **New columns**: Existing D1 tables have no `producer_session_*` columns. Requires a migration (ALTER TABLE ADD COLUMN) which is safe for D1 if columns are nullable. Backfill old rows with NULLs or default values.
- **Worker code**: All workers (`combo_lipsync_worker`, `combo_wan26au_worker`, etc.) must propagate these columns from the job input to the output or next stage. Any worker that reads or writes job rows must be updated to include these columns; otherwise they will be lost (inheritance break).
- **Storyboard APIs**: Must return these columns. Existing clients (Storyboard 4 HTML) that ignore extra fields are safe; but the tooltip code must handle missing `producer_session_name` gracefully if it is NULL for old jobs.

### Backward Compatibility
- **Old job rows**: Will have NULLs for new columns. The tooltip should display “unknown” or omit the section if all session fields are NULL.
- **Old workers**: If a worker that is not updated still creates a job row, the insertion will fail (because D1 expects columns) unless the schema allows NULL defaults or the insertion code supplies placeholder values. A safe default is to set all producer columns to NULL if not provided.
- **Email/paging tools**: Any downstream consumers of job rows (e.g., dashboards, alerts) that select `*` will receive new columns; ensure they do not break on unexpected fields.

### Recommended Tests
1. **Insert with full identity**: Call `fire_job` with all env vars set and a `CODEX_THREAD_ID`. Verify D1 row has correct values.
2. **Fallback to SQLite**: Clear `MOMA_PRODUCER_*` env vars, ensure `~/.codex/state_5.sqlite` has a matching thread ID. Verify `producer_session_name` is read correctly.
3. **Missing SQLite file**: Delete the state file. Verify worker falls back to a default (e.g., "unknown") without crashing.
4. **Tag truncation**: Set a tag string of length 20. Verify stored tag is truncated to 10 chars (and that no multi-byte character is broken in half).
5. **Worker propagation**: Submit a job through the full pipeline, verify every intermediate worker log prints the tag without error, and all derived rows contain the columns.
6. **Storyboard display**: Create a job with full identity. In Storyboard 4, verify that the reel thumbnail shows the tag and tooltip shows all five fields. Then check an old job (NULL columns) – tooltip shows no producer section.
7. **Schema upgrade**: Run migration on a non‑empty table. Verify old rows keep existing data and new inserts populate the columns.

---

## Summary of High‑Risk Areas
| Area | Risk | Mitigation |
|------|------|------------|
| localStorage polling override | Lost user selection | Check saved selection before polling write |
| Cross‑tab race | Temporary inconsistency | Use storage event as trigger, not poll |
| SQLite read in worker | Blocked or missing file | Short timeout + fallback env/default |
| Worker column propagation | Lost session identity | Update all workers; add assertion in test |
| Schema migration on D1 | Existing rows break queries | Add columns with NULL default, update all `SELECT *` consumers |

**Recommendation**: Implement the two changes incrementally, with unit and integration tests covering the bullet points above before merging.
