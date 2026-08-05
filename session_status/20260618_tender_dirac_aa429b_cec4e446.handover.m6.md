# Scribe handover - milestone 6 (~455K tokens)
# session: 20260618_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-18 08:01:48 by deepseek-v4-pro

# HANDOVER - D21: sc10 Merged Multiline Lipsies Rebuild

---

## GOAL (in Max's words)

Rebuild sc10 - the full 33-line Anna?Ishtab two-hander - as **merged multiline lipsies** (~4 lines per lipsie, where time allows), replacing the old per-line approach. The scene follows a path: **greeting hall ? walking corridor ? window with Earth ? alcove ? doorway/room**. Every lipsie must use the correct location still and every prompt must include the actual spoken lines labeled by speaker/position.

---

## DECISIONS MADE + WHY

### The 15-second hard cap drives the arrangement structure
- wan2.6 i2v-flash has a hard ~15s clip ceiling. Most dialogue lines are short, so 2-7 lines fit together. But two are long monologues (line 8 ?14s, line 23 ?13s) - each fills a clip alone. These two singles are forced, not a choice.
- Silence pads: `silence_buffer=1.0` adds 1s before/after speech, but only where speech ?13s (pad + speech + pad ? 15s). The long monologues get virtually no pad.

### The winning prompt recipe (arrived at through ~20 test fires)
1. **Describe both characters + positions FIRST**, then the quoted lines - not bare "Left/Right" labels (wan ignores those). Example: *"On the left: a young woman with long red hair, white cloak... On the right: an older woman with long dark hair, red robes, jade beads..."*
2. **Speak-ORDER explicit**: *"She speaks first, then the elder answers"* - this is what finally fixed the speaker-swap problem. Order-of-mention matters more than positional labels.
3. **No smile/grin words ANYWHERE** - "grins," "smiles," "warm" all trigger stupid laughing. Kill them entirely. Use "composed," "calm," "formal," "serious."
4. **Only the speaker's lips move; listener stays still** - for standing scenes. This kills the penguin-nodding.
5. **Walking shots need NEUTRAL hand phrasing** - "completely still" froze Ishtab's hand mid-air (robotic), "arms moving naturally" overcorrected to robotic periodic motion. The fix: don't direct hands at all in walking shots. Just let them walk and talk; wan figures out the rest.
6. **In profile, eyes on each other, never the camera** - "at any moment, a formal meeting with the other official, not the camera" stops them addressing a third party.
7. **"Formal meeting of officials" framing** - sets the gravity, minimal nods, royal postures.

### Location stills per beat
The spine already has a distinct per-line still for every line. I reused ONE still per location (B1 for all walking beats, sc05 for all windows) - **this is wrong**. Max's post-review note: every arrangement needs its own starting still (different corridor framing, different window angle, etc.). The stills exist in the spine - just need to pull them per-arrangement.

### Arrangement boundaries
The 33 lines are split into **11 arrangements** (one merged lipsie each). Boundaries come from the existing DB arrangement containers (ids 2-7) and natural beat breaks:
- arr01: 0-3 (greeting)
- arr02: 4-5 (hall, "turning point")
- arr03: 6-7 (hall, "brightest babies")
- arr04: 8 (Anna monologue, forced single - 14s)
- arr05: 9 (Ishtab, "you must have questions")
- arr06: 10-16 (window, staccato call-and-response)
- arr07: 17-22 (window, "what is delaying the contact")
- arr08: 23 (Ishtab monologue, forced single - 13s)
- arr09: 24-27 (alcove, "one coalition")
- arr10: 28-29 (doorway, "explain")
- arr11: 30-32 (room, "make yourself at home")

---

## CURRENT STATE

### Final approved lipsie set (11 jobs)
| arr | lines | job id | status |
|---|---|---|---|
| 01 | 0-3 (greeting) | **2774** | approved |
| 02 | 4-5 | **2775** | approved |
| 03 | 6-7 (walking) | **2810** | approved ("excellent") |
| 04 | 8 (Anna mono, walking) | **2812** | done - the ONE new clip Max hasn't reviewed yet |
| 05 | 9 (walking) | **2811** | approved ("great") |
| 06 | 10-16 (window) | **2805** | approved ("not too bad") |
| 07 | 17-22 (window) | **2806** | approved |
| 08 | 23 (Ishtab mono, window) | **2807** | approved |
| 09 | 24-27 (alcove) | **2808** | approved |
| 10 | 28-29 (doorway) | **2794** | approved |
| 11 | 30-32 (room) | **2795** | approved |

Max's last message: "these were all my approvals, I reapproved. I expected a new batch. These are mostly already approved. Maybe 1 new. read all comments in that batch."

So only **2812** (line 8 walking) is truly unreviewed. The rest were re-approved.

### Status field issue
At some point the 11 lipsies showed as 'approved' when they should have been 'done'. Max says that was his doing (re-approving). The worker only writes 'done' - there's no auto-approve bug. But worth noting: if the modified Lipser auto-sets status on load, that could cause confusion.

### Lipsies not showing in MOMA arrangements
The merged lipsies carry synthetic line-hashes (from the merged audio track, not from individual sc10 script lines), so they don't attach to the per-line spine that the arrangement view lists. Max modified the Lipser to view by scene instead of arrangement to work around this. The arrangement containers may show empty in the old view.

### Max's critique for next round
"Every lipsie must start from a different image" - the walking beats all reused B1_corridor_walk, the window beats all reused sc05_window_twoshot. The spine has distinct per-line stills; each arrangement should pull its own.

---

## EXACT NEXT STEP

1. **Read ALL comments** on the 11 final jobs (especially 2812, and any comments Max left on the already-approved ones during his re-review).
2. **Present only 2812** to Max for fresh review (the one unreviewed clip - line 8, Anna monologue, walking corridor, neutral-hands recipe).
3. **Wait for Max's green light**, then plan the next round: re-fire the whole scene with a **distinct starting still per arrangement** (pulled from the spine's per-line stills for each arrangement's starting line), using the locked winning recipe.
4. After that, Max mentioned "the next arrangement" - likely sc10's next scene or the next project.

---

## OPEN QUESTIONS AWAITING MAX

- **Is 2812 (line 8 walking) good?** It used the same recipe as approved 2811 - should be fine, but needs Max's nod.
- **How should the spine-attachment be handled?** The merged lipsies don't show in arrangements because of synthetic line-hashes. Does Max want them propagated into the spine, or is scene-view sufficient?
- **Budget for the distinct-still redo round:** ~11 fires ? $0.30 ? $3.30. Max authorized $4-5 for finishing.

---

## KEY PATHS / IDs / COMMANDS

### Database
- **D1Client** lives at `C:\moma\sc10\combo_runner\code\moma_db.py`
- Query: `d1.query_sql('SELECT ... FROM jobs WHERE ...')`
- Useful fields: `id`, `output_status` ('pending'|'processing'|'done'|'junked'|'approved'), `output_comment`, `comment2`, `vocal_line`, `audio_hash`, `prompt`, `source_still_path`

### Job IDs - final set
`2774, 2775, 2810, 2812, 2811, 2805, 2806, 2807, 2808, 2794, 2795`

### Job IDs - junked/obsolete (do not reuse)
2761-2763, 2765-2770, 2772, 2783, 2784, 2787-2793, 2796, 2798-2804, 2809 (various experiments)

### Source stills used
- **Greeting hall two-shot:** `sc01_meet_twoshot_var01.png` (Anna left, Ishtab right, red hair/white cloak vs elder/red robes/jade beads)
- **Walking corridor two-shot:** `B1_corridor_walk_warm_v01.png` (Anna left, Ishtab right, walking toward camera)
- **Window two-shot:** `sc05_window_twoshot.png` (Ishtab LEFT, Anna RIGHT - speakers FLIPPED for this beat, Earth drifting outside)
- **Alcove frame:** extracted mid-frame from existing spine lipsie (Anna left, Ishtab right, garden backdrop)
- **Doorway/room frames:** extracted from existing spine lipsies `door_pan_left` (both jobs 2794 and 2795 used same frame - needs fixing)

### Audio resolver
- `audio_resolver.py` - `resolve_per_line_audio(line_hashes, vocal_line)` returns MP3 path
- Merged audio built via `_merge_fire_exp.py` pattern (concatenate per-line MP3s with ffmpeg)
- Merged audio tracks stored under `C:\moma\sc10\combo_runner\data\` with naming like `merged_d21e8...`

### Lipser review links
- Full scene: `http://localhost:8779/lipser?ids=2774,2775,2810,2812,2811,2805,2806,2807,2808,2794,2795&title=sc10%20FINAL`
- Single clip: `http://localhost:8779/lipser?ids=2812&title=...`

### MOMA stack
- GUI server: `localhost:8779` (started via `C:\moma\sc10\start_moma.bat`)
- wan26au worker: `combo_wan26au_worker.py` - poll loop, model `wan2.6-i2v-flash`, `prompt_extend` OFF
- Worker PID stored in `../data/wan26au_worker_pid.txt`

### Memory files (saved lessons)
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_no_grin_smile_words.md` - never use grin/smile/warm words
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md` - when Max asks for a variation, don't re-fire his verbatim prompt
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md` - fire and move on; don't block on polling
- `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_distinct_still_per_lipsie.md` - every lipsie needs its own starting still
- Main MEMORY.md at `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` indexes all feedback

### Helper scripts (ad-hoc, in `C:\moma\sc10\combo_runner\code\`)
- `_d21_probe.py`, `_d21_probe2.py`, `_d21_probe3.py` - D1 queries to map lines/arrangements/stills
- `_d21_spine.py` - ingested the full spine (lipsie?clip?still trace)
- `_d21_textmap.py` - dumped the 11 arrangements with actual dialogue text
- `_d21_readcomment.py` - reads a job's comments from D1
- `_d21_batch.py` - reads comments across a batch of job IDs
- `_d21_setdone.py` - reset statuses to 'done'
- `_d21_walkfix.py` - fired 2810 (speak-order fix) and 2811 (neutral hands)
- `_d21_line8_final.py` - fired 2812 (line 8 final)
- Various `_d21_fire*.py`, `_d21_poll.py`, `_d21_test3.py`, `_d21_deftest.py`, `_d21_final.py` - earlier experiments

### Worklog
- `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"` - append entry
- `python C:/claude_base/compaction_kb/scripts/worklog.py read` - view entries

### CWD
`C:\moma\.claude\worktrees\tender-dirac-aa429b`

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **Smiles/grins** in prompt ? laughter and idiotic nodding. **Rule: never use smile, grin, warm, or any positive-emotion adjective.**
2. **Bare "Left:" / "Right:" labels** ? wan ignores them; speaker swap persists. **Fix: describe both characters physically first, then state speak-order explicitly.**
3. **"Completely still" for walking shots** ? freezes limbs mid-air, looks robotic. **Fix: don't direct hands at all for walking shots; neutral phrasing.**
4. **Writing dialogue text in the prompt does NOT sync the nods** - the model can't read line timing from text. The prompt only controls visual style and who-speaks-when.
5. **Bracket text** (surrounding preceding/following dialogue) ? confused the model about which speaker is on which side. **Dead end - don't use.**
6. **Single prompt for 4-turn 15s clip** ? too much idle time, model invents nodding. **Mitigation: shorter merges (2-3 lines), or explicit "listener stays still" clause.**
7. **"Minimal grins"** - even the word "grins" triggers smiling. **Rule: ban the word itself.**
8. **One still reused for all beats in a location** - Max wants distinct starting stills per arrangement. **Fix for next round: pull the spine's per-line still for each arrangement's first line.**
9. **Camera gaze** ("they looked at the camera like referring to a third party") ? **Fix: "in profile, eyes on each other, a formal meeting with the other official, not the camera."**
10. **"Grand" wording** ("vast celestial spectacle") spawned the Earth planet in the background. **Fix: grounded, literal descriptions only.**
11. **The worker is detached** - Max's rule: fire and stay responsive, don't block on polling. Use ScheduleWakeup for autonomous checks when Max is away.
12. **Only Max approves** - the worker writes 'done', never 'approved'. The approval path is Max-only via the Lipser GUI.
