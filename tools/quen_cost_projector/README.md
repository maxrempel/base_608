# Quen (Qwen) cost projector

Tracks pure Qwen chat spend (model qwen3.8-max, DashScope Model Studio
International) separately from MoMA video generation.

## Data source

`collect_quen_balance_v01.py` (schema 2) scans local Codex session logs
(`~/.codex/sessions/**/rollout-*.jsonl`) whose session_meta declares
`model_provider = "qwen"`, sums the per-API-call `last_token_usage` of every
`token_count` event (forked sessions do not replay parent usage, so there is
no double count), and prices it at list rates: input $2.00/1M, context-cache
hit input $0.20/1M (10% of list), output $6.00/1M (reasoning tokens included).
`input_tokens` is treated as inclusive of `cached_input_tokens`. Daily buckets
use Pacific time. All dollar figures are estimates and are labeled as such on
the page.

The ds_ledger DashScope total (100% MoMA wan2.6-i2v-flash video generation) is
fetched as context only and shown as a separate line, never mixed into the
Qwen cards or chart.

## Outputs

- `quen_balance.json` / `quen_balance.js` - written atomically (temp + rename)
  so the page's 60-second auto-refresh never reads a half-written file.

## Page

`quen_tracker.html` - light-theme dashboard: lifetime/today/7-day/token cards,
cumulative spend chart with zoom, polling schedule phases, and the shared
four-source summary table (`../shared_expense_summary.js`, which injects all
four tracker data files and renders on every tracker page).

## Schedule

Windows Scheduled Tasks:
- "Quen Balance Collector" - every 5 min on Aug 5, then 20 min (Aug 6-7), then
  30 min (Aug 8+). Runs hidden via pythonw.exe.
- "Quen Schedule Updater" - daily 00:05, runs `update_schedule.py` which
  recreates the collector task at the interval for the current phase.

## Archive

`archive/` holds the schema-1 ledger-only collector, the pre-rewrite page, and
obsolete test files.
