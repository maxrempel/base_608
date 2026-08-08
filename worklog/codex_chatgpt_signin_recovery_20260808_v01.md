# Codex desktop app: ChatGPT sign-in recovered after the backend restore

Date: 2026-08-08
Agent: Claude Opus 5, Pine
Branch: claude1/codex-chatgpt-restore-599f1f

## What Max reported

The morning after the 2026-08-07 restore of the interactive Codex backend to
ChatGPT defaults, the Codex desktop app started but came up on its sign-in
screen and the sign-in would not go through. Max described it as "stuck in the
front screen saying that something is blocked". He asked whether reinstalling
the app would be the easiest fix.

## Diagnosis

Not a broken install and not a broken config.

- `~/.codex/config.toml` was already correct: no `model_provider`, no
  `[model_providers.*]` block, no `forced_login_method`, no
  `preferred_auth_method`. Stock ChatGPT defaults, exactly as the 2026-08-07
  restore intended.
- No `OPENAI_*` / `CODEX_*` environment variable was forcing API-key auth,
  in the process environment or in `HKCU\Environment`.
- `codex.exe login status` returned `Not logged in`.
- `~/.codex/auth.json` did not exist. It had been deleted during the DeepSeek
  and Qwen trials, and the 2026-08-07 restore correctly did not recreate it
  (the switch tool never touches credential files).

So the single missing piece was the ChatGPT credential file. The app had
nothing to sign in with, which is what the front screen was reporting.

A reinstall would not have fixed this: a fresh install still has no
`auth.json` and still lands on the sign-in screen. It would additionally have
cost the MCP server definitions, the plugin list, the trusted-project list,
the light appearance theme, and the Codex++ patch layer carrying Max's
session-board tweak.

## Fix

1. Ran `codex.exe login` from a shell. It started the local login server on
   `http://localhost:1455` and produced the `auth.openai.com` authorization
   URL. Max approved it in his browser against his existing ChatGPT Pro
   session. No password was handled by an agent.
2. `Successfully logged in`; `~/.codex/auth.json` written 07:47 local.
3. `codex.exe login status` -> `Logged in using ChatGPT`.
4. Fully closed the desktop app (root `ChatGPT.exe` pid 18700 plus the
   `codex.exe` app-server child; the graceful close did not complete within
   20 s so it was forced) and relaunched via the Start Menu shortcut target,
   `ChatGPT.exe --user-data-dir=...\codex-plusplus\profile`.

The restart was required because the app starts its `codex.exe app-server`
child once and that child reads `auth.json` only at startup.

## Verification

- `codex doctor`: `config loaded`, `model <default> - openai`,
  `auth is configured`, `stored auth mode chatgpt`, `stored ChatGPT tokens
  true`, `stored API key false`, `model provider openai`, `wire API responses`,
  `handshake result HTTP 101 Switching Protocols`, `reachability mode ChatGPT
  auth`, ChatGPT base URL reachable.
- Codex++ layer intact after the restart: `main.log` logged
  `discovered 1 tweak(s): com.maxrempel.session-board` and
  `started main tweak: com.maxrempel.session-board`, no errors.
- End-to-end smoke test: `codex exec` ran on `model: gpt-5.6-sol, provider:
  openai` and returned the expected answer. 19,809 tokens.

## Left as-is, reported to Max

- The Notion MCP connector fails its OAuth refresh with `invalid_grant`
  (expired refresh token). Pre-existing, unrelated to the backend, and it
  needs a reauthorization of the Notion connector inside the Codex app.
- `codex doctor` warns that the rollout/thread database has 59 missing
  archived rows and 9 stale rows, and that `thread_history_1.sqlite` is
  missing. Cosmetic history bookkeeping; sessions open and run normally.
  Not touched.

## DeepSeek fallback: confirmed still one command

Max asked to keep the DeepSeek route available in case the ChatGPT weekly
limit runs out again. Nothing was lost in the restore:

- `switch_codex_backend.py deepseek` switches back in one command.
- The DeepSeek entries remain in `~/.codex/models.json`; the API key file in
  Nextcloud was never touched; `~/.codex/backup-deepseek/config.toml` holds a
  snapshot of the last working DeepSeek config.
- `deepseek-v4-pro` is already whitelisted for when the DeepSeek API opens it
  to Codex, which Max expects shortly:
  `switch_codex_backend.py deepseek --model deepseek-v4-pro`.

## Documentation

`tools/codex_backend/README.md`: status section updated to signed-in and
verified, and a new section 7a records the blocked-sign-in symptom, why a
reinstall is the wrong move, the exact recovery, and the app-server restart
requirement.
