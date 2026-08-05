# Scribe handover - milestone 5 (~387K tokens)
# session: 20260706_zealous_jemison_bdd0f1_8d635a7b
# cwd: C:\claude_base\.claude\worktrees\zealous-jemison-bdd0f1
# written: 2026-07-06 12:37:40 by deepseek-v4-pro

# HANDOVER - Tamza Secret Link Distribution + FB Banner

---

## GOAL (in Max's own words)

After a hooligan attack (July 4, 2026) where impersonators joined the Tamza Zoom with fake names, Max needs:

1. **A tightly controlled, secret distribution channel** for the rotating Zoom link - only verified real people get it. Not published openly on tamza.com.
2. **A Facebook group banner** made from the club's own event posters, spread across time (not just recent ones), varied types, with posters shown **whole - never cropped**.

A sub-goal expressed: eventually auto-send the rotating link to a curated list of ~100-150 trusted regulars, possibly using Telegram. SMS was explored and rejected.

---

## DECISIONS MADE + WHY

### Channel for secret link: PRIVATE TELEGRAM CHANNEL with admin approval

- **SMS rejected.** Research showed Russia blocks ALL business SMS by default (Aug 2025 law) AND blocks any SMS containing a URL as spam. Since the message IS a Zoom link, SMS-to-Russia is dead on every provider. Ukraine = best-effort with silent drops. Israel/Germany/US = fine but that's a minority of the audience. SMS is not the primary tool.
- **Telegram Channel chosen** because: free, the Russian-speaking club already lives on Telegram, it's one-way (admins post, members read), and a **private channel + invite link with "Request Admin Approval" ON** gives exactly the controlled-vet-one-by-one gate that Max needs against impersonators.
- **Not a Messenger group.** Facebook Messenger groups can't be one-way and have no message approval. Wrong tool.
- **Not a Facebook sub-group of the public group.** Sub-groups require parent-group membership, so a secret sub-group under a public parent leaks the boundary. Better: separate private+hidden group.
- **Facebook Group (separate, private) was created** as a parallel channel - admins-post-only, approve-to-join.

### The Telegram channel itself
- **Name:** ??????-????? (Thumbs and Zooms)
- **Owner:** Max Rempel's personal Telegram account (logged in via QR code in Playwright)
- **Created in the live Playwright session** - channel exists and is live.

### Invite link strategy
- **Two links exist on the channel.** The DEFAULT link (t.me/+-dawRmE72YswOTAx) has NO approval - anyone with it joins instantly. THIS LINK MUST NOT BE SHARED.
- **The approval-gated link** (t.me/+D7nxFaemjjRiNWUx) has "Request Admin Approval" ON - people only request; Max approves one by one. This is the one to distribute.
- **Friendly redirect deployed:** `https://tamza.com/telega` ? 302 redirects to the approval-gated invite link. Deployed via the Cloudflare Worker (`tamza_worker_live.txt`) by inserting a `/telega` route before the existing routes. All existing site routes verified intact (homepage, Kartoteka, data.json, /dezh - all 200).

### How the verify-then-approve workflow works
- Person contacts Max (voice message, known face, whatever) ? Max confirms they're real ? Max gives them `tamza.com/telega` ? they tap, request to join ? Max taps "Approve" in Telegram ? they're in the channel forever.
- After that, every rotating Zoom link gets posted once in the channel ? all approved members see it automatically. No re-verifying, no re-sending.
- Membership of the channel IS the trusted list. Remove anyone with one tap.

### Facebook account for automation
- **Rule added to global2.md:** Claude MUST use the dedicated **Max Steinberg** account (`maxsteinberg2@gmail.com`, Bitwarden "Steinberg 201904") for ANY Facebook automation (login, scraping, posting). NEVER use Max's main FB account (`max.rempel2@gmail.com`). Reason: automated logins risk security checkpoints / temporary locks, and Max can't afford that on his main account. The Steinberg account is the throwaway for Claude to take that risk.

### Facebook group banner - the long journey
- **First attempt was a disaster.** I center-cropped 10 text-heavy event posters into a 1640?856 grid. Every title became shredded half-words. Max: "cropping of the poster is super idiotic."
- **Rule saved to memory:** NEVER crop event posters or any text-bearing image in a collage/banner. ALWAYS fit each poster whole (full aspect ratio, letterbox on background). Also: ALWAYS look at the render before showing Max.
- **Time-spread required:** Not just the latest events - pick every ~2-3 weeks across the available range, varied types (concerts, ??????? ?? ??????, ??????????? ??????, birthday, different performers).
- **Source:** Only event covers from the `clubtamza` Facebook group's events page. The group has only ~12-14 Facebook event objects total, so that's the real ceiling.
- **Final chosen version: v08 - branded montage.** 14 whole posters, dense grid, framed with a **"???? ?????"** title band at top and **tamza.com** footer at bottom, cream/beige background, zero cropping, 1640?856 px. Every poster legible. Frame filled - no orphan rows, no dead space.

---

## CURRENT STATE

### Done
- **Telegram channel ??????-?????** created, live, Max is admin.
- **Approval-gated invite link** created.
- **tamza.com/telega** redirect deployed and verified (Cloudflare Worker, route `/telega` ? 302 to the approval link).
- **Max Steinberg FB account** joined the `tamzazoom` Facebook group - **pending Max's approval** (request shows "Cancel request" state).
- **FB group banner v08** built and saved - the branded, dense, no-crop montage. **Not yet uploaded to the group** (held off - it's a visible change, waiting for Max's final look).
- **Rule in global2.md:** use Steinberg account for FB automation.
- **Rule in memory:** never crop posters; always look at renders before showing Max.
- Playwright browser is **closed**, lock released.

### In flight / not yet touched
- **The ORIGINAL task is still undone:** tamza.com still has the old public Zoom link exposed on the "????? ? ?????" buttons. After the July 4 attack, this needs to be replaced with something that doesn't publicly leak the link. Max and Claude discussed replacing it with a notice pointing people to contact Max or subscribe to the newsletter. The text was drafted but never applied to the site.
- **The banner v08 has not been presented to Max for final approval** - he saw v06 ("It's better but... fill it up and put like three times more posters") and left. I responded to his "fill it up" by building v08 (branded, 14 posters, dense) while he was away. He hasn't seen v08 yet.

---

## EXACT NEXT STEP

**1. Show Max the banner v08 first** - let him see it and decide. The file is at:
`C:/claude_base/projects/tamza_fb_banner/output/tamza_fb_group_banner_BRANDED_1640x856_v08.jpg`
If he approves, upload it as the clubtamza group cover (or he does it manually - the Steinberg account may not have admin rights).

**2. Return to the original site-update task:**
- Figure out which pages/templates on `tamza.com` have the public Zoom "????? ? ?????" links.
- Replace them with the notice about the secret link, pointing to the newsletter or Max's contact info.
- The text drafted earlier (translated from session):
  > ?????? ?? ??? ?????? ????????? (??-?? ????????? ?????????). ???? ?? ?????? ????????, ????? ????????. ????? ???????? ?????? ?????? - ???????? ????? ???????: WhatsApp / Telegram / SMS / ??????????, +1 (585) 705-1400. ??????????? ?? ???????? - admin@tamza.com. ??? ????? ? Zoom ????????? ??????, ????? ?? ??????, ??? ?? ???????? ????????.

**3. Approve Max Steinberg (Max Rempel II) in the tamzazoom Facebook group** - the join request is pending.

---

## OPEN QUESTIONS

- ? Does Max want the **banner v08 as-is**, or adjustments? It uses all 14 available unique event posters. If he literally wants "3? more," the ceiling from events is hit - non-event images would be needed.
- ? Does Max want the FB group cover uploaded automatically (Steinberg account may lack admin rights), or manually?
- ? Where exactly on tamza.com are the "????? ? ?????" links? The worker routes requests; the link text may be in static HTML, worker JS, or an include. Need to locate.
- ? Does Max want the Telegram channel link posted as the first message in the channel, or wait?
- ? Is the **member list / database** being built in a parallel session (as Max mentioned)? That session's output will determine the invite workflow.

---

## KEY PATHS, IDs, AND NAMES

### Telegram
- Channel: **??????-?????** (private, admin: Max Rempel's personal Telegram)
- Approval-gated invite: `https://t.me/+D7nxFaemjjRiNWUx`
- Default (DO NOT SHARE) invite: `t.me/+-dawRmE72YswOTAx`
- Friendly redirect: `https://tamza.com/telega` ? 302 to approval link above

### Facebook
- Main group: `https://www.facebook.com/groups/clubtamza/`
- Secret group (for posting links): `https://www.facebook.com/groups/tamzazoom/`
- Claude's FB account: **Max Steinberg** / `maxsteinberg2@gmail.com` (Bitwarden: "Steinberg 201904")
- Main FB account (NEVER use for automation): `max.rempel2@gmail.com` (Bitwarden: "202602max.rempel2 Facebook")

### Zoom
- Tamza Zoom account: `admin@tamza.com` (Bitwarden: "Tamza zoom 202206")
- Current secret Zoom link (from the June 6 newsletter): Meeting ID 873 4648 6242, Passcode 44, link `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1`

### Files
- Banner output: `C:/claude_base/projects/tamza_fb_banner/output/tamza_fb_group_banner_BRANDED_1640x856_v08.jpg`
- Banner build script: `C:/claude_base/projects/tamza_fb_banner/scripts/build_banner_branded_v08.py`
- README: `C:/claude_base/projects/tamza_fb_banner/README.md`
- Worker source (live): `C:/Users/maxre/AppData/Local/Temp/claude/tamza_worker_live.txt`
- Worker deploy token: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/cloudflare_workers_kv_token_20260303.txt`
- Global rules: `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md`
- Session memory: `C:/Users/maxre/.claude/projects/C--claude-base/memory/MEMORY.md`
- Never-crop rule: `C:/Users/maxre/.claude/projects/C--claude-base/memory/feedback_never_crop_posters.md`
- Cloudflare Worker deploy reference: `C:/Users/maxre/.claude/projects/C--claude-base/memory/reference_tamza_worker_deploy_dezh.md`
- Bitwarden session file: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt` (session token may expire - may need `bw unlock` again)

### Bitwarden session
- Current BW_SESSION: `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==` (may be stale by the time this session resumes)

---

## GOTCHAS AND DEAD ENDS

- **SMS to Russia is dead.** Any URL-bearing SMS is spam-blocked by Russian carriers. Aug 2025 law blocks all A2P SMS by default. No provider (Twilio, Telnyx, Plivo, etc.) can reliably deliver a link to a Russian number. Do not attempt SMS for Russia.
- **Telegram bots cannot cold-message people.** Each person must tap "Start" on a bot first. The channel approach (invite link ? admin approval) works around this.
- **Private Telegram channels cannot have pretty/custom links.** A custom `t.me/Name` requires making the channel public, which removes the approval gate and makes it searchable. The ugly random hash is the price of secrecy + control.
- **Facebook Messenger groups cannot be one-way or moderated.** Messages post instantly; no approval queue; any member can post. Use a Facebook Group, not a Messenger chat.
- **Facebook sub-groups require parent-group membership.** A sub-group under a public parent is not a truly secret container. Use a separate private+hidden group instead.
- **The clubtamza Facebook group only has ~12-14 event objects.** The poster supply for the banner is finite. "3? more" than 9 means ~27, which requires either duplicates or non-event images.
- **Two event covers (the upcoming ones: July 4 charity concert + July 5 guitar circle) were login-blocked** - returned HTML login pages not images when fetched via the crawler endpoint. They couldn't be included.
- **Playwright browser sessions use a persistent profile at** `C:\claude_base\playwright_profile`. The Bitwarden extension only loads if the MCP server was launched with that config (needs a Claude Code restart to take effect). In this session, Bitwarden was NOT loaded in Playwright - QR login was used for Telegram, and manual password entry for Facebook.
- **The Cloudflare Worker deploy uses `sed` + `curl` with multipart/form-data.** Inserting a route requires careful boundary handling. The deploy token lives in the Nextcloud file above. The worker has bindings for MEDIA (r2), REPORTS (d1), and MAILHOOK_SECRET - all must be preserved on redeploy.
- **The original site-update task (hiding the public Zoom link) is still not done.** This is the actual security gap from the July 4 attack and should be priority zero when Max returns.
