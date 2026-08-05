# MOMA Comment Extraction – Implementation Recommendation

## 1. Current Comment Write/Read Flow and Concrete Weaknesses

**Current flow (inferred from file structure and naming):**  
- `moma_db.py` contains a Python `MomaDb` class that interacts with a SQLite database (and optionally Cloudflare D1 via `moma_db_worker.js`).  
- Comments are likely stored as a simple string column (`comment`) on the `reel` or `job` table, overwritten on each write.  
- The GUI in `combo_gui.py` provides a text field and a “Save Comment” button that calls `db.save_comment(job_id, text)`.  
- No separate comment history table – each comment replace the previous one. Timestamps are not recorded per edit.  
- No mechanism to mark a comment as “processed” by an external session.  
- No ordering guarantee for multiple comments on the same job (only last one exists).  

**Concrete weaknesses:**  
1. **Loss of edit history** – each new comment overwrites the previous, making it impossible to track evolving review feedback.  
2. **No independent timestamps** – cannot order comments across jobs or determine freshness.  
3. **No processed-tracking** – external sessions cannot fetch only new/unread comments without manual bookkeeping.  
4. **Single comment per job** – if reviewers need to leave multiple remarks (e.g., for different issues) they must either append or break the data model.  
5. **No chronological order guarantee** – without a `created_at` column, sorting by internal rowid may be fragile.  
6. **Concurrent edits** – two sessions could overwrite each other’s comments silently.

## 2. Minimal Durable Schema

Create a new table `review_comments` to store each comment as an independent event. Keep the original `comment` column on the job table *only* as a convenience for display (optional). The new schema:

```sql
CREATE TABLE IF NOT EXISTS review_comments (
    id          TEXT PRIMARY KEY,          -- UUID v4
    job_id      TEXT NOT NULL,             -- FK to job (reel identity)
    prompt      TEXT NOT NULL,             -- snapshot of the reel prompt at creation time
    body        TEXT NOT NULL,             -- comment text
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),  -- ISO-8601, immutable
    processed   INTEGER NOT NULL DEFAULT 0   -- 0 = fresh, 1 = incorporated
);

CREATE INDEX idx_rc_job_id ON review_comments(job_id);
CREATE INDEX idx_rc_created ON review_comments(created_at);
CREATE INDEX idx_rc_unprocessed ON review_comments(processed, created_at);
```

**Rationale:**  
- Every write creates a new row – no overwrites.  
- `prompt` is captured at comment creation (re-read from job table) so extraction includes the exact prompt.  
- `created_at` is set once and never updated (immutable).  
- `processed` flag is updated atomically when a session acknowledges the comment.  
- Index on `(processed, created_at)` makes fetching all unprocessed comments in chronological order a simple range scan.  

If D1 is used, replace `datetime('now')` with `(datetime('now'))` (D1 supports SQLite datetime functions). The UUID can be generated in Python (`uuid.uuid4().hex`) or via extension.

## 3. Exact Proposed HTTP Endpoints and One-Command Python Interface

### HTTP Endpoints (to be implemented in `moma_db_worker.js` – Workers or Express)

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST   | `/api/comments` | Create a new comment | `{ job_id, body }` | `{ id, job_id, prompt, body, created_at, processed }` (201) |
| GET    | `/api/comments/unprocessed` | Fetch all unprocessed comments, oldest first | – | Array of comment objects |
| PATCH  | `/api/comments/:id/processed` | Mark a single comment as processed | – | 200 OK |

### One-Command Python Interface (`MomaDb` class extension)

```python
# Inside moma_db.py

class MomaDb:
    # ... existing methods ...

    def add_comment(self, job_id: str, body: str) -> dict:
        """Create a new comment for a job. Returns the new comment record."""
        prompt = self.get_job_prompt(job_id)  # retrieve current prompt
        comment_id = uuid.uuid4().hex
        self.execute(
            "INSERT INTO review_comments (id, job_id, prompt, body) VALUES (?, ?, ?, ?)",
            (comment_id, job_id, prompt, body)
        )
        return self.get_comment(comment_id)

    def get_fresh_comments(self) -> list:
        """Return all unprocessed comments ordered by created_at, with prompt."""
        return self.query(
            "SELECT id, job_id, prompt, body, created_at FROM review_comments "
            "WHERE processed = 0 ORDER BY created_at ASC"
        )

    def mark_comment_processed(self, comment_id: str) -> None:
        """Mark a single comment as processed so it won't appear in fresh fetch."""
        self.execute(
            "UPDATE review_comments SET processed = 1 WHERE id = ?",
            (comment_id,)
        )

    # Optional: clear comment history for a job (admin use)
    def clear_job_comments(self, job_id: str) -> int:
        """Delete all comments for a job. Returns number deleted."""
        self.execute("DELETE FROM review_comments WHERE job_id = ?", (job_id,))
        return self.cursor.rowcount  # or D1 equivalent
```

**Usage example for a session:**
```python
db = MomaDb()
for comment in db.get_fresh_comments():
    process(comment["prompt"], comment["body"])
    db.mark_comment_processed(comment["id"])
```

## 4. Compatibility: Cloudflare D1 and Local SQLite

Both SQLite and D1 share the same SQL dialect for this schema. Potential pitfalls and solutions:

- **UUID generation**: Python’s `uuid` module works locally; on D1 worker, use `crypto.randomUUID()` (JavaScript) or generate in Python before sending to HTTP. Alternatively, use `hex(random.getrandbits(128))`.  
- **`datetime('now')`**: supported in both. Ensure timezone is UTC (default).  
- **`processed` flag updates**: simple `UPDATE` works; D1 uses batch writes if atomicity is critical, but single row update is fine.  
- **Index creation**: same syntax.  
- **`INSERT ... RETURNING`**: Not standard in SQLite/D1. Instead, `INSERT` then `SELECT` (or return from Python after insert).  
- **Concurrency**: SQLite has writer lock; D1 uses serializable isolation per request. For local use, wrap in `BEGIN IMMEDIATE` if multiple writers. For D1, each request is a single transaction.  
- **Migration**: Use a versioned schema file (e.g., `migrations/002_add_review_comments.sql`). Apply on startup if table doesn’t exist.

**Recommended adapter pattern** in `moma_db.py`:
```python
def _ensure_tables(self):
    self.execute("""
        CREATE TABLE IF NOT EXISTS review_comments (
            id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            prompt TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            processed INTEGER NOT NULL DEFAULT 0
        )
    """)
    self.execute("CREATE INDEX IF NOT EXISTS idx_rc_unprocessed ON review_comments(processed, created_at)")
```

## 5. Test Checklist

| # | Scenario | Expected Behaviour |
|---|----------|-------------------|
| 1 | **Add single comment** | New row appears; `created_at` is set; `processed` = 0. |
| 2 | **Add two comments on same job** | Two rows, same `job_id`, different `id` and `created_at`. |
| 3 | **Add comments on two different jobs** | Both fetched by `get_fresh_comments` in chronological order. |
| 4 | **Fetch fresh comments after mark** | Marked comment absent; unmarked present. |
| 5 | **Ordering by time** | Comments added out of order (e.g., old job then newer) return sorted by `created_at asc`. |
| 6 | **Idempotent mark** | Marking same `comment_id` twice does not error; no duplicate effect. |
| 7 | **Edit a comment** | Should NOT update existing row – add a *new* comment row. Verify old row still exists with original timestamp. |
| 8 | **Clear comments for a job** | Deletes all rows for that job; other jobs untouched. Then fresh fetch does not include them. |
| 9 | **Concurrent session A & B** | Both fetch same fresh comments; A marks one, B marks another: both updates succeed independently (no lost update). |
| 10 | **Prompt snapshot** | If prompt changes after comment is written, the `prompt` field in the comment row retains the prompt at time of comment creation. |
| 11 | **Empty comment body** | Should be allowed (empty string) or rejected? Decide and test accordingly. |
| 12 | **Database migration** | Running on existing database creates new table without breaking existing tables. |

## 6. Specific Files/Functions to Modify

| File | Modification |
|------|--------------|
| `sc10/combo_runner/code/moma_db.py` | Add `_ensure_tables()` call (or migration). Add methods: `add_comment`, `get_fresh_comments`, `mark_comment_processed`, `clear_job_comments`. Modify `get_job_prompt()` helper if needed. |
| `sc10/combo_runner/code/moma_db_worker.js` | Add HTTP handlers for `POST /api/comments`, `GET /api/comments/unprocessed`, `PATCH /api/comments/:id/processed`. Ensure they call the new Python methods (or replicate SQL logic in JS if using Cloudflare Workers as a separate server). |
| `sc10/combo_runner/code/combo_gui.py` | Update the “Save Comment” button to call `add_comment()` instead of overwriting. Optionally add a “Mark all processed” button or integrate with session logic. |
| `sc10/combo_runner/code/batches.py` | If batch operations (e.g., marking all comments for a batch run as processed) are needed, add a method `mark_batch_comments_processed(batch_id)`. |
| Test files | Create `test_review_comments.py` covering the checklist. Add a migration script (e.g., `migrations/002_add_review_comments.sql`). |

**Priority:**  
1. Schema + `moma_db.py` methods.  
2. `moma_db_worker.js` endpoints.  
3. GUI integration.  
4. Batch utilities and tests.  

**Remarks:**  
- Do not change existing `comment` column on job table – it can remain as a convenience display field.  
- The `get_fresh_comments` command is the single clean API for a session: one call returns everything needed (`id`, `job_id`, `prompt`, `body`, `created_at`).  
- Use UUIDs rather than auto-increment to avoid accidental ordering assumptions and to simplify D1 idempotency.  
- Ensure all writes use parameterised queries to prevent injection.
