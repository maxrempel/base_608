
## [2026-06-17 13:20] ? 2d46a16d
- DID: Relaxed context-discipline rules in global2.md for 1M Opus; softened PREVENT DESKTOP SUICIDE to light SESSION HYGIENE; backed up strict versions to C:\claude_base\context_discipline_backup_tomemex.md
- STATE: Edits done in global2.md (CONTEXT DISCIPLINE now discretionary-by-size + model-conditional Opus/Fable; suicide section now light hygiene). block_death_spiral hook still wired.
- NEXT: Optional: raise harness ~169K auto-compact threshold (settings.json) if Max wants fewer compactions

## [2026-06-17 14:11] ? 2d46a16d
- DID: Softened all 3 per-turn context hooks (worklog/gauge/status) to gentle tone; raised gauge cliff 169K->840K for 1M; relaxed context-discipline rules to discretionary-by-size + model-conditional; trimmed death-spiral section to light hygiene
- STATE: All committed+pushed to master (claude_base). global2.md edits live in Nextcloud. Strict originals backed up in context_discipline_backup_tomemex.md
- NEXT: Writing a change report into the backup file per Max's request

## [2026-06-25 14:14] ? 2d46a16d
- DID: Fixed DeepSeek daily cost leak: (1) throttled bcast safety_watcher to judge once per 30min/team instead of every 10min sweep; (2) root-caused broken ledger attribution = Cloudflare 1010-bans Python-urllib UA, added browser UA to ds_report.py - fixes all consumers. Verified end-to-end.
- STATE: Both committed+pushed to claude_base master. Culprit was safety_watcher (~70% of daily spend). Ledger now classifies correctly.
- NEXT: Address Max's 'Check-in is C35' message - likely bcast id assignment but abrupt, confirm before acting
