# Scribe handover - milestone 10 (~801K tokens)
# session: 20260619_cranky_noether_5d066f_63a837ee
# cwd: C:\moma\.claude\worktrees\cranky-noether-5d066f
# written: 2026-06-19 15:05:26 by deepseek-v4-pro

## Handover: D24 ? next session (MOMA storyboard / sc10)

### GOAL (Max's words)
Max wants **elegance and reliability**, not fragile filters. He said:  
*"Idea of complex filters is idiotic long run, they break and break everything. Simple thing is not a monster."*  
*"I only need proper images - with two ladies, everything else should not be there."*  
*"Better fix tags than tons of stupid filters that confuse future sessions."*

Currently he is reviewing the storyboard after a series of fixes, and the last message was *"Let me check"*.

### DECISIONS + WHY

**1. Storyboard pile (which images show in the image grid)**
- The pile now uses **three gating criteria only**: `status`, `role`, and a simple arrangement filter.
- `role='shot'` items are shown; `role='plate'` items (backgrounds) are hidden. No filename?based blacklist / whitelist. Reason: filename?based filters break, hide real two?shot images, and create "monsters". The plate/shot distinction is metadata, not heuristics.
- A rogue "scene?only" filter added by a retired session (D23) was **reverted** (v55). It hid every `arrangement_id=None` image, which lost most of Max's sc10 pictures. The filter code was **completely removed** (v56) and a HARD RULE added to `MOMA/MEMORY.md` forbidding any future "smart" pile filters. The only arrangement gating left: when a specific arrangement is picked, show only that arrangement; when "ALL scene" is picked, show everything (no arrangement restriction, `arrOk` passes all).
- Background plates were bulk?retagged from `role='shot'` to `role='plate'` (59 images) based on filename patterns (`bg_*`, `extrap*`, `iter_bg`, station, etc.). A full backup was saved: `sc10_role_backup_20260618_180040.json`. An over?catch (images 930?932) was immediately restored. The pile now shows **~31 genuine two?shot shots**.
- **Important:** D22 (the data?lane session) also performed a parallel retag of 78 images into arrangement 6; that retag was *not* reverted when the scene?only filter was removed, so some images may now have duplicate rows or tags. This has not yet been fully consolidated - see Open Questions.

**2. Missing two?shot images ("~2x more at least that are lost")**
- Max believes many more Anna+Ishtab two?shots exist but don't appear in the pile.
- A full inventory was done: by filename, by prompt, and by tracing the actual stills used in the lipsie spine. The conclusion: essentially every real sc10 two?shot **still** is already visible. The pile does contain all known shots.
- The remaining candidates that could be "lost" are:
  - The **~20 animated clips** (`.mp4` files stored as `job_type='image'`) - these are the moving walk/window/room takes. They *do* show in the pile when the role filter passes them, but they show as video thumbnails.
  - **Junked/unapproved versions** of existing two?shot stills - by design not in the pile.
  - Possibly some images tagged to the **wrong scene's arrangement** (e.g., `arr=1` which is sc09's arrangement). Only one candidate pair (J2707/2708) was found, but visual inspection showed they are **Anna+Driver from sc09**, not sc10.
- **Bottom line:** the data side says the pile is complete. If Max still sees missing images, he needs to provide an example or the session should ask him to point at a specific image he remembers, then trace it by ID.

**3. 2nd spine (alternate takes lane)**
- Made **three?state expandable** (compact / medium / wide ~4?) with the label `2ND SPINE [+]` / `[++]` / `[+++]`. Works.
- The label now always renders (v59), even when there are no alternate takes, so Max can click to expand the lane area at will.
- **Junked takes are NOT shown** in the 2nd spine (v58 reverted v57). Max explicitly: *"Junk doesn't belong there."*
- A **drop handler** was added (v60) so dragging a clip from the 1st spine onto the 2nd spine un?pins it (demotes the pick), instead of causing a Windows file?open popup. Reason: pre?existing bug - the lane had no drop handler and the browser misinterpreted the drag data as a file path.

**4. Merge traceability & total sync**
- A proper audit ledger (`merge_ops` table in D1, `merge_ops.py`) was built. Every merge/rearrange can be recorded with the command, session, propagation stages (sass?libup?lipsie?Notion).
- The sass MERGE pass now inserts a configurable gap (`MERGE_GAP_S`, default 0.10s) between concatenated member MP3s, configurable in `production.json`.
- The canonical merge?fire script (`fire_merge_lipsie.py`) can optionally accept an `op_id` and stamp the ledger.
- **Reverse Notion sync** (writing `[[MERGE]]` blocks back into the Notion script page) is **NOT DONE**. It is gated: irreversible, requires Max's explicit go?ahead. The code is written but dry?run only; DO NOT execute it unattended.

**5. UI improvements shipped**
- Lipser now **shows actual dialogue lines** in the prompt cell and **moves comment boxes** to the actions column.
- The **scene/arrangement picker** is dual?level (ALL scene or per?arrangement) and is shared across all tabs.
- Trim dialog video **retains audio when scrubbing**.
- A **`batches.py` helper** allows pulling Max's comments by fire?batch (clusters `created_at` by 180s gap). The DB column `commented_at` was added and all comment?save endpoints stamp it.

### CURRENT STATE

- **Storyboard:** pile shows ~31 sc10 two?shot shots, no backgrounds, no scene?narrowing regression. 2nd spine expandable, drop handler fixed, junk absent.
- **Lipser/clipper/imager:** all functional, scene picker works.
- **Merge pipeline:** ledger ready, sass gap tuned, fire tracing wired. No merges have been created through the new pipeline yet - the existing sc10 merges are D21's ad?hoc ones from earlier (untraced).
- **Notion:** untouched; reverse?sync pending.
- **Lost two?shots investigation:** closed on the data side (pile correct), but Max may disagree. The session should ask him if he still sees a discrepancy.
- **Database:** `jobs.commented_at` exists, `merge_ops` table exists, `sc10_role_backup_20260618_180040.json` in `d24_scratch/`. D22's own retag backup also exists separately (`sc10_pile_tags_backup_20260618_164336.json`).
- **All code changes are pushed to master.**

### EXACT NEXT STEP
**Wait for Max.** He said "Let me check" after the 2nd?spine and drop?handler fixes. When he returns:
- Ask if the storyboard looks good now (pile, 2nd spine).
- If he still says images are missing, **do not mutate data blindly.** Ask him to show you an example (a job ID or a filename he remembers), then trace it through D1 and the disk. The pile is data?complete according to the DB, so a discrepancy means either he remembers an unapproved/junked variant or a renamed file.
- If he's happy, he may then want to move on to the reverse?Notion sync, or to finalize the merged lipsie arrangements (arr02+), or to something entirely new.

### OPEN QUESTIONS (await Max)
1. **Lost two?shots:** Max still felt ~2? more good images were hidden. Data says they're all there. Need his direct example or confirmation that the pile is now sufficient.
2. **D22's parallel retag:** D22 tagged 78 images into arrangement 6 while the scene?only filter was active. After the filter revert, those tags may cause double?counting or odd arrangement assignments. Should they be reverted/consolidated?
3. **Reverse Notion sync:** When to activate? Max must decide after reviewing the dry?run diff.
4. **Merged lipsies for sc10:** It appears only arr01 (job 2774) is approved; other arrangements still need proper location?aware merged lipsies. D21 may resume that.

### KEY FILE PATHS & IDs
- Storyboard editor: `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (version v60, commit 6dce775)
- Pile filter logic: `getBinImages` (filter on `role`, `status`, arrangement)
- Role retag backup: `C:\moma\sc10\combo_runner\local_state\d24_scratch\sc10_role_backup_20260618_180040.json`
- D22's backup: `C:\moma\sc10\combo_runner\code\_d2x_scratch_archive\sc10_pile_tags_backup_20260618_164336.json`
- Merge ops ledger: `C:\moma\sc10\combo_runner\code\merge_ops.py`
- Sass merge gap: `C:\moma\sc10\sound_assembly\code\sass.py` (config `merge_gap_s`)
- Notion sync (pending): code in `merge_ops.py` but dry?run only
- Database: Cloudflare D1 (uuid cd12626c-3697-4dfe-a52b-0a22abd9d8e2), admin MCP for DDL
- Important job IDs:
  - 2774 (approved arr01 merged lipsie)
  - 887, 889, 925 (blank?thumb fixes)
  - 440, 650, 884, 885, 889 (stragglers correctly kept as shots)
  - 783?942 (background plates correctly tagged)
- MOMA memory: `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` (contains HARD RULES about push?before?verify and no smart pile filters)

### GOTCHAS
1. **Never add junk to the 2nd spine.** Max was very clear.
2. **Never invent "smart" pile filters.** The rule is burned into MEMORY.md. Any future pile filtering must only use `role='shot'` and arrangement selection. If junk is visible, junk it once (junk persists) - do not filter by filename, prompt, or heuristics.
3. **Browser caching on storyboard:** slideshow_server (port 8790) has no?cache headers in code but the server was never restarted, so caching can still occur. Hard?refresh (Ctrl+Shift+R) is often required. The bulletproof fix (external JS with `?v=mtime`) has not been done. If Max says "the storyboard didn't change," suspect cache first.
4. **Reverse?Notion?sync is gated.** Do not run it unattended or without Max's explicit go?ahead. It writes to his hand?curated Notion script.
5. **Many sessions have touched the storyboard file.** Always check `bcast` board and pull before editing. D26 currently owns the spine UX features.
6. **Role field is reliable now** for pile gating. Do not add more columns or flags without Max's approval; simplicity is the mandate.
