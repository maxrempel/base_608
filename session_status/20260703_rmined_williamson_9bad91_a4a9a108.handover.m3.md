# Scribe handover - milestone 3 (~238K tokens)
# session: 20260703_rmined_williamson_9bad91_a4a9a108
# cwd: C:\claude_base\.claude\worktrees\determined-williamson-9bad91
# written: 2026-07-03 16:48:46 by deepseek-v4-pro

# HANDOVER: Track-2 - XG1 Paper Reproduction + Genome-Wide Hotspot Map

## MAX'S GOAL (his words, distilled)
Reanalyse his XG1 paper's central finding (581 parent?child trios from 1000 Genomes, find long runs - "haplotype substitutions" - where a child carries alleles absent from both parents, first spotted on chromosome 3 at ~75.5?Mb), then extend the same detector **genome?wide**, map where these non?parental?allele (NPA) hotspots recur across unrelated people, and later feed additional datasets (autism hotspots, etc.). He wants a "map of recurrent anomalies," not a single?SNP de?novo caller.

## DECISIONS MADE (and why)

1. **Reproduce the exact original method rather than reinvent it.**
   *Why:* Max's paper (viXra:2505.0194) and his own Python code on GitHub (https://github.com/maxrempel/xg1, cloned to `C:\claude_base\projects\XG1\paper_reproduction_src`) give the algorithm verbatim - sliding 60?SNP window, 20?SNP step, count alleles in child not in either parent, flag windows with ?5?NPAs, collapse overlaps, classify. Reusing his logic guarantees comparability.

2. **Split the pipeline into two agents: detector (X12B) and recurrence?map aggregator (X11B).**
   *Why:* X11B had already claimed the extension lane (genome?wide recurrence mapping) when X12B was assigned the whole paper. A clean interface avoided duplication: X12B emits one per?trio TSV of collapsed NPA regions (only runs, not isolated single NPAs); X11B consumes that file and builds recurrence bins.

3. **Use Lak (100.110.225.89) as the primary compute box.**
   *Why:* Max cannot provide a dedicated machine; he "uses a Locarian" (likely his local desktop) which is throttled. Lak (RempelServer, 8?core, 700?GB free, Python 3.11) was already accessible over SSH (key `~/.ssh/lakarian_key.pem`, user `mrempadmin`) and could be set up quickly. It is throttled to ~40?% CPU/disk and ~10?% internet - but that is enough for a selective fetch.

4. **Avoid full?chromosome download by range?fetching only the hotspot window via pysam.**
   *Why:* The raw 1000G NYGC 30? GRCh38 VCF for chr3 alone is 115?GB; the whole genome would be ~3?TB. A throttled home line cannot pull that. The file's index supports region queries, so we can pull just the few?MB window around chr3:75.5?Mb to reproduce HG01505's cluster. That test uses negligible bandwidth and respects Max's usage.

5. **Install pysam in a venv on Lak, not system?wide.**
   *Why:* apt?installed tabix lacked HTTP support; pysam's bundled htslib has curl. System pip was blocked by PEP 668, so a venv (`~/xg1_paper_repro/venv`) was created with pysam 0.24. This worked and avoids breaking the system Python.

6. **Detector output schema matches X11B's aggregator exactly.**
   *Why:* X11B expects one file per trio, per?variant rows (`child_id, chrom, pos, ref, alt, type, qual`), deduped per child, and only variants inside qualifying runs. The detector emits exactly that TSV (with `type` = "NPA_haplotype") and drops isolated NPAs below the window threshold.

## CURRENT STATE (as of the last turn)

- **Detector** is built, tested on synthetic data, and staged on Lak:  
  `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts\npa_detector.py`  
  Also copied to Lak at `~/xg1_paper_repro/scripts/npa_detector.py`.
- **Aggregator** (X11B's piece) is built and synthetic?tested; its input spec is documented in  
  `C:\claude_base\projects\XG1\kenefick\paper_repro\hotspot_aggregator_method_v01_tomemex.md`.
- **Paper source code** cloned locally for reference, but the active pipeline uses the newly written `npa_detector.py`, not the original notebooks.
- **Pedigree** file for 3202 samples (20130606_g1k.ped) downloaded to Lak at `~/xg1_paper_repro/data/` - includes all trios, HG01505's family is present.
- **Lak environment**:
  - SSH: `ssh -i ~/.ssh/lakarian_key.pem mrempadmin@100.110.225.89`
  - sudo password: `3fn81k3lwhhlrl4hlalz`
  - working directory: `~/xg1_paper_repro/`
  - venv: `~/xg1_paper_repro/venv/` (with pysam)
  - Python command inside venv: `~/xg1_paper_repro/venv/bin/python`
- **Probe fetch** to confirm the hotspot region is **in flight** on Lak.  
  A script (`fetch_region.py`) was submitted via SSH that uses pysam to pull 20?kb around `3:75500000` from the public URL  
  `http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20190425_NYGC_GATK/nygc_chr3_3202samples.vcf.gz`.  
  The task was spawned with `os.system` in the background - we do not yet have the result. The output is written to `~/xg1_paper_repro/probe_chr3_75500000.vcf`.

## EXACT NEXT STEP

1. **Check the probe fetch result.**  
   Log into Lak and look at `~/xg1_paper_repro/probe_chr3_75500000.vcf`.  
   a) If it contains variants and HG01505 appears with a dense cluster of NPAs ? the region is confirmed.  
   b) If empty or contig name miss (maybe the index uses "chr3" not "3") ? adjust the region string and re?run.

2. **If successful, widen the fetch window** to cover the entire original hotspot (maybe 75.4-75.6?Mb) and run the detector on that mini VCF + pedigree, comparing output counts to Max's 348 NPA for HG01505. That is the positive?control reproduction.

3. **If probe fails** because of HTTP/HTTPS or connectivity on Lak, fall back: download just the index + file locally using a tool that does work (e.g., `curl -r`) and copy the tiny slice to Lak, or run the fetch on a local machine and transfer.

4. **Once the chr3 hotspot reproduces, propose a genome?wide strategy to Max:**  
   The full raw dataset (~3?TB) cannot be pulled on a home line. The obvious path is a temporary cloud VM (AWS, with high?speed access to the 1000G bucket) to run the detector chromosome?by?chromosome and then bring only the aggregated results (a few GB at most) back. Present that as the next decision point; Max will need to approve the cloud spend.

5. **Log all progress** using `python C:\claude_base\compaction_kb\scripts\worklog.py log "..."`.

## OPEN QUESTIONS (pending Max's input)

- None right now. The positive?control test does not require Max. The cloud?compute question will be raised once reproducibility is shown.

## KEY FILE PATHS AND IDENTIFIERS

| item | path / detail |
|------|---------------|
| Local project root | `C:\claude_base\projects\XG1` |
| Original paper code (cloned) | `C:\claude_base\projects\XG1\paper_reproduction_src` |
| Active working directory | `C:\claude_base\projects\XG1\kenefick\paper_repro` |
| Detector script (local) | `C:\claude_base\projects\XG1\kenefick\paper_repro\scripts\npa_detector.py` |
| Detector method doc | `C:\claude_base\projects\XG1\kenefick\paper_repro\npa_detector_method_v01_tomemex.md` |
| Aggregator input spec (X11B) | `C:\claude_base\projects\XG1\kenefick\paper_repro\hotspot_aggregator_method_v01_tomemex.md` |
| Inter?agent board | `C:\claude_base\branch_bulletin\bcast.py` |
| Worklog | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| Lak SSH identity | `~/.ssh/lakarian_key.pem` (local) |
| Lak user & host | `mrempadmin@100.110.225.89` |
| Lak sudo pass | `3fn81k3lwhhlrl4hlalz` |
| Lak working dir | `~/xg1_paper_repro` |
| Lak venv | `~/xg1_paper_repro/venv` |
| Lak pedigree | `~/xg1_paper_repro/data/20130606_g1k.ped` |
| Lak probe script | `~/xg1_paper_repro/fetch_region.py` |
| Lak probe output | `~/xg1_paper_repro/probe_chr3_75500000.vcf` |
| Public VCF root | `http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20190425_NYGC_GATK/` |
| Chrome 3 file | `nygc_chr3_3202samples.vcf.gz` (115?GB, with `.tbi` index) |
| Hotspot coordinate | `3:75500000` (may need `chr3` prefix) |
| Paper | "Preliminary evidence of traces of alien genetic manipulation in humans", viXra:2505.0194 |
| GitHub repo | https://github.com/maxrempel/xg1 |

## GOTCHAS AND DEAD ENDS RULED OUT

- **Don't download whole chromosomes** - the throttled internet makes that infeasible. Region?fetch via index.
- **tabix on Lak is broken for remote files** (built without HTTP support). Use pysam's bundled htslib instead (installed in the venv).
- **Contig naming** - the VCF index may use `3` or `chr3`. The probe used `3`; be ready to switch to `chr3` if no variants are returned.
- **Single NPAs are noise** - Max explicitly warned that
