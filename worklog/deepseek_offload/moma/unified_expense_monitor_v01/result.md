**Compact critique**  
The design is fundamentally sound but harbors a concrete double-counting trap for FishAudio, several operational delivery gaps, and a timestamp consistency hazard. The unique-index idempotency pattern is appropriate.

**Risks**

1. **Double-counting for FishAudio** – Central ledger already holds authoritative FishAudio spend from prepaid balance deltas. MoMA reports will send the same usage amounts to the `fishaudio` provider. Unless the central ledger explicitly marks MoMA reports as **non-additive** (e.g., zero amount or a dedicated flag), every MoMA FishAudio submission will inflate the total. The proposal states “reports only categorize usage” but provides no mechanism to prevent the ledger from summing them.

2. **Delivery loss for live rows** – `best-effort POST` without retry or queue means a transient failure (central ledger down, network issue) permanently loses that cost from the unified monitor. The CLI backfill covers historical rows, but live expenses will be orphaned.

3. **Timestamp mismatch** – Using `lastrowid` from D1 insert does not guarantee the stored timestamp matches the original API call time, especially if insert is deferred. Central ledger’s `event_ts` should reflect the actual expense moment, not the logging time.

4. **CLI backfill on unready schema** – If the central ledger’s partial index on `(provider, source_id)` is not yet created, the backfill will fail on duplicate key errors or silently insert duplicates. No validation step is described.

5. **NULL cost rows** – FishAudio rows have `NULL cost`. Sending them as `usd=0` could still be recorded and later misinterpreted as legitimate spend. The CLI targets “non-null” rows, but the live recording path may attempt to send NULL-valued rows, potentially causing an error or a zero-cost entry.

6. **Central ledger schema evolution** – Adding `source_id` and `event_ts` requires API and database changes. If these are deployed after MoMA starts sending, early submissions will be rejected or silently dropped.

**Concrete corrections**  

- For FishAudio: modify the central ledger `/spend` to accept an optional `non_additive` boolean (or similar). When true, the amount is recorded but not summed into the provider’s headline total. MoMA must set this flag for all FishAudio reports. Alternatively, send amount `0` and store the usage breakdown in a separate metadata field.

- Implement a persistent retry queue (e.g., in D1 or a local file) for live POSTs. On failure, requeue the payload; purge only after receiving a success response (or duplicate-conflict which is acceptable).

- Ensure `expense_log.record()` uses the API call’s original timestamp as `event_ts`, not the D1 insertion time. Store that timestamp in the D1 row.

- In the `--sync-ledger` CLI, first check that the central ledger’s unique index exists (e.g., by querying the ledger’s schema endpoint or attempting a dummy insert). If missing, abort with a clear message.

- For NEW NULL rows (not yet in D1), skip live POST entirely. For existing NULL rows in the backfill, do not send. The CLI already handles this with “non-null”, but ensure the live path also checks for `cost IS NOT NULL`.

- Coordinate deployment: roll out central ledger schema changes (new columns, partial index) **before** enabling MoMA’s live submissions. Use a rollback plan if the ledger is not ready.

- (Optional) Add a `source` field (e.g., `"moma"`) to `/spend` so the ledger unambiguously identifies report origin, easing future audits.
