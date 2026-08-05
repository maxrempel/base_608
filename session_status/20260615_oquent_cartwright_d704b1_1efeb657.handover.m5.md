# Scribe handover - milestone 5 (~76K tokens)
# session: 20260615_oquent_cartwright_d704b1_1efeb657
# cwd: C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1
# written: 2026-06-15 11:08:57 by deepseek-v4-pro

# HANDOVER: starseedgenetics.com Migration - Google Sites ? Cloudflare

---

## GOAL (Max's words)
"Migrate starseedgenetics.com from Google Sites to my Cloudflare. Faithful copy with images, and backgrounds. Make it as pretty or better."

---

## DECISIONS + WHY

**1. No DNS migration needed - DNS is already on Cloudflare.**
- `dig` / `whois` / `nslookup` confirmed the domain uses Cloudflare nameservers (`kurt.ns.cloudflare.com`, `ullis.ns.cloudflare.com`) and is proxying traffic to the current Google Site origin.
- Decision: skip registrar/nameserver work entirely. Only the origin target changes.

**2. Strategy: copy-first, then improve.**
- The assistant proposed (a) faithful copy first then (b) redesign. Max chose "faithful copy with images, and backgrounds. Make it as pretty or better" - this merges both: copy everything faithfully but also make it prettier from the start. No separate "first ugly, then polish" phase.

**3. Forms stay on Google.**
- Noted early that forms (Participate, Register, Consent, Subscribe, etc.) remain as-is on Google Forms. Only the static site pages move.

---

## CURRENT STATE

**Discovery complete:**

| What | Finding |
|------|---------|
| Registrar | Cloudflare (via whois) |
| Nameservers | kurt.ns.cloudflare.com / ullis.ns.cloudflare.com |
| Current origin | Google Sites (proxied behind Cloudflare) |
| Site structure | 1 main page + 11 linked pages |

**Pages identified:** Home, Participate, Updates, Donate, Publications, Subscribe, Register, Consent, Tools, Team, Links.

**What has NOT been done yet:**
- No content has been scraped from the Google Site.
- No images or background assets have been downloaded.
- No Cloudflare Pages / Workers / R2 project has been scaffolded.
- No DNS record change has been planned or executed.

---

## EXACT NEXT STEP

1. **Scrape the current Google Site** - fetch the homepage and all linked pages, capturing full HTML structure, text content, image URLs, background styling (CSS, inline styles, theme settings from Google Sites).
2. **Download all assets** - pull down every image and background asset referenced across all pages into a local working directory.
3. **Rebuild as a static site** - produce clean HTML/CSS for all 12 pages, faithfully reproducing content while improving visual polish (modern layouts, responsive design, better typography, preserved color scheme).
4. **Deploy to Cloudflare** (likely Cloudflare Pages or Workers) and point the existing DNS record to the new origin instead of Google Sites.
5. **Validate** - confirm all pages, images, backgrounds, and links work before cutting over.

---

## OPEN QUESTIONS

*None asked yet - the next session picks up immediately with scraping.*

However, the cold session should clarify:
- Which Cloudflare product to host on? (Pages for static, Workers if dynamic needed - but this looks static. Pages is the natural fit.)
- Does Max have access to the current Google Site's backend to assist with any scraping auth if needed?

---

## KEY PATHS / IDS

| Item | Value |
|------|-------|
| Domain | `starseedgenetics.com` |
| Current origin | Google Sites (proxied) |
| Cloudflare NS | `kurt.ns.cloudflare.com`, `ullis.ns.cloudflare.com` |
| Working directory | `C:\claude_base\.claude\worktrees\eloquent-cartwright-d704b1` |
| Session turns used | 6 turns, ~76K tokens (compaction at ~169K) |
| Linked pages | Participate, Updates, Donate, Publications, Subscribe, Register, Consent, Tools, Team, Links |

---

## GOTCHAS

- **No whois registrar details were fully confirmed** - the `whois` command was truncated/killed (`2>/dev/null` + grep). But since nameservers are already Cloudflare, registrar ownership is not blocking.
- **Google Sites scraping can be tricky** - Google Sites sometimes renders content dynamically (JS-heavy) or uses obfuscated image URLs (lh3.googleusercontent.com etc.). A simple `curl` may not capture everything; a headless browser fetch may be needed for backgrounds and embedded images.
- **Forms are staying on Google** - links to forms should remain as-is, not be recreated. Only informational pages move.
- **"Make it pretty or better" is subjective** - the cold session should confirm color preferences, font choices, layout wishes, or note that it should infer from the existing site's visual identity and enhance it incrementally rather than do a radical redesign.
