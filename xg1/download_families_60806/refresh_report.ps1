$ErrorActionPreference = 'Continue'

$report = 'C:\base_608\xg1\download_families_60806\REPORT.md'
$log    = 'C:\base_608\xg1\download_families_60806\report_refresh.log'
$stamp  = Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'

$remote = @'
cat /mnt/green24/1kgp_longread_trios/state/PROGRESS.md 2>/dev/null
echo "---SEP---"
tail -4 /home/maxre/remote_md5_check_20260806.log 2>/dev/null
echo "---SEP---"
df -h /mnt/green24 2>/dev/null | tail -1
'@ -replace "`r", ""

$b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($remote))
$cmd = "echo $b64 | base64 -d | bash"

$out = $null
try {
    $out = ssh -i C:\Users\maxre\.ssh\bitwarden_ed25519 -o ConnectTimeout=15 -o BatchMode=yes `
        rempel@astolfodebian.tail251d88.ts.net `
        "ssh -i /home/rempel/.ssh/sol_key -o ConnectTimeout=15 -o BatchMode=yes maxre@192.168.1.142 '$cmd'" 2>$null
} catch {
    $out = $null
}

$sep = @($out | Where-Object { $_ -eq '---SEP---' }).Count
if (-not $out -or $sep -lt 2) {
    "refresh failed at $stamp (ssh returned no usable data)" | Out-File -FilePath $log -Append
    exit 1
}

$sections = @()
$current = @()
foreach ($line in $out) {
    if ($line -eq '---SEP---') { $sections += ,@($current); $current = @(); continue }
    $current += $line
}
$sections += ,@($current)

$progress = ($sections[0] -join "`n")
$md5tail  = ($sections[1] -join " | ")
$disk     = ($sections[2] -join ' ').Trim()

$progressTable = $progress -replace '(?m)^#.*$', ''
$progressTable = $progressTable.Trim()

$content = @"
# Q38 Long-Read Trio Download - Live Report

Last refreshed: $stamp (auto-updates every 3 hours)

## TLDR

- Census total: **33 unique open-access complete families, 36 trios** (v03, saturated 2026-08-06).
- Download plan covers all 33: **assemblies first** (19 families have assemblies for all members; 1 partial), reads later for the rest.
- Assembly payload: **~250-300 GB**. Optional Vienna reads add ~162 GB.
- Original 13 trios: **1-7 assemblies COMPLETE**, **8-13 (Vienna reads) queued after the assembly phase (~1 day)**.
- Green24 free space: $disk

## Progress (live from Green24 state)

$progressTable

Checksum-repair job (families 1-2, EBI ground truth): $md5tail

## Planned download table (all 33 families)

| Group | Families / trios | Members | Files to download | Est. size | Sequencing platform | Cultured? | Status |
|---|---|---|---|---|---|---|---|
| HGSVC3 (F01-F03) | 3 trios | 3 each (9) | Verkko phased assembly FASTA, 2 haplotypes per member (.gz) | ~4.4 GB per family | PacBio HiFi + ONT + Strand-seq | Yes (EBV LCL) | COMPLETE (3/3) |
| LRSC / 1KGP-ONT (F04-F07) | 4 trios | 3 each (12) | Phased assembly FASTA, 2 haplotypes per member (hapdup / hifiasm) | ~17.7 GB per family | Oxford Nanopore (R9/R10) | Yes (Coriell LCL) | COMPLETE |
| Vienna (F08-F13) | 6 trios | 3 each (18) | Reads only: hg38 CRAM + .crai + GAF per member | ~23-33 GB per family (~162 GB total) | ONT ~17x | Yes (LCL) | queued after assemblies |
| Platinum Pedigree (F18-F32 + F08/F09 overlap) | 15 new units / 17 trios | 23 open | Near-T2T Verkko FASTAs (11 members) + hifiasm diploid FASTAs (12 members), 2 haplotypes each | 120.5 GB | HiFi/Illumina from blood + UL-ONT/Strand-seq from LCL | Partial (blood + LCL) | not started |
| PAN027 / WashU (F17) | 1 trio + 1 extra | 4 | v1.3.1 polished FASTAs, 2 haplotypes each | 24.6 GB | HiFi from blood + ONT/Omni-C from LCL | Partial (blood + LCL) | not started |
| T2T-CQ Chinese Quartet (F16) | 2 trios (MZ twin daughters) | 4 | Twins' combined T2T diploid genome: 2 haplotypes via GWH; parents' v2.0 assemblies to verify | Unknown (GWH) | ONT ultralong + PacBio HiFi | Yes (LCL) | not started |
| Arab Pangenome trio (F33) | 1 trio | 3 | Phased assemblies, 2 haplotypes each (GenBank / mbru.ac.ae) | Est. ~18 GB (exact to resolve) | PacBio HiFi + ONT + Hi-C | **No - blood, first fully non-cultured** | not started |
| GIAB Ashkenazi (F14) | 1 trio (partial) | 3 | HG002 T2T assembly (child); HG003/HG004 reads later | TBD | HiFi + ONT | Yes (LCL) | not started |
| GIAB Chinese (F15) | 1 trio | 3 | Reads only | Deferred | HiFi + ONT | Yes (LCL) | deferred |

## When we will have 13

- **1-7 (all assemblies): COMPLETE.** 8-13 (Vienna reads) can start once the current assembly queue (Platinum + PAN027 extensions) finishes or if started in parallel.
- **8-13 (Vienna reads, ~162 GB): within about a day** if Vienna runs right after 1-7.

## Bandwidth policy (Max, 2026-08-06)

- Home line measured 500 Mbps. Caps: daytime (07:00-23:00) total 250 Mbps, nighttime total 350 Mbps, split across two concurrent family streams. If the source server is slower, no extra limiting is applied.

## Machine / storage facts

- Taygeta 1 live; Green24 at /mnt/green24. Taygeta 2 arrives 2026-08-07 night; 3 days for migration. All data/state on Green24; software committed to GitHub as backup.
"@

[System.IO.File]::WriteAllText($report, $content, (New-Object System.Text.UTF8Encoding($false)))
"refresh ok at $stamp" | Out-File -FilePath $log -Append
