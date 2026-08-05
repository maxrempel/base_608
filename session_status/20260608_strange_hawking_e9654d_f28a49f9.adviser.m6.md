# Adviser note - milestone 6 (~92K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# written: 2026-06-08 10:49:16 by claude-opus-4-8

TO MAX:
This is a big, multi-system rework (Notion marks, sass split/assemble, sb liftup) described in one dense paragraph. Before any code, make the Assistant read back its plan and pick ONE slice to do first. Your real goal - "force sloppy LLM sessions into correct format programmatically" - is the hard part; don't let it get buried under the easy line-merging plumbing.

TO ASSISTANT:
Do not start coding yet. The prompt bundles at least five distinct changes: (1) merge-command parsing (e.g. "merge lines 2,3,4"), (2) a naming convention like lines2-4, (3) sass splitting then re-assembling the combined mp3, (4) sb liftup replacing the multiple lines, (5) programmatic enforcement so sessions can't skip the format. Restate this as a numbered plan and confirm with Max before touching files. Flag open questions explicitly: what marks encode a merge in Notion, who writes them (hand vs template), and where enforcement lives. Pick the smallest end-to-end slice first. No silent scope guesses.
