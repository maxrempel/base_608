#!/usr/bin/env bash
set -u

echo PRIVATE_WGS
find /home/rempel/genomics/kenefick -maxdepth 4 -type f \
  \( -name '*.bam' -o -name '*.cram' -o -name '*.bai' -o -name '*.crai' \) \
  -printf '%p\t%s\n' | sort | head -120

echo PUBLIC_LOCAL_WGS
find /home/rempel/genomics/popref -maxdepth 4 -type f \
  \( -name '*.cram' -o -name '*.crai' \) \
  -printf '%p\t%s\n' 2>/dev/null | sort | head -120
