# Scribe handover - milestone verify1 (~166K tokens)
# session: VERIFY_vigorous_jemison_5edc814f
# cwd: C:/claude_base/.claude/worktrees/vigorous-jemison-340d7a
# written: 2026-06-07 13:11:55 by claude-opus-4-5

# Handover for Session 5edc814f-2a47-4c16-bc2c-c7ea422b2aa1
(Worktree: vigorous-jemison-340d7a | Host: C1 / compaction-experiment coordinator)

---

## Goal (in Max's words)

Build a multi-branch coordination system where parallel Claude Code chats ("branches") share lessons and decisions rather than diverging. Then run a compaction-calibration experiment to learn exactly when and how Claude loses context. Make it programmatic ("because Opus ignores instructions").

Later, Max wanted **two oversight agents**: the **Scribe** (a neutral, rich handover writer) and the **Adviser** (a skeptical, active guardian that can whisper warnings back into the session and to Max).

---

## Key decisions and why

| Decision | Why |
|----------|-----|
| bcast.py broadcast board, local append-only JSONL | One shout ? all named branches hear; no remote deps. |
| Identity keyed by worktree cwd (sha1 hash) | Each worktree isolates its own branch name. |
| Two-mode halt: standby (keep timer) vs full halt | Old halt killed timers so workers never woke; standby keeps them reachable. |
| 4-min self-wake timer **mandated** at whoami + every board read | Workers were silently dropping off; this makes dormancy impossible. |
| c-prefix for compaction team (c1/c2/c3/c0), b-prefix for kartoteka team | Two teams collided on the same board with duplicate b1?b4 labels; separate prefixes fix it. |
| ~15K-token milestones for status dumps | ~11 dumps before the ~169K compaction cliff; spaces snapshots across the danger zone. |
| Two-layer status: mechanical breadcrumb (guaranteed) + richer model report (best-effort) | Guarantees at least a breadcrumb even if the model ignores the nudge. |
| Read personality from editable text files (`scribe.md`, `adviser.md`) | Max can tune behavior without touching code. |

---

## Current state

| Item | Status |
|------|--------|
| bcast.py broadcast board | Live, committed, two-mode halt + 4-min timer mandate shipped. |
| Compaction calibration | Solved: auto fires ~169K (~85%), ~94% memory loss; 149 events harvested; data in `compaction_kb/kb/`. |
| worklog.py per-worktree durable journal | Live, Component 6 declared DONE. |
| session_status.py token-milestone breadcrumbs | Live, hook wired (Pine settings.json). |
| The Watch (Scribe + Adviser) | Freshly wired. Worker built it; c1 just made personalities editable. Now running an end-to-end test to confirm real Opus output persists. |
| Inter-team channel feature (per-job board + addressed cross-team posts) | Designed but parked; not yet built. |

---

## Exact next step

Confirm the end-to-end test of session_oversight.py produces persisted `.handover.*` and `.adviser.*` files. Then commit the editable-personality fix and declare the Watch live.

---

## Open questions for Max

1. Trigger size for status dumps: keep 15K tokens, or tighter/looser?
2. Inter-team channels: assign a worker to build, or park?
3. Want a real chat backup (cc_recover-style) in addition to the lightweight trace, or is the trace + Scribe handover enough?

---

## Key file paths / IDs

| What | Path |
|------|------|
| Broadcast board tool | `C:\claude_base\branch_bulletin\bcast.py` |
| Token-milestone hook | `C:\claude_base\compaction_kb\scripts\session_status.py` |
| Oversight runner (Scribe + Adviser) | `C:\claude_base\compaction_kb\scripts\session_oversight.py` |
| Personality files | `C:\claude_base\compaction_kb\personalities\{scribe,adviser}.md` |
| The Watch manual | `C:\claude_base\compaction_kb\the_watch_oversight_tomemex.md` |
| Pine settings (hooks) | `C:\Users\maxre\.claude\settings.json` |
| worklog output | `C:\claude_base\worklog\<worktree>_<hash>.md` |
| Status output | `C:\claude_base\session_status\<date>_<project>_<session>.md` |
| Compaction KB | `C:\claude_base\compaction_kb\kb\compaction_events.jsonl` |

---

## Gotchas and dead ends

- Never `cd` before running bcast.py ? identity is keyed by cwd; cd breaks it.
- Use forward slashes in Bash commands; backslash paths lose chars.
- A Stop hook (decision=block) forces session continuation = wedge risk; use UserPromptSubmit.
- Workers must re-arm ScheduleWakeup every turn or they silently drop off (the old dormancy bug).
- The Adviser's note appears one turn later (next hook fire), not mid-action.
- The worker's test output used a throwaway stem; live files only persist when the hook fires for a real session.
