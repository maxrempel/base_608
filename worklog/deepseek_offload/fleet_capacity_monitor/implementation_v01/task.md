# Fleet capacity monitor implementation review

Date: 2026-08-03
Last editor: Codex (GPT-5.6 SOL)

Design the smallest durable implementation for a cross-platform fleet computation monitor.

Context:

- Existing Python standard-library monitors use a reporter-to-Dax push model, SQLite history, deterministic Telegram alarms, and a light web dashboard.
- Required machines initially include Dax on AWS Lightsail, Lakarian, Asto, and Taygeta. The design must allow more machines without code changes.
- Each reporter must collect exact logical processor count, memory capacity, current processor and memory use, load, disk and network counters, uptime, and top compute processes.
- The hub must keep five-minute samples and hourly long-term history, show current capacity and usage history, and expose authenticated JSON and HTML endpoints.
- A task or service publishes one of four states: working, healthy_intermission, waiting, or complete, plus task name, owner, reason, and expected progress evidence.
- Evaluate possible stalls only after a complete 20-minute window. Never infer unjustified idleness solely from low utilization. Alert only when state is working and progress evidence has not changed for 20 minutes, or the expected process disappeared, or a required always-on reporter is stale.
- Healthy intermission, waiting, and complete never trigger idle alarms. High resource usage can produce a safety alarm, using per-host configured ceilings.
- Read-only monitor: no automatic restart, task creation, or resource changes.
- Python standard library only, Linux and Windows reporters, SQLite hub, authenticated push, secrets kept outside source.
- Retain raw samples for 30 days and hourly aggregates indefinitely.
- Dashboard must be light theme and concise.

Provide:

1. A concrete schema and API contract.
2. Deterministic state and alarm logic with edge cases.
3. A compact file layout.
4. Implementation pitfalls and a focused test matrix.
5. Suggestions for deploying on Dax and scheduling reporters without visible consoles.

Do not access files or write code. Plain English, concise, and implementation-ready.
