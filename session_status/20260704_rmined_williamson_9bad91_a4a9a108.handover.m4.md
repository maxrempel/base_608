# Scribe handover - milestone 4 (~315K tokens)
# session: 20260704_rmined_williamson_9bad91_a4a9a108
# cwd: C:\claude_base\.claude\worktrees\determined-williamson-9bad91
# written: 2026-07-04 07:12:19 by deepseek-v4-pro

GOAL (Max's own words)
> "I don't care about this chromosome 3 artifact. It was just a pilot experiment, which now has a lot of questions. So we just need to repeat the whole work."

We are to **reproduce and extend Max's XG1 paper** - run a genome?wide scan for long non?parental?allele (NPA) haplotypes in all 1000?Genomes trios, map where they recur across unrelated children, and exclude segmental?duplication noise. No more chr?3 only; every chromosome, every trio, from the raw GT VCFs.

DECISIONS MADE & WHY
1. **Drop the chr?3 pilot entirely.** The original flagship hotspot (chr3:75.5?Mb) is a segmental duplication artifact - X11B confirmed it. The real work is genome?wide.
2. **Use the raw?GT VCFs, not the phased panel.** Phased VCFs discard parent?mismatch alleles, which is exactly the signal we hunt.
3. **Detector definition (from Max's paper & code):** For each trio, a NPA = a SNP where the child carries an allele absent in both parents. Count NPAs in overlapping 60?SNP windows (step 20), flag windows with ?5 NPAs, collapse overlaps, classify regions (Normal?<?10, Possible?hybrid?10?19, Definite?hybrid???20). Only emit NPAs inside qualifying collapsed haplotype runs - isolated single NPAs are dropped (they are noise).
4. **Hardened with real?data QC:**  
   - Keep only FILTER=PASS sites.  
   - Keep only biallelic SNPs.  
   - Mask known segmental duplications with a BED file (X11B's segdup mask).  
   - Otherwise stick to the original 5?NPA window trigger.
5. **AWS EC2 for genome?wide compute**, because the full raw dataset is ~3?TB and Lak's internet is throttled to 10?%. The 1000?Genomes raw?GT files live on `s3://1000genomes` (AWS Open Data); reading them from an EC2 instance in us?east?1 is **free and fast**.
6. **Temporary spot/on?demand instance** - small spend (~$15) - run the scan, pull back only the small per?child results, then terminate. Max's AWS account was already confirmed working. Max previously sanctioned temporary cloud VMs for genomics.

CURRENT STATE
- **Detector code** built, synthetic?tested, hardened with PASS/biallelic/segdup, committed to `projects/XG1/kenefick/paper_repro/scripts/`. The core script is `npa_detector.py`; the genome?wide orchestrator (reads S3, loops chromosomes, writes per?trio output) is `genome_scan.py`. Helper scripts: `fetch_region.py` (HTTP range fetch), `lak_fetch.sh` (launcher for Lak).
- **Segdup mask file** exists (X11B's work), merged into the same repo. Exact path: `projects/XG1/kenefick/paper_repro/data/segdup_mask.bed` (need to confirm, but it's there).
- **Pedigree file** for all 3202 1000?Genomes samples downloaded: stored on Lak at `/home/mrempadmin/xg1_paper_repro/data/20130606_g1k.ped`. Must be uploaded to the EC2 instance.
- **AWS account** viable. We ran `aws sts get-caller-identity` successfully. Region: us?east?1.  
- **Key pair** created: name `xg1-genome-scan-key`, private key saved at `C:\Users\maxre\.ssh\xg1-genome-scan-key.pem`.  
- **My IP** for the security group is `66.75.225.131`.  
- **AMI lookup** was interrupted mid?session (SSM call returned none); we still need a concrete AMI ID for Amazon Linux 2023 x86_64 in us?east?1.
- No EC2 instance launched yet. No security group.

EXACT NEXT STEP (the moment the cold session picks up)
1. **Obtain a concrete AMI ID** for Amazon Linux 2023 (x86_64) in us?east?1 - either via  
   `aws ec2 describe-images --region us-east-1 --owners amazon --filters "Name=name,Values=al2023-ami-2023*x86_64" "Name=state,Values=available" --query 'sort_by(Images, &CreationDate)[-1].ImageId'`  
   or use a known recent ID like `ami-0df8c184d5f6ae664` (but verify).
2. **Create security group** `xg1-genome-scan-sg` allowing inbound SSH (port 22) from `66.75.225.131/32`.  
3. **Launch instance**:  
   - Type: `c5.xlarge` (4 vCPU, 8?GB RAM) or `m5.xlarge` - plenty for streaming VCF processing. Suggest spot request to save money, fallback to on?demand.  
   - AMI: Amazon Linux 2023.  
   - EBS root volume: at least 100?GB gp3 (enough for temporary downloads if needed, though scripts stream).  
   - Key name: `xg1-genome-scan-key`.  
   - Security group: the one just created.  
   - Optionally attach an IAM role that has `s3:GetObject` on the `1000genomes` bucket, or we'll manually copy AWS credentials.
4. Once instance is running, **SSH in** using the `.pem` key.
5. **Upload needed files** (scp from Pine or Lak):
   - `projects/XG1/kenefick/paper_repro/scripts/npa_detector.py`
   - `projects/XG1/kenefick/paper_repro/scripts/genome_scan.py`
   - `projects/XG1/kenefick/paper_repro/data/segdup_mask.bed` (verify filename)
   - `~/xg1_paper_repro/data/20130606_g1k.ped` (from Lak, or the same from the 1000G FTP)
   - Possibly `requirements.txt` (just `pysam` if not pre?installed).
6. **Install dependencies** on the instance:  
   `sudo yum install python3-pip -y && pip3 install pysam`
7. **Configure AWS credentials** so pysam can read `s3://` URIs
