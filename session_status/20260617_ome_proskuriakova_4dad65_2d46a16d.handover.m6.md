# Scribe handover - milestone 6 (~90K tokens)
# session: 20260617_ome_proskuriakova_4dad65_2d46a16d
# cwd: C:\claude_base\.claude\worktrees\awesome-proskuriakova-4dad65
# written: 2026-06-17 13:16:23 by deepseek-v4-pro

# HANDOVER - Context Discipline Update for 1M Window

---

## GOAL (in Max's words)

Max wants to update autoloaded instructions to reduce "context overload scare" now that Opus has a 1M context window (5x larger than before). But he wants this done carefully:

- Back up the old strict context-saving rules into a **referenced but non-autoloaded file** so they can be restored when using smaller models (Fable).
- Relax the rules when running Opus (1M), but **keep them active** when running Fable.
- **Do NOT relax the death-spiral hook.** That's a different failure mode and remains fully active regardless of model.
- The harness compaction threshold (settings.json) should be **discretionary, depending on size** - not a single fixed jump.

---

## DECISIONS MADE + WHY

### 1. Model window ? harness compaction cliff
The model itself has 1M context. But the Claude Code **harness** auto-compacts at ~169K tokens (the gauge in Max's hook). This is the actual bottleneck - not the model window. Raising the *rules* alone won't reduce the 5 compactions he's seeing; the harness threshold is the real lever.

### 2. Death spiral stays untouched - PREVENT DESKTOP SUICIDE stays
Confirmed by Max explicitly: "death spiral is still very real. That should completely remain active." This is a thinking-block wall from tool-response bloat, not a context-size issue. 1M doesn't help it.

### 3. Split: what gets relaxed vs what stays
- **RELAX (Opus only):** Pure context-*size* discipline - "grep before read," "short subagent returns," "compact at milestones," fear-of-the-gauge.
- **KEEP FULL (all models):** PREVENT DESKTOP SUICIDE, the death-spiral hook.
- **BACKUP:** Old strict rules copied verbatim to a referenced, non-autoloaded file. Fable sessions point to it.

### 4. Harness threshold: discretionary, not fixed
Max's last word: "should be discretionary, depending on size." He was cut off but the intent is clear - no hardcoded jump to 600-800K. The threshold should scale with the model's actual window, decided per session or per model tier.

---

## CURRENT STATE

- **Research complete:** Confirmed 1M is default for Opus 4.8 (shipped May 28, 2026). The stale MODEL WARNING in CLAUDE.md that treated 1M as an anomaly needing loud alerts is now false-alarming.
- **Plan agreed, not executed:**
  - Relaxed context-discipline rules: **not yet written.**
  - Backup file: **not yet created.**
  - Harness compaction threshold in settings.json: **not yet adjusted.**
  - Death-spiral hook: confirmed kept as-is, **no edits needed.**
- **Open question answered:** Death spiral stays. Confirmed.

---

## EXACT NEXT STEP

1. **Create the backup file** - copy the three context-saving sections ("CONTEXT DISCIPLINE - GREP BEFORE READ", "PREVENT DESKTOP SUICIDE", death-spiral hook) into a non-autoloaded reference file (e.g., `C:\claude_base\context_discipline_backup_tomemex.md`).

2. **Edit global2 CLAUDE.md autoloaded instructions:**
   - **Keep:** PREVENT DESKTOP SUICIDE + death-spiral hook (unchanged, always active).
   - **Replace** the pure context-size discipline ("grep before read", "short subagent returns", "compact at milestones", gauge-fear) with a **model-conditional block:**
     - **If Opus (1M):** largely lifted - read whole files okay, longer subagent returns okay, don't fear the gauge; retain only cheap wins (worklog, don't inhale truly giant dumps, don't loop throwaway scripts).
     - **If Fable / small model:** full discipline restored - point to the backup file.

3. **Adjust harness compaction threshold** in `settings.json` - discretionary, scaling with model size. Not a single jump; a conditional or tiered approach (e.g., Opus ? ~600K+, Fable ? ~169K default).

4. **Fix the stale MODEL WARNING** in CLAUDE.md that false-alarms on 1M being active (since 1M is now standard for Opus 4.8).

---

## OPEN QUESTIONS

- **What exact threshold for Opus in settings.json?** Max said "discretionary" - needs a concrete number or formula. Suggested starting point: ~600-700K for Opus 1M, keeping the default ~169K for Fable.
- **What file path for the backup?** Suggested: `C:\claude_base\context_discipline_backup_tomemex.md` - awaiting Max's confirmation.
- **Should the model-conditional rule check model ID or context size?** Checking the model ID string (`opus` vs `fable`) is simpler and less fragile than reading a gauge.

---

## KEY PATHS / IDS

| What | Path/Value |
|---|---|
| Session cwd | `C:\claude_base\.claude\worktrees\awesome-proskuriakova-4dad65` |
| Global CLAUDE.md (autoloaded) | `C:\claude_base\CLAUDE.md` (global2) |
| Proposed backup file | `C:\claude_base\context_discipline_backup_tomemex.md` (not autoloaded) |
| Harness compaction threshold | `settings.json` - field for compaction cliff (~169K currently) |
| Current model | `claude-opus-4-8[1m]` - 1M context, default as of May 28, 2026 |
| Stale warning rule | MODEL WARNING section in CLAUDE.md (treats 1M as anomaly) |

---

## GOTCHAS / DEAD ENDS

- **Do NOT just relax the rules without touching settings.json** - the harness compacts at 169K regardless of model window. Edits to tone alone won't reduce compaction count.
- **Death spiral is not a context problem** - it's a tool-response-bloat problem. 1M doesn't fix it. Max was explicit: keep it fully active.
- **The stale MODEL WARNING** in CLAUDE.md fires loudly whenever 1M is active, but 1M is now standard for Opus. This is a separate fix from the context-discipline relaxation, but should be done in the same pass.
