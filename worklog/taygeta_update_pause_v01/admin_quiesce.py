import os
import paramiko


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

command = (
    "sudo -S -p '' sh -c '"
    "systemctl stop apt-daily.timer apt-daily-upgrade.timer; "
    "systemctl kill --signal=SIGTERM apt-daily.service 2>/dev/null || true; "
    "sleep 3; "
    "systemctl is-active apt-daily.service apt-daily.timer "
    "apt-daily-upgrade.service apt-daily-upgrade.timer 2>/dev/null || true"
    "'"
)
stdin, stdout, stderr = client.exec_command(command)
stdin.write(password + "\n")
stdin.flush()
result = stdout.read().decode().strip()
error = stderr.read().decode().strip()
status = stdout.channel.recv_exit_status()
client.close()

if status != 0:
    raise SystemExit(error or f"Remote admin quiesce failed with exit {status}.")
print(result)
