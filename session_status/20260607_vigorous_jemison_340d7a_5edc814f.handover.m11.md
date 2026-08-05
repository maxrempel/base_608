# Scribe handover - milestone 11 (~166K tokens)
# session: 20260607_vigorous_jemison_340d7a_5edc814f
# cwd: C:\claude_base\.claude\worktrees\vigorous-jemison-340d7a
# written: 2026-06-07 14:05:29 by claude-opus-4-5

# HANDOVER ? session vigorous-jemison-340d7a (2026-06-07)

---

## GOAL (in Max's own words)

Build a reliable, programmatic per-session oversight system that does NOT depend on the working "Opus" cooperating ? because "Opus ignores instructions."

Two watchers, both full Opus, both read the whole transcript, both run automatically every ~15 K tokens:

1. **Scribe** ? calm, neutral. Writes a rich handover so a cold session resumes exactly.
2. **Adviser** ? skeptical, protective. Catches trouble, speaks up into the chat (to Max AND to the Assistant), and is **reachable** (Max types `adviser: <question>`, Adviser answers).

Names locked: **Max** (user), **Assistant** (working model in the chat), **Adviser** (overseer). "Call them by name so all three know who's talking to whom."

---

## DECISIONS MADE + WHY

| Decision | Reason |
|----------|--------|
| Token-triggered dumps (~15 K), not turn-triggered | Dumps cluster near the 169 K compaction cliff ? the exact danger zone. |
| Two-layer design: Layer 1 mechanical breadcrumb, Layer 2 agent notes | If Opus ignores the nudge, you always have the guaranteed Layer 1 trace. |
| Detached/hidden subprocess launches the agents | Turn finishes instantly; no 40 s freeze waiting for Opus. |
| Editable personality files in `personalities/*.md` | Max can tune characters without touching code. |
| Adviser talks into the same chat (no separate window) | Simplest; the chat already has the context. |
| `adviser:` trigger for reachable Q&A | Clear signal that this line is for the Adviser, not the Assistant; baked into the trigger-capture logic. |

---

## CURRENT STATE

### DONE
- `session_status.py` ? hook, Layer 1 breadcrumb, launches oversight subprocess.
- `session_oversight.py` ? runs Scribe + Adviser, reads editable personality files, writes versioned handover/adviser files, logs errors, fails open.
- Personality files (`scribe.md`, `adviser.md`) ? editable text, not code.
- Operating manual (`the_watch_oversight_tomemex.md`) ? reading outputs, troubleshooting, cost, limits, disabling.
- All committed + pushed to master (`3d4ad028`, then one doc update).
- `global2.md` updated with "CONSCIOUS WORK-LOG" section (synced via Nextcloud).
- SKILL one-liner handed to b3 (not landed yet ? propose-only).

### IN FLIGHT (worker task)
- **Reachable Adviser** ? build was dispatched via `Agent` subagent just before this handover. Expected deliverable: the hook detects `adviser: ...` triggers, wakes the Adviser with the question + full transcript, and injects the labelled `ADVISER:` answer on the next turn.

### NOT STARTED (parked)
- **Inter-team channels** ? design agreed (per-team boards + addressed cross-team posts). Waiting for Max's go.
- **More-reliable work-log pieces** ? auto-read on entering a worktree; auto-capture right before compaction. Ideas only.
- **Sirius / Vega hook sync** ? the Watch hook lives in `~/.claude/settings.json`, which is not synced to other machines. Pine-only for now.

---

## EXACT NEXT STEP

Read the worker's completion notification for the "reachable Adviser" agent task, verify the new code:
1. Check that `session_status.py` now captures `adviser: ...` lines.
2. Check that it wakes `session_oversight.py` (or a new script) with the user's question.
3. Confirm the Adviser's answer lands as `ADVISER:` in the next turn.
4. Verify names (Max / Assistant / Adviser) appear in the adviser personality and in the injected text.
5. Do one live end-to-end test (ask `adviser: why the skeptical tone?` or similar) and confirm the reply.
6. Commit + push.

---

## OPEN QUESTIONS (for Max)

1. **Trigger-size decision** ? I set 15 K tokens; Max never explicitly confirmed or changed it.
2. **Inter-team channels** ? build now, or park?
3. **Sirius / Vega rollout** ? stay Pine-only or sync the hook?
4. **Em-dash bug** ? ASCII strip turns em-dashes into `?`. Fix, or leave?

---

## KEY PATHS / IDS

| Thing | Path / ID |
|-------|-----------|
| Hook entry point | `python C:/claude_base/compaction_kb/scripts/session_status.py --hook` (wired in `~/.claude/settings.json` UserPromptSubmit) |
| Oversight worker | `C:/claude_base/compaction_kb/scripts/session_oversight.py` |
| Personality files | `C:/claude_base/compaction_kb/personalities/scribe.md`, `adviser.md` |
| Status/handover output dir | `C:/claude_base/session_status/` |
| State (milestone tracking) | `C:/claude_base/session_status/.state/<sessionid>.json` |
| Operating manual | `C:/claude_base/compaction_kb/the_watch_oversight_tomemex.md` |
| bcast.py (team board) | `C:/claude_base/branch_bulletin/bcast.py` |
| worklog.py | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| Log | `C:/claude_base/session_status/oversight.log` |
| This session's transcript | `C:/Users/maxre/.claude/projects/C--claude-base--claude-worktrees-vigorous-jemison-340d7a/5edc814f-2a47-4c16-bc2c-c7ea422b2aa1.jsonl` |

---

## GOTCHAS / DEAD ENDS

- **no-cd rule** ? always invoke tools with forward-slash full paths from the worktree cwd; never `cd` into a directory before running. The identity hash keys off cwd.
- **Stop-hook danger** ? a Stop hook can only nudge via `decision=block`, forcing the session to continue (wedge risk). Always use UserPromptSubmit for advisory messages.
- **Suicide-prevention hook** ? blocks the third identical Bash command. Avoid triple-polling.
- **Self-wake gotcha** ? the forced 4-min timer is a MUST; workers that finish a turn without re-arming silently drop off forever.
- **ASCII strip** ? Unicode em-dashes become `?` in output files; harmless cosmetic bug.
- **Halt vs standby** ? standby keeps timers armed (stays reachable); halt stops everything. Use standby unless truly shutting down.
- **Two-team collision** ? fixed by c-prefix for compaction team vs b-prefix for kartoteka team, but the board still has no real channels. Don't reuse prefixes.
- **settings.json is Pine-only** ? hook changes don't propagate to Sirius/Vega.

---

End of handover.
