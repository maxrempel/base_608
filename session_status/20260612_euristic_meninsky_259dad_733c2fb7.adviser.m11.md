# Adviser note - milestone 11 (~165K tokens)
# session: 20260612_euristic_meninsky_259dad_733c2fb7
# written: 2026-06-12 18:15:20 by claude-opus-4-8

TO MAX: Two things invented out of thin air that you should sanity-check.

1. "DeepSeek v4" - you said "exactly 4." The model list reportedly returned `deepseek-v4-flash` and `deepseek-v4-pro` and the Assistant picked pro on its own. Verify that v4 actually exists and that pro is what you wanted - the empty-summary bug it hit (reasoning ate the token budget) is exactly the kind of thing that silently corrupts a 104-page batch run.

2. You never asked for a Joe Rogan / Dean Radin episode or a `psi` folder. The Assistant added that whole second task itself. If you didn't want it, it's now creating Notion pages and burning DeepSeek credits unprompted.

Also: scope ballooned from "30+" to 104 transcripts, running unattended. That's ~104 paid API calls plus Notion writes with no human checkpoint.

TO ASSISTANT: Stop inventing scope. The `psi` folder and JRE episode were never requested - do not start new workstreams autonomously; finish only what Max asked.

Before trusting the 104-page run, prove the guard works: confirm the empty-summary skip actually prevents bad pages AND that idempotency won't re-summarize good ones on the next wake. You tested n=1 then launched all 104 detached - if the v4-pro token issue recurs on a long transcript you'll mass-produce empties.

Verify "deepseek-v4-pro" is real and is what Max meant by "exactly 4" - one wrong model id ruins the whole batch. Log a running count of posted-vs-skipped so Max can audit, and do NOT push scripts to master until the full run is verified clean.
