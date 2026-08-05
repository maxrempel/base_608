# Tamza Weekly Video Copier — Design Draft

## 1. Concise Architecture and State Machine

The system is a **scheduled job** that runs every Tuesday at 01:00 America/Los_Angeles on the **Centauri Windows machine**. It relies on the existing `ytdow` pipeline (running on Lak) to deposit verified MKV files into a shared directory on Centauri. The job does **not** perform any download itself.

**Architecture overview:**

```
Lak (Linux)                    Centauri (Windows)
+------------------+          +------------------------+
| ytdow pipeline   | ---->    | Tamza backup area      |
| (source channel) |  MKV     | (verified files)       |
+------------------+          |                        |
                              | Weekly Copy Job        |
                              | - Discovery (YouTube   |
                              |   Data API)            |
                              | - Ledger (SQLite)      |
                              | - Telegram approvals   |
                              | - Upload (YouTube API) |
                              | - ffprobe validation   |
                              +------------------------+
```

**State machine for each candidate video:**

```
NEW ──> DISCOVERED ──> PENDING_APPROVAL ──> APPROVED ──> UPLOADING ──> UPLOADED_UNLISTED ──> PENDING_PUBLIC_APPROVAL ──> PUBLIC
         │                  │ (reject)                       │ (failure)                      │
         └── SKIPPED ──────┘                                └── FAILED ──────────────────────┘
```

- **NEW**: video ID not yet seen in ledger.
- **DISCOVERED**: found via YouTube Data API, candidate for this week.
- **PENDING_APPROVAL**: waiting for Max to approve via Telegram.
- **APPROVED**: human approval given, ready to upload.
- **UPLOADING**: upload in progress (resumable).
- **UPLOADED_UNLISTED**: upload succeeded, video is unlisted, waiting for second approval.
- **PENDING_PUBLIC_APPROVAL**: waiting for Max to approve making it public.
- **PUBLIC**: successfully made public.
- **FAILED**: upload or publication failed, will be retried (max 3 times) unless the state machine prevents duplicate entries.
- **SKIPPED**: rejected by human or outside weekly window.

## 2. Exact File Tree

```
tamza-copier/
├── config/
│   └── yt_api_key.json          # (external, not committed)
│   └── telegram_bot_token.txt   # (external, not committed)
│   └── settings.yaml            # channel IDs, timezone, etc.
├── src/
│   ├── __init__.py
│   ├── main.py                  # entry point (Scheduled Task calls this)
│   ├── discover.py              # fetches new streams from source channel
│   ├── approval.py              # Telegram bot interaction & state changes
│   ├── uploader.py              # YouTube Data API upload (resumable, unlisted)
│   ├── publicizer.py            # changes video visibility to public
│   ├── ledger.py                # SQLite CRUD, idempotency
│   ├── validator.py             # ffprobe validation of MKV
│   ├── notifier.py              # Telegram messages for start/finish/fail
│   └── dryrun.py                # dry-run discovery, ledger, local file check
├── data/
│   └── ledgers/
│       └── tamza_copier.db      # SQLite database (auto-created)
├── tests/
│   ├── test_discover.py
│   ├── test_ledger.py
│   ├── test_uploader.py
│   ├── test_validator.py
│   └── test_approval.py
├── requirements.txt
└── README.md
```

## 3. Python Module Boundaries and Command-Line Interfaces

### 3.1 Module responsibilities

| Module       | Responsibility                                                                 |
|--------------|--------------------------------------------------------------------------------|
| `main.py`    | Entry point. Reads config, initializes SQLite ledger, runs the weekly workflow. |
| `discover.py` | Uses YouTube Data API to list recent broadcasts from `@prostoproverka/streams`. Returns list of dicts (videoId, title, description, date, duration). Filters to today ±1 day window (Tuesday). |
| `approval.py` | Contains `ApprovalBot` class that uses python-telegram-bot to send approval requests to a predefined chat ID (Max). Waits for explicit reply (yes/no per candidate or batch). Updates ledger state. |
| `uploader.py` | Implements resumable upload using google-api-python-client. Assumes video file exists at a known path on Centauri (constructed from `ytdow` metadata). Validates with `validator.py`. Uploads as unlisted. Returns YouTube video ID. |
| `publicizer.py`| Updates video status from `unlisted` to `public` using YouTube API. Requires second approval via Telegram. |
| `ledger.py`   | SQLite database with table `videos` (source_video_id, state, yt_dest_id, title, description, upload_attempts, created_at, updated_at). Methods: `add_video`, `update_state`, `get_videos_by_state`, `get_video`. |
| `validator.py` | Calls `ffprobe` to check MKV file integrity (no corruption, expected duration within tolerance). Returns boolean. |
| `notifier.py` | Sends start/end/failure Telegram messages to Max using a simple bot token. |
| `dryrun.py`   | Performs discovery, ledger updates, and local file existence checks. Reports but does not upload or notify. Can be run with `--dry-run` flag. |

### 3.2 Command-Line Interfaces

`main.py` supports these modes (via argparse):

```
python src/main.py --dry-run           # only dry-run mode
python src/main.py --weekly            # full weekly job
python src/main.py --approve <video_id>        # mark one or more as approved (manual trigger)
python src/main.py --public-approve <video_id> # mark for publication
python src/main.py --status                     # print current ledger state
```

The Windows Scheduled Task runs `python src/main.py --weekly` every Tuesday at 01:00 America/Los_Angeles.

The Telegram bot part of `approval.py` runs asynchronously within `main.py`. The bot listens for Max’s replies (text commands like `/approve <video_id>`, `/approve_all`, `/skip`, `/public <video_id>`). The bot token and chat ID are read from external files.

## 4. Failure and Idempotency Rules

### 4.1 Idempotency via SQLite Ledger

- **Key**: `source_video_id` (string, unique).
- **Duplicate prevention**: On any action, first check if ledger entry exists. If yes and state is `PUBLIC`, skip entirely. If state is `FAILED`, retry only if `upload_attempts < 3`. Otherwise skip.
- **Resumable upload**: YouTube API resumable upload protocol. The uploader stores the upload URI in memory; if interrupted, on next run it can continue if the same source video is not yet in `UPLOADING` state. For simplicity, we assume the job always completes within one weekly run. If not, the upload restarts from scratch (but with a new upload attempt). The ledger ensures no duplicate destination videos because the YouTube video ID is stored on success.
- **State transitions are atomic**: SQLite transaction before and after each API call.

### 4.2 Failure scenarios

| Failure | Handling |
|---------|----------|
| `ytdow` file missing on Centauri | Log error, set state to `FAILED`. Will retry next week. |
| ffprobe validation fails | Log error, set state to `FAILED`. |
| YouTube API upload failure (non-resumable) | Increment `upload_attempts`. If <3, retry next week; else permanent skip. |
| Telegram bot offline | Approval pending; job continues but waits for manual approval on next run. Notifications queued? Not supported; next run will re-send if needed. |
| Network partition | Timeout and retry next week. |

- **Reboot safety**: SQLite ledger is written to disk. Job checks current state at start; any `UPLOADING` state older than 1 hour is considered stale and reset to `APPROVED` (to allow retry).
- **Bandwidth consciousness**: Upload is single-threaded; no parallel uploads. Dry-run does zero network.

## 5. Dependency List

```
# Python 3.10+
google-api-python-client>=2.86.0
google-auth-httplib2>=0.1.0
google-auth-oauthlib>=0.4.6
python-telegram-bot>=20.0
pyyaml>=6.0
pytz>=2022.1
ffmpeg-python>=0.2.0   # only for ffprobe wrapper (or subprocess call)
```

- `ffprobe` must be installed on Centauri (from FFmpeg binaries).
- External files: `yt_api_key.json`, `telegram_bot_token.txt`, `settings.yaml`.

## 6. Practical Implementation Draft and Tests

### 6.1 Implementation draft (core classes)

```python
# src/main.py (simplified)
import yaml
from pathlib import Path
from ledger import Ledger
from discover import SourceDiscoverer
from approval import ApprovalBot
from uploader import Uploader
from publicizer import Publicizer
from notifier import Notifier
from validator import FileValidator
import argparse

def main():
    args = parse_args()
    config = yaml.safe_load(Path("config/settings.yaml").read_text())
    ledger = Ledger(config["db_path"])
    notifier = Notifier(config["telegram_token"], config["max_chat_id"])

    if args.dry_run:
        from dryrun import DryRun
        dry = DryRun(ledger, config)
        dry.execute()
        return

    # Full weekly workflow
    if args.weekly:
        # 1. Discovery
        discoverer = SourceDiscoverer(config["source_channel_id"], config["youtube_api_key"])
        candidates = discoverer.get_candidates(weekday=2, timezone_str="America/Los_Angeles")
        for vid in candidates:
            ledger.add_video(vid)

        # 2. Initial approval
        bot = ApprovalBot(config["telegram_token"], ledger, config["max_chat_id"])
        bot.send_approval_requests(candidates)
        # Wait for replies (blocking, with timeout)
        approved = bot.wait_for_approvals(timeout=3600)
        # For simplicity, we process approved in the same run

        # 3. For each approved video, validate & upload
        for vid in approved:
            entry = ledger.get(vid)
            local_path = Path(config["storage_base"]) / f"{vid}.mkv"
            if not FileValidator.validate(local_path):
                ledger.update_state(vid, "FAILED")
                continue
            uploader = Uploader(config["youtube_auth"], config["destination_channel_id"])
            yt_video_id = uploader.upload_unlisted(local_path, entry.title, entry.description)
            if yt_video_id:
                ledger.update_state(vid, "UPLOADED_UNLISTED", yt_id=yt_video_id)
                notifier.notify_upload_success(vid, yt_video_id)
            else:
                ledger.update_state(vid, "FAILED")
                notifier.notify_upload_failure(vid)

        # 4. Second approval for public
        unlisted_videos = ledger.get_videos_by_state("UPLOADED_UNLISTED")
        for vid in unlisted_videos:
            bot.send_public_approval_request(vid)
        # Wait for replies
        public_approved = bot.wait_for_approvals(timeout=3600)
        publicizer = Publicizer(config["youtube_auth"])
        for vid in public_approved:
            entry = ledger.get(vid)
            if publicizer.make_public(entry.yt_dest_id):
                ledger.update_state(vid, "PUBLIC")
                notifier.notify_public(vid)
```

### 6.2 Tests

- `test_ledger.py`: unit tests for SQLite insert/update/get, duplicate prevention, state transitions.
- `test_discover.py`: mock YouTube API responses, test candidate filtering by weekday.
- `test_uploader.py`: mock youtube service, test that resumable upload returns video ID.
- `test_validator.py`: mock ffprobe output, test success/failure.
- `test_approval.py`: mock telegram bot, test approval flow.
- `test_main.py`: integration with mocked modules.

All tests run without network access.

## 7. Pilot and Deployment Checklist

### 7.1 Pilot steps

1. **Set up environment** on Centauri:
   - Install Python 3.10+, dependencies via `pip install -r requirements.txt`.
   - Place `ffprobe.exe` in PATH.
   - Create `config/` directory with external secrets.
   - Create `data/ledgers/` directory.

2. **Configure ytdow integration**:
   - Ensure `ytdow` deposits MKV files to `\\Centauri\Tamza_backup\<video_id>.mkv`.
   - Verify that `ytdow` uses the sam

[TRUNCATED: result exceeded 12000 characters]
