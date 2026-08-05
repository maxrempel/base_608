# Scribe handover - milestone 9 (~680K tokens)
# session: 20260619_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-19 17:39:24 by deepseek-v4-pro

# HANDOVER: D21 - sc10 Merged Multiline Lipsies

---

## GOAL (Max's words)
Rebuild sc10 (33-line Anna?Ishtab two-hander) as **multiline merged lipsies** - ~4 lines per arrangement, one continuous clip per beat. The conversation moves along a path (lobby ? corridor ? window ? alcove ? room). Every arrangement must have a **distinct starting still**, not share the same background across beats. The merged reels must auto-land in the spine/storyboard.

---

## WHAT WAS DONE

### Scene rebuilt into 11 multi-line merged arrangements
All 33 lines are covered. Each arrangement = one wan2.6-i2v-flash lipsie from a merged audio track. The beats (from the scene's own DB arrangement containers):
- **arr01** (0-3): greeting in the hall ? approved (2774)
- **arr02** (4-5): turning point ? walking corridor ? approved (2828/J483 still)
- **arr03** (6-7): babies/recognition ? walking corridor ? approved (2833, "perfect")
- **arr04** (8): Anna 14s monologue ? walking corridor ? approved (2812, "perfect" on B1_corridor_walk)
- **arr05** (9): Ishtab "you must have questions" ? walking corridor ? approved (2811, "great")
- **arr06** (10-16): "they think they're alone" staccato ? window ? approved (2805)
- **arr07** (17-22): government/why ? window ? approved (2806)
- **arr08** (23): Ishtab 13s monologue ? window ? approved (2807)
- **arr09** (24-27): alcove ? approved (2808)
- **arr10** (28-29): doorway ? approved (2794)
- **arr11** (30-32): room arrival ? approved (2795)

**Two arrangements are forced singles** (not 4-line): arr04 (line 8, 14s) and arr08 (line 23, 13s) are long monologues that each fill the 15s clip cap alone. Not a choice - a time limit.

### The locked prompt recipe (what finally worked)
- **Describe both characters + their positions first** ("On the left: a young woman with long red hair... On the right: an older woman with long dark hair, red robes...")
- **Speak-ORDER** ("Left speaks first, then right answers") - killed the speaker-swap bug
- **No smile/grin words** - "smiles" causes laughter; "minimal grins" still triggers grinning. Use "calm, formal, composed" only
- **Only the speaker's lips move** - listener remains still (for standing/serious beats)
- **Walking shots: neutral hands** - don't say "hands still" (frozen) or "arms moving" (robotic). Use "walks calmly and naturally, relaxed"
- **In profile, eyes on each other** - never address the camera (weather-forecast look)
- **No zoom-ins from a low-res still** - wan fabricates faces. Walking away from camera is safe
- **Describe-both-first** prevents wan from swapping L/R speakers (the model ignores bare "Left"/"Right" labels but tracks named characters)

### The spine auto-land bug - FIXED
**Problem:** merged reels weren't showing in the storyboard/spine because each re-fire got a new synthetic `line_hash` that didn't match the spine's `line_current_clip` picks. Two failure modes: re-renders (hash mismatch) and reels made while storyboard was closed (absorbed into baseline).

**Fix shipped** (commit `21562f7`): `fire_merge_lipsie.py` now auto-pins `line_current_clip` for every member line at fire time. Every new merged reel claims its spine spot on creation - cannot be forgotten. D30recoder is also running a one-shot repair from the membership map D21 provided (`d21_merge_membership_*.json` - 75 reels mapped by beat).

### The background distinctness work
Max requires every arrangement to start from a **different image** - no two beats on the same still. Replaced the B1-corridor triplet (arr03/04/05 all shared `B1_corridor_walk`) with distinct stills: arr02 = walk2-A (J483), arr03 = walk2-B (? "perfect"), arr04 = B1 (?, now unique to arr04). arr05 still needs its fourth distinct corridor walking two-shot.

**Key insight about hands:** bent/frozen hands come from the **source still's hand pose**, not the prompt. Wan2.6 freezes whatever hand pose is in the starting frame. The lever is **frame/still selection** (pick relaxed-hands frames), not prompt wording. Full-quality PNG stills beat frame-extracted 720p (quality loss, motion blur).

### The clipper tab - retired
Removed from `moma_restart.py` and `moma_refresh.py` auto-open tab lists (pushed to master, `de86db2`). Tabs now: imager, lipser, storyboard.

---

## CURRENT STATE
- **11 merged arrangements covering all 33 lines** - all approved by Max
- **arr05 (line 9)** is the only beat that still needs a distinct walking still (its current version shares B1 with arr04, which is now B1's only owner - acceptable but not yet distinct)
- **Walking corridor two-shots available:** walk2-A (J483, on arr02), walk2-B (on arr03), B1_corridor_walk (on arr04). Need a 4th for arr05
- **Spine auto-land:** permanent fix shipped; D30's one-shot repair running
- **Next round punch-list from Max's comments** (not yet executed):
  1. Distinct still per lipsie - the big remaining item for the full scene
  2. arr11 (2795): room is behind them - they should turn toward it; portraits drifted from canon
  3. arr07 (2806): Anna's delivery should be more relaxed, analytical, warm
  4. Minor: arr02 last-half-second smile; arr06 small artistic interpretations

---

## EXACT NEXT STEP
**For arr05 (line 9):** obtain a fourth distinct corridor walking two-shot (Anna-L/Ishtab-R, relaxed hands, good quality PNG). Max can drop one into the spine (like he did with J483), or D21 can generate one. Once the still exists, fire a merged walking lipsie for line 9 using the locked recipe (describe-both-first, walk continuously toward camera, eyes on each other, neutral hands), keyed to line 9's canonical merge id so it auto-lands.

**Then:** apply the remaining punch-list (arr11 turn-to-room, arr07 Anna warmer).

---

## OPEN QUESTIONS FOR MAX
1. **arr05 fourth walking still:** drop one in the spine (like J483), or generate one?
2. **arr11 "turn toward the room":** every existing frame has them facing forward. Wan can't rotate characters 180?. This needs a freshly *generated* still (face-to-room + canon portraits). Go ahead with that image-gen?
3. **Full re-roll with distinct stills:** after arr05 is resolved, want a complete re-pass making every one of the 11 arrangements use a unique still, applying all punch-list notes?

---

## KEY PATHS & IDs

### The scene (in order)
| arr | lines | approved job | still used |
|-----|-------|-------------|------------|
| 01 | 0-3 | 2774 | sc01_meet_twoshot |
| 02 | 4-5 | 2828 | walk2-A (J483, `sc_walk2_c2_pan_right_v01_A_v01.png`) |
| 03 | 6-7 | 2833 ? | walk2-B (`sc_walk2_c2_pan_right_v01_B_v01.png`) |
| 04 | 8 | 2812 | B1_corridor_walk (885) |
| 05 | 9 | 2811 | B1_corridor_walk (shared - needs distinct) |
| 06 | 10-16 | 2805 | sc05_window_twoshot |
| 07 | 17-22 | 2806 | sc05_window_twoshot (distinct frame variant) |
| 08 | 23 | 2807 | sc05_window_twoshot |
| 09 | 24-27 | 2808 | alcove frame from spine clip |
| 10 | 28-29 | 2794 | door_pan_left frame |
| 11 | 30-32 | 2795 | door_pan_left frame |

### Critical files
- `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py` - **modified** (spine auto-pin, commit `21562f7`)
- `C:\moma\sc10\combo_runner\code\batches.py` - use `python batches.py comments N` to read Max's verdicts
- `C:\moma\sc10\combo_runner\local_state\d21_merge_membership_*.json` - gold membership map (75 reels ? member lines)
- `C:\moma\sc10\moma_restart.py` and `moma_refresh.py` - clipper tab removed
- Still library: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\`
- Composites: same path under `\composites\`

### Memory files (Max's rules, saved for all sessions)
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md` - no smile/grin/grin words; also no zoom-in on low-res
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md` - don't re-fire Max's verbatim prompt
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md` - fire and detach; don't block on render polling
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_distinct_still_per_lipsie.md` - every arrangement needs a unique starting still
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_only_max_approves.md` - observation = discuss only; fire only on explicit command
- `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` - master index

---

## GOTCHAS & DEAD ENDS

### Prompt failures (do not repeat)
- **"smiles" / "warm" / "grins"** ? random bursts of laughter or excessive smiling. Use "calm, formal, composed, serious" only
- **Writing dialogue text in the prompt does NOT sync nods** - the model can't read line timing from text. It's useful for speaker attribution (who says what) but not for timing
- **"Listener completely still / motionless"** ? freezes the listener's hand mid-air unnaturally (especially bad on walking shots)
- **"Arms moving with her steps"** ? robotic periodic arm motion
- **Bracket text** (wrapping lines with preceding/following dialogue in the prompt) ? scrambles Left/Right speaker assignment (2767/2768)
- **Zoom-in from a static frontal still** ? wan fabricates face detail (low input resolution) or makes them address the camera like a weather forecast
- **Static standing still for a walking shot** ? wan slides them instead of walking ("floating")

### Technical constraints
- **15-second hard clip cap** on wan2.6 - forces the two long monologues (line 8 = 14s, line 23 = 13s) to be singles
- **Total sc10 dialogue = ~2 min 5 s** (125s speech, ~2:15 with turn gaps)
- **Model = wan2.6-i2v-flash** - same model that worked on sc09's short 2-line clips
- **Hands are a wan weak spot** - the only reliable lever is picking a source still with relaxed hands; no prompt wording fully controls them
- **Speaker assignment is unreliable with bare L/R labels** - the describe-both-first + speak-order recipe is what cracked it
- **Frame extraction degrades quality** (720p, motion blur) - always prefer full-quality PNG source stills from the spine
- **MOMA UI at `localhost:8779`** - lipser view: `/lipser?ids=X,Y&title=...`

### Process rules (learned painfully)
- **Never re-fire Max's own verbatim prompt** - he already fired it; you're making a variation
- **Fire and detach** - never block/sleep polling renders. Just fire, note the link, move on
- **Observations are NOT action commands** - discuss/advise, don't fire until Max explicitly says "do it" / "please" / "yes"
- **Only Max approves** - never set `output_status='approved'`. The worker stamps `'done'`; Max approves via the UI
- **Max can't read 4-digit numbers or long blocks** - keep responses short, no job ID lists in narration
- **Use `batches.py comments N`** to read Max's verdicts grouped by fire-batch
- **Now called "reels" not "lipsies"** - team rename for dictation clarity
