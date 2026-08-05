
## [2026-07-15 22:06] ? 8941679b
- DID: Set up Tageta (new GPU box, RTX 5060 Ti 16GB): wiped Windows, installed Ubuntu 24.04, SSH key-only from Pine (ssh -i ~/.ssh/sol_key maxre@192.168.1.142), firewalled to LAN, hostname taygeta. NVIDIA driver 595 already working. Launched detached overnight installs.
- STATE: Genomics venv (~/genomics/venv: pysam/whatshap/etc) + MoMA video stack (~/ComfyUI + torch cu128 + WanVideoWrapper/KJNodes/VideoHelper nodes) installing; Wan2.1 I2V 14B + MultiTalk model download throttled 10MB/s. Logs in ~/setup/logs/ on taygeta.
- NEXT: Verify installs completed; check torch.cuda + node loads; CORRECT any wrong model filenames/URLs in moma_models.sh (flagged as needs-verify); test a ComfyUI Wan+MultiTalk render with Max; register $99 protection plan; add taygeta to global CLAUDE.md MACHINES.

## [2026-07-15 22:13] ? 8941679b
- DID: Taygeta night wrap: genomics venv DONE (pysam/whatshap). Heartbeat monitor DONE - repurposed dead sol-host Healthchecks check to 'taygeta-host (heartbeat)', 5-min cron on Taygeta, alarms TG+email (HC free tier at 20-check cap). Stopped/deleted local Wan I2V download - those don't lipsync.
- STATE: MoMA image+audio->lipsync = CLOUD Wan 2.6 i2v-flash on DashScope (combo_wan26au_worker.py). Local lipsync would be MultiTalk/InfiniteTalk. ComfyUI base install hit torch-cu128 conflict, parked.
- NEXT: Ask Max: install InfiniteTalk locally on Taygeta vs keep cloud Wan2.6-flash. If local: fix ComfyUI torch-cu128 install + get InfiniteTalk. Register $99 plan. Add taygeta to global CLAUDE.md MACHINES.

## [2026-07-15 23:08] ? 8941679b
- DID: Overnight check (23:08): Taygeta healthy. Genomics venv verified (pysam 0.24/whatshap import OK). Heartbeat cron pinging every 5min. No stray video downloads. GPU idle 30C.
- STATE: All autonomous work done. Video (image+audio lipsync) PARKED pending Max: local InfiniteTalk/MultiTalk vs cloud Wan2.6-flash. ComfyUI torch-cu128 install still needs fixing IF going local.
- NEXT: When Max returns: get his local-vs-cloud lipsync decision. If local: fix ComfyUI torch cu128 dep conflict + install InfiniteTalk. Register $99 plan. Add taygeta to global CLAUDE.md MACHINES.

## [2026-07-16 08:03] ? 8941679b
- DID: Killed all Sol Healthchecks monitors (sol-host reused as taygeta heartbeat; sol-cpu-temp + sol-notion-task-sync deleted) - Sol alarm spam stopped, account 20->18 checks. Read Telegram monitor logs (confirmed taygeta-host RECOVERED 22:12).
- STATE: DECIDED local lipsync tool = ComfyUI + Wan 2.2 S2V (Speech-to-Video): image+sound+prompt -> lipsynced video ~15s (3 chained sections), FP8 fits RTX 5060 Ti 16GB. Alt MuseTalk (faster, mouth-only). ComfyUI base install still has torch-cu128 dep conflict to fix.
- NEXT: Install path: fix ComfyUI torch-cu128 install on taygeta, add Wan 2.2 S2V custom nodes + download S2V FP8 weights (throttled), test image+audio+prompt render. Then register $99 plan, add taygeta to global CLAUDE.md MACHINES.

## [2026-07-16 08:35] ? 8941679b
- DID: IMPLEMENTING Wan 2.2 S2V on taygeta (autonomous): relaunched ComfyUI install with STABLE torch cu128 (fixes nightly dep conflict) + WanVideoWrapper/KJNodes/VideoHelper nodes (comfy_fix.sh). Launched throttled S2V model download (s2v_models.sh, 6MB/s): wan2.2_s2v_14B_fp8_scaled, umt5_xxl_fp8, wav2vec2_large_english_fp16, wan_2.1_vae into ComfyUI/models/{diffusion_models,text_encoders,audio_encoders,vae}. Exact URLs from docs.comfy.org Comfy-Org repackaged repos.
- STATE: Both detached+logged (~/setup/logs/comfy_fix.log, s2v_models.log). Torch install ~10min, models ~1hr. Genomics done; heartbeat live; sol monitors killed.
- NEXT: On wake: verify torch.cuda_ok, nodes load, 4 S2V models present; then headless ComfyUI + run S2V test render (image+audio+prompt) - need a sample image + short audio. Register $99 plan; add taygeta to global CLAUDE.md MACHINES.

## [2026-07-16 09:05] ? 8941679b
- DID: Formatted+mounted 24TB Seagate Expansion on taygeta as red24 (ext4, /mnt/red24, fstab nofail, UUID cd5128bf...); was empty factory exFAT. Added tay=taygeta synonym + red24 to user dictionary + drives_registry.
- STATE: red24 live, 22TB free, writable, survives reboot. S2V install + model download still running in background.
- NEXT: Confirm drive name color with Max (chose red24); use red24 for render outputs/genomics + docker user data.

## [2026-07-16 09:38] ? 8941679b
- DID: Wan 2.2 S2V install on taygeta SUCCESS: torch 2.11.0+cu128 cuda_ok True (RTX 5060 Ti), all 4 custom nodes load (WanVideoWrapper/KJNodes/VideoHelper/Manager), ComfyUI headless up on 127.0.0.1:8188 (API 200, no errors, only optional FantasyPortrait/onnx warning). Models: diffusion 15.3GB + text_encoder 6.3GB DONE; wav2vec2 audio_encoder + wan_2.1_vae still downloading (small, ~min).
- STATE: ComfyUI running headless on taygeta. green24 (24TB exFAT) mounted. Genomics done, heartbeat live, sol monitors killed.
- NEXT: When last 2 models land: run S2V test render (copy a MoMA portrait to tay + short TTS audio, native Wan2.2 S2V API workflow) -> verify lipsynced mp4. Optional: pip install onnx to enable FantasyPortrait. Then Docker-for-users (Mike/Liz, 33% ceilings) - AWAIT Max answer on their container purpose + login method.

## [2026-07-16 10:04] ? 8941679b
- DID: S2V END-TO-END RENDER WORKING on taygeta: built native ComfyUI Wan2.2 S2V API workflow (UNETLoader fp8 + CLIPLoader umt5 wan + VAELoader + AudioEncoderLoader/Encode wav2vec2 + WanSoundImageToVideo + KSampler uni_pc/simple + VAEDecode + CreateVideo + SaveVideo). Inputs: moma plate portrait + espeak-ng speech.wav. Render RUNNING: WAN22_S2V loaded fp8, sampling ~15s/step, 13GB/16GB, GPU 100%, no OOM. prompt_id c615e361. Script: ~/setup/scripts/s2v_fire.py.
- STATE: Render in progress (480x480x49f, 20 steps ~5min). ComfyUI headless on :8188. Tailscale installed but NOT yet authed (Max must click login URL).
- NEXT: Collect finished mp4 from ~/ComfyUI/output, copy to /mnt/green24, verify it is a real lipsynced video. Then Docker containers (Mike/Liz, Tailscale remote, SSH keys, 33% ceilings). Register $99 plan.

## [2026-07-16 10:16] ? 8941679b
- DID: S2V PIPELINE PROVEN on taygeta: first render output s2v_test_00001_.mp4 verified real - h264 480x480 49 frames 3.06s + AAC audio embedded (lipsynced talking clip). Saved to /mnt/green24/s2v_tests/, fetched to Pine, sent to Max. Full image+audio+prompt->lipsync working on RTX 5060 Ti 16GB (13GB used, no OOM, ~15s/step).
- STATE: Wan 2.2 S2V fully operational. ComfyUI headless :8188. Tailscale installed but STILL logged out - Max hasn't clicked auth URL (https://login.tailscale.com/a/16b7e2f018827).
- NEXT: BLOCKED on Docker containers until Max auths Tailscale. Then build Mike/Liz containers (GPU, sshd, 33% ceilings, homes on green24, reachable over tailnet). Register $99 plan. Optionally test longer/higher-res S2V render + real TTS voice.

## [2026-07-17 17:34] ? 8941679b
- DID: Updated ALL docs for Taygeta setup: created canonical C:\claude_base\tools\taygeta\taygeta_setup_20260716_v01_tomemex.md (auto-syncs Memex); added Taygeta to global_CLAUDE.md MACHINES; updated infra_map (taygeta heartbeat + sol monitors retired); green24 in drives_registry; tay synonym in user_dictionary; global2 Taygeta section; Notion Servers page (id 2ee0316f...5161) new Taygeta section.
- STATE: Docs complete. Taygeta fully operational: S2V proven, genomics, heartbeat, green24, hardened. Tailscale installed, auth PENDING - Max authorized me to do it via Playwright+Bitwarden (tailnet rempel house = GitHub SSO, user maxrempel).
- NEXT: Resume: authorize Taygeta onto tailnet via Playwright+Bitwarden (GitHub SSO login), then build Mike/Liz Docker containers. Register $99 protection plan. Optionally render a quality S2V sample.
