# Scribe handover - milestone 2 (~164K tokens)
# session: 20260629_zzling_lichterman_38ba23_076a9bc5
# cwd: C:\moma\.claude\worktrees\dazzling-lichterman-38ba23
# written: 2026-06-29 16:40:04 by deepseek-v4-pro

# HANDOVER: Suno Music Cataloging - d54

---

## GOAL (Max's own words)

Download ~30 Suno tracks, catalog/annotate them in a database, rename tracks with sequential IDs, star-rate tracks and pieces, cut usable pieces for the movie, and later loop-extend the best pieces with crossfade overlaps.

---

## DECISIONS MADE + WHY

1. **Playwright, not unofficial API:** Max chose Playwright for downloading. Suno has no public API; a 3rd-party/unofficial API would be paid, brittle, and against ToS. Playwright uses Max's logged-in Pro account directly, is free, and gives access to Suno's own internal JSON endpoints (cleaner than clicking 30 "Download" buttons).

2. **Scrape internal API, not UI clicks:** Instead of clicking "..." ? Download 30 times in the UI, the approach pivoted to intercepting Suno's internal `/api/feed/v3` endpoint. This returns a JSON song list with title, style prompt, duration, and CDN mp3 URLs - giving us both the audio files and structured metadata for the catalog in one pass.

3. **Chromium profile issue:** The initial browser session loaded the wrong profile. Closing and reopening Playwright resolved it - second launch landed on max_remple2 (Pro Plan), which is the correct account. This is a known Playwright gotcha: profile persistence depends on how the browser was last closed.

4. **DB location - STILL OPEN:** Earlier, I proposed a separate SQLite/D1 just for music (clean, decoupled from the MOMA movie pipeline), versus adding a table inside the existing MOMA D1. Max has NOT answered this yet. No database has been created.

---

## CURRENT STATE

- **Logged in:** Playwright browser is open and authenticated as **max_remple2 (Pro Plan)** on `https://suno.com/me`.
- **Library visible:** The Library page shows Max's tracks (v9, v8, etc.) with style descriptions and durations.
- **API endpoint discovered:** `/api/feed/v3` is the internal Suno endpoint that lists songs with metadata and mp3 URLs.
- **In flight:** The session was probing the shape of the `/api/feed/v3` JSON response via `browser_evaluate` when Max interrupted. The response structure is partially known but needs full extraction to write the download script.
- **Nothing downloaded yet.** No files written. No DB created. No catalog schema designed.
- **Tasklog entry exists:** "Music project: download ~30 Suno tracks via Playwright, then catalog/annotate/star/cut pieces in a DB"

---

## EXACT NEXT STEP

1. **Finish probing `/api/feed/v3`** - Call `fetch('/api/feed/v3')` from the Playwright console on the authenticated Suno page and dump the full JSON response. Identify:
   - Pagination (how many per page? is there a cursor/offset?)
   - Each song's fields: id, title, metadata (style prompt), duration_seconds, audio_url (mp3 CDN link), created_at
   - Total count to confirm ~30 tracks

2. **Download the mp3s** - Once the JSON shape is known, write a script (Python + requests, using cookies extracted from Playwright) to iterate all pages, download each mp3 to a local directory (e.g., `C:\moma\music\raw\`), and save a `tracks.json` with all metadata.

3. **Wait for Max's DB decision** - Before building the catalog, Max must choose: separate music-only SQLite/DB, or a table inside the existing MOMA D1.

4. **Design catalog schema** - After the DB decision: tables for `tracks` (sequential ID, original title, renamed file, style prompt, duration, description, overall stars) and `pieces` (track_id, start_time, end_time, piece_type like intro/drop/loop, stars, movie_placement_notes).

---

## OPEN QUESTIONS (awaiting Max)

- **DB location:** Separate music database or inside existing MOMA D1?
- **Download directory:** Is `C:\moma\music\raw\` acceptable for the raw mp3s?
- **Naming convention:** Sequential ID format - e.g., `M001`, `M002`? Or date-based? Just numeric?
- **"Stars" scale:** 1-5? 1-10? Something else?
- **Piece types:** What categories of pieces does Max envision? (intro, drop/chorus, loop-able section, bridge, outro, etc.)

---

## KEY PATHS & IDS

| What | Value |
|------|-------|
| Worktree | `C:\moma\.claude\worktrees\dazzling-lichterman-38ba23` |
| Suno account | max_remple2 (Pro Plan) |
| Suno internal API | `https://suno.com/api/feed/v3` |
| Suno library page | `https://suno.com/me` |
| Branch bulletin script | `C:/claude_base/branch_bulletin/bcast.py` |
| Tasklog script | `C:/claude_base/tools/tasklog/tasklog.py` |
| Approx track count | ~30 |
| Working identity | d54 |

---

## GOTCHAS & DEAD ENDS AVOIDED

- **Wrong Chromium profile:** First Playwright launch landed on a wrong/guest Suno account. Fix: close browser (`browser_close`) and reopen - the second launch correctly used max_remple2. If it happens again, the profile may need explicit flagging in Playwright launch args (e.g., `--profile-directory`).
- **UI-click download path abandoned:** Downloading 30 tracks via clicking each "..." menu would be fragile and slow. The internal API approach is faster and gives metadata for free.
- **No official API exists:** Confirmed - Suno has no documented/public API. Any third-party wrapper is reverse-engineered and breakable. Playwright + internal API calls is the safest path.
- **Playwright lock:** The `ScheduleWakeup` tool was used to set a release reminder - if the browser is still held open during a long gap, the next session should call `browser_close` to release the shared lock before proceeding.
