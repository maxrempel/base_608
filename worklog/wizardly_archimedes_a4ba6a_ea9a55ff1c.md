
## [2026-06-15 10:58] b20 18c5af9c
- DID: Added dated expandable announcement (<details id=katAnnounce>) near top of Kartoteka page via app.js injection above .searchwrap
- STATE: Committed only app.js (master 7096be6a) + pushed; deployed via deploy_catalog.py --appjs, byte-verified live (68187B), backup saved; live app.js confirmed contains injectAnnounce
- NEXT: Visual browser QC pending (shared playwright profile busy with sibling) - Max to refresh tamza.com/kartoteka and click the announcement to eyeball
