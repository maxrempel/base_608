# Scribe handover - milestone 4 (~330K tokens)
# session: 20260706_zealous_jemison_bdd0f1_8d635a7b
# cwd: C:\claude_base\.claude\worktrees\zealous-jemison-bdd0f1
# written: 2026-07-06 09:29:26 by deepseek-v4-pro

# HANDOVER - TAMZA Secure Communications & Collateral (b51g, 2026-07-06)

---

## PRIMARY GOAL (in Max's words)

After a security incident (July 4, 2026 - hooligans/GDB agents impersonating TAMZA members in Zoom with spoofed names and profile pictures), Max needs to **rotate the Zoom link to a secret one, distribute it only to trusted verified regulars, and update the TAMZA website to stop publishing the link openly.** Two parallel tracks emerged: (1) a Telegram channel for controlled link distribution, (2) a Facebook group for the same purpose, and (3) a collage banner for the existing Facebook group.

A side goal: explore SMS/WhatsApp/Telegram for automated link delivery to a list of ~100-150 phone numbers.

---

## THREAD 1: ZOOM LINK SECURITY + DISTRIBUTION STRATEGY

### The Threat
- On July 4, attackers joined Zoom using familiar names/profile pictures with cameras off and caused disruption
- The new secret Zoom link (ID: 873 4648 6242, passcode: 44) must only go to verified real people - not published openly

### SMS Exploration (Deprioritized)
- **Decision:** SMS is NOT the primary channel. Russia blocks any SMS containing a URL as spam (Aug 2025 anti-spam law). Ukraine is "best-effort" with silent drops. Israel/Germany work but expensive. For a Russian-speaking audience where everyone's already on Telegram, SMS makes no sense.
- **Fallback only:** Telnyx (cheapest API, good intl routes) could cover the IL/DE/US minority who aren't on Telegram. Kept on standby, not built.

### Telegram Channel - DECIDED AS PRIMARY

**Design decision:** A **private Telegram Channel** (not a bot, not a group chat), because:
- Channels are inherently one-way (admins post, members read) - matches Max's "announcements only, no discussion" requirement
- Private = not searchable, invite-only, keeps the secret link contained
- **"Request Admin Approval"** enabled on the invite link ? Max must approve each person, which is the identity gate against impersonators
- No database, no scripts, no coding needed to start - Telegram's own member management IS the control panel

**Alternative considered and rejected:** A bot sending individual DMs (more complex, each person needs to press Start, requires Telegram user IDs, the "press Start once" step is an extra friction). Channel is simpler and easier for Max to manage.

**Created:**
- Channel: **"?????-????"** (private, Max Rempel = owner/admin)
- **Approved invite link:** `https://t.me/+D7nxFaemjjRiNWUx` - gives a join request; nobody enters until Max approves
- **WARNING:** There's a SECOND default link (`t.me/+-dawRmE72YswOTAx`) that lets people join WITHOUT approval - this must NEVER be shared
- **Friendly redirect:** `https://tamza.com/telega` ? 302 redirects to the approval link above (deployed via CF Worker, added route to `worker.js`, verified working, homepage/cartotheque/dezh all still functional)

### Workflow
1. Person contacts Max (voice message, WhatsApp, whatever)
2. Max verifies they're real - one-time human check
3. Max sends them `tamza.com/telega` (friendly link)
4. They tap ? request to join ? Max taps "Approve"
5. They're in forever. When Zoom link rotates, Max posts it once in the channel ? all approved members see it instantly
6. Max can remove anyone anytime

---

## THREAD 2: FACEBOOK GROUP (Parallel Effort)

### Decision
A **Facebook Group** (not Messenger chat) because:
- Messenger groups have no message approval, no admin-post-only mode - anyone can post
- Facebook Groups support **"Admins/post only"** + **"Approve member requests"** + **screening questions** - exactly the secret controlled list Max wants
- Sub-groups were considered but rejected: sub-group members must be in the parent group, and this group is public - so a sub-group wouldn't be truly secret

### Created
- Max created the Facebook group manually (details not captured in this session)
- It's set to Private + Hidden, with approval-to-join and admins-post-only

### Custom Link
- Facebook Groups can have a custom web address (`facebook.com/groups/yourname`) but only after reaching a minimum number of members and if the name is unique. The raw invite code can't be renamed.

---

## THREAD 3: FACEBOOK GROUP BANNER COLLAGE

### Goal
Collect event cover images from `facebook.com/groups/clubtamza/events` and make a collage banner for the group.

### Banner Spec
- Facebook Group cover: **1640 ? 856 pixels (1.91:1 aspect ratio)** - confirmed via web search

### Process
- Logged into Facebook as **Max Steinberg** (maxsteinberg2@gmail.com, Bitwarden "Steinberg 201904") - NOT Max's main account (per new global2 rule - see below)
- Navigated to the group events page, collected 10 event links
- Fetched cover images via logged-out `og:image` Facebook crawler endpoint with a crawler user-agent
- 8 of 10 covers downloaded cleanly as real event posters; 2 upcoming events (??????? concert, "????" event) returned login pages - skipped them

### Output
- **Banner file:** `C:/claude_base/projects/tamza_fb_banner/output/tamza_fb_group_banner_1640x856_v01.jpg`
- 8 event posters in a 4?2 grid, center-cropped to fill the wide format, no gaps
- Honest caveat: the original posters are vertical/text-heavy, so cropping to landscape loses some edge text - looks lively but a bit busy. Max may want a redesign (add padding/background instead of cropping, or add a "?????" title overlay)

### Cannot Upload
- The Max Steinberg account is NOT an admin of the Facebook group, so Claude cannot set the cover image. Max must upload it manually to the group.

---

## NEW RULE ADDED TO GLOBAL2

```
FACEBOOK - USE THE MAX STEINBERG ACCOUNT, NOT MAX'S MAIN ACCOUNT (added 2026-07-06)
For any Facebook automation, Claude MUST use Max Steinberg (maxsteinberg2@gmail.com,
Bitwarden "Steinberg 201904"), NOT Max's main account (max.rempel2@gmail.com).
Why: automated logins risk captchas/locks, and Max can't afford that on his main account.
If a task genuinely requires the main account's admin rights, STOP and ask Max first.
```

---

## CURRENT STATE

| Item | Status |
|------|--------|
| Telegram channel "?????-????" | **Created, ready for use.** Max is owner. Approval-on link ready. Friendly redirect deployed. |
| Friendly redirect tamza.com/telega | **Deployed and verified.** |
| Facebook Group | **Created by Max.** Settings assumed private + approval-to-join + admins-post-only. |
| Banner collage | **Done.** 1640?856 JPG at the path above. Max needs to upload manually. |
| SMS research | **Done.** Conclusion: don't use SMS as primary. Telegram is the answer. |
| Database of phone numbers | **Not built.** The Telegram channel approach eliminates the need for a phone-number database. |
| Playwright browser lock | **Closed** (released after banner was created). |

---

## EXACT NEXT STEP

**The session ended with Max looking at the banner collage.** The very last thing was Claude asking which of three paths to take:

1. Max uploads the current banner manually as-is
2. Redesign the banner (less cropping, add background/title)
3. Add more event images to reach 15-20

**The cold session should pick up EXACTLY here:** ask Max whether he wants to keep the banner, redesign it, or add more images - and then act on his answer. The Playwright browser is closed; reopening it requires logging in again.

---

## OPEN QUESTIONS

1. **Banner:** Keep, redesign, or expand with more events? Max hasn't answered yet.
2. **Telegram channel:** Should we post the first message (current Zoom link) into the channel? Should we add co-organizers as admins?
3. **Facebook Group custom URL:** Did Max set the custom web address? If not, it can only be done after the group has enough members.
4. **Coordination with the newsletter:** Is the Telegram channel meant to replace newsletter link delivery, or supplement it (people who aren't on the newsletter)?
5. **Existing members:** Does Max want to bulk-invite his existing trusted contacts into the Telegram channel, or just invite new people one-by-one as they request?

---

## KEY FILES, PATHS, AND IDS

| What | Path/ID |
|------|---------|
| Telegram channel | "?????-????" (private, Max is owner) |
| Approval invite link | `https://t.me/+D7nxFaemjjRiNWUx` |
| Dangerous auto-join link (DO NOT SHARE) | `t.me/+-dawRmE72YswOTAx` |
| Friendly redirect | `https://tamza.com/telega` ? approval link |
| CF Worker source | `C:/Users/maxre/AppData/Local/Temp/claude/tamza_worker_live.txt` |
| Deploy script | Reference: `C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_tamza_worker_deploy_dezh.md` |
| Token file | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/cloudflare_workers_kv_token_20260303.txt` |
| Banner output | `C:/claude_base/projects/tamza_fb_banner/output/tamza_fb_group_banner_1640x856_v01.jpg` |
| Cover images (raw) | `C:/claude_base/projects/tamza_fb_banner/covers_raw/` |
| Facebook event IDs | 1052239564150786, 1554638936267132, 2448211325624695, 1375475131157735, 862695286896843, 1152307027776459, 745304667851745, 1192490123202206, 558584637365621, 1913456656392877 |
| Facebook Claude account | maxsteinberg2@gmail.com (Bitwarden "Steinberg 201904") |
| FB login 2FA | Will trigger reCAPTCHA on fresh login - Max needs to solve it |
| Branch name | zealous-jemison-bdd0f1 (b51g inside it) |
| Broadcast board | `C:/claude_base/branch_bulletin/bcast.py` |
| Global rules | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| Zoom account | admin@tamza.com (Bitwarden "Tamza zoom 202206") |
| Zoom secret link (current) | ID 873 4648 6242, passcode 44, pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1 |

---

## GOTCHAS AND DEAD ENDS

1. **SMS to Russia is dead.** Any SMS with a URL is spam-blocked; an Aug-2025 Russian law blocks all A2P SMS by default. No provider can beat this. Don't retry.
2. **Facebook Messenger groups cannot be one-way.** No message approval, no admin-post-only. The feature doesn't exist. Don't build this.
3. **Facebook sub-groups of public groups aren't secret.** Members must already be in the parent, defeating the purpose of a secret controlled list.
4. **Telegram private channel invite links are inherently ugly (t.me/+hash).** This is by design - the randomness IS the privacy. A pretty custom link requires making the channel public, which removes the approval gate. The compromise is the friendly redirect on the TAMZA domain.
5. **The Telegram channel has TWO invite links** - the approval one and a default one that auto-admits. The default one MUST NOT be shared or the impersonator gate is broken.
6. **Facebook login always triggers reCAPTCHA.** The Steinberg account will need Max to solve it manually on any fresh Playwright session.
7. **Facebook event covers for upcoming events can't be fetched via HTTP** - they return a login wall. Must be captured from the rendered page (logged-in browser).
8. **Bitwarden session token** for this session: `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==` (may expire).
9. **Playwright browser profile** for Telegram login is persisted - reopening should keep the Telegram session if the same profile dir is used (`C:\claude_base\playwright_profile` + `pw_mcp_config.json`). However, the session lacked Bitwarden extension; Max noted this but let it slide since QR login didn't need it.
