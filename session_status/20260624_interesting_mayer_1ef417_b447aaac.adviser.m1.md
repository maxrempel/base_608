# Adviser note - milestone 1 (~147K tokens)
# session: 20260624_interesting_mayer_1ef417_b447aaac
# written: 2026-06-24 15:10:40 by deepseek-v4-pro

TO ASSISTANT: When you pass passwords on command lines (curl -d with router password, cmdkey with Cent password, and now documenting that password in global2 for printer setup), those land in shell history and session logs. That's three credentials across this session. For global2 especially - consider whether the printer section should reference "the standard Cent maxre password" rather than hardcoding the literal. The router password in curl commands is worse since those are GET/POST logged. Use netrc files or stdin pipes where available, or at minimum flag to Max that these are in the transcript.

TO MAX: The printer setup is solid - IP pinned, Pine works, Oksana's PC path is clear. One thing: the exact Cent password is now written in global2.md (shared via Nextcloud) and appears in this session's raw logs. If you're fine with that given LAN-only, cool. If not, tell the Assistant to redact global2 to just reference "standard Cent maxre credentials" and purge the log copies.
