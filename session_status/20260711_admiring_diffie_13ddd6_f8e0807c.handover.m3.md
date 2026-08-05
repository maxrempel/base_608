# Scribe handover - milestone 3 (~226K tokens)
# session: 20260711_admiring_diffie_13ddd6_f8e0807c
# cwd: C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6
# written: 2026-07-11 18:35:47 by deepseek-v4-pro

# Handover: Starseed Genetics Site Update Session

## GOAL (in Max's own words)

- Switch the DNA collection method from 23andMe genotyping (?$100) to full?genome sequencing at sequencing.com (?$400/person).
- Drop the requirement that children must be adults; accept kids of any age with parental consent.
- Accept all family configurations: individuals, single parent + child, both parents + child (not just complete families).
- Update the project start date to July 2024 and show a live?running age counter (years with decimals) on the homepage.
- Hide the 23andMe forwarding helper page from menus and the public face; tuck it somewhere quiet.
- Change the main headline to focus on checking for traces of alien genetic manipulation, not the ?$6K fundraiser.
- Use the exact phrase "brushing inside the cheek" for collection method.
- Make clear that we accept DNA **sequence data** from sequencing.com, not physical DNA.
- Make the fundraising?update date on the Donate page auto?roll to today's date each day.

## DECISIONS + WHY

1. **Platform switch (23andMe ? sequencing.com full?genome)**  
   Max wants full?genome 30? coverage, not genotyping. The old price was ~?$100; the new price is ~?$400. The site must reflect this everywhere.

2. **All family configurations & all ages**  
   The project now accepts any family configuration (individual, one parent + child, both parents + child) and children of any age with parental consent. The old "adult child, 18+, complete families only" wording was removed from Register, Consent, and home page.

3. **Project start date: July 2024**  
   Max changed the start from "March 2025" to "July 2024." A live counter was added so the "X years and counting" number ticks every second with 8 decimals; a static "2.0" fallback exists for no?JS visitors. This was done on the homepage only.

4. **Collection wording: "brushing inside the cheek"**  
   Max specified this exact phrase. It replaced all occurrences of "cheek swab" or "swab the inside of your cheek."

5. **DNA sequence data, not physical DNA**  
   Max corrected: the project does **not** accept physical DNA. Participants order a kit from sequencing.com, collect the sample, mail it back **to sequencing.com**, and then share the resulting sequence data with Max. The homepage headline, subline, and button were re?written accordingly.

6. **Headline change**  
   The old hero text led with the ?$6K fundraiser. Now it invites people to "Check for traces of alien genetic manipulation in your DNA". The primary sidebar button became "Submit your DNA data" (gold), with "Donate" demoted to a secondary link.

7. **Hiding the 23andMe forwarding page**  
   The page ("how to export your existing 23andMe data") was removed from the Links page and all menus. It is now reachable only through a quiet "Already have 23andMe data?" link at the bottom of the Updates page.

8. **Fundraising update date auto?rolls daily**  
   On the Donate page the line `Update April 27, 2026:` now shows today's date dynamically with JavaScript (static fallback = today's date). The amount remains un?changed because no new donations came in. The script updates every day automatically - no redeploy needed.

9. **All changes kept bilingual (English / Russian)**  
   The worker is a single file serving both languages. Every edit was mirrored in the Russian version.

10. **Deployment and backup**  
    - Source location: `C:\claude_base\sites\starseed-site\src\worker.js`  
    - Deploy script: `bash deploy.sh` (uses wrangler to push worker `starseed-site`)  
    - Before each deploy, the live worker code is backed up to `C:\claude_base\backups\cf_workers\starseed-site\history`.  
    - After deploy, each change was committed individually and merged to master via the standard merge?push workflow.

## CURRENT STATE

- **All requested edits are live** on `starseedgenetics.com` (EN) and `ru.starseedgenetics.com` (RU). Verified with direct curl and cache?busting after each deploy.
- The last commit on master contains the auto?rolling date functionality and the DNA?vs?data correction.
- The site now cleanly communicates the new intake policy: full?genome sequencing, any configuration, any age, data?only.
- The 23andMe legacy forwarding page still exists and is functional, but hidden from normal navigation.
- The ?$6K fundraiser remains on the Donate page as a separate ongoing campaign; its sidebar progress bar and static date of the actual donation (Feb 7) are unchanged.

## EXACT NEXT STEP

The immediate batch of changes is complete. The session ended with two open questions:

1. Whether to bump the "10 families" number in the dated February 2026 fundraising story (Donate page) to the ~20 families / ~60 people mentioned in the "Starseed Handover 01" Notion document.
2. Whether to make the sidebar "thank you to our first donors - February 7" date also auto?roll to today's date.

**The next action is to ask Max for a decision on these two items.** (He may also provide further instructions from the Notion page he linked but that data was not yet applied.)

## OPEN QUESTIONS AWAITING USER

- Family count discrepancy: site says "10 families" in the historical fundraiser section; handover says "about 20 families, ~60 people." Should we update that section, or leave it as a dated record?
- Sidebar thank?you date (Feb 7): keep as a static historic note or make it dynamic like the Donate page update?

## KEY FILE PATHS, IDs, COMMANDS, NAMES

- **Site source (the only file):**  
  `C:\claude_base\sites\starseed-site\src\worker.js`

- **Deploy script:**  
  `C:\claude_base\sites\starseed-site\deploy.sh`  
  (runs `bash deploy.sh` from that directory; does a wrangler deploy, then a test curl)

- **Backup location:**  
  `C:\claude_base\backups\cf_workers\starseed-site\history`  
  (backups are timestamped JSON copies of the live worker code)

- **Live domain:**  
  `starseedgenetics.com` (English)  
  `ru.starseedgenetics.com` (Russian)

- **Cloudflare worker name:**  
  `starseed-site`

- **Claude worktree (current session):**  
  `C:\claude_base\.claude\worktrees\admiring-diffie-13ddd6`

- **Notion page Max referenced (untapped):**  
  `https://app.notion.com/p/39a0316f55608108ba46fd875c0f6236`  
  (He said to update based on that data, but then gave specific verbal corrections; we may need to revisit this page if further changes are needed.)

- **Handover document:**  
  "Starseed handover number 1" in Notion - already read at session start; contains the presentation script and open items.

## GOTCHAS & DEAD ENDS RULED OUT

- **Cloudflare edge?cache** frequently shows stale content for up to 15 minutes. Always use multiple requests with random cache?buster (e.g., `?cb=$RANDOM`) and set `Cache-Control: no-cache` to verify changes.
- The worker is one large bundled file; there is no separate template engine. All edits were done inline inside `src/worker.js`. Do not try to split into separate files without understanding the current bundling.
- The "Forwarding" page (23andMe export helper) was kept alive intentionally, not deleted. If Max ever wants it removed entirely, delete the function `pageForwarding` from the worker and also remove the hidden link in `pageUpdates`. Do not simply delete the route - the function would become dead code.
- The Russian language strings are near?identical copies of the English strings with commas instead of dots for decimals. Any change to English content must be mirrored in the corresponding Russian section (look for the switch on language variable in `pageHome`, `pageConsent`, etc.).
- The live counter script is inserted into the homepage body using a `<script>` tag that calculates elapsed seconds from a fixed epoch (July 1, 2024 midpoint). It uses `Date.now()`. If the site ever switches to a static generator, this logic must be preserved or the counter will break.
- The backup routine copies the *live worker code* (via wrangler), not the local `src/worker.js`. So if you edit locally and the deploy fails, the backup will still contain the previous live version. Good practice: back up *before* editing, not after.
