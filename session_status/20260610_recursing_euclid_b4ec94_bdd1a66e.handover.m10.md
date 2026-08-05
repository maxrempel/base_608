# Scribe handover - milestone 10 (~155K tokens)
# session: 20260610_recursing_euclid_b4ec94_bdd1a66e
# cwd: C:\moma\.claude\worktrees\recursing-euclid-b4ec94
# written: 2026-06-10 17:13:05 by claude-opus-4-8

# HANDOVER - Assemble Video b-roll fix (D13)

## GOAL (in Max's words)
"We added b roll clips to the sb [storyboard], but the video assembly failed to take them - make it take them and assemble the video properly."

Then, after the first fix attempt: **"it didn't - i assembled and it didn't propagate. Haha."**

So the reported bug is NOT yet actually resolved from Max's point of view. He ran an Assemble Video and the b-roll still did not show up. The work is **in flight**, not done - despite the prior session declaring victory.

## DECISIONS + WHY
- **Root cause diagnosis (believed):** The renderer `render_mixboard_video_v01.py` was old (dated Apr-18, predated b-roll). It built the movie by walking each script line and picking media **by scene tag + a unified sort**, and it required every clip to carry its own spoken audio. B-roll clips are pinned in the storyboard but have **no spoken line / no per-line audio**, so the renderer dropped them to a black "blank" frame.
- **Chosen fix:** Make the renderer mirror exactly what the mixboard *player* (`mixboard.html`) does:
  1. Match each line's media **by line identity (line_hash)**, not scene tag.
  2. **Honor the exact clip Max pinned** in the storyboard (the pinned job wins).
  3. Add a new **b-roll / no-audio branch** (`clipNoAudio` equivalent): a pinned clip with no spoken line plays **once at its native length**, keeping its own audio if present, otherwise silent.
- **Why mirror mixboard:** the player already renders b-roll correctly, so matching its logic guarantees parity between what Max previews and what gets assembled.
- Removed two now-dead bits (`junk_ids`, an `audio_file` block) for cleanliness and bumped the version header to **v06**.

## CURRENT STATE
- Edits were made to the **worktree** copy of the renderer, syntax-checked, and test-rendered for scene 9. Self-test reported mix `{'clip': 2, 'lipsie': 10}` - both b-roll lines ("opening title card" ~8s, "earth arrival" ~5s) appeared, full render ~59s.
- Committed on branch `claude/recursing-euclid-b4ec94`, pushed, and **merged --no-ff into master and pushed**.
- Posted "JOB DONE" to the branch bulletin as D13.
- **THEN Max tested a real Assemble Video and the b-roll did not propagate.** The fix did not take effect in his actual workflow. This is the live problem to solve now.

## EXACT NEXT STEP
Figure out **why Max's Assemble Video click did not pick up v06**. Prime suspects, in order:
1. **Which file does the live server actually spawn?** The edits + merge landed in the main checkout `C:\moma` via master merge, but the running **slideshow/export server may be serving the worktree copy or a different checkout**, or vice-versa. Confirm the path the live Assemble Video button actually executes, and confirm THAT file is v06. (There was already one path-confusion incident this session - a grep ran against `/c/moma` while edits were in the worktree.)
2. **Was the server holding old code in memory?** The prior session claimed "renderer is spawned fresh per export, no restart needed" - verify that assumption is actually true. If the export server imports/caches the renderer, it needs a restart.
3. **Did Max assemble the same scene (9), or a different one?** Confirm the scene he tested actually has pinned b-roll, and that the new line_hash matching resolves those pins for that scene.
4. Re-examine whether the new `build_primary_picks` logic truly resolves the pin for Max's case - the test render was the script's own self-test, which may not match the exact code path the live server export takes.

Start by asking Max which scene he assembled and where the output went, then trace the live Assemble Video button ? which script + which file path it runs.

## OPEN QUESTIONS (awaiting Max)
- Which scene did you assemble, and where did the output land?
- (Previously offered, now moot/secondary) Want scene 9 assembled to the rehearsals folder to watch?

## KEY PATHS / IDS
- Worktree root: `C:\moma\.claude\worktrees\recursing-euclid-b4ec94`
- Main checkout: `C:\moma`
- Renderer (the file edited, now v06): `sc10\sound_assembly\code\render_mixboard_video_v01.py`
- Export/slideshow server: `sc10\sound_assembly\code\slideshow_server_v01.py`
- Player (the parity reference): `sc10\sound_assembly\code\mixboard.html`
- Per-machine data root (gitignored): `sc10\combo_runner\code\moma_data_root.txt` - had to be copied into the worktree to run the renderer there.
- Live server endpoints used for inspection: `http://localhost:8790/scene_lines_manifest?scene=9` and `http://localhost:8790/api/storyboard_state_v2?scene=9`
- B-roll jobs/clips: scene 9 has two b-roll lines - idx=-1 "opening title card" and idx=10 "earth arrival"; jobs **2757 / 2758**; an earlier BROLL clip reference was **2754**.
- Branch: `claude/recursing-euclid-b4ec94`; merge commit message: "Merge: Assemble Video b-roll fix (render_mixboard_video_v01 v06)".
- Bulletin / identity tooling: `python "C:/claude_base/branch_bulletin/bcast.py" whoami D13` / `catchup` / `post`. This session is **D13**. D12 had warned the renderer predated b-rolls.

## GOTCHAS / DEAD ENDS
- **Two checkouts exist** (main `C:\moma` + worktree). Commands silently ran against the wrong one once. Always confirm which path you're editing AND which path the live server runs.
- B-roll clips carry `scene_id='sc09'` - the **whole scene shares that id**, NOT a unique `bg_` id. So picking by scene_id grabs a random dialogue clip, not the pinned b-roll. The fix relies on line_hash matching + honoring the pin instead.
- The renderer's b-roll case must NOT require audio; b-roll may be silent.
- Master had **unrelated uncommitted work** (CLAUDE.md + scratch `_*.py` files) from other sessions - left untouched; only the single renderer file was merged. Keep avoiding those.
- **Do not assume the merge = live.** The whole reason this handover exists: the merge happened, the self-test passed, yet Max's real Assemble Video did not show the b-roll. Treat "it's in master" and "it propagated to the running button" as two separate facts that both need proving.
