#!/usr/bin/env bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
# Guard for sol_health_watch.sh. Resilient liveness check = DIGEST FRESHNESS (not process
# listing - pgrep is absent in Git Bash). If the digest is missing or older than 150s, the
# watcher is dead/stuck -> relaunch it. Run by a Windows scheduled task every 2 min + at logon,
# so the watcher survives process death AND Pine reboot.
WATCH="C:/claude_base/worklog/sol_health_watch.sh"
DIGEST="C:/claude_base/worklog/sol_health_digest.txt"
GLOG="C:/claude_base/worklog/sol_health_guard.log"
STALE=150

now=$(date +%s)
mtime=0
[ -f "$DIGEST" ] && mtime=$(stat -c %Y "$DIGEST" 2>/dev/null || echo 0)
age=$(( now - mtime ))

if [ ! -f "$DIGEST" ] || [ "$age" -ge "$STALE" ]; then
  nohup bash "$WATCH" >/dev/null 2>&1 &
  echo "[$(date)] guard: digest age=${age}s (stale/missing) -> relaunched watcher" >> "$GLOG"
fi
