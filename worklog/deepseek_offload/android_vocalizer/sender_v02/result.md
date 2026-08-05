```markdown
# /android_vocalizer.py

```python
#!/usr/bin/env python3
"""
Android Vocalizer sender - a command-line tool to push notifications via ntfy.sh.

Supports setup of private configuration and sending messages with optional
priority, title, and call request. Uses only standard library modules.
"""

import argparse
import json
import os
import secrets
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Optional, Tuple

# Exit codes
EXIT_SETTINGS = 1
EXIT_VALIDATION = 2
EXIT_NETWORK = 3
EXIT_REMOTE = 4

DEFAULT_CONFIG_PATH = os.path.join(
    os.environ.get("USERPROFILE", os.path.expanduser("~")),
    "Nextcloud",
    "zSyncMain",
    "ssh",
    "android_vocalizer_config_v01.json",
)
DEFAULT_BASE_URL = "https://ntfy.sh"
DEFAULT_TIMEOUT = 15


def create_default_config(path: str) -> None:
    """
    Create a default configuration file at `path` with atomically exclusive creation.
    If the file already exists, do nothing. On Windows, try to set user-only permissions.
    """
    config = {
        "base_url": DEFAULT_BASE_URL,
        "topic": secrets.token_hex(16),
        "bearer_token": "",
        "call_enabled": False,
        "timeout_seconds": DEFAULT_TIMEOUT,
    }
    # Atomic exclusive creation
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return
    except OSError as e:
        raise RuntimeError(f"Failed to create config file: {e}") from e

    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Best-effort permission tightening (Windows: only owner write/read)
    try:
        if os.name == "nt":
            # Windows: attempt to remove 'everyone' and 'users' permissions using icacls?
            # Simpler: set file attribute to normal (no share) – not effective.
            # We'll just set mode to owner-only via os.chmod (works partially).
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        else:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass  # never fail setup


def load_config(path: str) -> dict:
    """Load and validate configuration from file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {path}. Run 'setup' first.", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)

    # Validate required fields and types
    required = ["base_url", "topic", "bearer_token", "call_enabled", "timeout_seconds"]
    for key in required:
        if key not in config:
            print(f"Missing required config field: {key}", file=sys.stderr)
            sys.exit(EXIT_SETTINGS)

    if not isinstance(config["base_url"], str):
        print("Config base_url must be a string", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)
    if not isinstance(config["topic"], str):
        print("Config topic must be a string", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)
    if not isinstance(config["bearer_token"], str):
        print("Config bearer_token must be a string", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)
    if not isinstance(config["call_enabled"], bool):
        print("Config call_enabled must be a boolean", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)
    if not isinstance(config["timeout_seconds"], (int, float)) or config["timeout_seconds"] <= 0:
        print("Config timeout_seconds must be a positive number", file=sys.stderr)
        sys.exit(EXIT_SETTINGS)

    return config


def validate_https(url: str) -> None:
    """Raise ValueError if URL is not HTTPS."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")


def validate_topic(topic: str) -> None:
    """Raise ValueError for invalid topic shape (non-empty, no whitespace)."""
    if not topic:
        raise ValueError("Topic cannot be empty")
    if " " in topic or "\t" in topic or "\n" in topic:
        raise ValueError("Topic must not contain whitespace")


def validate_message(message: str) -> None:
    """Raise ValueError for empty or too long message."""
    if not message:
        raise ValueError("Message cannot be empty")
    if len(message) > 1000:
        raise ValueError("Message too long (max 1000 characters)")


def send_ntfy(
    config: dict,
    message: str,
    title: Optional[str] = None,
    priority: Optional[int] = None,
    call: bool = False,
    dry_run: bool = False,
) -> Tuple[int, Optional[str]]:
    """
    Send a message to ntfy. Returns (exit_code, message_id or None).

    On dry_run, simulates without network.
    """
    base_url = config["base_url"].rstrip("/")
    topic = config["topic"]
    bearer_token = config["bearer_token"]
    timeout = config["timeout_seconds"]

    # Validate
    try:
        validate_https(base_url)
        validate_topic(topic)
        validate_message(message)
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return (EXIT_VALIDATION, None)

    # Build URL
    url = f"{base_url}/{urllib.parse.quote(topic, safe='')}"

    # Headers
    headers = {"Content-Type": "text/plain; charset=utf-8"}

    # Priority
    if priority is not None:
        headers["Priority"] = str(priority)

    # Title
    if title:
        headers["Title"] = title

    # Tags (optional, could add)
    headers["Tags"] = "android_vocalizer"  # default tag

    # Call request
    if call:
        if not bearer_token:
            print("Call requested but no bearer_token configured", file=sys.stderr)
            return (EXIT_SETTINGS, None)
        headers["Call"] = "yes"

    # Authorization
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    if dry_run:
        print("DRY RUN - would send:", file=sys.stderr)
        print(f"  URL: {url}")
        print(f"  Headers: { {k: v for k, v in headers.items() if k != 'Authorization'} }")
        print(f"  Message: {message}")
        return (0, None)

    # Send
    data = message.encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            resp_data = response.read().decode("utf-8")
            resp_json = json.loads(resp_data)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            detail = ""
        print(f"HTTP error {e.code}: {detail}", file=sys.stderr)
        return (EXIT_REMOTE, None)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return (EXIT_NETWORK, None)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return (EXIT_NETWORK, None)

    # Parse response
    try:
        message_id = resp_json["id"]
    except (KeyError, TypeError):
        print("Unexpected response format", file=sys.stderr)
        return (EXIT_REMOTE, None)

    # Print only safe fields
    print(f"Message ID: {message_id}")
    if "time" in resp_json:
        print(f"Time: {resp_json['time']}")
    if "event" in resp_json:
        print(f"Event: {resp_json['event']}")
    print("Published successfully")
    return (0, message_id)


def main(argv: Optional[list] = None) -> int:
    """Parse arguments and execute command."""
    parser = argparse.ArgumentParser(
        description="Push notifications to Android via ntfy.sh"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Create default config file")
    setup_parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help=f"Config file path (default: {DEFAULT_CONFIG_PATH})",
    )

    # Send command
    send_parser = subparsers.add_parser("send", help="Send a notification")
    send_parser.add_argument("text", help="Message text (UTF-8 plain text)")
    send_parser.add_argument("--title", help="Notification title")
    send_parser.add_argument(
        "--priority",
        choices=["routine", "urgent", "emergency"],
        help="Notification priority",
    )
    send_parser.add_argument(
        "--call",
        action="store_true",
        help="Request a phone call (requires bearer_token configured)",
    )
    send_parser.add_argument("--dry-run", action="store_true", help="Simulate without sending")
    send_parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help=f"Config file path (default: {DEFAULT_CONFIG_PATH})",
    )

    args = parser.parse_args(argv)

    if args.command == "setup":
        create_default_config(args.config)
        print(f"Config created at: {args.config}")
        return 0
    elif args.command == "send":
        config = load_config(args.config)

        # Determine priority
        priority_map = {"routine": 3, "urgent": 5, "emergency": 5}
        priority = priority_map.get(args.priority) if args.priority else None

        call = args.call
        if args.priority == "emergency":
            # Emergency always requests a call
            if not config["bearer_token"]:
                print("Emergency priority requires a bearer_token configured", file=sys.stderr)
                return EXIT_SETTINGS
            call = True

        exit_code, _ = send_ntfy(
            config,
            args.text,
            title=args.title,
            priority=priority,
            call=call,
            dry_run=args.dry_run,
        )
        return exit_code
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

# /tests/test_android_vocalizer.py

```python
"""Unit tests for android_vocalizer.py using mock objects. No network access."""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open

# Ensure the parent module is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from android_vocalizer import (
    create_default_config,
    load_config,
    send_ntfy,
    main,
    EXIT_SETTINGS,
    EXIT_VALIDATION,
    EXIT_NETWORK,
    EXIT_REMOTE,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
)


class TestCreateDefaultConfig(unittest.TestCase):
    """Tests for create_default_config atomic creation and content."""

    @patch("android_vocalizer.os.open")
    @patch("android_vocalizer.os.fdopen")
    @patch("android_vocalizer.secrets.token_hex", return_value="mockedtopic123")
    @patch("android_vocalizer.os.chmod")
    def test_create_new_file(self, mock_chmod, mock_token, mock_fdopen, mock_open):
        """File does not exist, create it with exclusive open."""
        mock_open.side_effect = [10]  # returns fd
        mock_file = MagicMock()
        mock_fdopen.return_value.__enter__.return_value = mock_file

        path = "/fake/config.json"
        create_default_config(path)

        mock_open.assert_called_once_with(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        mock_fdopen.assert_called_once_with(10, "w", encoding="utf-8")
        # Check written config
        expected_config = {
            "base_url": DEFAULT_BASE_URL,
            "topic": "mockedtopic123",
            "bearer_token": "",
            "call_enabled": False,
            "timeout_seconds": DEFAULT_TIMEOUT,
        }
        written_content = mock_file.write.call_args[0][0]
        self.assertEqual(json.loads(written_content), expected_config)

        # Check chmod called
        self.assertTrue(mock_chmod.called)

    @patch("android_vocalizer.os.open", side_effect=FileExistsError)
    def test_file_exi

[TRUNCATED: result exceeded 12000 characters]
