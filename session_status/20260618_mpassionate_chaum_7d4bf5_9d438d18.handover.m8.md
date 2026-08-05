# Scribe handover - milestone 8 (~619K tokens)
# session: 20260618_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-18 17:03:18 by deepseek-v4-pro

# HANDOVER - D24 / sc10 Merge Production & Traceability

---

## GOAL (Max's words)

1. **sc10 multiperson lipsies**: Produce merged ~4-line lipsie clips for the sc10 scene, one lipsie per arrangement beat, with Anna and Ishtab talking in a two-shot. The lines must be labeled Left/Right with descriptions of both characters, formal officials atmosphere, eyes on each other, minimal nods/grins. Each prompt MUST include the spoken lines.

2. **Make every tab show all arrangements per scene at once** (since merged lipsies mean fewer items).

3. **Fix lipser UI**: Show actual dialogue lines in the lipser table, move comment boxes to the actions column.

4. **Fix lipser trim dialog**: Scrubbing the video makes audio go silent - must keep playing with sound.

5. **Timestamp comments + lipsie fire-time in DB** so any session can ask "comments for the last N fire-batches."

6. **Merge traceability + total propagation**: No hidden surgery. Every merge/rearrange must be declared, traced, and synced everywhere (audio, script_lines, Notion). Smaller audio gaps in merged audio.

---

## DECISIONS MADE + WHY

### sc10 lipsie production (D21 era)
- **arr01 (lines 0-3, greeting) approved as job 2774**: Formal-officials template, describe-both-characters-first (name + position before lines), Anna on LEFT, Ishtab on RIGHT. "Smiles" causes laughter/nods - removed. "Barely-moving" helps but isn't a silver bullet.
- **arr02-05 were fired** but many were on the wrong stills (static greeting two-shot for corridor/window beats). The scene has a developed path: hall ? corridor ? window ? alcove ? doorway. The right still per location matters.
- **The canonical merge path exists** (sass ? merges.json ? libup merge ? fire_merge_lipsie) but D21 bypassed it with ad-hoc throwaway scripts - that's the "hidden surgery" you hate.
- **The alcove/doorway stills** were extracted as frames from already-approved spine lipsies (clean Anna-L/Ishtab-R two-shots). This is the correct method when no standalone character two-shot exists.

### Scene picker (D22)
- Changed `arrangement_picker.js` from per-arrangement to per-scene filtering.
- **Later hotfixed** (D24) to dual-level: each scene has "ALL whole scene" + individual arrangements. Storyboard needs per-arrangement; clipper/lipser/imager want scene-wide.

### Lipser UI (D22)
- `runner_core.js` lipsie row now extracts quoted Left/Right lines from the prompt, shows them in the freed prompt cell. Comment boxes moved to the actions column.

### Trim audio fix (D22)
- `shared_ui/popup.js`: `_openTrim` now sets `vid.muted=false` explicitly; the START handle stopped force-pausing on scrub. Lipsie mp4s do carry aac audio (verified with ffprobe).

### Comments + fire-batch timestamps (D22)
- New column `jobs.commented_at` (added via Cloudflare D1 MCP, not the HTTP API which blocks ALTER). Stamped on every comment save in `combo_gui.py`.
- `batches.py` clusters lipsie `created_at` by 180s gap into batches. Usage: `python batches.py comments [N]` gives comments for the last N fire-batches.

### Merge traceability (D24)
- **`merge_ops` D1 table** + `merge_ops.py` helper: records every merge/rearrange with session, request verbatim, member line hashes, gap, and propagation checklist. `merge_ops.start()`, `.stamp()`, `.complete()`.
- **sass merge gap**: Added `MERGE_GAP_S` config (default 0.10s, via `production.json`) to the canonical merge-audio concat in `sass.py`. Format-matched silence so concat stays clean.
- **`fire_merge_lipsie.py` wired to `merge_ops`**: Optional `op_id` param - if passed, the fire stamps the ledger.
- **Corpse cleanup**: 36 errored sc10 lipsies junked. 43 null-arrangement orphans left unreviewed (not auto-junked - could be referenced).

### Rules saved to memory
- **HARD RULE #1 (top rank)**: Always merge+push to master BEFORE asking Max to verify (he sees only merged main branch).
- **No verbatim re-fires**: When Max asks for a variation of his prompt, don't fire his prompt verbatim again.
- **Don't block on polling**: Fire and let the detached worker render; stay responsive.

---

## CURRENT STATE

**4 of 5 merge-traceability pieces shipped to master:**

| Piece | Commit | Status |
|---|---|---|
| `merge_ops` ledger table + helper | `24a2be6` | Done |
| sass merge gap (0.10s) | `ed8d935` | Done |
| `fire_merge_lipsie.py` ? ledger wiring | `42bd0ff` | Done |
| Corpse cleanup (36 errored) | (included above) | Done |
| **Reverse Notion sync** | - | **NOT DONE** - irreversible Notion write, D24 left for Max |

**sc10 lipsies: arr01 (2774) approved. arr02-05 were fired but many on wrong stills.** The D21 ad-hoc merges (synthetic hashes, throwaway scripts) never declared in the script, never traced. To redo properly: declare `[[MERGE]]` blocks in the script ? sass merges audio ? libup collapses script_lines ? fire_merge_lipsie.py fires with `op_id`.

**Storyboard hotfix applied** (`fe7860a`): dual-level picker restores per-arrangement selection. Sb needs hard-refresh (no cache-buster on that include).

**Autonomous loop ended** by D24 - no safe work left unattended. The Notion sync is yours to drive.

---

## EXACT NEXT STEP

1. **Vet the sc10 lipser**: /lipser with scene "sc10" ? "ALL whole scene" - see which lipsies are keepers vs junk. The D21-fired arr02-05 clips may have wrong stills (static greeting room instead of corridor/window/alcove).

2. **Declare the proper `[[MERGE]]` blocks** in the sc10 script (Notion or the local script file). Decide the final merge groupings (which lines per beat). The canonical pipeline then takes over: sass ? libup ? fire_merge_lipsie.py (with `op_id` for tracing).

3. **Approve the reverse Notion sync spec** - D24 left it as "build dry-run first, show diff before any Notion write." The `merge_sync_traceability_spec_v01_tomemex.md` has the full design.

4. **Hard-refresh the storyboard tab** if not already done.

---

## OPEN QUESTIONS

- **Which lipsies from the D21 batch are keepers?** Many were fired; only arr01/2774 was explicitly approved. arr02-05 may be on wrong stills.
- **What are the final merge groupings for sc10?** Max wanted ~4 lines per lipsie. The rearrangement D21 did (shown in the transcript) needs vetting.
- **Notion sync design**: Dry-run preview first? Full rewrite of the script page's arrangement blocks, or only update `## ARRANGEMENT` blocks leaving raw dialogue alone?
- **The 43 null-arrangement orphans** in sc10 - should they be junked or re-assigned?

---

## KEY PATHS / IDs

- **MOMA root**: `C:\moma\sc10\combo_runner\code\`
- **Sound assembly**: `C:\moma\sc10\sound_assembly\code\sass.py`
- **Shared UI**: `C:\moma\sc10\shared_ui\popup.js`
- **Picker**: `C:\moma\sc10\combo_runner\code\arrangement_picker.js`
- **Merge ledger**: `C:\moma\sc10\combo_runner\code\merge_ops.py`
- **Batches helper**: `C:\moma\sc10\combo_runner\code\batches.py`
- **Canonical merge fire**: `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py`
- **Spec doc**: `C:\moma\sc10\combo_runner\code\merge_sync_traceability_spec_v01_tomemex.md`
- **Batches method doc**: `C:\moma\sc10\combo_runner\code\batches_method_v01_tomemex.md`
- **MOMA memory**: `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`
- **Scratch scripts**: `C:\moma\sc10\combo_runner\local_state\d21_scratch\` and `d24_scratch\`
- **Database**: Cloudflare D1, accessed via MCP tool `mcp__fee7c39e-4816-4a04-b41f-7067182da1c3__d1_database_query` or the local `moma_db.py` D1Client
- **Key two-shot stills**: `sc01_meet_twoshot_var01.png` (hall greeting, Anna-L/Ishtab-R), `sc05_window_twoshot.png` (window, Ishtab-L/Anna-R), `B1_corridor_walk_warm_v01.png` (corridor walk)
- **Approved arr01 lipsie**: job 2774 (`sc10_lipsie_v2774_wan26flau.mp4`)
- **UI ports**: combo_gui=8779, slideshow_server(storyboard/mixboard)=8790, prompter=8791

---

## GOTCHAS

- **wan2.6-i2v-flash ignores bare "Left/Right" labels** - must describe both characters by name + appearance + position first, THEN give the lines. "Smiles" triggers random laughter bursts and exaggerated nodding. "Barely-moving" and "listener frozen" help but aren't guarantees.
- **The storyboard has no cache-buster** on the arrangement_picker.js include - always needs a hard-refresh (Ctrl+Shift+R) when that file changes.
- **D1 HTTP API blocks ALTER TABLE** - schema changes must go through the Cloudflare D1 MCP tool.
- **Notion writes are flaky** - the existing rules say to snapshot/duplicate before any write and verify every write individually. This is why D24 didn't do it unattended.
- **The canonical merge path exists** - `sass.py MERGE pass` builds merged audio; `libup.py merge` collapses script_lines; `fire_merge_lipsie.py` fires. D21's ad-hoc merges (synthetic hashes in `_d21_build_arr01.py` etc.) bypassed this entirely - that's the "hidden surgery."
- **Merges are declared as `[[MERGE]]` blocks** in the script (sourced from Notion). Declaring them there propagates through the whole pipeline with full traceability.
- **MOMA's worker is a poll loop** (`combo_wan26au_worker.py`). Fire a job, then the worker renders it. If MOMA stack is down, a standalone worker can be started but the normal stack kills it on launch.
- **prompt_extend is OFF** on the wan26au worker - no auto-beautify of prompts.
