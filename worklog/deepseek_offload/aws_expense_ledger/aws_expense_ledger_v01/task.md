# AWS expense ledger implementation review

Last edited: 2026-07-28 by Codex (GPT-5.6 SOL)

Act as a senior Python reliability engineer. Produce a compact, concrete
implementation blueprint and test matrix for this change.

Existing system:

- A Python standard-library-only service on an always-on AWS Lightsail host.
- SQLite tables include `reports(ts, provider, category, model, usd, note,
  source_id)` with a unique partial index on `(provider, source_id)`.
- Providers are either `balance` (authoritative spend comes from prepaid balance
  deltas) or `meter` (authoritative spend is the sum of report rows).
- A poller runs every five minutes, but expensive provider APIs should be called
  only every six hours.
- Dashboard, aggregate email, and Telegram/audio summaries enumerate a fixed
  provider registry and order.
- The host runs Python 3.11 and currently has no third-party Python packages.
- AWS Cost Explorer `GetCostAndUsage` is available and returns daily
  `UnblendedCost`, grouped by `SERVICE`. Current-day values are estimated and
  may be revised.
- AWS request signing must use pure Python standard library. AWS access material
  will live only in a protected server-side file and must never be logged.

Requested behavior:

1. Add AWS as a first-class provider in the combined expense ledger.
2. Refresh AWS costs four times daily without multiplying the bill.
3. Backfill daily costs from 2026-01-01 onward, grouped by AWS service.
4. Reconcile revised Cost Explorer estimates by updating the same rows, using
   stable source IDs; do not append duplicates.
5. Preserve historical rows and never turn a temporary API failure into zero.
6. Include AWS in dashboard, grand totals, milestone email, Telegram, and audio.
7. Convert the existing scheduled DeepSeek-only Telegram report into a combined
   expense report while retaining DeepSeek and FishAudio balances.
8. Give specific failure handling, retry, UTC date-boundary, SQLite upsert, and
   AWS Signature Version 4 recommendations.
9. Provide a focused unit/integration test matrix, including deterministic
   signing tests and idempotent revised-estimate tests.

Do not write a broad essay. Return an ordered implementation checklist,
important pseudocode or SQL fragments, and tests. Call out any double-counting
or historical-accuracy traps.
