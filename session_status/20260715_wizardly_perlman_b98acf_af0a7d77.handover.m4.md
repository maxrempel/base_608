# Scribe handover - milestone 4 (~309K tokens)
# session: 20260715_wizardly_perlman_b98acf_af0a7d77
# cwd: C:\claude_base\.claude\worktrees\wizardly-perlman-b98acf
# written: 2026-07-15 07:26:44 by deepseek-v4-pro

# HANDOVER: 1000 Genomes 600?Trio NPA Mapping - Point and Omega

---

## GOAL (Max's own words)

> *"let's now focus on mapping - what is downloadable - we are interested in replicating the results from 1000genomes - 600 trios - looking for NPAs - point and omega type."*

The work is to identify exactly which files to pull so we can rerun an NPA (novel?insertion / de?novo point) analysis on the 1000 Genomes high?coverage trio panel, treat it as open?access, and then decide how to get the data onto an appropriate machine for the two separate analyses: single?base point NPAs and omega (insertion) NPAs.

---

## DECISIONS MADE (and WHY)

### 1. Target dataset identified as the open 1000 Genomes 30x panel
- The "600 trios" turned out to be the **1000 Genomes High Coverage 30x WGS GRCh38 resource** (Byrska?Bishop 2022 paper).
- The cohort contains **603 complete mother?father?child trios**.
- **This data is fully open?access** - no dbGaP application, no decryption key, not gated.  
  *(WHY: The earlier autism dbGaP track is open only for GRU controls and remains paused pending a decision about a DS?ASD amendment. That path is separate and not needed here.)*

### 2. Two NPA types require two different data layers
- **Point NPAs (de novo single?base)** live in **variant calls**, not reads ? small (~35?GB) download.
- **Omega NPAs (insertions / foreign?DNA)** live in **reads** ? need whole?genome alignments (~15?GB per sample, ~28?TB for all 603 trios).

### 3. Lak is the agreed home machine for downloads
- Max said "use Lak".  
- Lak (Debian?12, 656?GB free) can hold the point?NPA variant set easily and can stream one trio at a time for the omega pilot, but cannot store the full 28?TB of alignments.

### 4. Point?NPA data: a **caution flag** was raised but not resolved
- The publicly available **phased SNV+INDEL+SV VCFs** (~35?GB) are a polished panel version that **may have stripped Mendelian?violation sites** - exactly the sites a de?novo caller would pull.
- The assistant noted that *for de?novo detection we should use raw/unfiltered trio calls or re?call from per?sample files*, but did not yet identify where the raw per?sample gVCFs (or raw VCFs) are on the FTP server.  
  *(WHY: We need to verify what variant data is downloadable and fit?for?purpose before downloading gigabytes of possibly wrong files.)*

### 5. Omega approach: two viable strategies, not yet chosen
- **Stream through Lak**: pull one trio (three ~15?GB CRAMs), process, save small result, delete, loop. Peak disk stays low. Downside: 28?TB over home internet is slow.
- **Process in the cloud**: the same CRAMs live on Amazon's open?data / AnVIL. Run the omega detector there, never download the raw alignments. This is the scalable answer.
- The assistant recommended a **small pilot on Lak** (one trio) for omega while setting up the cloud path.

---

## CURRENT STATE

- **Mapping is complete** for the top?level structure of the 1000 Genomes high?coverage FTP tree:
  - Root: `http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage`
  - Pedigree with 603 trios: `20130606_g1k_3202_samples_ped_population.txt`
  - Phased variant directory: `working/20220422_3202_phased_SNV_INDEL_SV/` (~35?GB total, `.vcf.gz` + `.tbi` files)
  - CRAMs at EBI: pattern `https://ftp.sra.ebi.ac.uk/vol1/run/ERR323/ERR3239480/NA12718.final.cram` (example from a pilot lookup).
- **No 1000 Genomes downloads have started** on Lak.
- **Lak is ready**: the SRA toolkit is installed (but won't be used for 1000?Genomes work). Basic tools like `wget` are present; `samtools`/`bcftools` may be absent - not yet checked.
- **The dbGaP pilot (autism GRU run SRR7480235) may still be running** on Lak (its `prefetch` was pulling reference genome pieces, not the main data). It is unrelated to 1000?Genomes and can be stopped or left to idle - it does not block anything.
- **No decisions are pending** about the earlier autism data amendment; that is a separate track.
- **The browser lock (Playwright) is released** - no session is holding it.

---

## EXACT NEXT STEP (what a cold session should do first)

The immediate priorities:

1. **Clarify the correct point?NPA variant source with Max.**  
   - Ask: *"The phased panel VCFs likely strip Mendelian violations - do you want me to look for raw per?sample gVCFs (or unphased SNV calls) on the FTP instead? Or do you have a known file set in mind?"*

2. **Start the omega pilot on Lak while the question is open.**  
   - Pick one trio from the pedigree.  
   - Download its three CRAM files to Lak using `wget` (or `aria2` if available) into a working directory, e.g. `~/genomics/1kGP_omega_pilot/`.  
   - Check available disk, throttle if needed.  
   - Log the result.

3. **Investigate cloud?processing options for omega at scale.**  
   - Look up the 1000 Genomes bucket on AWS (`s3://1000genomes`) or the AnVIL workspace.  
   - Confirm Terra access (Max has an account).  
   - Draft a plan: e.g., spin up a VM, mount the bucket, run the omega detector on all trios, export results.

4. **Resume the point?NPA download** once the file?source question is settled.  
   - Most likely pull from the FTP into Lak under `~/genomics/1kGP_point_NPA/`.  
   - Ensure `bcftools` is installed on Lak for downstream processing.

---

## OPEN QUESTIONS AWAITING MAX

- **Point variant source:** Should we use the phased panel VCF (~35?GB) despite the Mendelian?violation strip, or locate raw per?sample gVCFs / unphased SNV calls?  
- **Omega execution venue:** Stream through Lak (trio?by?trio) or process fully in the cloud (AWS / AnVIL)?  
- **Disk policy on Lak:** Is it acceptable to use the 656?GB for temporary storage of one trio's CRAMs, or should we keep it strictly for final results?

---

## KEY PATHS, IDs, COMMANDS, NAMES

| What | Path / Value |
|------|--------------|
| 1000G FTP root | `http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage` |
| Pedigree (603 trios) | `.../20130606_g1k_3202_samples_ped_population.txt` |
| Phased VCFs | `.../working/20220422_3202_phased_SNV_INDEL_SV/` (exact filenames unlisted, ~35?GB) |
| CRAM example | `https://ftp.sra.ebi.ac.uk/vol1/run/ERR323/ERR3239480/NA12718.final.cram` |
| Lak SSH | `ssh -i ~/.ssh/lakarian_key.pem mrempadmin@100.110.225.89` |
| Lak free space | ~656?GB (confirmed) |
| Tools on Lak | SRA toolkit in `~/genomics/dbgap/tools/sratoolkit.*/bin/`; `wget` present; `samtools`/`bcftools` status unknown |
| dbGaP key (autism track) | `~/genomics/dbgap/keys/prj_42416.ngc` (not needed for 1000G) |
| 1000G SRA accession (example) | Pilot GRU run was `SRR7480235` (autism) - not 1000G; use CRAM paths instead |
| Notion status page | "[XG1 Autism Data Access - Consolidated Status & Unstuck Plan](https://app.notion.com/p/39d0316f556081d3968ae2e68d1fb677)" - the 1000G mapping will likely get its own subpage later. |

---

## GOTCHAS & DEAD ENDS ALREADY RULED OUT

- **The earlier dbGaP autism path is a dead end for 1000?Genomes work.** It was explored in
