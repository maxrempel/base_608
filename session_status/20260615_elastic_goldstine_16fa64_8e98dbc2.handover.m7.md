# Scribe handover - milestone 7 (~107K tokens)
# session: 20260615_elastic_goldstine_16fa64_8e98dbc2
# cwd: C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64
# written: 2026-06-15 08:47:44 by deepseek-v4-pro

# HANDOVER - B12: rename Top?20 headings on kartoteka page

## GOAL (in Max's own words)
> **just rename the titles to /???-20 ??????? ?? ?????????? ??????????/**

(Implicit: do the same for performers - "???-20 ???????????? ?? ?????????? ??????????".)

## DECISIONS + WHY
- The earlier investigation into expanding author names (initials ? full) was overruled. Max clarified he only wants the heading text changed, not the author-name data. The assistant must **not** touch the author-name expansion.
- The assistant already confirmed that the Top?20 lists exist on the live site and are already sorted by performance count; the only missing piece is the complete descriptive heading.

## CURRENT STATE
- Live page at `https://tamza.com/kartoteka` currently displays:
  - "???-20 ????????????" (full names, counts)
  - "???-20 ???????" (initials, counts)
- The headings are hard?coded in `app.js` (the file served from `wp-content/kartoteka/app.js`), probably around lines 270?280.
- The local working copy that can be edited is:
  `C:\claude_base\tools\tamza_songs\pipeline\output\app.js`
- The assistant has **not** made any code changes yet.

## EXACT NEXT STEP
1. **Locate** the two heading strings in `output/app.js` - likely `"???-20 ???????"` and `"???-20 ????????????"` (or similar).
2. **Replace** them with:
   - `"???-20 ??????? ?? ?????????? ??????????"`
   - `"???-20 ???????????? ?? ?????????? ??????????"`
3. **Deploy** the updated `app.js` to the live CDN using:
   `python C:/claude_base/tools/tamza_songs/pipeline/scripts/deploy_catalog.py`
   (This script uploads `output/app.js` to R2; ensure any required credentials/env are set - consult the script's docstring or previous runs.)
4. **Verify** on `https://tamza.com/kartoteka` that both headings now read correctly.

## OPEN QUESTIONS
- None. The user's last instruction is unambiguous: change only the titles, nothing else.

## KEY PATHS / IDS
- Local app.js (edit target):  
  `C:\claude_base\tools\tamza_songs\pipeline\output\app.js`
- Live app.js (served on site):  
  `https://tamza.com/wp-content/kartoteka/app.js`
- Deploy script:  
  `C:\claude_base\tools\tamza_songs\pipeline\scripts\deploy_catalog.py`
- Branch bulletin identity: **B12** (`python "C:/claude_base/branch_bulletin/bcast.py" whoami b12`)

## GOTCHAS / DEAD ENDS RULED OUT
- Do **not** expand author names (initials ? full names). That rabbit hole was explicitly closed by Max.
- The page may cache aggressively; a hard refresh or cache-buster (`?v=` query) might be needed after deploy.
- If `deploy_catalog.py` requires arguments (e.g., AWS profile, bucket name), double?check its `if __name__` block. A quick `python deploy_catalog.py --help` or reading the script can clarify.
- The assistant previously confirmed that the performer heading does not already include "?? ?????????? ??????????" - it was just "???-20 ????????????". So both headings need updating.
