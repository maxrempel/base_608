# Scribe handover - milestone 5 (~416K tokens)
# session: 20260721_claude_base_a6d44e5f
# cwd: C:\claude_base
# written: 2026-07-21 23:13:52 by deepseek-v4-pro

# HANDOVER: Taygeta (tay) - GPU Workstation Setup

---

## GOAL (in Max's words)

Set up the new computer (RTX 5060 Ti, 16GB) as a local render + genomics server. Core need: **image + sound + prompt ? lip-synced video**, ~15 seconds, running locally on the GPU. Plus genomics toolchain, plus Docker containers for Mike and Liz with throttled resources and SSH-key access over Tailscale.

---

## DECISIONS MADE + WHY

### OS & Install
- **Pure Ubuntu 24.04, wiped Windows entirely.** Cleaner for NVIDIA drivers, better as a server, Windows had no data.
- **Desktop installer, not Server.** The old stick that actually booted was a Desktop ISO; Server would have been fine but Desktop was what worked.
- **Ticked "third-party drivers" during install** - pulled in NVIDIA driver automatically. This WORKED. The RTX 5060 Ti was live on first boot.

### Access & Security
- **SSH key-only login** (sol_key). Passwords now refused. Firewall limited to 192.168.1.x (home LAN). SSH enabled at boot.
- **Password stored** in `shared_logins_frequent.txt` as backup.
- **No cloud-init / auto-SSH trick.** The Sol "rescue boot" plan never fully worked; interactive install + one manual `sudo apt install openssh-server` was the reliable path. Max hated it but it was unavoidable.

### Video Pipeline (THE KEY DECISION)
- **Wan 2.2 S2V (Speech-to-Video), not I2V, not MultiTalk, not InfiniteTalk.** The I2V models only animate images - they cannot lip-sync to audio. S2V is the only local Wan model that takes image + audio + prompt and produces a talking video. This was confirmed via research during this session.
- MoMA's cloud reels use **Wan 2.6 i2v-flash** on Alibaba DashScope (cloud-only, ~$0.43/clip). S2V 2.2 is the closest local equivalent.
- **ComfyUI** is the engine. Installed with stable CUDA 12.8 PyTorch (torch 2.11.0+cu128). The nightly build caused a dependency conflict; stable cu128 fixed it.

### 24TB External Drive
- Originally formatted ext4 as "red24", then Max requested **universal Windows+Unix compatibility**.
- **Reformatted to exFAT, renamed green24.** Mounted at `/mnt/green24`, auto-mounts on boot. exFAT handles cross-platform and large files fine.
- Convention: color + size in TB (teal16 was taken, green24 is new).

### Heartbeat Monitor
- **Healthchecks.io, repurposed Sol's dead `sol-host` slot.** Free tier was maxed at 20 checks. Sol is dead, so its 3 checks were killed (2 deleted, 1 renamed to `taygeta-host`). Pings every 5 minutes, alarms to Telegram + email if silent.

### Docker for Mike & Liz (DESIGNED, NOT BUILT)
- One container per person. **SSH with keys over Tailscale.** Remote access from anywhere.
- 33% CPU/RAM ceiling each - releasable (idle containers use near-zero resources).
- Home folders on green24.
- GPU shared cooperatively (can't be hard-split like CPU/RAM).
- **Still awaiting:** their public keys (or I generate keypairs), and confirmation of what they actually do inside the containers.

---

## CURRENT STATE - WHAT IS DONE

| Layer | Status |
|---|---|
| Ubuntu 24.04 installed, bootable | ? |
| Hostname: taygeta (synonym: tay) | ? |
| IP: 192.168.1.142 (DHCP, may drift) | ? |
| SSH key-only, LAN firewall, survives reboots | ? |
| NVIDIA RTX 5060 Ti working (16GB, CUDA 13.2) | ? |
| Genomics venv (pysam 0.24, whatshap, samtools, bcftools, bwa) | ? |
| Heartbeat monitor (Healthchecks.io) | ? |
| green24 drive (24TB exFAT, /mnt/green24) | ? |
| ComfyUI + Wan 2.2 S2V pipeline | ? **PROVEN** |
| First test render (3s lipsync mp4) | ? Saved to green24 + Pine Downloads |
| Tailscale installed on Taygeta | ?? **NOT AUTHORIZED** |
| Docker containers for Mike/Liz | ? Not built |
| All docs updated (local + Notion) | ? |

### The Test Render
- `s2v_test_00001_.mp4` - h264 480?480, 49 frames, 3.06s, with embedded AAC speech audio.
- Deliberately rough (low-res MoMA plate thumbnail + robotic espeak TTS) - a pipeline proof, not a beauty shot.
- GPU fit it comfortably (~13GB of 16GB used).
- **Locations:** `~/ComfyUI/output/s2v_test_00001_.mp4` on Taygeta, `/mnt/green24/s2v_tests/`, and `C:\Users\maxre\Downloads\taygeta_s2v_test_first.mp4` on Pine.

---

## EXACT NEXT STEP

### #1 - TAILSCALE AUTHORIZATION (blocks Docker containers)
Tailscale is installed on Taygeta (v1.98.9) but **not yet joined to the "rempel house" tailnet.** Max said to authorize it myself using Playwright + Bitwarden rather than handing him a login link.

The tailnet uses **GitHub SSO** (user maxrempel). Credentials are in Bitwarden. A fresh auth link may be needed - the old one (`https://login.tailscale.com/a/16b7e2f018827`) is likely expired.

Once authorized, confirm with `tailscale status` on Taygeta - it should show as connected.

### #2 - DOCKER CONTAINERS FOR MIKE & LIZ (after Tailscale)
Build: one GPU-enabled Ubuntu container each, SSH-key access, 33% CPU/RAM releasable caps, home on green24. Generate keypairs if theirs aren't provided. Containers reachable over Tailscale from anywhere.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **What do Mike and Liz actually do in their containers?** AI/video, coding, genomics, general sandbox? This determines what software goes inside.
2. **Their SSH public keys** - do they have existing ones, or do I generate keypairs and hand you the private keys to forward?
3. **Static IP for Taygeta?** Currently DHCP (192.168.1.142). Pinning it would prevent address drift after reboots. I offered, Max hasn't decided.

---

## KEY PATHS / IDs / COMMANDS

### Access
- **SSH:** `ssh -i ~/.ssh/sol_key maxre@192.168.1.142`
- **Password:** `T2w3e4r5t6y=` (stored in `shared_logins_frequent.txt`)
- **Tailscale auth:** GitHub SSO, maxrempel, Bitwarden

### File Paths on Pine
- **Canonical setup doc:** `C:\claude_base\tools\taygeta\taygeta_setup_20260716_v01_tomemex.md`
- **Machine memory:** `C:\Users\maxre\.claude\projects\C--claude-base\memory\project_tageta_machine.md`
- **Global register:** `C:\Users\maxre\Nextcloud\claude_md_synced\global_CLAUDE.md`
- **Drives registry:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\drives_registry.md`
- **Healthchecks API key:** `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (read-only for listing; writes may need a different key)
- **sol_key:** `~/.ssh/sol_key` (ed25519, also called "pine-to-sol" in memories)

### File Paths on Taygeta
- **ComfyUI:** `~/ComfyUI/` (venv at `~/ComfyUI/venv/`)
- **Models:** `~/ComfyUI/models/{diffusion_models,text_encoders,audio_encoders,vae}/`
- **S2V fire script:** `~/setup/scripts/s2v_fire.py`
- **Logs:** `~/setup/logs/{comfy_fix.log,s2v_models.log,genomics.log,moma.log}`
- **green24:** `/mnt/green24/` (UUID `cd5128bf-03d6-404a-85ce-59b4d8f58680`, exFAT)
- **Test output:** `/mnt/green24/s2v_tests/s2v_test_20260716_101525.mp4`

### S2V Models (downloaded, verified working)
- `wan2.2_s2v_14B_fp8_scaled.safetensors` - 15.3 GB (diffusion_models)
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` - 6.3 GB (text_encoders)
- `wav2vec2_large_english_fp16.safetensors` - 1.2 GB (audio_encoders)
- `wan_2.1_vae.safetensors` - 249 MB (vae)

### Healthchecks.io
- **taygeta-host:** UUID `023cf3f6-186a-4af4-88df-ee7cd4b103d7` (was sol-host, renamed)
- **Deleted:** sol-cpu-temp, sol-notion-task-sync
- **Monitor account:** 18/20 used (2 freed by deleting Sol checks)

### Docker Design (saved, not implemented)
- Per-user containers, SSH-key access, Tailscale reachable
- 33% CPU/RAM releasable caps (~8 cores each on a 24-thread machine)
- GPU shared (no hard split possible)
- Home dirs on green24

---

## GOTCHAS & DEAD ENDS

### The Boot/Install Ordeal
- **Secure Boot on MSI boards rejects old bootloaders** (SBAT policy violation). Disabling Secure Boot sometimes doesn't stick on AM5 MSI boards. The fix: use a **fresh** Ubuntu ISO whose bootloader is current.
- **The old 16GB SanDisk was Debian, not Ubuntu** - the photo that failed to send would have revealed this earlier. Max found an Ubuntu stick later that actually booted.
- **Flashing USB from Windows/WSL deadlocks** - Windows locks the disk, WSL can't get exclusive access. The workaround: copy the ISO to **Lak** (a Linux server) and `dd` it there. Lak is `192.168.1.199`, SSH: `ssh -i ~/.ssh/lakarian_key.pem mrempadmin@100.110.225.89`.
- **"Two sticks" memory is obsolete** - that was the DVD era. Modern Ubuntu is a single all-in-one stick.

### SSH Setup
- **`curl` is not installed on fresh Ubuntu Desktop.** The `curl ... | sudo bash` bootstrap failed. The fix that worked: `sudo apt install -y openssh-server` directly. This is inescapable - a fresh Linux box has no remote door until someone opens it once at the keyboard.
- **The Sol "cloud-init auto-SSH" trick never worked reliably.** Don't waste time on it again.

### Video Pipeline
- **Wan I2V 2.1/2.2 models DO NOT lip-sync.** They only animate images. I started downloading them and Max stopped it. The correct model for image+sound?talking is **Wan 2.2 S2V** (Speech-to-Video).
- **Wan 2.6 i2v-flash is cloud-only** (Alibaba DashScope). Not downloadable.
- **ComfyUI nightly PyTorch caused dependency conflicts.** Stable CUDA 12.8 (`torch==2.11.0+cu128`) works. Custom nodes needed: WanVideoWrapper, KJNodes, VideoHelperSuite, ComfyUI-Manager.
- **The S2V render IS slow on 16GB** (~15s per sampling step, ~5 minutes for a short clip). It fits, but it's not fast.

### Naming
- The machine registered as **"taigeta"** on the network initially (Ubuntu picked up a typo from... somewhere). Renamed to **taygeta** via `hostnamectl`, fixed `/etc/hosts`.
- Synonym: **tay** = taygeta (registered in terminology dictionary).
