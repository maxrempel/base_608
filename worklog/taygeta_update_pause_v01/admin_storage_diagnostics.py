import os
import paramiko
from pathlib import Path


host = "192.168.1.142"
username = os.environ.get("TAYGETA_USER", "")
password = os.environ.get("TAYGETA_PASS", "")
key_path = os.path.expanduser("~/.ssh/sol_key")

if not username or not password:
    raise SystemExit("Taygeta credential fields are unavailable.")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    host,
    username=username,
    key_filename=key_path,
    timeout=8,
    look_for_keys=True,
    allow_agent=False,
)

command = r"""sudo -S -p '' bash -lc '
echo "=== NVME SMART ==="
timeout 30 smartctl -x /dev/nvme0 2>&1 || true
echo "=== GREEN24 SMART SAT ==="
timeout 45 smartctl -x -d sat /dev/sda 2>&1 || true
echo "=== BLOCKED TASKS ==="
python3 - <<"PY"
import os
for name in sorted((x for x in os.listdir("/proc") if x.isdigit()), key=int):
    base = f"/proc/{name}"
    try:
        stat = open(base + "/stat").read()
        r = stat.rfind(")")
        state = stat[r + 2:].split()[0]
        if state != "D":
            continue
        comm = open(base + "/comm").read().strip()
        wchan = open(base + "/wchan").read().strip()
        try:
            stack = " | ".join(x.strip() for x in open(base + "/stack") if x.strip())
        except Exception as e:
            stack = f"<{e}>"
        print(f"pid={name} comm={comm} wchan={wchan} stack={stack}")
    except Exception:
        pass
PY
echo "=== DEVICE STATE ==="
for p in /sys/block/nvme0n1/device/state /sys/block/sda/device/state /sys/block/sda/device/timeout /sys/block/sda/device/queue_depth /sys/block/sda/queue/io_timeout /sys/block/nvme0n1/queue/io_timeout; do
  test -e "$p" && echo "$p=$(cat "$p")"
done
echo "=== RAS ERRORS ==="
ras-mc-ctl --errors 2>&1 | tail -n 120 || true
'"""

stdin, stdout, stderr = client.exec_command(command, timeout=120)
stdin.write(password + "\n")
stdin.flush()
result = stdout.read().decode(errors="replace")
error = stderr.read().decode(errors="replace")
status = stdout.channel.recv_exit_status()
client.close()

output_path = Path(__file__).with_name("admin_storage_diagnostics_output.txt")
output_path.write_text(result + ("\n" + error if error else ""), encoding="utf-8")
if status != 0:
    raise SystemExit(f"Remote storage diagnostics failed with exit {status}.")
