#!/usr/bin/env bash
# Cloudflare R2 + D1 -> Lak restic backup. Created 2026-06-02 by Claude Opus 4.8 for Max.
# Stream 2 of the CF backup design. Captures EVERYTHING heavy/growing with GFS thinning:
#   - R2 media (images, audio, video) via rclone sync
#   - ALL D1 databases (site text, books, design data) via the db-backup-export worker
# Stream 1 (worker code + KV) -> GitHub separately (kept forever, diffable).
# No silent fallbacks: any error aborts with non-zero and is logged loudly.
set -euo pipefail

BASE="/home/mrempadmin/cf_backups"
export RESTIC_REPOSITORY="$BASE/restic_r2"
export RESTIC_PASSWORD_FILE="$BASE/keys/restic_pw.txt"
STAGE_ROOT="$BASE/staging"          # restic backs up this whole tree (r2 + d1)
R2_STAGE="$STAGE_ROOT/r2"
D1_STAGE="$STAGE_ROOT/d1"
LOG="$BASE/logs/backup_$(date +%Y%m%d_%H%M%S).log"
BUCKETS="babel-files postcontact-media postcontact-podcast tamza-media"
DB_URL="https://db-backup-export.max-rempel2.workers.dev"
DB_SECRET="$(cat "$BASE/keys/db_export_secret.txt")"

exec > >(tee -a "$LOG") 2>&1
echo "=== CF backup start $(date -u +%FT%TZ) ==="

# --- R2 media ---
for b in $BUCKETS; do
  echo "--- rclone sync r2:$b ---"
  rclone sync "r2:$b" "$R2_STAGE/$b" --fast-list --transfers 16 --checkers 32 --stats-one-line --stats 30s
done

# --- D1 databases (all of them, via the read-only export worker) ---
echo "--- D1 dumps ---"
mkdir -p "$D1_STAGE"
DBS=$(curl -fsS --retry 5 --retry-delay 3 --retry-all-errors -m 60 -H "Authorization: Bearer $DB_SECRET" "$DB_URL/" \
      | python3 -c "import sys,json;print('\n'.join(json.load(sys.stdin)['databases']))")
for db in $DBS; do
  echo "  dump $db"
  curl -fsS --retry 5 --retry-delay 3 --retry-all-errors -m 120 -H "Authorization: Bearer $DB_SECRET" "$DB_URL/db/$db" -o "$D1_STAGE/$db.json.tmp"
  python3 -c "import json,sys; d=json.load(open('$D1_STAGE/$db.json.tmp')); assert d.get('tables') is not None"
  mv "$D1_STAGE/$db.json.tmp" "$D1_STAGE/$db.json"
done

echo "--- restic backup ---"
restic backup "$STAGE_ROOT" --tag cf-r2 --host lakarian

# Long tail = one snapshot per 6-month period, kept forever via tag.
# (restic has no native semiannual unit; tagging is the clean idiom.)
PERIOD="$(date +%Y)H$([ "$(date +%-m)" -le 6 ] && echo 1 || echo 2)"
if [ "$(restic snapshots --tag "$PERIOD" --json 2>/dev/null)" = "[]" ]; then
  echo "tagging latest snapshot as semiannual $PERIOD"
  restic tag --add semiannual --add "$PERIOD" latest
fi

echo "--- restic forget + prune ---"
# Recent ladder: 48 half-hourly (24h), 7 daily, 8 weekly, 12 monthly (1yr).
# Long tail: every snapshot tagged 'semiannual' is kept (1 per 6mo, ~20 over 10yr).
restic forget --tag cf-r2 --keep-last 48 --keep-daily 7 --keep-weekly 8 --keep-monthly 12 --keep-tag semiannual --prune

echo "--- snapshots ---"
restic snapshots --tag cf-r2 --compact | tail -15

# Status manifest (latest run summary) for monitoring
STAT="$BASE/status.txt"
{
  echo "Last CF backup: $(date -u +%FT%TZ)"
  echo "Repo: $RESTIC_REPOSITORY"
  echo "D1 dbs dumped: $(echo "$DBS" | tr '\n' ' ')"
  restic stats --tag cf-r2 --mode raw-data 2>/dev/null | grep -i "total" || true
} > "$STAT"
echo "=== CF backup OK $(date -u +%FT%TZ) ==="
