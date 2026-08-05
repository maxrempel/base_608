# Scribe handover - milestone 7 (~117K tokens)
# session: 20260617_ome_proskuriakova_4dad65_2d46a16d
# cwd: C:\claude_base\.claude\worktrees\awesome-proskuriakova-4dad65
# written: 2026-06-17 13:37:23 by deepseek-v4-pro

# HANDOVER - Relax Context-Saving Rules for Opus 1M + Raise Harness Threshold

---

## GOAL (Max's words)

"Save the backup of the context saving instructions in a referenced but not autoloaded file, and fix them with understanding that the context is 1M - 5-fold higher. ... If we are using Opus, we largely lift them; if Fable, we largely keep them. Death spiral is still very real - that should completely remain active." Followed by: "yes raise autocontext thing."

In short: **relax the extreme context-hoarding rules now that Opus has 1M (the defaults are 5x larger), but keep the death-spiral guard intact, and raise the harness's auto-compaction ceiling so sessions don't keep getting cut at the old ~169K boundary.**

---

## DECISIONS MADE + WHY

### 1. Confirmed: 1M is default for Opus 4.8 (no beta, no header)
- Timeline: Opus 4.6 got 1M beta Feb 2026 ? general availability Mar 2026 ? Opus 4.8 shipped May 2026 with 1M on by default.
- The old MODEL WARNING rule in CLAUDE.md that treats 1M as an anomaly is now stale.

### 2. The compaction cliff (~169K) is NOT the model window - it's the Claude Code harness
- The model has 1M, but the harness auto-compacts at ~169K regardless. Relaxing rule *tone* alone won't reduce compaction count. The settings.json threshold needs raising too. This is the actual lever for "5x more room."

### 3. Death spiral != context exhaustion
- Death spiral is a thinking-block wall from tool-call bloat, not a context-size problem. 1M does not mitigate it. Therefore: **death-spiral hook stays 100% active, untouched, across all models.** Not relaxed, not moved.

### 4. Split the old strict rules into two categories

| Section | Action | Why |
|---|---|---|
| **CONTEXT DISCIPLINE** (grep before read, short subagent returns, compact at milestones, fear-the-gauge) | **Relaxed for Opus** - now discretionary by file size + model-conditional | 1M makes hoarding pointless; but Fable/small-model users need the old rules back |
| **PREVENT DESKTOP SUICIDE** + death-spiral hook | **Death-spiral hook: UNTOUCHED. Suicide section: softened to calm hygiene** | Death spiral is a different failure mode. Suicide warnings were alarmist and deaths aren't being observed lately |

### 5. "Grep before read" ? discretionary by file size (Opus only)
- On Opus 1M: read normal files whole, reach for grep-first only when a file is genuinely large. On Fable/small model: full strict version restored from backup.

### 6. Backup file location chosen
- `C:\claude_base\context_discipline_backup_tomemex.md` - referenced, NOT autoloaded. Contains the verbatim strict versions for when Fable or a small model is in use.

---

## CURRENT STATE - WHAT IS DONE

### Files modified

1. **`C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`** (live, autoloaded instructions):
   - **CONTEXT DISCIPLINE** section: rewritten with model-conditional logic. Opus ? discretionary/size-based. Fable ? back to strict. Kept only cheap habits (don't inhale giant dumps, don't loop throwaway scripts, moderate subagent returns).
   - **PREVENT DESKTOP SUICIDE** ? renamed to **SESSION HYGIENE - LIGHT**. Calm, plain-habit framing. Three habits: don't read huge files, be moderate with web searches (spin a branch/agent for heavy research), don't loop deterministic failures. The `block_death_spiral.py` hook stays wired and noted.
   - One stale cross-reference was fixed.

2. **`C:\claude_base\context_discipline_backup_tomemex.md`** (new, not autoloaded):
   - Contains strict verbatim versions of both sections - CONTEXT DISCIPLINE (original grep-before-read, compact-at-milestones, fear-the-gauge) and the old PREVENT DESKTOP SUICIDE/death-spiral text.
   - Preserved so Fable or any future small-model Claude can reinstate them.

3. **Worklog** was updated via the Python script at `C:/claude_base/compaction_kb/scripts/worklog.py`.

---

## EXACT NEXT STEP (NOT YET DONE)

**Raise the harness auto-compaction threshold in settings.json from ~169K toward ~600-800K.**

This is what Max's final "yes raise autocontext thing" refers to. The Claude Code harness (not the model window) is what triggers compactions - it's set at ~169K and that number has not been touched yet. Without this change, sessions will keep hitting 5+ compactions regardless of the doc edits.

The settings.json location was not read during the session, so the exact path and key name need to be located (likely under the Claude Code config directory). The assistant previously suggested a target of ~600-800K but Max did not pick a specific number - that's still an open question.

---

## OPEN QUESTIONS

1. **Exact compaction threshold number**: 600K? 800K? Some other fraction of the 1M window? Max hasn't specified. The assistant offered ~600-800K as a range.
2. **settings.json path**: Not yet confirmed in this session. Likely somewhere under the Claude Code config tree.
3. **Should the stale MODEL WARNING rule** (the one that screams when 1M is active) also be updated? The assistant offered to do it earlier but Max focused on the context-discipline sections instead. This is still stale and will false-alarm in future sessions.
4. **Fable conditions**: How will the session know it's running on Fable vs. Opus? The model-conditional language assumes the session can detect its own model ID, but the exact mechanism wasn't discussed.

---

## KEY PATHS / IDS

| What | Path |
|---|---|
| **Live autoloaded rules** | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| **Strict-rules backup** (not autoloaded) | `C:\claude_base\context_discipline_backup_tomemex.md` |
| **Worklog script** | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| **Death spiral hook** | `block_death_spiral.py` (wired in global2 but path not read in session) |
| **Harness compaction settings** | ~settings.json under Claude Code config - NOT YET READ |
| **Session model ID** | `claude-opus-4-8[1m]` |

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **Do not touch the death-spiral hook.** Max was unequivocal: "wait death spiral is still very real. That should completely remain active." 1M does not help with death spiral. The hook in global2 stays exactly as-is.

2. **The backup file must NOT be autoloaded.** It's a cold-storage reference for when Fable is in use. If `context_discipline_backup_tomemex.md` somehow gets autoloaded, it would re-impose the strict rules.

3. **Doc edits alone won't reduce compactions.** The harness threshold in settings.json is the real lever. If the next session edits only docs without touching that number, compactions will continue at the same rate. The assistant flagged this clearly and Max agreed with the last prompt.

4. **"grep before read" is now conditional, not abolished.** On Opus, it's discretionary for large files. On Fable, it's back to strict. The backup file preserves the verbatim original so there's no loss.

5. **The cross-reference in the relaxed CONTEXT DISCIPLINE section was fixed** (it pointed to the old section name - now corrected to point to SESSION HYGIENE - LIGHT).
