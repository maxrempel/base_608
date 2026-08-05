# Scribe handover - milestone 5 (~376K tokens)
# session: 20260718_claude_base_ab9bf426
# cwd: C:\claude_base
# written: 2026-07-18 14:13:53 by deepseek-v4-pro

# HANDOVER - X31Bt (Oliver WGS Point-Mutation NPA)

## GOAL (Max's words)

"Get the list of NPAs from Oliver, but they should be like real NPAs, properly filtered." Max was frustrated that previous sessions had only done large-insertion NPA analysis on Oliver's WGS data, not point mutations. He wanted a genome-wide SNV-level NPA scan with population-frequency filtering, comparable to the array-based Bowater family analysis. He also wanted the work moved to the new compute box Taygeta instead of the guest box asto.

Separate earlier thread (COMPLETE before this): download the Bowater family 23andMe trio (Lottie, Julie, Roger), run array-based NPA scan, cross-family/proximity/permutation/gene-annotation, email Lottie.

## DECISIONS + WHY

1. **Kept analysis on asto for the local gnomAD resource.** Initially tried running gnomAD lookups remotely from Taygeta (tabix over HTTPS to gnomAD v4.1). The chr22 pilot was pathologically slow (~150ms per TLS handshake for sparse queries). Discovered asto already had a local `af-only-gnomad.hg38.vcf.gz` (3GB, tabix-indexed) - local tabix finished all 149k positions in 15 seconds. Used asto for the compute-heavy part, then shipped small result files to Taygeta.

2. **Tiled/v02 approach abandoned.** Wrote `annotate_gnomad_maf_v02.py` (tiled, one query per 1Mb window instead of per-candidate) but it was still latency-bound and downloading unnecessary data. Killed it once the local resource was found.

3. **Two-pass population filter: local af-only first, full gnomAD v4.1 second.** The local `af-only-gnomad` is the smaller gnomAD-v2-based resource - "novel" there overcounts. So: local pre-filter (149,387 ? 7,511), dbSNP filter drops known inherited variants (7,511 ? 613), QC (het-only + segdup-mask + decluster) (613 ? 574), then accurate re-check of just the 574 against full gnomAD v4.1 (572 remain novel).

4. **Used the prior session's QC scripts where possible.** Found `novelty_filter_v01.py`, vendor dbSNP-annotated VCFs, and segdup mask already on asto from the earlier insertion work. Reused the segdup mask and dbSNP annotation. Wrote only the population-MAF filter (the missing piece), not a whole new pipeline.

5. **Provisioned Taygeta with Kenefick BAMs over LAN.** Copied both Oliver (61GB) and Kristen (35GB) .mq.bam files from Centauri teal16 to Taygeta green24 over the local network. Verified intact with samtools quickcheck. Indices came along. Now Taygeta is self-sufficient and future runs stay off Liz's guest box.

6. **Full 574 read-level QC (not just spot-check).** Max's hard rule: look at the actual reads. Initial spot-check of 15 showed 13/15 textbook-clean. Then ran all 574 through pileup QC. First launch crashed silently (wrong Python env, no pysam). Fixed and re-ran: **507/574 (88%) read-level clean**, ~12% flagged (mostly minor low-VAF/homopolymer; 9 show maternal alt reads = inherited).

7. **Classification: 0 confirmable maternal de-novo.** Every traceable candidate (phaseable-maternal) turned out to be dbSNP-known = mis-phased inherited. 49 paternal, 0 maternal. The survivor set (574 pre-v4.1, 572 post-v4.1) is dominated by UNPHASEABLE (435) - the short-read wall.

## CURRENT STATE

**DONE and DELIVERED:**
- Oliver genome-wide point-mutation NPA scan complete: 149,387 not-from-mother SNVs ? population-MAF + dbSNP + QC filter ? 572 novel candidates ? **0 confirmable maternal de-novo SNVs**
- Full read-level QC on all 574 survivors: 88% clean, 0 confirmable de-novo
- Report + all outputs in Nextcloud: `xg1_data/xp2_analysis/260716_NPA_Oliver_WGS_pointmut/`
- Scripts committed and pushed (10 named files in `projects/XG1/xp2_npa/`)
- Reusable HOWTO written: `HOWTO_process_wgs_npa_sample_v01_tomemex.md`
- Taygeta provisioned with verified Kenefick BAMs on green24
- Result shared to P5 and P2 rooms
- Earlier Bowater array work also complete (separate folder: `260713_NPA_Bowater_23andme_trio/`)

**IN FLIGHT:** Nothing. Task is complete. Session has been parking autonomously for ~2 days with periodic wake checks - no new instructions from Max.

**HONEST CEILING:** A mother-son duo cannot confirm a point-mutation NPA without the father's genome. The 572 survivors are real heterozygous variants genuinely absent from the mother - but they're rare private alleles inherited from the unsequenced father, not de-novo mutations. This independently confirms the earlier insertion-work finding via a cleaner population-frequency method.

## EXACT NEXT STEP

None - task is complete. When Max returns, the live conclusion to present is:

**"Oliver cannot yield a confirmed point-mutation NPA without sequencing the father."**

If Max wants to advance the XG1 NPA research with zero funding, the move is: take the existing Bowater array candidates (CAPN14, MAF, CTNNA3) as documented targets, and either sequence the Bowater trio (but Max has no funding) or find another complete trio already sequenced.

## OPEN QUESTIONS

None outstanding - all deliverables shipped, all boards updated, no DM replies pending.

## KEY PATHS/IDs

**Nextcloud (backed up, Memex-indexed):**
- Bowater trio data: `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`
- Bowater array NPA analysis: `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\`
- Oliver WGS point-mutation NPA: `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260716_NPA_Oliver_WGS_pointmut\`
  - `REPORT_oliver_wgs_pointmut_NPA_v01_tomemex.md` (main report, has full QC numbers)
  - `outputs/oliver_filtered_npa_final_v01.tsv` (574 rows, annotated)
  - `outputs/allpileup.txt` (FLAGS tally for all 574)
  - `outputs/oliver_npa_summary_v01.txt`
  - `outputs/oliver_npa_tier_by_verdict_v01.tsv`

**Git repo (committed + pushed):**
- `C:\claude_base\projects\XG1\xp2_npa\` - 10 scripts + HOWTO
  - `annotate_local_afonly_v01.py` (the MAF filter - the missing piece)
  - `classify_oliver_npa_v01.py` (tier classification)
  - `gnomad_v41_check.py` (v4.1 re-check)
  - `pileup_spotcheck.py` (read-level QC)
  - `build_final.py` (final table + gene annotation)
  - `run_funnel.sh` (the full funnel pipeline)
  - `HOWTO_process_wgs_npa_sample_v01_tomemex.md` (reusable methodology)
  - Plus: Bowater scanner + cross-family + proximity + annotation scripts

**Compute boxes:**
- **Taygeta** (192.168.1.142, key `~/.ssh/sol_key`, user `maxre`): 24 cores, 16GB GPU, green24 has 22TB free. Now has both Kenefick BAMs at `/mnt/green24/kenefick/oliver/oliver.mq.bam` and `/mnt/green24/kenefick/kristen/kristen.bwa.mq.bam` (verified intact, indexed). Can SSH to Centauri via its own ed25519 key.
- **asto** (astolfodebian.tail251d88.ts.net, key `~/.ssh/bitwarden_ed25519`, user `rempel`): The WGS pipeline ran here. Has local `af-only-gnomad.hg38.vcf.gz`, vendor VCFs, segdup mask, reference GRCh38.fa. The `gw_maternal_snv` scan output is at `/home/rempel/genomics/omega_run/out/genome_oliver/gw_maternal_snv/` (chunked).
- **Centauri teal16** (192.168.1.176): Original Kenefick BAM backup on D:/genomics/kenefick/.

**bcast rooms:**
- P5: Bowater/array comparison room (shared with X31Bd/X12B)
- P2: NPA 1000G reference distribution lane

**23andMe login:** `max@tamza.com` / password in `shared_logins_frequent.txt`. 2FA via `bw get totp 7772765a-6e05-44ab-9955-b3fa0142a736 --session $BW_SESSION`. All Bowater kits under this account.

## GOTCHAS

1. **No father sequenced = Oliver is a duo, not a trio.** A true point-mutation NPA ("neither parent has this allele") cannot be confirmed without the father's genome. The population-MAF filter is the rescue, but it only identifies candidates - it cannot confirm them as new mutations. This is a genuine wall, not a broken pipeline.

2. **gnomAD remote tabix is latency-bound, not bandwidth-bound.** The v4.1 remote lookup via HTTPS was ~150ms per query (TLS handshake). Per-candidate: ~45 min for chr22. Per-window (v02): better but still slow. **Use the local `af-only-gnomad.hg38.vcf.gz` on asto** for pre-filtering - it's 3GB, tabix-indexed, instant. Then v4.1 re-check only the small survivor set.

3. **The local `af-only-gnomad` is gnomAD-v2-based.** "Novel" there overcounts (misses variants known in fuller databases). Always follow with a full gnomAD v4.1 re-check on survivors.

4. **pysam needs the conda environment.** System `python3` on asto doesn't have pysam. The correct path is `/home/rempel/miniconda3/envs/xtea/bin/python3`. The first full-574 pileup launch crashed silently because `$XPY` variable didn't survive into the `setsid` shell.

5. **`pkill -f annotate_gnomad_maf` kills its own parent.** The pattern matched the SSH command line itself. Use bracket-escaping: `pkill -f 'annotate_gnomad_maf_v0[1]'`.

6. **Taygeta SSH can throttle.** Rapid repeated connections from Pine to Taygeta (192.168.1.142) sometimes return 255. It's transient - wait 10-20 seconds and retry.

7. **The Bowater canonical folder is on Nextcloud (survives disk cleaning).** If it appears missing, check `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` - it's synced and backed up.

8. **NPA scanner was a re-implementation.** The original `L473v1_...NPA_Scanner` script was ephemeral (January session, not saved to disk). The re-implementation is `npa_scanner_bowater23_v01.py` - it's faithful but should be flagged as such in any report. The clone (X31B/X31Bd) added this caveat to the report.

9. **Bitwarden CLI for 2FA solves the browser-extension contention.** Only one session can hold the logged-in Bitwarden browser profile. For 23andMe login, use `bw get totp` from the command line - no browser needed. Session token is in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt`.
