#!/usr/bin/env bash
set -u
HOUR=$(date +%-H)
if [ "$HOUR" -ge 7 ] && [ "$HOUR" -lt 23 ]; then
  export RATE_KBPS=7000
else
  export RATE_KBPS=9000
fi
exec /usr/bin/python3 /home/maxre/1kgp_longread_trios/software/assembly_downloader_v01.py --family "$1"
