# Genomics computation pause

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Max ordered all genomics computation paused because the current token budget was exhausted. Taygeta infrastructure testing is the sole exception.

## UPDATE 2026-08-05: pause lifted for downloads only

Max explicitly lifted the pause for the resumable family downloads in his
2026-08-05 instruction (takeover session): "go ahead and build the system for
resumable downloads ... the priority is to get complete families." The
authorized scope is downloading and checksum-accepting public 1000 Genomes
CRAM/CRAI inputs through the new control system at
`paper_repro/deployment/aluya5_family_stream_v01/downloads_control_v01/`
(deployed to Green 24 under `aluya5_pilot_v01/code/downloads_control_v01`).
Production analysis, atlas ingestion, Ben, and all other genomics compute
remain paused or gated by their own owners (Verigen) until Max lifts them
separately. Partials and accepted inputs remain preserved and are never
deleted or restarted from zero.

Observed and acted state:

- Asto: stopped the exact transient service `aluya5-source-recovery-pel016-hg01941-asto-v01.service` and its surviving curl child. The resumable HG01941 CRAM partial is preserved at exactly 7,521,157,120 bytes. It remained unchanged across repeated checks. No active genomics service, process, timer, or cron entry remained after the stop.
- Asto: terminated five stale, noncomputing genomics diagnostic shell groups that had been waiting for hours. No data were deleted or modified by this cleanup.
- Taygeta: no active genomics service or process was found. No testing process, service, mount, or data was changed.
- Pine, Lakarian, and Dax: no active genomics computation was found. No matching automatic restart task was found on Pine.
- Asto fleet state is `waiting`, with task `Genomics paused by Max` and the token-budget intermission recorded as the reason.

Resume rule: do not restart genomics downloads, recovery, analysis, or production until Max explicitly lifts this pause. Preserve all partials, inputs, outputs, markers, logs, and scientific evidence. Taygeta infrastructure testing may continue independently.

### Dated exception 2026-08-05: 1KGP long-read trio downloads only

Max explicitly commanded a resumable download system for complete 1000 Genomes
Project long-read trios (research handover and spec in
`projects/1kgp_longread_trios/HANDOVER_START_HERE_v01_tomemex.md`). This lifts
the pause for that project only: the next session may build the downloader and
run the 13-family queue, storing data on Green24. Every other genomics download,
recovery, analysis, or production run still requires Max to lift the pause.
