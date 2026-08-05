# Scribe handover - milestone 2 (~166K tokens)
# session: 20260624_ptimistic_germain_f69be6_8ec57f54
# cwd: C:\moma\.claude\worktrees\optimistic-germain-f69be6
# written: 2026-06-24 14:15:32 by deepseek-v4-pro

# HANDOVER - D43: sc10 spot2 + spot9 fixes (COMPLETE)

---

## GOAL (Max's words)

1. **spot2 (L04-L05):** "There was a good lipsie for sc10 spot2 L04-L05 lh=f8806da07fc6d8 spine=(empty) but after redesign of filtering it got filtered out. Fish it out, it was the latest one and reclassify to bring it back to sb."
2. **spot9 (L24-L28):** "Also this one is missing sc10 spot9 L24-L28 lh=5f7e72930d36c6 spine=J444 And I'm not sure if that was a good Lipsy, but I would suspect that was a good Lipsy for that." Later sent a screenshot showing spot9 as "merged 5 lines, L24-L28" pinned to image J444 and said **"The reel is absent."**

Both are now fixed and verified.

---

## DECISIONS + WHY

### spot2 - Reclassify, not re-fire

J2835 (approved, lip_rating=5, the latest reel for the L04-L05 span) was the good merged reel but its `line_hash` had been corrupted to L05's single hash (446df00dc11f2c) instead of the merge hash - the known pin-rewrite bug. The new filter couldn't see it as a merged spot and hid it.

**Decision:** Register the merge canonically and re-tag the existing reel (data-only, no D1 code changes). Chose this over re-firing a fresh reel because J2835 was already approved with perfect lip sync and contained both current lines (verified via Deepgram transcription - "measure, don't trust labels").

**Actions taken:**
- Called `register_merge.register(10, ['f8806da07fc6d8','446df00dc11f2c'], 'D43', ...)` ? minted merge_hash `sp94849a807a77`
- Updated J2835: `line_hash` and `birth_line_hash` ? `sp94849a807a77`, vocal_line ? merged dialogue text
- Repointed `line_current_clip`: deleted stale single-line pins (f8806?2835, 446df?2835), inserted one pin for sp94849a807a77 ? job_id 2835
- Verified: merge_ops resolves to idxs [4,5], J2835 derives to [4,5]
- Data-only fix - live in D1 immediately, no code to push

### spot9 - Junk-guard the layout derivation (code fix)

Two obsolete **junk** reels (2783, 2789) from an earlier merge attempt had `vocal_line` containing the literal text `[24, 25, 26, 27, 28]`. The storyboard layout builder (`slideshow_server_v01.py`, endpoint `/api/reel_membership_sc10`) derives spot geometry from four sources. Two of them - Source A (D21 seed file, keyed by job_id) and Source C (regex on vocal_line) - had **no junk/status filter**, so dead reels were secretly fabricating a 5-line spot9 that no approved 4-line reel could match. The canonical data was already correct: `sp7a518eeb5e90` = L24-L27 (active, reel 2935 approved), `sp109ddb58dbea` = L28-L29 (spot10).

**Decision:** Add a junk-status guard to Sources A and C in the membership derivation, not just patch the seed or mute the two reels' vocal_line. This is a root-cause, class-wide fix: dead/junk reels must never define spot geometry. Aligned with D40's ongoing supersede work (which already guarded Sources B and B2). Also hardened the guard to catch both `'junk'` and `'junked'` (two variant spellings exist in the DB).

**Actions taken:**
- Edited `slideshow_server_v01.py` (3 edits): added `output_status` to the reels SQL query; built `jid2status` map; skip junk in Source A (seed loop) and Source C (regex loop) via `jid2status.get(id,'').startswith('junk')`
- Committed (5951ffe then cf7bb20 for hardening), pushed to master
- Restarted slideshow_server on port 8790 (killed old PID 20164, launched new detached process ? PID 38040)
- Verified live: no more [24,25,26,27,28] span; spot9 derives to [24,25,26,27] filled by approved reel 2935
- Archived my earlier failed seed-only attempt (`d21_merge_membership_20260624_093830.json` ? `local_state/archive/`) - the code guard makes it unnecessary
- Cleaned all `_d43_*.py` scratch files

### Rejected approach

A seed-only fix (removing entries 2783/2789 from the D21 seed) was tried first and **failed** - Source C regex re-derived the 5-line span from those reels' `vocal_line` regardless of seed contents. Demoting the seed wholesale was rejected because it's still load-bearing for many pre-D44 non-canonical merges (m-prefixed hashes not in merge_ops).

---

## CURRENT STATE

**Both spots are fixed and verified on the live server.** Master is at commit `cf7bb20` (pushed to origin/master). The slideshow_server on port 8790 (PID 38040) is running the fixed code.

**spot2:** J2835 (approved) fills the L04-L05 merged spot. Merge `sp94849a807a77` registered in merge_ops (op_id 11).

**spot9:** 4 lines (L24-L27), filled by approved reel 2935. Lines are:
- L24 ANNA: "One coalition for eight billion people?"
- L25 ISHTAB: "That's the requirement."
- L26 ANNA: "But what is the reason for it?"
- L27 ISHTAB: "Experience."

L28 ("Could you explain?") belongs to spot10 (L28-L29).

**Worktree state** (C:\moma, branch master, worktree keen-lumiere-644969):
- 2 unrelated modified tracked files exist (NOT mine - left untouched): `fire_mediakit_portrait.py` (+27), `render_mixboard_video_v01.py` (substantial changes). These belong to prior-session work in this worktree.
- All `_d43_*.py` scratch files deleted.
- Archived seed: `local_state/archive/obsolete_d21_merge_membership_20260624_093830_d43_failed_seedonly_attempt.json`
- Active seed: `local_state/d21_merge_membership_20260619_172144.json` (pristine original)

---

## EXACT NEXT STEP

Nothing. Both tasks are complete. Max's last question ("does it match the lines?") was answered - spot9 is 4 lines, reel 2935 matches exactly. If Max confirms the storyboard looks correct after refresh, this session can close.

If spot9 still looks wrong after refresh, the most likely cause is a stale frontend cache (the slideshow_server was restarted; the frontend reads from it live, but a browser hard-refresh may be needed).

---

## OPEN QUESTIONS

None. Both tasks delivered per spec.

---

## KEY PATHS / IDS

- **Repo:** `C:\moma` (main checkout, branch master, worktree `keen-lumiere-644969`)
- **Edited file:** `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (commits 5951ffe, cf7bb20)
- **Live server:** port 8790, PID 38040 (pythonw.exe), serves from `C:\moma\sc10\sound_assembly\code\`
- **Seed dir (hardcoded in server):** `C:\moma\sc10\combo_runner\code\local_state\`
- **Canonical merge entry point:** `C:\moma\sc10\combo_runner\code\register_merge.py`
- **D1 live DB:** accessed via `C:\moma\sc10\combo_runner\code\moma_db.py` (D1Client)
- **spot2 merge_hash:** `sp94849a807a77` (L04 + L05), op_id 11
- **spot2 reel:** J2835 (approved, lip_rating=5, file `sc10_lipsie_v2835_wan26flau.mp4`)
- **spot9 merge_hash:** `sp7a518eeb5e90` (L24-L27), active
- **spot9 reel:** J2935 (approved, lip_rating=3)
- **spot10 merge_hash:** `sp109ddb58dbea` (L28-L29), active
- **Junk reels causing spot9 bug:** 2783, 2789 (output_status='junk', vocal_line contains `[24, 25, 26, 27, 28]`)
- **Deepgram key:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/deepgram_key_20260515.txt`
- **Output lipsies dir:** `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/scenes/scene10_images/combo_runner/data/output_lipsies/`
- **bcast board:** `C:/claude_base/branch_bulletin/bcast.py`

---

## GOTCHAS

- **D43 name collision on bcast:** Two sessions claimed D43 (one was "D30recoder", I am the "was b6" one per Max's assignment). If another D43 wakes up, this needs untangling.
- **Two junk spellings in the DB:** `'junk'` (72 rows) and `'junked'` (2 rows). The guard uses `.startswith('junk')` to catch both. If anyone adds a third spelling, the guard won't catch it.
- **D40 owns slideshow_server_v01.py** - I coordinated via bcast before editing. D40 was actively reshaping spot9 (splitting L28 out) and adding supersede support. My fix (junk-guard on Sources A/C) complements their B/B2 supersede guards and does not conflict.
- **Hardcoded paths in slideshow_server:** The server hardcodes `C:\moma\sc10\combo_runner\code\local_state` for the seed dir. If the server is ever run from a different worktree or checkout, the seed won't be found.
- **My earlier wrong board post (09:30 "spot9 no fix needed"):** I posted a correction, but if Max or D40 saw only the original post they may think spot9 was fine. The correction post is live on bcast.
- **The 2 unrelated modified files in the worktree:** `fire_mediakit_portrait.py` and `render_mixboard_video_v01.py` have substantial uncommitted changes. I deliberately excluded them from my commits. If a future session commits from this worktree, they'll need to decide whether to include or discard those changes.
- **Seed archive is reversible:** `local_state/archive/obsolete_d21_merge_membership_20260624_093830_d43_failed_seedonly_attempt.json` can be deleted or restored. The code guard makes it unnecessary, but it's there if needed for archaeology.
- **Slideshow_server restart pattern:** Used `subprocess.Popen` with `creationflags=DETACHED_PROCESS` from a Python wrapper - NOT `start "" /B` (which triggers the B:\ drive popup). If the server needs another restart, use this pattern or `moma_restart.py`.
