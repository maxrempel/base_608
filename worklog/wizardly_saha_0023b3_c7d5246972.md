
## [2026-07-02 11:56] ? 68a1ff04
- DID: typer.py: switched upload format from lossy MP3 (~40kbps, Max heard+rejected it) to FLAC lossless; moved _last_sample debug out of repo into temp; warm clip -> FLAC. Committed master 4a8a462a, pushed.
- STATE: FLAC verified round-trip in venv (libsndfile 1.2.2); measured real 13s clip WAV 427KB->FLAC 233KB vs MP3 71KB so speed win kept, lossless quality restored. Live instance STILL on old MP3 code (recreates _last_sample.mp3 each dictation) - needs restart.
- NEXT: Offer Max a restart of the 3 hidden typer instances to make FLAC live; keep scanning current typer for further bugs if asked.

## [2026-07-02 12:40] ? 68a1ff04
- DID: DIAGNOSED typer slowness (finder role). Root cause is NOT the typer code: it's NETWORK. Measured TCP+TLS connect latency from Pine: Cloudflare 1.1.1.1 avg 2331ms (0.7-6s), google 3142ms, api.groq 1435-2900ms - should all be <200ms. Log confirms round-trips are length-INDEPENDENT (58s clip=1.1s, 15s clip=14s) and slow on BOTH OpenAI(am) and Groq(pm), so format/provider/model are irrelevant.
- STATE: Home residential internet is congested/degraded - every cloud transcription call pays multi-second connection latency = the 5-10s Max sees. Likely shared-uplink saturation (fleet uploads: ytdow/Odysee) OR ISP/Wi-Fi issue. Needs a network check, not a code change. MP3 vs FLAC is irrelevant to speed - Max was right.
- NEXT: Report to Max; suggest to E25B: (1) verify what's saturating the home uplink / check router-Wi-Fi/ISP, (2) code mitigation = keep ONE keep-alive HTTPS connection warm (ping ~10s not 20s) to skip the 1-5s TCP+TLS setup per call. NOT fixing - finder role.
