# Scribe handover - milestone 3 (~258K tokens)
# session: 20260706_unruffled_mayer_13bd3b_fcca9c41
# cwd: C:\claude_base\.claude\worktrees\unruffled-mayer-13bd3b
# written: 2026-07-06 09:17:51 by deepseek-v4-pro

# HANDOVER - tamza.com secret Zoom link distribution

## GOAL (in Max's own words)
After a Zoom-bombing attack by agents of the state (GB/FSB) on July 4, 2026 - where impersonators joined with members' names and cameras off - the Zoom link must become **secret** and distributed only to a tightly controlled, personally verified list of ~100-150 trusted regulars. The link will rotate regularly.

**Max's words:** "?????????? ???????? (?????????, ???????) ? ????? ??? ?????? ? ?? ????, ?? ?????????. ????????? ?????? ?? ??? ??????? ????? ? ????? ? ?? ????? ?????? ??????????."

## DECISIONS MADE + WHY

1. **NOT SMS.** Researcher (agent task a9505eec9188da2d2) confirmed: Russia blocks all URL-bearing SMS as spam, plus an Aug 2025 Russian law blocks all A2P (business) SMS by default. Ukraine = best-effort/silent drops. SMS is dead for the main audience. Research report in full at the task output file path in the notification above.

2. **NOT a Telegram bot bulk-DMing.** Would require pacing to avoid spam-ban, phone numbers only weakly map to Telegram user IDs, and cold DMing has ban risk.

3. **Telegram private Channel** (not group, not bot) - **"?????-????"**. Channels are inherently one-way (only admins post, members just read). Private = not searchable, only reachable by invite link. With **"Request Admin Approval"** toggled ON, every join request waits for manual approval - Max's identity gate against impersonators.

4. **Friendly redirect: tamza.com/telega** - deployed to the live Cloudflare Worker (tamza.com), does a 302 redirect to the channel's approval-gated invite link. This gives a decent, easy-to-dictate URL instead of the ugly t.me/+hash link.

5. **One-time verify, forever deliver.** The model: Max verifies a person once (voice message, personal recognition) ? sends them the invite link ? approves ? they're in the channel forever. The rotating Zoom link gets posted once into the channel ? all approved members see it. No re-verification, no weekly re-sending, no database.

6. **Facebook Group** - Max created one independently in a parallel step. It's a separate container, not linked to the Telegram channel. Max declined Facebook sub-groups (because the existing Tamza Facebook group is public, and a sub-group would inherit public parent membership - not secret enough). A separate Private + Hidden group was recommended. Done.

## CURRENT STATE

**What is DONE:**
- Telegram private channel **??????-?????** created, owned by Max Rempel's personal Telegram account.
- Invite link with **admin approval ON**: `https://t.me/+D7nxFaemjjRiNWUx` (link name: "???? ? ??????????").
- **WARNING: the default/primary invite link** (`t.me/+-dawRmE72YswOTAx`) lets people join **without approval** - it MUST NOT be shared. Only use the approval link above.
- Friendly redirect **https://tamza.com/telega** ? 302 to the approval link. Deployed and verified (curl confirmed: 302 redirect working; homepage, Kartoteka, /dezh all 200 OK).
- Facebook Group created by Max (separately).
- Parallel session exists: b51b is building a contact database of ~200 phone numbers, which will become the source of truth for invite decisions.
- Playwright browser: **CLOSED**, lock released. Telegram login session preserved in profile for reuse.

**What is NOT done / in-flight:**
- The Telegram channel has **zero subscribers** besides Max (the owner). No invites have been sent yet.
- No message has been posted to the channel.
- No co-organizers/admins added to help with approval.
- The parallel session (b51b) building the contacts database is still in progress.
- The rotating Zoom link itself has not been distributed anywhere yet.

## EXACT NEXT STEP

**Immediate:** Nothing blocking. The channel and redirect are live and ready for use.

**Next action when Max is ready (ordered by priority):**
1. **Post the first message** - the current secret Zoom link (from the newsletter: `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` / Meeting ID: 873 4648 6242 / Passcode: 44) and any introductory text - into channel ??????-?????.
2. **Add co-organizers as admins** (if desired) to share the approval workload.
3. **Begin sending invites** to the first verified people. The friendly URL to give them: **tamza.com/telega**.
4. **Connect b51b's database** - once the contact DB is built in the parallel session, reconcile who's been invited, who's joined, who's still pending.

## OPEN QUESTIONS (awaiting Max)

1. Should we post the first Zoom link message now, or wait?
2. Which co-organizers should be added as channel admins? (?????? ????????-???????, ???? ??????, others?)
3. How to handle the **default (no-approval) invite link** - should we revoke/delete it entirely so it can't accidentally leak? (Currently both links coexist; the approval one is the one we created, the default one has no approval gate.)
4. Should the tamza.com website's "????? ? ?????" buttons be updated to point to tamza.com/telega instead of direct Zoom links? (The newsletter says the link should only go to ????????, not be public on the site.)

## KEY PATHS / IDs / NAMES

- **Telegram channel:** ??????-????? (private, owner: Max Rempel's personal Telegram)
- **Approval-gated invite link:** `https://t.me/+D7nxFaemjjRiNWUx`
- **Default (unsafe, no-approval) link:** `t.me/+-dawRmE72YswOTAx` - DO NOT SHARE
- **Friendly redirect:** `https://tamza.com/telega` ? the approval link (deployed on Cloudflare Worker)
- **Cloudflare Worker:** tamza worker, deployed via PowerShell using token from `C:/Users/maxre/Nextcloud/zSyncMain/ssh/cloudflare_workers_kv_token_20260303.txt`, bindings: MEDIA (r2), REPORTS (d1), MAILHOOK_SECRET
- **Current secret Zoom link (newsletter 6 July 2026):** `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` / ID: 873 4648 6242 / Passcode: 44
- **Bitwarden item:** "Tamza zoom 202206" (user: admin@tamza.com)
- **SMS research report:** at agent task output `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-serene-bardeen-4aa03c\5840f1e2-794c-45f4-bc18-4de58a59a8e3\tasks\a9505eec9188da2d2.output`
- **Parallel session b51b:** building contact database (b51c/b51g paired on bulletin board)
- **Branch bulletin:** b51g is the active name for this session on the broadcast board
- **Playwright profile:** persistent at `C:\claude_base\playwright_profile` (Telegram login saved; Bitwarden extension may/may not be loaded - needs verification on next restart)

## GOTCHAS / DEAD ENDS ALREADY RULED OUT

1. **SMS to Russia = dead.** Aug 2025 Russian anti-spam law blocks all A2P SMS. Additionally, any SMS containing a URL is classified as spam and blocked by Russian carriers. No provider can bypass this - it's the Russian network policy, not a vendor limitation. Do not revisit SMS for RU contacts.

2. **SMS to Ukraine = unreliable.** "Best-effort" delivery, ~$0.23/msg, silent drops common during wartime. Alphanumeric sender ID "TAMZA" supported but no guarantees.

3. **Beautiful custom Telegram link = impossible for private channels.** A pretty link like t.me/TamzaZoomy requires making the channel **public** (searchable, no approval gate). Our ugly t.me/+hash is the price of privacy and approval. The tamza.com/telega redirect solves the user-facing ugliness.

4. **Messenger group chat can't be one-way or moderated.** No message approval, join links bypass admin approval, anyone can post. That's why we went with Telegram Channel instead.

5. **Facebook sub-group of public parent = not secret.** Sub-groups require parent-group membership, so a public parent's audience bleeds in. Separate Private + Hidden group is the correct container.

6. **Bitwarden was not loaded in Playwright this session.** The MCP started without the Bitwarden extension. Max noticed - next session, verify `pw_mcp_config.json` is active and the persistent profile has the extension before driving. (For Telegram QR login it didn't matter, but for sites needing credentials it would.)

7. **Agent name changes this session:** started unnamed, registered as b21b, renamed to b51c, renamed to b51g. The bulletin board post to b51b was made as b51c. Current name is b51g.
