# Scribe handover - milestone 5 (~375K tokens)
# session: 20260617_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-17 23:36:34 by deepseek-v4-pro

# HANDOVER - MOMA D22 ? Next Session

## GOAL (Max's words)
"next, in moma, every tab, make it possible to view all arrangmenets per scene at once. Since we now make lipsies by arrangment, we have much fewer items, so need to see all at one sceen. You can simply replace the filter by arrangment by the filter by scene. in every tab."

Translation: MOMA currently filters by arrangement within a scene. Now that lipsies are merged per-arrangement (fewer items), the user wants to see ALL arrangements for a scene together on one screen. The UI change: swap the "arrangement" filter dropdown for a "scene" filter dropdown - in every tab.

## WHAT ALREADY HAPPENED (D21 + D22)

### D21 - sc10 rebuilt as merged multiline lipsies
The entire sc10 (33 lines, Anna?Ishtab two-hander) was rebuilt as ~4-line merged lipsies per beat, location-respecting. Key outcomes:

- **Approved template** (from arr01, job 2774): "formal meeting of officials, eyes on each other, minimal nods/grins" + lines quoted and attributed with character descriptions.
- **Speaker-switching fix discovered**: bare "Left:" / "Right:" labels confuse wan2.6. Instead, describe both characters by name+appearance+position FIRST, then give the lines. Example: *"On the left: a young woman with long red hair, white cloak - Anna. On the right: an older woman with long dark hair, red robes, jade beads - Ishtab. Anna says: '...' Ishtab says: '...'"*
- **Prompt requirements** (Max's rules): every prompt MUST include actual lines. Quotation marks help. No smiles/warm/emotion adjectives (they cause laughter). "Barely-moving" / "calm" for stillness. The "listener frozen" clause unreliable; better to keep minimal movement language.
- **Location tracing** (from spine lipsies?clips?stills): greeting hall (lines 0-9), corridor/window (10-23), alcove (24-27), doorway/room (28-32). For alcove/door where no standalone two-shot existed, mid-frames were extracted from approved spine lipsies as the wan26flau input still.
- **12 chunks rendered**, all done: 2774(arr01 ?approved), 2775-2778(hall), 2785-2786+2791-2792(window), 2793(alcove, later refired as 2796), 2794-2795(door). The window beat has Ishtab-Left/Anna-Right (the still is flipped); all others are Anna-Left/Ishtab-Right.
- **15s clip cap** forced some single-line orphans where monologues are long (line 8: 14s, line 23: 13s - can't take neighbors). Three orphan singles remain by necessity.

### D22 - lipser UI fix
Branch off D21. Changes to `runner_core.js` in the lipser table row:
- **Dialogue lines now shown** in the prompt cell - parses the quoted Left/Right lines from the prompt, skipping staging boilerplate. Single-line lipsies show their line.
- **Comment 1 & 2 boxes moved** into the actions (buttons) column, freeing the prompt cell for text display.
- Committed as `2ebba53`, pushed to master. Cache-busted by mtime. Just needs browser refresh.

Max said "great, thanks" - the lipser change is done and approved.

## CURRENT STATE

- **D21 sc10 lipsies**: All 12 chunks rendered and ready for review at `/lipser?ids=2774,2775,2776,2777,2778,2785,2786,2791,2792,2793,2794,2795`. 2793 has a speaker-swap issue (known - refired as 2796 with the describe-both-first method, needs confirmation it fixed it).
- **D22 lipser UI**: Merged to master, done.
- **New task (NOT STARTED)**: Replace arrangement filter with scene filter across all MOMA tabs. No code has been touched for this yet.

## EXACT NEXT STEP

1. **Find all MOMA UI tabs** that have an arrangement filter dropdown. The main render pipeline is in `runner_core.js` and `runner_page.html`. There's also `combo_gui.py` (the Flask server). Read these to find every tab/page where arrangement filtering happens.

2. **Identify the filtering logic**: Each tab likely has a dropdown that sends an `arrangement_id` parameter to limit results. The change is to make it filter by `scene_id` instead - showing all arrangements within the selected scene rather than one arrangement.

3. **Implement the replacement** in each tab:
   - Change the dropdown from listing arrangements to listing scenes.
   - Update the filtering query/server-side endpoint to accept scene_id and return all arrangements under it.
   - Verify the "/lipser" tab, the main combo runner tab, and any review/approve tabs.

4. **Test**: Pick a scene with multiple arrangements, confirm all its lipsies appear together on one screen.

## KEY FILE PATHS

| Path | Role |
|---|---|
| `C:\moma\sc10\combo_runner\code\runner_core.js` | Main UI JS - lipser table render, the file just edited for D22 |
| `C:\moma\sc10\combo_runner\code\runner_page.html` | Main HTML template - tab structure, dropdowns |
| `C:\moma\sc10\combo_runner\code\combo_gui.py` | Flask server - routes, data endpoints, asset cache-busting |
| `C:\moma\sc10\combo_runner\code\moma_db.py` | D1Client - database queries |
| `C:\moma\sc10\combo_runner\code\_d21_*.py` | D21 helper scripts (fire, merge, probe, audit) - reference only |
| `C:\moma\sc10\combo_runner\data\` | Worker PID, rendering logs, output stills |
| `C:\Users\maxre\.claude\projects\C--moma\memory\project_production_process.md` | Production rules |
| `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md` | Rule: don't re-fire user's exact prompt verbatim |
| `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md` | Rule: fire jobs detached, don't block on poll |

## GOTCHAS & DEAD ENDS

- **wan2.6 speaker-switching**: The model ignores bare "Left:" / "Right:" labels. Fix: open with full character description (name + appearance + position), then attribute lines by name. This is now the proven pattern (job 2796 test).
- **"Smiles" / emotion words**: In wan26flau prompts, "smiles", "warm", "gentle smiles" cause random bursts of laughter and ham acting. Keep language minimal and formal.
- **15s clip cap**: Audio length drives chunk boundaries. Long monologues (line 8 at 14s, line 23 at 13s) must be single-line lipsies - cannot merge with neighbors.
- **Two per-line rendered clips per beat**: The spine has BEEN assembled (per-line clips exist), merger just needs the right still per chunk. Frames can be extracted from existing approved clips when no standalone two-shot exists.
- **Window beat speaker flip**: The `sc05_window_twoshot.png` still has Ishtab on LEFT, Anna on RIGHT - opposite of the greeting/corridor stills. Prompts must reflect this.
- **Do NOT block on poll**: Fire lipsie jobs and let the detached wan26au worker render them. Check back with scheduled wakeups or on request.
- **MOMA startup**: `C:\moma\sc10\start_moma.bat` - starts the combo_gui server on port 8779 AND the wan26au worker. The worker runs as a poll loop picking up queued jobs.
- **Cache-busting**: JS assets are cached by `?v=__ASSETVER__` (mtime-based), so file edits take effect on browser refresh (the watcher auto-restarts Flask).

## OPEN QUESTIONS

None from Max. The task is clear: swap arrangement filter ? scene filter in every MOMA tab. Just do it.
