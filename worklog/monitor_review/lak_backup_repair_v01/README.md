# Lak Cloudflare backup repair v01

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

The `CF R2+D1 restic backup (Lak)` monitor went down after an unrelated
restic maintenance process exited and left a stale repository lock. Scheduled
runs continued creating snapshots but failed during retention pruning, so they
sent failure rather than success pings.

The production script on Lak now:

- uses a non-blocking file lock so scheduled and manual copies cannot overlap;
- runs plain `restic unlock` before backup to remove stale locks without using
  the unsafe `--remove-all` option.

The prior production script is preserved on Lak under the backup tool's
`archive` directory with the date `20260803` in its name.

Verification on 2026-08-03:

- all four R2 buckets synchronized;
- all eleven D1 databases exported;
- a new 2.204 GiB restic snapshot was saved;
- retention pruning completed;
- the success ping was delivered;
- Healthchecks API reported the check as `up`;
- a forced overlapping invocation exited cleanly without disturbing the owner.

No credential payload is stored in this worklog.
