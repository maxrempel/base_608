#!/usr/bin/env bash
# Per-family cap: total budget / 9 concurrent families.
# Budget = 70% of measured line max (459 Mbps -> 322 Mbps night),
# capped at Max day limit 250 Mbps (07:00-23:00).
set -u
HOUR=$(date +%-H)
if [ "$HOUR" -ge 7 ] && [ "$HOUR" -lt 23 ]; then
  export RATE_KBPS=3390
else
  export RATE_KBPS=4360
fi
exec /usr/bin/python3 /home/maxre/1kgp_longread_trios/software/assembly_downloader_v01.py --family "$1"
