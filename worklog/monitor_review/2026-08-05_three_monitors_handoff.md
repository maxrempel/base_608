# Three expense monitors - cross-links and automation (2026-08-05)

Agent: Codex /root. Task: make the DeepSeek, Claude, and Codex (ChatGPT)
expense monitors constantly updated and cross-linked.

## What changed

- Cross-links added to all three monitors: DeepSeek tracker (both log and
  linear views), Claude allowance tracker, and Codex allowance tracker each
  have a nav row linking to the other two. A `Claude Cost Projector.url`
  desktop shortcut should still be created (only DeepSeek and Codex shortcuts
  exist today).
- DeepSeek: collector was actually running every 20 minutes, but the tracker
  pages loaded `deepseek_balance.js` without cache-busting, so the chart could
  show stale data. Both pages now re-fetch the payload with a timestamp and
  re-render; scheduled task cadence set to 30 minutes per Max's instruction;
  texts and README updated to 30 minutes. Verified: page renders $8.92 with
  403 snapshots and "Updated" label.
- Claude: added the official 18% reading from Max's screenshot (observed
  2026-08-05 09:32, reset Fri 2026-08-07 20:59) to the tracker seed and made
  the tracker default to the current weekly cycle. Tracker now also loads
  `claude_readings.js` (same pattern as the other monitors) and cache-busts it.
  New `collect_claude_usage_v01.py` reads the logged-in Claude usage page
  hourly and appends readings; scheduled task `Claude Usage Collector` runs it
  hidden every hour. Verified the tracker renders 18% / reset Aug 7 8:59 PM.
- Codex (ChatGPT): already auto-updates via the Lakarian API collector +
  Pine sync (`allowance_history.js` + `session_usage.js`); verified fresh at
  09:40 and 09:30. No browser login needed.
- Recurring 6-hour audit wake armed (f8f62be2) to verify all three monitors.

## Known human step (blocking for Claude automation)

claude.ai login is behind a Cloudflare bot wall; automation cannot log in.
A real-Chrome window with the dedicated monitor profile
(`C:\Users\maxre\AppData\Local\ClaudeUsageMonitor\profile`) was opened at
claude.ai/login for Max to complete the one-time login (account
max.rempel2@gmail.com). Until that login succeeds, the Claude collector writes
`status: login_required` to `collector_state.json` and retries hourly. Close
the login window after signing in so the hourly collector can use the profile.
