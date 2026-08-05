# Scribe handover - milestone 11 (~165K tokens)
# session: 20260615_oquent_cartwright_d704b1_1efeb657
# cwd: C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1
# written: 2026-06-15 11:50:02 by deepseek-v4-pro

# HANDOVER - starseedgenetics.com Migration (Google Sites ? Cloudflare)

---

## GOAL (Max's words)
"Deploy fully now. This is already acceptable."

Migrate starseedgenetics.com from Google Sites to Cloudflare. The redesigned preview is approved - flip it live.

---

## DECISIONS MADE + WHY

1. **Left vertical sidebar** (maxrempel.com style) - replaces the v1 top nav bar. Max said "repeat maxrempel.com design with vertical menu." Off-canvas on mobile via CSS checkbox hack (`#nav-toggle`).

2. **Two-column home** - original Google Site had two columns. Reproduced: main content left, right rail with donor thanks box + progress bar ($605/$6,000) + Donate/Participate buttons. Collapses to single column on mobile.

3. **Hero image unobstructed - hard rule.** Max: "nothing should block the faces on image - that's a rule, rather than limitation." Hero is a clean `<img>` with title below. No panels, no overlays, no frosted glass.

4. **Sharp hero** - v1 had a blurry 1244px screenshot. Recovered the real 1792?1024 original from Google Sites by extracting a fresh in-browser token and fetching with `Referer` header (=w2000). Stored as `public/assets/home-hero-bg.jpg`.

5. **No invented text** - v1 headline "Searching for alien DNA in human chromosomes" was fake. Removed. Only faithful real site content.

6. **Mobile-friendly** - Max said 50% mobile users. Breakpoint at 760px: sidebar goes off-canvas, columns stack, hamburger menu appears in a `.mtop` header bar with scrim overlay.

7. **Light theme always** - Max never wants dark. Colors: `--teal #1f7a8c`, `--gold #dd9a2b`, warm `--bg #f6f3ef`, Calibri font.

8. **Faithful copy** - all 11 pages reproduced: Home, Updates, Donate, Publications, Subscribe, Register, Consent, Tools, Team, Links, Forwarding. Google Forms embedded (Subscribe, Register, Consent). PayPal/Venmo/Zelle/check on Donate page.

9. **Preview-first, no DNS touch** - Max's explicit instruction: live site has real visitors, only flip DNS after approval. That approval just happened.

---

## CURRENT STATE

- **Preview URL** (live, approved): `https://starseed-site.max-rempel2.workers.dev`
- **Live DNS**: still points to the old Google Site - visitors see no change yet.
- **Code**: committed, merged to `master`, pushed.
- **Worker**: single ES module at `sites/starseed-site/src/worker.js`. All HTML generated server-side. Static assets in `public/assets/` (26 images).
- **Domain**: already on Cloudflare nameservers (`kurt.ns.cloudflare.com` / `ullis.ns.cloudflare.com`). No registrar change needed.
- **Verified**: desktop (1280?800), mobile (375?812), hamburger menu open - all screenshots confirmed correct.

---

## EXACT NEXT STEP

**Add a custom domain route so `starseedgenetics.com` serves the Worker instead of the Google Sites origin.**

Currently `wrangler.toml` has only `workers_dev = true` (preview). To go live:

1. Add a route binding `starseedgenetics.com/*` (and optionally `www.starseedgenetics.com/*`) to the `starseed-site` Worker in Cloudflare dashboard - OR - add `[routes]` to `wrangler.toml` and re-deploy.

2. Verify the DNS A/AAAA records for `starseedgenetics.com` are proxied (orange cloud) through Cloudflare. They should already be proxied since the domain was pointing to Google Sites via CF proxy.

3. If the Worker route is added via dashboard: set it to `starseedgenetics.com/*` pointing to the `starseed-site` Worker. If via wrangler: add to `wrangler.toml`:
   ```toml
   [[routes]]
   pattern = "starseedgenetics.com/*"
   zone_name = "starseedgenetics.com"
   ```
   Then run `deploy.sh`.

4. Test `https://starseedgenetics.com` resolves to the new Worker. The Google Site origin is bypassed - no downtime because Cloudflare routes at the edge.

5. (Only if needed) add a redirect from `www.starseedgenetics.com` ? `starseedgenetics.com`, or route both to the Worker.

---

## OPEN QUESTIONS

None. Max approved the preview and said deploy fully.

---

## KEY PATHS, IDs, COMMANDS

| What | Value |
|---|---|
| **Project root** | `C:/claude_base/.claude/worktrees/eloquent-cartwright-d704b1/sites/starseed-site/` |
| **Worker source** | `src/worker.js` |
| **Static assets** | `public/assets/` (26 images) |
| **Wrangler config** | `wrangler.toml` |
| **Deploy script** | `deploy.sh` (exports CF token + account ID, runs `npx wrangler@4 deploy`) |
| **Preview URL** | `https://starseed-site.max-rempel2.workers.dev` |
| **CF account ID** | `e4dc2224d6baa721873dca77dc6f057d` |
| **CF API token** | `ZUyIUYjo_6w53JHSBfGmw1Tei9XgBBNsnpKTMR2b` |
| **Wrangler** | `npx --yes wrangler@4 deploy` (v4.100.0) |
| **Node** | v22, at `C:/Users/maxre/nodejs-lts` |
| **Sharp hero** | `public/assets/home-hero-bg.jpg` (1792?1024) |
| **Git worktree** | branch `claude/eloquent-cartwright-d704b1`, merged to `master` at `C:/claude_base` |

---

## GOTCHAS

1. **Google Sites hero tokens expire** - the `googleusercontent.com/sitesv/` URLs 403 server-side without a `Referer: https://www.starseedgenetics.com/` header. The sharp hero was fetched via Playwright extracting an in-browser token + `curl` with referer. The local copy in `public/assets/` is permanent and safe.

2. **Dedup-by-content broke filenames** - earlier I deduped by MD5, which removed `logo.jpg` (identical content to `forwarding-img1.jpg`) and merged duplicate background images. Worker references 404'd. Fixed by copying ALL files verbatim; Cloudflare deduplicates on upload server-side. Don't do client-side dedup on assets whose filenames are referenced in code.

3. **wrangler.toml currently workers_dev=true** - the preview URL works, but the custom domain won't route until a route binding is added. Don't just re-deploy; add the route first.

4. **DNS is already proxied** - the domain currently shows Google Sites content through Cloudflare's proxy. When the Worker route is added, Cloudflare will intercept and serve the Worker instead. No DNS record changes needed, just the route binding.

5. **Mobile hamburger menu** - uses a CSS-only checkbox hack (`#nav-toggle:checked ~ .wrap .sidebar { left: 0 }`). No JavaScript. The `.scrim` overlay dims content; tapping it closes the menu (the label wraps the scrim, toggling the hidden checkbox).

6. **Google Forms** - Subscribe, Register, and Consent pages embed Google Forms via iframes. Resolved URLs:
   - Short registration: `https://docs.google.com/forms/d/e/1FAIpQLSeqRKIYIrn01GP1V19DnwUSHZX9JjK7dsv33l7NpSAhKndU-g/viewform?embedded=true`
   - Long interview: `https://docs.google.com/forms/d/e/1FAIpQLSeJ70jUNlxVLe_r2ZoiZDAkV1rLnuHSn-d6ynTM11Oei8OrTQ/viewform?embedded=true`
   - PayPal donate: hosted_button_id `KVFX7PEDZKRHA`
