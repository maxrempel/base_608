---
title: Telegram monitor denoise implementation review
version: 01
date: 2026-07-30
last_editor: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

# Objective

Review three tightly scoped monitor-noise changes and return a concise engineering
recommendation. Do not modify files. Do not request or expose credentials.

## 1. Safety watcher false Git-loss pages

File: `C:\claude_base\branch_bulletin\safety_watcher.py`

The watcher already annotates deleted files by checking `git ls-tree HEAD`, but on
July 29 it still sent repeated Telegram pages claiming tracked archive and Cloudflare
backup files were uncommitted, absent from Git history, and unrecoverable. A direct
July 30 check showed:

- the named paths are returned by `git ls-files`;
- none of the named paths are staged;
- the working-tree deletions are therefore recoverable from Git;
- the paid judge ignored or contradicted the evidence annotation.

Recommend a deterministic post-judgment guard that prevents Telegram escalation
when the only stated danger is deletion of files proven present in committed Git
history. It must not suppress a real simultaneous danger such as force-push,
history rewrite, repository deletion, untracked-file deletion, credential exposure,
paid job firing, or database corruption. Recommend exact tests.

## 2. Expense digest cadence

Files:

- `C:\claude_base\tools\ds_ledger\deepseek-balance-report.timer`
- `C:\claude_base\tools\ds_ledger\README_tomemex.md`
- `C:\claude_base\tools\ds_ledger\ds_ledger.py`

Change the routine combined Telegram expense report from four times daily
(00:00, 06:00, 12:00, 18:00 Pacific) to one daily report at 09:00 Pacific.
Preserve all urgent low-balance warnings, spend-threshold alerts, live dashboard,
provider polling, AWS refreshes, and Healthchecks liveness. Identify every text or
test that needs updating. The AWS polling loop must remain four times daily even
though the Telegram digest becomes daily.

## 3. Clipfisher classification

Telegram bot `clipfisher_monitor_bot` currently delivers completed YouTube transcript
audio summaries. Those are product results, not infrastructure alarms. Recommend
the safest denoise option that does not delay, drop, or alter those results. Consider
removing the bot from the default `tg_alerts.py` trouble view and keeping it available
through an explicit flag, rather than changing live delivery.

# Output

Return:

1. root-cause assessment;
2. minimal patch design;
3. concrete test cases;
4. deployment and rollback checklist;
5. any safety concern that should block implementation.
