
## [2026-06-10 07:41] ? 18701c80
- DID: maxrempel.com: fixed mobile hamburger menu; embedded noeticusai.com at /noeticus inside site chrome (menu+back, desktop+mobile); renamed menu AI->Noeticus AI, /ai 301->/noeticus; crawled whole site (no nav traps, menu everywhere); fixed RU blog (bare /blog now serves current subdomain lang, ru shows 3 RU posts)
- STATE: All deployed to master + pushed. Site verified live EN+RU, desktop+mobile.
- NEXT: Awaiting Max. Possible follow-up: slim double-menu on /noeticus if desired.

## [2026-06-10 09:12] ? 18701c80
- DID: maxrempel.com/noeticus FINAL: chat widget under SINGLE rempel menu, branded 'Noeticus AI', calls live Noeticus API (config:luminous_api_url +/chat/stream) - tested, streams real answer. Dropped iframe (caused double-menu). /ai 301->/noeticus. RU blog fixed earlier. All on master+pushed.
- STATE: maxrempel side complete+live. noeticusai.com is a SEPARATE site (NOT maxrempel-site worker; not in that CF account's worker list under a noeticus name) - source likely Sol-based luminous_deploy/noeticus_deploy pipeline; backups at C:\Users\maxre\Nextcloud\z_luminous_deploy_backups\backup_20260525_1551_working\ (has dns_noeticusai.com.json, maxrempel_wrangler.toml).
- NEXT: PENDING (Max's last ask): make noeticusai.com ALSO use the Rempel menu (unify nav across both sites, ideally from shared D1 nav table). Must LOCATE the live noeticusai.com worker first - confirm which CF worker/Pages serves it before editing. Do fresh (context was ~145K).
- LESSON: Cross-origin iframe cannot have its chrome hidden from parent; to embed another site menu-less you must add an embed mode to THAT site, or render the widget natively.
