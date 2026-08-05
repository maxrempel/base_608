---
title: Draft Pine Windows Update watchdog v01
date: 2026-07-29
author: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Draft a compact, production-quality design and code for a deterministic Windows
Python watchdog plus a PowerShell installer. Do not access tools, credentials, or
external systems. Return proposed code and review notes only in result.md.

Requirements:

- Target Pine, Windows 10/11 Pro.
- Every minute and at startup, verify these DWORD values under
  HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU:
  NoAutoUpdate=1, AUOptions=2, NoAutoRebootWithLoggedOnUsers=1.
- The scheduled task runs hidden as NT AUTHORITY\SYSTEM, so remediation can write
  HKLM without UAC.
- If any value is absent or wrong, immediately restore all three values, run
  gpupdate /Target:Computer /Force without a visible window, verify the repair,
  append a concise log, and email Max.
- Email uses the existing module
  C:\claude_base\tools\mxmail\mxmail_v01.py, sender mass@tamza.com, recipients
  max@tamza.com and max.rempel2@gmail.com, no assistant signature.
- Deduplicate alerts by incident: one email for the detected/reset event; no email
  on healthy runs. If email fails, retry on later runs until sent. A new future
  mismatch must create a new incident and alert.
- Keep state and logs beside the script, using atomic state writes. Do not record
  secrets.
- Add --check (normal), --self-test (no registry mutation; validate local logic
  and optionally send a clearly labeled test email), and useful exit codes.
- Use Python standard library plus winreg. Prevent visible consoles for child
  processes with CREATE_NO_WINDOW.
- Handle concurrent invocation safely with a simple lock or atomic exclusive file.
- Installer creates/updates a hidden Windows Scheduled Task named
  WindowsUpdateManualOnlyWatchdog with startup plus one-minute repetition,
  IgnoreNew, no battery restriction, reasonable timeout, and SYSTEM highest
  privileges. It must not store credentials in the task.
- Include likely failure modes and tests. Avoid unnecessary dependencies.
