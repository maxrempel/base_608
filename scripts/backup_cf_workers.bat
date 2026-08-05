@echo off
REM Nightly Cloudflare workers + KV backup. Created 2026-05-22 by Claude Opus 4.7.
REM 1) Pull all workers + KV via CF API into C:\cloud_base\backups\.
REM 2) Commit + push to github.com/maxrempel/cloud_base.
cd /d C:\cloud_base
python scripts\backup_cf_workers.py
if errorlevel 1 (
  echo backup_cf_workers.py FAILED, skipping git commit
  exit /b 1
)
git add backups/cf_workers backups/cf_kv_pages backups/backup_cf.log
git diff --cached --quiet
if errorlevel 1 (
  for /f "tokens=*" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH:mm"') do set TS=%%i
  git commit -q -m "cf workers+kv backup %TS%"
  git push origin master
) else (
  echo no changes
)
