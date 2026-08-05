# Scribe handover - milestone 2 (~156K tokens)
# session: 20260710_sleepy_feistel_3e6add_2fe6e5f9
# cwd: C:\claude_base\.claude\worktrees\sleepy-feistel-3e6add
# written: 2026-07-10 13:53:12 by deepseek-v4-pro

# HANDOVER - Facebook Group "?????-????" auto-approval problem

---

## GOAL (Max's words)
"I requested that all members should be approved. It's a closed group, invisible, and all members should be approved by the administrators, moderators, but the members still sneak in and get pre-approved ... I need to approve anyone, everyone, absolutely. There should be no exceptions."

Find the bypass, kill it, so that every joiner waits for Max's manual approval.

---

## DECISIONS + WHY

1. **Logged into the Steinberg Facebook account** (not Max's main one) because Max sent an admin invite to that account and told us to accept it and investigate from there.

2. **Checked core membership settings first** - they were fine: only admins/mods approve, nobody preapproved, group private+hidden. The request gate was on; the leak was elsewhere.

3. **Found the real culprit in Admin Assist** - a rule that auto-approved anyone with **5 or more friends already in the group**. This was acting as a silent robot admin, overriding all manual-approval settings. We deleted that rule immediately. Reasoning: the rule is the only plausible explanation for members "just jumping in" without any approval notification, and matches the "new profiles get pre-approved" symptom Max described.

4. **Kept a decline rule** (auto-reject profiles younger than 24 months) because it only blocks, it doesn't approve.

5. **Identified a remaining legitimate bypass**: invites. If Max or any existing member sends an invite to someone and they accept, they join instantly - no approval queue. That's how some members show "invited by Max." This is a feature, not a bug, but may need to be restricted.

---

## CURRENT STATE

- Steinberg account is **logged in**. Playwright Chromium browser window is open, sitting somewhere on the group page (last visible was after deleting the rule, showing Admin Assist with the "Approve member request if" slot empty).
- The **auto-approve leak is fixed** - the 5-friend rule is deleted. No Admin Assist approval criteria remain.
- Core settings confirmed correct and untouched.
- A question is **pending with Max**: "Do you want me to also turn off member invites (so only admins can invite), so that truly nothing but your manual approval lets anyone in?"
- We are waiting for Max's response.

---

## EXACT NEXT STEP

Resume the conversation: ask Max for a decision on the pending invite question. If he says yes:
- Navigate to Group Settings ? Membership, find the "Who can invite members" control, set it to "Only admins."
- Verify the change, then report back.

If he says no or doesn't care, we can close the browser, or leave it open for further tasks.

No other tasks are queued.

---

## OPEN QUESTIONS

- **Invite permissions**: Should Max restrict invitations to admins only, to close the last way people can join without approval? (Max's choice, pending.)

---

## KEY PATHS AND IDS

- **Group**: "?????-????", group ID `1812867806817312`, URL `https://www.facebook.com/groups/tamzazoom`
- **Admin Assist page**: navigated to via group sidebar (left menu) ? "Admin Assist" (showed "3 actions, 3 criteria" at the time). The rule we deleted was under "Manage people" ? "Approve member request if ... person has 5 friends or more in the group."
- **Steinberg account credentials**: stored somewhere in the session's environment; not needed for next step since browser is already logged in.
- **Playwright browser**: open, logged in. Use `mcp__playwright__browser_navigate`, `browser_snapshot`, `browser_click`, `browser_find` to interact.

---

## GOTCHAS

- **The 5-friend auto-approve rule** is the hidden approval bypass Max couldn't find. It lives in Admin Assist, not the main Membership Settings. Any similar investigation should always check Admin Assist for any approval criteria.
- **The CAPTCHA on login** required Max to manually solve an image challenge ("motorcycles"). If the session logs out, another CAPTCHA is likely, and we'll need Max to solve it again.
- **Plain group URL is not an invite link** - Max correctly suspected that. The real leak was Admin Assist, not the link. The link only makes the group findable (in a hidden group, it's already hidden from search, but direct URL can still be shared).
- **The activity log** (Admin Activity Log) would have shown "Approved by Admin Assist" for those mystery joins, which would have revealed the rule faster. In future, always check the log for one suspicious member to see *what* approved them.

