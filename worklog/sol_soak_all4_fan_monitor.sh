#!/bin/bash
# MONITOR-ONLY soak for all4+FAN (already launched cleanly at 50GB). Does NOT reconfigure/reset.
# Just polls, logs rounds/crashes/temp, and KEEPS the soak alive: if it ever reads NORUN (a reboot
# where the guard relaunched a stale config), it re-forces 50GB + flag so the load stays correct.
# 4h wall-clock cap then disarm. Soak = never disarm on crash; count them.
LOG=C:/claude_base/worklog/sol_soak_all4_fan_monitor.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=12 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== MONITOR all4+FAN 64GB @50GB 4h soak $(date) ===" > "$LOG"
START=$(date +%s)
i=0
while [ $i -lt 300 ]; do
  i=$((i+1)); ts=$(date +%H:%M:%S); now=$(date +%s)
  if [ $((now-START)) -ge 14400 ]; then
    echo "[$i $ts] 4-HOUR SOAK COMPLETE -> disarming" >> "$LOG"
    $SSH 'rm -f /home/maxre/campaign.run; pkill -f /home/maxre/ramscan' 2>/dev/null
    break
  fi
  stat=$($SSH 'echo -n "c="; grep -c "^BOOT" campaign_boots.log 2>/dev/null; echo -n "r="; cat campaign_round.cnt 2>/dev/null; echo -n "f="; grep RESULT campaign32.log 2>/dev/null | grep -vc "bad_words=0 "; echo -n "run="; [ -f campaign.run ] && echo 1 || echo 0; echo -n "done="; grep -c "RESULT ROUND" campaign32.log 2>/dev/null; echo -n "t="; sensors 2>/dev/null | awk "/Package id 0:/{print \$4}"; echo -n "last="; grep "RESULT ROUND" campaign32.log 2>/dev/null | tail -1' 2>/dev/null)
  if [ -z "$stat" ]; then
    echo "[$i $ts] Sol unreachable (heavy load or FREEZE/reboot)" >> "$LOG"
  else
    c=$(echo "$stat" | sed -n 's/^c=//p'); r=$(echo "$stat" | sed -n 's/^r=//p')
    f=$(echo "$stat" | sed -n 's/^f=//p'); run=$(echo "$stat" | sed -n 's/^run=//p')
    done=$(echo "$stat" | sed -n 's/^done=//p'); t=$(echo "$stat" | sed -n 's/^t=//p')
    last=$(echo "$stat" | sed -n 's/^last=//p')
    echo "[$i $ts] crashes=${c:-NA} round=${r:-NA} done=${done:-NA} flips=${f:-NA} run=${run:-NA} temp=${t:-NA} | $last" >> "$LOG"
    if [ "$run" = "0" ]; then
      $SSH 'cd /home/maxre; grep -q "for gb in 50" campaign.sh || sed -i "s/for gb in [0-9 ]*/for gb in 50/" campaign.sh; touch campaign.run; pgrep -f /home/maxre/campaign.sh >/dev/null || setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
      echo "[$i $ts] re-armed flag+50GB campaign (was NORUN) to keep soak going" >> "$LOG"
    fi
  fi
  sleep 50
done
echo "watcher-end" >> "$LOG"
