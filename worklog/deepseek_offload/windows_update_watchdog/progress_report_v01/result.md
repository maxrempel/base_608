```markdown
# Pine Windows Update interruption and manual-only watchdog

- **Version**: 01
- **Date**: 2026-07-29
- **Last edited**: 2026-07-29 by Codex (GPT-5.6 SOL)
- **Status**: RESOLVED AND MONITORED
- **Memex search terms**: Windows Update, overnight run interrupted, Microsoft Store, ChatGPT install, forced restart, manual-only, Pine, watchdog, NoAutoUpdate, Update Orchestrator

---

## 1. Executive summary

On 2026-07-29 between 01:29 and 01:38 local time, Pine experienced three forced restarts caused by Windows Update. These interruptions broke overnight batch runs and highlighted that manual-only update control had been silently lost. Immediate registry hardening restored manual-only behavior, and a persistent watchdog task now enforces the policy every minute and alerts via email if violations occur. The system is currently stable, all policy values are healthy, and no further unscheduled restarts have occurred.

## 2. What happened

Windows System event 1074 recorded three planned restarts:

- 01:29 – initiated by `MoUsoCoreWorker.exe`
- 01:35 – initiated by `TrustedInstaller.exe`
- 01:38 – initiated by `TrustedInstaller.exe`

Active hours were configured from 07:00 to 01:00, so the first forced restart occurred just minutes after active hours ended. Updates KB5100998, KB5101650, and KB5120102 were installed during these restarts. After investigation, no reboot remained pending.

Before the incident, no computer policy existed under `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`. The Windows Update and Update Orchestrator services were both set to automatic start, leaving the system vulnerable to automatic download and installation.

## 3. Root-cause assessment

**Evidence (directly observable):**

- Registry policy keys were absent, meaning Windows Update fell back to default behavior (automatic download and install).
- Services were set to automatic.
- A prior session involved installing ChatGPT from the Microsoft Store; the Store often modifies Windows Update related settings to enable the downloading of app updates and dependencies.
- No registry-change auditing was enabled, so the exact chain of registry modifications cannot be reconstructed.

**Inference (supported by context, but not proven):**

- The most likely cause is that the Microsoft Store / ChatGPT installation session re-enabled Windows Update components (e.g., set services to automatic, removed existing manual-only policies) and did *not* restore the original manual-only configuration.
- It is *not* necessarily true that the Microsoft Store itself always enables all automatic Windows updates, but in this case the combination of a Store session and the observed loss of policy strongly suggests it was the trigger.
- The absence of an existing `AU` policy made it easy for any application or installer to restore default update behavior without leaving a record.

## 4. Immediate remediation

The following DWORD values were set and verified under `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`:

- `NoAutoUpdate = 1`
- `AUOptions = 2`
- `NoAutoRebootWithLoggedOnUsers = 1`

These registry entries block automatic update download and installation, notify the administrator, and prohibit automatic reboots while users are logged on. Manual checks through Windows Settings remain available.

## 5. Permanent watchdog behavior

A hidden scheduled task named **WindowsUpdateManualOnlyWatchdog** was created and stored in:

`C:\claude_base\tools\windows_update_manual_only`

The task:

- Runs as SYSTEM
- Triggers at system startup and every minute thereafter
- Reads the three policy values from the registry
- If any value is missing or incorrect, restores all three, runs `gpupdate /force`, and verifies the repair
- Logs all actions locally
- Sends an email to `max@tamza.com` (sender: `mass@tamza.com`, BCC: `max.rempel2@gmail.com`) once per incident
- If sending fails, retries indefinitely
- If a repair fails, sends one urgent alert, continues retrying every minute, and sends one recovery alert when the values are healthy again

During routine healthy runs the task is completely silent. An hourly local heartbeat log entry proves the watchdog is alive.

The task was installed with result **SUCCESS**, current status **Ready**, hidden, SYSTEM account, last result **0**. An end-to-end email test with SYSTEM privileges passed: the policy was healthy and the test email was delivered.

## 6. Verification evidence

- Immediate post‑remediation registry check confirmed all three values were present and correct.
- Recurring heartbeat logs after installation show all values still healthy.
- Deterministic synthetic tests validated:
  - Incident deduplication (only one alert per event)
  - Email retry on transient failure
  - Repeated remediation on persistent policy drift
  - New incident detection after a resolved incident
  - Recovery alert after a simulated failed repair
- The source code and configuration were committed and pushed to `claude_base` master in commit `794ebbbc`.

## 7. Operations and future maintenance

- The watchdog is self‑healing and requires no routine attention.
- If policy values change again (due to Store updates, manual edits, or other processes), the watchdog will detect the drift within one minute and restore the manual-only configuration.
- Email alerts will reach Max at the primary and backup addresses.
- To inspect the watchdog, check the task scheduler library or review the logs in `C:\claude_base\tools\windows_update_manual_only\logs\`.
- If a legitimate update is desired, the watchdog must be temporarily disabled and re‑enabled after the update completes.

## 8. Current status

**RESOLVED AND MONITORED.** All three registry policies are in place, the watchdog is running and passing heartbeat checks, and no new forced restarts have been reported. The system is back to manual-only update control with active enforcement.
```
