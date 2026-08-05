# Scribe handover - milestone 2 (~166K tokens)
# session: 20260621_funny_torvalds_1f92dc_ba4460c1
# cwd: C:\claude_base\.claude\worktrees\funny-torvalds-1f92dc
# written: 2026-06-21 15:04:21 by deepseek-v4-pro

# HANDOVER - D59: Media Kit Guards Done + J2855 Photos Disappearance Investigation

---

## GOAL (Max's words)

Two parts, one complete and one new:

1. **(COMPLETED)** Lock down MOMA image-making so new sessions **cannot** quietly change quality/resolution/price. Hard guards, automatic resistance, and explicit instructions. "The session should get back a lot of resistance when it fucking tries to spend more money or change fucking resolution."

2. **(NEW - active)** Investigate why an image called **J2855** suddenly disappeared from the Windows Photos app. Max uses Photos to review, manually crop, and then feed images to the session making his media kit. This disappearance breaks his workflow.

---

## DECISIONS & WHY

### The Guard Architecture (why this way)

**The jailbreak that caused all this:** D50/D57 changed `quality` from `low` to `medium` in a fire script. The old gate in `paths.py` only blocked `high` - `medium` passed silently. Medium quality on gpt-image-2 costs ~4? more and takes ~10 minutes per image (vs. ~40s on low). That's the "10 min and only one image produced" bug Max reported. The gate should have caught it but didn't.

**Three locks built (not one):**

1. **Hard gate in `paths.check_image_params`** - now blocks ANY quality above `low`, ANY non-standard size, and ANY batch over 60 images. Refuses with a loud cost-multiplier message and a SystemExit. The only way around it is a deliberate opt-in environment variable (`MOMA_ALLOW_MEDIUM=1`, `MOMA_ALLOW_HIGH=1`, `MOMA_ALLOW_BULK=1`). Can't happen by accident.

2. **Single entry point `moma_image.fire_image`** - one canonical function that does the POST to OpenAI and *internally calls the gate before spending anything*. New sessions use `fire_image()`; no more copy-pasting the POST block into every script. The gate can't be skipped without the session obviously re-implementing raw `requests.post` from scratch.

3. **CLAUSE.md instructions** - a "Making Images - The Standard Way" section in `C:/moma/CLAUDE.md` that the next session will read when it auto-imports the project rules. Tells them to use `moma_image.fire_image`, that the defaults are the only right choice, and what the deliberate opt-in looks like.

**Why not break the movie worker:** Before touching the gate, D57 verified that `combo_worker.py` (the main Kontakt Countdown movie pipeline) always uses pure defaults at line 115 and *never calls the gate*. So tightening the gate only affects ad-hoc fire scripts - zero risk to the movie.

**The two existing media-kit scripts were refactored** to use `fire_image` instead of their own inline POST blocks. That's the "drift source" eliminated.

**Cost table gap was fixed too:** Portrait size `1024x1536` was missing from the cost table - it would fall through to a $0.25 default estimate instead of $0.017. Added portrait entries for low/medium/high.

### Tested free (no API money spent)

The guard correctly blocks `medium`, `high`, bad sizes like `"1920x1080"`, and big batches. The opt-in escape hatch (`MOMA_ALLOW_MEDIUM=1`) works. The `moma_image` module compiles and imports cleanly.

### The J2855 Investigation

**Not yet started.** Max just dropped the task in the last turn of the transcript. We know:
- The image is called J2855 (likely a job ID or filename from the MOMA pipeline)
- It was visible in Windows Photos and is now gone
- Max uses Photos for manual crop + review before feeding into media-kit sessions
- He asked to "investigate" why it disappeared

---

## CURRENT STATE

**Guards - fully deployed:**
- `paths.py` v10 with the hard gate (committed master `d74cc17`)
- `moma_image.py` created as the canonical entry point
- Both fire scripts refactored to use `fire_image`
- `C:/moma/CLAUDE.md` updated with the standard-way section
- Broadcast posted to sibling sessions via bcast

**Media-kit images - complete and untouched:**
- 18 portraits: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\media_kit\output\` (flat folder)
- 6 rainbow variations: `...\media_kit\rainbow_variations\`
- These were the product of D50/D57's work and are not related to the J2855 issue except that they share the same pipeline.

**J2855 - zero progress:**
- No investigation has been done yet
- No file search performed
- Don't know if J2855 is in the KAZARIAN_ROOT, the Windows Photos database, or somewhere else
- The task was stated in the very last user prompt of the transcript, which immediately precedes this handover

---

## EXACT NEXT STEP

1. **Clock in as D59** on the board (replace the old D57 identity).
2. **Investigate J2855.** First, search for it:
   - In the MOMA D1 database (`jobs` table - look for job ID containing or matching "J2855")
   - On disk under `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\` (KAZARIAN_ROOT)
   - In the Windows Photos app's own database (likely `%LOCALAPPDATA%\Packages\Microsoft.Windows.Photos_*\LocalState\` or similar)
   - In `C:\Users\maxre\OneDrive\Pictures\` and `C:\Users\maxre\Downloads\`
3. **Determine what J2855 IS** - a MOMA job? A rendered frame? A raw photo Max cropped? The name suggests it could be a job ID (MOMA jobs follow a pattern, though J2855 might be a frame number or something else).
4. **Trace why it disappeared** - was it deleted by a MOMA process? Moved? Windows Photos index corruption? Something D51's MOMA troubleshooting did? (D51 was troubleshooting MOMA while D57 ran images - it killed python processes at least once.)

---

## OPEN QUESTIONS (for Max, when appropriate)

- Is J2855 an image file on disk, or just a thumbnail in the Photos app?
- Was it one of the media-kit outputs D57 just produced, or an older image from before this session?
- Do you know any more about J2855 - is it a job name, a filename, a frame number?
- Did the disappearance happen during this session (while D50/D57 and D51 were both active) or earlier?

---

## KEY PATHS & IDENTIFIERS

| What | Path/Value |
|---|---|
| MOMA code root | `C:\moma` (GitHub maxrempel/moma, master branch) |
| Combo runner code | `C:\moma\sc10\combo_runner\code\` |
| The new guard gate | `C:\moma\sc10\combo_runner\code\paths.py` (v10) |
| The canonical fire helper | `C:\moma\sc10\combo_runner\code\moma_image.py` |
| MOMA project instructions | `C:\moma\CLAUDE.md` (has the new standard-way section) |
| Media-kit portrait script | `C:\moma\sc10\combo_runner\code\fire_mediakit_portrait.py` |
| Rainbow variations script | `C:\moma\sc10\combo_runner\code\fire_rainbow_variations.py` |
| Image output root | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\` (KAZARIAN_ROOT) |
| Media-kit outputs | `...\kazarian_episode\media_kit\output\` (18 .png) |
| Rainbow outputs | `...\kazarian_episode\media_kit\rainbow_variations\` (6 .png) |
| Headshot A (dnavibe) | `C:\Users\maxre\OneDrive\Pictures\max rempel max port 2026 dnavibe.jpg` |
| Headshot B (2023) | `C:\Users\maxre\OneDrive\Pictures\max port 2023.JPG` |
| Rainbow reference | `C:\Users\maxre\Downloads\rainbow.jpg` |
| Compaction KB / memory | `C:\Users\maxre\.claude\projects\C--claude-base\memory\` |
| No-parallelize memory | `...\memory\feedback_no_parallel_image_api.md` |
| MOMA D1 database | Cloudflare D1 via REST (`moma_db.D1Client`) |
| Guard commit | `d74cc17` on master (pushed) |
| Session identity | Was D50 ? D57; now tasked to clock in as **D59** |
| Sibling D51 | Was doing MOMA troubleshooting during D57's image run |
| Current worktree | `C:\claude_base\.claude\worktrees\funny-torvalds-1f92dc` |

---

## GOTCHAS & DEAD ENDS

1. **Do NOT parallelize image API calls.** Ever. Max was explicit and wrote it to memory. Sequential only. The `moma_image.fire_image` helper is sequential by design.

2. **Medium/high quality will be blocked by the new gate.** If a future session wants those, Max must deliberately set the env var. This is by design - it's the lock working.

3. **The combo worker is NOT affected by the gate.** The movie pipeline (`combo_worker.py:115`) uses pure defaults and never calls `check_image_params`. It will keep working unchanged.

4. **D51's troubleshooting may have side effects.** D51 was active during D57's image runs - it killed python processes at least once (D57 had to resume after fire process died). If J2855 disappeared during that window, D51's actions are a suspect.

5. **The Windows Photos app database is separate from the file system.** An image can exist on disk but disappear from Photos if the app's index/catalog gets corrupted or if the file is moved outside its monitored folders. Don't assume J2855 is deleted just because Photos can't see it.

6. **Python stdout redirection is block-buffered.** Log files written by background processes may appear empty until the process exits. Use `tail` on the log, not `cat`, or check filesystem for output PNGs to gauge progress.

7. **Cost table estimate for portrait was fixed.** Before v10, portrait `1024x1536` returned $0.25 estimate (the code fell through to the default). Now it returns correct values.
