# Alusieve strict-survivor adjudication script draft

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL), role Alusieve.

## Objective

Draft a deterministic, audit-only Python analysis and small shell runner for two
sealed strict Aluminum screen survivors. The script must not change production,
the frozen caller, or frozen labels.

Read and reuse patterns from:

- `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts\audit_alusieve_locus_credibility_v01.py`
- `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts\run_alusieve_locus_credibility_v01.sh`

Targets and authoritative ENA CRAMs:

1. family 1377, chr4:61750563 G>A; child NA10865 ERR3989302, mother NA11892 ERR3239461, father NA11891 ERR3989305.
2. family PR26, chr5:51264043 G>A; child HG01087 ERR3988836, mother HG01086 ERR3241817, father HG01085 ERR3241816.

Reference on Taygeta:
`/mnt/green24/kenefick/aluya5_pilot_v01/heavy_input/reference/GRCh38_full_analysis_set_plus_decoy_hla.fa`

Output root on Taygeta:
`/mnt/green24/kenefick/alusieve_attrition_audit_v01/strict_survivor_adjudication_v01`

## Required evidence

- Raw and filtered trio pileups at each site, including base, base quality,
  mapping quality, strand, read number, CIGAR, clipping, supplementary/secondary,
  duplicate flag, template/read name, alignment and fragment starts, read group,
  flowcell and lane.
- Counts at raw 0/0, permissive 20/20, primary 40/30, and strict 60/30.
- Diploid genotype likelihoods for GG, GA, AA from individual base and mapping
  qualities, normalized PL and GQ, with an explicit documented error model.
- Child allele balance and exact two-sided binomial P under 0.5.
- Unique alternate templates, starts and fragment signatures; strand/read-number,
  read-group, flowcell and lane distributions against child reference reads.
- Local haplotype consistency: compare flanking bases co-observed on child
  alternate and reference reads, identify informative nearby heterozygous sites,
  and report whether alternate reads form a coherent local haplotype.
- Permissive parent search and exact parent genotype evidence.
- Machine-readable TSV/JSON plus checksum manifest and atomic completion marker.
- A shell runner that additionally extracts bounded trio BAMs and runs an
  independent bcftools mpileup/call at raw and strict thresholds. It may query
  the public 3,202-sample high-coverage phased panel using the URL pattern:
  `https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20201028_3202_phased/CCDG_14151_B01_GRM_WGS_2020-08-05_chr{chrom}.filtered.shapeit2-duohmm-phased.vcf.gz`
- Keep the work resumable and bounded to roughly +/-2 kb per locus, 2 threads.

Do not make a biological mutation classification automatically. Produce exact
evidence for Codex to adjudicate as sequence-supported de novo, unresolved, or
technical artifact. Provide patch-ready code and a concise testing checklist in
`result.md`; do not edit the repository.
