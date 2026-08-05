# Scribe handover - milestone 10 (~750K tokens)
# session: 20260619_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-19 18:49:24 by deepseek-v4-pro

# D21 SC10 - HANDOVER FOR COLD SESSION

## GOAL (Max's words)

Max registered D21 to work on sc10: merge per-arrangement script lines into **one multiperson lipsie (now called a "reel")** each, covering all 33 lines of the Anna?Ishtab two-hander. At the end of the session, **D31 updated the storyboard script and lost lots of recent reels** - Max wants D21 to coordinate with the team (D26, D30) and restore them.

---

## DECISIONS MADE + WHY

### The winning prompt recipe (arrived at after ~30 fires)

After many failures, the template that works for merged two-person reels on wan2.6-i2v-flash:

1. **Describe both characters first** - names + positions ("On the left: a young woman with long red hair... On the right: an older woman with long dark hair, red robes...") - wan ignores bare "Left/Right" labels but responds to character description + position.
2. **Explicit speak-ORDER** - "the red-haired woman on the left speaks first, then the elder on the right answers." This, not position labels, fixes the speaker-swap bug.
3. **No smile/grin words anywhere** - any mention of "smile," "grin," "gentle smile," "warm" causes wan to produce random laughter or grinning on serious topics. The winning words: "composed," "serious," "formal."
4. **Neutral hand phrasing** - "walks calmly, relaxed and at ease" works. "Listener completely still" freezes hands mid-air in unnatural poses. "Arms moving with steps" makes robotic periodic motion. Neutral = best.
5. **"In profile, eyes on each other, never the camera"** - frontal stills make them address the lens (Max called it "weather-forecast look").
6. **Walking shots need a walking-pose source still** - wan can't invent a gait from a standing still (produces "floating"). Use mid-stride character two-shots.
7. **Source still's hand pose = rendered hand pose** - the single biggest lever for hand quality is frame selection, not prompt wording. Pick stills where hands are relaxed/natural.

### The 15-second clip cap

Each merged reel has a hard ceiling of ~15s (wan2.6 max clip length). Two lines are 13-14s monologues (L8 Anna ?14s, L23 Ishtab ?13s) that must be singles - nothing else fits. Everything else is 2-7 lines per reel.

### Distinct stills per arrangement

The scene moves along a path: lobby ? corridor ? window ? alcove ? room. Every arrangement must start from a **different** source still (different part of the path). Reusing the same still across multiple arrangements (e.g. B1 for arr03/04/05) was wrong. The fix: each arrangement gets its own full-quality character two-shot from the pile, not a frame extracted from a clip (extraction = 720p motion blur, quality loss).

### Spine auto-land fix (shipped to master)

Root cause of reels not showing in the storyboard: merged reels carried synthetic line-hashes that didn't match the DB's `line_current_clip` picks, so the storyboard couldn't place them. **Fix shipped** in `fire_merge_lipsie.py` (commit `21562f7`): the endpoint now auto-pins `line_current_clip` for every member line at fire time, so merged reels always land in the first spine. D30 also healed 12 beats from D21's membership map.

### The 6-7 corridor image problem

Max placed a new image for lines 6-7 (`extrap3_06_8ft_v2.png`) - it was an **empty corridor** (no characters). Instead of slow compositing, D21 found a ready-made character walking two-shot in the same corridor style (`sc_walk_extrap3_05_8ft_A_v01.png`) and used that.

---

## CURRENT STATE (at end of session)

### The approved scene structure (from Max's "good copy" paste)

```
arr01 (L0-L2):  merged reel 585  - greeting, lobby
L03:            reel 2826        - "arrived at the right moment" + walk-to-camera transition
arr02 (L4-L5):  reel 2835        - walking corridor, from J483/c483 plate
arr03 (L6-L7):  reel 2836        - walking corridor, from extrap3_05_8ft two-shot (just made)
L08:            reel 2812        - Anna monologue, walking (Max: "perfect")
L09:            reel 2815        - Ishtab, walking ("great")
arr06 (L10-L16): reel 2829      - window dialogue, Anna relaxed (just made)
arr07 (L17-L22): reel 2817      - window dialogue
L23:            reel 2837        - Ishtab monologue, from J482 plate (just made)
arr09 (L24-L27): reel 2808      - alcove
arr10 (L28-L29): reel 2839      - from J444 plate (just made)
arr11 (L30-L31): reel 2838      - from J490 plate (just made, has label bug - see gotchas)
L32:            reel 2795        - final room
```

### What D31 broke

D31 updated the storyboard script (`storyboard_editor.html` or `slideshow_server_v01.py`) and **lots of recent reels disappeared from the spine**. The reels exist in the DB (they have job IDs and rendered files), but the storyboard isn't showing them in the first-spine picks anymore. The reels made just before the break were 2836, 2837, 2838, 2839 - plus potentially earlier ones D31's change may have clobbered.

### Files just committed to master

- `sc10/moma_restart.py` (v15) - clipper tab removed from auto-open
- `sc10/moma_refresh.py` (v05) - clipper tab removed from auto-open
- `sc10/combo_runner/code/fire_merge_lipsie.py` - auto-pin spine picks at fire time

### Membership map delivered to D30

`C:\moma\sc10\combo_runner\code\local_state\d21_merge_membership_*.json` - maps every merged reel job_id to its member line indices. D30 used this for the 12-beat heal. This file is the gold record if anything needs re-pinning.

---

## EXACT NEXT STEP

1. **Coordinate with D26 and D30 on the bcast board** (`python C:/claude_base/branch_bulletin/bcast.py read`). D31's storyboard-script change is the cause of the lost reels - D26 (storyboard owner) needs to identify what D31's commit changed that wiped the spine picks.

2. **Verify which reels are actually lost** by dumping the current `line_current_clip` table and comparing against the good-copy map above. Script already exists at `_d21_spine_state.py`.

3. **Re-pin any lost reels** using the same pattern already proven: upsert `line_current_clip` for each member line to point to the correct reel job_id. The fire_merge_lipsie auto-pin logic (commit `21562f7`) is the reference implementation - copy that upsert pattern.

4. **Check if D30's repair process relabeled 2838** - the reel has correct merged audio (L30+L31) but its `vocal_line` got overwritten to "Indeed." (L31's text). D30 was flagged on the bcast board but it may not be resolved yet.

5. **2830-2832 were D21's attempt at distinct-bg redos of the B1 triplet** - but Max approved the original B1 versions (2812/2815) plus the new walk2-B (2833). 2831 and 2832 were junked. Make sure the spine has the approved ones, not the junked ones.

---

## OPEN QUESTIONS

- **What exactly did D31 change in the storyboard script?** This needs to be traced from the git log. The fix depends on whether it was a schema change, a wipe of pick state, or a rendering bug.
- **Is the arr05 (line 9) reel finalized?** Max had approved 2815 but also wanted a distinct bg - it was using B1 which also belongs to arr04 (2812). A 4th distinct corridor walking two-shot was still needed.
- **L32 standalone vs merged?** Currently L32 is standalone (2795). It could merge with L30-L31 but Max seemed to want it separate.
- **Does the 6-7 corridor image need Anna+Ishtab composited into it?** D21 used a pre-existing two-shot instead of Max's placed empty-corridor image. Max may want it done from his exact image.

---

## KEY PATHS, FILES, IDs

| What | Where |
|---|---|
| MOMA code checkout | `C:\moma\` (worktree at `C:\moma\.claude\worktrees\tender-dirac-aa429b`) |
| sc10 combo_runner code | `C:\moma\sc10\combo_runner\code\` |
| DB client | `moma_db.py` ? `D1Client`, `connect_db()`, `fire_job()` |
| Audio resolver | `audio_resolver.py` ? `resolve_per_line_audio()` |
| Fire merge endpoint | `fire_merge_lipsie.py` (has the auto-pin fix) |
| Storyboard server | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` |
| Batches/comments tool | `batches.py` ? `python batches.py comments N` |
| Spine state dump | `_d21_spine_state.py` (D21's script) |
| Membership map | `local_state/d21_merge_membership_*.json` |
| MOMA GUI | `http://localhost:8779` (lipser, imager, storyboard) |
| Bcast board | `python C:/claude_base/branch_bulletin/bcast.py read` |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| Memory rules | `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` |
| Good-copy spine reference | Max's paste in the transcript (after "I have the copy of what was before") |

### Key job IDs (the approved set)

**In spine order:** 585, 2826, 2835, 2836, 2812, 2815, 2829, 2817, 2837, 2808, 2839, 2838, 2795

**Also approved but pre-merge fallbacks:** 2774, 2775, 2810, 2811, 2805, 2806, 2807, 2794

**Source images used:**
- J483/c483 - corridor walk, plate for arr02 (L4-L5)
- J482 - corridor+window, plate for L23 (`sc_walk2_c2_orig_B_v01`)
- J490 - room door, plate for L30-L31 (`sc_door_d_pan_right_v01_B`)
- J444 - alcove, plate for L28-L29 (`sc_walk_fix_alcove_color_v01_B`)
- extrap3_05_8ft - walk two-shot used for L6-L7 (not the empty corridor)

---

## GOTCHAS + DEAD ENDS ALREADY RULED OUT

1. **Zoom-ins are doomed** - input still resolution is too low; wan makes up faces. Walk-away or walk-toward-camera works; push-in to closeup does not.
2. **Frontal stills = characters address the camera** - they must face each other in the still (profile/three-quarter). A frontal still can't be prompted into profile; wan won't rotate them.
3. **"Smiles" / "grins" / "warm" / "gentle" in prompts ? laughter** - never use any positive-emotion word in wan2.6 prompts for these characters. "Formal," "composed," "serious" only.
4. **"Listener stays still / frozen / motionless" ? frozen hands mid-air.** Only use for standing/serious static shots. For walking: "walks naturally, relaxed, at ease" with no hand-direction words at all.
5. **"Arms moving with steps" ? robotic periodic motion.** Neutral is the only working lever.
6. **Bare "Left"/"Right" labels are ignored by wan** - must describe both characters + positions first, then use explicit speak-order.
7. **Extracting frames from rendered clips = 720p quality loss** - always use full-quality source PNG stills from the pile instead.
8. **The merge-audio line-hash is a synthetic random ID** - it can't match any `script_lines` row, which was the root cause of the spine-not-showing-reels bug. The fix (auto-pinning `line_current_clip`) is live on master.
9. **D30's repair process relabels fresh reels** - it overwrites the `vocal_line` and `line_hash` on reels it touches. Flagged but may not
