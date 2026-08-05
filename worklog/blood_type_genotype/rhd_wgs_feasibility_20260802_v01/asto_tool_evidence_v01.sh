#!/usr/bin/env bash
set -u

for p in \
  /home/rempel/miniconda3/envs/manta_env/bin/python \
  /home/rempel/miniconda3/envs/manta_env/bin/configManta.py \
  /home/rempel/genomics/popref/delly_out/oliver.vcf.gz \
  /home/rempel/genomics/popref/delly_out/kristen.vcf.gz
do
  if test -e "$p"; then
    stat -c 'present=%n bytes=%s mtime=%y' "$p"
  else
    echo "missing=$p"
  fi
done
