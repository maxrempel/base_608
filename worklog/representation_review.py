import csv, subprocess, sys, os, re, statistics
from collections import defaultdict
root, manifest, cand, out = sys.argv[1:]
candidates=defaultdict(list)
with open(cand,newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
    candidates[r['region']].append((int(r['pos']),r['ref'],r['alt']))
def parse(line, sites):
  a=line.rstrip().split('\t'); flag=int(a[1]); pos=int(a[3]); mapq=int(a[4]); cigar=a[5]; seq=a[9]
  q=0; rp=pos; got={}; soft=0; indel=0
  for n,op in re.findall(r'(\d+)([MIDNSHP=X])',cigar):
    n=int(n)
    if op in 'M=X':
      for j in range(n):
        if rp+j in sites: got[rp+j]=seq[q+j]
      rp+=n; q+=n
    elif op in 'IS': q+=n; soft += n if op=='S' else 0; indel += n if op=='I' else 0
    elif op in 'DN': rp+=n; indel += n
    elif op in 'HP': pass
  return flag,mapq,pos,got,soft,indel
rows=[]
with open(manifest,newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
with open(out,'w',newline='') as fo:
  w=csv.writer(fo,delimiter='\t'); w.writerow(['sample','region','class','reads','median_mapq','both_strands','duplicate_reads','secondary_reads','supplementary_reads','softclip_reads','indel_reads','distinct_starts','callable_reads'])
  for r in rows:
    region=r['region']; sites=candidates.get(region,[]); labels={p:(ref,alt) for p,ref,alt in sites}; bam=os.path.join(root,r['bam']); rec=defaultdict(list)
    p=subprocess.Popen(['samtools','view','-h',bam],stdout=subprocess.PIPE,text=True)
    for line in p.stdout:
      if line.startswith('@'): continue
      flag,mq,start,got,soft,indel=parse(line,{x[0] for x in sites})
      if not got: continue
      vals=[labels[p][1] if b==labels[p][1] else labels[p][0] if b==labels[p][0] else 'O' for p,b in got.items()]
      cls='alternate' if 'A' in vals else 'reference' if all(v=='R' for v in vals) else 'other'
      rec[cls].append((flag,mq,start,soft,indel))
    p.wait()
    for cls in ('alternate','reference','other'):
      z=rec[cls]
      if not z: continue
      w.writerow([r['sample'],region,cls,len(z),round(statistics.median(x[1] for x in z),2),len({x[0]&16 for x in z})>1,sum(bool(x[0]&1024) for x in z),sum(bool(x[0]&256) for x in z),sum(bool(x[0]&2048) for x in z),sum(x[3]>0 for x in z),sum(x[4]>0 for x in z),len({x[2] for x in z}),sum(len(v) for v in rec.values())])
