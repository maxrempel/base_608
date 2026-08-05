#!/bin/bash
# SOAK TEST: 3 sticks (2,3,4 in slots 1,2,3 = 48GB) at 42GB load, run ~4 hours.
# Stick 1 removed from slot 4. Waits for Sol DOWN->UP after the swap, then launches.
# SOAK = do NOT disarm on crash; let Sol's guard/@reboot cron auto-relaunch through
# each freeze and KEEP the load on for 4h. Just log + count crashes. maxrounds set high
# so it won't self-finish inside the window. Baselines crash count after a 60s settle.
LOG=C:/claude_base/worklog/sol_soak_3stick_4h_watch.log
SSH="ssh -i $HOME/.ssh/sol_key -o ConnectTimeout=12 -o StrictHostKeyChecking=no maxre@192.168.1.113"
echo "=== SOAK 3-stick (2,3,4 slots1,2,3) 48GB @42GB 4h $(date) ===" > "$LOG"
launched=0
prev_c=0
START=$(date +%s)
i=0
# ~4h: poll every 50s -> up to ~290 iterations. Also hard-stop at 4h wall clock.
while [ $i -lt 300 ]; do
  i=$((i+1))
  ts=$(date +%H:%M:%S)
  now=$(date +%s)
  if [ $((now-START)) -ge 14400 ]; then
    echo "[$i $ts] 4-HOUR SOAK COMPLETE -> disarming" >> "$LOG"
    $SSH 'rm -f /home/maxre/campaign.run; pkill -f /home/maxre/ramscan' 2>/dev/null
    break
  fi
  if $SSH 'true' 2>/dev/null; then up=1; else up=0; fi
  if [ $up -eq 0 ]; then
    echo "[$i $ts] Sol DOWN (swap/reboot/freeze)" >> "$LOG"
  else
    if [ $launched -eq 0 ]; then
      $SSH 'cd /home/maxre; rm -f campaign.run; pkill -9 -f /home/maxre/ramscan; sleep 3; sed -i "s/for gb in [0-9 ]*/for gb in 42/" campaign.sh; echo 0 > campaign_round.cnt; echo 200 > campaign_maxrounds; echo "=== WINDOW SOAK 3stick(2,3,4 slots1,2,3) 48GB 42GB 4h $(date) ===" > campaign32.log; echo "WINDOW-START $(date) PAIR=3stick-234-slots123-48GB-42GBload-SOAK" > campaign_boots.log; touch campaign.run; setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
      launched=1
      sleep 60
      prev_c=$($SSH 'grep -c "^BOOT" campaign_boots.log 2>/dev/null' 2>/dev/null)
      prev_c=${prev_c:-0}
      echo "[$i $ts] Sol BACK UP -> LAUNCHED 3-stick SOAK (48GB, 42GB load, 4h); baseline crashes=$prev_c" >> "$LOG"
    else
      stat=$($SSH 'echo -n "c="; grep -c "^BOOT" campaign_boots.log 2>/dev/null; echo -n "r="; cat campaign_round.cnt 2>/dev/null; echo -n "f="; grep RESULT campaign32.log 2>/dev/null | grep -vc "bad_words=0 "; echo -n "run="; [ -f campaign.run ] && echo 1 || echo 0; echo -n "done="; grep -c "RESULT ROUND" campaign32.log 2>/dev/null; echo -n "last="; grep "RESULT ROUND" campaign32.log 2>/dev/null | tail -1' 2>/dev/null)
      c=$(echo "$stat" | sed -n 's/^c=//p'); r=$(echo "$stat" | sed -n 's/^r=//p')
      f=$(echo "$stat" | sed -n 's/^f=//p'); run=$(echo "$stat" | sed -n 's/^run=//p')
      done=$(echo "$stat" | sed -n 's/^done=//p'); last=$(echo "$stat" | sed -n 's/^last=//p')
      echo "[$i $ts] crashes=${c:-NA} round=${r:-NA} done=${done:-NA} flips=${f:-NA} run=${run:-NA} | $last" >> "$LOG"
      # SOAK: if the guard didn't re-arm the flag after a reboot, re-arm it ourselves so the load stays on.
      if [ "$run" = "0" ] && [ "$up" = "1" ]; then
        $SSH 'cd /home/maxre; touch campaign.run; pgrep -f /home/maxre/campaign.sh >/dev/null || setsid bash /home/maxre/campaign.sh >/dev/null 2>&1 < /dev/null &' 2>/dev/null
        echo "[$i $ts] re-armed flag+campaign (was NORUN) to keep soak going" >> "$LOG"
      fi
    fi
  fi
  sleep 50
done
echo "watcher-end" >> "$LOG"
