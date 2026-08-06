#!/usr/bin/env bash
# Start (or keep running) up to MAX_ACTIVE family assembly downloads, in queue order.
# Safe to run repeatedly. Families already complete are skipped.
set -u
ROOT="${KGTRIO_ROOT:-/home/maxre/1kgp_longread_trios}"
GREEN="${KGTRIO_GREEN:-/mnt/green24/1kgp_longread_trios}"
MAX_ACTIVE="${MAX_ACTIVE:-3}"
UNIT="kgp-assembly-dl-v01"

findmnt -n /mnt/green24 >/dev/null 2>&1 || { echo "FATAL: /mnt/green24 not mounted"; exit 1; }
mkdir -p "$GREEN/data" "$GREEN/state" "$GREEN/logs" "$GREEN/software"

families=$(awk -F '\t' 'NR > 1 {print $1}' "$ROOT/ASSEMBLY_MANIFEST_v01.tsv" | awk '!seen[$0]++')
active=0
for fam in $families; do
  st="$GREEN/state/$fam.json"
  if [ -f "$st" ] && grep -q '"status": "complete"' "$st"; then
    echo "complete: $fam"
    continue
  fi
  if systemctl --user is-active --quiet "$UNIT@$fam"; then
    echo "active:   $fam"
    active=$((active + 1))
    continue
  fi
  if [ "$active" -ge "$MAX_ACTIVE" ]; then
    echo "queued:   $fam"
    continue
  fi
  echo "starting: $fam"
  if systemctl --user start "$UNIT@$fam"; then
    active=$((active + 1))
  fi
done
echo "---"
systemctl --user list-units "$UNIT@*" --no-legend 2>/dev/null || true
