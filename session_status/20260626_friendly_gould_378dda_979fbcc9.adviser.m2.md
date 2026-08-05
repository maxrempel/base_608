# Adviser note - milestone 2 (~180K tokens)
# session: 20260626_friendly_gould_378dda_979fbcc9
# written: 2026-06-26 14:38:36 by deepseek-v4-pro

TO ASSISTANT: You declared the cheat sheet "done" but it's not saved anywhere permanent. The overlay on the BambooHR tab vanishes on refresh, and Max has no offline copy. You created `team_cheatsheet/photos/` but never populated it. Download the 52 portraits via curl (you have the wildcard signed token that's good for months) and build a saved HTML grid there. Also: you spent ~10 scroll/harvest turns fighting a virtualized list before checking for an API - when a page shows 24 of 52 cards, probe the network tab or XHR after the second failed scroll attempt, not the tenth. The API was right there at `/api/v1_1/employees/directory`.

TO MAX: The cheat sheet is only in your chat window and as a temporary overlay on the BambooHR tab - refresh that tab and it's gone. No permanent file was saved. You may want to tell the Assistant to finish the download-and-save step properly. Also, you never answered the automated-vs-manual question on the weekly huddle routine from the prior context - that's still hanging.
