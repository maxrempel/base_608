"""Install the Alibaba Spend Collector scheduled task.

Version 02, 2026-08-06 by Claude Opus 5.

The old ramping schedule (5 / 20 / 30 minutes) existed because the previous
collector estimated Qwen spend from local session logs, which change every
few minutes. The new collector reads the Alibaba bill, which updates a few
times a day, so a fixed hourly poll is the right cadence: often enough to
catch a bill update the hour it lands, cheap enough to run forever.

Max's rule, 2026-08-06: hourly if the numbers can come through an API,
every eight hours if a human has to log in each time. The BSS OpenAPI route
is an API, so this installs hourly. Set HOURS below to 8 if the access key
is ever removed and the tracker falls back to manual console reads.

Running this also removes the superseded "Quen Balance Collector" task.
"""

from __future__ import annotations

import subprocess
import sys

TASK_NAME = "Alibaba Spend Collector"
OLD_TASK_NAME = "Quen Balance Collector"
SCRIPT_PATH = r"C:\base_608\tools\quen_cost_projector\collect_alibaba_spend_v02.py"
PYTHONW = r"C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe"
HOURS = 1


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    removed = run(["schtasks", "/Delete", "/TN", OLD_TASK_NAME, "/F"])
    if removed.returncode == 0:
        print(f"removed superseded task: {OLD_TASK_NAME}")

    run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"])
    result = run(
        [
            "schtasks", "/Create",
            "/TN", TASK_NAME,
            "/TR", f'"{PYTHONW}" "{SCRIPT_PATH}"',
            "/SC", "HOURLY",
            "/MO", str(HOURS),
            "/ST", "00:07",
            "/F",
        ]
    )
    if result.returncode != 0:
        print(f"failed to create task: {result.stderr.strip()}", file=sys.stderr)
        return 1
    print(f"installed {TASK_NAME}: every {HOURS} hour(s), hidden, at :07 past the hour")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
