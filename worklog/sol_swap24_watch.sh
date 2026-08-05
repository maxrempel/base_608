#!/bin/bash
# Watch Sol go DOWN (Max swapping sticks to slots 2+4) then come back UP,
# auto-launch the same 100%/27GB 20-round test, then monitor for crash.
LOG=C:/claude_base/worklog/sol_swap24_watch.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=10 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== swap-to-slots2+4 auto-launch watcher $(date) ===" > "$LOG"
seen_down=0
launched=0
prev_c=0
i=0
while [ $i -lt 360 ]; do
  i=$((i+1))
  ts=$(date +%H:%M:%S)
  if $SSH 'true' 2>/dev/null; then
    up=1
  else
    up=0
  fi
  if [ $up -eq 0 ]; then
    seen_down=1
    echo "[$i $ts] Sol DOWN (swap in progress)" >> "$LOG"
  else
    if [ $launched -eq 0 ]; then
      if [ $seen_down -eq 1 ]; then
        # Sol came back after the swap -> launch the test fresh
        $SSH 'cd /home/maxre; sed -i "s/for gb in [0-9 ]*/for gb in 27/" campaign.sh; echo 0 > campaign_round.cnt; echo 20 > campaign_maxrounds; echo "=== WINDOW slots2+4 sticks2+3 green 27GB 20rounds $(date) ===" > campaign32.log; echo "WINDOW-START $(date) PAIR=sticks23-slots24-green-100pct" > campaign_boots.log; touch campaign.run; setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
        launched=1
        echo "[$i $ts] Sol BACK UP -> LAUNCHED slots2+4 test (27GB x20)" >> "$LOG"
      else
        echo "[$i $ts] Sol still UP, waiting for Max to power down for swap" >> "$LOG"
      fi
    else
      # monitoring the running test
      stat=$($SSH 'echo -n "c="; grep -c "^BOOT" campaign_boots.log 2>/dev/null; echo -n "r="; cat campaign_round.cnt 2>/dev/null; echo -n "f="; grep RESULT campaign32.log 2>/dev/null | grep -vc "bad_words=0 "; echo -n "run="; [ -f campaign.run ] && echo 1 || echo 0; echo -n "done="; grep -c "RESULT ROUND" campaign32.log 2>/dev/null' 2>/dev/null)
      c=$(echo "$stat" | sed -n 's/^c=//p'); r=$(echo "$stat" | sed -n 's/^r=//p')
      f=$(echo "$stat" | sed -n 's/^f=//p'); run=$(echo "$stat" | sed -n 's/^run=//p')
      done=$(echo "$stat" | sed -n 's/^done=//p')
      echo "[$i $ts] crashes=${c:-NA} round=${r:-NA} done=${done:-NA} flips=${f:-NA} run=${run:-NA}" >> "$LOG"
      if [ -n "$c" ] && [ "$c" -gt "$prev_c" ] 2>/dev/null; then
        $SSH 'rm -f /home/maxre/campaign.run; pkill -f /home/maxre/ramscan' 2>/dev/null
        echo "[$i $ts] CRASH-DETECTED crashes=$c -> DISARMED (stop crash-loop)" >> "$LOG"
        break
      fi
      if [ -n "$done" ] && [ "$done" -ge 20 ] 2>/dev/null; then
        echo "[$i $ts] DONE-20 clean" >> "$LOG"
        break
      fi
    fi
  fi
  sleep 60
done
echo "watcher-end" >> "$LOG"
