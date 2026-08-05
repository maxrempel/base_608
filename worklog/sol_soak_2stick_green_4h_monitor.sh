#!/bin/bash
# MONITOR-ONLY 4h soak for 2-stick GREEN config (stick1 in slot1 + stick3 in slot3 = 32GB) at 27GB load.
# This is the KNOWN-GOOD config (green slots 1+3). Launched cleanly already; this just polls + keeps alive.
# If it ever reads NORUN (a reboot where the guard didn't re-arm), it re-forces 27GB + flag so the load stays correct.
# SAFETY: re-arm uses 27GB ONLY (this is a 32GB box -- 50GB would OOM). 4h wall cap then disarm.
# SOAK = never disarm on crash; just count them.
LOG=C:/claude_base/worklog/sol_soak_2stick_green_4h_monitor.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=12 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== MONITOR 2stick GREEN (s1slot1+s3slot3) 32GB @27GB 4h soak $(date) ===" > "$LOG"
START=$(date +%s)
i=0
while [ $i -lt 320 ]; do
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
      $SSH 'cd /home/maxre; grep -q "for gb in 27" campaign.sh || sed -i "s/for gb in [0-9 ]*/for gb in 27/" campaign.sh; touch campaign.run; pgrep -f /home/maxre/campaign.sh >/dev/null || setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
      echo "[$i $ts] re-armed flag+27GB campaign (was NORUN) to keep soak going" >> "$LOG"
    fi
  fi
  sleep 50
done
echo "watcher-end" >> "$LOG"
