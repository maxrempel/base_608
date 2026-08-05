# Work log: Codex backend DeepSeek -> Qwen (Alibaba)

Last edited: 2026-08-05 by Codex

## [2026-08-05 14:35-15:00]
- DID: Switched the interactive Codex backend from DeepSeek to Qwen 3.7 Plus on
  Alibaba DashScope (Beijing key), after Max pivoted from Kimi to Qwen.
- DID: Built reversible switch tool `tools/codex_backend/switch_codex_backend.py`
  (status / qwen / deepseek, timestamped backups, fail-closed on missing key),
  README, and unit tests (4/4 pass).
- DID: Added `qwen3.7-plus` to `~/.codex/models.json`; kept DeepSeek entries.
- DID: Verified: direct API (plain + tools + responses-with-reasoning), CLI
  `codex exec` smoke test answered correctly. Alibaba streaming dropped the
  stream a few times; Codex auto-retried and completed.
- SIDE EFFECT: `codex exec` deleted `~/.codex/auth.json` (ChatGPT login
  record). Machine is API-key-only by design; model access unaffected. Notion
  MCP OAuth refresh failed during the CLI test (invalid refresh token,
  pre-existing, unrelated to Qwen).
- STATE: config.toml active provider qwen / model qwen3.7-plus. DeepSeek intact.
  Revert: `python C:\claude_base\tools\codex_backend\switch_codex_backend.py deepseek`.
- NEXT: Max starts a new Codex task to try Qwen; watch for streaming stability.
  Full handover doc: `deepseek_to_qwen_switch_20260805_v01_tomemex.md`.
