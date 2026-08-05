# Adviser note - milestone 10 (~164K tokens)
# session: 20260609_romantic_ritchie_3ecc2a_d087b720
# written: 2026-06-09 12:44:36 by claude-opus-4-8

TO MAX: The Assistant edited and committed/pushed to your LIVE master checkout (C:\moma), not the worktree it was spawned in. Commit f81afaa is already on master. If that wasn't your intent, decide now whether to keep it there or move it. Also your last message "we are still making b rolls" sounds like the Assistant misread your goal - it built a BROLL-line parsing feature; you may have just meant clip production is ongoing. Clarify before it does more.

TO ASSISTANT: Stop and confirm scope with Max - his "still making b rolls" likely means you solved the wrong problem. Two real concerns: (1) You committed to master from a worktree session without confirming that was wanted - that bypasses the worktree isolation. Verify Max wanted master, not the branch. (2) You found a 0-based vs 1-based line_hash mismatch between sass manifest and libup spine and called it "pre-existing, won't touch." That off-by-one is exactly what binds clips to slots - if your b-roll hash uses libup's numbering but the manifest uses the other, the clip won't bind. Do not declare this "verified offline" and done until you prove the SAME hash flows through both paths for a broll line. Don't insert any real b-roll until Max confirms what he actually asked for.
