param(
    [int]$IntervalMinutes = 5
)

$ErrorActionPreference = "Stop"

$taskName = "CodexThreadLabelWatcher"
$homeDir = [Environment]::GetFolderPath("UserProfile")
$script = Join-Path $PSScriptRoot "label_threads.py"
if (-not (Test-Path -LiteralPath $script)) {
    throw "Labeler not found: $script"
}

$pythonwCandidates = @(
    (Join-Path $homeDir "AppData\Local\Python\bin\pythonw.exe"),
    (Join-Path $homeDir "AppData\Local\Python\pythoncore-3.14-64\pythonw.exe")
)
$pythonw = $pythonwCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $pythonw) { throw "Could not find pythonw.exe." }

$logDir = Join-Path $homeDir ".codex\logs"
$logFile = Join-Path $logDir "thread_label_watcher.log"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

# Hidden, non-interactive run: pythonw.exe has no console, so nothing flashes.
$taskAction = '"{0}" "{1}" apply --log "{2}"' -f $pythonw, $script, $logFile
schtasks.exe /Create /F /SC MINUTE /MO $IntervalMinutes /TN $taskName /TR $taskAction | Out-Null

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -Hidden `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Set-ScheduledTask -TaskName $taskName -Settings $settings | Out-Null

# Label today's untagged threads immediately and wait for completion.
Start-Process -FilePath $pythonw `
    -ArgumentList ('"{0}" apply --log "{1}"' -f $script, $logFile) `
    -Wait -WindowStyle Hidden

# Confirm the registered task also starts cleanly.
Start-ScheduledTask -TaskName $taskName

$task = Get-ScheduledTask -TaskName $taskName
$taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
$installRecord = [ordered]@{
    schemaVersion = 1
    installedLocal = (Get-Date).ToString("o")
    editingAgent = "Codex GPT-5.6 SOL"
    taskName = $taskName
    taskState = $task.State.ToString()
    intervalMinutes = $IntervalMinutes
    lastTaskResult = $taskInfo.LastTaskResult
    labeler = $script
    logFile = $logFile
}
$installRecord | ConvertTo-Json -Depth 5
