# Scribe handover - milestone 1 (~109K tokens)
# session: 20260710_sleepy_feistel_3e6add_2fe6e5f9
# cwd: C:\claude_base\.claude\worktrees\sleepy-feistel-3e6add
# written: 2026-07-10 12:45:56 by deepseek-v4-pro

# HANDOVER - Facebook Group Auto-Approval Bug Investigation

---

## GOAL (in Max's own words)

Max runs a private, invisible Facebook group called **?????-????** (URL: `facebook.com/groups/tamzazoom`). He set it so **every single member must be manually approved by an admin or moderator - no exceptions.** Despite this, people are "sneaking in" and getting auto-approved without anyone clicking an approval button. He wants to know why this is happening and how to block ALL automatic entry so he alone controls who joins.

Quote: *"I need to approve anyone, everyone, absolutely. There should be no exceptions."*

---

## DECISIONS + WHY

1. **The public group URL (`facebook.com/groups/tamzazoom`) is NOT the culprit.** Max posted this plain group URL publicly, but it's just a regular group address - it lets people find and request access, it does not itself approve them. The distinction between "invite link" (a special Facebook-generated token link) and "regular group URL" was established.

2. **Systematic checklist was provided and ruled out item by item:**
   - **"Who can approve member requests"** ? must be "Only admins and moderators" (not "Anyone in the group")
   - **"Who is pre-approved to join"** ? must be empty (no pre-approved groups, files, or lists)
   - **Admin Assist rules** ? every rule under "Approve member request if..." must be **deleted entirely**, not just turned off. This was flagged as a critical gotcha from user reports.
   - **Invite with link toggle** ? must be OFF (separate from the regular group URL; this is a Facebook-generated invitation link)
   - **Page-linked automatic invites** ? if the group is connected to a Facebook Page, switch to the Page profile and disable "Automatic Invites" under Page ? Groups ? three dots

3. **Admin Activity Log was identified as the single source of truth.** For any suspicious new member, the log should say WHO or WHAT approved them (Admin Assist, another admin/moderator, preapproval, invite link, etc.). This hasn't been checked yet.

4. **Max's suspicion - Facebook bug.** After reviewing all settings, Max believes none of his settings should allow auto-approval, yet people "just jump in." He suspects the platform is broken. The session was in the middle of searching for user reports confirming this when interrupted.

---

## CURRENT STATE

- All Facebook settings have been reviewed verbally.
- Max confirmed the group shows 6 members, with 5 new members joining this week (Tuesday-recent), and 2 invitations showing as "Invited by Max Rempel" (the two ????? ??????? accounts - one possibly a duplicate).
- The group structure: Max Rempel is sole admin. One pending admin invite (Max Rempel II). No moderators active.
- **Admin Activity Log has NOT been checked yet** - this is the critical missing piece.
- **Admin Assist rules have NOT been visually confirmed as deleted** - only talked about.
- Web search was interrupted mid-flight; Claude was looking for user reports of this exact "auto-approval despite correct settings" bug.

---

## EXACT NEXT STEP

1. **Open Admin Activity Log** for the group and inspect how the 5 new members were approved. Look for entries like:
   - "approved by Admin Assist"
   - "approved by [name]"
   - "joined via invite link"
   - "pre-approved"
   
   This will immediately reveal the bypass mechanism. If it says "Admin Assist," then rules exist despite settings looking clean. If it says nothing or shows a contradiction with settings, that's strong evidence of a Facebook bug.

2. **Resume the interrupted web search** for recent Facebook user reports / Reddit threads / Meta Community forums documenting auto-approval bugs where members bypass admin approval in private groups despite all correct settings. Look for keywords like: *"facebook private group members auto approved without admin" "facebook group bypass approval bug 2025 2026" "members joining without request private group"*

3. **If Admin Assist shows no rules but members still auto-join:** Document the bug with screenshots and consider filing a Meta bug report or posting in the Meta Community Forums.

---

## OPEN QUESTIONS (awaiting Max)

- What does the **Admin Activity Log** actually say about the 5 new members? Who/what approved them?
- Has Max physically gone into **Admin Assist ? Manage people ? Approve member request if...** and confirmed there are zero rules listed? Not just toggled off - actually deleted?
- Is this group connected to a Facebook **Page**? If so, has the Page-level "Automatic Invites" setting been checked?
- Who invited the two ????? ??????? accounts? The log says "Invited by Max Rempel on Monday" - did Max actually send those invitations?

---

## KEY PATHS / IDS

- **Group:** ?????-???? (tamzazoom)
- **Group URL:** `https://www.facebook.com/groups/tamzazoom`
- **Admin:** Max Rempel (sole admin, digital creator, 5,429 followers)
- **Member count:** 6
- **New members this week:** 5 (Igor Li, Lilya Te, ??????? ????????, Ann Nelasa, + 2 invited ????? ??????? accounts)
- **Pending admin invite:** Max Rempel II
- **Group created:** July 6, 2026

---

## GOTCHAS

- **The "regular group URL vs. invite link" confusion was resolved.** The public `facebook.com/groups/tamzazoom` URL is harmless - it's not a token-based invite link. No need to delete the public post sharing it, though keeping it private adds safety.
- **Admin Assist rules must be DELETED, not just toggled off.** User reports and Meta documentation both confirm that merely disabling rules is insufficient; they must be removed entirely.
- **Facebook Page-linked groups have a separate hidden auto-invite setting.** If the group was created under or linked to Max's Facebook Page, there's a separate "Automatic Invites" menu accessible only when switched into the Page profile that can silently add members.
- **The two ????? ??????? accounts appear to be duplicates** (same name, same join date, both "Invited by Max Rempel on Monday"). This may be a display bug or an actual duplicate invitation.
- **Session was interrupted before confirming the root cause.** The working theory from Max is "Facebook bug," but the Admin Activity Log will provide the definitive answer.
