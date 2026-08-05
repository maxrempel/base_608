param(
    [switch]$Execute
)

# Lesson 1 cleanup to the Windows Recycle Bin.
# Last edited: 2026-08-01 by Codex (GPT-5.6 SOL).

$ErrorActionPreference = 'Stop'

$tmpRoot = 'C:\moma\tmp'
$mixRoot = 'C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\music_mix'
$outRoot = Join-Path $mixRoot 'out'
$manifestPath = 'C:\claude_base\worklog\lesson1_cleanup_20260801\recycle_manifest_v01.json'
$resultPath = 'C:\claude_base\worklog\lesson1_cleanup_20260801\recycle_result_v01.json'

$publishedMaster = Join-Path $outRoot 'lesson1_COMPLETE_v123_20260731_231644.mp4'
$sourceAssembly = 'G:\My Drive\00Main2026\00_rehearsals\mixboard_assembly_scene305_20260730_142710.mp4'
$approvedMap = Join-Path $outRoot 'lesson1_LOSSLESS_clean_map_v10_20260730_143212.txt'
$inputTrumpet = 'C:\Users\maxre\Nextcloud\suno_music_catalog\audio\select2\11 v8      Nice trumpets. Pretty slow, pretty happy, pretty profound..mp3'

$protected = @(
    $publishedMaster,
    $sourceAssembly,
    $approvedMap,
    $inputTrumpet,
    'C:\moma\sc10\sound_assembly\code\musicunder'
)

$tmpNames = @(
    'lesson1_complete_v15',
    'lesson1_complete_v116',
    'lesson1_complete_v117',
    'lesson1_complete_v118',
    'lesson1_complete_v119',
    'lesson1_slides_then_music_v120',
    'lesson1_v122_qc_gated',
    'lesson1_v123_timestamp_preserved',
    'lesson1_v15_whisper',
    'musicunder_skill_test_v02'
)

$mixDirectoryNames = @(
    'closing_candidates',
    'pieces',
    'pieces_ending',
    'pieces_vid',
    'qc_v116',
    'qc_v116_190155',
    'qc_v118_195542',
    'qc_v122_225140',
    'qc_v15'
)

$targets = [System.Collections.Generic.List[object]]::new()

function Add-Target {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Reason
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    foreach ($item in $protected) {
        if ($resolved.Equals($item, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Protected path was selected: $resolved"
        }
        if ($resolved.StartsWith($item.TrimEnd('\') + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Path inside protected tree was selected: $resolved"
        }
    }
    $allowed = $resolved.StartsWith($tmpRoot + '\', [System.StringComparison]::OrdinalIgnoreCase) -or
        $resolved.StartsWith($mixRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)
    if (-not $allowed) {
        throw "Target is outside the two approved cleanup roots: $resolved"
    }

    $itemInfo = Get-Item -LiteralPath $resolved -Force
    if ($itemInfo.PSIsContainer) {
        $files = @(Get-ChildItem -LiteralPath $resolved -Recurse -File -Force -ErrorAction Stop)
        $bytes = [int64](($files | Measure-Object Length -Sum).Sum)
        $fileCount = $files.Count
        $kind = 'directory'
    } else {
        $bytes = [int64]$itemInfo.Length
        $fileCount = 1
        $kind = 'file'
    }
    $targets.Add([pscustomobject]@{
        Path = $resolved
        Kind = $kind
        Reason = $Reason
        FileCount = $fileCount
        Bytes = $bytes
        GiB = [math]::Round($bytes / 1GB, 6)
        LastWriteTime = $itemInfo.LastWriteTime.ToString('o')
    })
}

foreach ($name in $tmpNames) {
    Add-Target -Path (Join-Path $tmpRoot $name) -Reason 'Lesson 1 scratch build or QC output'
}
foreach ($name in $mixDirectoryNames) {
    Add-Target -Path (Join-Path $mixRoot $name) -Reason 'Reproducible chopped piece or QC directory'
}

$intermediateMedia = Get-ChildItem -LiteralPath $outRoot -File -Force | Where-Object {
    $_.FullName -ne $publishedMaster -and (
        $_.Extension -in @('.mp4', '.mp3') -or $_.Name -like '*.mp4-*'
    )
}
foreach ($file in $intermediateMedia) {
    Add-Target -Path $file.FullName -Reason 'Rejected, superseded, preview, or numbered Lesson 1 media output'
}

if (-not (Test-Path -LiteralPath $publishedMaster -PathType Leaf)) {
    throw 'Published v123 master is missing before cleanup'
}
if (-not (Test-Path -LiteralPath $sourceAssembly -PathType Leaf)) {
    throw 'Synchronized source assembly is missing before cleanup'
}
if (-not (Test-Path -LiteralPath $approvedMap -PathType Leaf)) {
    throw 'Approved v10 music map is missing before cleanup'
}
if (-not (Test-Path -LiteralPath $inputTrumpet -PathType Leaf)) {
    throw 'Input trumpet track is missing before cleanup'
}

$totalBytes = [int64](($targets | Measure-Object Bytes -Sum).Sum)
$plan = [pscustomobject]@{
    Created = (Get-Date).ToString('o')
    ExecuteRequested = [bool]$Execute
    Policy = 'Recoverable Windows Recycle Bin; do not empty without Max approval'
    Protected = $protected
    TargetCount = $targets.Count
    FileCount = [int](($targets | Measure-Object FileCount -Sum).Sum)
    TotalBytes = $totalBytes
    TotalGiB = [math]::Round($totalBytes / 1GB, 3)
    Targets = @($targets)
}
$plan | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding utf8

Write-Output ("TARGETS={0}" -f $targets.Count)
Write-Output ("FILES={0}" -f $plan.FileCount)
Write-Output ("TOTAL_GIB={0}" -f $plan.TotalGiB)
$targets | Sort-Object Bytes -Descending | Format-Table Kind, FileCount, GiB, Path -AutoSize

if (-not $Execute) {
    Write-Output "PLAN_ONLY=$manifestPath"
    exit 0
}

if ($env:LESSON1_ARCHIVE_VERIFIED -ne 'YES') {
    throw 'Archive verification gate is not set'
}

Add-Type -AssemblyName Microsoft.VisualBasic
$completed = [System.Collections.Generic.List[object]]::new()
foreach ($target in ($targets | Sort-Object Bytes -Descending)) {
    if ($target.Kind -eq 'directory') {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory(
            $target.Path,
            [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
            [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin,
            [Microsoft.VisualBasic.FileIO.UICancelOption]::ThrowException
        )
    } else {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
            $target.Path,
            [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
            [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin,
            [Microsoft.VisualBasic.FileIO.UICancelOption]::ThrowException
        )
    }
    if (Test-Path -LiteralPath $target.Path) {
        throw "Recycle operation returned but target still exists: $($target.Path)"
    }
    $completed.Add($target)
}

$result = [pscustomobject]@{
    Completed = (Get-Date).ToString('o')
    Status = 'MOVED_TO_RECYCLE_BIN_NOT_EMPTIED'
    TargetCount = $completed.Count
    FileCount = [int](($completed | Measure-Object FileCount -Sum).Sum)
    TotalBytes = [int64](($completed | Measure-Object Bytes -Sum).Sum)
    TotalGiB = [math]::Round((($completed | Measure-Object Bytes -Sum).Sum) / 1GB, 3)
    Targets = @($completed)
}
$result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultPath -Encoding utf8
Write-Output "STATUS=MOVED_TO_RECYCLE_BIN_NOT_EMPTIED"
Write-Output "RESULT=$resultPath"
