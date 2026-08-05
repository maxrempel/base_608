# Scribe handover - milestone 1 (~118K tokens)
# session: 20260714_musing_swirles_ceb1a9_49d4d856
# cwd: C:\claude_base\.claude\worktrees\musing-swirles-ceb1a9
# written: 2026-07-14 08:55:45 by deepseek-v4-pro

# HANDOVER - Tamza Registration Inquiry

---

## GOAL (in Max's words)
"Create a folder for Tamsa registration, it will be company registrations. I think should be a separate folder. Maybe it already exists. And start gathering information about what do we need to do with Tamsa registration. It's a sophisticated pattern."

---

## DECISIONS MADE + WHY

1. **Searched for "Company Registrations" folder before creating anything** - wanted to avoid duplication. Used ES (Everything Search CLI) and direct filesystem listing.

2. **Confirmed the folder already exists** - `G:\My Drive\00Main2026\10 Companies - registrations main2025\00 Tamza Nonprofit registrations\` - so no new folder needed.

3. **Read the existing SAM.gov renewal method document** (`sam_gov_entity_renewal_method_v01_tomemex.md`) to understand whether Tamza was a SAM registration. It wasn't - the document applies to Stichting Tomemex (a different entity), not Tamza. This ruled out a dead end.

4. **Identified Tamza as a registered California 501(c)(3) nonprofit** with incorporation in Sept 2022, IRS determination in Nov 2022. The "sophisticated pattern" refers to the multi-agency recurring compliance calendar for CA nonprofits.

5. **Flagged a gap** - the paper trail stops at 2023 filings. Nothing on file for 2024, 2025, or 2026.

---

## CURRENT STATE

- **Folder found** (no creation needed):
  - `G:\My Drive\00Main2026\10 Companies - registrations main2025\00 Tamza Nonprofit registrations\`
  - Contains 4 subfolders: `00 Registration receipts`, `01 Profile info`, `02 Annual taxes/reg`, `03 Banking`
  - A master tracker sheet `Registrations - when to file current 2025j` lives in the parent `10 Companies - registrations main2025\` folder.

- **Tamza entity details on file:**
  - Name: Tamza (California 501(c)(3) public-benefit nonprofit)
  - CA Secretary of State registration #5232561 (Sept 2022)
  - EIN: 92-0733765
  - IRS 1023-EZ filed Oct 2022; 501(c)(3) granted Nov 2022
  - Statement of Information filed (date unclear from transcripts)
  - IRS 990-PF and CA FTB 199N e-postcard filed for 2023

- **What was ruled out:**
  - SAM.gov renewal (the existing SAM folder/doc applies to Stichting Tomemex, not Tamza)
  - Need to create a new folder (it already exists)

- **Four compliance agencies identified for CA nonprofits:**
  1. **IRS** - Form 990 series annually
  2. **CA FTB** - Form 199 / 199N e-postcard annually
  3. **CA Secretary of State** - Statement of Information (SI-100) every 2 years
  4. **CA Attorney General** - RRF-1 charity renewal annually

- **Burning question raised:** No filings are documented for 2024, 2025, or 2026. Are they overdue?

---

## EXACT NEXT STEP

The session ended asking Max whether he wants the assistant to:
1. Dig into the master tracker sheet (`Registrations - when to file current 2025j`) to determine exactly what's overdue for Tamza right now.
2. Or confirm whether he meant something else entirely by "Tamza registration" (e.g., a brand-new registration for a different entity or jurisdiction).

**Next action:** Wait for Max's response to that question before proceeding further.

---

## OPEN QUESTIONS (awaiting Max)

1. **Are we checking for lapsed 2024-2026 filings for the existing Tamza nonprofit?** Or is this a new/different registration?
2. **Does Max want a full compliance gap analysis** drawn from the master tracker?

---

## KEY PATHS & IDS

| What | Path / Value |
|------|-------------|
| Company Registrations folder | `G:\My Drive\00Main2026\10 Companies - registrations main2025\` |
| Tamza subfolder | `G:\My Drive\00Main2026\10 Companies - registrations main2025\00 Tamza Nonprofit registrations\` |
| Master tracker | `G:\My Drive\00Main2026\10 Companies - registrations main2025\Registrations - when to file current 2025j` (sheet) |
| SAM renewal doc (NOT about Tamza) | `C:\claude_base\tools\sam_gov_renewal\sam_gov_entity_renewal_method_v01_tomemex.md` |
| ES search tool | `C:\claude_base\tools\es\es.exe` |
| Tamza CA Entity # | 5232561 |
| Tamza EIN | 92-0733765 |
| Everything (voidtools) binary | `C:/Program Files/Everything/Everything.exe` |
| Working directory | `C:\claude_base\.claude\worktrees\musing-swirles-ceb1a9` |

---

## GOTCHAS & DEAD ENDS

1. **SAM.gov is a red herring for Tamza.** The SAM renewal documentation in `tools/sam_gov_renewal/` applies only to Stichting Tomemex (a Dutch foundation doing US federal contracting). Tamza is a CA nonprofit with no SAM registration in evidence. Do not conflate them.

2. **ES (Everything Search) indexing issue.** The ES CLI tool initially returned no results because the Everything daemon wasn't running. Required starting `Everything.exe -startup` and waiting for indexing before `es.exe` queries would return hits on the G: drive. If ES is silent in future sessions, check whether the Everything service is running.

3. **Folder naming convention.** The parent folder uses a leading number (`10 Companies - registrations main2025`) and the Tamza subfolder uses `00` prefix. This is a deliberate sorting scheme in the Google Drive folder structure. Don't rename or reorder.

4. **No 2024+ filings on file.** The documented history stops at 2023. This is either because filings weren't done, weren't saved to this folder, or were handled elsewhere. The master tracker is the quickest way to resolve this - it should have a per-entity schedule.
