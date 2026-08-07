# Codex Backend Switch: DeepSeek <-> Qwen (Alibaba DashScope)

Operational reference for the interactive Codex backend on Pine.

Last edited: 2026-08-06 by Codex

## 1. Purpose

The interactive Codex app normally talks to a model backend defined in
`C:\Users\maxre\.codex\config.toml`. It ran on ChatGPT, was moved to DeepSeek on
2026-08-03, was trialed on Alibaba's Qwen 3.8 Max (2026-08-05), and was
switched back to DeepSeek the same evening at Max's request. This folder holds
the reversible switch between backends: the inactive provider stays fully
configured, and switching is one command. Nothing in this experiment touches
the headless agent route or the DeepSeek offload runner, which remain pinned to
DeepSeek per the shared rules.

## 2. Current status (2026-08-06)

- Active provider: `deepseek` (DeepSeek, official API).
- Active model: `deepseek-v4-flash` (fast tier). DeepSeek V4 Pro is expected
  to support Codex integration in early August 2026 and is rejected by the API
  until then, so Pro is one command away but not yet active.
- Qwen: DISABLED 2026-08-06 at Max's request. The Alibaba DashScope API key
  stays valid for other uses. Re-enable with
  `switch_codex_backend.py enable-qwen`, then `switch_codex_backend.py qwen`.
- Config file: `C:\Users\maxre\.codex\config.toml`.
- Model catalog: `C:\Users\maxre\.codex\models.json` (entries for both
  providers).
- Terminal title: `[tui] terminal_title = ["spinner", "project", "model"]`,
  so the active model is visible in the embedded terminal title of the Codex
  app (official Codex setting, applied 2026-08-05).
- Status verified end to end with a real `codex exec` run.

## 3. Quick start

Show the active provider:

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py status

Switch to Qwen (the current trial):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py qwen

Switch between verified Qwen variants (for example step down to 3.7 Plus):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py qwen --model qwen3.7-plus

Revert to DeepSeek (one-command rollback):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py deepseek

Switch to DeepSeek V4 Pro when the API opens it for Codex (expected early
August 2026):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py deepseek --model deepseek-v4-pro

Disable Qwen in the interactive Codex app (the Alibaba key stays valid):

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py disable-qwen

Re-enable Qwen later:

    python C:\claude_base\tools\codex_backend\switch_codex_backend.py enable-qwen
    python C:\claude_base\tools\codex_backend\switch_codex_backend.py qwen

The change applies to NEW Codex tasks. A task already running keeps the backend
it started with.

## 4. How the switch works

The tool edits only `~/.codex/config.toml` (user-level Codex state, outside the
git repository):

- `model = "qwen3.8-max"` (or a verified Qwen variant via `--model`, or
  `"deepseek-v4-flash"`).
- `model_provider = "qwen"` or `"deepseek"`.
- `model_auto_compact_token_limit` (350000 for both, matching the 1M-token
  context of each model).
- The `[model_providers.<name>]` block: base URL, wire API, and the bearer
  token read fresh from the canonical credential file.

`models.json` is never rewritten by a switch: it keeps catalog entries for both
backends. The active model must exist in the catalog, and the switch verifies
this before writing. `--model` accepts only variants in the `QWEN_MODELS` and
`DEEPSEEK_MODELS` whitelists (models verified working on the respective
accounts), so stepping between Qwen versions, or from DeepSeek Flash to
DeepSeek Pro, is itself a one-command, reversible operation.

Before every edit the tool writes:

- `~/.codex/backups\config.toml.<YYYYMMDD-HHMMSS>` (timestamped backup).
- `~/.codex\backup-<provider>\config.toml` plus `manifest.txt` (snapshot of the
  newly active provider).

If a provider's API key file is missing or empty, the switch fails closed and
changes nothing.

## 4b. Disabling Qwen (2026-08-06)

Max asked to turn Qwen off in the interactive Codex app while keeping the
Alibaba key valid, because Qwen remains in use elsewhere. `disable-qwen`
performs, in order:

- Timestamped backups of `config.toml` and `models.json` in
  `~/.codex/backups/`.
- Removal of the `[model_providers.qwen]` block from `config.toml` (the bearer
  token is removed from the live config; the key file in Nextcloud is never
  touched).
- Removal of the Qwen entries from `~/.codex/models.json`, so the app no
  longer offers Qwen in the model picker.
- A copy of the removed Qwen catalog entries in
  `~/.codex/backup-qwen/models.qwen.json`.
- The disable marker `~/.codex/qwen.disabled`.

While the marker exists, `switch_codex_backend.py qwen` fails closed with a
clear message. `--force` overrides the marker for a single command, which is
only useful after `enable-qwen` has restored the catalog (without the catalog
entries the switch verification fails and nothing is changed).

`enable-qwen` restores the Qwen catalog entries from
`~/.codex/backup-qwen/models.qwen.json` and deletes the marker; it does not
activate Qwen. Activation remains an explicit `switch_codex_backend.py qwen`.

The disable applies to new tasks; restart the Codex app for the app to pick up
the changed config and catalog immediately.

## 5. Provider reference

| Provider | Model | Base URL | Wire API | Key file |
| --- | --- | --- | --- | --- |
| `deepseek` (active) | `deepseek-v4-flash` | `https://api.deepseek.com/` | responses | `Nextcloud\zSyncMain\ssh\deepseek_api_key_20260226.txt` |
| `deepseek` (pending) | `deepseek-v4-pro` | `https://api.deepseek.com/` | responses | `Nextcloud\zSyncMain\ssh\deepseek_api_key_20260226.txt` |
| `qwen` (trialed) | `qwen3.8-max` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | responses | `Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt` |

DeepSeek V4 Pro (`deepseek-v4-pro`) is whitelisted and present in `models.json`,
but the DeepSeek API currently rejects it for Codex integration with "will be
available starting early August 2026". Retry `deepseek --model deepseek-v4-pro`
once the API opens it.

Qwen 3.8 Max on Alibaba: 1M-token context, tool calling, thinking mode. It was
the strongest tier on the account and the model Max chose for the trial, which
ended on 2026-08-05. Max tier pricing is higher than the Plus tier (Qwen 3.7
Plus was about $0.32-$0.40 per million input and $1.28-$1.60 per million
output); the exact Max rate is shown on Alibaba's billing page.

The current Codex build requires `wire_api = "responses"` for custom providers;
`wire_api = "chat"` is rejected at config load. Alibaba's compatible-mode
endpoint supports the Responses API, verified by direct calls and by the real
CLI run.

## 6. Verification performed on 2026-08-05

- Direct API calls to `qwen3.8-max` with the Alibaba Beijing key through the
  Responses-style endpoint: completed answer OK (model thinks first, then
  answers). Earlier the same key verified `qwen3.7-max`, `qwen3.7-plus`,
  `qwen3.7-flash`, `qwen3.5-plus`, `qwen3-max`, and
  `qwen3-coder-480b-a35b-instruct`.
- `switch_codex_backend.py` unit tests (isolated temp config/catalog/key
  files): 6/6 pass (switch to qwen, revert to deepseek, missing-key
  fail-closed, backups created, switch to a Qwen variant, unknown variant
  fails closed).
- Real `codex exec` smoke test through the CLI with the switched config:
  ran on `model: qwen3.8-max, provider: qwen` and answered correctly.
  Alibaba's streaming endpoint can drop the stream; Codex retries
  automatically and completes the answer.
- 2026-08-05 evening, after reverting to DeepSeek: unit tests 8/8 pass
  (DeepSeek variant tests added, revert-suggestion bug fixed). Real `codex
  exec` smoke test ran on `model: deepseek-v4-flash, provider: deepseek` and
  answered correctly. `deepseek-v4-pro` was rejected by the DeepSeek API for
  Codex integration ("will be available starting early August 2026"); the
  switch stayed reversible and the Pro variant remains one command away.

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
- Add or change a Qwen variant: extend the `QWEN_MODELS` whitelist in
  `switch_codex_backend.py` and add the catalog entry in
  `~/.codex\models.json`; verify the model answers through the Responses-style
  endpoint before listing it.
- Add or change a DeepSeek variant: extend the `DEEPSEEK_MODELS` whitelist in
  `switch_codex_backend.py` and add the catalog entry in `~/.codex\models.json`;
  verify the model answers through the Responses endpoint before listing it.
- Rotate a key: replace the key file content in Nextcloud, then run
  `switch <provider>` again; the tool refreshes the token in the provider block.
- After any edit, run the tests:

      cd C:\claude_base\tools\codex_backend
      python -m unittest test_switch_codex_backend

## 10. Thread model labeler (added 2026-08-06)

Max runs sessions on several backend generations (ChatGPT/GPT, DeepSeek, Qwen
3.7, Qwen 3.8) and the sidebar did not show which backend ran which session.
`label_threads.py` fixes that by prefixing every saved thread title with a
short model tag, for example `[Q3.8] Fix login bug`.

Tags: `[GPT]` OpenAI/ChatGPT, `[DS]` DeepSeek, `[Q3.8]` / `[Q3.7]` /
`[Q3.5]` / `[Q3]` / `[Q3C]` / `[QW]` for the Qwen tiers. The tag is derived
from the model recorded per thread in the database, so a thread keeps the tag
of the backend that actually ran it, even after the global backend switches.

Commands:

    python C:\claude_base\tools\codex_backend\label_threads.py preview   # show what would change
    python C:\claude_base\tools\codex_backend\label_threads.py apply     # backup + label all untagged
    python C:\claude_base\tools\codex_backend\label_threads.py apply --log C:\Users\maxre\.codex\logs\thread_label_watcher.log
    python C:\claude_base\tools\codex_backend\label_threads.py status    # tag distribution
    python C:\claude_base\tools\codex_backend\label_threads.py undo      # restore previous titles

`apply --log <file>` is the quiet, console-free form used by the scheduled
watcher: it writes one outcome line per run and prints nothing, so it is safe
to launch hidden with `pythonw.exe`.

Where it writes:

- `~/.codex/state_5.sqlite`, table `threads`, column `title`: the
  authoritative thread record.
- `~/.codex/session_index.jsonl`: the sidebar display-name index (append-only;
  the newest entry per thread wins), kept in sync so the desktop sidebar shows
  the tag.

Safety and reversibility:

- Every `apply` first writes a consistent SQLite backup and a copy of
  `session_index.jsonl` into `~/.codex/backups/thread_labels/run_<timestamp>/`,
  plus a `changes.json` undo manifest.
- `undo` restores the original titles from the newest run (or `--run <dir>`
  for a specific one). The full backups remain as a second recovery path.
- Idempotent: titles that already start with a `[TAG] ` prefix are never
  touched again. A full `apply` run takes well under a second and is safe
  while the Codex app is open.
- Continuous labeling: the hidden scheduled task `CodexThreadLabelWatcher`
  (installed by `install_thread_label_watcher.ps1`) runs `apply --log` every
  5 minutes, so every new thread is labeled without any session having to run
  the command. The task is hidden, uses `pythonw.exe` (no console window),
  ignores overlapping instances, and logs each run to
  `~/.codex/logs/thread_label_watcher.log`. The shared agent rules keep the
  manual `apply` as a fallback for the rare case the watcher is unavailable.
- App-title reconciliation: the Codex desktop app also auto-names active
  sessions and stamps them with its own lowercase tags (`ds ...`,
  `deepseek ...`, `qw ...`). The labeler recognizes those as already-tagged,
  normalizes them to the standard `[DS] ...` form, strips nested tags
  (`[DS] ds ...` becomes `[DS] ...`), and shortens raw dictation-style
  first-message titles, so the sidebar never shows double tags or full
  message dumps. The app's own informative renames are preserved; only the
  tag format and obviously raw titles change.
  Raw-title shortening is limited to threads created in the last 7 days, so
  old session names are never rewritten. `apply` writes only when something
  actually changes: it syncs the database to the newest display index entry,
  skips no-op entries entirely, and never appends an identical index line,
  so the 5-minute watcher stays quiet when there is nothing new.

Known display limitation (verified 2026-08-06): the desktop app keeps its own
in-memory copy of thread titles for the sidebar and does not always reflect
external edits to the database or `session_index.jsonl`, even though the
stores are correct. Threads it re-titles (active sessions) can show the app's
own title, sometimes reverting our changes; old idle threads usually keep our
tagged titles. A full app restart reloads titles from the store, which is the
reliable way to make the sidebar show the prefixes. The watcher keeps the
store correct continuously, so every reload shows the right result.

Install or reinstall the watcher (also labels the current backlog):

    powershell -ExecutionPolicy Bypass -File C:\claude_base\tools\codex_backend\install_thread_label_watcher.ps1

## 11. Related documents

- Handover record:
  `C:\claude_base\deepseek_to_qwen_switch_20260805_v01_tomemex.md`.
- Work-log entry:
  `C:\claude_base\worklog\codex_qwen_switch_20260805_v01.md` (local only, the
  `worklog` folder is gitignored by design).
