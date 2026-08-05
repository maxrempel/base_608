
## [2026-07-22 22:51] ? bfb1d25b
- DID: Funded Liz's Expatrio blocked account: USD 14,177 -> EUR 12,131 via Flywire Pay-by-Bank (Chase ...7302), Payment ID GPX459505491, status Payment sent
- STATE: Payment complete; record file written to Nextcloud applications/expatrio_blocked_account
- NEXT: Await Flywire funds-received email; blocking confirmation doc will follow

## [2026-07-25 13:16] ? c0b63b29
- DID: Fixed Tamza secret Zoom rotation: all 8 links now carry the Restream stream key and have the waiting room off; added scripts + method doc v02; added 3 Zoom OAuth scopes via Playwright
- STATE: Committed and pushed to master (0a81a33c). Playwright lock released.
- NEXT: Nothing pending. If new rotation links are needed, use create_meeting_v01.py in tools/tamza_zoom_rotation.

## [2026-07-26 14:15] ? c0b63b29
- DID: Updated Tamza mass-mailing Google Doc to rotation link 04 (892 8786 3804) and week 27 July - 3 Aug 2026, via claude-in-chrome; backup doc 1c2LdTJOJHEY3qzm5va8FNZRP03cXXD-ijFBqPKWIMbs
- STATE: Doc verified: hyperlink target points at 89287863804, not just visible text. Max approved building real automation.
- NEXT: Build a Google Docs API batchUpdate script in C:/claude_base/tools/tamza_zoom_rotation/ that updates the doc for week N; then Telegram channel Bot API, then FB group tamzazoom via Playwright (Max Steinberg account).
