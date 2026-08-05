# Scribe handover - milestone 4 (~344K tokens)
# session: 20260617_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-17 23:11:19 by deepseek-v4-pro

# HANDOVER - D22: Fix lipser to show dialogue lines

## GOAL (Max's words, verbatim)

"Fix lipser to actually show the lines. There is a lot of useless things there. If you can, move comment boxes to the right to the column with buttons. This frees up space to place actual text lines."

## WHAT THIS MEANS

The `/lipser` page on MOMA's UI (served from `localhost:8779`) displays rendered wan26flau lipsie clips for review. Right now it shows the video player and some comment boxes, but does **not** show the spoken dialogue lines (the actual text of what's being said in each clip). Max wants:

1. **Show the actual lines** - each clip's dialogue text displayed on the page.
2. **Clean up useless elements** - remove things that don't belong.
3. **Move comment boxes to the right column** (where the action buttons live) to free up the main area for the text lines.

## DECISIONS MADE IN D21 (background, not the current task)

- The approved prompt template for sc10 lipsies: formal officials, eyes on each other (profile, not camera), minimal nods/grins, royal posture, lines in quotation marks labeled by speaker.
- For position labeling: bare "Left:" / "Right:" prefixes confuse wan2.6. The fix is to **describe both characters and their positions first** ("On the left: a young woman with long red hair... On the right: an older woman with long dark hair, red robes, jade beads..."), then give the quoted lines.
- The scene sc10 was rebuilt into ~4-line merged multiline lipsies (12 chunks covering 33 lines) using location-appropriate two-shots traced from the spine.
- Job 2774 (arr01, greeting lines 0-3) is fully approved. Everything else is rendered but still under review.

## CURRENT STATE

**Branch:** `compassionate-chaum-7d4bf5` (a worktree under `C:\moma\.claude\worktrees\`)
**Session register:** D22 (was D21; task changed)
**MOMA stack:** Running at `localhost:8779` (combo_gui + wan26au worker)
**Database:** D1 (SQLite), via `moma_db.py` ? `D1Client`

**Lipser entry point:** `http://localhost:8779/lipser?ids=...&title=...`
The lipser page likely lives in the combo_gui codebase under `C:\moma\sc10\combo_runner\code\`.

**Where the dialogue lines live in the DB:**
- `script_lines` table has the text per line (`line_id`, `line_text`, `speaker`, `arrangement_id`).
- Jobs have `prompt` and `custom_metadata` columns that may hold the spoken lines.
- The audio resolver (`audio_resolver.py`) maps line hashes to MP3 files.
- The merged fire scripts (e.g., `_d21_arr234.py`, `_d21_fire_v9.py`) prove the lines are accessible per job via `line_text` queries.

## EXACT NEXT STEP

1. **Find the lipser code** - most likely in `combo_gui.py` or a template/HTML file served by it. Grep for `"/lipser"`, `"lipser"`, or `"def lipser"` in `C:\moma\sc10\combo_runner\code\`.
2. **Read the current page structure** - understand how comment boxes, buttons, and the video player are laid out.
3. **Query how to get lines per job** - `script_lines` joined with `job_lines` or `arrangement_lines` to map job IDs ? line text + speaker.
4. **Remove useless elements**, move comment boxes to the right column, add a text area for the dialogue lines in the freed main space.
5. **Test** by viewing any existing lipsie URL (e.g., `/lipser?ids=2774`).

## OPEN QUESTIONS

- What exactly is "useless" on the lipser page? Max will need to point at it, or you read the code and spot cruft.
- Does "move comment boxes to the right" mean CSS flex/grid repositioning, or physically relocating the HTML elements?
- Should the lines be displayed as raw text, or formatted with speaker labels (like the prompt format)?

## KEY PATHS

- **Worktree:** `C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5`
- **MOMA code:** `C:\moma\sc10\combo_runner\code\`
- **Main GUI server:** `combo_gui.py` (likely) - serves lipser at port 8779
- **DB client:** `moma_db.py` ? `D1Client` with `query_sql(sql)` method
- **MOMA stack launcher:** `C:\moma\sc10\start_moma.bat`
- **Worklog script:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"`
- **Memory files:** `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` (has rules like "no verbatim re-fires", "don't block on polls")
- **Approved arr01 lipsie:** job 2774 (`sc01_meet_twoshot_var01.png` still)

## GOTCHAS

- **Don't block on polls** - this was saved as a rule. Fire and move on; the detached worker renders in the background.
- **Don't re-fire the user's prompt verbatim** - another saved rule. If they share a prompt, they've already fired it; only fire variations.
- **Left/Right labels fail wan2.6** - describe characters by appearance + position instead.
- **The 15s clip cap** forces some long monologue lines (e.g., line 8 at 14s, line 23 at 13s) to be single-line lipsies; they physically can't take neighbors.
- **The MOMA stack (combo_gui + worker) must be running** for the lipser page to serve and for jobs to render. If port 8779 is down, run `C:\moma\sc10\start_moma.bat`.
- **This is a different worktree** - main checkout may have different code; work in `C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5`.
