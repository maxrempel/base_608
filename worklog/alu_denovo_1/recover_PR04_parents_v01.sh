#!/usr/bin/env bash
set -euo pipefail

root=/home/rempel/genomics/aluya5_family_stream_v01/source_recovery_v01
manifest="$root/deployment/PR04_source_recovery_manifest_v01.tsv"
runner="$root/deployment/recover_aluya5_source_input_v01.sh"
output="$root/accepted_inputs"
reference=/home/rempel/genomics/controls/GRCh38DH.fa

export PATH="$root/deployment/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export ALUYA5_RECOVERY_RATE=${ALUYA5_RECOVERY_RATE:-500K}

"$runner" "$manifest" HG00641 "$output" "$reference"
"$runner" "$manifest" HG00640 "$output" "$reference"
