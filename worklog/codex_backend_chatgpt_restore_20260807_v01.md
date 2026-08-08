# Work log: interactive Codex backend back on ChatGPT defaults

Last edited: 2026-08-07 by Codex

## [2026-08-07 ~23:00]

- DID: Restored the interactive Codex app to stock ChatGPT defaults at Max's
  request (his ChatGPT weekly limit refreshed, so the app goes back to
  ChatGPT). `~/.codex/config.toml` now carries no backend overrides: no
  `model`, `model_provider`, reasoning/compact overrides, API-key auth
  overrides, catalog override, or `[model_providers.*]` blocks.
- WHY: the ChatGPT-era sessions (181 rollouts) all used the built-in `openai`
  provider; the last pre-switch session ran `gpt-5.6-sol` with
  `model_provider = "openai"`, so "defaults" means built-in provider +
  app-managed model, not a `chatgpt` provider id.
- DID: Extended `tools/codex_backend/switch_codex_backend.py` with a
  `chatgpt` action (removes every backend override, backs up first, verifies)
  and made the switch insert backend keys when they are missing, so
  DeepSeek/Qwen remain one command away from a default config. Fixed a
  Windows path bug (catalog path is written with forward slashes) and a
  variable-shadowing bug that could put the wrong token in a provider block.
- DID: Unit tests 12/12 pass in both C:\base_608 and C:\claude_base mirrors;
  files mirrored and README updated in both repos.
- DID: Ran `switch_codex_backend.py chatgpt` on the live machine:
  - timestamped backup: `~/.codex/backups/config.toml.20260807-230748`
  - ChatGPT-default snapshot: `~/.codex/backup-chatgpt/` (config + manifest)
  - DeepSeek snapshot refreshed in `~/.codex/backup-deepseek/` so a revert
    restores the exact pre-restore state
- DID: Verified live: `config.toml` parses; `codex doctor` reports
  `default model provider openai`, `model <default>`, `config.toml parse ok`,
  `reachability mode ChatGPT auth`. Personal settings (approval never, full
  sandbox, 7 MCP servers, 11 plugins, light theme, trusted projects) are all
  intact.
- STATE: `~/.codex/auth.json` is absent (deleted during the 2026-08-03
  DeepSeek trial), so after Max restarts the Codex app it may ask him to sign
  in with ChatGPT once. New tasks then run on ChatGPT (gpt-5.6-sol) and the
  thread labeler tags them `[GPT]`.
- RESTORE (if Max ever wants DeepSeek or Qwen back):
  `switch_codex_backend.py deepseek` or `qwen` after `enable-qwen`.
  DeepSeek V4 Pro remains rejected by the API for Codex (expected early
  August 2026).
