# Scribe handover - milestone 4 (~318K tokens)
# session: 20260711_admiring_diffie_13ddd6_f8e0807c
# cwd: C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6
# written: 2026-07-11 23:25:55 by deepseek-v4-pro

# Handover - Starseed Genetics Website Overhaul + Blog Posts

## GOAL (in Max's own words)
Update the entire Starseed Genetics site and publish blog posts so that there is **one unified pitch**: people order a 30? WGS kit from sequencing.com for ~$379, brush inside their cheek, send us the data, we analyse free and return all findings. No more 23andMe, no long?read fundraising, no $6,000 PacBio trio campaign. Individuals, pairs, families - all accepted, kids of any age with parental consent. Also hide the old 23andMe forwarding page and remove every trace of the obsolete tiers.

## DECISIONS + WHY

1. **Switched from 23andMe to sequencing.com**
   - Reason: Max decided to use full?genome sequencing (30? WGS) instead of genotyping. Real price from sequencing.com site is $379, verbatim.
   - Site now says "about $379 per person" in EN/RU, all instructions refer to sequencing.com flow.

2. **Dropped adult?child, "complete families only" requirement**
   - Now any individual, parent?child pair, or full trio can join. Kids of any age with parental consent.
   - Reason: wider inclusion, simpler message.

3. **Collection method wording verbatim: "brushing inside the cheek"**
   - Changed everywhere from "cheek swab" / "genotyping kit" etc. Exactly as Max dictated.
   - Participants send a photo of the **labeled tube** with the sample code, not the box code.

4. **New headline + framing**
   - Home headline: "Check for traces of alien genetic manipulation in your DNA"
   - Sidebar button: "Submit your DNA data" (we accept data, not physical DNA).
   - Old "Send us your DNA" removed.
   - Primary message now invitation to sequence, not the $6K fundraiser.

5. **Purged ALL long?read / $6,000 / PacBio / genotyping / 23andMe references**
   - Deleted the $6,000 fundraiser narrative, the long?read update, and the "genotyping has reached its limit" text.
   - Removed the 23andMe forwarding page entirely (route + function).
   - Donate page no longer shows a $6,000 goal bar - it still records $605 received but reframes donations as helping families afford sequencing.
   - Glossary/footer references to long?read removed.
   - Reason: Max explicitly said "forget the long reads. We are just one pitch now."

6. **Live age counter on home page**
   - Project start changed to July 2024, and a JavaScript counter shows "X.xxxxxxxx years and counting" ticking every second. Fallback static value 2.0.
   - Fundraising update date on Donate page now auto?rolls to today's date daily via JS.

7. **Forwarding page hidden**
   - Removed from Links page and menus; only a quiet link in Updates (which itself was later removed when the whole Updates page was rewritten). Now completely gone.

8. **Blog posts published on maxrempel.com**
   - Two posts inserted into D1 `blog_posts` table, both English.
   - Post 1 ("Starseed Genetics Project Update"): published verbatim, no price changes.
   - Post 2 ("You Are an Alien Hybrid, and We Can Look"): published with the one factual correction - outdated "photo of the code on the box" replaced by "whole?genome sequencing kit from sequencing.com ... photo of the labeled tube with its sample code".
   - Neither post contained long?read or $6,000 content, so they are already consistent.

## CURRENT STATE

- **StarseedGenetics.com worker (`starseed-site`)**: fully updated source at `C:\claude_base\sites\starseed-site\src\worker.js`, deployed to Cloudflare. All pages (Home, Register, Consent, Updates, Donate) reflect the single?pitch, $379 sequencing.com flow. No long?read, no 23andMe, no genotyping tiers.
- **maxrempel.com blog**: two new posts live, slugged:
  - `starseed-genetics-project-update-2026-07`
  - `you-are-an-alien-hybrid-and-we-can-look`
- **Git**: all changes committed on branch `claude1/gracious-turing-72ae8e` (in worktree `admiring-diffie-13ddd6`), then merged to `master` and pushed.
- **Backups**: old live worker backed up to `C:\claude_base\backups\cf_workers\starseed-site\history` before editing.

## OPEN QUESTIONS
None left. Max's last correction - purge long?read everywhere - was executed completely. The handover note about "the cost is $6,000..." was a leftover that he immediately corrected; the site already reflects the $379, short?read?only pitch.

## KEY PATHS / IDS / COMMANDS

- **Website source**: `C:\claude_base\sites\starseed-site\src\worker.js`
- **Deploy script**: `C:\claude_base\sites\starseed-site\deploy.sh` (runs `wrangler deploy` for worker `starseed-site`)
- **Live domains**: `starseedgenetics.com`, `ru.starseedgenetics.com`
- **Blog site source**: `C:\claude_base\sites\maxrempel-site\src\blog.js`
- **Blog database**: Cloudflare D1, database ID `...` (referenced via MCP tool `d1_database_query` on database `maxrempel-site-db`, table `blog_posts`)
- **Cloudflare API**: worker listing via MCP tool `workers_list`, worker code fetch via `workers_get_worker_code`, D1 queries via `d1_database_query`
- **Git worktree**: `C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6`
- **Backup dir**: `C:\claude_base\backups\cf_workers\starseed-site\history`

## GOTCHAS

- Edge cache on starseedgenetics.com is aggressive; after deploy you often need to add random query params (`?cb=$RANDOM`) and set `Cache-Control: no-cache` to verify the fresh version.
- The Russian translation lives in the same worker file, so every edit must be mirrored for both languages.
- The old forwarding page route (`/forwarding`) was fully removed; navigating there now gives a 404 "Page not found" (verified).
- The only dollar figure still present is the factual "$605 received" on the Donate page - intentional, not a leftover.
- No changes were needed to the maxrempel.com worker itself; blog posts go directly into the D1 database using the MCP query tool, no redeploy required.

## EXACT NEXT STEP (if a cold session resumes)
None. All tasks are complete. The site is live and consistent, and the blog posts are published. The next conversation would likely start with Max's new instructions.
