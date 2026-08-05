# Scribe handover - milestone 11 (~169K tokens)
# session: 20260610_optimistic_yalow_e584a0_793da793
# cwd: C:\claude_base\.claude\worktrees\optimistic-yalow-e584a0
# written: 2026-06-10 06:42:03 by claude-opus-4-8

# HANDOVER - Tamza ????????? / ????? ?????? (you are now B7)

## YOUR IDENTITY
You were just copied from B6 and re-branded **B7**. Max's exact words: *"Copied you from B6, branched just now, you will be b7, but the others are disarmed. sleeping. So register, but you are alone working at the moment."* All other branches (b0 safety gate, b1, b2, b5, c-team) are DISARMED/asleep. There is no one to coordinate with right now - you work solo. Register as b7 via bcast, but do not wait on any sibling branch for gating (they won't answer).

## GOAL (in Max's words)
The newest task, verbatim: *"on android browser, the player popup is not visible in the screen. Maybe just place it not as a popup, but as a replacement screen. So essentially, the play buttons will move the viewer to the next tab, each with its own address."*

Plain reading: the radio player is a fixed-position popup (`#radioBar`, bottom-right) that is off-screen / invisible on Android mobile browsers. Max wants to rethink it - instead of a floating popup, make play navigate to a **dedicated screen/view with its own URL** (a real address per song/player state), so it works on mobile and is shareable/linkable. This also touches a known gap Max has hit repeatedly: there is currently **NO per-song deep link** - search state doesn't persist to the URL, and only `#p=<slug>` (performer) and `#a=<slug>` (author) hash links exist.

This is a DESIGN task - think before coding. Do not assume; Max has corrected wrong assumptions before.

## OVERALL PROJECT CONTEXT
tamza.com/kartoteka is a searchable bard-song catalog (26,283 rows). Each "song" is a segment inside a long YouTube concert video. The "????? ??????" feature plays an author's/performer's songs back-to-back in an embedded YouTube IFrame player, auto-advancing song to song. The catalog "database" is a single JSON file (data.json) served from Cloudflare R2; there is no real DB.

## CURRENT STATE (what is live & working)
- **Live and verified:** the radio player works; the 2-min cap; newest-first play order; ??????/????? skip buttons; band-collapse display; one-line compact rows; "????????" report link; short performer/author links + top-20 chips; per-song timing cap-lift.
- **Just shipped (last action before you took over):** a global **+7 second ending pad**. The constant `END_PAD_SEC = 7` in app.js makes a timed song play to `min(seg_end + 7, nextStart)` - fixes endings being clipped ~7s early (Max caught "????? ?????" cutting before the final applause). Deployed app.js-only, auto-backed-up, live. This was done on Max's direct "of course" after the b0 gate proved pointless (team asleep).
- **Song-timing pipeline (the big background job):** running autonomously on Sol (home server). Phase 2 (DeepSeek mapping of per-song start/end from YouTube captions) is mapping all 509 videos, one at a time, politely. First two videos done. Only ~45 pilot songs (all from ONE mixed concert, video `NastMtX6Mhg`) are currently published live with real ends - so on the live site the radio keeps landing on that one concert until more batches publish.

## EXACT NEXT STEP
1. Register as b7 on the bulletin board (bcast.py - see gotchas re cwd).
2. **Investigate the Android popup problem** before designing: read how `#radioBar` is positioned/shown in app.js, and how the SPA routing/hash currently works (`location.hash`, `#p=`/`#a=` handling around lines 126, 302, 309).
3. Design the "player as a screen with its own address" approach. Decide: does "play moves viewer to the next tab, each with its own address" mean a new browser tab/page, or an in-SPA view swap with a distinct hash/URL? Likely the latter (in-SPA full-screen player view with a per-song URL), but **confirm intent with Max if ambiguous** - he's awake and steering.
4. Prototype, verify (Playwright headless+muted, mobile viewport), then deploy app.js-only on Max's say-so.

## OPEN QUESTIONS FOR MAX
- "Replacement screen with its own address" = a separate browser tab/page, or a full-screen in-app view with its own URL/hash? (Get this right before building.)
- Bigger unresolved policy question I raised earlier and Max hasn't answered: **do we need a verification/correction step for AI-detected song endings before trusting all 509 mapped videos?** Some endings are inaccurate ("2 min of torture then a wrong cut" is worse than the old flat cap). The +7s pad helps clipping but not genuinely-wrong boundaries (esp. recited poems, where there's no musical end).
- Publish new timing batches as Sol finishes each video, or wait for the whole run? (Asked, unanswered.)

## KEY PATHS / IDS
- Live front-end (deploy source): `C:\claude_base\tools\tamza_songs\pipeline\output\app.js`
- Deploy script (app.js only, auto-backup, byte-verify): `C:\claude_base\tools\tamza_songs\pipeline\scripts\deploy_catalog.py --appjs`
- Live URLs: `https://tamza.com/wp-content/kartoteka/app.js` and `.../data.json`; page at `https://tamza.com/kartoteka`
- Radio popup element: `#radioBar` (fixed, bottom-right) - THE thing that's off-screen on Android.
- Timing store: `...\pipeline\song_timing\_work\song_timing.json` (keyed `<vid>:<start_sec>`); enrichment folded into build via `enrich_catalog.py`.
- Sol server: 192.168.1.113, user maxre, SSH key `~/.ssh/sol_key`, work dir `/home/maxre/song_timing/` (venv, cron guard every 15 min, harvest.log).
- Pilot video id: `NastMtX6Mhg`. Pilot transcript: `...\song_timing\_work\transcripts\NastMtX6Mhg.json` (format `{t,d,x}`).
- bcast: `python "C:/claude_base/branch_bulletin/bcast.py"` ; worklog: `C:/claude_base/compaction_kb/scripts/worklog.py`.

## GOTCHAS (already learned the hard way)
- **bcast.py identity is cwd-keyed.** Call it by full forward-slash path with NO `cd` first, or it fails "no id set for this branch." (Bit me repeatedly.)
- **Windows console crashes on Cyrillic** (cp1252). Prefix Python with `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`; dump Cyrillic to UTF-8 files rather than printing.
- **Suicide-prevention hook** blocks the 3rd repeat of a Bash command (normalized first 100 chars) and cancels parallel batches if one errors. Don't loop `python -c` one-liners - write a reusable script file (also Max's rule). Lead bundled commands with a different-prefix command.
- **data.json gets rebuilt** by build_catalog.py (frozen legacy base + fresh recent layer) - never hand-edit it; timing lives in the separate store and is re-merged on rebuild. app.js is a static asset (safe to edit directly).
- **Deploy scope:** deploy app.js + data.json ONLY. Never re-upload index.html/worker.js (reintroduces a dead banner 404).
- **app.js is one big IIFE** - internals aren't global; use the `window.__radio` debug hook for tests.
- **Sol single-instance rule:** NEVER run two timing workers (parallel YouTube hits = block risk). The 15-min cron guard can race manual launches. Authoritative count: `pgrep -cf 'venv/bin/python timing_pipeline'`. Kill-all then ONE clean launch.
- **AI endings are imperfect** - captions-based; reliable for sung songs (~0.95), weak for recited poems.
- **Max's style:** pingpong, TLDR-first, plain English, no code unless asked, no Unicode in output. A question mark = answer only, NO action/no Python. "dtalk" = stop doing, just talk. He hates branch-collisions and lost work; commit + push after meaningful changes.
- **NEVER touch Max's Google/YouTube login** (his channels were terminated - deep trauma). Viewer-side IFrame embed + anonymous yt-dlp/transcript only. NEVER auto-translate transcripts (rate-limit/block risk).
- The KRUGVK "drop ????????? ???????" rule is **VK-migration-only** (Russia-Ukraine war / account-ban politics) - it does NOT apply to the catalog. Don't let it leak again.

## DO NOT
Re-arm any autonomous self-wake loop unless Max asks - he disarmed the team. He said you're "alone working at the moment," so act on his direct requests, stay quiet otherwise, don't invent work.
