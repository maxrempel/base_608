# Work log: Qwen disabled in interactive Codex app (key kept)

Last edited: 2026-08-06 by Codex

## [2026-08-06 ~17:00]

- DID: Disabled Qwen in the interactive Codex app at Max's request ("kill all
  Qwen for now, do NOT kill the key"). The Alibaba DashScope API key stays
  valid for other uses and was not modified.
- DID: Extended `tools/codex_backend/switch_codex_backend.py` with
  `disable-qwen` / `enable-qwen` actions and a guard marker
  `~/.codex/qwen.disabled` that blocks `switch qwen` (escape hatch `--force`).
  Also made switches fail closed before writing when the model is missing from
  the catalog.
- DID: Ran `disable-qwen` on the live machine:
  - removed `[model_providers.qwen]` from `~/.codex/config.toml`
  - removed Qwen entries from `~/.codex/models.json`
  - backups: `~/.codex/backups/config.toml.20260806-170152`,
    `~/.codex/backups/models.json.20260806-170152`
  - Qwen catalog snapshot: `~/.codex/backup-qwen/models.qwen.json`
  - marker: `~/.codex/qwen.disabled`
- DID: Verified live: active provider deepseek / deepseek-v4-flash; catalog
  has only deepseek-v4-flash + deepseek-v4-pro; `switch qwen` fails closed
  with the disable message; no Qwen token left in config.toml.
- DID: Unit tests 10/10 pass in both C:\claude_base and C:\base_608 mirrors.
  README updated in both repos; files mirrored from claude_base to base_608.
- STATE: Qwen cannot start new Codex tasks and cannot be switched back on by
  accident. Restart the Codex app to apply immediately.
- RESTORE (later, if Max wants Qwen back): `switch_codex_backend.py
  enable-qwen`, then `switch_codex_backend.py qwen`. The key file
  `Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt` is
  untouched.
- NOTE: The Qwen threads that refuse to archive cannot run or charge anymore
  once the app is restarted; archiving them is a separate app-side issue if it
  persists.
