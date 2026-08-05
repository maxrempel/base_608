
## [2026-07-26 13:28] ? 387e881d
- DID: Promoted Tayscribe to main Numpad+ key on Taygeta GPU (large-v3 cuda/float16); fixed missing cuBLAS/cuDNN via venv install + systemd LD_LIBRARY_PATH drop-in
- STATE: LIVE and confirmed by Max: + key ~0.4s/clip, Russian stays Russian, English stays English, mixed dictation correct. Cloud clamp fallback on Num6. Committed to master (1e79e967).
- NEXT: Clipboard-history pollution fix (player2 get_selection Ctrl+C without history-exclusion) still queued pending Max go-ahead

## [2026-07-26 14:24] ? 387e881d
- DID: Added vertical left-edge VU bars on every monitor (meter_e25c.py _draw_v/_draw_processing_v via _build_bar); made deploy_stt_server.sh GPU-aware; wrote tayscribe_gpu_setup_v01_tomemex.md; committed to master 12f8a648
- STATE: Idle-safe typer restart queued (bg bwrw5tf43) to load bars; Tayscribe live on Numpad+ GPU, confirmed by Max in RU+EN
- NEXT: Clipboard-history pollution fix (player2 Ctrl+C without exclusion) still queued pending Max go-ahead

## [2026-07-27 14:15] ? 387e881d
- DID: Added stutter guard (no_repeat_ngram_size=3 etc, deployed live to Taygeta) + automatic GPU-busy failover: + key probes Taygeta /health, routes to asto (same RU/EN method, no translation) when a render loads the GPU. Committed 018f1ff3
- STATE: Server live on Taygeta (health reports gpu_busy/gpu_util, probe HTTP200). Client failover loads on idle-safe restart (bg bs8u89coc)
- NEXT: Clipboard-history pollution fix (player2) still queued pending Max

## [2026-07-28 11:05] ? 387e881d
- DID: Diagnosed the 'six-digit number typed into Codex window' bug: paste_via_clipboard (typer_e25c.py ~1686) sets clipboard, Ctrl+V, waits settle (floor 0.30s), then RESTORES prev clipboard. A slow/async terminal (Codex) consumes the paste AFTER the restore, so it pastes prev (a 6-digit number) not the dictation. Logs confirm transcription+paste 'ok'; only the restore race is at fault.
- STATE: Root cause found, NOT yet fixed (Max asked 'why' = question). Fix options offered: (A) much longer settle floor, or (B) stop restoring prev clipboard entirely (bulletproof, but replaces prior clipboard with last dictation). Awaiting Max's pick.
- NEXT: Also still queued: player2 clipboard-history pollution fix
