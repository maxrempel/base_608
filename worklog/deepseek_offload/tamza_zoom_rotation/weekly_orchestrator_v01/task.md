# TAMZA weekly Zoom rotation orchestrator design

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

## Objective

Design a deterministic, idempotent weekly orchestrator for the existing tools in
`C:\claude_base\tools\tamza_zoom_rotation`.

The orchestrator will ultimately run on an always-on Linux server and must:

1. Read the live Google mass-mailing document to determine the current week and
   current rotation link.
2. On the scheduled weekly run, advance the Google Doc exactly once to the next
   week/link.
3. Post that same new week/link to the existing Telegram channel exactly once.
4. Produce the exact Facebook post text and machine-readable state for a separate
   browser/native-scheduling layer. It must not attempt Facebook login itself.
5. Be safe to rerun after partial failure. It must resume missing destinations
   without advancing the Google Doc a second time or duplicating Telegram.
6. Support `--dry-run`, structured logs, retained state, lockout against concurrent
   runs, and a clear nonzero exit on unresolved partial failure.
7. Avoid exposing or copying secrets. Existing credentials remain external.

Read these files fully:

- `C:\claude_base\tools\tamza_zoom_rotation\README_tomemex.md`
- `C:\claude_base\tools\tamza_zoom_rotation\update_mailing_doc_v01.py`
- `C:\claude_base\tools\tamza_zoom_rotation\telegram_post_v01.py`
- `C:\claude_base\tools\tamza_zoom_rotation\google_docs_api_v01.py`
- `C:\claude_base\tools\tamza_zoom_rotation\rotation_links_v01.json`

Return only `result.md` containing:

- recommended state machine and weekly timing;
- exact invariants and failure/retry behavior;
- a compact implementation blueprint, including proposed function boundaries;
- a test matrix covering first run, repeat run, partial failures, week mismatch,
  concurrent launch, and rotation 8-to-1;
- Linux deployment considerations for Lakarian;
- any changes needed to the existing scripts to make orchestration safe.

Do not modify project files. Do not include credentials or live Zoom links in the
result.
