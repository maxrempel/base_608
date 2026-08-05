# result.md

## Producer-Session Identity Feature Audit

### 1. What Works and What Is Missing

**Works:**
- Producer metadata capture: `producer_identity.ts` in `combo-runner/src` reads `X-Producer-Id` header and writes to `producer_metadata` table (D1) with columns `job_id`, `producer_id`, `created_at`.
- `fire_job` function (`combo-runner/src/fire_job.ts`) extracts the metadata and passes it as part of `JobContext` to the Sound Assembly pipeline.
- Sound Assembly (`sound-assembly/src/storyboard4/pool.ts`) creates a Storyboard 4 pool entry using the job’s `producer_id` as a string field `producerRef`.
- The Storyboard 4 badge component (`sound-assembly/src/storyboard4/badge.ts`) reads a `badgeData` object and renders a visual badge on the primary spine UI.

**Missing:**
- The badge component does not receive the `producer_id` from the pool entry. The data flow stops at the pool: `pool.ts` stores `producerRef` but does not expose it through the API response used by the badge.
- The Storyboard 4 API endpoint (`/api/v1/storyboard4/badge`) queries only `pool_id` and `spine_id`; it never includes `producer_id` in the response.
- The D1 table `producer_metadata` lacks a `session` column needed to differentiate multiple sessions from the same producer. The current schema only maps job→producer, not job→session.
- No migration script exists for the missing `session` field; the D1 HTTP API is configured with `ALTER TABLE` disabled.

### 2. Safest Minimal Schema & Migration Route

**Assumption:** Public D1 HTTP API rejects `ALTER TABLE`; direct D1 queries via Wrangler or D1 Console are allowed.

**Minimal schema change (in `combo-runner/schema.sql`):**
```sql
CREATE TABLE IF NOT EXISTS producer_metadata (
  job_id TEXT PRIMARY KEY,
  producer_id TEXT NOT NULL,
  session_id TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
```
*Note: We add `session_id` with a default empty string. Existing rows become session `''`; the application must handle this gracefully.*

**Migration route (safe, no downtime):**
1. Deploy new application code that writes `session_id` from the `X-Producer-Session` header (or from a combined `X-Producer-Identity: <id>:<session>`).
2. Manually run a Wrangler migration (or D1 Console) to add the column:
   ```sql
   ALTER TABLE producer_metadata ADD COLUMN session_id TEXT NOT NULL DEFAULT '';
   ```
   Even though the HTTP API might reject ALTER, this is executed locally or via the Wrangler CLI, which uses the same D1 service with full SQL permissions. (Double-check D1 plan – if the public HTTP API is the only allowed interface, fallback to recreating the table.)
3. If no ALTER is possible, recreate the table in a new name and copy data via a script:
   ```sql
   CREATE TABLE producer_metadata_v2 (... with session_id);
   INSERT INTO producer_metadata_v2 SELECT job_id, producer_id, '', created_at FROM producer_metadata;
   DROP TABLE producer_metadata;
   ALTER TABLE producer_metadata_v2 RENAME TO producer_metadata;
   ```

**Recommended:** Use Wrangler `d1 migrations` – it does allow ALTER TABLE via the managed migration framework, which bypasses the public HTTP API restrictions.

### 3. Specific Failure Modes / Compatibility Traps

- **Missing session_id in old jobs:** The badge may show producer id without session. Ensure badge component can handle `session_id === ''` gracefully (e.g., show producer id only).
- **Duplicate producer+session identification:** Without a unique constraint on (producer_id, session_id), the same session could be recorded multiple times for different jobs. Add `UNIQUE(producer_id, session_id)` only if required; otherwise accept multiple rows.
- **Storyboard 4 pool API contract:** If `pool.ts` expects a flat `producerRef` but the badge expects a structured `{ id, session }`, the types will break. Define a shared TypeScript interface in `types.ts` and enforce with runtime checks.
- **Badge rendering race:** The badge component may render before the D1 query completes. Ensure `async` data loading with skeleton UI.
- **D1 HTTP API ALTER TABLE rejection:** If the migration script relies on ALTER via the HTTP API (e.g., a cron job using `fetch`), it will silently fail. Always use Wrangler or D1 Console for schema changes.
- **Storyboard 4 pool scaling:** The pool might be in a different D1 binding than producer metadata. Ensure both bindings use the same database.

### 4. Recommended Patch Plan

| # | File / Function | Change |
|---|----------------|--------|
| 1 | `combo-runner/src/producer_identity.ts` | Extract `X-Producer-Session` (or parse combined identity) and store in new `session_id` field. Update insert statement. |
| 2 | `combo-runner/schema.sql` | Add `session_id` column as `TEXT NOT NULL DEFAULT ''`. |
| 3 | `combo-runner/src/fire_job.ts` | Include `session_id` in `JobContext.producerSession`. |
| 4 | `sound-assembly/src/storyboard4/pool.ts` | Accept `session` from `JobContext.producerSession` and store as part of pool entry (e.g., `producerSession` field). |
| 5 | `sound-assembly/src/storyboard4/badge.ts` | Update type `BadgeData` to include `producerSession: string`. Modify render to display both producer id and session (e.g., "p123 (session abc)"). |
| 6 | `sound-assembly/src/api/storyboard4/badge.ts` | Modify SQL query to join or fetch `session_id` from `producer_metadata` table (if not in pool entry) and include in response. |
| 7 | Migration script | Create `migrations/001_add_session_id.sql` with `ALTER TABLE producer_metadata ADD COLUMN session_id TEXT NOT NULL DEFAULT '';` Apply via `wrangler d1 migrations apply`. |
| 8 | Integration test | Add test that verifies full chain: request with `X-Producer-Id` + `X-Producer-Session` → badge shows producer and session. |

All changes are backward-compatible; existing rows default to empty session, and badge code handles empty.
