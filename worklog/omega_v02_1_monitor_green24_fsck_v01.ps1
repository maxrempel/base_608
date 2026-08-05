$ErrorActionPreference = 'Stop'
$keyPath = 'C:\Users\maxre\Nextcloud\zSyncMain\ssh\asto_bitwarden_ed25519_20260618.txt'
$workspace = 'C:\Users\maxre\genomics_private\omega_v02_1_blind_production_20260803_v01'
$logPath = Join-Path $workspace 'green24_fsck_monitor_v01.tsv'
$completionPath = Join-Path $workspace 'green24_fsck_completion_service_log_v01.txt'
$markerPath = Join-Path $workspace 'GREEN24_FSCK_MONITOR_COMPLETE_v01.json'
$unit = 'systemd-fsck@dev-disk-by\x2duuid-7B5F\x2dD16C.service'
$sep = [char]9

if ((Test-Path -LiteralPath $logPath) -or (Test-Path -LiteralPath $markerPath)) {
    throw 'Monitor output already exists; refusing to overwrite append-only state.'
}

$header = @('timestamp','pid807_active','pid807_state','pid807_elapsed_s','service_active','service_substate','service_result','service_exit_status','mountpoint_active','device_uuid','device_label','filesystem','device_read_only','io_some_avg10','io_full_avg10','kernel_error_count') -join $sep
Add-Content -LiteralPath $logPath -Value $header

while ($true) {
    $remote = @'
ts=$(date --iso-8601=seconds)
if [ -r /proc/807/stat ]; then
  pid_active=1
  pstate=$(ps -o state= -p 807 | tr -d ' ')
  pelapsed=$(ps -o etimes= -p 807 | tr -d ' ')
else
  pid_active=0
  pstate=absent
  pelapsed=0
fi
unit='systemd-fsck@dev-disk-by\x2duuid-7B5F\x2dD16C.service'
active=$(systemctl show "$unit" -p ActiveState --value 2>/dev/null || echo unknown)
sub=$(systemctl show "$unit" -p SubState --value 2>/dev/null || echo unknown)
result=$(systemctl show "$unit" -p Result --value 2>/dev/null || echo unknown)
estatus=$(systemctl show "$unit" -p ExecMainStatus --value 2>/dev/null || echo unknown)
if mountpoint -q /mnt/green24; then mounted=1; else mounted=0; fi
read uuid label fstype ro <<EOF
$(lsblk -dnro UUID,LABEL,FSTYPE,RO /dev/sda1)
EOF
some=$(awk '/^some/{for(i=1;i<=NF;i++)if($i~/^avg10=/){split($i,a,"=");print a[2]}}' /proc/pressure/io)
full=$(awk '/^full/{for(i=1;i<=NF;i++)if($i~/^avg10=/){split($i,a,"=");print a[2]}}' /proc/pressure/io)
errors=$(journalctl -b -k --no-pager 2>/dev/null | grep -Eic 'I/O error|reset|timeout|media error|nvme.*error|sda.*error|exfat.*error' || true)
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "$pid_active" "$pstate" "$pelapsed" "$active" "$sub" "$result" "$estatus" "$mounted" "$uuid" "$label" "$fstype" "$ro" "$some" "$full" "$errors"
'@
    $encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($remote))
    $line = ssh -o BatchMode=yes -i $keyPath rempel@astolfodebian.tail251d88.ts.net "ssh -o BatchMode=yes -i ~/.ssh/sol_key maxre@192.168.1.142 'echo $encoded | base64 -d | bash'"
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($line -join ''))) {
        Add-Content -LiteralPath $logPath -Value ((Get-Date -Format o) + $sep + 'monitor_transport_error')
        Start-Sleep -Seconds 120
        continue
    }
    $safeLine = ($line -join [Environment]::NewLine).Trim()
    Add-Content -LiteralPath $logPath -Value $safeLine
    $fields = $safeLine -split $sep
    if ($fields.Count -ge 16 -and $fields[1] -eq '0' -and $fields[4] -notin @('active', 'activating')) {
        $logRemote = "journalctl -b --no-pager -u '$unit' -n 120; systemctl --no-pager --full status '$unit' 2>&1 || true"
        $logEncoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($logRemote))
        $serviceLog = ssh -o BatchMode=yes -i $keyPath rempel@astolfodebian.tail251d88.ts.net "ssh -o BatchMode=yes -i ~/.ssh/sol_key maxre@192.168.1.142 'echo $logEncoded | base64 -d | bash'"
        $serviceLog | Set-Content -LiteralPath $completionPath -Encoding utf8
        $marker = [ordered]@{
            schema = 'green24_fsck_monitor_complete_v01'
            recorded_at = (Get-Date -Format o)
            final_status_line = $safeLine
            service_log = [IO.Path]::GetFileName($completionPath)
        }
        $marker | ConvertTo-Json | Set-Content -LiteralPath $markerPath -Encoding utf8
        break
    }
    Start-Sleep -Seconds 120
}
