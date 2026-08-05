
## [2026-06-17 08:51] ? aa23f003
- DID: Built mass@tamza inbox watcher (tools/mass_check/mass_check_v01.py, read-only IMAP) + 20-min wakeup timer (id 942e2050). Fixed global2: restored 'do homework/search Memex before asking' rule at top; added machine job-placement policy (Dax=low-cpu crons, Lak=high-disk only, Cent+Sol less-valuable/Sol down, Liz's 'asto' to offload Lak, genomics=Sol or AWS VM). Identified Clawy=OpenClaw lobster bot on Sol via Telegram.
- STATE: global2 edits saved+local. mass_check committed+pushed. 20-min timer live, firing OK (nothing new). asto sudo question answered; drafted minimal reply to Liz.
- NEXT: Decide: duplicate mass@tamza check to Dax as low-cpu cron (policy says Dax). Confirm Liz reply send method. Consider committing global2 (it's in Nextcloud, not git).
