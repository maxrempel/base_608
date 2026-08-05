
## [2026-07-16 16:10] ? 2bd401c8
- DID: Built clickable-link file opener: localhost server (port 47600) opens any local file (md/pdf/etc) in real Chrome; only http:// clicks survive Claude Code, file:// and custom schemes get swallowed
- STATE: DONE+LIVE: server autostarts via Startup VBS (Pine); 'chromelink' trigger word wired as UserPromptSubmit hook so all open sessions succeed w/o restart; documented in global2
- NEXT: Optional: replicate on Sirius/Vega/Centauri
