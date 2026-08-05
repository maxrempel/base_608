# Scribe handover - milestone 1 (~149K tokens)
# session: 20260706_zealous_jemison_bdd0f1_8d635a7b
# cwd: C:\claude_base\.claude\worktrees\zealous-jemison-bdd0f1
# written: 2026-07-06 07:42:43 by deepseek-v4-pro

# HANDOVER - Tamza Secret Zoom Link Distribution

## GOAL (in Max's own words)

Max needs a way to securely distribute the rotating secret Zoom link to **trusted, verified Tamza regulars** (~100-150 people), without exposing the link publicly or to impersonators. The context: on July 4, 2025, hooligans (described as "GB agents") attacked the Tamza Zoom meeting, joining with disabled cameras and impersonating respected regulars. The Zoom link must now be kept **secret**, given only to known, vetted people - and rotated regularly.

The broader vision Max described: collect typical participants, gather their contact info, and **automatically send them the rotating link** each time it changes - so he doesn't have to manually re-send every week.

## DECISIONS MADE + WHY

### 1. SMS was explored and **rejected as the primary channel**.
- A research agent surveyed Twilio, Telnyx, Plivo, Vonage, MessageBird.
- **Russia is a hard blocker**: an Aug 2025 Russian anti-spam law blocks all business SMS by default, AND Russia blocks any SMS containing a URL as spam. Since the message IS a link, no provider can deliver to Russia reliably.
- Ukraine = wartime "best-effort," ~$0.23/msg, silent drops possible.
- Israel/Germany/US = works fine but the RU problem makes SMS unviable as the sole channel for a Russian-speaking audience.
- Best SMS backup: Telnyx (cheapest, good intl routes) or Plivo - but only for non-RU stragglers.

### 2. Telegram is the chosen primary channel.
- Max agreed it's "perfect" - the club is Russian-speaking, everyone is already on Telegram, zero cost, no carrier filtering, works identically in all target countries.
- After discussion of bot-vs-channel, the **private Channel with approve-to-join** emerged as the simplest and best fit.

### 3. The "one-time verification, then channel does the rest" model.
This was the critical design insight that resolved Max's manageability concerns:

- **Verification is human, one-time.** A person proves they're real (voice message, Max/orgs recognize them). No software replaces this.
- **After verification, they're approved ONCE** into a private Telegram channel.
- **Every future rotating link is just posted to the channel** - all approved members see it automatically.
- **Membership = the living trusted list.** No separate database needed. Remove someone = kick them from the channel (one tap).
- **No phone numbers needed** for ongoing management. New person ? they message Max ? he verifies ? he sends them the invite link right in that chat ? done.

This eliminates the database complexity, the weekly re-sending burden, and the impersonator risk in one design.

### 4. Database approach was discussed but deemed overcomplicated.
- Unique per-person invite links tied to a DB was proposed but Max said it "sounds a little bit tricky."
- The simpler "private channel + manual approve" was accepted as the starting point.
- Automation can be layered on later if manual approving becomes annoying.

## CURRENT STATE

**Branch setup**: A branch was created from a branch. Two agents are registered on the broadcast board:
- **b51c** (this session) - owns the Zoom-link distribution design.
- **b51b** - a parallel session; b51c posted to b51b asking what they're building.

**What's been explored/completed:**
- ? Zoom participant reports pathway identified (zoom.us ? Reports ? Usage ? Meeting history).
- ? Bitwarden entry located: **"Tamza zoom 202206"** with username **admin@tamza.com** (password not yet retrieved/used).
- ? SMS provider comparison done (full research report with live sources).
- ? Design for Telegram-based distribution settled: private channel + approve-to-join.
- ? Zoom login NOT completed (was at the sign-in page, interrupted before entering credentials).
- ? No Telegram channel created yet.
- ? No Zoom participant list extracted yet.
- ? The parallel DB-building session (b51b) - status unknown to b51c.

## EXACT NEXT STEP

**Await b51b's response** on the broadcast board - Max paired b51c and b51b for a reason. b51b may be building the contact/participant list. Once that's clear:

**Then, to start building (in priority order):**

1. **Retrieve Zoom password from Bitwarden** for "Tamza zoom 202206" (admin@tamza.com), log in, and pull participant history to understand who regularly attends.

2. **Create the Telegram private channel:**
   - Name it (e.g., "????? - ????????? ??????" or similar)
   - Set to private, with "approve new members" on
   - Generate the invite link
   - Max or an org becomes the admin/approver

3. **Define the verification flow:**
   - Person contacts Max/orgs ? human verification (voice, recognition, referral)
   - Max sends them the channel invite link
   - Max approves their join request
   - Done - they receive all future rotating links automatically

4. **Post the current secret link** (the one from the July 6 newsletter: `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1`, Meeting ID: 873 4648 6242, Passcode: 44) as the first message.

5. **Later (Phase 2):** Automate the "post new link" step - a simple script or bot that pushes the rotating link to the channel when it changes, so Max doesn't have to manually post.

## OPEN QUESTIONS (awaiting Max)

- ? What is **b51b** building in the parallel session? (The database of people to invite?)
- ? Should the website (tamza.com) buttons be updated alongside this, or is the Telegram channel the only delivery mechanism?
- ? Who will be the channel admin(s) - just Max, or also other orgs (Natasha Grinbaum-Smirnos, Sasha Noskov, etc.)?
- ? For the ~100-150 verified people: is there already a mental list, or does it need to be built from scratch (Zoom reports + contacts)?

## KEY PATHS / IDS / NAMES

| Item | Value |
|---|---|
| **Zoom account** | admin@tamza.com |
| **Bitwarden entry** | "Tamza zoom 202206" |
| **Current secret Zoom link** | `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` |
| **Meeting ID** | 873 4648 6242 |
| **Passcode** | 44 |
| **Max's contact** | +1 (585) 705-1400 (WhatsApp, Telegram, SMS, Messenger) |
| **Newsletter admin** | admin@tamza.com |
| **Tamza calendar** | https://tamza.com/calendar/ |
| **Main YouTube** | https://youtube.com/@Tamza |
| **Live stream** | https://www.youtube.com/@prostoproverka/streams |
| **Backup site** | pomoga.org |
| **Branch bulletin board** | `C:\claude_base\branch_bulletin\bcast.py` |
| **b51c's board ID** | Registered as "b51c" |
| **b51b's board ID** | Posted to "b51b" - awaiting reply |

## GOTCHAS & DEAD ENDS

- ? **SMS to Russia is DEAD for link-bearing messages.** Russian carriers block any SMS containing a URL as spam, plus an Aug 2025 law blocks all business SMS by default. No SMS provider can beat this - it's policy at the network level. Do NOT attempt SMS-to-Russia; it will silently fail.
- ? **Telegram bots cannot cold-message people.** Each person must press "Start" once before a bot can DM them. This is why the **private channel** (where people join via invite link, then receive all posts) is the correct design - no "Start" friction, just "tap the link and get approved."
- ? **Impersonator risk is real.** The same attackers who hit the Zoom will try to infiltrate the Telegram channel. Human verification (voice message, personal recognition) must gate every approval. No automated verification can replace this.
- ? **Any trusted member could forward the link.** This is an unavoidable limitation - no Telegram design prevents a bad actor (or careless member) from re-sharing the link. The security is only as strong as the trustworthiness of the approved people.
- ? **Bitwarden session** was active in this session with the session token. Future cold sessions may need to re-authenticate.
- ? **Zoom login was interrupted** - the browser was sitting at the Zoom sign-in page when the task was redirected. No credentials were entered yet.
