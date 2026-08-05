Review this expense-monitor integration design and identify correctness risks.

Context:
- MoMA already writes every successful paid API call into Cloudflare D1 table
  api_expenses through expense_log.py. Current tracked lifetime is $79.81:
  DashScope wan2.6-i2v-flash $74.025, OpenAI gpt-image-2 $5.508,
  Fal Kling $0.28, SiliconFlow wan22 $0, and two FishAudio rows with NULL cost.
- A separate always-on central ledger at ledger.maxrempel.com currently tracks
  DeepSeek and FishAudio from prepaid balance deltas, plus self-reported meter
  providers. Its /spend endpoint accepts provider/category/model/usd.
- The central ledger currently knows deepseek, fishaudio, claude, and legacy wan.
- Goal: show all current MoMA costs in the central ledger without double counting.

Proposed implementation:
1. Add central meter providers openai, dashscope, siliconflow, fal, and syncso.
2. Send FishAudio MoMA reports to the existing fishaudio provider, where balance
   deltas remain the authoritative headline and reports only categorize usage.
3. Send every other MoMA D1 cost to its matching central provider with category
   "moma", preserving the model.
4. Add source_id and event_ts to /spend. Add a unique partial index on
   (provider, source_id), so historical backfill and live retries are idempotent.
5. In expense_log.record(), capture the D1 insert lastrowid, then best-effort POST
   the same cost with source_id "moma_api_expenses:<id>".
6. Add a --sync-ledger CLI that replays all existing non-null D1 rows. The central
   unique index makes it safe to rerun.
7. Keep MoMA D1 as the detailed source and central ledger as the unified monitor.

Return:
- A compact critique.
- Any double-counting, timestamp, SQLite migration, idempotency, or delivery risks.
- Concrete corrections only; no code.
