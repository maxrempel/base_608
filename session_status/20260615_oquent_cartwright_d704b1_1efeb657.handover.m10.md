# Scribe handover - milestone 10 (~156K tokens)
# session: 20260615_oquent_cartwright_d704b1_1efeb657
# cwd: C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1
# written: 2026-06-15 11:37:39 by deepseek-v4-pro

# HANDOVER - starseedgenetics.com Cloudflare rebuild (preview live, revisions requested)

## GOAL (Max's own words)
> "Manu is fake. and blurry, the original site had two columns. Make the site mobile friendly, most of the users will be mobile, i say 50/50. Next, repeat maxrempel.com design with vertical menu. Otherwiese pretty good. Nice tohave the image."

## DECISIONS + WHY
- **Faithful copy with images/backgrounds** - Decided to rebuild all 11 pages as a single Worker, keeping the hero, banners, and team photos.
- **Preview-first, DNS untouched** - Deploy to `starseed-site.max-rempel2.workers.dev` so Max can review; live `starseedgenetics.com` still serves the Google Site. No nameserver changes needed (Cloudflare already authoritative).
- **Single-column compact layout (maxrempel.com style)** - Chosen initially; now Max wants **two columns + vertical menu**, matching original site but with maxrempel visual language.
- **Manu was listed on the Team page** - identified as fake/blurry; must remove that person entirely.

## CURRENT STATE
- **Deployed preview**: https://starseed-site.max-rempel2.workers.dev (all pages return 200, visually verified)
- **All pages built**: Home, Updates, Donate, Publications, Subscribe, Register, Consent, Tools, Team, Links, Forwarding
- **Forms**: Google Forms (Subscribe, Register) embedded as iframes; PayPal/Venmo/Zelle/check on Donate page
- **Assets**: All images (hero, banners, team photos, logo) in `public/assets/`; deduplicated by MD5 but all needed filenames preserved
- **Worker code**: single `src/worker.js` (HTML/CSS/JS routing all inline, no external stylesheets)
- **Wrangler**: v4.100, Node 22, API token `ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b`
- **Commit**: merged to master in `C:\claude_base`, pushed
- **The problem areas** (from Max):
  1. **Manu** - a false team member with a blurry photo, must be removed from the Team page
  2. **Hero image is blurry** - home-hero-bg.jpg was a screen-capture (1244?px wide), needs sharpening/upscaling
  3. **Two-column layout** - currently single-column; original site had two columns; must re-introduce two columns that stack responsively for mobile (50/50 mobile/desktop target)
  4. **Vertical menu** - need a sidebar/vertical navigation like maxrempel.com's design (the existing build has no menu, just section anchors)

## EXACT NEXT STEPS (in order, for a cold session)

### 1. Remove Manu from the team
- Open `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1\sites\starseed-site\src\worker.js`
- Locate the `TEAM` array (likely near the bottom, inside `<script>` or computed data). Find the entry with `name: "Manu"` (or similar) and delete the whole object.
- Verify that no other reference to Manu remains in the file.

### 2. Sharpen/upscale the hero image
- Source: `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1\sites\starseed-site\public\assets\home-hero-bg.jpg`
- The image is a 1244?px screen-capture; Max says it's blurry.
- Possible approaches:
  - **Try to fetch the original hero from Google Sites** - The scraper captured `home-hero-bg.jpg` from the rendered page; the original Google Sites image URL might still work if the session IDs haven't expired. Look in capture notes (`STYLE_NOTES.md`, `manifest.json`) for the original URL, attempt direct download with `curl`/`wget`. If it works, replace with the full-resolution version.
  - **Upscale using AI** - If any upscaler is available (e.g., `node real-esrgan`, Python script, or even `sharp` to resize with high-quality kernel), upscale to 2560?px width (retina adequate) and replace the asset.
  - **CSS fallback** - apply `image-rendering: auto` and let the browser handle it, but Max wants it truly sharp, so an actual upscale is expected.
- After replacement, test the preview home page.

### 3. Implement two-column responsive layout + vertical menu
- **Study maxrempel.com's actual layout** - Look at `C:\claude_base\sites\maxrempel-site\src\styles.js` and `index.js` (or `worker.js` if it's a Worker) to understand the vertical menu design you originally built for that domain. It likely has a left sidebar with navigation and a right content area that collapses on mobile.
- **Redesign the starseed Worker** to mirror that structure:
  - Left sidebar (vertical menu) listing all pages: Home, Updates, Donate, Publications, Subscribe, Register, Consent, Tools, Team, Links. Use `maxrempel` styling (dark background, compact text, maybe with subtle banners).
  - Right main content area showing the current page's hero (full-width over content) and the page-specific content below.
  - On mobile (??768?px), move the menu to a hamburger icon in the header, or to the top, and stack the sidebar above content.
  - Keep the existing hero section on the home page (and subpage banners) but adapt them to the two-column space.
- Ensure all existing page content (forms, donate buttons, progress bar, team photos, publications lists, etc.) remains intact; just restructured into the new layout.
- Increase font sizes / touch targets for mobile friendliness (50/50 mobile) - maybe 16?px base, 20?px on buttons.

### 4. Deploy revised preview and show Max
- From `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1\sites\starseed-site`
- Use the same token: `export CLOUDFLARE_API_TOKEN=ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b && npx wrangler deploy`
- Verify all pages render correctly (home, team, donate, etc.) on both desktop and mobile (use Playwright or screenshots at 375?px width).
- Screenshot the home, team, and a subpage to confirm the new layout and sharp hero.
- Send the preview URL to Max with the updates.

## OPEN QUESTIONS (awaiting Max)
None - the feedback is explicit. Just the above fixes needed.

## KEY PATHS, IDs, COMMANDS

### Files
- **Worker source** (all HTML/CSS/JS): `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1\sites\starseed-site\src\worker.js`
- **Assets** (images): `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1\sites\starseed-site\public\assets\`
  - Hero: `home-hero-bg.jpg`
  - Logo: `logo.jpg`
  - Team photos: e.g., `team1.jpg` ... `team7.jpg` (need to identify Manu's
