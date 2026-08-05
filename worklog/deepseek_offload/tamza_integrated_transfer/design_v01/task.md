# Integrated Tamza transfer and household bandwidth controller design v01

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

## Assignment

Produce a detailed engineering design and implementation review for repairing an
existing multi-host household bandwidth controller and integrating a weekly
video-copy workflow. Do not use credentials or private data. Return only
`result.md`.

## Existing facts

- One sanctioned YouTube downloader, ytdow, runs on an always-on Linux server.
  It has one yt-dlp worker, a wide inter-video gap, a single-writer lock, and
  drains verified MKV files over the LAN to a Windows storage server.
- The 16 TB storage volume is currently healthy. LAN copies must not count as
  internet bandwidth.
- A Windows uploader already sends local media to a second video platform with
  an internal token-bucket upload limiter.
- A retired Python controller on a Linux compute host adjusted systemd transfer
  caps. It was disabled because it confused residual speed with total capacity,
  had incomplete multi-host inventory, and enabled actuation before adequate
  validation.
- Current measurement agents on three hosts use small Cloudflare downloads.
  The official Ookla Speedtest CLI is installed on several hosts.
- The new requirement is to preserve at least 50 Mbps downstream capacity for
  household users. Upload capacity must be measured and controlled separately.
- Required measurements: before, during, and after each controlled bulk
  transfer. A full saturating Speedtest should not itself violate the reserve.
- The repaired system must coordinate genomic transfers, ytdow, YouTube
  uploads, and the existing second-platform uploader. It must fail closed,
  support shadow mode, inventory all active jobs, exclude verified LAN traffic,
  and alarm on stale measurements or failed jobs.
- New livestreams from one source YouTube channel are copied to a clean
  destination channel after a 36-hour delay. Every new recording is eligible;
  normally two appear per week.
- Existing source videos are already copied. The first production candidate is
  next week. Testing must use one newly generated short synthetic video,
  uploaded private exactly once. Never upload any file with the same content
  fingerprint twice.
- The source video must be downloaded only once by ytdow. The uploader consumes
  that same verified local file and preserves source title and description.
- The user approves autonomous implementation, private-only pilot upload, and
  enabling the repaired system after staged validation.

## Deliverable

Recommend the smallest coherent design that reuses the existing system. Include:

1. component placement and single-source dataflow;
2. a precise capacity/residual/throughput model for downstream and upstream;
3. a safe Ookla before/during/after protocol;
4. dynamic actuation mechanisms appropriate to Linux yt-dlp/curl/aria2 and a
   Python HTTP uploader on Windows;
5. central lease and inventory semantics across hosts;
6. crash-safe SQLite or file state, idempotency, and content fingerprint rules;
7. a shadow-to-live validation ladder with measurable acceptance tests;
8. failure monitors and fail-closed behavior;
9. hazards in the proposed design and concrete corrections.

Be concise but technically specific. Do not recommend a second downloader.
