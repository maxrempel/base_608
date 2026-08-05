#!/bin/bash
# Monitor all-4 sticks (64GB) at 50GB load, 30 rounds, AFTER clean manual launch.
# Baseline crashes=0 (logs reset clean at launch). 4-crash tolerance: let guard auto-relaunch
# between crashes; only disarm after 4 total (50GB unreliable verdict on all-4).
LOG=C:/claude_base/worklog/sol_mon_all4_watch.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=12 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== ALL4 sticks 64GB 50GB 30rounds monitor $(date) ===" > "$LOG"
prev_c=0
i=0
while [ $i -lt 360 ]; do
  i=$((i+1)); ts=$(date +%H:%M:%S)
  stat=$($SSH 'echo -n "c="; grep -c "^BOOT" campaign_boots.log 2>/dev/null; echo -n "r="; cat campaign_round.cnt 2>/dev/null; echo -n "f="; grep RESULT campaign32.log 2>/dev/null | grep -vc "bad_words=0 "; echo -n "run="; [ -f campaign.run ] && echo 1 || echo 0; echo -n "done="; grep -c "RESULT ROUND" campaign32.log 2>/dev/null; echo -n "last="; grep "RESULT ROUND" campaign32.log 2>/dev/null | tail -1' 2>/dev/null)
  if [ -z "$stat" ]; then
    echo "[$i $ts] Sol unreachable (heavy load or reboot=possible FREEZE)" >> "$LOG"
  else
    c=$(echo "$stat" | sed -n 's/^c=//p'); r=$(echo "$stat" | sed -n 's/^r=//p')
    f=$(echo "$stat" | sed -n 's/^f=//p'); run=$(echo "$stat" | sed -n 's/^run=//p')
    done=$(echo "$stat" | sed -n 's/^done=//p'); last=$(echo "$stat" | sed -n 's/^last=//p')
    echo "[$i $ts] crashes=${c:-NA} round=${r:-NA} done=${done:-NA} flips=${f:-NA} run=${run:-NA} | $last" >> "$LOG"
    if [ -n "$c" ] && [ "$c" -ge "$((prev_c+4))" ] 2>/dev/null; then
      $SSH 'rm -f /home/maxre/campaign.run; pkill -f /home/maxre/ramscan' 2>/dev/null
      echo "[$i $ts] 4-CRASH-LIMIT crashes=$c -> DISARMED (50GB unreliable on all-4)" >> "$LOG"; break
    fi
    if [ -n "$done" ] && [ "$done" -ge 30 ] 2>/dev/null; then
      echo "[$i $ts] DONE-30" >> "$LOG"; break
    fi
  fi
  sleep 50
done
echo "watcher-end" >> "$LOG"
