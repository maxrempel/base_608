## Fleet capacity monitor – compact design

### 1. Schema & API contract (hub SQLite + JSON/HTTP)

**Database tables** (created via `schema.py`, WAL mode enabled):

```sql
CREATE TABLE machines (
    machine_id   TEXT PRIMARY KEY,       -- unique hostname
    hostname     TEXT,
    ip           TEXT,
    os           TEXT,                   -- 'linux' / 'windows'
    capacity_cpu  INTEGER,               -- logical cores
    capacity_mem  INTEGER,               -- bytes
    always_on    INTEGER DEFAULT 0,      -- 1 = required reporter
    config_ceilings TEXT,                -- JSON: {cpu_pct, mem_pct}
    last_seen    TEXT                    -- ISO8601 UTC
);

CREATE TABLE samples (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id    TEXT NOT NULL,
    ts            TEXT NOT NULL,          -- ISO8601 UTC
    cpu_pct       REAL,
    mem_pct       REAL,
    load_1m       REAL,
    load_5m       REAL,
    load_15m      REAL,
    disk_used     INTEGER,               -- bytes
    disk_total    INTEGER,
    net_sent      INTEGER,               -- cumulative bytes
    net_recv      INTEGER,
    uptime        INTEGER,               -- seconds
    top_procs     TEXT,                  -- JSON array of {pid, name, cpu, mem, cmd}
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

CREATE TABLE hourly_aggs (
    machine_id    TEXT NOT NULL,
    hour_bucket   TEXT NOT NULL,         -- '2026-08-03T14:00Z'
    cpu_mean      REAL,
    cpu_max       REAL,
    mem_mean      REAL,
    mem_max       REAL,
    load1m_mean   REAL,
    load5m_mean   REAL,
    load15m_mean  REAL,
    disk_used_avg REAL,
    net_sent_total INTEGER,
    net_recv_total INTEGER,
    uptime_max    INTEGER,
    sample_count  INTEGER,
    PRIMARY KEY (machine_id, hour_bucket)
);

CREATE TABLE tasks (
    machine_id            TEXT PRIMARY KEY,
    task_name             TEXT,
    state                 TEXT,            -- working / healthy_intermission / waiting / complete
    owner                 TEXT,
    reason                TEXT,
    progress_evidence     TEXT,
    expected_process_name TEXT,
    last_state_change     TEXT,
    last_progress_change  TEXT             -- time when evidence last changed
);

CREATE TABLE alarms_sent (
    alarm_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id  TEXT,
    alarm_type  TEXT,                      -- stale, idle, missing_process, high_cpu, high_mem
    ts          TEXT,
    details     TEXT,
    UNIQUE(machine_id, alarm_type, ts)     -- prevent duplicates within same second
);
```

**API contract** (authentication: header `X-Monitor-Token` checked against env `MONITOR_TOKEN`):

- **`POST /api/v1/report`** – push sample  
  Body:
  ```json
  {
    "machine_id": "lakarian",
    "ts": "2026-08-03T14:05:00Z",
    "cpu_pct": 34.2,
    "mem_pct": 71.0,
    "load_1m": 2.1, "load_5m": 1.9, "load_15m": 1.8,
    "disk_used": 21000000000, "disk_total": 50000000000,
    "net_sent": 123456789, "net_recv": 987654321,
    "uptime": 86400,
    "top_procs": [{"pid":1234, "name":"python", "cpu":15.2, "mem":8.1, "cmd":"python worker.py"}]
  }
  ```
  Response `204 No Content`. On receipt: update `machines.last_seen`, insert sample. Evaluate high-resource alarms (if cpu > ceiling or mem > ceiling configured for that machine, fire alarm with cool‑down).

- **`POST /api/v1/task`** – update task state  
  Body:
  ```json
  {
    "machine_id": "lakarian",
    "task_name": "nightly-sim",
    "state": "working",
    "owner": "alice",
    "reason": "simulation run #42",
    "progress_evidence": "iteration 1542/5000",
    "expected_process_name": "sim_engine"
  }
  ```
  Response `204`. Upserts `tasks` row. If `state = "working"` and `progress_evidence` differs from stored, set `last_progress_change = now()`. Update `last_state_change` when state changes.

- **`GET /api/v1/status`** – current fleet summary  
  Returns JSON: list of machines, each with latest sample, task info, and any active alarms not yet cleared (alarms cleared after resolution or manually via dashboard).  
  Optional `?
