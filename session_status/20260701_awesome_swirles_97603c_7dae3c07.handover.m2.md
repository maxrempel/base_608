# Scribe handover - milestone 2 (~166K tokens)
# session: 20260701_awesome_swirles_97603c_7dae3c07
# cwd: C:\moma\.claude\worktrees\awesome-swirles-97603c
# written: 2026-07-01 16:50:50 by deepseek-v4-pro

# Handover - D02A session: sc11 spot1 merged reel (L00?L01), corrected and awaiting review

## GOAL (Max's own words)

> "Okay, make a reel from that. sc11 spot1 L00?L01 lh=e3d6d39b36f10a spine=J3091"

After seeing the first result (J3097), Max gave four corrections:

1. **Anti?glamour** - portrait likeness lost, everyone "glamorized to a very high extent"  
2. **Ishtab's age** - she is about 70, but was rendered ~15; must stay elderly  
3. **One hand** - she was pointing two hands in different directions; should raise only ONE hand, toward Anna, introducing her to the men  
4. **Men rise** - "guys stand up when ladies approach ... ladies have to approach the table and guys stand up. That's the essential part." He was unsure the model could do it, but it must be in the prompt.

All four fixes applied in J3098. That reel is rendered and waiting on Max's review.

## DECISIONS + WHY

- **First fire (J3097)**  
  We used the canonical `fire_merge_lipsie` path. The storyboard `lh=` field gave the anchor line's hash, not the merge hash. Correct merge is `spd8ff62c3f575` (audio 14.45?s, under the ~15?s cap). Still: `sc11_arr02_v39.png` (spine J3091 approved). Prompt was constructed using **The Gesturing Protocol** for multi-turn merged reels (position list, speaker order, verbatim quotes, exclusivity clause, no?smile words). The prompt for J3097 was the baseline (see transcript).

- **Worker crash & resilience fix**  
  The wan26au worker had died on startup: `OSError: [WinError -2145452027] ... os.makedirs(LIPSYNC_TEMP, exist_ok=True)` because the `lipsync_temp` folder sits on Nextcloud and a placeholder blip made `makedirs` fail. The folder later materialised and the worker auto?recovered (pid 9984). I replaced the bare `os.makedirs` with a retry helper that survives the transient error, and committed the fix.

- **Corrections for J3098**  
  Anti?glamour: added "Keep every face EXACTLY as in the source image" + "matte skin, ... real pores, no makeup" + "soft haze filter on faces ... diffused light."  
  Elderly Ishtab: explicitly wrote "about seventy years old, aged face with wrinkles."  
  One hand: "she raises only ONE hand ... toward Anna; her other hand stays at her side."  
  Men rise: "as the ladies approach, both men rise to their feet from their chairs to greet them, standing up politely."

  **Rationale for re?fire instead of editing J3097:** MOMA's workflow re?renders from the same merge/still with a corrected prompt; we spine?pinned the new reel to keep the storyboard current.

- **Men?standing caveat**  
  The starting still shows everyone seated. i2v?flash starts from that frame, so a full stand?up motion is difficult. Max acknowledged the limitation but wants the prompt to push it as far as possible. If the result doesn't read, the next step would be a new still showing the ladies approaching / men half?risen.

## CURRENT STATE

- **Merged reel J3098 (sc11 spot1 corrected)** is **rendered** and spine?pinned.
- Output file exists: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\sc11_arr02_lipsie_v3098_wan26flau.mp4` (size ~7?MB).
- **Viewer link:** [J3098 on /lipser](http://localhost:8779/lipser?ids=3098&title=sc11%20spot1%20redo%20v2%20-%20antiglamour%2C%20Ishtab%20elderly%2C%20one%20hand%20to%20Anna%2C%20men%20rise%20as%20ladies%20approach)
- Max **has not yet reviewed** J3098. He just checked in as D02A (renamed from duplicate D56A).
- The wan26au worker is up and idle; its resilience fix is committed on branch `awesome-swirles-97603c`.
- No other open tasks or conflicts from the check?in.

## EXACT NEXT STEP

1. **Await Max's verdict on J3098.** He will likely open the /lipser link and decide whether the four fixes landed adequately.  
2. If he approves, the task is done.  
3. If further adjustments are needed (e.g., the men?stand motion failed, or Ishtab's age still off), the immediate action is to fire another corrected reel (J3099+) with an adjusted prompt, possibly using a new starting still that sets up the standing action better.

## OPEN QUESTIONS (awaiting Max)

- Does the "men rise" motion read at all from the seated still?  
- Is Ishtab's age now convincing?  
- Is the anti?glamour sufficient, or do faces still look over?beautified?  
- Is the single?hand gesture clear?

## KEY PATHS, IDs, NAMES

- **Canonical project doc:** `C:/Users/maxre/.claude/projects/C--moma/memory/project_wan26flau_lane.md` (contains The Gesturing Protocol)
- **Staging bible:** `C:\moma\memos\kazarian_staging_bible_tomemex.md`
- **Fire path:** `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py` (the sanctioned function)
- **Worker:** `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` (now with resilience fix)
- **DB access:** `moma_db.D1Client` (live Cloudflare D1)
- **Spine still:** `sc11_arr02_v39.png` (job J3091, arrangement 20)
- **Merge hash:** `spd8ff62c3f575` (lines0?1)
- **Line hashes:** L00 = `e3d6d39b36f10a` (Ishtab), L01 = another hash for Werner
- **Reel IDs:** J3097 (first, flawed), J3098 (corrected, current)
- **Scene identifiers:** sc11, rank?11, arrangement?20 (briefing at table)

**Viewer command pattern:**
```
http://localhost:8779/lipser?ids=<jobid>&title=...
```

## GOTCHAS & DEAD ENDS

- **Line hash ? merge hash.** The storyboard `lh=` field is the anchor line's hash; do NOT use it as the merge hash. We resolved to `spd8ff62c3f575` via `merges.json`.
- **Worker crash on Nextcloud placeholder.** The `os.makedirs(lipsync_temp)` call fails when the folder is an online?only placeholder. Fixed with a retry loop in `combo_wan26au_worker.py`. If the worker dies again, check that fix is applied (branch `awesome-swirles-97603c`, already committed via `git push`).
- **One arrangement = one spot, audio ?15?s.** J3098 stays under the cap.
- **The "men rise" motion is hard for i2v.** The model starts from a seated frame; Max is aware. If he wants a retake, the first move should be to generate a still with the men already half?standing / ladies approaching, then re?fire.
- **No D1 PRAGMA allowed.** All database schema inspection must use `SELECT * ... LIMIT 1` and read `.keys()`.
- **Temp scripts were deleted.** Diag and fire scripts (`_diag_spot1.py`, `_fire_spot1.py`, `_fire_spot1_v2.py`) were cleaned up after use.
