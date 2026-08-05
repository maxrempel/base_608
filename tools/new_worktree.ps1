# Create a new worktree for a session
# Usage: .\new_worktree.ps1 <session-name>
# Example: .\new_worktree.ps1 moma_lesson_v3

param(
    [Parameter(Mandatory=$true)]
    [string]$SessionName
)

$worktreePath = "C:\base_608\worktrees\$SessionName"
$branchName = "codex/$SessionName"

Write-Host "Creating worktree for session: $SessionName"
Write-Host "  Path: $worktreePath"
Write-Host "  Branch: $branchName"

# Create the worktree
git worktree add -b $branchName $worktreePath

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nWorktree created successfully!"
    Write-Host "To work in this session:"
    Write-Host "  cd $worktreePath"
    Write-Host "`nTo list all worktrees:"
    Write-Host "  git worktree list"
    Write-Host "`nTo remove when done:"
    Write-Host "  git worktree remove $worktreePath"
} else {
    Write-Host "Failed to create worktree" -ForegroundColor Red
}
