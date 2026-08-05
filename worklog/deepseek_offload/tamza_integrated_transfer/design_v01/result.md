# Integrated Tamza Transfer & Household Bandwidth Controller – Design v01

## 1. Component Placement and Single-Source Dataflow

### Topology
- **Central Controller (CC)** – Python daemon on the existing Linux compute host (where the retired controller ran). One process, systemd-managed (restart on failure).
- **Measurement Agents (MA)** – One per host (Linux server, Windows storage server, Linux compute host). Existing Cloudflare download scripts extended to report WAN interface throughput (`/proc/net/dev` on Linux, `Get-NetAdapterStatistics` on Windows) every 30 s. Data sent via HTTP POST to CC.
- **Actuation Stubs** – On Linux: `tc` qdisc per cgroup (downstream & upstream). On Windows: a small HTTP listener alongside the Python uploader that adjusts its token bucket rate.
- **Job Inventory** – SQLite database at CC (`/var/lib/bandwidth/jobs.db`). Single source of truth for all active transfers (ytdow, genomic, uploads, video copy).
- **Video Copy Pipeline** – CC watches source YouTube channel via yt-dlp `--flat-playlist` (hourly). When a new livestream appears (time >= 36h after upload), CC creates a download job for ytdow. After download completes and file is verified (MKV integrity), CC creates an upload job for the Windows uploader. The Windows uploader reads the same local file (LAN mount) and posts to destination channel, preserving title and description from metadata.

### Dataflow (simplified)
```
Source YT → yt-dlp (ytdow) → local MKV → (LAN copy) → Windows server → Uploader → Dest YT
                                ↓
                          CC records fingerprint & status
```

All measurement and actuation traffic goes over a dedicated control network or the same LAN but is excluded from bandwidth accounting (by interface or VLAN tag).

## 2. Capacity / Residual / Throughput Model

### Definitions
- **C_down(t)**, **C_up(t)** – Estimated total bandwidth of the household link (down/up). Measured by a scheduled Speedtest once per hour (off-peak, no bulk transfers active). Stale after 1 h.
- **T_down(t)**, **T_up(t)** – Total instantaneous throughput on the WAN interface (all traffic) measured by MAs.
- **R_down(t) = C_down(t) - T_down(t)** – Residual downstream capacity available.
- **R_up(t) = C_up(t) - T_up(t)** – Residual upstream capacity.
- **Reserve floor**: R_down(t) ≥ 50 Mbps, R_up(t) ≥ 10 Mbps (configurable).

### Operation
- When a bulk transfer job is requested, CC checks `R_down` / `R_up`. If reserve is already below floor, job is queued (not started) until capacity frees.
- During a transfer, CC monitors T_down/T_up every 5 s (from MA data). If R drops below floor (e.g., household load increases), CC reduces (throttles) the sum of active transfer bandwidths to restore R.
- Throttling is proportional: each job gets a weight (equal by default, higher for genomic). New bandwidth limit = current total job bandwidth * (R_after_reserve / R_before). Minimum allowed per job = 1 Mbps.

## 3. Safe Ookla Before/During/After Protocol

We use Speedtest only as a calibration tool, not for real-time control, to avoid violating the reserve.

- **Before bulk transfer**: CC checks age of last Speedtest. If older than 1 h, it schedules a Speedtest on the Linux compute host (or any host with CLI). The test runs with `--duration 5` (5 s) and `--interface` on the WAN interface. To ensure it does not steal the reserve, CC pauses all *other* transfers and limits the Speedtest's own bandwidth to (C_down - 50) Mbps using a `tc` filter on its egress (only for that test flow). If C_down is unknown, we use a conservative default of 100 Mbps.
- **During transfer**: No Speedtest is run. Residual is computed from MA data.
- **After transfer**: Optionally, a similar capped Speedtest runs to update C_down/C_up for future.

Rationale: The 5 s test with a cap ensures the reserve is never breached. The cap is computed as `max(0, C_down_last - 50)` where `C_down_last` is the last known capacity (from the previous uncapped test). During initial calibration, we run a full Speedtest at 3 AM with no other traffic.

## 4. Dynamic Actuation Mechanisms

### Linux (yt-dlp, curl, aria2)
- Each download/upload process is placed in a dedicated cgroup.
- CC uses `tc` classful qdisc (HTB) on the WAN egress interface. Classes are created per job.
- Downstream: shape egress of the download processes (actually ingress on WAN is shaped via `ifb`).
- Upstream: shape egress of upload processes.
- CC sends commands via SSH (or locally if on same host) to set class rates.
- Systemd service `bandwidth-ctl` runs CC; it has the capability to modify `tc`.

### Windows (Python uploader)
- The uploader already has an internal token bucket. We add a small HTTP endpoint (`/set_rate?up=<kbps>`).
- CC sends requests to the Windows host (port 8080, firewall allowed). The uploader updates its rate immediately.
- Additionally, we shape the upload process by adjusting TCP congestion window? Not needed; token bucket is sufficient.

## 5. Central Lease and Inventory Semantics

- All active jobs are registered in SQLite table `jobs`:
  ```sql
  CREATE TABLE jobs (
    id TEXT PRIMARY KEY,        -- UUID
    host TEXT,                  -- 'linux-server' | 'windows-storage' | 'compute'
    type TEXT,                  -- 'download' | 'upload' | 'genomic'
    status TEXT,                -- 'pending' | 'running' | 'paused' | 'completed' | 'failed'
    bandwidth_limit_bps INTEGER,
    pid INTEGER,
    created_at TEXT,
    updated_at TEXT,
    fingerprint TEXT,           -- SHA256 of file (nullable)
    source_url TEXT,            -- YouTube URL or genomic job ID
    dest_url TEXT
  );
  ```
- **Lease**: Each job is owned by the host that executes it. When starting, the host sends a `POST /jobs/{id}/claim` to CC. CC checks that no other job with same `fingerprint` is running (idemp
