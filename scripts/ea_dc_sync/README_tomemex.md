# EA DC -> Notion event sync

Created 2026-06-02 by Claude Opus 4.8 (Claude Code on Pine) with Max.

## What it does

Pulls the public **EA DC Events** Google Calendar and adds any events inside
Mike's DC window to the Notion **Mike DC Events** database, automatically, on a
daily schedule. No browser, no manual clicking.

Part of Mike's DC summer 2026 walk-in networking plan (Notion: "2026-05-09 Mike
DC Networking Walk-In Only Plan").

## How auto-pulled events are separated from manual ones

The DB has an **Origin** column (added 2026-06-02):
- `Manual entry` (gray) -- rows a human/Claude added by hand. All 10 pre-existing
  rows were backfilled to this value.
- `Auto-pull: EA DC feed` (green) -- rows this script created.

So Max can filter/sort the DB and instantly see which events came from the feed
vs which were curated by hand.

## Source of truth

EA DC publishes a public Google Calendar ("EA DC Events"). Its ICS feed:

    https://calendar.google.com/calendar/ical/c_ad1b8fdbf4c2b7117d24b8176cd79d262dceafc02baa329317c989418772f9aa%40group.calendar.google.com/public/basic.ics

Found via the subscribe link on https://www.effectivealtruismdc.org/event
(Squarespace site; the `cid` on the page base64-decodes to the calendar id).

As of creation the feed had nothing past **May 27, 2026** -- EA DC posts events
about 3-5 weeks ahead. So live runs are a clean no-op until June/July events get
posted, then they appear in Notion automatically on the next daily run.

## Files

- `ea_dc_sync.py` -- the sync script.
- `logs/ea_dc_sync.log` -- append-only run log.

## Run manually

    python ea_dc_sync.py            # live
    python ea_dc_sync.py --dry-run  # show what it would create, write nothing
    python ea_dc_sync.py --all      # ignore the date window (whole feed)

## Idempotency

Each created row stores the calendar event's iCal UID in the Notion **Source**
field (`AUTOPULL uid=<UID> ...`). Re-runs skip any UID already present, so the
job never duplicates. Safe to run as often as you like.

## Window

`WINDOW_START` / `WINDOW_END` constants in the script. Currently
**2026-06-03 .. 2026-07-31** (Mike's DC stay). Edit these if the trip dates
change.

## Auth

Notion internal integration **"Sol Sync 20260319"** (already shared with the
DB). Token read at runtime from:

    C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt

Notion DB id: `40a81164d8564fab8dfae93e6f0c7eb4`.

## Schedule (Pine, Windows Task Scheduler)

Task name **`EA_DC_event_sync`**, daily at **07:30**, runs via `pythonw.exe`
(no console window pops up). StartWhenAvailable so a missed run (laptop asleep)
fires when the machine wakes.

Inspect / change:

    schtasks /query /tn "EA_DC_event_sync" /fo LIST
    schtasks /run   /tn "EA_DC_event_sync"     # run now
    schtasks /delete /tn "EA_DC_event_sync" /f # remove

Currently wired on **Pine only**. If Mike's work moves to another machine,
re-register the task there (the script + token are in Nextcloud-synced paths,
but the Task Scheduler entry is per-machine).

## To extend to other feeds

The same pattern works for any public Google Calendar / ICS source (e.g. a Luma
city calendar). Copy the script, swap `ICS_URL`, adjust `Category`/`Source`
labels. Keep the Origin tag distinct per feed if you want to tell them apart.
