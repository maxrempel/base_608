# Scribe handover - milestone 7 (~113K tokens)
# session: 20260615_quirky_kepler_ad43cd_5a3401e9
# cwd: C:\claude_base\.claude\worktrees\quirky-kepler-ad43cd
# written: 2026-06-15 08:54:02 by deepseek-v4-pro

# HANDOVER - Session B10: Tamza Player Button Row

---

## GOAL (Max's exact words, final turn)

> "It is very hard to see the link. Make a real button, create a second row of buttons under current ones. Next add two buttons Like and dislike. But don't call them, just use thumbs up and down."

Three tasks, in priority order:
1. **Replace the "????????" link** (added this session) with a visible, **real button** - not a text link.
2. **Create a second row of buttons** below the existing player controls / header bar.
3. **Add Like and Dislike buttons** using thumbs-up / thumbs-down emojis or icons - do NOT label them with words like "Like" or "Dislike."

---

## DECISIONS MADE + WHY

### Completed this session (before the final request):

- **Where to put the "????????" link:** In the player header bar, next to the close ("?") button. *Reasoning:* It mirrors the report link already present in the song list rows; the user wanted to avoid navigating back to the list to report a mislabeled song.
- **How to wire it:** Refactored the existing `openRep(...)` function to accept an optional pre-built row object (new internal `openRepForRow(row)`). The list-row click handler still builds a row from DOM attributes and calls `openRepForRow`; the player button builds a synthetic row from the currently-playing song's JS object and calls the same function. *Reasoning:* DRY - one modal, one set of prefilled fields, no duplicated logic.
- **CSS approach:** Added a `.player-report` style scoped to the brown player header bar, with white text, underline, and hover opacity. *Reasoning:* Minimal visual intrusion while matching the header's color scheme.
- **Deployment:** Used `deploy_catalog.py --appjs` which backs up live `app.js` to archive, uploads the new one, and verifies byte-match. *Reasoning:* Reversible, safe, existing pipeline.
- **Broadcast:** Posted to the shared bulletin board (`bcast.py post`) warning b7 that `app.js` was updated, because b7 also deploys that file. *Reasoning:* Prevent sibling overwrite from a stale build.
- **Git sync:** Committed and pushed to master. The commit also brought the already-live media-session code into git (the worktree's HEAD was behind production). *Reasoning:* Keep git == production, avoid future diffs confusing the next developer.

### What the final request changes:

- The text link "????????" in the player header is **too subtle** - the user explicitly said "it is very hard to see." So the link must become a button (likely styled with background, border, padding to stand out).
- A **second row** of buttons is needed - this implies a layout change in the player bar. The current player bar has one row of controls (play/pause, close, etc.). A new row beneath it should hold the report button + like/dislike buttons.
- **Like/Dislike** are new functionality - they didn't exist anywhere before. They need thumbs-up and thumbs-down emojis (? / ? or similar) as the sole visual label - no text.

---

## WHAT IS DONE

- ? The "????????" **text link** exists in the player header and is live on the production site (`https://tamza.com/wp-content/kartoteka/app.js`).
- ? Clicking it opens the same report modal as the list-row button, prefilled with the current song's artist/title/youtube-id.
- ? `openRep` refactored into `openRepForRow` - callable from both list rows and player.
- ? CSS class `.player-report` created (currently styles it as an underlined text link - **this is what Max wants changed**).
- ? Deployed, committed (ff077aac), pushed to master, broadcasted.

## CURRENT STATE - IN FLIGHT

- ? The "????????" element is still a **text link** - Max wants a real button.
- ? No second row of buttons exists yet.
- ? No like/dislike buttons exist yet.
- The codebase is clean and matches production (no uncommitted drift aside from the future changes needed here).

## EXACT NEXT STEPS

1. **Read the current player bar HTML/CSS** in `app.js` to understand the exact DOM structure and styling of the player header. (The player is rendered via JS - find the string template that builds it, likely containing `data-radio`, `.player-header`, or similar.)
2. **Design the second row:** Create a new `<div>` (e.g., `.player-actions-row` or similar) positioned below the existing player controls row, styled with appropriate spacing/background to look like a natural extension of the player bar.
3. **Convert "????????" to a button:** Change the `<a class="player-report">` into a `<button>` (or styled `<a>` that looks like a button), give it a background color, border, padding - something that stands out. Place it in the new second row.
4. **Add Like button:** A button with ? (thumbs-up emoji/unicode) as its content. Wire a click handler - this is new logic. Decide: does it store a like? Send to server? Just UI feedback? (This was not specified - it's an **open question** below.)
5. **Add Dislike button:** A button with ? as its content, same open question about backend.
6. **Update CSS** to style the new row and buttons (probably in the existing `<style>` block in `app.js`).
7. **Syntax check:** `node --check app.js`
8. **Deploy** via `deploy_catalog.py --appjs`
9. **Broadcast** to bulletin board so b7 (and others) know `app.js` changed again.

## OPEN QUESTIONS (awaiting Max)

1. **What should Like/Dislike actually DO?** No backend endpoint or existing like/dislike logic was found in `app.js`. Options: (a) just UI toggle (highlight when clicked, no persistence), (b) send to server (needs an endpoint spec), (c) store in localStorage. This blocks implementing the click handlers beyond a visual toggle.
2. **Where exactly should the second row appear?** Inside the same brown header bar? Below it as a separate band? In the iframe container? The user said "under current ones" - the current ones are in the player header. Clarify if the new row should be inside or outside the brown header `<div>`.
3. **Button sizing and colors?** "Real button" could mean many things - a filled pill, an outlined button, matching the existing player's color scheme? Needs a quick design preference or permission to choose sensibly.

## KEY PATHS, IDS, AND COMMANDS

| What | Path/Command |
|---|---|
| **Live app.js** | `https://tamza.com/wp-content/kartoteka/app.js` |
| **Worktree app.js** | `C:/claude_base/tools/tamza_songs/pipeline/output/app.js` |
| **Deploy script** | `C:/claude_base/tools/tamza_songs/pipeline/scripts/deploy_catalog.py --appjs` |
| **Syntax check** | `cd C:/claude_base/tools/tamza_songs/pipeline/output && node --check app.js` |
| **Bulletin broadcast** | `python C:/claude_base/branch_bulletin/bcast.py post "message"` |
| **Git remote** | origin/master, commit ff077aac is HEAD |
| **Backup archive** | `C:/claude_base/tools/tamza_songs/pipeline/output/archive/live_backup_*_wp-content_kartoteka_app.js` |
| **Existing report function** | `openRepForRow(row)` - refactored, takes row object with `.dataset.artist`, `.dataset.title`, `.dataset.src` |
| **Existing report link in player** | `<a class="player-report" ...>????????</a>` - selector `a[data-rep-player]` or class `.player-report` |
| **Player header CSS class** | Brown header bar inside the player iframe/radio container - find via `data-radio` or `player-header` |
| **Like/Dislike (new)** | No existing code, selectors, or backend - starts from scratch |

## GOTCHAS + DEAD ENDS RULED OUT

- **Do NOT deploy raw app.js without syntax check** - `node --check` must pass first.
- **The worktree was behind production** - the already-live media-session code wasn't in git. That's now synced. If you see media-session code in your diff, it's NOT your change - it's pre-existing and must stay.
- **Deploy is reversible** - `deploy_catalog.py --appjs` creates a timestamped backup in `archive/` before uploading. To roll back, swap the backup file back to the live path.
- **b7 conflict risk** - b7 also deploys `app.js`. Always broadcast after any change to this file so they don't overwrite with a stale build.
- **The "????????" link is live RIGHT NOW** - your first edit must change the existing element, not add a duplicate.
- **openRepForRow expects `row.dataset.artist`, `.dataset.title`, `.dataset.src`** - the player's synthetic row object must provide these same properties or the modal will be blank. Currently the player button calls it with a proper object; don't break that wiring when moving the button.
