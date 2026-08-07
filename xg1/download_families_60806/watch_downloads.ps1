$ErrorActionPreference = 'Continue'

$base      = 'C:\base_608\xg1\download_families_60806'
$stateFile = Join-Path $base 'watch_state.json'
$alerts    = Join-Path $base 'watch_alerts.log'
$stamp     = Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'

$remote = @'
cat /mnt/green24/1kgp_longread_trios/state/PROGRESS.md 2>/dev/null
echo "---SEP---"
systemctl --user list-units 'kgp-assembly-dl-v01@*' --no-legend --plain 2>/dev/null | awk '{print $1, $3}'
echo "---SEP---"
python3 - <<'PY'
import json, os, glob
d = '/mnt/green24/1kgp_longread_trios/state'
for p in sorted(glob.glob(os.path.join(d, '*.json'))):
    try:
        st = json.load(open(p))
    except Exception:
        continue
    bad = [f['status'] for f in st['files'] if f.get('status') in ('verify_failed', 'failed')]
    if st['status'] == 'failed' or bad:
        print(st['family'], st['status'], ','.join(bad))
PY
echo "---SEP---"
df -h /mnt/green24 2>/dev/null | tail -1
'@ -replace "`r", ""

$b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($remote))
$cmd = "echo $b64 | base64 -d | bash"

$out = $null
try {
    $out = ssh -i C:\Users\maxre\.ssh\bitwarden_ed25519 -o ConnectTimeout=20 -o BatchMode=yes `
        rempel@astolfodebian.tail251d88.ts.net `
        "ssh -i /home/rempel/.ssh/sol_key -o ConnectTimeout=20 -o BatchMode=yes maxre@192.168.1.142 '$cmd'" 2>$null
} catch {
    $out = $null
}

if (-not $out) {
    "watch failed at $stamp (ssh returned no data)" | Out-File -FilePath $alerts -Append
    exit 1
}

$sections = @()
$current = @()
foreach ($line in $out) {
    if ($line -eq '---SEP---') { $sections += ,@($current); $current = @(); continue }
    $current += $line
}
$sections += ,@($current)

$progress  = ($sections[0] -join "`n")
$services  = ($sections[1] -join "`n")
$anomalies = ((@($sections[2]) | Where-Object { $_ -match '\S' }) -join "`n").Trim()
$disk      = ($sections[3] -join ' ').Trim()

$completeFams = @()
$familyStatus = @{}
$familyBytes  = @{}
foreach ($line in ($progress -split "`n")) {
    if ($line -match '^\| (\S+) \| [^|]+ \| (\S+) \| \d+/\d+ \| ([0-9,]+) \|') {
        $fam = $Matches[1]
        $familyStatus[$fam] = $Matches[2]
        $familyBytes[$fam]  = $Matches[3] -replace ',', ''
        if ($Matches[2] -eq 'complete') { $completeFams += $fam }
    }
}

$prev = @{}
if (Test-Path $stateFile) {
    try { $prev = Get-Content -Raw $stateFile | ConvertFrom-Json } catch { $prev = @{} }
}

$events = @()

if ($anomalies) {
    $prevAn = if ($prev.anomalies) { [string]$prev.anomalies } else { '' }
    if ($prevAn -ne $anomalies) {
        $events += "ANOMALY: $anomalies"
    }
} elseif ($prev.anomalies) {
    $events += "ANOMALIES CLEARED"
}

$prevComplete = @()
if ($prev.completed) { $prevComplete = @($prev.completed) }
$newComplete = @($completeFams | Where-Object { $prevComplete -notcontains $_ })
if ($newComplete.Count -gt 0) {
    $events += "COMPLETED: $($newComplete -join ', ')"
}

$stallCount = @{}
if ($prev.stall_count) { foreach ($p in $prev.stall_count.PSObject.Properties) { $stallCount[$p.Name] = [int]$p.Value } }
foreach ($fam in @($familyStatus.Keys)) {
    if ($familyStatus[$fam] -ne 'downloading') { $stallCount[$fam] = 0; continue }
    $prevSt = if ($prev.family_status.$fam) { [string]$prev.family_status.$fam } else { '' }
    $prevBy = if ($prev.family_bytes.$fam) { [string]$prev.family_bytes.$fam } else { '' }
    if ($prevSt -eq 'downloading' -and $prevBy -eq [string]$familyBytes[$fam]) {
        $stallCount[$fam] = ([int]$stallCount[$fam]) + 1
        if ($stallCount[$fam] -ge 2) {
            $events += "STALLED: $fam unchanged for at least 2 watch cycles"
            $stallCount[$fam] = 0
        }
    } else {
        $stallCount[$fam] = 0
    }
}

$state = [ordered]@{
    last_run      = $stamp
    disk          = $disk
    completed     = $completeFams
    anomalies     = $anomalies
    services      = $services
    family_status = $familyStatus
    family_bytes  = $familyBytes
    stall_count   = $stallCount
}
[System.IO.File]::WriteAllText($stateFile, ($state | ConvertTo-Json -Depth 4), (New-Object System.Text.UTF8Encoding($false)))

if ($events.Count -gt 0) {
    foreach ($e in $events) {
        "$stamp $e" | Out-File -FilePath $alerts -Append -Encoding utf8
    }
    & (Join-Path $base 'refresh_report.ps1') | Out-Null
}

"watch ok at $stamp (completed=$($completeFams.Count), anomalies=$([bool]$anomalies))" | Out-File -FilePath (Join-Path $base 'watch.log') -Append -Encoding utf8
