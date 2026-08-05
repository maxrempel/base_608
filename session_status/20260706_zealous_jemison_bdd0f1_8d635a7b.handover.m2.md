# Scribe handover - milestone 2 (~151K tokens)
# session: 20260706_zealous_jemison_bdd0f1_8d635a7b
# cwd: C:\claude_base\.claude\worktrees\zealous-jemison-bdd0f1
# written: 2026-07-06 07:44:25 by deepseek-v4-pro

# HANDOVER - Tamza Secret Link Distribution System

---

## GOAL (in Max's words)
Find ways to securely distribute a rotating secret Zoom link to verified Tamza regulars (~100-150 people) across Russia, Ukraine, Israel, Germany, and the US. The club was attacked on July 4, 2026 by impersonators (agents of GB). The link is now secret and must only reach trusted, verified people - and be easy to rotate and redistribute when it changes. Explore both Telegram and Facebook as distribution channels.

## ORIGINAL TANGENT (from earlier in session)
Max also needed the Tamza **website (tamza.com) updated** to remove public Zoom links and replace them with instructions telling people to contact Max (+1-585-705-1400) or subscribe to the newsletter for the secret link. This was discussed but not yet executed - the session shifted to the distribution-automation problem. Website update is pending.

## DECISIONS MADE + WHY

### 1. SMS - ruled out for Russia (the core audience)
- **Research completed** (full live shopping round across Twilio, Telnyx, Plivo, Vonage, MessageBird). The killer finding: **Russia blocks all SMS containing a URL as spam**, and a new Aug-2025 Russian anti-spam law blocks all business (A2P) SMS by default. Since the message IS a link, no provider can deliver it into Russian phones. This is a network-policy block, not a vendor limitation.
- Ukraine SMS works (best-effort, ~23?/msg), Israel/Germany/US fine. But Russia is the dealbreaker.
- If SMS is needed as a fallback for non-RU contacts: **Telnyx** recommended (cheapest, best international routes, good Python API). Budget is trivially met (~50-80 msgs/week = a few dollars/month).

### 2. Telegram - chosen as the primary channel
- Free, zero per-message cost, no carrier filtering, works identically in RU/UA/IL/DE/US, and the Russian-speaking club already lives there.
- After extended design discussion, the preferred approach evolved from a bot-with-allowlist to a **private Telegram Channel with approve-to-join** - the simplest, most manageable option.
- The key design insight: **verify each person ONCE (human check - voice message, call, you recognize them), then approve them into the channel.** From then on, every rotating link just gets posted in the channel and all verified members see it. No re-verification, no re-sending, no phone list needed, no database. The channel membership IS the living verified list.

### 3. Facebook Messenger - being evaluated now (b51g)
- Messenger **group chat** can't do one-way announcements (any member can post, no admin-only mode). Ruled out.
- **Facebook Page Broadcast Channel** = purest one-way (only admins post, followers just read + emoji react). Good but tied to a Page, less tight identity control.
- **Private Facebook Group** (locked settings): admins-only posting, approve-to-join with screening questions. Matches the Telegram pattern - shareable invite link + one-by-one approval + optional screening questions = controlled, vetted entry. This is the recommended Facebook approach.

### 4. General principle settled
- Impersonator problem is solved by ONE-TIME human verification before entry into a locked channel/group. No software replaces the human identity check - but after that, delivery is fully automatic.
- Any trusted member could re-forward the link onward - this is unavoidable regardless of tool. The link is only as secret as the people you trust with it.
- Phone numbers are NOT needed as an identifier for this approach - you invite people through existing conversations (Telegram, WhatsApp, email), they click the invite link, you approve. The database-of-phone-numbers idea was discussed and deemed overly complex for the goal.

---

## CURRENT STATE

### Branch b21b - SMS/Telegram Delivery Design
- Shopping round complete; live research report with 10 vendor comparison + sources saved.
- Recommendation delivered: Telegram private channel as primary, Telnyx as SMS fallback for non-RU stragglers.
- No code built yet. Pure design/recommendation stage.

### Branch b51c - Paired with b51b
- b51c registered, posted to b51b on the broadcast board with the design summary (private Telegram channel, verify-once-approve-once). Awaiting b51b's reply with what they are building.
- No code built yet.

### Branch b51g - Facebook Group Settings Inquiry (CURRENT / LAST TOPIC)
- Question answered: Facebook Messenger group chat is the wrong tool for one-way broadcast.
- Facebook private Group (locked to admins-only post + approve-to-join with screening) is the right Facebook equivalent.
- Last specific Q&A: YES, Facebook Groups support one invite link with one-by-one approval. Each person requests, you see their profile, tap Approve/Decline. Optional screening questions ("who invited you/real name") appear before you decide.
- **No action taken yet** - the conversation ended with Claude offering to walk through creating the group with these exact settings.

### Zoom Credentials (from earlier in session)
- Bitwarden item: **"Tamza zoom 202206"** - login **admin@tamza.com**
- Session pulled credentials but was interrupted before logging in to pull participant reports.
- Zoom participant reports are available at zoom.us ? Reports ? Usage ? Meeting history ? click participant count ? Export CSV. Only for host on paid (Pro+) account. Appears 15-30 min after meeting ends.

---

## EXACT NEXT STEP
Max's last question was answered (yes, Facebook Groups support invite-link + one-by-one approval). The natural next step, per the last Claude offer: **walk Max through creating the Facebook Group with locked settings (admins-only posting, approve-to-join, screening questions) OR set up the Telegram private channel - whichever Max wants first.**

Alternatively, b51b may respond on the broadcast board with their build, which could redirect the session.

---

## OPEN QUESTIONS (still awaiting Max)

1. **Which to set up first - Telegram private channel or Facebook locked Group?** Both follow the same verify-once-approve-once pattern.
2. **Website update (tamza.com):** Is this still needed, and should the website point to the new channel/group as the way to get the link?
3. **Zoom participant reports:** Should Claude still log into Zoom as admin@tamza.com and pull past participant lists as a starting point for vetting who to invite?
4. **b51b status:** What is b51b building on their side? Coordination item.

---

## KEY PATHS / IDs / NAMES

| Item | Value |
|---|---|
| Current cwd | `C:\claude_base\.claude\worktrees\zealous-jemison-bdd0f1` |
| Broadcast board | `C:/claude_base/branch_bulletin/bcast.py` |
| Bitwarden session | Has live session (`3Q1LuTvallMTPux...`) |
| Bitwarden item | "Tamza zoom 202206" - user `admin@tamza.com` |
| Zoom Meeting ID | 873 4648 6242 |
| Zoom Passcode | 44 |
| Secret Zoom link (as of July 6, 2026) | `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` |
| Max's contact | +1 (585) 705-1400 (WhatsApp, Telegram, SMS, Messenger) |
| Tamza site | tamza.com |
| Newsletter admin | admin@tamza.com |
| Research report saved | Agent output with full vendor comparison + 10 sources |

## GOTCHAS / DEAD ENDS RULED OUT

1. **SMS to Russia = dead end.** Do not attempt. URL-bearing SMS is blocked as spam by Russian carriers, and Aug-2025 law blocks all A2P SMS. No provider bypasses this.
2. **Messenger group chat = wrong tool.** Cannot be made one-way. Use a Facebook Group with locked settings instead.
3. **Bot cold-messaging = spam-ban risk.** Telegram bot can't cold-message - person must tap Start first. Private channel avoids this entirely.
4. **Phone-number database approach = overcomplicated.** The channel/group + one-time-verification model eliminates the need to maintain a phone list. Invite links are sent through existing conversations.
5. **No method prevents link forwarding** - any trusted member could leak the link onward. This is a human trust problem, not a technical one. Acknowledged and accepted.
6. **Zoom participant CSV = incomplete for contacts.** It gives display names + email (only for those logged into a Zoom account). Won't give phone numbers. Useful as a starting point for "who attends" but not a complete contact list.
