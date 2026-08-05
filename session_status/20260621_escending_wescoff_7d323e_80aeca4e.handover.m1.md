# Scribe handover - milestone 1 (~85K tokens)
# session: 20260621_escending_wescoff_7d323e_80aeca4e
# cwd: C:\claude_base\.claude\worktrees\condescending-wescoff-7d323e
# written: 2026-06-21 13:57:57 by deepseek-v4-pro

# HANDOVER: Podcast Guest Media Kit for Max Rempel

## GOAL (Max's words)
"Prepare a podcast appearance portfolio / media package for me, and publish on my site. Photo, bio, shmio, you know better."

Translation: Build a podcast guest one-sheet page on maxrempel.com containing everything a podcast host would need to book and introduce Max.

## DECISIONS + WHY

**Scope defined by Claude, no objections from Max:**
- Headshot photo
- Three bio lengths (1-line, short paragraph, long paragraph)
- Topics Max speaks on
- Suggested interview questions
- Credentials / social proof
- Past appearances list
- Booking contact info

**Deployment target:** maxrempel.com - a page within the existing site (not a PDF one-sheet, not a separate site).

**Work style:** Max wants parallel progress. He said to proceed with everything while he hunts down a headshot. So the implied decision is: build the page structure, populate draft bios and content, leave the headshot as a placeholder until he provides it.

## CURRENT STATE

- **Session turns:** 2
- **Tool calls made:** 0
- **Content gathered:** None yet. No file reads, no site exploration, no bios written.
- **Headshot status:** Max is actively searching for it offline. Assume not yet provided.
- **Site context:** Working directory is `C:\claude_base\.claude\worktrees\condescending-wescoff-7d323e` - this appears to be a git worktree for Max's site project. The actual site files live somewhere under this path.

## EXACT NEXT STEP

1. **Explore the site repo structure** - figure out how pages are built (static HTML, Hugo, Jekyll, Next.js, etc.), where existing pages live, and what templating or routing is used. This is critical before writing any page file.

2. **Draft all written content for the media kit page** based on what you can infer or find in Max's existing site/about content - bios, credentials, appearances. Use `maxrempel.com` existing copy as a source.

3. **Build the media kit page file** with a headshot placeholder (empty `<img>` with an obvious alt or a comment marking where to insert it).

4. **Present the draft** to Max for approval, clearly flagging the headshot as pending.

## OPEN QUESTIONS (awaiting Max)

- **Headshot file** - Max is searching. Do not block on it; use a placeholder.
- **Preferred tone / style** for bios - conversational, corporate, witty? (Infer from existing site copy if available.)
- **Specific past appearances** - if not on the site, ask when Max returns.
- **Booking contact** - email? contact form link? specific calendar link (Calendly, etc.)?
- **Page URL preference** - e.g., `/press`, `/podcast`, `/media-kit`, `/guest`?

## KEY PATHS / IDS

- **Repo root:** `C:\claude_base\.claude\worktrees\condescending-wescoff-7d323e`
- **Live site:** `maxrempel.com`
- **No specific files identified yet** - need to explore the repo first.

## GOTCHAS / RULED OUT

- **Nothing ruled out yet** - the session is brand new.
- **Potential pitfall:** Don't assume the site structure. It could be any framework. Read the directory tree and config files before creating anything.
- **Potential pitfall:** Max said "do everything" but the headshot is clearly a dependency he owns. Don't stall the whole task waiting for it - build everything else and flag the gap.
- **No existing media kit page** - this is net-new, not an edit.
