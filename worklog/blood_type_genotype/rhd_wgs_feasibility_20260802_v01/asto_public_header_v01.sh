#!/usr/bin/env bash
set -u

root=/home/rempel/genomics/popref/omega_balanced20_v01/inputs_replaceable
count=$(find "$root" -mindepth 2 -maxdepth 2 -type f -name '*.final.cram' | wc -l)
echo "local_public_crams=$count"
f="$root/HG00555/HG00555.final.cram"
samtools quickcheck -v "$f"
samtools view -H "$f" | awk -F '\t' '$1=="@HD" || ($1=="@SQ" && ($2=="SN:chr1" || $2=="SN:1")) || $1=="@RG" {print; n++; if(n>=5) exit}'
