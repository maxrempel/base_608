# Scribe handover - milestone 10 (~759K tokens)
# session: 20260618_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-18 17:59:49 by deepseek-v4-pro

# HANDOVER: D24 - MOMA sc10 Production & Storyboard Pile Fix

---

## GOAL (Max's words)

1. **"produce a lipsie" for sc10 arrangements** - merged multiline lipsies (not per-line), 4 lines per clip where possible, using the formal-officials template (Anna-left/Ishtab-right, eyes on each other, minimal nods). Already produced for arr01-04 on the correct path locations (hall ? corridor/window ? alcove ? doorway) using frame-extracted two-shot stills where needed.

2. **"fix lipser to actually show the lines"** - show the actual dialogue text in the lipsie table, move comment boxes to the actions column. DONE.

3. **"make it possible to view all arrangements per scene at once"** - replace per-arrangement filter with per-scene filter. DONE (dual-level picker: "ALL whole scene" + individual arrangements).

4. **"fix lipsie trim dialog so scrubbing keeps audio playing"** - trim was going silent on seek. DONE (unmute in trim + don't force-pause on scrub).

5. **"comments must be timed"** - add `commented_at` to jobs, build `batches.py` so any session can query "comments for the last N fire-batches". DONE.

6. **"traceability and complete propagation from any point" - MERGE SYNC** - no hidden surgery. Every merge/rearrange must be tracked and sync through the whole pipeline (sass ? libup ? fire ? Notion). 4/5 pieces shipped; reverse-Notion-sync waits for Max.

7. **Storyboard pile: "only proper images - with two ladies, everything else should not be there"** - resolved approach: role-based filtering (shots vs plates), not filename filters. The system is in place; data retagging is in flight (D26).

---

## DECISIONS + WHY

### Merged multiline lipsies for sc10
- **Decision:** Produce one merged lipsie per ~4-line beat using the canonical `fire_merge_lipsie.py`, not ad-hoc per-line clips.
- **Why:** Max wanted fewer items, multiline clips. The previous D21 approach used throwaway scripts with synthetic hashes - this bypassed the canonical pipeline and created "hidden surgery" with no trace.

### Formal-officials template
- **Locked template:** "Left: red-haired woman says X. Right: elder woman says Y. Formal meeting of officials, eyes on each other, minimal nods, royal postures, minimal grins."
- **Why:** Through many iterations, this was the only prompt that didn't produce random nodding/penguin-bobbing or speaker-switching. "Smiles"/"warm" caused laughter bursts (wan2.6 limitation). Writing all dialogue text in quotes labeled Left/Right proved essential. For the alcove (where "Left/Right" labels were ignored), added a "describe both characters first" opening.

### Walking path locations
- **Decision:** arr01 (greeting, lines 0-3) on `sc01_meet_twoshot`, arr02 (hall, lines 4-9) also on meeting two-shot, arr03 (corridor/window, lines 10-21) on `sc05_window_twoshot`, arr04 (alcove/doorway, lines 22-29) on frame-extracted stills from approved spine lipsies.
- **Why:** The scene is already assembled along a path in the DB (per-line picks). Merger had to use the existing two-shot stills for each location. For alcove/doorway (no standalone two-shot), frames were pulled from the approved spine clips.

### Storyboard pile: role-based, not filters
- **Decision:** Filter pile by `role='shot'` (hide `role='plate'`). Remove all filename/content-based filters. The long-term fix is to tag backgrounds as `plate` at creation time.
- **Why:** Max was right - complex filename filters become monsters that break. The elegant solution uses the existing `role` metadata field. Plates (empty corridors, interiors, window views) get `role='plate'`; shots (Anna+Ishtab two-shots) get `role='shot'`. Future sessions: no junk enters the pile if the role is correct from the start.

### Cache saga
- **Root cause confirmed:** The storyboard (slideshow_server on :8790) serves inline JS in the HTML page - no `?v=mtime` cache-busting like combo_gui has. D23 added `Cache-Control: no-cache` headers but the server was never restarted, so old cached JS kept running.
- **Fix:** The permanent fix is to extract storyboard JS into an external file with `?v=mtime` (like combo_gui). NOT YET DONE - deferred.

### Merge traceability architecture
- **Decision:** Build a `merge_ops` D1 ledger table + `merge_ops.py` helper. Every merge/rearrange records intent at the start and stamps each propagation stage (audio_reassembled, script_lines_collapsed, lipsie_fired, notion_synced).
- **Why:** Max wanted "no hidden surgery" - any session must be able to trace what merges happened and where they propagated.

---

## CURRENT STATE

### Shipped (all on master):
| What | Commit | Status |
|---|---|---|
| Lipser shows dialogue lines, comments moved | `2ebba53` | ? DONE |
| Scene picker (dual-level: ALL + individual arrangements) | `0c9715b` + `fe7860a` | ? DONE |
| Trim dialog: audio stays on when scrubbing | `7fbbefe` | ? DONE |
| `batches.py` + `commented_at` column - comments by fire-batch | `4a62ec9` | ? DONE |
| `merge_ops` D1 table + `merge_ops.py` ledger | `24a2be6` | ? DONE |
| sass merge gap: configurable 0.10s default | `ed8d935` | ? DONE |
| `fire_merge_lipsie.py` wired to `merge_ops` ledger | `42bd0ff` | ? DONE |
| Corpse cleanup: 36 errored sc10 lipsies junked | - | ? DONE |
| HARD RULE #1 raised in MEMORY.md: "always merge+push before asking Max to verify" | - | ? DONE |
| Storyboard pile: **role-based filter (shot vs plate)** | `59a514c` | ? SHIPPED |
| Storyboard pile: filename filter removed | `12a2817` | ? DONE |
| Storyboard pile: reverted bad whitelist (`d75fbba`) | `aac4809` | ? DONE |

### In flight (delegated):
- **D26 retagging sc10 backgrounds `shot?plate`** - this makes the role filter actually clean the pile. Without it, 90 of 94 sc10 pile images show because they're tagged `shot` even though they're location plates.

### NOT YET DONE (deferred for Max):
- **Reverse Notion sync** - writing arrangement/merge structure back into the Notion script. Built as a dry-run first (preview + diff, no write). Not done unattended because Notion writes are irreversible and the hand-curated script is sensitive.
- **Extract storyboard JS to external `?v=mtime` file** - the permanent cache fix.
- **sc10 production D21** - the running autonomous session producing lipsies for sc10 arrangements. D21 is alive and has `batches.py` available for checking recent comments.

---

## EXACT NEXT STEP

**When Max returns:** Verify the storyboard pile is clean after D26's retag. Then decide on:

1. **Reverse Notion sync** - Max wanted total sync. The dry-run is safe to build unattended. The actual write needs Max's review.

2. **Permanent cache fix** - extract storyboard inline JS to external file with `?v=mtime`, matching combo_gui's pattern. This prevents ALL future cache disasters.

3. **Complete sc10 production** - D21 is running autonomously producing lipsies. Max can review/junk/approve per arrangement in the lipser.

---

## OPEN QUESTIONS

1. **Does the role-based pile filter show only two-shots after D26's retag?** - The system is in place; the data needs verification.

2. **Reverse Notion sync direction:** When D1 and Notion disagree, D1 wins (production structure becomes truth and is written INTO Notion). Is that the final word? And should it fully rewrite the script page structure or only update `## ARRANGEMENT ...` blocks?

3. **Storyboard JS extraction** - is this a priority now or after sc10 is complete?

4. **sc10 arr05 (lines 30-32, "here is the room")** - not yet produced. Needs a doorway/room two-shot still (or a frame from the approved spine clip).

---

## KEY PATHS / IDs / COMMANDS

**Files I own/edited:**
- `C:\moma\sc10\combo_runner\code\runner_core.js` - lipser table render (lines display + comment box move)
- `C:\moma\sc10\combo_runner\code\arrangement_picker.js` - dual-level scene+arrangement picker
- `C:\moma\sc10\shared_ui\popup.js` - trim dialog audio fix
- `C:\moma\sc10\combo_runner\code\merge_ops.py` - merge audit ledger helper
- `C:\moma\sc10\combo_runner\code\batches.py` - comments by fire-batch
- `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py` - wired to merge_ops
- `C:\moma\sc10\sound_assembly\code\sass.py` - MERGE_GAP_S (0.10s) in merge pass
- `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` - role-based pile filter (reverted filename filters removed)

**Memory files (Nextcloud-synced, NOT git):**
- `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` - HARD RULE #1 at top
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_always_push.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md`
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md`

**DB state:**
- D1 table `merge_ops` - new, columns: id, created_at, session, op, request, scene_id, arrangement_id, member_line_hashes, merge_hash, gap_s, propagation (JSON), error
- D1 table `jobs` - new column `commented_at` (TIMESTAMP, NULL for old comments)
- Sc10 arrangements: ids 2-7 (arr01-arr06), + arr6 created for broll pool

**Key approved stills for sc10 lipsies:**
- `sc01_meet_twoshot_var01.png` - Anna-L/Ishtab-R, greeting hall
- `sc05_window_twoshot.png` - Ishtab-L/Anna-R, window with Earth
- `B1_corridor_walk_warm_v01.png` - walking corridor
- Frame-extracted: `_d21frames/frame_alcove_*.png`, `_d21frames/frame_door_*.png`

**Key commands:**
- `python batches.py` - list recent fire-batches
- `python batches.py comments` - comments on last batch
- `python batches.py comments 3` - comments on last 3 batches
- `python C:/claude_base/branch_bulletin/bcast.py read` - check team board
- Storyboard: `http://localhost:8790/storyboard`
- Lipser: `http://localhost:8779/lipser`
- `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` - log to worklog

**Scratch directories:**
- `C:\moma\sc10\combo_runner\local_state\d21_scratch\` - D21 throwaway scripts
- `C:\moma\sc10\combo_runner\local_state\d22_scratch\` - D22 migration script
- `C:\moma\sc10\combo_runner\local_state\d24_scratch\` - D24 probe scripts

---

## GOTCHAS

1. **wan2.6-i2v-flash model quirks:** "smiles"/"warm" causes random laughter bursts. "Left/Right" labels alone are unreliable - describe both characters by appearance+position first, then give the quoted lines. Multi-turn 15-second clips invite random nodding; "barely-moving," "listener stays frozen" helps but doesn't eliminate it.

2. **Browser cache on storyboard:** The storyboard (port 8790) serves inline JS with no cache-busting. Firefox often runs stale cached JS even when Chrome shows the current version. **Hard-refresh (Ctrl+Shift+R) or clear site data** to see changes. The permanent fix (extract JS to external `?v=mtime` file) is not yet done.

3. **No-cache headers don't work reliably** - they're in the code (D23 added them) but the server was never restarted, and browsers/proxies often ignore them anyway.

4. **Ad-hoc merges by D21 bypassed the canonical pipeline** - synthetic hashes, throwaway scripts, no trace. This is the "hidden surgery" Max hated. The rule now is: all merges must be declared as `[[MERGE]]` blocks in the script ? sass ? libup ? fire, with `merge_ops` tracing every step.

5. **Notion writes are flaky and irreversible** - the script is hand-curated. Any Notion write must be preceded by a backup/snapshot and verified.

6. **Storyboard `getBinImages` now filters by `role='shot'`** - if images aren't showing, check their `role` in the DB. Plates (empty rooms, corridors, window views) should have `role='plate'`.

7. **The D21 running session** is producing sc10 lipsies autonomously. It has been taught `batches.py` and can check comments. Its merge approach is the old ad-hoc one - it should be migrated to the canonical pipeline for future arrangements.
