# Scribe handover - milestone 5 (~81K tokens)
# session: 20260611_some_grothendieck_db17dd_15179594
# cwd: C:\claude_base\.claude\worktrees\awesome-grothendieck-db17dd
# written: 2026-06-11 15:51:08 by claude-opus-4-8

# HANDOVER - Liz/Samuel German MSc Application Strategy

## GOAL (in Max's words)
"Go figure out Liz's Samuel's applications." Liz (Samuel Myakishev-Rempel) applied to several German Master's programs. She got an acceptance from K?ln that demands she commit within a week, but her preferred university is Hannover. Max's core question: "What's the strategy? Should Liz accept K?ln and then withdraw or not?" Now the work has expanded to: check all the application emails in the emm@ mailbox, and help reply to the K?ln offer from the correct address. Latest instruction: "open all relevant emails of course" - meaning open the TU Dortmund portal emails (and any other relevant ones) to find out if Dortmund is a new offer.

## DECISIONS + WHY
- **Strategy = accept K?ln now, withdraw later if Hannover comes through.** Reasoning: in Germany, accepting an admission offer is not binding like a US deposit. No blacklist, no shared database, students routinely hold multiple offers. The only money at risk is the ~300 EUR Semesterbeitrag paid at enrollment, and that comes weeks later and is mostly refundable before the semester starts.
- **K?ln offer is explicitly "non-binding"** - confirmed from Prof. Freiburg's email. Replying "yes" costs nothing and just holds the seat; real enrollment + fee happens later.
- **Reply should come FROM emm@transposon.org** - that is the dedicated mailbox Samuel applied with for all the German applications. It forwards into max.rempel2@gmail.com (that's why Freiburg's mail showed up in Max's Gmail).
- **Strategy is now even safer than originally thought:** Hannover decides by END OF JUNE (not July-August as first assumed). So K?ln's ~June 17 reply deadline and Hannover's answer land within ~2 weeks of each other, before any K?ln fee is ever due.

## CURRENT STATE
- Max already forwarded the full Claude-drafted advice + ready-to-send acceptance text to Liz and Oksana at 8:04 AM (email + Discord versions). That message is out.
- Max set up emm@transposon.org as a "Send mail as" alias in his own Gmail (with the Scribe/Claude walking him through Settings > Accounts and Import) and confirmed he successfully sent a test from his Gmail.
- A test "please ignore" letter was sent earlier to max@tamza.com to verify the signature handling - it went FROM mass@tamza.com (not emm@), signed plainly as "Samuel Myakishev-Rempel" with NO robot/AI signature. The auto AI-signature block was successfully suppressed.
- The emm@transposon.org password was provided by Max and saved to the MXroute creds file.
- The emm@ inbox was read via IMAP. Status of all German applications confirmed:
  - **K?ln (TH K?ln, Gummersbach):** offered, NON-BINDING, reply due ~June 17. Master of Engineering in Automation & IT, starts Oct 2026.
  - **Hannover (LUH):** PENDING, decision by end of June. THE PREFERRED ONE. App #94540635, M.Sc. AI-driven Mechatronics & Robotics, Winter 2026/27. Admissions officer Veronika Bonsch wrote (May 30): decisions ready by end of June.
  - **RPTU Kaiserslautern:** rejected (May 28).
  - **Siegen:** likely rejected - status change / new portal doc June 3.
  - **TU Dortmund:** sent Campusportal login details TODAY (June 11) - NEW, unread, may be a fresh offer or next step.

## EXACT NEXT STEP
Open the TU Dortmund Campusportal email(s) in the emm@transposon.org inbox (via IMAP, using the mxmail tool) and determine whether Dortmund is a new admission offer or just a routine portal-setup step. Also open any other relevant unread emails. Report findings to Max.

## OPEN QUESTIONS AWAITING MAX
- Whether to actually send the K?ln acceptance now (and from where - emm@ via tool, or Max sends from his Gmail alias himself). Not yet sent.
- What Dortmund's portal email actually means - pending the open.

## KEY PATHS / IDS / CREDENTIALS
- Mail tool: `C:\claude_base\tools\mxmail\mxmail_v01.py` (function `send_mail`); run from `C:/claude_base/tools/mxmail`. Use `PYTHONIOENCODING=utf-8` for IMAP reads (German chars).
- Creds file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\mxroute_smtp_creds_20260528.txt`
- emm@transposon.org password: `TT2w3e4r5t6y=` (saved to creds file)
- Application mailbox: emm@transposon.org (forwards to max.rempel2@gmail.com)
- Other available send addresses: mass@tamza.com and tamza.com mailboxes
- K?ln contact: Prof. Dr. Michael Freiburg, michael.freiburg@th-koeln.de, Institute of Automation & Industrial IT, TH K?ln, Steinmuellerallee 1, 51643 Gummersbach
- Applicant name for signatures: Samuel Myakishev-Rempel
- Max: max.rempel2@gmail.com, max@tamza.com, +1(585)705-1400
- Hannover: officer Veronika Bonsch, app #94540635

## GOTCHAS / DEAD ENDS RULED OUT
- Freiburg's email had NO visible To: address - it was BCC'd to all admitted applicants. This is normal, not a red flag, and does NOT tell us which mailbox received it. Don't chase this; the reply just goes from emm@ regardless.
- **Do NOT include any AI/robot signature** in real outgoing mail. The mxmail tool auto-appends a "Claude ... AI assistant" block by default - it must be suppressed. Max is specifically worried about a wrong signature or "you are a robot" slipping in. Real letters sign as Samuel Myakishev-Rempel only.
- Originally assumed Hannover decides July-August - CORRECTED to end of June. Use end-of-June everywhere.
- Earlier the tool could only send from mass@tamza.com, not emm@ (password wasn't on file). That's now resolved - emm@ password is saved.
- Environment: Chrome/phone, no python servers running on Max's side; Scribe runs tools locally. Connectors available: Notion, Memex, Gmail, Calendar, Drive, Cloudflare, Babel.
