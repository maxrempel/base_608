import csv, subprocess, sys, os, re
from collections import defaultdict, Counter

root, manifest, cand, out = sys.argv[1:]
candidates=defaultdict(list)
with open(cand, newline='') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        candidates[r['region']].append((int(r['pos']),r['ref'],r['alt']))
rows=[]
with open(manifest, newline='') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        rows.append(r)
def read_bases(line, sites):
    a=line.rstrip('\n').split('\t'); name=a[0]; flag=int(a[1]); pos=int(a[3]); cigar=a[5]; seq=a[9]
    q=0; refpos=pos; got={}
    for n,op in re.findall(r'(\d+)([MIDNSHP=X])',cigar):
        n=int(n)
        if op in 'M=X':
            for j in range(n):
                if refpos+j in sites: got[refpos+j]=seq[q+j]
            refpos+=n; q+=n
        elif op in 'I S': q+=n
        elif op in 'DN': refpos+=n
    return name,got
with open(out,'w',newline='') as fo:
    w=csv.writer(fo,delimiter='\t'); w.writerow(['sample','region','bam','reads_with_any_candidate','haplotype','read_count','candidate_sites_observed'])
    for r in rows:
        region=r['region']; sites=candidates.get(region,[])
        if not sites: continue
        sm=r['sample']; bam=os.path.join(root,r['bam']); posset={x[0] for x in sites}; labels={x[0]: (x[1],x[2]) for x in sites}; counts=Counter(); n=0
        p=subprocess.Popen(['samtools','view','-h',bam],stdout=subprocess.PIPE,text=True)
        for line in p.stdout:
            if line.startswith('@'): continue
            name,got=read_bases(line, posset)
            if not got: continue
            n+=1; h=[]
            for po in sorted(got):
                ref,alt=labels[po]; b=got[po]
                h.append('R' if b==ref else 'A' if b==alt else 'O')
            counts[''.join(h)] += 1
        p.wait()
        for h,c in sorted(counts.items()): w.writerow([sm,region,r['bam'],n,h,c,len(h)])
