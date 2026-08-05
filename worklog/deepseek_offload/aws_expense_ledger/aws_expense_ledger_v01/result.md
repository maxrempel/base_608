## Implementation Blueprint: AWS Expense Ledger

### 1. Data Model & Index

```sql
-- Existing table unchanged. Partial unique index guarantees idempotency.
CREATE UNIQUE INDEX IF NOT EXISTS idx_reports_provider_source
ON reports(provider, source_id);
```

**AWS source_id:** `"YYYY-MM-DD_ServiceName"` (e.g. `"2026-07-28_AmazonS3"`)  
**ts:** UTC datetime of the API call (not the cost date).  
**usd:** `UnblendedCost` as float.  
**note:** free-text – can store "CostExplorer daily estimate" or "revised".  
**category:** leave empty or map to a generic "AWS" – grouping by service is done via model column (model = service name).

No schema migration needed – existing columns suffice.

### 2. AWS Signature V4 (pure stdlib)

**Pseudocode (core functions):**

```python
import hashlib, hmac, datetime, urllib.parse

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(secret_key, datestamp, region, service):
    kDate = sign(('AWS4' + secret_key).encode('utf-8'), datestamp)
    kRegion = sign(kDate, region)
    kService = sign(kRegion, service)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def build_canonical_request(method, uri, query_params, headers, payload_hash):
    canonical_uri = uri  # e.g. '/'
    canonical_querystring = urllib.parse.urlencode(sorted(query_params.items()))
    canonical_headers = '\n'.join(f"{k.lower()}:{v}" for k,v in sorted(headers.items())) + '\n'
    signed_headers = ';'.join(sorted(h.lower() for h in headers))
    return f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

def create_sigv4_request(access_key, secret_key, region, service, method, uri, query_params, payload=b''):
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    payload_hash = hashlib.sha256(payload).hexdigest()

    headers = {
        'host': f'{service}.{region}.amazonaws.com',
        'x-amz-date': amzdate,
        'x-amz-content-sha256': payload_hash,
    }

    canonical_request = build_canonical_request(method, uri, query_params, headers, payload_hash)
    credential_scope = f'{datestamp}/{region}/{service}/aws4_request'
    string_to_sign = f'AWS4-HMAC-SHA256\n{amzdate}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}'
    signing_key = get_signature_key(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    headers['Authorization'] = f'AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
    return headers
```

**Critical:** Never log `headers['Authorization']` or the secret key. Load credentials from a file with `chmod 600`; trap reading errors gracefully.

### 3. AWS Cost Explorer API Call (every 6 hours)

**Poller logic (extend existing 5-minute loop):**

```python
def should_fetch_aws(last_aws_sync_file):
    try:
        with open(last_aws_sync_file) as f:
            last_sync = datetime.fromisoformat(f.read().strip())
    except (FileNotFoundError, ValueError):
        return True
    return (datetime.utcnow() - last_sync).total_seconds() >= 6 * 3600

# In poller:
if should_fetch_aws('/var/run/last_aws_sync'):
    try:
        # Retry with exponential backoff (max 3 attempts, 1/2/4 min interval)
        for attempt in range(3):
            try:
                aws_rows = fetch_cost_explorer(time_start, time_end)  # backfill last 3 days to catch revisions
                sync_aws_to_sqlite(aws_rows)
                write_last_sync(datetime.utcnow())
                break
            except Exception:
                if attempt == 2: raise
                time.sleep((2**attempt) * 60)
    except Exception:
        log.warning("AWS sync failed – rows unchanged.")
```

**fetch_cost_explorer:**  
- Requests `Granularity=DAILY`, `Metrics=UnblendedCost`, `GroupBy=SERVICE`.  
- `TimePeriod` = last 3 days (today inclusive). Backfill from 2026-01-01 via separate one-time script.  
- Convert API response to list of tuples `(date, service, cost)`.  
- **Never insert zero rows:** if API fails for a day, skip it – no zero insertion. Existing rows remain.

### 4. Upsert & Reconciliation

```python
def upsert_aws_row(ts, date_str, service, cost):
    source_id = f"{date_str}_{service}"   # e.g. "2026-07-28_AWSLambda"
    cur.execute("""
        INSERT INTO reports (ts, provider, category, model, usd, note, source_id)
        VALUES (?, 'aws', '', ?, ?, 'CostExplorer', ?)
        ON CONFLICT(provider, source_id) DO UPDATE SET
            usd = excluded.usd,
            note = excluded.note,
            ts = excluded.ts
    """, (ts, service, round(cost,6), source_id))
```

**Why it works:**  
- Same `date_service` re-insert triggers conflict and updates the cost (revised estimate).  
- No duplicates because of the partial unique index.  
- Historical rows stay after conflict update – they are replaced, not appended.

### 5. Backfill Script (one-time)

- Run outside poller, e.g. `python backfill_aws.py 2026-01-01 2026-07-27`.  
- Same upsert logic but skip if `usd` round-trip is 0 (avoid inserting zero-cost services – Cost Explorer may include $0 services).  
- Handle pagination (Cost Explorer granularity=DAILY can return many pages for many services).  
- Use same retry logic, no zero insertion.

### 6. Dashboard & Outputs

Add AWS to the **fixed provider registry** (a list or dict variable). Ensure AWS appears after FishAudio and before any future providers. In aggregation queries:

```sql
SELECT provider, SUM(usd) as total
FROM reports
WHERE provider IN ('balance', 'meter', 'aws')
  AND ts >= ?
GROUP BY provider
```

For grand totals, simply sum across all providers. Milestone email, Telegram summary, audio script must iterate the same list.

**Order:** [Balance, FishAudio, DeepSeek, AWS] – adjust if existing order is different.

### 7. Double-Counting & Historical Accuracy Traps

- **Double-counting:** If AWS costs are also recorded via a balance delta (prepaid) you would double-count. Confirm that AWS is NOT already included in the `balance` provider. If it is, you must exclude AWS rows from the balance sum or vice versa. **Recommendation:** explicitly subtract AWS rows when summing balance provider if balance includes AWS credits.  
- **Temporary API failure:** The code above leaves existing rows in place – never inserts a zero. Good.  
- **UTC boundary:** All timestamps should be UTC. Cost Explorer `TimePeriod` uses UTC dates. Ensure `date_str` is YYYY-MM-DD in UTC.  
- **Partial backfill:** If backfill fails mid-way, re-run is idempotent – same source_ids update without duplication.  
- **Revised current day:** Next poll at 6h will overwrite the same source_ids with new estimates. This is correct.  
- **Service name changes:** Cost Explorer may rename services; source_id uses the exact name from API – no crosswalk needed.  
- **Zero cost services:** If a service had $0 cost for a day, API may return a row with 0. The upsert will write it. Avoid inserting rows with `usd = 0` if you want to hide them, but that is a presentation choice. For accuracy, storing $0 is acceptable.

## Test Matrix

| ID | Test | Scope | Details |
|----|------|-------|---------|
| T1 | SigV4 deterministic signing | Unit | Given fixed date, region, credentials, compute signature and compare to known golden value (pre-recorded). Must produce identical signed headers. |
| T2 | Upsert idempotency (same source_id) | Unit | Insert row with source_id '2026-07-28_AmazonS3', then again with same source_id but higher cost. Assert one row exists, cost updated. |
| T3 | Upsert no duplicate (different source_ids) | Unit | Two rows with different source_ids both inserted. |
| T4 | Failure leaves existing rows untouched | Integration (mock API) | Seed table with a row for '2026-07-28'. Call `sync_aws_to_sqlite` with API failure (raises exception). Assert row unchanged, no new rows. |
| T5 | No zero insertion on empty API response | Unit | API returns empty list for a day. Call upsert – assert no row inserted for that day. |
| T6 | Schedule logic (6-hour window) | Unit | Mock time. Assert `should_fetch_aws` returns True when no last sync, False when recent sync (<6h), True when >6h. |
| T7 | Backfill script idempotency | Integration | Run backfill twice for same date range – row counts unchanged, costs reflect latest run. |
| T8 | Actual AWS API call (integration with sandbox or recorded data) | Integration | Use a test AWS account with Cost Explorer enabled, or replay a captured response. Verify SQLite rows match. |
| T9 | Revised estimate update | Integration | Insert a row for current day with low cost. Then simulate new API call returning higher cost. Assert single row with updated cost. |
| T10 | Output inclusion | Unit (dashboard) | After inserting AWS rows, verify grand total includes AWS sum. Verify ordering in provider list. |
| T11 | Log sanitization | Unit | Assert that `Authorization` header is never present in log messages (inject a mock logger). Fail test if any log call contains 'Authorization'. |
| T12 | Retry mechanism | Unit | Mock API to fail twice, succeed third time. Assert `fetch_cost_explorer` called 3 times, row inserted. |

All tests run without network (except T8). Use `unittest.mock` for external calls. Database tests use in-memory SQLite.
