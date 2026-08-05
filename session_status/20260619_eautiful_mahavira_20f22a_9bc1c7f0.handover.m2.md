# Scribe handover - milestone 2 (~156K tokens)
# session: 20260619_eautiful_mahavira_20f22a_9bc1c7f0
# cwd: C:\moma\.claude\worktrees\beautiful-mahavira-20f22a
# written: 2026-06-19 18:29:53 by deepseek-v4-pro

# HANDOVER - D31 Fixer Session

---

## GOAL (in Max's words)

Spot 1 on the storyboard went empty even though a perfect reel was there an hour ago. Fix it so the functions just work. He's not a programmer and doesn't care about internals - he just needs expected behavior.

---

## DECISIONS + WHY

### 1. Root cause identified: wrong reels pinned to spot 1
Spot 1 (script lines 0-3) was pinned to:
- **J585** on lines 0-2 (an old single-line reel, no membership record in D21's map)
- **J2826** on line 3 (a "walk-to-camera" experiment, only belongs to line 3)

D30's new strict v2 filter (commit aee1269) requires every reel in a spot to have membership data that exactly matches the spot's lines. J585 and J2826 both lack proper 4-line membership for spot 1, so the filter correctly ejected them - leaving the spot empty.

The correct reel, **2774**, was never pinned to spot 1.

### 2. Fix applied: re-pinned spot 1 to reel 2774
Used the server's `/api/storyboard/assign` endpoint to pin lines 0-3 to reel 2774 (hash `2fcce2b861d639` etc.). 2774 is the approved 4-line greeting reel and matches D21's authoritative membership map (lines [0,1,2,3], approved).

### 3. Collateral damage caught and repaired
The `/api/storyboard/assign` endpoint has a systemic bug (D21 flagged it earlier): every assign call **secretly rewrites the reel's own `line_hash`** in the jobs table to the last line it touched. So my 4 assign calls corrupted 2774's identity:
- `line_hash` got overwritten to line 3's hash (`6beb37625a0e97`)
- `vocal_line` also got scrambled

This was repaired by directly updating D1's jobs table to restore 2774's correct `line_hash` and `vocal_line` (using its intact `birth_line_hash` = `m8df5135e0702c` as reference, which follows the convention other merged reels use).

### 4. Systemic bug identified - NOT yet fixed
The same `/api/storyboard/assign` handler in `slideshow_server_v01.py` (lines 1388-1405) is the deeper cause. Every pin operation silently mutates the reel's own job identity. This is why reels keep falling out of spots. D31 posted to the board asking whether the mixboard still depends on this behavior before removing it, because D21/D24/D30 share that file.

---

## CURRENT STATE

- **Spot 1 renders correctly** - verified in browser via Playwright screenshot (`d31_spot1_fixed.png`). groupLines returns reel 2774 for lines 0-3.
- **2774's job identity is restored** - `line_hash` back to `m8df5135e0702c`.
- **The `/api/storyboard/assign` bug is NOT fixed** - the secret line_hash rewrite is still live in the server code. Asked teammates on the board whether it can be removed safely.

---

## EXACT NEXT STEP

Consult with D21/D24/D30 on the branch bulletin board. Once they confirm the mixboard no longer depends on the secret line_hash rewrite in `/api/storyboard/assign`, remove that mutation from `slideshow_server_v01.py` (lines ~1388-1405 where `jobs.line_hash` gets overwritten during pin operations). Then push the code fix.

---

## OPEN QUESTIONS

- **Does the mixboard (or any other consumer) still rely on `/api/storyboard/assign` rewriting `jobs.line_hash`?** D31 asked this on the board. No reply yet. Until that's confirmed, the erase is on hold.

---

## KEY PATHS / IDS

| Thing | Value |
|---|---|
| Reel 2774 (greeting, spot 1) | lines [0,1,2,3], approved, membership in `d21_merge_membership_20260619_172144.json` |
| 2774 birth_line_hash | `m8df5135e0702c` |
| 2774 restored line_hash | `m8df5135e0702c` |
| J585 (wrong, old single reel) | no membership record |
| J2826 (wrong, walk experiment) | only line 3 |
| Buggy endpoint handler | `sc10/sound_assembly/code/slideshow_server_v01.py` lines ~1388-1405 |
| Storyboard v2 file | `sc10/sound_assembly/code/storyboard_editor_v2.html` |
| D21 membership map | `sc10/combo_runner/code/local_state/d21_merge_membership_20260619_172144.json` |
| Board | `python "C:/claude_base/branch_bulletin/bcast.py"` |
| Worklog | `python "C:/claude_base/compaction_kb/scripts/worklog.py"` |
| v2 strict filter commit | `aee1269` |
| Server URL | `http://localhost:8790` |
| Storyboard v2 route | `/storyboard2` |
| Assign API | `/api/storyboard/assign` |
| State API | `/api/storyboard_state_v2` |

---

## GOTCHAS

- **Any assign call silently corrupts the reel's own line_hash.** This is the systemic bug. Until the server code is patched, every pin operation risks scrambling reel identities. If you must assign again, always check and restore the reel's `line_hash` via direct D1 SQL afterward.
- **Max cannot read non-highlighted content.** He doesn't understand "secret rewrite" - he just wants functions to work. Don't explain internals to him unless he asks. Fix silently and confirm the visible result.
- **D21 warned about this bug earlier.** The assign handler rewriting `jobs.line_hash` is known but unfixed. Teammates share the server file, so changes need coordination.
- **The filter itself is correct.** D30's strict membership check isn't wrong - it just exposed that the wrong reels were pinned. The fix was re-pinning to the correct reel, not relaxing the filter.
