# Scribe handover - milestone 3 (~236K tokens)
# session: 20260714_wizardly_perlman_b98acf_af0a7d77
# cwd: C:\claude_base\.claude\worktrees\wizardly-perlman-b98acf
# written: 2026-07-14 16:38:59 by deepseek-v4-pro

## GOAL (in Max's words)
Get unstuck - figure out how to actually download the approved autistic short?read sequencing datasets (long?read would be even better, but short is fine). The focus is on the public?data approvals for XG1 / Starseed Genetics. Max wants to prioritize and actually start getting data, not just re?approve permissions.

## DECISIONS MADE + WHY

- **No new accounts or registrations** - Max said "don't finalize any letters or registrations." The session avoided creating anything (e.g., `Login.gov`?`new NCBI account` was intentionally skipped because it would be a fresh, unlinked identity). Only existing, pre?approved resources were touched.

- **Source of truth is Memex + Notion** - The "public data approvals" project lives across both; after searches, the key pages were read fully. All findings are now consolidated into a single Notion status page so a cold session can pick up immediately.

- **Autism Sequencing Consortium (ASC) is already approved** - dbGaP project #42416 (PI: max.rempel, org TRANSPOSON) has access to `phs000298` (ASC WES, ~5300 trios) granted 13 Mar 2026. The block was never permission - it was download mechanics.

- **Download path is classic SRA Toolkit, not AnVIL** - In March the team got stuck chasing an AnVIL portal that doesn't hold the data. The session confirmed that `phs000298` has 12,775 SRA runs in NCBI's controlled?access repository. This means it can be downloaded with the standard `prefetch`/`fastq-dump` tools using a dbGaP repository key file (`.ngc`). That path was never attempted.

- **One login remains manual** - The session successfully drove Login.gov (using Bitwarden for email/password/TOTP), but dbGaP/eRA Commons requires the `eRA authenticator` (a push/code to Max's phone) that has no seed in Bitwarden. Attempts to route Login.gov ? eRA returned a 403 error (same wall as March). So the final download?portal login cannot be automated yet; it needs Max's phone for exactly one step.

- **Autonomous everything else** - Passwords and TOTPs for Login.gov, Bitwarden session file located, Notion status page created, worklog updated, browser correctly closed.

## CURRENT STATE

- **Approvals in hand**  
  - `phs000298` (autism exomes) - approved  
  - `phs003647` (ADHD controls) - approved  
  - `phs000199` (CHOP CNV) - approved  
  - All of Us - rejected  
- **No download attempted yet** - No `.ngc` key file, no SRA cart, no local data.
- **Automated login blocked** - dbGaP portal requires Max to log in with his eRA Commons credentials + phone authenticator.
- **One consolidated status page** exists in Notion at `https://app.notion.com/p/39d0316f556081d3968ae2e68d1fb677` with the full board and the unstuck plan.
- **Worklog has been written** - a checkpoint of the breakthrough using the compaction_kb script.

## EXACT NEXT STEP
Max needs to **log into the dbGaP Authorized Access portal once** on his regular browser (with his phone nearby for the eRA authenticator push). After that login, the session can take over:  
1. From the authorised?access page, obtain the **project repository key** (`.ngc` file).  
2. Build the download list for `phs000298` (and optionally `phs003647`).  
3. Run `prefetch` + `fastq-dump` on a compute box, resumable and throttled.  

Once the key file is in the session's filesystem, everything else is scriptable without further interaction.

## OPEN QUESTIONS AWAITING MAX
- **When** does he want to do that one login? ("See you later" was stated; next session likely starts after he logs in or gives the go?ahead.)
- **Preference for automation** - after this initial download, does he want the eRA authenticator seed added to Bitwarden so future dbGaP logins can be fully autonomous? (That would require capturing the TOTP secret during a login.)
- **Data destination** - where should the downloaded FASTQs land? (Local attached storage, a NAS, a cloud bucket, etc. - not specified yet.)

## KEY PATHS / IDs
- **dbGaP project**: `#42416` (PI: `transposonPI`; Signing Official: `transposonSO`; AA: `transposonAA`)
- **Target dataset**: `phs000298.v4.p3` (Autism Sequencing Consortium WES)
- **SRA runs found**: 12,775 (controlled-access, `dbGaP`)
- **Additional datasets** (quick wins): `phs003647`, `phs000199`
- **Login.gov** account: `max.rempel2@gmail.com`, TOTP seed in Bitwarden item `"login.gov Sam.gov 51119"`
- **eRA Commons** username: `transposonPI`, password in Bitwarden, but **no TOTP seed** stored
- **Bitwarden session file**: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt` (unlocked; used to self?serve TOTP for Login.gov)
- **Notion status page**: `https://app.notion.com/p/39d0316f556081d3968ae2e68d1fb677`
- **No existing `.ngc` key file**: path searched, nothing found
- **Terra account** (not needed): `dna@dnaresonance.org`

## GOTCHAS & DEAD ENDS
- **Do NOT create a new NCBI account**. The `Login.gov` ? `NCBI` flow leads to a "finish creating a new NCBI account" screen; that identity would not carry the dbGaP project approval. The session correctly stopped there.
- **AnVIL is a dead end for ASC**. The "AnVIL_Autism_HighSeq_GRU" workspace listed in the approval email does not actually host the sequencing files. Do not repeat the March pain.
- **eRA Commons Login.gov linkage returns 403**. The federation gateway blocks automated browser attempts. The only working path is the eRA Commons direct login with phone authenticator.
- **No local download artifacts from March exist**. A search for `.ngc`, cart files, and project keys returned nothing - the previous work never left the AnVIL loop.
- **Worklog script is in use** at `C:/claude_base/compaction_kb/scripts/worklog.py`. A cold session should run it to see the latest logged checkpoint and continue from there.

**Handover ready.** A cold session, given this note plus the ability to read the Notion status page, can immediately act once Max provides the `.ngc` key file or performs the one login himself.
