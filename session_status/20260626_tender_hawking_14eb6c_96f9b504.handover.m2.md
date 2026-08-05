# Scribe handover - milestone 2 (~159K tokens)
# session: 20260626_tender_hawking_14eb6c_96f9b504
# cwd: C:\claude_base\.claude\worktrees\tender-hawking-14eb6c
# written: 2026-06-26 07:30:43 by deepseek-v4-pro

# HANDOVER: Liz's German MSc Applications - Status Check

---

## GOAL (in Max's words)
"Check out the status of liz's applications" - then "doit" (login to Hannover portal to check for a decision not surfaced by email).

---

## DECISIONS + WHY

1. **Live DB queried alongside snapshot doc**: The master pointer doc (`LIZ_APPLICATIONS_SYSTEM_tomemex.md`) was from June 12 (two weeks stale). Max wanted the real current state, so both the snapshot and live D1 database were checked. They match exactly - nothing changed in the pipeline since June 12.

2. **Checked recent emails (since June 13)**: No new status emails arrived. Latest is the Dortmund portal login info from June 13. Gmail search confirmed this.

3. **Logged into the Hannover (LUH) QIS portal directly**: Because the admissions officer (Veronika Bonsch) promised "decisions by end of June" and today is June 26, but no email had arrived. The portal check was the logical escalation to catch a decision that email might have missed.

4. **No DB update made**: Since the portal showed no decision change either, the pipeline state is frozen. Nothing to write back.

5. **Browser closed after check**: Playwright session was explicitly closed to release the lock.

---

## CURRENT STATE

### The 5 Applications (live DB = June 12 snapshot - no changes):

| School | Programme | Status | Details |
|--------|-----------|--------|---------|
| **Hannover (LUH)** | AI-driven Mechatronics & Robotics | **PENDING** - this is the preferred one | App 94540635. Portal says: "processed, forwarded to admissions committee." No decision in portal or email. |
| **TU Dortmund** | Automation & Robotics | **PENDING** | Via uni-assist, in evaluation. Est. ~July 15. |
| **TH K?ln (Gummersbach)** | Automation & IT | **ADMITTED** | Official letter in hand. Enrollment deadline Aug 31. Seat held as backup. |
| RPTU Kaiserslautern | - | **REJECTED** | Incomplete: 2 recommendation letters never submitted. |
| Siegen | - | **REJECTED** | Generic rejection, no reason given. |

### Strategy
Hold the K?ln seat. If Hannover admits ? take Hannover. If Hannover rejects ? enroll K?ln by Aug 31. Dortmund is a tertiary option.

### Hannover Portal Details (as of June 26)
- **Login**: `qis.verwaltung.uni-hannover.de`
- **Username**: `94540635`
- **Token**: `5D7F61DB` (stored in `LIZ_APPLICATIONS_SYSTEM_tomemex.md`)
- **Account name**: Samuel Myakishev-Rempel
- **Programme**: M.Sc. Mechatronik und Robotik, Winter 26/27
- **Status text**: "Application received on time and has been processed. It is being forwarded to the admissions committee of your faculty for the decision."
- **Portal's own timeline text**: Winter applicants notified end-July to mid-September (written + electronic notice in portal)

### Timeline Tension
- **Veronika Bonsch (admissions officer)** said in writing (May 30): "decisions ready by end of June"
- **The portal itself** says: end-July to mid-September
- So "end of June" may slip. The portal is the ground truth until an email arrives.

---

## EXACT NEXT STEP

Nothing actionable right now. The only logical next action is:

> **Re-check the Hannover portal and/or Liz's email inbox in a few days.** Today is June 26. The stated deadline ("end of June") is in ~4 days. A re-check on June 30 or July 1 would be reasonable.

If Max wants, offer to set a self-wake / reminder. This was already offered at the end of the session and awaits his response.

If a decision appears in the portal before an email, update the database and notify Max immediately.

---

## OPEN QUESTIONS (awaiting Max)

1. **Self-wake / reminder**: Max was asked "Want me to set a self-wake to re-check the portal in a few days?" - no answer yet.
2. **Dortmund follow-up**: No action requested yet for the Dortmund application. It's just sitting there.
3. **K?ln enrollment**: No action requested yet. Deadline is Aug 31, so no urgency.

---

## KEY PATHS, IDS, COMMANDS

### Files
- **Master pointer doc**: `C:\Users\maxre\Nextcloud\2026 Applications as senior undergrad\LIZ_APPLICATIONS_SYSTEM_tomemex.md` - contains credentials, timelines, the full snapshot.

### Database (D1)
- Queried live via MCP tool `mcp__fee7c39e-4816-4a04-b41f-7067182da1c3__d1_database_query`
- Tables queried: applications, status_history, application_tracker
- Pipeline state is locked - no rows changed since June 12.

### Email
- Gmail searched via MCP tool for messages after June 13 - empty.
- Thread search for "Hannover admission" etc. - latest is May 31 confirmation, no decision.

### Hannover Portal
- **URL**: `https://qis.verwaltung.uni-hannover.de`
- **Credentials**: Username `94540635`, token `5D7F61DB`
- **Navigation path after login**: "Status Ihrer Bewerbung" ? "Bearbeitungsstatus" ? "Antr?ge" tab
- **MCP tools used**: `mcp__playwright__browser_navigate`, `browser_snapshot`, `browser_type` (fields: `asdf` and `f`), `browser_press_key` (Enter to submit), `browser_click`

---

## GOTCHAS

1. **Wrong portal URL initially**: Tried `uni-hannover.de/en/studium/bewerbung/online-bewerbung/` - that's a landing page, not the QIS portal. Found the correct URL by reading the original confirmation email (May 31 thread).

2. **Login form field names**: The QIS login form uses unconventional field names - `asdf` for username and `f` for password. `browser_fill_form` with `{"Username":"...", "Password":"..."}` didn't match; had to use explicit `browser_type` with correct `target` element refs.

3. **Overlay blocking click**: After filling the form, clicking "Anmelden" was blocked by an overlay. Workaround: pressed Enter key while focused in the password field.

4. **Timeline pessimism**: Don't assume Bonsch's "end of June" is binding. The portal's official text (end-July to mid-September) is the safer expectation. If nothing by July 1, it's probably slipped into the portal's standard window.

5. **Browser lock**: Playwright MCP session was explicitly closed. A future re-check will need to open a fresh browser session, navigate, and log in again.

6. **Stale snapshot risk**: The master pointer doc is now 2+ weeks old. Any future session should always query the live database first, not rely on the doc.
