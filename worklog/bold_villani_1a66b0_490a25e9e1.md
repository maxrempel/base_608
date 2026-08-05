
## [2026-06-26 09:27] x2 db4ebe9d
- DID: Set up anna@maxrempel.com mailbox: saved creds to mxroute_smtp_creds file, added per-mailbox password lookup to mxmail (PASS:<addr> keys), test-sent OK, added BW item 1c5a12ee
- STATE: anna@maxrempel.com fully usable as a sender via mxmail; forwards to max.rempel2@gmail.com (Max set forwarder). Default sender still mass@tamza.com
- NEXT: Switch default sender to anna@ only if Max asks; dnaresonance.org->MXroute migration still a Notion task

## [2026-06-26 11:39] C35 db4ebe9d
- DID: Built+shipped mail_watch doorbell (tools/mail_watch/, commit 16bf0821, pushed to master). Non-Claude Gmail poller on Pine task mail_watch_doorbell (every 12min, StartWhenAvailable, 12-minute-pattern boot grace). Detects new mail to anna@maxrempel.com+mass@tamza.com, wakes C40 via 'bcast wake --name C40'. C40=persistent triage session (detect->alarm Max->sort/catalog), NEVER auto-reply.
- STATE: LIVE. Task registered Ready. Auth/scan/detect verified via --dry-run. Test wake to C40 QUEUED (lands when C40 next takes a turn / wake_listener arms). Max: keep watching ALL assistant-mailbox mail for now (incl Healthchecks noise to mass@), scale down later via WATCH_QUERY mute.
- NEXT: C40 to confirm wake lands on its next turn. Later: optional full-Gmail watch (needs triage filter); optional Telegram/attention fallback when no C40 alive.

## [2026-06-26 15:20] F35 db4ebe9d
- DID: Built+shipped mail_watch doorbell (non-Claude Gmail poller, 12-min Win task, 12-min settle pattern, wakes triage session F40 via bcast). Cleaned C40->F40 refs, committed 4c57dcb4. F40 live+self-briefed. Now watching as F35 on a decel self-wake.
- STATE: Doorbell healthy (polling every 12min, already rang once for real at 14:49). Test wake to F40 still queued - F40 hasn't taken a turn to consume it. Decel timer at 4m rung, idle 2/3.
- NEXT: On next wakes: confirm F40 consumed the queued wake (board post from F40) + keep watching doorbell log. Let decel slow it down if quiet.

## [2026-06-27 07:52] F35 db4ebe9d
- DID: Watching mail_watch doorbell as F35. Pine slept overnight 19:01->07:51; doorbell task Ready, last result 0, next run 8:01 AM.
- STATE: By design the doorbell didn't poll while asleep; 12-min pattern will fire on first post-sleep run (arm 12m settle, no baseline advance, then ring F40 for overnight mail). f4 confirmed F40 mail-division. Decel timer slowed to 30-40m per Max.
- NEXT: Wake ~8:30 to verify the post-sleep 12-minute-pattern ring to F40 actually fires end-to-end in the wild.

## [2026-06-27 17:56] F35 db4ebe9d
- DID: FOUND+FIXED real bug: live doorbell.py (main checkout, what the Win task runs) still had WAKE_TARGET=C40; F40 repoint never landed there. Every ring went to C40 not F40. Pushed b58982bd. One real Mike email (Re: Your DC options) was misrouted to C40 at 17:25; flagged f4 (already handled Mike today).
- STATE: Doorbell now correctly targets F40. Healthy, polling every 12min. Slow flexible decel timer.
- NEXT: Next wake: confirm the next real ring (if any) logs 'RANG doorbell -> F40'. Keep watching slow.
