# Codex Backend Switch: DeepSeek <-> Qwen (Alibaba DashScope)

Operational reference for the interactive Codex backend on Pine.

Last edited: 2026-08-05 by Codex

## 1. Purpose

The interactive Codex app normally talks to a model backend defined in
`C:\Users\maxre\.codex\config.toml`. It ran on ChatGPT, was moved to DeepSeek on
2026-08-03, and is now being trialed on Alibaba's Qwen 3.7 Plus (2026-08-05).
This folder holds the reversible switch between backends: DeepSeek stays fully
configured, and reverting is one command. Nothing in this experiment touches
the headless agent route or the DeepSeek offload runner, which remain pinned to
DeepSeek per the shared rules.

## 2. Current status (2026-08-05)

- Active provider: `qwen` (Qwen 3.7 Plus on Alibaba DashScope).
- Active model: `qwen3.7-plus`.
- Previous provider: `deepseek` (`deepseek-v4-flash`), still configured.
- Config file: `C:\Users\maxre\.codex\config.toml`.
- Model catalog: `C:\Users\maxre\.codex\models.json` (entries for both
  providers).
- Status verified end to end with a real `codex exec` run.

## 3. Quick start

Show the active provider:

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py status

Switch to Qwen (the current trial):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py qwen

Revert to DeepSeek (one-command rollback):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py deepseek

The change applies to NEW Codex tasks. A task already running keeps the backend
it started with.

## 4. How the switch works

The tool edits only `~/.codex/config.toml` (user-level Codex state, outside the
git repository):

- `model = "qwen3.7-plus"` or `"deepseek-v4-flash"`.
- `model_provider = "qwen"` or `"deepseek"`.
- `model_auto_compact_token_limit` (350000 for both, matching the 1M-token
  context of each model).
- The `[model_providers.<name>]` block: base URL, wire API, and the bearer
  token read fresh from the canonical credential file.

`models.json` is never rewritten by a switch: it keeps catalog entries for both
backends. The active model must exist in the catalog, and the switch verifies
this before writing.

Before every edit the tool writes:

- `~/.codex/backups\config.toml.<YYYYMMDD-HHMMSS>` (timestamped backup).
- `~/.codex\backup-<provider>\config.toml` plus `manifest.txt` (snapshot of the
  newly active provider).

If a provider's API key file is missing or empty, the switch fails closed and
changes nothing.

## 5. Provider reference

| Provider | Model | Base URL | Wire API | Key file |
| --- | --- | --- | --- | --- |
| `qwen` (active) | `qwen3.7-plus` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | responses | `Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt` |
| `deepseek` | `deepseek-v4-flash` | `https://api.deepseek.com/` | responses | `Nextcloud\zSyncMain\ssh\deepseek_api_key_20260226.txt` |

Qwen 3.7 Plus on Alibaba: 1M-token context, tool calling, thinking mode, about
$0.32-$0.40 per million input tokens and $1.28-$1.60 per million output. That is
the "intermediate" pricing tier Max chose (cheaper than Anthropic/OpenAI
flagships, more expensive than DeepSeek).

The current Codex build requires `wire_api = "responses"` for custom providers;
`wire_api = "chat"` is rejected at config load. Alibaba's compatible-mode
endpoint supports the Responses API, verified by direct calls and by the real
CLI run.

## 6. Verification performed on 2026-08-05

- Direct API calls to `qwen3.7-plus` with the Alibaba Beijing key: plain answer
  OK, function calling OK, Responses-style request with tools and reasoning OK.
- `switch_codex_backend.py` unit tests (isolated temp config/catalog/key
  files): 4/4 pass (switch to qwen, revert to deepseek, missing-key
  fail-closed, backups created).
- Real `codex exec` smoke test through the CLI with the switched config:
  answered correctly. Alibaba's streaming endpoint dropped the stream a few
  times; Codex retried automatically and completed the answer.

## 7. Troubleshooting

- `wire_api = "chat" is no longer supported`: the provider block must use
  `wire_api = "responses"`. The switch tool always writes the correct value.
- `API key login is required, but ChatGPT is currently being used`: this
  machine is API-key-only by design (`forced_login_method = "api"`). The CLI
  logs out a stale ChatGPT login record when it conflicts. Model access is not
  affected because each provider carries its own bearer token. If the desktop
  app asks Max to sign in again for account features, he signs in with ChatGPT.
- Streaming disconnects with `stream disconnected - retrying sampling request`:
  observed once on Alibaba's Responses endpoint. Codex retries up to 5 times and
  completed the run. If this becomes frequent on real tasks, re-evaluate the
  endpoint or provider before blaming the model.
- MCP OAuth failures such as Notion `invalid_grant`: pre-existing connector
  token expiry, unrelated to the backend switch. Reauthorize the connector
  separately.
- Missing or empty key file: the switch fails closed with a clear message.
  Restore a known-good config from `~/.codex\backups\` if a manual edit ever
  goes wrong, then re-run the switch.

## 8. Security

- API keys live only in the documented Nextcloud credential files under
  `Nextcloud\zSyncMain\ssh\`. The switch reads them from there and writes the
  active one into `config.toml`, which is outside the git repository.
- Never print, paste, log, or commit a key. The tool never prints tokens.
- Keys are never copied into this repository, task definitions, or process
  arguments.

## 9. Maintenance

- Add a provider: extend the `PROVIDERS` dict in
  `switch_codex_backend.py`, add a catalog entry in `~/.codex\models.json`, and
  add a unit test in `test_switch_codex_backend.py`.
- Rotate a key: replace the key file content in Nextcloud, then run
  `switch <provider>` again; the tool refreshes the token in the provider block.
- After any edit, run the tests:

      cd C:\claude_base\tools\codex_backend
      python -m unittest test_switch_codex_backend

## 10. Related documents

- Handover record:
  `C:\claude_base\deepseek_to_qwen_switch_20260805_v01_tomemex.md`.
- Work-log entry:
  `C:\claude_base\worklog\codex_qwen_switch_20260805_v01.md` (local only, the
  `worklog` folder is gitignored by design).

## 11. Thread model labeler and continuous watcher (added 2026-08-06)

Max runs sessions on several backend generations (ChatGPT/GPT, DeepSeek, Qwen
3.7, Qwen 3.8) and the sidebar did not show which backend ran which session.
`label_threads.py` fixes that by prefixing every saved thread title with a
short model tag, for example `[DS] Verify Qwen expense tracker`. Tags:
`[GPT]` OpenAI/ChatGPT, `[DS]` DeepSeek, `[Q3.8]` / `[Q3.7]` / `[Q3.5]` /
`[Q3]` / `[Q3C]` / `[QW]` for the Qwen tiers. The tag is derived from the
model recorded per thread in the database, so a thread keeps the tag of the
backend that actually ran it, even after the global backend switches.

Commands:

    python C:\base_608\tools\codex_backend\label_threads.py preview
    python C:\base_608\tools\codex_backend\label_threads.py apply
    python C:\base_608\tools\codex_backend\label_threads.py status
    python C:\base_608\tools\codex_backend\label_threads.py undo

`apply --log <file>` is the quiet, console-free form used by the scheduled
watcher: it writes one outcome line per run and prints nothing, so it is safe
to launch hidden with `pythonw.exe`.

The hidden scheduled task `CodexThreadLabelWatcher` runs `apply --log` every 5
minutes (installer: `install_thread_label_watcher.ps1`), so every new thread
is labeled automatically. It uses `pythonw.exe` (no console window), ignores
overlapping instances, writes a backup + undo manifest before any change, and
logs each run to `~/.codex/logs/thread_label_watcher.log`. The canonical
committed copy of the labeler also lives at
`C:\claude_base\tools\codex_backend\label_threads.py`; keep both in sync.

The labeler also reconciles with the app's own title management: the Codex
desktop app auto-names active sessions and stamps them with lowercase native
tags (`ds ...`, `deepseek ...`, `qw ...`). The labeler treats those as
already-tagged, normalizes them to the standard `[DS] ...` form, strips
nested tags (`[DS] ds ...` becomes `[DS] ...`), and shortens raw
dictation-style first-message titles, so the sidebar never shows double tags
or full message dumps. The app's own informative renames are preserved;
raw-title shortening is limited to threads created in the last 7 days, and
`apply` writes only when something actually changes (no index churn, no
duplicate lines), so the watcher stays quiet when there is nothing new.

Known display limitation (verified 2026-08-06): the desktop app keeps its own
in-memory copy of thread titles for the sidebar and does not always reflect
external edits to the database or `session_index.jsonl`, even though the
stores are correct. A full app restart reloads titles from the store, which
is the reliable way to make the sidebar show the prefixes. The watcher keeps
the store correct continuously, so every reload shows the right result.
