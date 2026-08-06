#!/usr/bin/env bash
# Queue supervisor for 1KGP trio downloads. Loops every 10 minutes:
#   1. Advances the assembly queue (resume_assemblies_v01.sh).
#   2. When every assembly family is complete, advances the aligned-reads queue.
# Safe to restart at any time; all logic is idempotent.
set -u
ROOT="${KGTRIO_ROOT:-/home/maxre/1kgp_longread_trios}"
GREEN="${KGTRIO_GREEN:-/mnt/green24/1kgp_longread_trios}"
LOG="$GREEN/logs/supervisor.log"
mkdir -p "$(dirname "$LOG")"
log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG"; }

all_complete() {
  local manifest="$1" fam st
  [ -f "$manifest" ] || return 1
  fams=$(awk -F '\t' 'NR > 1 {print $1}' "$manifest" | awk '!seen[$0]++')
  [ -n "$fams" ] || return 1
  for fam in $fams; do
    st="$GREEN/state/$fam.json"
    if ! { [ -f "$st" ] && grep -q '"status": "complete"' "$st"; }; then
      return 1
    fi
  done
  return 0
}

log "supervisor start pid=$$"
while true; do
  if findmnt -n /mnt/green24 >/dev/null 2>&1; then
    bash "$ROOT/software/resume_assemblies_v01.sh" >> "$LOG" 2>&1 || log "resume_assemblies rc=$?"
    if all_complete "$ROOT/ASSEMBLY_MANIFEST_v01.tsv"; then
      log "all assembly families complete; advancing aligned-reads queue"
      bash "$ROOT/software/resume_aligned_v01.sh" >> "$LOG" 2>&1 || log "resume_aligned rc=$?"
    fi
  else
    log "WARNING: /mnt/green24 not mounted; skipping cycle"
  fi
  sleep 600
done