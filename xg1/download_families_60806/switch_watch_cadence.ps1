$ErrorActionPreference = 'Continue'
$taskCmd = 'powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\base_608\xg1\download_families_60806\watch_downloads.ps1"'

schtasks /Delete /TN "Q38DownloadWatch" /F 2>$null
& schtasks @('/Create', '/TN', 'Q38DownloadWatch', '/TR', $taskCmd, '/SC', 'MINUTE', '/MO', '45', '/F')
schtasks /Delete /TN "Q38DownloadWatchCadence45" /F 2>$null

"watch cadence switched to 45 minutes at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')" | Out-File -FilePath 'C:\base_608\xg1\download_families_60806\watch.log' -Append -Encoding utf8
