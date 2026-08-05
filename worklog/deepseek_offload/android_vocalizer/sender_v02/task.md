# Android Vocalizer sender version 01

Draft a small production-quality Python 3 command-line sender and tests.

Target files are `android_vocalizer.py` and
`tests/test_android_vocalizer.py`.

Requirements:

- Standard library only.
- `setup` creates a private JSON settings file if absent. Generate an
  unguessable ntfy topic with `secrets`. The default file is
  `%USERPROFILE%\Nextcloud\zSyncMain\ssh\android_vocalizer_config_v01.json`.
  Never print private values or the full endpoint.
- `send TEXT` publishes to ntfy over HTTPS.
- Send options: `--title`, `--priority` with routine, urgent, or emergency;
  `--call`; `--dry-run`; and `--config PATH`.
- Map routine to ntfy priority 3. Map urgent and emergency to 5.
- Routine and urgent publish a push. `--call` adds `Call: yes`; it must fail
  clearly if no bearer value is configured. Emergency automatically requests a
  call and likewise requires a bearer value.
- Settings fields: `base_url` defaults to `https://ntfy.sh`; `topic`;
  `bearer_token` empty initially; `call_enabled` false initially; and
  `timeout_seconds` 15.
- Validate HTTPS, topic shape, and non-empty message up to 1000 characters.
- Use `urllib.request`; send UTF-8 plain text with title, priority, tags, and
  authorization headers when applicable.
- Parse ntfy JSON response and print only safe fields such as message ID and
  status. Never print request headers, private settings, or endpoint.
- Meaningful nonzero exit codes for settings, validation, network, and remote
  errors.
- On Windows, make the new settings file best-effort private without failing
  setup if access tightening is unavailable.
- Atomic file creation with exclusive-create behavior; never overwrite.
- Include testable functions and unit tests with mocks; tests must not access
  the network or user settings location.
- Include a short module docstring. Do not embed any real private values.

Return complete proposed contents of both files in `result.md`, separated with
clear file headings. Do not create files yourself.
