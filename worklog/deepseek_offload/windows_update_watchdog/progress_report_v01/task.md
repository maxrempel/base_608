---
title: Draft Windows Update watchdog progress report v01
date: 2026-07-29
author: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Draft a concise but proper operational incident-and-remediation report in
Markdown. Return only the proposed report in result.md. Do not use tools or
invent facts.

Required metadata near the top:

- Title: Pine Windows Update interruption and manual-only watchdog
- Version 01
- Date 2026-07-29
- Last edited 2026-07-29 by Codex (GPT-5.6 SOL)
- Status: RESOLVED AND MONITORED
- Memex search terms

Audience: Max, Codex, and Claude. The report must be useful months later and
searchable by phrases such as Windows Update, overnight run interrupted,
Microsoft Store, ChatGPT install, forced restart, manual-only, Pine, watchdog,
NoAutoUpdate, and Update Orchestrator.

Verified facts:

- Windows System event 1074 recorded planned restarts on 2026-07-29 at 01:29,
  01:35, and 01:38 local time. The first was initiated by
  MoUsoCoreWorker.exe; the next two by TrustedInstaller.exe.
- Active hours were 07:00 through 01:00, so the first forced restart happened
  shortly after active hours ended.
- Before remediation, no computer policy existed under
  HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU. Windows Update and
  Update Orchestrator services were configured automatic.
- Updates KB5100998, KB5101650, and KB5120102 were installed. There was no
  reboot pending after investigation.
- Likely operational cause, not fully auditable: a prior Microsoft Store /
  ChatGPT installation session re-enabled Windows Update components and did
  not restore manual-only mode. Registry-change auditing was not enabled, so
  the exact process that removed or failed to restore the old setting cannot
  be proven.
- Immediate remediation set and verified DWORD values NoAutoUpdate=1,
  AUOptions=2, and NoAutoRebootWithLoggedOnUsers=1. Manual Windows Settings
  checks remain available.
- Durable tool folder:
  C:\claude_base\tools\windows_update_manual_only
- Hidden scheduled task WindowsUpdateManualOnlyWatchdog runs as SYSTEM at
  startup and every minute.
- It restores all three values, runs gpupdate, verifies the repair, logs it,
  and emails Max once per incident. Failed email attempts retry. A failed
  repair sends one urgent alert, continues retrying each minute, then sends
  one recovery alert.
- Email sender is mass@tamza.com, visible recipient max@tamza.com, with
  max.rempel2@gmail.com on BCC.
- Routine healthy runs are silent; an hourly local heartbeat proves liveness.
- Installation result: SUCCESS, task Ready, hidden, SYSTEM, last result 0.
- End-to-end SYSTEM email test passed, with policy healthy and email sent.
- Recurring heartbeat after installation confirmed all values healthy.
- Deterministic synthetic tests passed for incident deduplication, email retry,
  repeated remediation, new incidents, and recovery after a failed repair.
- Source committed and pushed to claude_base master in commit 794ebbbc.

Required sections:

1. Executive summary
2. What happened
3. Root-cause assessment, clearly separating evidence from inference
4. Immediate remediation
5. Permanent watchdog behavior
6. Verification evidence
7. Operations and future maintenance
8. Current status

Keep it around 700 to 1,100 words, plain English, no secrets, no raw URLs, and
no unsupported claim that Microsoft Store itself necessarily enables all
automatic Windows updates.
