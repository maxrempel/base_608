#!/usr/bin/env bash
set -u

for f in \
  /home/rempel/genomics/kenefick/oliver/oliver.mq.bam \
  /home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam
do
  echo "FILE=$f"
  if test -f "$f"; then
    stat -c 'bytes=%s mtime=%y' "$f"
    for i in "$f.bai" "${f%.bam}.bai"; do
      if test -f "$i"; then
        stat -c 'index=%n bytes=%s mtime=%y' "$i"
      fi
    done
    samtools quickcheck -v "$f"
    samtools view -H "$f" | awk -F '\t' '$1=="@HD" || ($1=="@SQ" && ($2=="SN:chr1" || $2=="SN:1")) || $1=="@RG" {print; n++; if(n>=8) exit}'
  else
    echo missing
  fi
done

echo TOOLS
command -v samtools || true
samtools --version | head -2
for tool in mosdepth cnvkit.py delly manta gridss sniffles bcftools; do
  printf '%s=' "$tool"
  command -v "$tool" || true
done
