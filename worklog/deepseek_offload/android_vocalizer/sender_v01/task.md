# Android Vocalizer sender version 01

Draft a small production-quality Python 3 command-line sender and tests.

Target location:

- `C:\claude_base\tools\android_vocalizer\android_vocalizer.py`
- `C:\claude_base\tools\android_vocalizer\tests\test_android_vocalizer.py`

Requirements:

- Standard library only.
- Commands:
  - `setup`: create a private JSON config if absent. Generate an unguessable
    ntfy topic with `secrets`; default config path is
    `%USERPROFILE%\Nextcloud\zSyncMain\ssh\android_vocalizer_config_v01.json`.
    Never print the topic, token, phone number, or full endpoint.
  - `send TEXT`: publish to ntfy over HTTPS.
- Options on `send`: `--title`, `--priority` (`routine`, `urgent`,
  `emergency`), `--call`, `--dry-run`, `--config PATH`.
- Map priorities to ntfy values: routine=3, urgent=5, emergency=5.
- Routine and urgent publish a push. `--call` adds `Call: yes`; it must fail
  clearly if no bearer token is configured. Emergency automatically requests a
  call and must likewise require a token.
- Config fields: `base_url` (default `https://ntfy.sh`), `topic`,
  `bearer_token` (empty initially), `call_enabled` (false initially),
  `timeout_seconds` (15).
- Validate HTTPS, topic shape, message non-empty and <= 1000 characters.
- Use `urllib.request`; send UTF-8 plain text with title, priority, tags, and
  authorization headers where applicable.
- Parse ntfy JSON response and print only safe fields such as message ID and
  status. Never print request headers, secrets, config contents, or endpoint.
- Return meaningful nonzero exit codes for configuration, validation, network,
  and remote errors.
- On Windows, make the created credential file best-effort private without
  failing setup if ACL tightening is unavailable.
- Atomic config creation with exclusive-create behavior; never overwrite.
- Include testable functions and unit tests using mocks/local objects; tests
  must not access the network or user credential directory.
- Include a short module docstring but no embedded credentials.

Return the complete proposed contents of both files in `result.md`, separated
with clear file headings. Do not create files yourself.
