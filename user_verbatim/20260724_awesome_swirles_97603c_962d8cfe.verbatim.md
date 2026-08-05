# VERBATIM user (Max) log - session 962d8cfe-bcf7-406a-b458-aa34a495ae85
# cwd: C:\moma\.claude\worktrees\awesome-swirles-97603c
# Every line Max typed, saved verbatim, so it survives compaction.
# Recover specs / investigate trouble by reading this file.


## [2026-07-24 22:26:24] turn 1
Increase the default compaction trigger from 175 to 230,000 tokens. Set it as default in the settings.

## [2026-07-24 22:27:43] turn 2
OK, wonderful. Next trouble is that for some reason I created a new session. So this is a new session and amazingly extraordinary. It started from 130K which is...

## [2026-07-24 22:28:20] turn 3
Which is way above my default instructions that are loaded by default. Because in the past it was about half of that. It was about 70K was instructions. Now it suddenly doubled. So go and search, maybe there is some inflation of instructions that just suddenly happened.

## [2026-07-24 22:29:42] turn 4
Compare the context, because I don't know what global agent rules. It is something very new to me. Somebody created it just recently, and it's super weird. Maybe it was in response to my request, but I don't recognize it.

## [2026-07-24 22:30:16] turn 5
And wait a second, even with that, 40k tokens is not 100, 130k tokens. There is something else which is swallowed, there is 100k tokens which is unaccounted for.

## [2026-07-24 22:31:33] turn 6
The story with Codex is that I migrated to Codex, it swallowed its plan much faster than needed so I am now running parallel Codex and Claude because they both swallow weekly limit in half of the time, in 3-4 days. So that agent rules should be, I guess, updated strongly, basically we are running them in parallel and probably they want to communicate between each other. So review it thoroughly and remove all nonsense and outdated stuff.

## [2026-07-24 22:41:26] turn 7
Python bridges, remove them. DialogTrainer, remove them. Remove it. MCP registry, remove it. Don't delete them, just make them unavailable. Not loaded by default.

## [2026-07-24 22:45:36] turn 8
What is the current size of the automatically loaded tokens?

## [2026-07-24 22:46:15] turn 9
Just tested the context window remains huge.

## [2026-07-24 22:47:41] turn 10
The context is still very big.

## [2026-07-24 22:49:44] turn 11
I tried to, basically I test by creating a new session and the context is 150 tokens, 150,000 tokens, which is super weird.
I'll go ahead and bump the default compaction level to 300 K.
Search online. Maybe there is some weird update and maybe people already discovered that. Because basically it swallows the context very fast. There is something which is loaded which I don't understand what. Let me ask the other session what it is. Search online for now.
