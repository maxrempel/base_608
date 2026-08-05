#!/usr/bin/env python3
"""Deploy and start the authorized Taygeta NVMe read stress test."""

from __future__ import annotations

import os
from pathlib import Path

import paramiko


HOST = "192.168.1.142"
USER = os.environ["TAYGETA_USER"]
PASSWORD = os.environ["TAYGETA_PASS"]
KEY = str(Path.home() / ".ssh" / "sol_key")
BASE = Path(r"C:\claude_base\tools\taygeta_housekeeper")
FILES = {
    BASE / "taygeta_nvme_read_stress_v01.py": "/tmp/taygeta_nvme_read_stress_v01.py",
    BASE / "taygeta-nvme-read-stress-v01.service": "/tmp/taygeta-nvme-read-stress-v01.service",
}


def main() -> int:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username=USER,
        key_filename=KEY,
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
        look_for_keys=False,
        allow_agent=False,
    )
    sftp = client.open_sftp()
    for local, remote in FILES.items():
        sftp.put(str(local), remote)
    sftp.close()

    command = r"""sudo -S -p '' bash -eu -o pipefail -c '
export DEBIAN_FRONTEND=noninteractive
apt-get install -y fio
install -d -m 0755 /var/log/taygeta_nvme_read_stress_v01
install -m 0755 /tmp/taygeta_nvme_read_stress_v01.py /usr/local/sbin/taygeta_nvme_read_stress_v01.py
install -m 0644 /tmp/taygeta-nvme-read-stress-v01.service /etc/systemd/system/taygeta-nvme-read-stress-v01.service
install -d -o maxre -g maxre -m 0755 /home/maxre/housekeeping/runtime
printf "%s\n" "Taygeta science hold: Max ordered no valuable compute during the 13-hour read-only NVMe stress test. Use Asto. Created 2026-07-29." > /home/maxre/housekeeping/runtime/TAYGETA_SCIENCE_HOLD_20260729_v01.txt
chown maxre:maxre /home/maxre/housekeeping/runtime/TAYGETA_SCIENCE_HOLD_20260729_v01.txt
systemctl daemon-reload
systemctl stop taygeta-nvme-read-stress-v01.service 2>/dev/null || true
systemctl reset-failed taygeta-nvme-read-stress-v01.service 2>/dev/null || true
systemctl start taygeta-nvme-read-stress-v01.service
sleep 5
systemctl --no-pager --full status taygeta-nvme-read-stress-v01.service
'"""
    stdin, stdout, stderr = client.exec_command(command, timeout=180)
    stdin.write(PASSWORD + "\n")
    stdin.flush()
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    status = stdout.channel.recv_exit_status()
    client.close()
    log = Path(__file__).with_name("deploy_and_start_output.txt")
    log.write_text(output + ("\nSTDERR\n" + error if error else ""), encoding="utf-8")
    if status != 0:
        raise SystemExit(f"Deployment failed with exit {status}; inspect {log}.")
    print("Taygeta NVMe read stress service started successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
