# Scribe handover - milestone 5 (~383K tokens)
# session: 20260715_wizardly_perlman_b98acf_af0a7d77
# cwd: C:\claude_base\.claude\worktrees\wizardly-perlman-b98acf
# written: 2026-07-15 08:59:57 by deepseek-v4-pro

# HANDOVER - XG1 / Starseed Genetics: Autistic Whole-Genome Trio Access for NPA Replication

---

## GOAL (in Max's own words)

Get access to **whole-genome** autistic short-read sequencing data - complete trios - to replicate his existing 1000 Genomes NPA analysis (point-type de novo single-base variants, and omega-type insertions). ~600 trios needed, comparable to the 1000G high-coverage set he already analyzed.

---

## WHAT HAPPENED & DECISIONS MADE

### 1. The "public data approvals" project was already in Memex + Notion
We never needed to import it - it's all in his existing Notion (Trio Dataset Applications Status, dbGaP notes) and Memex (AnVIL blocker, All of Us rejection, eRA Commons config). Fully readable.

### 2. dbGaP project #42416: we logged in and downloaded the key
- Logged in as `transposonPI` at the dbGaP Authorized Access portal (password from Bitwarden - **no phone MFA was required this time**).
- Project active, renews 2027-01-01.
- Downloaded `prj_42416.ngc` and saved it to `C:\Users\maxre\Nextcloud\zSyncMain\ssh\dbgap_prj_42416_key_20260714.ngc` and copied to Lak.
- The approved datasets are all **General Research Use only**: phs000298 (ASC), phs003647 (ADHD controls), phs000199 (CHOP CNV controls). **No disease-specific-autism (DS-ASD) consent was granted.**

### 3. Pilot download PROVEN on Lak
- Lak (Debian 12, `mrempadmin@100.110.225.89`, 656 GB free) - SRA Toolkit 3.4.1 installed.
- Pilot run SRR7480235 (GRU consent, WXS exome, ~3.1 GB) downloaded and `vdb-validate` reports **"is consistent."**
- DS-ASD run was correctly denied (SRR7480234) - proof the key works, consent tiers enforced properly.

### 4. Pivot: the ASC dataset is WRONG for Max's goal - it's exome-only
Max needs **whole genome**. ASC (phs000298) is **whole-exome** (~2% of genome). Even with full DS-ASD access, it cannot run the omega insertion scan genome-wide. The ADHD and CHOP sets are controls, not autism.

### 5. Decision: SSC (Simons Simplex Collection) over MSSNG
**Recommendation accepted by Max.** Reasoning:
- SSC is whole-genome, Illumina ~30x - same platform as his 1000G trios (apples-to-apples for omega comparison).
- ~1,800 complete families (quads + trios) - far more than the 600 needed.
- **Simplex quads include an unaffected sibling** - built-in matched control.
- **No consent-tier subsetting trap** like dbGaP's GRU/DS-ASD split. The full WGS set is released to all approved researchers.
- Downloadable to own machines, no cloud lock-in.
- MSSNG rejected because mixed sequencing platforms would confound omega insertion detection.

### 6. SFARI Base: logged in, institutional blocker fully mapped
- Logged in as `mrempel@dnaresonance.org` (password from Bitwarden, no captcha).
- SSC confirmed to carry **WGS** data (visible on SFARI Base's SSC card).
- **The blocker:** DRRF (Max's institution) is listed as **"For Profit"** with **no tax ID (EIN)**. Therefore the institution shows as **"unconfirmed"** and the data-use Joinder is **unsigned.**
- This is the **same for-profit flag that stalled the SPARK request** (#188259). Fix it once, unblock both.
- Signing Official on record: **Oksana.**
- The researcher account cannot edit the institution record (403 on the institution page) - it must be done by the Signing Official or via SFARI help desk.

### 7. Plan documented, drafts written - NOT sent
- Full plan file: `C:\claude_base\projects\XG1\ssc_access\SSC_WGS_access_plan_v01_tomemex.md`
- Contains: research-use statement draft, SFARI correction email draft (in Max's voice), step-by-step unblock-and-apply sequence.
- Nothing was submitted, registered, or sent to any external party.

---

## CURRENT STATE

- **Lak:** SRA Toolkit installed, working. One validated GRU exome sitting there. No bulk download running.
- **dbGaP:** Access key for project #42416 is secured. Three GRU-only datasets are approved. ASC is exome-only - useless for Max's goal.
- **SFARI Base:** Account active. Institution (DRRF) is **unconfirmed** due to for-profit flag. Joinder unsigned. SSC WGS is the target - data is there, access is paperwork-blocked.
- **SPARK:** Still stuck on same institutional verification (ticket #188259).
- **Consolidated status page:** [Notion page](https://app.notion.com/p/39d0316f556081d3968ae2e68d1fb677) updated to reflect all findings.

---

## EXACT NEXT STEP

**Get Max to confirm: Is DRRF a registered non-profit, and what is its EIN?**

That single fact is the key. With it:
1. Finalize the SFARI correction email to switch institution type from "For Profit" to "Non-Profit" (attach EIN).
2. Have Oksana (Signing Official) sign the Joinder.
3. Submit the SSC WGS data request.

Without the EIN, we cannot proceed past the institutional verification gate.

---

## OPEN QUESTIONS AWAITING MAX

1. **Is DRRF a registered non-profit? What's the EIN?** (If DRRF is not actually a non-profit, the approach changes - SFARI may charge fees for for-profit access, and the Joinder terms differ.)
2. **Which IRB/exemption covers this project?** Max said "yes" to having an IRB, but the specific IRB approval or exemption determination document hasn't been identified yet. Needed for the SSC application.
3. **Who emails SFARI?** Max, Oksana, or Claude-drafted email from Max's account? The draft is ready but needs a sender decision.

---

## KEY PATHS & IDs

| Item | Value |
|---|---|
| **Consolidated Notion page** | https://app.notion.com/p/39d0316f556081d3968ae2e68d1fb677 |
| **SSC access plan** | `C:\claude_base\projects\XG1\ssc_access\SSC_WGS_access_plan_v01_tomemex.md` |
| **dbGaP key (local)** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\dbgap_prj_42416_key_20260714.ngc` |
| **dbGaP key (Lak)** | `~/genomics/dbgap/keys/prj_42416.ngc` |
| **dbGaP project** | #42416, PI Max Myakishev-Rempel, org TRANSPOSON, renews 2027-01-01 |
| **SRA Toolkit on Lak** | `~/genomics/dbgap/tools/sratoolkit.3.4.1-*/bin/` |
| **Lak SSH** | `ssh -i ~/.ssh/lakarian_key.pem mrempadmin@100.110.225.89` |
| **SFARI Base account** | `mrempel@dnaresonance.org` (also `max@dnaresonance.org` exists, same password) |
| **SFARI institution** | DRRF, UUID `fa9f3370-3d2b-4583-9313-48c11f1b6350`, Signing Official: Oksana |
| **SPARK ticket** | #188259 (same for-profit flag) |
| **Bitwarden session** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt` |
| **Login.gov** | `max.rempel2@gmail.com` (TOTP in Bitwarden - works fully autonomously) |
| **eRA Commons / NIH Login** | `transposonPI` (no TOTP seed in Bitwarden - needs phone push for MFA) |
| **IRB** | Confirmed exists, but specific doc not yet identified |

---

## GOTCHAS & RULED-OUT DEAD ENDS

- **SRA Toolkit on Lak needs `--ngc` flag and the key file path explicitly set.** Pilot command worked: `prefetch --ngc keys/prj_42416.ngc SRR7480235`. Without the flag, dbGaP consent check fails silently.

- **Login.gov?eRA Commons route throws 403.** The NIH federation gateway blocks it. The working login path is: go directly to `https://dbgap.ncbi.nlm.nih.gov/aa/wga.cgi?page=login&login=NFL` and use the transposonPI username/password.

- **Login.gov?NCBI account link creates a NEW (wrong) NCBI account.** The page warns: don't continue if you already have an account. We correctly stopped there. Max's dbGaP access is tied to his eRA identity, not a standalone NCBI account.

- **Do NOT create a new NCBI account or register anything.** Max explicitly said: "don't finalize any letters or registrations."

- **phs000298 is exome-only, not whole-genome.** The 12,775 SRA records are all WXS. Even with full consent access, this dataset cannot satisfy Max's whole-genome requirement.

- **phs000298 consent split is real and enforced.** ~98% of runs are DS-ASD (denied), ~2% are GRU (granted). The pilot error was dbGaP speaking directly: "request permission for phs000298 / DS-ASD."

- **PCGC pediatric-cardiac trios (WGS) were rejected twice by NHLBI.** Not an option.

- **SFARI institution record is NOT editable by the researcher account.** Only the Signing Official or SFARI help desk can change the institution type. We got a 403 confirming this.

- **MSSNG ruled out** because its mixed sequencing platforms (not uniform Illumina) would confound omega insertion detection.

- **SPARK is still blocked on the same DRRF for-profit flag as SSC.** Fixing the institution once unblocks both.
