Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Review and propose a concrete implementation for the existing project at
C:\claude_base\tools\home_speed_monitor_v02.

Goal: replace its latest-reading-only network probe with a dependable unified
speed monitor for every Unix machine in Max's fleet: Lakarian, Taygeta, Asto,
Sol, and Dax. The monitor must keep timestamped history, report download Mbps,
upload Mbps, latency milliseconds, transferred byte counts, duration, success
or failure, and probe version. It must avoid simultaneous home probes and avoid
saturating the connection: a small bounded Cloudflare download/upload probe is
preferred, every 30 minutes on home machines with staggered offsets, hourly on
Dax. Offline machines must simply produce stale/offline status rather than
breaking the system. Existing controller-authenticated report endpoints and D1
storage should be extended, preserving the public speed.maxrempel.com site.

The dashboard needs clear light-theme cards for each machine, freshness state,
download/upload/latency, a selectable 24-hour/7-day/30-day line chart, recent
probe outcomes, and explicit notes that tests are small bounded samples rather
than ISP line certification. Keep raw participant/science data out of it.

Return a concise architecture, schema migration, exact file-change list,
failure-mode checklist, and test plan in result.md. Do not edit the project.
