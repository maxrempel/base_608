#!/usr/bin/env bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"   # robust regardless of launch method (login or not)
# E5 Sol health trouble-watch. Max doing REAL work on Sol (fan ON = known-clean config).
# Detects trouble FROM OUTSIDE Sol (no reliance on Sol's own log files): freeze (uptime reset),
# overheat (temp>=80C), unreachable (SSH dead). Record kept on PINE (off Sol). Pages Max on
# Telegram @MMMMonitorMaxBot per event (no spam) so alarms reach him even with no Claude session.
SOL="maxre@192.168.1.113"
KEY="$HOME/.ssh/sol_key"
LOG="C:/claude_base/worklog/sol_health_watch.log"
DIGEST="C:/claude_base/worklog/sol_health_digest.txt"
TG_TOKEN="8980727843:AAFBSk2F9iVmxjEeJdESpNtGoHf3BKIMerU"
TG_CHAT="1395850773"
PERIOD=50
HOT=80
HOT_CLEAR=74   # re-arm overheat alarm only after it cools below this

tg() { curl -s -m 15 "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
         --data-urlencode "chat_id=${TG_CHAT}" --data-urlencode "text=$1" >/dev/null 2>&1; }

prev_up=-1
maxtemp=0
deadcount=0
unreach_sent=0
overheat_sent=0
alarms=""

echo "=== sol_health_watch started $(date) ===" >> "$LOG"
tg "Sol health-watch ARMED $(date '+%H:%M'). Watching for freeze/overheat/unreachable. Fan-on config."
while true; do
  ts=$(date '+%H:%M:%S')
  out=$(ssh -i "$KEY" -o ConnectTimeout=12 -o StrictHostKeyChecking=no "$SOL" \
    "echo UPSEC=\$(cat /proc/uptime | awk '{print int(\$1)}'); \
     echo LOAD=\$(cut -d' ' -f1-3 /proc/loadavg); \
     echo MEMFREE=\$(free -m | awk '/Mem:/{print \$7\"MB_avail\"}'); \
     echo TEMP=\$(sensors 2>/dev/null | grep 'Package id' | grep -o '+[0-9.]*' | head -1)" 2>/dev/null)

  if [ -z "$out" ]; then
    deadcount=$((deadcount+1))
    line="[$ts] SSH-DEAD (x$deadcount) - possible freeze/hang"
    echo "$line" >> "$LOG"
    if [ "$deadcount" -ge 2 ] && [ "$unreach_sent" -eq 0 ]; then
      alarms="${alarms}[$ts] UNREACHABLE x$deadcount - Sol may have FROZEN\n"
      tg "TROUBLE: Sol UNREACHABLE since $ts (x$deadcount polls) - possible HARD FREEZE. (E5 health-watch)"
      unreach_sent=1
    fi
  else
    [ "$unreach_sent" -eq 1 ] && tg "Sol reachable again at $ts." && alarms="${alarms}[$ts] recovered (reachable)\n"
    deadcount=0; unreach_sent=0
    upsec=$(echo "$out" | grep '^UPSEC='   | cut -d= -f2)
    load=$(echo "$out"  | grep '^LOAD='    | cut -d= -f2-)
    memf=$(echo "$out"  | grep '^MEMFREE=' | cut -d= -f2)
    temp=$(echo "$out"  | grep '^TEMP='    | cut -d= -f2)
    tnum=$(echo "$temp" | tr -d '+C')
    [ -n "$tnum" ] && awk "BEGIN{exit !($tnum>$maxtemp)}" && maxtemp=$tnum
    upmin=$(( ${upsec:-0} / 60 ))
    line="[$ts] up=${upmin}min load=$load mem=$memf temp=$temp"
    echo "$line" >> "$LOG"
    if [ "$prev_up" -ge 0 ] && [ "${upsec:-0}" -lt "$prev_up" ]; then
      alarms="${alarms}[$ts] REBOOT DETECTED (uptime ${upmin}min < prior) = Sol likely FROZE + recovered\n"
      tg "TROUBLE: Sol REBOOTED at $ts (uptime reset to ${upmin}min) = likely a FREEZE during your work. Check it. (E5 health-watch)"
    fi
    if [ -n "$tnum" ]; then
      if awk "BEGIN{exit !($tnum>=$HOT)}" && [ "$overheat_sent" -eq 0 ]; then
        alarms="${alarms}[$ts] OVERHEAT temp=$temp (>=${HOT}C)\n"
        tg "TROUBLE: Sol OVERHEAT temp=$temp at $ts (>=${HOT}C). (E5 health-watch)"
        overheat_sent=1
      elif awk "BEGIN{exit !($tnum<$HOT_CLEAR)}"; then
        overheat_sent=0
      fi
    fi
    prev_up=${upsec:-$prev_up}
  fi

  {
    echo "SOL HEALTH DIGEST  updated $ts"
    echo "latest: $line"
    echo "max_temp_seen: ${maxtemp}C"
    echo "--- TROUBLE ALARMS (reboot/overheat/unreachable) ---"
    echo -e "${alarms:-none - Sol healthy}"
  } > "$DIGEST"

  sleep $PERIOD
done
