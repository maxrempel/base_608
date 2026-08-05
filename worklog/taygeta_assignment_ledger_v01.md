# Taygeta and active science assignment ledger v01

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

## Standing assignments

1. Keep healthy scientific sessions running autonomously. Do not stop unrelated
   work because a drive is intermittently unreliable.
2. Treat Green24 faults as recoverable, exact-unit incidents. Preserve partial
   files, checkpoint before restarting an affected unit, and restart only the
   affected unit when safe.
3. Keep passive Taygeta telemetry active. Stop an exact unit only for direct
   evidence of data corruption, accumulating D-state, a new storage or kernel
   fault, or another measured machine-safety failure.
4. Taygeta identity must be verified before storage action: boot ID beginning
   `ffd06644-`, MAC `9c:6b:00:ae:44:0d`, and Green24 serial
   `00000000NT17WFMN`.
5. PEL016 child recovery is narrowly held to Green24. Its partial file stays
   preserved. The healthy Asto/Purple4 path is the active bypass; do not delete
   or restart from zero.
6. Do not use Xeno or AWS. Keep deterministic work on Asto and Taygeta within
   their machine ceilings.
7. Use email and Telegram for operational alerts. Use Android Vocalizer only
   for urgent daytime alerts when Max is away from the computer.

## Reread schedule

- First 24 hours: reread this ledger every three hours.
- After 24 hours: reread it once daily.
- At each reread, compare active services, holds, bypasses, and checkpoint
  state against this ledger. Record only material drift or corrections.

## 2026-08-05: new assignment - 1KGP long-read trio downloads

Max assigned the next session to build and run a resumable downloader for the 13
complete long-read trios in the 1000 Genomes Project, two families at a time,
highest quality first, with verified artifacts. Entry point:
`projects/1kgp_longread_trios/HANDOVER_START_HERE_v01_tomemex.md` (manifest and
spec beside it). Scope: downloads only; data and state on Green24
(`/mnt/green24/1kgp_longread_trios/`); software and docs on Taygeta plus GitHub.
Genomics pause remains in force for everything else (see the dated exception in
`worklog/genomics_pause_20260803_v01.md`).
