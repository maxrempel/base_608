# libas01 - Libretto Assembler Report

Date: 2026-04-16
Author: Claude Opus 4.7 (1M) on Vega, via Claude Code
Script name: libas01 (libretto assembler v01)

## Purpose

Auto-assemble the current CONTACT COUNTDOWN movie script (formerly Kazarian movie) from individual scene pages in Notion into a single timestamped page under an "assemblies" subfolder. Runs every 30 minutes on DAX via cron. Reassembles only when at least one scene has been edited since the last assembly.

## Notion layout

- Parent folder: Current Versions Kazarian movie (page id 3140316f5560815bba63f8aa6daaf4c4)
- Output folder: assemblies (page id 3440316f556081ea8d1dc88ebd875ff3), created 2026-04-16 as a subpage of the above
- Archive: "Archive, move all backups here..." (page id 3430316f55608047afb4ec9a8bbdd79c). The stale page "55 COMPLETE ASSEMBLY (2026-04-11)" was moved there and renamed with OBSOLETE prefix during this session.

## Scene file rule

A page under Current Versions is treated as a scene if and only if:

1. Its title starts with a 1-to-3-digit number followed by whitespace and at least one non-space character. Regex: ^\s*(\d{1,3})\s+\S
2. Its title does NOT contain any of: OBSOLETE, BACKUP, ARCHIVE, ASSEMBLY (case insensitive substring match).

Scenes matched as of 2026-04-16: 10, 12, 15, 20, 30, 50, 60, 65, 75, 77, 80 (eleven scenes).
Assembly order is by the leading scene number, ascending.

## Deployment on DAX

- Host: AWS Lightsail DAX, 35.80.203.42, user bitnami, Debian 12, Python 3.11.2 (stdlib only, no pip dependencies).
- Script directory: /home/bitnami/libas01/
  - libas01.py - main script, uses urllib from stdlib, no external deps
  - run.sh - cron wrapper, cd's into the directory and redirects stdout/stderr to the log
  - .notion_token - chmod 600, contains the internal Notion integration token (same token stored at C:\Users\maxre\Nextcloud2\zSyncMain\ssh\notion_internal_token_20260319.txt on Vega/Pine)
  - state.json - persistent state: last_assembled_max_scene_edit, last_run, last_page_title, last_page_id
  - libas01.log - append-only log
- Cron entry: `*/30 * * * * /home/bitnami/libas01/run.sh`
- Source copy committed in this repo: C:\claude_base\dax_scripts\libas01\

## Algorithm per run

1. Load .notion_token and state.json.
2. GET children blocks of Current Versions page. Filter to child_page blocks whose titles match the scene rule.
3. Compute max_last_edited_time across matched scenes.
4. If state.json has a last_assembled_max_scene_edit equal to or newer than max_last_edited_time, log "no scene change" and exit.
5. Otherwise:
   - Create a new child page under assemblies with title "Kazarian assembly libas01_YYYY-MM-DD_HH-MM" (UTC) and a brief intro paragraph (scene count, max edit timestamp, ordered scene list).
   - For each scene in order, fetch its content blocks recursively, flatten to plain text line by line, and PATCH the new page with a heading "=== Scene NN title ===", a source-id+last-edited meta line, a divider, one paragraph block per text line, and another divider.
   - Update state.json with the new max edit timestamp and the new page id.

## Resumability

- cron service on DAX is systemctl enabled and active, so it auto-starts on reboot.
- Crontab entry persists in /var/spool/cron/crontabs/bitnami.
- state.json lives on disk, so the next scheduled run picks up where the previous successful run left off.
- No long-running daemon, no in-memory state.
- Mid-run reboot: the partially created assembly page stays in Notion and state.json is NOT updated, so the next run produces a fresh complete assembly alongside it. Worst case: one orphan page that can be moved to Archive manually.

## Verification (first live run)

- First run 2026-04-16 23:09 UTC: matched 11 scenes, created libas01_2026-04-16_23-09 with 1022 blocks.
- Second run 30 seconds later: correctly skipped with "no scene change since last assembly".
- Link: https://www.notion.so/3440316f5560816cb93eef5029357ee2

## Known limitations

- Formatting is lossy: the script copies text content only (paragraphs, headings, lists, quotes, to-dos, callouts, code) as paragraph blocks. Inline styling like bold/italic is NOT preserved. This is fine for a rehearsal libretto but not for typesetting.
- No archival of prior assemblies. Over time the assemblies folder will accumulate pages. Housekeeping for old assemblies is manual for now.
- The script exits 0 on partial failures (e.g. one scene fails to fetch) and logs a warning. It will still update state.json on success, so the next run won't retry partially assembled content.

## Possible next steps (not implemented)

- Preserve inline formatting by copying raw block structures instead of flattening to text.
- Auto-archive assemblies older than N days.
- Send a short Notion comment or email when a new assembly is created.
