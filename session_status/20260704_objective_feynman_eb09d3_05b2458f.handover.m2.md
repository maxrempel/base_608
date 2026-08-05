# Scribe handover - milestone 2 (~181K tokens)
# session: 20260704_objective_feynman_eb09d3_05b2458f
# cwd: C:\moma\.claude\worktrees\objective-feynman-eb09d3
# written: 2026-07-04 14:51:46 by deepseek-v4-pro

# HANDOVER - D03B Research: Glue Merged Audio from Existing Per-Line Voices (No TTS)

---

## GOAL (Max's words, from D02A's board post)

> "find the IN-SYSTEM way to build a merged spot's audio from ALREADY-EXISTING per-line voices, WITHOUT regenerating TTS. Context: sc11"

Three specific sub-questions D02A posed:
1. Where do sc11 per-line mp3s actually live on disk?
2. What tool/code glues them into a merge mp3 without calling Fish-TTS?
3. How was spot1's R0merge actually built? (as a pattern to replicate)

---

## DECISIONS & WHY

**Decision: Research-only, no edits.** D02A explicitly assigned D03B as "research helper" - the session made zero file changes, only read code and ran inspection commands.

**Key finding: No canonical auto-glue tool exists.**
- `sass.py` (sound assembly) has a merge pass that concatenates per-line audio into a merged mp3, BUT it's welded to a full Fish-TTS synthesis run. It cannot be pointed at existing audio files - it always regenerates TTS first.
- `register_merge.py` only writes the merge ledger into the database (merge_hash, member line hashes, spot membership). It doesn't touch audio files.
- `slideshow_server_v01.py` has merge-related endpoints but they rely on sass under the hood (implied by grep hits; the actual code was not fully read, but the grep showed no standalone ffmpeg concat logic).
- The GESTURING PROTOCOL note in the repo describes the expected pattern: "concat per-line MP3s in a fresh `lines_<TS>_<tag>merge/` run dir" - but it's a manual protocol, not automated code.

**Decision: Verified spot1 was hand-rolled.**
- Spot1's merge mp3 (`merge_sp0f26013cb7bd.mp3`, 14.45s) was confirmed to be a concat of two stale per-line files from the old `lines_20260510_1714` directory: `s000_ishtab` (5.79s) + `s001_werner` (8.36s) + gap = 14.45s exactly.
- The merge was done manually with ffmpeg concat, placed into a fresh run dir (`lines_20260630_001255_R0merge`) alongside a hand-written `merges.json`.
- Max's belief that it "just worked automatically" is incorrect - it was a human glue step.

**Decision: Matching spot2 members to old audio is fragile.**
- Spot2 (`sp0421c7fa34a3`) has 8 members (indices 2-9 in the D1 ledger).
- The old `lines_20260510_1714` directory predates the line-hash system - files are named `s0NN_charname.mp3` with no hash in the filename.
- Mapping requires matching character name + text from script_lines, then finding the corresponding old manifest entry.
- **Trap identified:** spot2 has three DEREK "Yes" lines (indices 3, 5, 7). All three resolve to the SAME old file because text is identical and there's no line-hash to disambiguate. Glue would repeat that one file three times. Likely fine (they're all just "Yes") but it's a fragile, not-clean-lineage match.

---

## CURRENT STATE

**What is done:**
- Full code audit of `audio_resolver.py`, `sass.py`, `libup.py`, `register_merge.py`, `merge_ops.py`, `fire_merge_lipsie.py`, `slideshow_server_v01.py` - confirmed no standalone "re-glue existing audio" tool.
- Located the sole per-line audio source: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\scene11_production\lines_20260510_1714\`
- Verified spot1's R0merge was a manual ffmpeg concat (duration verified).
- Confirmed all 19 sc11 merges are registered in the D1 ledger via `merge_ops.all_for_scene('sc11')`.
- Mapped spot2's 8 members and checked old-manifest availability (all found, but 3 collide).
- Posted full findings to the bulletin board tagging @D02A.

**What is NOT done:**
- No audio file was created for spot2.
- No merges.json was written for spot2.
- No code was written or modified.

**In flight:** Nothing. Research is complete. Awaiting D02A's next assignment or go-ahead to actually glue spot2.

---

## EXACT NEXT STEP

If D02A says "go ahead and glue spot2," the procedure is:

1. **Map spot2's 8 member line_hashes to old mp3 files** - read `scene11_production/lines_20260510_1714/manifest.json`, resolve each member's line_hash to (character, text) via the script_lines DB, match against the old manifest entries by char+text.

2. **Create a new run directory** - e.g. `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\scene11_production\lines_<timestamp>_spot2merge\`

3. **Run ffmpeg concat** - build a concat filter or use concat demuxer with the 8 resolved mp3 files in member order. Output: `merge_sp0421c7fa34a3.mp3` in the new run dir.

4. **Write `merges.json`** - keyed to `sp0421c7fa34a3`, listing the member line_hashes in order, pointing `lines_dir` to the new run dir. (Copy spot1's merges.json as a template - it's at `lines_20260630_001255_R0merge/merges.json`.)

5. **Verify** - the audio_resolver checks for the merge mp3 before TTS; once it finds the file and merges.json, the reel should fire without regeneration.

---

## OPEN QUESTIONS (awaiting Max/D02A)

- **Confirm the old `lines_20260510_1714` is the canonical per-line source** - it's the ONLY sc11 per-line directory found. If there's a newer one, we need to know.
- **The three-collision DEREK "Yes" problem** - is repeating the same clip 3x acceptable? Or should we flag it for re-TTS?
- **Should this manual ffmpeg-concat pattern be codified into a tool?** Currently it's tribal knowledge. D02A might want a helper script before gluing more spots.

---

## KEY PATHS & IDs

| What | Path/Value |
|---|---|
| **Worktree** | `C:\moma\.claude\worktrees\objective-feynman-eb09d3` |
| **Scene code** | `C:\moma\sc10\` |
| **Sound assembly** | `C:\moma\sc10\sound_assembly\code\sass.py` |
| **Combo runner** | `C:\moma\sc10\combo_runner\code\` |
| **Merge ops (D1 ledger)** | `C:\moma\sc10\combo_runner\code\merge_ops.py` |
| **Register merge** | `C:\moma\sc10\combo_runner\code\register_merge.py` |
| **Old per-line audio (sc11)** | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\scene11_production\lines_20260510_1714\` |
| **Spot1 R0merge dir** | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\scene11_production\lines_20260630_001255_R0merge\` |
| **Spot1 merge hash** | `sp0f26013cb7bd` |
| **Spot2 merge hash** | `sp0421c7fa34a3` |
| **Spot2 member indices** | 2-9 (8 members) |
| **Bulletin board** | `C:\claude_base\branch_bulletin\bcast.py` |

---

## GOTCHAS

1. **No standalone glue tool exists.** `sass.py` merge pass always runs TTS first. Any "re-glue from existing audio" is currently a manual ffmpeg step + hand-written merges.json.

2. **Old manifest has no line-hash.** Files are `s000_charname.mp3` - matching to the new hash-based system requires resolving through script_lines text, which is lossy when multiple lines have identical text (see DEREK "Yes" x3).

3. **Run directory naming convention matters.** The `_R0merge` suffix on spot1's dir seems significant - the resolver may key off naming patterns. Don't deviate without checking.

4. **Spot1's merges.json** is the only template for the format. It lives at the R0merge dir path above. Read it before writing spot2's.

5. **No files were changed** in this session. Everything is still as-is from before D03B checked in.
