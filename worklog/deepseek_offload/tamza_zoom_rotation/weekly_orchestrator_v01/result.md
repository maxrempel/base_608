# Result: Weekly Zoom Rotation Orchestrator Design

## 1. State Machine & Weekly Timing

### States (persisted in `state.json`)

| State | Meaning |
|-------|---------|
| `PENDING` | Initial or after reset; no actions taken |
| `DOC_UPDATED` | Google Doc advanced to new week/link |
| `TELEGRAM_POSTED` | Telegram message sent |
| `FACEBOOK_PREPARED` | Facebook post text & metadata written |
| `COMPLETE` | All destinations reached |

State also stores:
- `last_completed_week` (integer 1‑8)
- `next_week` (integer)
- `next_link` (string)
- `telegram_message_id` (optional, for verification)
- `facebook_output_path` (if required by external scheduler)

### Weekly Trigger

Run once per week via cron/systemd timer (e.g. Monday 09:00 UTC).  
The orchestrator reads the Google Doc to determine the current week displayed.  
**Only runs successfully if `current_week == last_completed_week + 1` (mod 8)**.  
If gap detected, exits nonzero and logs manual intervention required.

---

## 2. Invariants & Failure/Retry Behaviour

### Invariants

1. **Idempotent per step** – each step is attempted only if its state flag is absent.
2. **Doc update is guarded** – the Google Doc script is called only when state is `PENDING`
   and the doc’s current week matches the expected old week.
3. **Telegram post is guarded** – only called when state is `DOC_UPDATED` (or `PENDING` if
   doc already advanced in a previous partial run? No – doc must be updated first).
4. **Facebook output** – pure text production, always safe, last step.
5. **Atomic lock** – OS-level lock file prevents concurrent runs.
6. **Week alignment** – orchestrator will *not* advance doc if the doc has been manually
   moved forward more than one week; instead it fails loudly.

### Failure & Retry

| Scenario | Behaviour |
|----------|-----------|
| Doc update fails | State stays `PENDING`; next run retries doc update. |
| Telegram post fails | State stays `DOC_UPDATED`; next run retries Telegram. |
| Facebook output fails | State stays `TELEGRAM_POSTED`; next run retries only Facebook output. |
| Lock file held | Second process exits 1 after timeout; logs warning. |
| Week mismatch (doc already advanced manually) | Log error, exit 1. |
| State file missing/corrupt | Treat as empty `PENDING`; read doc and proceed (assume first run). |
| Telegram duplicate prevention | Use week‑specific message identifier; store Telegram message ID in state after success; on retry, check for existing message ID (optional). |

### Exit Codes

- 0  → full success or idempotent skip (already done)
- 1  → partial failure (one or more steps still pending after this run)
- 2  → lock contention / timeout
- 3  → week alignment error / manual intervention needed

---

## 3. Compact Implementation Blueprint

```python
# orchestrator.py (new file)

import json, os, sys, time, logging, fcntl, argparse
from pathlib import Path

# -------------------------------------------------------------------
# Existing tools imported as modules (assumed refactored)
from update_mailing_doc_v01 import advance_doc
from telegram_post_v01 import post_telegram
from google_docs_api_v01 import read_current_week
from rotation_links_v01 import ROTATION  # list of 8 links

# -------------------------------------------------------------------
# Constants
STATE_FILE = "/var/lib/tamza/orchestrator_state.json"
LOCK_FILE  = "/var/run/tamza_orchestrator.lock"
FACEBOOK_OUTPUT_DIR = "/var/lib/tamza/facebook_posts/"

# -------------------------------------------------------------------
# Helper functions

def load_state() -> dict:
    """Load state from STATE_FILE; return default if missing."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'status': 'PENDING', 'last_completed_week': 0, 'next_week': None, 'next_link': ""}

def save_state(state: dict):
    """Atomically write state to STATE_FILE (replace via rename)."""
    tmp = STATE_FILE + ".tmp"
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)

def acquire_lock() -> bool:
    """Try to acquire exclusive lock on LOCK_FILE; return True if success."""
    try:
        fd = open(LOCK_FILE, 'w')
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except (IOError, BlockingIOError):
        return None

# -------------------------------------------------------------------
# Core orchestration steps (each idempotent when guarded by state)

def step_read_current_week(state: dict, dry_run: bool = False) -> dict:
    """Read Google Doc and compute expected next week."""
    if state['status'] not in ('PENDING',):
        return state  # already beyond this step

    current_week, current_link = read_current_week()
    expected_old_week = state['last_completed_week'] % 8
    if state['last_completed_week'] == 0:
        expected_old_week = current_week  # first run assumes doc is correct
    elif (current_week % 8) != ((expected_old_week + 1) % 8):
        logging.error(f"Week alignment error: doc shows week {current_week}, expected {expected_old_week+1}")
        sys.exit(3)

    state['next_week'] = (current_week % 8) + 1   # 1..8
    state['next_link'] = ROTATION[state['next_week'] - 1]   # list is 0‑indexed
    return state

def step_advance_doc(state: dict, dry_run: bool = False) -> dict:
    if state['status'] != 'PENDING':
        return state
    if dry_run:
        logging.info("DRY RUN: would advance doc to week %d", state['next_week'])
        state['status'] = 'DOC_UPDATED'   # in dry-run we still mark (for testing)
        return state
    success = advance_doc(new_week=state['next_week'], new_link=state['next_link'])
    if not success:
        logging.error("Failed to advance Google Doc")
        sys.exit(1)
    state['status'] = 'DOC_UPDATED'
    save_state(state)
    return state

def step_post_telegram(state: dict, dry_run: bool = False) -> dict:
    if state['status'] not in ('DOC_UPDATED',):
        return state
    message = f"Zoom link for Week {state['next_week']}: {state['next_link']}"
    if dry_run:
        logging.info("DRY RUN: would post to Telegram: %s", message)
        state['status'] = 'TELEGRAM_POSTED'
        state['telegram_message_id'] = None
        return state
    msg_id = post_telegram(message)
    if msg_id is None:
        logging.error("Failed to post to Telegram")
        sys.exit(1)
    state['telegram_message_id'] = msg_id
    state['status'] = 'TELEGRAM_POSTED'
    save_state(state)
    return state

def step_produce_facebook(state: dict, dry_run: bool = False) -> dict:
    if state['status'] not in ('TELEGRAM_POSTED',):
        return state
    text = f"Join us for Week {state['next_week']} of Tamza! Zoom link: {state['next_link']}"
    metadata = {"week": state['next_week'], "link": state['next_link'], "timestamp": time.time()}
    if dry_run:
        logging.info("DRY RUN: facebook text and metadata generated")
        state['status'] = 'FACEBOOK_PREPARED'
        return state
    out_file = Path(FACEBOOK_OUTPUT_DIR) / f"week_{state['next_week']}.json"
    with open(out_file, 'w') as f:
        json.dump({"text": text, "metadata": metadata}, f)
    state['facebook_output_path'] = str(out_file)
    # Mark as FACEBOOK_PREPARED; external scheduler reads the file and posts.
    # We will consider the run complete only after the external scheduler confirms (optional).
    state['status'] = 'COMPLETE'
    state['last_completed_week'] = state['next_week']
    save_state(state)
    return state

# -------------------------------------------------------------------
# Main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='No external effects')
    parser.add_argument('--force', action='store_true', help='Ignore lock and week alignment (admin use)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    lock_fd = acquire_lock()
    if lock_fd is None and not args.force:
        logging.error("Another instance is running. Exit 2.")
        sys.exit(2)

    try:
        state = load_state()
        logging.info("Current state: %s", state)

        # If already COMPLETE for this week, just exit 0
        if state['status'] == 'COMPLETE':
            logging.info("Week %d already completed. Exiting.", state['last_completed_week'])
            sys.exit(0)

        state = step_read_current_week(state, args.dry_run)
        state = step_advance_doc(state, args.dry_run)
        state = step_post_telegram(state, args.dry_run)
        state = step_produce_facebook(state, args.dry_run)

        if state['status'] == 'COMPLETE':
            logging.info("Orchestration complete for week %d", state['next_week'])
            sys.exit(0)
        else:
            logging.warning("Orchestration partially complete, status=%s", state['status'])
            sys.exit(1)

    finally:
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()

if __name__ == '__main__':
    main()
```

### Function Boundaries (per module after refactoring)

| Function | Existing Script | Purpose |
|----------|----------------|---------|
| `read_current_week()` | `google_d
