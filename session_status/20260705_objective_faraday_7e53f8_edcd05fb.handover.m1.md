# Scribe handover - milestone 1 (~105K tokens)
# session: 20260705_objective_faraday_7e53f8_edcd05fb
# cwd: C:\claude_base\.claude\worktrees\objective-faraday-7e53f8
# written: 2026-07-05 12:32:29 by deepseek-v4-pro

# HANDOVER - Tamza.com: Hide Secret Zoom Link

## GOAL (in Max's words)
Max needs to update tamza.com so the Zoom link is **no longer publicly visible**. Background: on July 4, 2026 (Saturday), club Tamza and friendly clubs were attacked by hooligans ("agents of GB") who joined Zoom with cameras off, using stolen names/avatars of respected participants, and caused disruption. As a result, the Zoom link is now **secret** - shared only via the email newsletter to known people.

## DECISIONS MADE + WHY

1. **Direct Zoom link must be removed from public-facing site.** Reason: security - only familiar people through the newsletter should get it. The link rotates regularly.

2. **Replacement approach agreed (in principle):** Instead of "Enter from site" buttons that link directly to Zoom, show a message explaining:
   - The link is now secret due to the hooligan attack
   - How to get the fresh link (contact Max directly)
   - How to subscribe to the newsletter (admin@tamza.com)
   - Reminder to turn on camera so organizers can verify identity

3. **Proposed replacement text** was drafted by Claude (see CURRENT STATE below). Max's response "??? ????? ???" ("Better now") - but the conversation stopped before final confirmation of exact wording and placement strategy.

## CURRENT STATE

- Claude drafted this replacement text:
  > ?????? ?? ??? ?????? ????????? (??-?? ????????? ?????????). ???? ?? ?????? ????????, ????? ????????.
  > ????? ???????? ?????? ?????? - ???????? ????? ???????: WhatsApp / Telegram / SMS / ??????????, +1 (585) 705-1400.
  > ??????????? ?? ???????? - admin@tamza.com.
  > ??? ????? ? Zoom ????????? ??????, ????? ?? ??????, ??? ?? ???????? ????????.

- No code has been touched yet. No files modified. The site is still as-is with public Zoom links.

## EXACT NEXT STEP

1. **Confirm the replacement text** with Max - is the drafted message acceptable?
2. **Decide placement strategy** - one banner at the top of the site, or replace each individual "Enter" button (Saturday concerts, Sunday Guitar Circle, all events)?
3. **After confirmation, implement** - find the relevant buttons/links in the site code and swap them.

## OPEN QUESTIONS (awaiting Max)

- Is the drafted replacement text final, or does it need edits?
- One site-wide banner at the top, or replace every individual "Enter from site" button/link?
- Should the old Zoom link be completely removed from the site source code, or just hidden behind a contact-gate?

## KEY PATHS / IDs / NAMES

- **Website:** tamza.com
- **New secret Zoom link:** https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1
- **Meeting ID:** 873 4648 6242, Passcode: 44
- **Max's contact:** +1 (585) 705-1400 (WhatsApp, Telegram, SMS, Messenger)
- **Newsletter subscription:** admin@tamza.com
- **PayPal for "????????? ???????":** pay@tamza.com (mark "MEDS")
- **YouTube channels:** https://www.youtube.com/@prostoproverka/streams (live), https://youtube.com/@Tamza (main archive)
- **Backup site:** pomoga.org
- **Alternative socials:** VK - https://vk.com/clubtamza, Telegram - https://t.me/+BujK2WUr65NhNDBh
- **Newsletter draft date:** July 6, 2026 (upcoming events cover July 4-13, 2026)

## GOTCHAS & DEAD ENDS

- **Claude initially misunderstood the task** - first asked "what to update?" despite the newsletter text clearly explaining the attack and the secrecy requirement. Max had to push ("?? ??, ?????, ?? ?????, ??? ??? ?????????") before Claude connected the dots. **Lesson for the next session:** the core ask is security-driven - hide the public Zoom link, period. Don't overcomplicate it.
- **The "secret link" will be rotated regularly** per the newsletter - so any hardcoded link replacement on the site is temporary. Better to point to a contact method (Max's phone / the newsletter) than to bake in a link that will go stale.
- **Two different Zoom links appear** in the newsletter: the new secret one (873 4648 6242) and an older one in the footer (828 3716 6247). The new secret one is the active one; the footer link is stale/old but left as a fallback in the newsletter draft. On the site, only the current secret link matters - but again, it rotates.
- **No code exploration has happened yet** - we don't know the site structure (static HTML? CMS? Where the "Enter" buttons live?). The next session will need to poke around the repo before implementing.
