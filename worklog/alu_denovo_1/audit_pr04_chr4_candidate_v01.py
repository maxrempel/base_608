#!/usr/bin/env python3
import hashlib, importlib.util, json
from collections import Counter
from pathlib import Path

spec = importlib.util.spec_from_file_location('a', '/home/rempel/genomics/_analysis/aluya5_exact_copy_npa_v01/code/analyze_aluya5_exact_copy_npa_onepass_v02.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
root = Path('/home/rempel/genomics/_analysis/aluya5_exact_copy_npa_v01/temp/target_crams/PR04/chr4')
roles = {'father':'HG00640','mother':'HG00641','child':'HG00642'}
pos = 77421635
out = {'status':'technical_screen_candidate_not_biological','family':'PR04','chromosome':'chr4','position_1based':pos+1,'reference_base':'C','child_candidate_base':'A','tiers':{}}
for tier, mq, bq in (('primary',30,25),('strict',60,30)):
    out['tiers'][tier]={'min_mapq':mq,'min_baseq':bq,'roles':{}}
    for role, sample in roles.items():
        with a.pysam.AlignmentFile(str(root/sample/f'{sample}.final.cram'),'rc',reference_filename='/home/rempel/genomics/controls/GRCh38DH.fa') as bam:
            e=a.pileup_chromosome(bam,'chr4',{pos},mq,bq)
        rows=e.get(pos,{})
        counts=Counter({base:len(v) for base,v in rows.items()})
        alt=rows.get('A',[])
        out['tiers'][tier]['roles'][role]={'depth':sum(counts.values()),'base_counts':{x:counts.get(x,0) for x in 'ACGT'},'candidate_reads':len(alt),'candidate_forward':sum(x[3]=='forward' for x in alt),'candidate_reverse':sum(x[3]=='reverse' for x in alt),'candidate_read_hashes':sorted({hashlib.sha256(x[4].encode()).hexdigest()[:16] for x in alt}),'candidate_mapq':sorted(x[0] for x in alt),'candidate_baseq':sorted(x[1] for x in alt),'candidate_edge_distance':sorted(x[2] for x in alt)}
print(json.dumps(out,indent=2))
