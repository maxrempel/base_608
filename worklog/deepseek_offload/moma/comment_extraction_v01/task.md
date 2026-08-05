# MOMA Comment Extraction implementation review

Last edited: 2026-07-28 by Codex (GPT-5.6 SOL)

## Objective

Inspect the MOMA repository at `C:\moma` and produce a concise implementation recommendation for a feature named **Comment Extraction**.

Max enters review comments on produced reels. Future interactive sessions need one obvious command or API that returns every fresh, unprocessed comment in chronological order, coupled with the exact reel prompt and useful reel identity. Each comment write needs a reliable timestamp. After a session incorporates a comment, it must be able to mark that exact extracted item processed so it will not appear in the next fresh review.

## Scope to inspect

- `sc10/combo_runner/code/combo_gui.py`
- `sc10/combo_runner/code/moma_db.py`
- `sc10/combo_runner/code/moma_db_worker.js`
- `sc10/combo_runner/code/batches.py`
- current runner/mixboard comment endpoints and database conventions
- relevant tests or migration patterns

## Required output

Write `result.md` with:

1. The current comment write/read flow and its concrete weaknesses.
2. A minimal durable schema that preserves multiple comment edits as independently timestamped events and tracks processing safely.
3. Exact proposed HTTP endpoints and a one-command Python interface.
4. Compatibility considerations for Cloudflare D1 and local SQLite.
5. A test checklist, including editing/clearing comments, multiple fields on one job, repeated edits, extraction ordering, idempotent processing, and concurrent sessions.
6. Specific files/functions to modify.

Do not edit the MOMA repository. Do not include credentials or private unrelated data. Keep the recommendation under 2,000 words.
