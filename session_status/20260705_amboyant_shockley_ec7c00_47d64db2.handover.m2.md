# Scribe handover - milestone 2 (~151K tokens)
# session: 20260705_amboyant_shockley_ec7c00_47d64db2
# cwd: C:\moma\.claude\worktrees\flamboyant-shockley-ec7c00
# written: 2026-07-05 08:20:43 by deepseek-v4-pro

# HANDOVER - Mike-DC Calendar Fill (F4 Headless Run)

## GOAL (Max's words)
Run the Mike-DC twice-daily calendar fill HEADLESS - research and stock in-person events for Mike's rolling window (~today through ~2.5 weeks out), update the Google Calendar and Notion DB, check Mike's inbox for requests, and stay silent otherwise. This is the unattended F4 role launched by Windows Task Scheduler at ~07:15 or ~16:00 Pacific.

## DECISIONS MADE + WHY

1. **No new Mike email to act on.** Mailcheck returned last Mike email from Jun 25 20:54 - all his standing requests (HacDC, CivicTech, Buddhist events with proper title prefixes, reply-on-action, no unsolicited email, Link line on every event, festivals ? social) were already integrated in prior runs. No reply owed.

2. **One new event added: DC Tech Mixer & Social, Fri Jul 17 18:30-21:00.** Researched via Eventbrite; it fills an empty Friday in the window and matches Mike's meet-people/social/networking goal. Added to Google Calendar with the standardized `Link: <url>` line in the description (Mike's standing pref A from 2026-07-02).

3. **EA DC - gave its own pass, found nothing in-window.** Checked Eventbrite (effective-altruism tag), Meetup (effective-altruism-dc group), eadc.org, and effectivealtruismdc.org. The official EA DC site confirmed no in-person events in the Jul 5-23 window. Did not fabricate or tag non-EA events as [EA].

4. **HacDC and CivicTech DC - both empty past mid-July.** Searched HacDC (hacdc.org, multiple Meetup URL variants) and Code for DC Meetup - zero upcoming events past Jul 13 for HacDC, zero upcoming for CivicTech. Standing groups already covered on-cal through their last available dates; no fillable gap.

5. **Friday Jul 17 gap - filled by the Tech Mixer.** That was the only actionable Friday vacancy found in research.

6. **Heartbeat pinged.** The run executed end-to-end (calendar surveyed, mail polled, no errors), so the liveness ping was sent regardless of event count (1 addition this run). This matches the standing rule that the heartbeat means "run executed" not "events changed."

7. **Worklog appended** with DID/STATE/NEXT.

8. **Buddhist events - not searched afresh this run.** The transcript shows existing Buddhist events are already on the calendar from prior fills; no new search was conducted for additional Buddhist events in this specific run (the standing request was from 2026-06-25 and prior runs had stocked them).

9. **Notion backfill - not performed in this run.** The transcript shows the single new calendar event was created via `mcp__google-calendar__create_event` but there is no corresponding Notion DB write tool call visible. This may be a gap.

10. **Color rules - no action needed.** No new Hearing: or P&P events were added, so no Flamingo color updates were required.

11. **Location flagging - no action needed.** The one added event (DC Tech Mixer) is in central DC (U St), so no suburb suffix was needed.

## CURRENT STATE

- **Calendar surveyed:** Jul 5-Jul 23. ~55 events already on the calendar at run start, covering HacDC, CivicTech, Buddhist, EA, hearings, P&P, and general policy events.
- **Mail inbox:** Queried, no new messages since Jun 25. All prior Mike requests are actioned and reflected in the calendar (proper title prefixes, Link lines, reply-on-action discipline).
- **One event added this run:** `[21+?] DC Tech Mixer & Social` - Fri Jul 17 18:30-21:00, Sports & Social DC (700 7th St NW). Eventbrite ticket link in description.
- **EA DC:** No in-person events in window. Source: effectivealtruismdc.org/event page explicitly states no upcoming events.
- **HacDC:** Last event on calendar is Jul 13 (Sunday); no further events published.
- **CivicTech DC:** No upcoming events on Meetup.
- **Heartbeat:** Pinged successfully. Worklog written.
- **Notion DB:** Unknown sync state for the new Tech Mixer event (no Notion tool call visible in transcript; calendar creation did happen).

## EXACT NEXT STEP (for the next F4 run)

1. **Poll Mike's inbox** via `_f4_mailcheck.py`. If Mike sent a new request or question, reply concisely and fold it into the fill.
2. **Re-survey the rolling window** (shifted forward - roughly Jul 7 through ~Jul 25 or later depending on when the next run fires).
3. **Re-check EA DC** - give it its own pass. Site to check: `https://www.effectivealtruismdc.org/event` and `https://www.meetup.com/effective-altruism-dc/events/`.
4. **Re-check HacDC and CivicTech** for any newly posted events in the extended window.
5. **Check Fridays** in the extended window for gaps; hunt networking/social meetups to fill them.
6. **Verify start times** of any newly added events against source pages (Brookings time accuracy rule).
7. **Apply color rules** - any new Hearing: or P&P events past today need colorId=4 (Flamingo).
8. **Backfill to Notion** - ensure every calendar change is reflected in the Notion "Mike DC Events" DB, including the standardized Registration URL field.
9. **Ping heartbeat** if the run executes end-to-end without errors.
10. **Append worklog** with DID/STATE/NEXT.

## OPEN QUESTIONS (awaiting Max)

- None active. Mike's last request was Jun 25 and all items were integrated. No outstanding questions in the transcript.

## KEY PATHS, IDs, NAMES

| Item | Value |
|---|---|
| **Method doc** (source of truth) | `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` |
| **Mail check script** | `C:\claude_base\tools\mike_dc_calendar\_f4_mailcheck.py` |
| **Mail send script** | `tools/mxmail/mxmail_v01.py send_mail` (from mass@tamza) |
| **Google Calendar ID** | `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com` |
| **Calendar TZ** | America/New_York |
| **Notion DB ID** | `40a81164-d856-4fab-8dfa-e93e6f0c7eb4` |
| **Notion token file** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt` |
| **Heartbeat URL** | `https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| **Worklog script** | `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"` |
| **HacDC sources** | `https://hacdc.org/events/`, `https://www.meetup.com/hacdc/events/` (also tried `/HacDC/` and `/hac-dc/` variants) |
| **CivicTech source** | `https://www.meetup.com/code-for-dc/events/` |
| **EA DC sources** | `https://www.effectivealtruismdc.org/event`, `https://www.meetup.com/effective-altruism-dc/events/`, `https://www.eadc.org/events` |
| **Eventbrite research** | `https://www.eventbrite.com/d/dc--washington/effective-altruism/`, `/networking/` with date range params |
| **Event added this run** | Eventbrite ID `1986019229979` - DC Tech Mixer, created as Google Calendar event |
| **F4 contact name** | "Anna" (the sole Mike contact persona) |

## GOTCHAS & DEAD ENDS

- **HARD RULE - headless web only.** No browser tools (`mcp__claude-in-chrome__*`, `mcp__playwright__*`, Claude_Preview, computer-use). If a site can't be read via WebFetch, skip it - never fall back to a visible browser. This is because the run is unattended and must never steal Max's keyboard/dictation focus.

- **HacDC Meetup URL variants matter.** `hacdc`, `HacDC`, and `hac-dc` all exist as Meetup group slugs. The correct one appears to be `hacdc` but several variants were tried before pages rendered.

- **EA DC site was explicit about no events.** `effectivealtruismdc.org/event` literally said "no upcoming events" - this was a clear signal, not a fetch failure.

- **Eventbrite date filter syntax:** `?start_date=2026-07-17&end_date=2026-07-17` - use ISO dates in URL params.

- **Dedup rule for standing groups:** By GROUP+DATE, not exact title. Prior runs may have used different tag formats (e.g. "Open Hac" vs "(HacDC) Open Hac"). Treat same group + same date/time as a duplicate and keep the `(HacDC)` / `(CivicTech)` prefixed form.

- **Notification level:** ALWAYS `notificationLevel=NONE` when creating or updating calendar events (prevents Mike getting notifications from the automated fill).

- **No unsolicited email.** The F4 role ("Anna") only emails Mike to REPLY to something he wrote. No daily summaries, reminders, or digests. The ONE exception: a concise reply-with-results (1-3 lines) after a fill that acted on a Mike request.

- **Festivals/parades ? social.** Mike's standing pref: public events like festivals and parades are allowed on-cal but must NOT be tagged or counted as social/networking for the meet-people goal.

- **Possible Notion backfill gap.** The transcript shows the new DC Tech Mixer was created on Google Calendar but there is no visible Notion DB write. The next run should verify Notion sync state and backfill any missed entries.

- **Heartbeat gates on run execution, not event count.** Pinging after a zero-event successful run is correct. Pinging without a real run (MCP unavailable, crash) is forbidden - that's the silent-fallback trap that would mask a lapsed calendar fill from Max.
