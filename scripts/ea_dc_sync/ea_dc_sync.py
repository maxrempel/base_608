#!/usr/bin/env python3
"""
EA DC -> Notion event sync.

Pulls the public "EA DC Events" Google Calendar (ICS feed) and adds any events
falling inside Mike's DC window to the Notion "Mike DC Events" database.

Design notes:
- Idempotent. Each created row stores the calendar event's iCal UID in the
  Notion "Source" field as "AUTOPULL uid=<UID> ...". A re-run skips any UID that
  already exists, so the job can run on a schedule forever without duplicating.
- Auto-pulled rows are tagged Origin = "Auto-pull: EA DC feed" (green), so they
  are visually + filterably separate from manual rows (Origin = "Manual entry").
- Never invents data. It only writes events that actually appear in the feed.
  As of creation (June 2026) the feed has nothing past May 27, so a live run is
  a clean no-op until EA DC posts the June/July events; then they appear
  automatically on the next run.

Run:
    python ea_dc_sync.py            # live: create missing rows, log result
    python ea_dc_sync.py --dry-run  # print what it would create, write nothing
    python ea_dc_sync.py --all      # ignore the date window (whole feed)

Token: Notion internal integration "Sol Sync 20260319", already shared with the
DB. Read from the shared creds file so it is not hard-coded here.
"""
import sys, json, datetime, urllib.request, urllib.error, os, re
try:
    from zoneinfo import ZoneInfo
    NY = ZoneInfo("America/New_York")
except Exception:
    NY = None

# ---- config ----
ICS_URL = ("https://calendar.google.com/calendar/ical/"
           "c_ad1b8fdbf4c2b7117d24b8176cd79d262dceafc02baa329317c989418772f9aa"
           "%40group.calendar.google.com/public/basic.ics")
DBID = "40a81164d8564fab8dfae93e6f0c7eb4"
TOKEN_FILE = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt"
EVENT_PAGE_BASE = "https://www.effectivealtruismdc.org/event"
# Mike's DC window (search window from the plan, with a small buffer).
WINDOW_START = datetime.date(2026, 6, 3)
WINDOW_END   = datetime.date(2026, 7, 31)

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')}  {msg}"
    print(line)
    with open(os.path.join(LOG_DIR, "ea_dc_sync.log"), "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_token():
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return f.read().strip().splitlines()[0].strip()


# ---- ICS parsing ----
def fetch_events():
    data = urllib.request.urlopen(ICS_URL, timeout=30).read().decode("utf-8", "replace")
    unf = []
    for ln in data.split("\n"):
        ln = ln.rstrip("\r")
        if ln[:1] in (" ", "\t") and unf:
            unf[-1] += ln[1:]
        else:
            unf.append(ln)
    events, cur = [], None
    for ln in unf:
        if ln == "BEGIN:VEVENT":
            cur = {}
        elif ln == "END:VEVENT":
            if cur is not None:
                events.append(cur); cur = None
        elif cur is not None and ":" in ln:
            k, v = ln.split(":", 1)
            cur[k.split(";")[0]] = v
    return events


def parse_dt(v):
    v = v.strip()
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%dT%H%M%S", "%Y%m%d"):
        try:
            return datetime.datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def ical_unescape(s):
    return (s.replace("\\,", ",").replace("\\;", ";")
             .replace("\\n", " ").replace("\\N", " ").replace("\\\\", "\\")).strip()


# ---- Notion ----
class Notion:
    def __init__(self, token):
        self.h = {"Authorization": "Bearer " + token,
                  "Notion-Version": "2022-06-28",
                  "Content-Type": "application/json"}

    def _req(self, method, path, body=None):
        req = urllib.request.Request("https://api.notion.com/v1/" + path,
                                     method=method, headers=self.h)
        if body is not None:
            req.data = json.dumps(body).encode()
        return json.loads(urllib.request.urlopen(req, timeout=30).read())

    def all_rows(self):
        rows, cur = [], None
        while True:
            body = {"page_size": 100}
            if cur:
                body["start_cursor"] = cur
            d = self._req("POST", f"databases/{DBID}/query", body)
            rows += d["results"]
            if d.get("has_more"):
                cur = d["next_cursor"]
            else:
                break
        return rows

    def existing_uids(self):
        uids = set()
        for r in self.all_rows():
            src = r["properties"].get("Source", {}).get("rich_text", [])
            txt = "".join(t["plain_text"] for t in src)
            m = re.search(r"uid=(\S+)", txt)
            if m:
                uids.add(m.group(1))
        return uids

    def create_event(self, props):
        return self._req("POST", "pages",
                         {"parent": {"database_id": DBID}, "properties": props})


def build_props(ev, dt):
    summary = ical_unescape(ev.get("SUMMARY", "Untitled EA DC event"))
    location = ical_unescape(ev.get("LOCATION", ""))
    uid = ev.get("UID", "").strip()
    raw = ev.get("DTSTART", "")
    is_dt = "T" in raw
    if is_dt:
        # Feed datetimes end in Z (UTC). Convert to America/New_York so Notion
        # displays the correct local DC time with an explicit offset.
        if raw.strip().endswith("Z") and NY is not None:
            aware = dt.replace(tzinfo=datetime.timezone.utc).astimezone(NY)
            start = aware.isoformat()
        else:
            start = dt.isoformat()
    else:
        start = dt.date().isoformat()
    source = (f"AUTOPULL uid={uid} | EA DC Google Calendar feed | "
              f"pulled {datetime.date.today().isoformat()}")
    props = {
        "Event Name": {"title": [{"text": {"content": summary}}]},
        "Date": {"date": {"start": start}},
        "Category": {"select": {"name": "Recurring meetup"}},
        "Cost": {"select": {"name": "Free"}},
        "Registration Type": {"select": {"name": "RSVP on platform"}},
        "Reliability": {"select": {"name": "Recurring - check next date"}},
        "Confidence": {"select": {"name": "Verified from official source"}},
        "Status": {"select": {"name": "Ready to register"}},
        "Origin": {"select": {"name": "Auto-pull: EA DC feed"}},
        "Official Site": {"url": EVENT_PAGE_BASE},
        "Source": {"rich_text": [{"text": {"content": source}}]},
    }
    if location:
        props["Venue"] = {"rich_text": [{"text": {"content": location}}]}
    return props, summary, start, uid


def main():
    dry = "--dry-run" in sys.argv
    take_all = "--all" in sys.argv
    log(f"=== EA DC sync start (dry_run={dry}, all={take_all}) ===")

    events = fetch_events()
    log(f"feed events fetched: {len(events)}")

    in_window = []
    for ev in events:
        dt = parse_dt(ev.get("DTSTART", ""))
        if not dt:
            continue
        d = dt.date()
        if take_all or (WINDOW_START <= d <= WINDOW_END):
            in_window.append((dt, ev))
    in_window.sort(key=lambda x: x[0])
    log(f"events in window {WINDOW_START}..{WINDOW_END}: {len(in_window)}")

    nt = Notion(get_token())
    have = nt.existing_uids()
    log(f"existing auto-pulled UIDs in DB: {len(have)}")

    created = 0
    for dt, ev in in_window:
        props, summary, start, uid = build_props(ev, dt)
        if uid and uid in have:
            log(f"  skip (exists): {start} {summary}")
            continue
        if dry:
            log(f"  WOULD CREATE: {start} {summary} | {ical_unescape(ev.get('LOCATION',''))}")
            continue
        nt.create_event(props)
        log(f"  CREATED: {start} {summary}")
        created += 1

    log(f"=== done. created {created} new row(s) ===")


if __name__ == "__main__":
    main()
