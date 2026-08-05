# Adviser note - milestone 4 (~305K tokens)
# session: 20260703_jolly_austin_dd9aa0_0acef98a
# written: 2026-07-03 16:32:33 by deepseek-v4-pro

TO ASSISTANT: You burned many cycles on deployment bugs that should have been one-and-done. The chain -- CRLF corruption, missing samtools PATH, reference mismatch -- each cost an asto-call window and a self-wake cycle. When a script fails silently, DO NOT re-arm and walk away. Verify it actually launched before leaving it. Check for a running process, a start marker, or log output immediately after the `setsid` call. Your "marker" approach was a good idea you only used on attempt 3 of 5. Also: Sol stress-test was too aggressive (24GB/31GB with verify) and knocked it offline mid-session, directly contradicting Max's later instruction to skip long tests. When Max says "it's fixed," take his word and move to real work.

TO MAX: The insertion hunt on Kristen only started running clean after ~5 deployment attempts spread across several hours. The science logic is sound but the plumbing was shaky. The final INSurVeyor run is underway now and should produce results in 1-2h. One thing to know: Sol's disk corruption was from your repeated hard power-offs -- the fsck fixed it, but if Sol crashes again under load, suspect the disk or RAM rather than rebooting. Your "disposable workhorse" rule for Sol is the right call.
