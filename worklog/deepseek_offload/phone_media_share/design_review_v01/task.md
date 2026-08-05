# Phone media share design review

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

Review this proposed Windows/Pine workflow and return a concise implementation checklist plus security and compatibility pitfalls. Do not write files.

Goal: Max produces videos under 2 GB on Windows Pine and wants to listen from a phone on the same Wi-Fi without waiting for Nextcloud.

Proposed design:
- A Python standard-library HTTP server bound only to Pine's private IPv4 address.
- It serves exactly one selected media file, not a directory.
- A fresh random URL token is required.
- HTTP byte-range support enables seeking on Android/iPhone.
- A small local landing page offers playback and download.
- A PowerShell launcher optionally uses FFmpeg to create a 64 kbps AAC `.m4a` listening copy, then starts the hidden server.
- Windows Firewall allows inbound TCP only on Private network profile and only for the chosen port.
- Output tells the agent a phone URL and estimated size/time savings.
- Stop script and PID/state file make shutdown deterministic.
- Skill instructions must work for both Codex and Anthropic Claude Desktop and must never expose the server to the public Internet.

Assess correctness, especially Windows firewall handling, dual Ethernet/Wi-Fi addresses, token leakage, process hiding, byte-range semantics, and a reliable automated test plan.
