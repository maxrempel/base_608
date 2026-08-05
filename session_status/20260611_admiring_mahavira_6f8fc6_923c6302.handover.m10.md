# Scribe handover - milestone 10 (~159K tokens)
# session: 20260611_admiring_mahavira_6f8fc6_923c6302
# cwd: C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6
# written: 2026-06-11 16:00:20 by claude-opus-4-8

# HANDOVER - Retroactivity / Lineage Manifest Work

## GOAL (in Max's words)
"The whole point [is] to have full retroactivity, not fucking imitation of it."

Max wants MOMA episode 1 to stay **fully traceable and re-buildable forever**, even as the system drifts over ~50 sessions. The driving fear (from his "Retroactivity" Notion memo): a video will exist but nobody will be able to trace which clip came from which image/prompt/audio - and worse, the hand-done **trims and flips** have no record at all.

He explicitly does NOT want a half-measure that only records *which clip / what order* (the trivial assembly layer). He wants each clip to be **self-describing enough to remake** - the full recipe, including the manual edits.

His last message is frustration: he expected the work **done**, and instead got asked permission to start the real part. Do not ask to begin the recipe work - he's already told you it's the whole point. Just do it (carefully).

## DECISIONS + WHY
- **Manifest writer is purely additive** - chosen first because Max said "make sure not to break." It only reads what the render already computed and writes a new companion file; if the write fails, the render still succeeds. This is layer 1 of the 3-layer plan (manifest ? lockbox ? swap-not-rerun).
- **Render is the hook point** - because render is the one moment the whole final timeline is assembled in order with chosen clips + audio. Before render the data is scattered; after, it's gone.
- **BUT Max corrected the priority**: the assembly (which clip, what order) is trivial. The **valuable, fragile part is each clip's recipe** - prompt text, mood codes, parameters, source-image chain, flip, trim - and that does NOT require render to capture.
- **Merge gate waived**: team (D12/D13/D15 editing same hot files, gated by D4) is asleep since yesterday; Max explicitly authorized merging to master and a live render "if you don't break things."

## CURRENT STATE
**Layer 1 (assembly manifest) is BUILT, MERGED to master, and VERIFIED - but it's the trivial half and has a proven gap.**

- Edited `render_mixboard_video_v01.py` ? bumped to **v07**. Added: full chosen-job lineage carried into each pick, a manifest-writer function, and a wrapped call in `main()` (after the segments sidecar) that can never break the render.
- Syntax-checked, unit-tested with synthetic data, then **live-rendered scene 9** (12 lines) to a temp path - real `.manifest.json` written next to a throwaway MP4, then deleted. Max's rehearsals folder untouched.
- Committed `0b4ba1d`, pushed to branch `claude/admiring-mahavira-6f8fc6`, then fast-forward merged to **master** (`f9693ce..0b4ba1d`). Clean, zero clobber.
- **THE PROVEN GAP**: in the real manifest, every clip has a pointer to the job that made it, but `prompt_id` came back **empty on all 10 lipsies**. A lipsie row doesn't hold the prompt - the recipe lives back up the chain on the source image. So the manifest knows *which* clip but the trail to *how to remake it* is broken.

## EXACT NEXT STEP
Build the **recipe-inline** capability (this IS the retroactivity Max wants - do not ask, do it carefully and non-breaking):

For each clip, trace the chain **lipsie ? clip ? source image ? winning prompt** and freeze, verbatim, inside the manifest:
- the winning prompt text + mood codes + parameters,
- the source-image lineage,
- **the flip** (currently unrecorded - manual, baked into files),
- **the trim** (same - unrecorded).

The flip/trim are the untracked gap from his memo. Per the memo's intent: make trims/flips **recorded data applied at render time**, not hand-baked. Validate by trying to regenerate one clip purely from the manifest/D1.

Keep it additive and non-breaking, same as layer 1. Do not break Max's existing flips/trims - those are baked into his real final files by hand; never touch those files.

## OPEN QUESTIONS (do NOT re-ask - these are now answered by Max)
- "Should the manifest chase the full recipe per clip?" ? **YES, that's the whole point.** Already answered. Proceed.

## KEY PATHS / IDS / COMMANDS
- Render code (now v07): `C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6\sc10\sound_assembly\code\render_mixboard_video_v01.py`
- Worktree root: `C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6`
- Branch: `claude/admiring-mahavira-6f8fc6`; merged commit on master: `0b4ba1d`
- Per-machine config (gitignored, must copy into worktree for module to import): `moma_data_root.txt` - source at `C:\moma\sc10\combo_runner\code\moma_data_root.txt`, dest at the worktree's `sc10\combo_runner\code\`
- Servers: combo on **8779**, slideshow on **8790** (both confirmed up)
- Live render command pattern: `python render_mixboard_video_v01.py --scene 9 --quality A --out <temp path>`
- Scene 9 is the active scene (12 lines, recent run). Scene line manifest: `http://localhost:8790/scene_lines_manifest?scene=9`
- Production process saved to: `C:\Users\maxre\.claude\projects\C--moma\memory\project_production_process.md` (indexed in `MEMORY.md`)
- Team board: `python C:/claude_base/branch_bulletin/bcast.py` (whoami/catchup/post) - you are **D16**. **bcast keys identity off cwd** - always post from the worktree root, not from a `cd`'d subdir.
- Worklog: `C:/claude_base/compaction_kb/scripts/worklog.py`; status: `session_status.py`

## THE PRODUCTION PROCESS (Max's own description - the map that was undocumented)
Briefs ? many redos, often editing mood codes and wording ? library-to-pics, lots of tries, dialog with Claude ? Max manually approves some and drops on the storyboard ? Claude+Max produce lipsies ? **flips often** (AI is weak on left/right, especially when camera rotates) ? lots of redos and trims. The redos, mood-code edits, flips, and trims are exactly the history currently being lost.

## GOTCHAS
- **Don't ask permission to start the recipe work.** Max read your last "ready?" question as imitation, not real retroactivity. He's frustrated. Lead with action.
- Manifest currently captures pointers only; `prompt_id` is empty for lipsies because the recipe is upstream on the source image - you must walk the chain.
- Flips and trims are **not recorded anywhere** - hand-done, baked into files. There's nothing to "lose," but there's also nothing to read; you'll need to make them recorded data.
- Keep everything additive/wrapped so render can never break (Max's hard constraint).
- Team is asleep; merge gate is waived for now, but you're editing the same hot file D12/D13/D15 use - keep changes tight and announce on the board.
- Max wants TLDR-style, highlights-only replies ("dtalk").
