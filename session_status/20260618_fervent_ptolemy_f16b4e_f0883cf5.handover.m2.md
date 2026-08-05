# Scribe handover - milestone 2 (~154K tokens)
# session: 20260618_fervent_ptolemy_f16b4e_f0883cf5
# cwd: C:\moma\.claude\worktrees\fervent-ptolemy-f16b4e
# written: 2026-06-18 15:23:05 by deepseek-v4-pro

# HANDOVER: AstolfoDebian (asto) Setup - Cold Session Resume

---

## GOAL (Max's words)

"let's setup that computer" - following Liz's instructions to get AstolfoDebian (a computer in Liz's home server room) accessible as an auxiliary compute node from Pine (Max's Windows machine). The machine is to be used for video processing, genomics alignment, transcription - general "send work there" tasks when Max needs more CPU/RAM than his local machine has.

---

## DECISIONS + WHY

1. **SSH key auth over password:** Liz's instructions specify a Bitwarden-shared SSH key ("mremp AstolfoDebain"). The private key was posted in the session and saved. Host key accepted on first connect (tailnet-encrypted, safe). The public key fingerprint Max originally supplied (`GuUr5m/...`) was actually the *auth key* fingerprint, not the host key - verified it matches.

2. **Tailscale join via GitHub (not Google):** When prompted for Tailscale login, Max's account is GitHub (`maxrempel`), NOT his Google account. Discovered live when Max authenticated. Saved to notes.

3. **Container base: Ubuntu 24.04 LTS, not Fedora:** Liz's instructions used `dnf` as an example (Fedora), but Max doesn't have a distro preference. I recommended Ubuntu 24.04 LTS because:
   - Genomics/ML tools assume Ubuntu (most copy-paste recipes)
   - LTS is stable for long-running auxiliary jobs
   - AMD GPU means CUDA is irrelevant; workloads are CPU-bound anyway
   Max agreed. The original Fedora container was deleted; Ubuntu 24.04 LTS created instead.

4. **No conda/genomics toolchain installed yet:** Max said "don't setup genomics yet." Only Python 3.12 + pip are installed inside the Ubuntu container. Genomics tools will be installed on-demand when a specific task arises.

5. **Container sudo is passwordless:** As Liz designed - `distrobox enter ubuntu` gives full root inside without the host password. Host sudo needs the password (from Bitwarden "Max login to AstolfoDebian"), but the design is to do work inside the container, not on the host.

6. **Tailscale install hiccup:** The winget installer hung at "Initializing" because the UAC popup was minimized on Max's second screen. Noted for future: Tailscale setup on Windows shows a UAC prompt that can get lost on multi-monitor setups.

---

## CURRENT STATE

### Access
- **Pine** (Windows) is joined to the **"rempel house" Tailscale tailnet** (GitHub login: `maxrempel`)
- **asto** is reachable at `astolfodebian.tail251d88.ts.net` with 4ms latency
- SSH key works: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
- User: `rempel`, host sudo password in Bitwarden "Max login to AstolfoDebian"

### Hardware (asto) - from `fastfetch`
- **Host OS:** Debian 13 (AORUS B760 motherboard)
- **CPU:** Intel i5-12600K, 16 threads, up to 4.9 GHz
- **RAM:** 31 GB (29 GB free) + 32 GB swap
- **GPU:** AMD Radeon RX 6650 XT (discrete) + Intel iGPU - **GPU re-seat + power cable fix worked**, card is alive
- **Disk /:** 1.2 TB total, 986 GB free (btrfs)
- **Disk /mnt/shared:** 503 GB, 86% full (ext4) - Liz's, don't touch without permission

### Container
- **Name:** `ubuntu`
- **Base:** Ubuntu 24.04 LTS
- **Inside:** Python 3.12.3 + pip installed
- **Sudo:** full passwordless root
- **Not installed:** ffmpeg, genomics tools, conda - deferred to on-demand

### Files saved
- Private key: `~/.ssh/bitwarden_ed25519` (Windows) + backup in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\`
- Known hosts: host key accepted
- Login notes: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt` - contains asto access details, specs, tailnet account note, container info
- Stuck install note: Tailscale UAC prompt got lost on second screen - documented in session

### Worklog
- Entry logged via `python C:/claude_base/compaction_kb/scripts/worklog.py log` summarizing the setup

---

## EXACT NEXT STEP

1. **Update all documentation** - Max wants:
   - Global2 (the knowledge base at `C:/claude_base/compaction_kb/` presumably)
   - A "report" to `tomemex.md` (or similar filename)
   - Notion - update any relevant Notion pages with the new asto access info
   - "Update all docs everywhere" - ensure asto is recorded in the system database (registered as "asto")

2. After docs are updated: **nothing else pending.** The machine is ready for work. When Max sends a task (video processing, transcription, alignment, etc.), SSH into asto, enter the Ubuntu container, install what's needed on-demand, and run it there.

---

## OPEN QUESTIONS

None awaiting Max - the setup is complete.

Implicit to-dos for future sessions when Max sends work:
- Install `ffmpeg` if video processing is needed
- Install conda + genomics tools (bwa, samtools, minimap2) if alignment/transcription tasks come
- `/mnt/shared` - Liz's mount, permission required before using

---

## KEY PATHS / IDS

| What | Path/Value |
|---|---|
| SSH key (private) | `C:\Users\maxre\.ssh\bitwarden_ed25519` |
| SSH key (backup) | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\` |
| Hostname (Tailscale) | `astolfodebian.tail251d88.ts.net` |
| Hostname (LAN) | `192.168.1.243` |
| SSH user | `rempel` |
| SSH command (Windows) | `ssh -i $HOME\.ssh\bitwarden_ed25519 -o ConnectTimeout=20 rempel@astolfodebian.tail251d88.ts.net` |
| Container entry | `distrobox enter ubuntu` (on asto) |
| Container name | `ubuntu` |
| Tailscale binary (Windows) | `C:\Program Files\Tailscale\tailscale.exe` |
| Login notes file | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt` |
| Worklog script | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| Bitwarden - SSH key | "mremp AstolfoDebain" |
| Bitwarden - user password | "Max login to AstolfoDebian" |
| Tailscale account | GitHub - `maxrempel` (NOT Google) |
| Tailnet name | "rempel house" |

---

## GOTCHAS

- **Tailscale UAC prompt can get lost on second screen** - if a winget install appears to hang, check all monitors for a minimized UAC popup before killing the process.
- **Container name is `ubuntu`, not `fedora`** - Fedora was deleted. Any future session that tries to `distrobox enter fedora` will fail.
- **SSH fingerprint confusion** - the `GuUr5m/...` fingerprint Max sent was the auth *key* fingerprint, not the host key. Host key was trusted on first connect via encrypted tailnet.
- **No root on host** - `rempel` is in the `sudo` group on asto but needs the Bitwarden password. All work is meant to happen inside the distrobox container where sudo is passwordless.
- **/mnt/shared is Liz's** - 86% full ext4 mount, not for Max's use unless explicitly cleared.
