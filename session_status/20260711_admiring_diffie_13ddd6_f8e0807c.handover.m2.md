# Scribe handover - milestone 2 (~162K tokens)
# session: 20260711_admiring_diffie_13ddd6_f8e0807c
# cwd: C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6
# written: 2026-07-11 18:19:14 by deepseek-v4-pro

# HANDOVER - Starseed Genetics website update: switch to sequencing.com & relaxed family rules

## GOAL (in Max's own words)

Max said:
- "Update Starseed Genetics as soon as possible, back it up and update one thing."
- "We just switched from 23andMe to sequencing.com from $100 to $400 at sequencing.com, full genome sequencing."
- "And we dropped the requirement for the kids to be an adult. We can take kids of any age with parental consent. And we are taking individuals and single parent, one child, and both parents, one child. So, all versions."
- "Update the front page primarily and then we'll go for the other pages. Just do that quick because we need it fast."

## DECISIONS MADE + WHY

1. **Only the home page was edited** - The user explicitly said "front page primarily and then we'll go for the other pages". The assistant followed that instruction, did the front page only, and then stopped to ask about the rest.

2. **Source of truth identified** - The site is a single Cloudflare Worker at `C:\claude_base\sites\starseed-site\src\worker.js` (1,274 lines). Its deploy script (`deploy.sh`) uses `wrangler deploy`. The worker name is `starseed-site`. Custom domains (`starseedgenetics.com` / `ru.starseedgenetics.com`) are attached to this worker.

3. **Backup before editing** - The old production worker code was saved to `C:\claude_base\backups\cf_workers\starseed-site\history\worker_backup_2025...js` before any changes.

4. **What specifically changed on the home page**:
   - **Participate section (EN & RU)**: Removed the "complete families (both parents + adult child)" restriction and the adult age requirement. Replaced the old $99 23andMe genotyping text with a mention of full-genome sequencing through sequencing.com at $400 per person. Removed the three-tier genotyping/short-read/long-read price list.
   - **Instructions section (EN & RU)**: Rewritten to describe the sequencing.com flow: order kit from sequencing.com, brush cheek, mail it, send Max a photo of the box code. Removed the "adult child, 18+" requirement entirely. Added that kids of any age are accepted with parental consent. Also expanded the family configurations: individual, one parent + child, both parents + child, or larger family.

5. **Bilingual handling** - The worker file contains both English and Russian strings inline. Both languages were updated in parallel. Verified that both `starseedgenetics.com` and `ru.starseedgenetics.com` serve the new content.

6. **Deployment** - Changes deployed via `bash deploy.sh`, which runs `npx wrangler deploy`. The assistant then verified live bytes with `curl` (bypassing web fetch cache). Successful.

7. **Git** - Changes committed to branch `claude1/gracious-turing-72ae8e` and merged into `master` per Max's always-merge-push rule.

## CURRENT STATE

- The home page of `starseedgenetics.com` (EN) and `ru.starseedgenetics.com` (RU) is **live, updated, verified**.
- The source file `C:\claude_base\sites\starseed-site\src\worker.js` has been edited (lines around the Participate/Instructions sections; specific edits made via Edit tool).
- The backup of the old live worker is saved at `C:\claude_base\backups\cf_workers\starseed-site\history\worker_backup_<timestamp>.js`.
- The assistant **explicitly flagged** that other pages still contain old language, and **asked Max whether to update those next**. Max has not yet responded.

## EXACT NEXT STEP

The immediate next action the assistant proposed was: update the **Register** and **Forwarding** pages, because:

- **Register page** still says "full families, adult child, all 18+".
- **Forwarding page** still is all about exporting 23andMe data.

The assistant asked: "Want me to update those next, or hold?"

So the very next step for a cold session is to **wait for Max's answer on that question** (or, if Max instructs to continue, edit those remaining pages in the same worker file, deploy, and commit). Do NOT proceed without explicit go-ahead, because the user said "front page primarily and then we'll go for the other pages" - the "then we'll go" was conditional on finishing the front page first, and the assistant paused to check.

## OPEN QUESTIONS

1. **Should the Register page be updated now?** (It still reflects old family/adult requirements.)
2. **Should the Forwarding page be updated now?** (It still talks about 23andMe data export.)
3. **Any changes to the DNA analysis submission flow page?** (Not mentioned, but worth asking if anything else needs changing.)
4. **Is the sequencing.com kit price exactly $400?** The user said "$400 at sequencing.com" - but in the code we placed "about $400". Confirm if exact price should be stated or left as approximate.

## KEY FILE PATHS, IDs, & COMMANDS

- **Source file**: `C:\claude_base\sites\starseed-site\src\worker.js`
- **Deploy script**: `C:\claude_base\sites\starseed-site\deploy.sh`
- **Backup directory**: `C:\claude_base\backups\cf_workers\starseed-site\history\`
- **Live site EN**: `https://starseedgenetics.com`
- **Live site RU**: `https://ru.starseedgenetics.com`
- **Cloudflare Worker name**: `starseed-site`
- **Git repo**: located at `C:\claude_base` with the site inside `sites/starseed-site/`
- **Verify live content (bypass cache)**: `curl -s "https://starseedgenetics.com/?cb=$RANDOM" | grep -i "sequencing.com"` etc.
- **Wrangler deploy**: `npx wrangler deploy` (run from within `C:\claude_base\sites\starseed-site`)

## GOTCHAS & DEAD ENDS

- **WebFetch caches for 15 minutes** - When the assistant used `WebFetch` to check the site, it returned stale content. They had to use raw `curl` with a random query string to see the real current version. Do not rely on WebFetch for verification; use `curl` or similar.
- **The worker is a bundled single file** - There's no React/Vue app; the entire site logic and HTML are in `worker.js`. Edits must be careful to preserve the inline bilingual structure and page router logic.
- **The page routing is based on path matching** - The home page corresponds to the function that handles `/` and `/index`. When editing other pages, locate the function for that path (e.g., `/register`, `/forwarding`). Use `grep -n` to find relevant page sections.
- **No separate template engine** - HTML is built with string concatenation. When changing the "who we accept" lists, note that both EN and RU versions are separate variables (e.g., `participateHTML`, `participateRU`). Both must be updated.
- **Deploy is instantaneous** - After `wrangler deploy`, the live site updates within seconds. Verify both language domains.
- **Git merge-push rule** - After any commit, the assistant always merges into `master` and pushes. Do the same.
- **The assistant never edited the Register/Forwarding pages** - So the cold session should not assume they were done; they are still pending unless Max says skip.

## END OF HANDOVER
