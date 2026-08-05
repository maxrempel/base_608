# Scribe handover - milestone 2 (~154K tokens)
# session: 20260724_objective_feynman_eb09d3_6a8885ef
# cwd: C:\moma\.claude\worktrees\objective-feynman-eb09d3
# written: 2026-07-24 22:34:06 by deepseek-v4-pro

# HANDOVER - Telepathy Training Tapes: Background Generation

---

## GOAL (in Max's own words)

Max wants a series of **darkened, cozy, comfortable/familiar background images** for the "Telepathy Training Tapes" - a series featuring his character Anna within the MoMA production system. The brief evolved across the session:

- **Mood**: meditative, protected, enclosed, warm, healing. *Not* nature (too exposed). Think reiki room or eastern massage-therapy room.
- **Look**: darkened but *not* black. Cozy. Maybe some candles. Variety - home, living room, dacha, yoga-studio-adjacent.
- **Hard constraint**: NO strong symbols/symbolics. Not heavily illustrated. Walls uncluttered.
- **Pipeline constraint** (repeated forcefully): MUST be generated *through MoMA* (fire_job ? fire_image) so they appear in the MoMA Image Maker at `/imager` on port 8779. Earlier telepathy reels were hand-rolled off-model - Max does NOT want that repeated.

---

## DECISIONS MADE + WHY

### 1. MoMA pipeline only (not hand-rolled)

**Decision**: Route through `fire_job()` + `fire_image()`, using `fire_mediakit_portrait.py` as the canonical template.

**Why**: Max explicitly said "Make sure to do it through MoMA, so I can see them listed in MoMA image maker" - twice. The earlier telepathy reels were ad-hoc and invisible in the Image Maker. This batch must be properly audited in the jobs table.

### 2. Dedicated scene + arrangement

**Decision**: Create a new non-movie scene and arrangement - NOT reuse arrangement 40 (the currently active one).

**Why**: `fire_job()` auto-stamps every new image with `app_state.current_arrangement_id`. Firing under arrangement 40 would pollute whatever that arrangement is (likely movie work). The mediakit portrait script demonstrates the clean pattern: create a dedicated scene (e.g. `"media_kit"`) with its own arrangement, so images group cleanly and don't cross-contaminate.

**What was chosen**: Scene name = `"Tape 1"`, Arrangement name = `"Tape 1"`. (Max corrected this from an earlier broader name - he wants it filed under Tape 1 specifically.)

### 3. No reference photo

**Decision**: Omit `input_ref` / `ref_bytes` entirely.

**Why**: These are pure background plates - there is no headshot or foreground subject to composite behind. The mediakit script uses ref bytes only because it swaps backgrounds behind Max's real portrait; here we generate environments from text alone.

### 4. Quality and size locked

**Decision**: `quality='low'`, `size=1536x1024`.

**Why**: `paths.IMAGE_QUALITY` defaults to `'low'` (~$0.017/image, ~40s each). Hard budget gate via `paths.check_image_params()` blocks medium/high unless env vars are set. 1536x1024 is the standard landscape ratio. No reason to deviate.

### 5. Sequential firing only

**Decision**: Loop one image at a time - no threads, no asyncio, no parallel.

**Why**: Parallel requests kill the OpenAI image API. MoMA rules are explicit about this.

### 6. Role = `'shot'` (default)

**Decision**: No explicit role override.

**Why**: Max didn't say "make a plate." Default is `'shot'`.

### 7. Session does NOT approve

**Decision**: Fire with `output_status='pending'` ? update to `'done'` - never approved.

**Why**: Only Max approves. The session is a candidate factory, not an approver.

---

## CURRENT STATE

### What happened before the autocompact thrash

1. **D1 state check** confirmed: no telepathy/reiki jobs exist (`JOBS n=0`), no telepathy arrangement exists (`ARR: []`), `current_arrangement_id = 40`.
2. **`fire_mediakit_portrait.py`** was read in full (295 lines) - it is the confirmed canonical pattern.
3. **A firing script was written** at `C:\moma\sc10\combo_runner\code\fire_telepathy_backgrounds.py`.
4. **Max corrected the scene/arrangement name** - it was set to `"Tape 1"` for both scene and arrangement. The script was edited to reflect this.
5. **Then the session hit autocompact thrashing** - context refilled to the limit within 3 turns of the previous compact, 3 times in a row. The compaction system suggested reading smaller chunks or using `/clear`.

### What was NOT done

- The Kazarian Image and Video Production Method doc was **never read** (required by CLAUDE.md rules before any Kazarian/MoMA image work).
- The firing script was **never executed**. No images were generated. No jobs were inserted.
- No picks-link was presented to Max.

### The firing script (`fire_telepathy_backgrounds.py`)

It exists at `C:\moma\sc10\combo_runner\code\fire_telepathy_backgrounds.py` and follows the mediakit pattern exactly. It should contain:

- Imports: `paths`, `fire_image`, `D1Client`, `connect_db`, `fire_job`, `expense_log`, `datetime`, `json`, `os`, `uuid`
- Constants: `SCENE_NAME = "Tape 1"`, `ARR_NAME = "Tape 1"`, `SCENE_TAG = "Tape 1"`, quality/size from `paths`
- `get_or_create_scene()` and `get_or_create_arrangement()` helpers
- A list of ~6 background prompts (variety of darkened cozy environments: reiki room, living room with curtains, dacha interior, candle-lit space, eastern healing room, warm home nook - all darkened-not-black, no strong symbols, warm earth palette)
- Per-image loop: INSERT prompt ? `fire_job()` ? `fire_image()` ? UPDATE done
- Pre-flight `check_image_params()` guard

---

## EXACT NEXT STEP

1. **Read the Kazarian Image and Video Production Method doc** (from Memex/Notion - required by CLAUDE.md before any Kazarian image work). This was the missing prerequisite that kept getting deferred.

2. **Re-read `fire_telepathy_backgrounds.py`** to confirm it's intact and has the correct 6 prompts and the `"Tape 1"` scene/arrangement names.

3. **Run the script**:
   ```
   cd C:\moma\sc10\combo_runner\code
   python fire_telepathy_backgrounds.py
   ```
   This will sequentially fire ~6 images through MoMA at quality='low', 1536x1024.

4. **Present results** to Max as a picks-link:
   ```
   http://localhost:8779/imager?ids=N,N,N,N,N,N&title=Telepathy+Training+Tapes+backgrounds
   ```
   Plus the verbatim prompts used, below the link.

---

## OPEN QUESTIONS (awaiting Max)

- **"Another six versions"**: Max said "do variety, another six versions" after initially asking for six. Unclear if he wants 6 total or 12 (6 first batch + 6 more). He hasn't seen the first batch yet, so start with 6 and let him react.
- **Candles y/n**: Max said "maybe with some candles or not - do the variations." Some prompts should include candles, some without - variety.
- **Dacha vs spa**: Max leaned homey-dacha but never locked it in. The assistant suggested leaning dacha (feels safer/warmer for telepathy training). Max's response: "Try variety." So prompts should span both.
- **Approval**: Max will approve/reject in the Image Maker after seeing the batch.

---

## KEY PATHS, IDs, & NAMES

| Thing | Value |
|---|---|
| Firing script | `C:\moma\sc10\combo_runner\code\fire_telepathy_backgrounds.py` |
| Canonical template | `C:\moma\sc10\combo_runner\code\fire_mediakit_portrait.py` |
| Scene name | `Tape 1` |
| Arrangement name | `Tape 1` |
| Scene tag | `Tape 1` |
| Target quality | `low` |
| Target size | `1536x1024` |
| Image model | `gpt-image-2` |
| Output subdir | likely `telepathy_tapes/output` or similar (check script) |
| D1 (live DB) | accessed via `D1Client` / `connect_db` from `moma_db.py` |
| Image Maker URL | `http://localhost:8779/imager` |
| Current arrangement ID | `40` (NOT to be used - script creates its own) |

---

## GOTCHAS & DEAD ENDS

1. **Never hand-roll `requests.post` to the image API** - only `moma_image.fire_image()`. Doing otherwise produced the earlier off-model reels that Max rejected.

2. **Never write raw `INSERT INTO jobs`** - only `fire_job()`. It handles auto-stamping, auditing, and integrity.

3. **Do NOT touch `scene_id` in the post-fire UPDATE query** - `fire_job()` already sets it to the TEXT scene tag. Overwriting with the numeric id from the scenes table breaks scene/name filters (this is explicitly warned in the mediakit script at lines 277-280).

4. **Local `combo_db.sqlite` is stale** - always query D1 (Cloudflare) via `D1Client`. Never trust the local SQLite.

5. **Parallel firing kills the API** - the script must use a plain sequential `for` loop, one image at a time.

6. **Quality gate is hard** - `paths.check_image_params()` will refuse `medium`/`high` unless `MOMA_ALLOW_MEDIUM=1` / `MOMA_ALLOW_HIGH=1` env vars are set. Stay at `low`.

7. **Autocompact thrashing** - the session hit a repetitive compaction loop after the script was written. The root cause was likely reading or producing output that was too large for the remaining context window. When resuming, work in smaller steps and avoid large reads/writes.

8. **Kazarian doc not yet read** - this is a CLAUDE.md hard requirement. Do not fire images until it's been read. Find it in Memex or Notion under "Kazarian Image and Video Production Method."
