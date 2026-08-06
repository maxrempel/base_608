"""Pine-idle controller for Taygeta fault isolation.

Version 01. Last edited 2026-08-04 by Codex (GPT-5.6 SOL).
Runs one heavy subsystem for 21 minutes, then rests 39 minutes: 35% duty time.
New phases start only after 2.5 hours without Pine keyboard or mouse input.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
RUNTIME = Path(os.environ.get("LOCALAPPDATA", str(HERE))) / "MaxTools" / "taygeta_fault_isolation_v01"
STATE = RUNTIME / "state.json"
LOG = RUNTIME / "controller.log"
FLAG = Path(r"C:\claude_base\tools\flag\flag.py")
REMOTE_RUNNER = "/home/maxre/taygeta_fault_isolation_v01/remote_runner_v01.sh"
UNIT = "taygeta-fault-test-v01"
IDLE_THRESHOLD_S = 150 * 60
ACTIVE_S = 21 * 60
CYCLE_S = 60 * 60
PHASES = ["memory_verify", "cpu_all", "cpu_memory_combo", "green24_sequential", "green24_random"]
SSH = [
    "ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
    "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=2",
    "-o", "ProxyCommand=ssh -i C:/Users/maxre/.ssh/bitwarden_ed25519 -o BatchMode=yes -o ConnectTimeout=10 -W %h:%p rempel@astolfodebian.tail251d88.ts.net",
    "-i", r"C:\Users\maxre\.ssh\sol_key", "maxre@192.168.1.142",
]


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def idle_seconds() -> float:
    info = LASTINPUTINFO(cbSize=ctypes.sizeof(LASTINPUTINFO))
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info)):
        raise ctypes.WinError()
    tick32 = ctypes.windll.kernel32.GetTickCount64() & 0xFFFFFFFF
    return float((tick32 - info.dwTime) & 0xFFFFFFFF) / 1000.0


def log(message: str) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.now().astimezone().isoformat(timespec='seconds')} {message}"
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"phase_index": 0, "next_eligible": 0.0, "remote_active": False, "unreachable": 0, "alerts": {}}


def save_state(state: dict) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="state_", suffix=".json", dir=RUNTIME)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
        os.replace(name, STATE)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def ssh(command: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(SSH + [command], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)


def ssh_bash(script: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    payload = base64.b64encode(script.encode()).decode()
    return ssh(f"printf '%s' '{payload}' | base64 -d | bash", timeout=timeout)


def remote_status_token(status_text: str) -> str:
    return status_text.split(maxsplit=1)[0] if status_text else ""


def alert(state: dict, key: str, message: str) -> None:
    # Repeated identical alerts back off: 6h for the first two, then daily.
    # A condition that persists is worth one reminder a day, not four.
    now = time.time()
    sent = state.setdefault("alerts", {})
    counts = state.setdefault("alert_counts", {})
    cooldown = 6 * 3600 if int(counts.get(key, 0)) < 2 else 24 * 3600
    if now - float(sent.get(key, 0)) < cooldown:
        return
    python = Path(sys.executable).with_name("python.exe")
    result = subprocess.run(
        [str(python), str(FLAG), message, "--urgent", "--from", "taygeta-idle-fault-controller"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=45,
    )
    output = result.stdout.strip()
    log(f"ALERT key={key} rc={result.returncode} delivery={output}")
    if "tg=True" in output and "email=True" in output:
        state["alerts"][key] = now
        state["alert_counts"][key] = int(state["alert_counts"].get(key, 0)) + 1


def remote_gate() -> tuple[bool, str]:
    script = r'''set -u
test "$(hostname)" = taygeta || { echo WRONG_HOST; exit 20; }
# Fault gate, three classes. A single flat pattern list over the whole boot was
# wrong: one deliberate USB replug counted as a kernel fault and, because the
# count never expired before a reboot, the controller refused to test and
# re-alerted every 6 hours forever (2026-08-06).
#
# HARD  - real machine faults. Any occurrence this boot blocks, because the
#         machine should not take added load until it is investigated.
# SOFT  - storage/transport errors that are often transient. Only a burst
#         (3 or more) inside the recent window blocks.
# USB   - a disconnect blocks only if the device never came back, i.e. more
#         disconnects than enumerations in the window. A clean unplug/replug
#         is normal operator activity, not a fault.
SOFT_WINDOW='60 min ago'
hard=$(journalctl -k -b --no-pager | grep -Eic 'general protection fault|Oops:|kernel panic|machine check|MCE.*error|EDAC.*error|AER.*error|NVRM.*Xid|reset controller|blocked for more than|hung task' || true)
[ "$hard" -eq 0 ] || { echo "KERNEL_FAULTS_HARD=$hard"; exit 21; }
recent=$(journalctl -k -b --no-pager --since "$SOFT_WINDOW" 2>/dev/null || true)
soft=$(printf '%s\n' "$recent" | grep -Eic 'I/O error|uas.*error|exfat.*error' || true)
[ "$soft" -lt 3 ] || { echo "KERNEL_FAULTS_SOFT=$soft window=60min"; exit 21; }
usb_gone=$(printf '%s\n' "$recent" | grep -Eic 'USB disconnect' || true)
# Count only "New USB device found": the kernel prints exactly one per
# enumeration. Also matching "new high-speed USB device" would double-count a
# single replug and let a genuinely lost device hide behind it.
usb_back=$(printf '%s\n' "$recent" | grep -Eic 'New USB device found' || true)
[ "$usb_gone" -le "$usb_back" ] || { echo "KERNEL_FAULTS_USB_LOST=$((usb_gone - usb_back)) gone=$usb_gone back=$usb_back window=60min"; exit 21; }
# Uninterruptible sleep (D state) is normal and constant on a busy machine: any
# process waiting on disk shows it for a moment. A single instantaneous sample
# therefore blocked testing and fired an urgent alert at random (2026-08-06 -
# the gate's own journalctl read tripped it). Only a D state that survives
# three samples over ~4s, or a pile-up of several at once, means a real stall.
dstate=0
for _ in 1 2 3; do
  n=$(ps -eo state= | awk '$1 ~ /^D/ {c++} END {print c+0}')
  [ "$n" -ge 4 ] && { dstate=$n; break; }
  [ "$n" -eq 0 ] && { dstate=0; break; }
  dstate=$n
  sleep 2
done
[ "$dstate" -eq 0 ] || { echo "DSTATE=$dstate"; exit 22; }
tasks=$(systemctl show workload.slice -p TasksCurrent --value 2>/dev/null || echo 0)
case "$tasks" in ''|'[not set]') tasks=0;; esac
[ "$tasks" -eq 0 ] || { echo "SCIENCE_TASKS=$tasks"; exit 23; }
load=$(cut -d' ' -f1 /proc/loadavg)
awk -v x="$load" 'BEGIN {exit !(x < 4.0)}' || { echo "LOAD=$load"; exit 24; }
gpu=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -n1 || echo 0)
[ "${gpu:-0}" -lt 20 ] || { echo "GPU=$gpu"; exit 25; }
echo "READY load=$load gpu=${gpu:-0} tasks=$tasks"
'''
    result = ssh_bash(script)
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def run_once(force: bool = False, duration: int = ACTIVE_S) -> int:
    state = load_state()
    now = time.time()
    try:
        status = ssh(f"{REMOTE_RUNNER} status", timeout=25)
    except Exception as exc:
        state["unreachable"] = int(state.get("unreachable", 0)) + 1
        if state.get("remote_active") and state["unreachable"] >= 2:
            alert(state, "active_test_unreachable", "Taygeta became unreachable during an active component-isolation test. Preserve the current phase marker and check for a reboot or hardware fault.")
        log(f"UNREACHABLE exception={type(exc).__name__}")
        save_state(state)
        return 2
    if status.returncode != 0:
        state["unreachable"] = int(state.get("unreachable", 0)) + 1
        if state.get("remote_active") and state["unreachable"] >= 2:
            alert(state, "active_test_unreachable", "Taygeta stopped answering during an active component-isolation test. This may be a reproduced crash; inspect the phase marker after reboot.")
        log(f"UNREACHABLE rc={status.returncode} detail={(status.stderr or status.stdout).strip()}")
        save_state(state)
        return 2
    state["unreachable"] = 0
    status_text = status.stdout.strip()
    # Only the leading status token is authoritative. An IDLE line includes the
    # previous result text, so a historical FAULT must not be re-alerted as a
    # current failure.
    status_token = remote_status_token(status_text)
    if status_token in {"CRASH_DETECTED", "INTERRUPTED_DETECTED", "FAULT"}:
        alert(state, "remote_fault_" + status_text.split()[0], "Taygeta fault-isolation controller recorded: " + status_text[:600])
    if status_text.startswith("ACTIVE"):
        state["remote_active"] = True
        save_state(state)
        return 0
    state["remote_active"] = False

    idle = idle_seconds()
    if not force and idle < IDLE_THRESHOLD_S:
        save_state(state)
        return 0
    if not force and now < float(state.get("next_eligible", 0)):
        save_state(state)
        return 0
    ready, detail = remote_gate()
    if not ready:
        if any(word in detail for word in ("KERNEL_FAULTS", "DSTATE")):
            # Key on the condition token, not a constant, so a genuinely new
            # fault is not silenced by an older condition's cooldown.
            alert(state, "preflight_fault:" + detail.split("=", 1)[0].strip(),
                  "Taygeta testing preflight found an existing system fault and refused to add load: " + detail[:500])
        log(f"SKIP gate={detail}")
        save_state(state)
        return 0

    index = int(state.get("phase_index", 0)) % len(PHASES)
    phase = PHASES[index]
    launch = f'''set -eu
test -x {REMOTE_RUNNER}
systemctl --user reset-failed {UNIT}.service 2>/dev/null || true
systemd-run --user --collect --unit={UNIT} --property=Nice=10 --property=CPUWeight=10 --property=IOWeight=10 --property=MemoryMax=24G --property=TasksMax=256 {REMOTE_RUNNER} run {phase} {int(duration)}
'''
    result = ssh_bash(launch)
    if result.returncode != 0:
        log(f"LAUNCH_FAIL phase={phase} detail={(result.stdout + result.stderr).strip()}")
        save_state(state)
        return 2
    state.update({
        "phase_index": (index + 1) % len(PHASES),
        "next_eligible": now + CYCLE_S,
        "remote_active": True,
        "last_phase": phase,
        "last_launch": now,
    })
    log(f"LAUNCHED phase={phase} duration_s={duration} idle_s={int(idle)} gate={detail}")
    save_state(state)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--force", action="store_true", help="bypass Pine idle/duty gates; preflight still applies")
    parser.add_argument("--duration", type=int, default=ACTIVE_S)
    args = parser.parse_args()
    return run_once(force=args.force, duration=args.duration)


if __name__ == "__main__":
    raise SystemExit(main())
