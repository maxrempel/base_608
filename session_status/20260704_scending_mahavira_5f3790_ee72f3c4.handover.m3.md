# Scribe handover - milestone 3 (~251K tokens)
# session: 20260704_scending_mahavira_5f3790_ee72f3c4
# cwd: C:\moma\.claude\worktrees\condescending-mahavira-5f3790
# written: 2026-07-04 20:51:20 by deepseek-v4-pro

# HANDOVER - D52 Scene 11 Work (condescending-mahavira-5f3790)

## GOAL (in Max's own words)
Make input images for Scene 11 ("Service Desk and Crisis Briefing") reels. The scene has two main arrangements: sc11-arr01 (the introduction - all four standing around the round table) and sc11-arr02 (spot 2 - the four gathered around the table for the briefing, Ishtab standing behind a chair).

## DECISIONS MADE + WHY

### Canon plates for Werner and Derek
Werner and Derek existed as files on disk but had no in-system plate rows. Max had me look at every approved portrait and register them. Registration path: `fire_job` creates the IMPORT row (input_status='done', zero API cost), then UPDATE sets role/kind/character_id/legacy_plate_id/notes (fire_job won't write those on insert - they're not in its whitelist), then two `plate_labels` rows per plate (canon0 + canon:<topic>). Canonical_slots/canonical_history tables are DEPRECATED; the live system is the plate_labels table (canon0..canon3 + canon:<topic>).

### Height canon (s3011 = sc11_heights_v16.png)
After many iterations, Max approved s3011 (job 3010, sc11_heights_v16.png) as the movie-wide size reference. Relative heights: Ishtab shortest, head top at Anna's nose tip. Anna ~5% shorter than Werner. Werner and Derek level (tallest). Derek must NOT be a giant - the model exaggerated when fed his "very tall" character constants. Fix: describe the gradient in plain words, use feet/head-anchors not cm numbers. Recorded in staging bible (kazarian_staging_bible_tomemex.md).

### s2961 as clean interior plate
station_wv_e_ls.png (job 2961) is the canonical empty Art Nouveau room - white walls, curved planet window, round table, bentwood chairs, no people. Feed this, not the populated v10 render, as the room ref.

### Derek constants (load-bearing)
Green reptilian scaly skin, golden eyes, **black beret ALWAYS on (never off)**, dark SC uniform, warm friendly smile, very tall/lanky/snake-like body sprawled loosely. Lesson: the "very tall" words in a prompt make the model exaggerate heights - suppress that in height-sensitive prompts.

### Surgical/minimal-edit principle (critical lesson learned)
When modifying an approved image, do NOT feed the rendered output back as the primary ref (#1). That produces a derivative - faces deteriorate, everyone ends up staring at the camera, mood changes. Instead: keep the **original formula** unchanged (all portrait refs, room, size ref), re-describe from scratch, and if you add the good output as a reference, put it as ref 2/3 (NEVER ref 1). Also: always feed portrait refs and insist "faces EXACTLY from the portraits" - every derivation degrades faces.

### Spot naming
"Reel" = lipsie (talking clip). "Spot" = one storyboard position. sc11-arr01 = spot 1 (introduction), sc11-arr02 = spot 2 (briefing).

### Worker resilience fix (applied, pushed, verified)
Image worker kept dying because Cloudflare D1 network blips (WinError 10054 / read timeout) were unhandled. Two-layer fix: (1) retry-with-backoff in moma_db.py `_request` (add `import time`; retry URLError/TimeoutError/OSError, not HTTPError - protects ALL callers); (2) try/except around worker `while True:` loop body logs+sleeps+continues instead of exiting. Confirmed live on the running workers after full stack restart.

### Memory index compacted
MEMORY.md grew past its token limit and was silently dropping entries. Compacted losslessly - moved 7 big inline rule paragraphs into topic files under memory/, left one-line pointers in the index.

## CURRENT STATE - WHAT IS DONE

| Arrangement | ID | Status | Best image |
|---|---|---|---|
| sc11-arr01 (intro, all four standing) | 8 | **Done** | v17 (3047) is the ideal; v37/v38/v39 (3080-82) have Derek's hello wave corrected |
| sc11-arr02 (briefing, spot 2) | 22 | **Done** | v53 (3114) or v52 (3113) - white Vienna chairs + white cups, podstakannik removed, natural circle |
| sc11-heights (size canon) | 21 | **Done** | s3011 (sc11_heights_v16.png) canonized |
| Werner canon plates | - | **Done** | 3 plates registered (face werner1, face-alt werner2, body sitting-sandals) |
| Derek canon plates | - | **Done** | 6 plates registered (3 faces, 3 bodies including seated_table and standing_leaning) |
| Worker fix | - | **Done** | Pushed to master, verified live on all workers |
| Memory index | - | **Done** | Compacted under limit |

## EXACT NEXT STEP
**Max said "Done" at the end** - spot 2 is finished with v53/v52. No explicit next task was given. The scene still needs per-line audio (script lines exist in the DB) and actual reel/lipsie generation, but Max hasn't asked for that yet. Wait for Max's next directive.

If picking up autonomously: the next logical steps are:
1. Let Max approve/pick v52 or v53 for spot 2
2. Register the spot 2 merge (L02-L09, merge_hash 7ba5320ac9a7c5 - but note: this hash is actually just line L02 alone, and Max said "the merge was fixed by D03B")
3. Generate per-line audio (sass_prep/sass) for scene 11
4. Fire reels/lipsies from the approved stills + audio

## OPEN QUESTIONS
- Spot 2 merge registration status: Max said D03B fixed it, but I couldn't verify. Check merge_ops table for 7ba5320ac9a7c5 before proceeding.
- The two-cup vs three-cup issue on v52/v53: the model under-renders teacups (shows ~2 rather than the prompt's 3). Not flagged as blocking by Max.
- Canonize s2961 as the sc11 room canon: Max asked for it ("use this to canonize as a canonizer and canonized version") but it hasn't been done yet.
- Delete the orphan `_d52_room_landscape_remake.py` script: I asked earlier, Max didn't answer.

## KEY PATHS, IDs, FILES

### Arrangements (scene_id=3)
- sc11-arr01 = id 8
- sc11-arr02 = id 22
- sc11-heights = id 21

### Critical job IDs
- 3010 (s3011, heights canon, sc11_heights_v16.png - SIZE reference)
- 2961 (s2961, station_wv_e_ls.png - clean room interior)
- 3047 (v17, the "ideal" intro - Derek's hand is the ONLY defect, reaching down)
- 3080-3082 (v37/v38/v39, Derek hello-wave corrected)
- 3112-3114 (v51/v52/v53, spot 2 minimal-edit white chairs + white cups)
- 3031 (v23, s3031 - original approved spot 2 base, wood chairs + podstakanniks)
- 2985 (v10, sc11_arr01_v10 - the old three-standing-one-sitting keeper, now superseded)

### Key paths
- OUTPUT_STILLS = `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\`
- Staging bible: `C:\moma\memos\kazarian_staging_bible_tomemex.md` (merged to master)
- Memory index: `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`
- Character folders: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\characters\<name>\approved_portrait\` (or `approved\`)
- Fire scripts (one-off, conventionally NOT committed): `C:\moma\sc10\combo_runner\code\_d52_fire_*.py`
- Notion scene 11: page id `3430316f-5560-8150-bc4f-de12b00ce5ac`

### Derek's canon hello wave spec
Right arm BENT at elbow, open hand RAISED to shoulder height, palm FACING FORWARD, fingers pointing straight UP. NOT flat palm-up, NOT a straight-arm salute - a simple friendly bent-arm wave.

### Script lines
Scene 11 has 85 lines in D1 (`SELECT * FROM script_lines WHERE scene=11`). Columns: scene (INTEGER), idx, char, text, line_hash, norm_text, hash_seed, status, created_at, updated_at.

## GOTCHAS & DEAD ENDS RULED OUT

1. **gpt-image-2 cannot do true panoramas or geometric camera-angle interpolation.** Both approaches tested and failed - the model invents a new room rather than computing the real halfway camera. Shelved per Max.

2. **Feeding TWO rooms (base scene + separate room ref) averages them** ? chair collapse. One dominant room ref only.

3. **Every derivation deteriorates faces.** Never copy faces from a derived image. Always start from the original portrait refs and "stay faithful."

4. **Firing multiple images is SEQUENTIAL** (parallel breaks OpenAI API) - ~40s each, so 3 variants ? 2 min. Not a crash.

5. **fire_job column whitelist** - `role`, `kind`, `character_id`, `legacy_plate_id`, `notes` are NOT accepted on insert. Use fire_job for the base row, then UPDATE for plate annotation.

6. **arrangement_id MUST be passed explicitly** - fire_job's orphan-prevention guard rejects None/''/0; the global current arrangement is sc10 id=2, not sc11.

7. **es.exe (Everything CLI) was unavailable** in this session (empty folder). Use python `os.walk` or the Glob tool for file search.

8. **D56A once cancelled my batch** (3074-76) thinking it duped 3071-73 - but mine had a required cup fix. Board coordination via bcast.py prevented recurrences.

9. **`query_sql` is SELECT-only** (D1 endpoint restriction). Use `execute_sql` for UPDATE/INSERT.

10. **MOMA standard image params**: gpt-image-2, quality low (~$0.017/img), 1536?1024 (16:9). Single source of truth: paths.py.

11. **Podstakannik image exists** at `characters/werner/archive_20260310/batch25_.../08_prop_podstakannik_tall_closeup.png` - found in job 3032's recipe, not via filename search. Search term was simply wrong.

12. **Memory index silently dropping entries** - compacted to 16.8KB (was 26.1KB). Now lossless (big texts in topic files, one-line pointers in index).

13. **Board hook assigns "? C51"** to this session - a known misidentification; true identity is D52.
