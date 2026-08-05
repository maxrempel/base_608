
## [2026-06-15 08:26] ? 12626b12
- DID: Diagnosed Telegram alert spam: NOT Sol (healthy). Cause = lak-clawy-kb-backup HC check scheduled in UTC while backup runs 03:30 Pacific -> 'down' ~6h daily; AND fleet_monitor re-sent same critical every 30-90min (keyed on DeepSeek prose that reworded each pass). Backup data itself fine (daily restic snapshots present).
- STATE: Fixed both: set clawy HC check tz=America/Los_Angeles (matches 03:30 PDT run); rewrote fleet_monitor.py alert dedup to key on sorted down-check NAMES + 12h reminder + RESOLVED msg. Deployed to Dax, verified clean pass, committed+merged+pushed. Audited other cron checks - all tz-correct.
- NEXT: Nothing pending. Watch tomorrow's 03:30 PDT clawy run pings green and no re-spam.

## [2026-06-15 10:02] ? 12626b12
- DID: Verified + shipped structural fleet_monitor fix: alarms keyed on HC down-status facts (not DeepSeek prose), EXPECTED_TZ tz self-heal guardrail, 7 tests green, master 93de72c2 pushed & origin in sync, recurrence ledger written
- STATE: DONE - both spam (BUG A) and false-DOWN tz (BUG B) fixed structurally; deployed to Dax; merged/pushed
- NEXT: Nothing pending - watch for resurfacing per recurrence ledger
- LESSON: Never dedup/gate alerts on LLM-generated text; key on deterministic facts. Recurring 'fixed' bugs need a ledger of prior fix claims.

## [2026-06-16 12:07] ? 12626b12
- DID: Fleet health sweep: 14/17 HC checks UP. Only issue = Centauri rebooted 6/15 ~2pm (no auto-logon -> no session -> 'run only when logged on' tasks couldn't run). Fixed host-heartbeat to run as SYSTEM (now UP, reboot-proof). Memex-backup broke under SYSTEM (0-byte zip) so reverted to user; Odysee sync needs a session too.
- STATE: Lak/Dax/Sol healthy; ds_ledger+fleet_monitor up. Centauri host UP. memex-backup(1d stale) + odysee need a logged-in session
- NEXT: Ask Max: enable auto-logon on Centauri so backup+odysee survive reboots (needs his Windows pw)
- LESSON: Headless Windows box: pure-ping tasks can run as SYSTEM, but tasks using a per-user Python/env hang or produce empty output as SYSTEM -- those need a real user session (auto-logon).

## [2026-06-16 12:32] ? 12626b12
- DID: Diagnosed Centauri reboot fix: maxre is a MICROSOFT account w/ PIN login (142525 is the Hello PIN, NOT the password - ValidateCredentials=False). Classic registry auto-login needs the real MS password, so unattended auto-login impossible with the PIN. Reverted bogus AutoAdminLogon/DefaultPassword cleanly. host-heartbeat already SYSTEM=reboot-proof and UP; memex-backup + odysee depend on a maxre GUI session (Nextcloud desktop client + OdyseeSync GUI app).
- STATE: centauri-host UP(SYSTEM). centauri-memex-kb-backup grace. centauri-odysee-sync DOWN (Odysee GUI needs session). Auto-login registry reverted to clean state.
- NEXT: Ask Max the one real fork: (A) give MS-account password -> true auto-login self-heals every reboot, or (B) he RustDesk-logs-in w/ PIN after the rare reboots. Optionally make host-heartbeat alert 'Centauri up but no session' so he knows to log in.
- LESSON: Before setting Windows auto-login, CHECK account type: Get-LocalUser PrincipalSource + ValidateCredentials. MicrosoftAccount + a 6-digit PIN means the PIN is NOT the password and registry AutoAdminLogon cannot work.

## [2026-06-16 12:46] ? 12626b12
- DID: FIXED Centauri fully. MS-account auto-login (maxrempel@icloud.com / pw L2w3e4r5t=) set in registry Winlogon works: reboot -> maxre auto-signs-in at console -> OdyseeSync + Nextcloud + monitoring tasks all start. 2FA did NOT block auto-login on the enrolled device. Triggered both user tasks; backup zipped ~1581 files and pinged.
- STATE: ALL 3 Centauri Healthchecks UP: centauri-host (SYSTEM, reboot-proof), centauri-odysee-sync (up), centauri-memex-kb-backup (up). MS creds saved to shared_logins_frequent.txt. Auto-login self-heals every reboot now.
- NEXT: Centauri task complete. Earlier ds_ledger expense work (7d/30d/lifetime windows + dashboard URL in alerts) already committed 3ba6378b. Nothing pending unless Max raises something.
- LESSON: Microsoft-account Windows boxes CAN auto-login via registry AutoAdminLogon even with 2FA enabled, as long as the device is already enrolled and you use the real MS-account password (not the Hello PIN). Verified on Centauri 2026-06-16.
