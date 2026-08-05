#!/bin/bash
# Wait for Sol to come back UP after Max adds stick 2 to slot 3 (slots 3+4),
# then STOP any auto-relaunched old test, reconfigure to 27GB, launch fresh 20-round 100% test, monitor.
LOG=C:/claude_base/worklog/sol_swap34_watch.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=12 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== slots3+4 (stick2-slot3 + stick3-slot4) 27GB 20rounds $(date) ===" > "$LOG"
launched=0
prev_c=0
i=0
while [ $i -lt 300 ]; do
  i=$((i+1))
  ts=$(date +%H:%M:%S)
  if $SSH 'true' 2>/dev/null; then up=1; else up=0; fi
  if [ $up -eq 0 ]; then
    echo "[$i $ts] Sol DOWN (swap in progress)" >> "$LOG"
  else
    if [ $launched -eq 0 ]; then
      # Sol is back: kill any guard-relaunched old campaign, then launch fresh 27GB test
      $SSH 'cd /home/maxre; rm -f campaign.run; pkill -f /home/maxre/ramscan; sleep 2; sed -i "s/for gb in [0-9 ]*/for gb in 27/" campaign.sh; echo 0 > campaign_round.cnt; echo 20 > campaign_maxrounds; echo "=== WINDOW slots3+4 stick2-slot3 stick3-slot4 27GB 20rounds $(date) ===" > campaign32.log; echo "WINDOW-START $(date) PAIR=slots34-stick2+3-100pct" > campaign_boots.log; touch campaign.run; setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
      launched=1
      echo "[$i $ts] Sol BACK UP -> LAUNCHED slots3+4 test (27GB x20)" >> "$LOG"
    else
      stat=$($SSH 'echo -n "c="; grep -c "^BOOT" campaign_boots.log 2>/dev/null; echo -n "r="; cat campaign_round.cnt 2>/dev/null; echo -n "f="; grep RESULT campaign32.log 2>/dev/null | grep -vc "bad_words=0 "; echo -n "run="; [ -f campaign.run ] && echo 1 || echo 0; echo -n "done="; grep -c "RESULT ROUND" campaign32.log 2>/dev/null; echo -n "last="; grep "RESULT ROUND" campaign32.log 2>/dev/null | tail -1' 2>/dev/null)
      c=$(echo "$stat" | sed -n 's/^c=//p'); r=$(echo "$stat" | sed -n 's/^r=//p')
      f=$(echo "$stat" | sed -n 's/^f=//p'); run=$(echo "$stat" | sed -n 's/^run=//p')
      done=$(echo "$stat" | sed -n 's/^done=//p'); last=$(echo "$stat" | sed -n 's/^last=//p')
      echo "[$i $ts] crashes=${c:-NA} round=${r:-NA} done=${done:-NA} flips=${f:-NA} run=${run:-NA} | $last" >> "$LOG"
      if [ -n "$c" ] && [ "$c" -gt "$prev_c" ] 2>/dev/null; then
        $SSH 'rm -f /home/maxre/campaign.run; pkill -f /home/maxre/ramscan' 2>/dev/null
        echo "[$i $ts] CRASH-DETECTED crashes=$c -> DISARMED" >> "$LOG"
        break
      fi
      if [ -n "$done" ] && [ "$done" -ge 20 ] 2>/dev/null; then
        echo "[$i $ts] DONE-20" >> "$LOG"; break
      fi
    fi
  fi
  sleep 50
done
echo "watcher-end" >> "$LOG"
