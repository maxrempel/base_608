"""Update the Quen Balance Collector scheduled task based on the current date.

The polling schedule ramps up:
- Every 5 minutes: 2026-08-05 until 2026-08-05 23:59
- Every 20 minutes: 2026-08-06 until 2026-08-07 23:59
- Every 30 minutes: 2026-08-08 onward

This script checks the current date and updates the task trigger accordingly.
Run it once per day via a separate scheduled task, or manually after the
transitions.
"""

import subprocess
import sys
from datetime import datetime

TASK_NAME = "Quen Balance Collector"
SCRIPT_PATH = r"C:\claude_base\tools\quen_cost_projector\collect_quen_balance_v01.py"
PYTHONW = r"C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe"


def get_schedule():
    now = datetime.now()
    if now.date() <= datetime(2026, 8, 5).date():
        return 5, "baseline (5 min)"
    elif now.date() <= datetime(2026, 8, 7).date():
        return 20, "phase 2 (20 min)"
    else:
        return 30, "phase 3 (30 min)"


def update_task(interval_minutes, phase_label):
    # Delete existing task if present
    subprocess.run(
        ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
        capture_output=True,
    )

    # Create new task with the specified interval
    result = subprocess.run(
        [
            "schtasks", "/Create",
            "/TN", TASK_NAME,
            "/TR", f'"{PYTHONW}" "{SCRIPT_PATH}"',
            "/SC", "MINUTE",
            "/MO", str(interval_minutes),
            "/ST", "00:00",
            "/F",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"Updated {TASK_NAME} to every {interval_minutes} minutes ({phase_label})")
    else:
        print(f"Failed to update task: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    interval, phase = get_schedule()
    update_task(interval, phase)


if __name__ == "__main__":
    main()
