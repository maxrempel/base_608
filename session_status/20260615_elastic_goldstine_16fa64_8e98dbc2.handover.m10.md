# Scribe handover - milestone 10 (~151K tokens)
# session: 20260615_elastic_goldstine_16fa64_8e98dbc2
# cwd: C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64
# written: 2026-06-15 09:14:40 by deepseek-v4-pro

# HANDOVER - B12: Kartoteka Top-20 Title Fix + Deploy Process Hardening

---

## GOAL (Max's exact words)

**Primary:** Rename the two Top-20 section headings on tamza.com/kartoteka so they read "???-20 ???????????? ?? ?????????? ??????????" and "???-20 ??????? ?? ?????????? ??????????" (adding "?? ?????????? ??????????" to each).

**Secondary (triggered by a deploy mishap):** Fix the process so a stale branch can never clobber a teammate's live deploy. Add pre-deploy guards to the catalog deployer.

**Tertiary (final Max prompt):** Make the process "negotiable" - allow a session to override any prohibition if it has the information, trusting Opus to decide. Max wants agency, not rigid blocks.

---

## DECISIONS MADE + WHY

### 1. Title-only change (not author-name expansion)
Max pasted a list of performers with counts, and an empty author list. Initially I thought the problem was author *names* showing as initials (?.????????) vs full performer names (?????? ?????? ???????). Max clarified: just rename the section *titles*, not the names inside. The lists already existed, were already ranked by performance count, and were already functional. Two heading strings changed. Done.

### 2. Deploying from the live file, not the worktree copy
My worktree branch was stale - it contained an older app.js missing b10's in-player "????????" button and lock-screen controls. First deploy briefly wiped those features. Caught it from a byte-size drop (42926 ? 40199 bytes). Rolled back by:
- Auto-backup of live file existed from the deploy script
- Applied only my two title edits onto the **live** file
- Redeployed the corrected live file

Lesson: never trust the worktree's copy of a shared file. Always pull live first.

### 3. Pre-deploy guards in deploy_catalog.py
Added two preflight checks to `tools/tamza_songs/pipeline/scripts/deploy_catalog.py`:
- **Git freshness check:** blocks deploy if local branch is behind origin/master (catches stale worktrees). Fails open if git fails.
- **Shrink guard:** blocks deploy if the new file is >1.5% smaller than live (catches accidental clobber of features a teammate added). Overridable with `--force`.

Pushed to master as commit af86de7c.

---

## CURRENT STATE

| Thing | Status |
|---|---|
| Top-20 headings live | **Done.** Both say "...?? ?????????? ??????????". Verified on tamza.com/kartoteka. |
| Author/performer lists | Already existed. Already ranked by performance count. No data changes needed. |
| In-player "????????" button (b10's work) | **Intact.** Restored after my stale-deploy regression. |
| Lock-screen/media-session controls (b10's work) | **Intact.** Same restoration. |
| Vote UI (b10's second push) | **Intact.** b10 built on my commit and redeployed. Both our changes survived. |
| deploy_catalog.py guards | **Live on master** (af86de7c). Stale-branch block + shrink block. `--force` overrides both. |
| publish_catalog.py (second deploy path) | **Not hardened yet.** No guards. Flagged to b7/b10 on the board. |
| Git master | Clean. My title edit + b10's vote edit merged without conflict (different lines). |
| Branch B12 worktree | Stale. The worktree app.js was an old copy. Cleaned up. |

---

## EXACT NEXT STEP

Max's final ask: **Make the deploy guards negotiable - Opus should be able to override any prohibition after reviewing the facts.**

This means modifying the guards so a Claude session (acting as an Opus-level agent) can:
1. Inspect the live file and the candidate file
2. Determine the shrink is intentional and safe
3. Proceed with `--force` or an equivalent bypass - WITHOUT a human having to manually type `--force`

**Next action:** Add a "negotiation" path to `deploy_catalog.py` (or the session workflow around it). Options:
- Make `--force` auto-supplied when a specific environment variable or marker file is present (session sets it after verifying)
- Add a `--opus-override` flag that requires a reason string but bypasses both guards
- Add a pre-check mode (`--dry-run` or `--audit`) that reports what would be blocked + why, then the session decides and re-runs with a bypass

Also unresolved: whether to port the same guards to `publish_catalog.py`. Max didn't answer this - left dangling.

---

## OPEN QUESTIONS AWAITING MAX

1. **Should I port the guards to publish_catalog.py?** Or does one deploy path suffice? (Asked, no answer yet.)
2. **What form should the "negotiable override" take?** Max wants Opus-level trust. Need to confirm: environment variable? Marker file? A `--trust-opus` flag that always works?
3. **Should the shrink threshold be configurable?** Currently hardcoded at 1.5%. May false-positive on legitimate reductions.

---

## KEY PATHS, IDs, COMMANDS

| What | Path/Value |
|---|---|
| Live catalog URL | `https://tamza.com/kartoteka` |
| Live app.js (R2) | `https://tamza.com/wp-content/kartoteka/app.js` |
| Live data.json (R2) | `https://tamza.com/wp-content/kartoteka/data.json` |
| Canonical app.js (master) | `C:\claude_base\tools\tamza_songs\pipeline\output\app.js` (672 lines) |
| Deploy script (guarded) | `C:\claude_base\tools\tamza_songs\pipeline\scripts\deploy_catalog.py` |
| Deploy script (unguarded) | `C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py` |
| B12's temp fix script (can delete) | `C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64\tools\tamza_songs\pipeline\_b12_fix_titles.py` |
| Git commits | `d2483eb2` (title edit), `af86de7c` (deploy guards) |
| Branch bulletin board | `python "C:/claude_base/branch_bulletin/bcast.py" post/catchup/whoami` |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| R2 bucket/auth | In `deploy_catalog.py` - uses boto3, endpoint_url + keys |
| The two lines edited | Lines near 274 (???-20 ??????? ? ???-20 ??????? ?? ?????????? ??????????) and its performer counterpart |

---

## GOTCHAS + DEAD ENDS ALREADY RULED OUT

1. **Do NOT deploy from a worktree's copy of app.js.** The worktree can be days stale. Always fetch the live file from R2 first, apply changes, then deploy - or rebase the worktree on master before editing. The shrink guard now catches this, but it's a last line of defense.

2. **Do NOT assume the worktree has latest master.** `deploy_catalog.py` now checks this, but `publish_catalog.py` does not. If anyone uses publish_catalog.py for app.js, the same regression can recur.

3. **Author names ARE initials in the data.** The `_aauth` field stores abbreviated forms (?.????????, ?.?.???????). This is a data-layer issue, not a display bug. If Max ever wants full author names, the fix is in `_aauth` generation in the pipeline, not in app.js.

4. **The two deploy scripts overlap.** `deploy_catalog.py` handles incremental deploys (app.js only, or data.json only). `publish_catalog.py` rebuilds everything. Both push to the same R2 paths. The guard is only in one. Until fixed, a `publish_catalog.py` run from a stale branch CAN still clobber live.

5. **Live page has ~5 minute cache.** Verifying via browser after deploy can show stale results. Direct curl of the R2 URL verifies instantly.
