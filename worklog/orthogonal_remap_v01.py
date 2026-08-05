import csv, os, sys
import pysam
from Bio.Align import PairwiseAligner

ref_path='/home/rempel/genomics/controls/GRCh38DH.fa'
cand='/home/rempel/genomics/npa_private/pjl_control_response_v01/control_candidates.tsv'
out=sys.argv[1]
rows=list(csv.DictReader(open(cand),delimiter='\t'))
regs={}
for x in rows: regs.setdefault(x['region'],[]).append(x)
fa=pysam.FastaFile(ref_path); al=PairwiseAligner(); al.mode='local'
al.match_score=2; al.mismatch_score=-3; al.open_gap_score=-5; al.extend_gap_score=-1
outf=open(out,'w'); outf.write('sample\tregion\treads\tref_preference\talt_preference\ttied\tmedian_delta\tmean_delta\n')
roots={'HG02683':'/home/rempel/genomics/npa_private/orthogonal_audit_v01/HG02683','HG02495':'/home/rempel/genomics/npa_private/pjl_control_response_v01','HG02605':'/home/rempel/genomics/npa_private/pjl_control_response_v01'}
for region,vs in regs.items():
 if region.startswith('chr15:'): continue
 chrom,start,end=region.split(':')[0],*map(int,region.split(':')[1].split('-')); seq=fa.fetch(chrom,start-1,end).upper(); alt=list(seq); failed=False
 for v in vs:
  p=int(v['pos'])-start
  if seq[p]!=v['ref'].upper(): failed=True; break
  alt[p]=v['alt'].upper()
 if failed: continue
 ref=''.join(seq); alt=''.join(alt)
 for sample,root in roots.items():
  mpath=os.path.join(root,'alignment_extract_response_manifest_v01.tsv')
  manifest=[x for x in csv.DictReader(open(mpath),delimiter='\t') if x.get('sample')==sample and x.get('region')==region]
  if not manifest: continue
  bam=pysam.AlignmentFile(os.path.join(root,manifest[0]['bam']))
  ds=[]
  for r in bam.fetch(chrom,start-1,end):
   if r.is_unmapped or not r.query_sequence: continue
   s=r.query_sequence.upper(); sr=al.score(s,ref); sa=al.score(s,alt); ds.append(sa-sr)
  n=len(ds); rp=sum(d<0 for d in ds); ap=sum(d>0 for d in ds); tie=sum(d==0 for d in ds)
  med=sorted(ds)[n//2] if n else 0; mean=sum(ds)/n if n else 0
  outf.write(f'{sample}\t{region}\t{n}\t{rp}\t{ap}\t{tie}\t{med:.3f}\t{mean:.3f}\n')
outf.close()
