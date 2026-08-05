#!/usr/bin/env bash
# E5 Sol thermal soak monitor - runs on Pine, polls Sol every 50s, zero LLM cost.
# Baseline: first BOOT (20:59:16) = Max's manual restart. Real freezes = bootcount - BASELINE_BOOTS.
SOL="maxre@192.168.1.113"
KEY="$HOME/.ssh/sol_key"
LOG="C:/claude_base/worklog/sol_thermal_monitor.log"
DIGEST="C:/claude_base/worklog/sol_thermal_digest.txt"
BASELINE_BOOTS=1          # the 20:59:16 manual reboot
PERIOD=50

prev_boots=-1
prev_badtotal=-1
maxtemp=0
alarms=""

echo "=== sol_thermal_monitor started $(date) ===" >> "$LOG"
while true; do
  out=$(ssh -i "$KEY" -o ConnectTimeout=12 -o StrictHostKeyChecking=no "$SOL" \
    "echo BC=\$(grep -c ^BOOT /home/maxre/campaign_boots.log 2>/dev/null); \
     echo LASTBOOT=\$(grep ^BOOT /home/maxre/campaign_boots.log 2>/dev/null | tail -1); \
     echo RND=\$(cat /home/maxre/campaign_round.cnt 2>/dev/null); \
     echo UP=\$(uptime -p); \
     echo BADTOTAL=\$(grep -o 'bad_words=[0-9]*' /home/maxre/campaign32.log 2>/dev/null | awk -F= '{s+=\$2} END{print s+0}'); \
     echo LASTBAD=\$(grep bad_words /home/maxre/campaign32.log 2>/dev/null | tail -1); \
     echo TEMP=\$(sensors 2>/dev/null | grep 'Package id' | grep -o '+[0-9.]*' | head -1)" 2>/dev/null)

  ts=$(date '+%H:%M:%S')
  if [ -z "$out" ]; then
    line="[$ts] SSH-DEAD (likely in-progress freeze/reboot)"
    echo "$line" >> "$LOG"
    alarms="${alarms}[$ts] SSH-DEAD\n"
  else
    bc=$(echo "$out"   | grep '^BC='       | cut -d= -f2)
    rnd=$(echo "$out"  | grep '^RND='      | cut -d= -f2)
    up=$(echo "$out"   | grep '^UP='       | cut -d= -f2-)
    badt=$(echo "$out" | grep '^BADTOTAL=' | cut -d= -f2)
    temp=$(echo "$out" | grep '^TEMP='     | cut -d= -f2)
    lastboot=$(echo "$out" | grep '^LASTBOOT=' | cut -d= -f2-)
    freezes=$(( ${bc:-1} - BASELINE_BOOTS ))
    tnum=$(echo "$temp" | tr -d '+C')
    [ -n "$tnum" ] && awk "BEGIN{exit !($tnum>$maxtemp)}" && maxtemp=$tnum
    line="[$ts] freezes=$freezes (bc=$bc) round=$rnd bad_total=$badt temp=$temp up=$up last_boot=$lastboot"
    echo "$line" >> "$LOG"
    # alarm detection
    if [ "$prev_boots" -ge 0 ] && [ "${bc:-0}" -gt "$prev_boots" ]; then
      alarms="${alarms}[$ts] NEW-FREEZE bc=$bc lastboot=$lastboot temp=$temp\n"
    fi
    if [ "$prev_badtotal" -ge 0 ] && [ "${badt:-0}" -gt "$prev_badtotal" ]; then
      alarms="${alarms}[$ts] NEW-CORRUPTION bad_total=$badt (was $prev_badtotal) temp=$temp\n"
    fi
    if [ -n "$tnum" ] && awk "BEGIN{exit !($tnum>=80)}"; then
      alarms="${alarms}[$ts] HOT temp=$temp\n"
    fi
    prev_boots=${bc:-$prev_boots}
    prev_badtotal=${badt:-$prev_badtotal}
  fi

  # rewrite digest (small, cheap for the session to Read)
  {
    echo "SOL THERMAL DIGEST  updated $ts"
    echo "latest: $line"
    echo "max_temp_seen: ${maxtemp}C"
    echo "--- ALARMS (new boots / corruption / temp>=80) ---"
    echo -e "${alarms:-none yet}"
  } > "$DIGEST"

  sleep $PERIOD
done
