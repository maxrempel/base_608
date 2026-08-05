# Scribe handover - milestone 9 (~139K tokens)
# session: 20260611_admiring_mahavira_6f8fc6_923c6302
# cwd: C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6
# written: 2026-06-11 13:59:10 by claude-opus-4-8

# HANDOVER - Retroactivity Layer 1 (D16)

## GOAL (in Max's words)
"Plan and implement but make sure not to break." The task is the **Retroactivity** memo from Notion (Max first half-remembered it as "retractability/retraceability"). The core worry: MOMA changes constantly (~50 sessions), so by the time episodes 2-3 are done, episode 1 won't auto-assemble anymore - and worst case, the video exists but nobody can trace which clip came from which image/prompt/audio.

The memo's agreed fix has three layers plus one gap:
1. **Manifest** - every render writes one file freezing the full timeline + lineage per clip.
2. **Lockbox** - on approval, freeze a folder (manifest + final clips/audio + D1 snapshot + git tag), never edited.
3. **Swap, not re-run** - to change one word later, regenerate just that clip and swap it in.
- **The "oops forgot" gap:** trims and flips have no history - done by hand, baked into files, no record. Plan is to make trims/flips recorded data applied at render time.

Max's latest instruction: keep it terse ("tldr, dtalk, read only highlights"), the team is asleep, **merge/push is approved**, and a **live render is OK as long as nothing breaks**.

## DECISIONS + WHY
- **Start with Layer 1 (manifest) only** - it is pure insurance: it only reads what the render already computed and writes a new file. Cannot alter how video is made. Chosen first precisely because Max said "don't break."
- **Wrapped the manifest write so a failure can't kill the render** - if writing fails, the render still succeeds.
- **Committed/pushed to the branch, NOT master** - the branch team has a safety rule: announce file+line ranges on the bulletin board, no master push without D4's approval. D16 respected that and requested a merge window from D4.
- **This is now superseded by Max's last message:** team is sleeping, Max explicitly authorized the merge/push himself. So waiting on D4 is no longer required - Max gave the go directly.

## CURRENT STATE
- Layer 1 manifest writer is **built, syntax-checked, and unit-tested** with synthetic data: it writes valid JSON with full lineage, captures the git commit, and gracefully handles blank/no-job lines.
- Four edits were made to the render file: (1) carry full chosen-job lineage into each pick, (2) add the manifest-writer function after `concat_segments`, (3) call it in `main()` after the segments sidecar, wrapped in try/except, (4) bumped version header to **v07**.
- **Committed + pushed to branch only** (commit `0b4ba1d`). NOT on master yet.
- Status posted to bulletin board; milestone logged to durable work-log.
- Layers 2, 3, and the trims/flips gap are **not started**.

## EXACT NEXT STEP
1. **Merge the branch to master and push** - Max approved this directly (team asleep, his call). Branch: `claude/admiring-mahavira-6f8fc6`, commit `0b4ba1d`.
2. **Then run one live render** to produce a real manifest and confirm it looks right end-to-end - Max said live render is OK "if you don't break things."
3. Keep the report **tldr / dtalk / highlights only**.

## OPEN QUESTIONS
- None blocking. The earlier "live render now or hold for D4?" question was answered: merge, push, and live render are all approved.
- Layers 2/3 and trims/flips still await Max's go, one at a time - do not start unprompted.

## KEY PATHS / IDS
- cwd / worktree: `C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6`
- Render file edited: `sc10\sound_assembly\code\render_mixboard_video_v01.py` (now v07)
- Branch: `claude/admiring-mahavira-6f8fc6` - commit `0b4ba1d`
- Per-machine config (gitignored): `moma_data_root.txt` - lives at `sc10\combo_runner\code\moma_data_root.txt`. Worktree was missing it; copied from main repo.
- Bulletin board: `python C:/claude_base/branch_bulletin/bcast.py` (whoami / catchup / post). Identity: **D16**.
- Work-log: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- The manifest file is written **next to the rendered MP4**, named like `<output>.manifest.json`.

## GOTCHAS / DEAD ENDS
- The worktree does **not** have `moma_data_root.txt` (it's gitignored) - the module won't import without it. It was copied from the main repo into the worktree; confirm it's present before any render.
- `render_mixboard_video_v01.py` is the **hot file** D12/D13/D15 were all editing. Normally requires D4 merge approval - but team is asleep and Max authorized directly, so proceed, but be aware of potential merge conflicts when the team wakes.
- The manifest only **reads** the `picks` list (which already holds all lineage per line) and **writes** a new file. Do not let any "improvement" make it modify render behavior - that would violate the "don't break" constraint.
- Keep responses short. Max is mid-task ("finishing this arrangement") and wants highlights only.
