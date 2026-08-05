# Scribe handover - milestone 11 (~168K tokens)
# session: 20260615_quirky_kepler_ad43cd_5a3401e9
# cwd: C:\claude_base\.claude\worktrees\quirky-kepler-ad43cd
# written: 2026-06-15 09:11:21 by deepseek-v4-pro

# HANDOVER - Kartoteka Player: Make Like/Dislike Toggle Back to Neutral

**GOAL (Max's own words):**  
"make it possible to uncheck either like or dislike, so it comes back to neutral."  
He wants the thumbs-up/thumbs-down buttons in the in-page player to behave as a three-state toggle: click ? to like, click ? to dislike, click the **same** active button again to clear the vote (back to neutral, no selection).

---

**DECISIONS MADE + WHY (prior session context):**

1. **1-vote-per-song-per-IP** - Implemented via Cloudflare D1 table `votes` with a composite primary key `(song_key, ip)`. The `song_key` is the full `play_url` (YouTube video ID + start timecode). This uniquely identifies a song segment, and the IP comes from `cf-connecting-ip`.

2. **Upsert logic** - The backend uses `INSERT ... ON CONFLICT(song_key, ip) DO UPDATE SET reaction=excluded.reaction, updated_at=...`. This means a second click on the opposite reaction automatically switches the vote; a second click on the same reaction would re-insert the same value (no change). Currently there is **no way to clear the vote**.

3. **Frontend `sendVote()`** - POSTs `{play_url, reaction, performer, song}`. On success, `applyVotes(d)` updates the button highlights: the button matching `d.mine` gets class `voted` (green background), and counts are shown. When `mine` is `null` (no vote), neither button is highlighted.

4. **GET endpoint** - `/kartoteka/vote?play_url=...` returns `{likes, dislikes, mine}` where `mine` is the current IP's reaction or `null`. Used by `loadVotes()` on song change.

5. **Worker deploy method** - The worker is updated via a Cloudflare API PUT (multipart), not wrangler. The source of truth is `C:\Users\maxre\Nextcloud\z_tamza_site\worker.js`. Each deploy backs up the previous version with a date stamp to the `archive/` folder, and the changelog in `DEPLOY_INSTRUCTIONS.txt` is updated.

6. **app.js deploy** - Uses `deploy_catalog.py --appjs`, which uploads to R2 `wp-content/kartoteka/app.js` after backing up the live version to `archive/`. No purge needed; CDN cache TTL is 300s.

7. **Sibling coordination** - b7 also deploys `app.js` and `data.json`. After any deploy, the operator broadcasts via `bcast.py` so b7 knows the live file changed. Already done for v40.

---

**CURRENT STATE:**

- Worker **v40** is live, D1 table `votes` created, `app.js` on R2 contains the second button row with report/like/dislike.
- Like/dislike work: clicking different button switches the vote; clicking the same button again does nothing (stays highlighted). Counts reflect correctly. 1-per-IP enforced.
- Commit `70767968` is pushed to `origin/master`, remote is up to date. Sibling broadcast for v40 has been sent.
- Playwright visual test **not done** (profile was locked by another session), but live-byte checks confirmed the code.
- No known regressions; the Top-20 heading rename from sibling is preserved.

---

**EXACT NEXT STEP (to implement the uncheck/neutral feature):**

### Frontend (`tools/tamza_songs/pipeline/output/app.js`)

1. **Modify `sendVote(reaction)`** - After extracting the current radio row, check `d.mine` (the current vote state) from the last loaded data.  
   - If the requested `reaction` is the same as `d.mine`, change the `reaction` sent to the backend to `"none"` (a special value meaning "clear").  
   - Otherwise, send the normal `reaction`.

2. **Modify click handlers** - Currently they call `sendVote('like')` or `sendVote('dislike')`. No change needed; `sendVote` will decide whether to clear or switch.

3. **Update `applyVotes(d)`** - It already handles `mine=null` (removes `voted` class). No change needed if the backend returns `"mine": null` when cleared.

4. **(Optional but good)** Ensure `loadVotes` works correctly after a clear, so that refreshing the UI shows no highlight.

### Backend (`C:\Users\maxre\Nextcloud\z_tamza_site\worker.js`)

1. **POST handler** - Before the current validation, check if `b.reaction` is `"none"`.  
   - If `"none"`, **delete the row** from the `votes` table for this `(song_key, ip)`.  
   - After deletion, perform the same count query to return `{ok:true, likes, dislikes, mine: null}`.  
   - The existing upsert path stays for `"like"`/`"dislike"`.

2. **Keep backwards compatibility** - The same POST still works for like/dislike switching. Deleting a row leaves no trace, so a subsequent like/dislike will insert fresh.

3. **VERSION bump** - Update the worker's first-line comment to `v41` and add a changelog entry in `DEPLOY_INSTRUCTIONS.txt`. Backup the current v40 worker before deploying.

4. **Test the endpoint live** - Use `curl` to POST `"reaction":"none"` and verify counts go down and `mine` is `null`. Then like again to confirm insert works from neutral.

### Deploy order

1. Deploy worker v41 (API PUT).
2. Deploy app.js (with `deploy_catalog.py --appjs`).
3. Commit both changes, push to master, broadcast to siblings.

---

**OPEN QUESTIONS (awaiting Max):**

- Should the uncheck be possible only for the same button, or should any click on an already-active button return to neutral? The request specifies "uncheck either like or dislike, so it comes back to neutral," which strongly implies clicking the **selected** button again clears it.
- Is there any need to limit clear actions (e.g., cooldown) or just instant? No instruction, so assume instant toggle.

---

**KEY PATHS / IDS:**

- **Worker source:** `C:\Users\maxre\Nextcloud\z_tamza_site\worker.js`
- **Worker deploy script:** API PUT (documented in `DEPLOY_INSTRUCTIONS.txt` in same folder)
- **app.js source:** `C:\claude_base\tools\tamza_songs\pipeline\output\app.js`
- **app.js deploy:** `C:\claude_base\tools\tamza_songs\pipeline\scripts\deploy_catalog.py --appjs`
- **D1 database:** `tamza-reports` (UUID `89d4699c-5f58-49de-b31d-c6d22581c73f`), table `votes`
- **Git worktree:** `C:\claude_base\.claude\worktrees\quirky-kepler-ad43cd`
- **Branch broadcast script:** `C:\claude_base\branch_bulletin\bcast.py`

---

**GOTCHAS / DEAD ENDS RULED OUT:**

- **Do not change the table schema** - The PRIMARY KEY is fine; deleting a row is clean and doesn't break future counts.
- **Do not introduce a new state like 'neutral' stored in reaction** - That would require adjusting the SUM() queries to ignore that value, which is fragile. Deletion is simpler.
- **Avoid edge cases** - If the user has no vote (`mine` is `null`) and they click like/dilike, `sendVote` will just post the normal reaction (since `d.mine` is `null`, not equal to the clicked one). That's correct.
- **Playwright browser test** - Still blocked by sibling session; verify via live R2 bytes + curl endpoint instead.
- **Worker v40 is live** - Do not overwrite it blindly; backup first with a timestamp, then deploy v41. Ensure the backup name includes "v40" for easy rollback.
- **Cache** - No explicit cache invalidation needed; app.js will pick up after ~5 min. The worker has no-cache headers already.
- **Sibling b7** - After deploy, broadcast again warning them that worker is now v41 and app.js has uncheck logic; they should pull/merge before their next deploy.
