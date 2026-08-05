# Lesson 1 archive, cleanup, and quality-control review, version 01

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

## Outcome

The published Lesson 1 master and its synchronized voice-only source assembly
are preserved both at their original locations and in the Centauri RAID archive.
The complete rebuild package, provenance, quality-control records, approved music
map, exact music bed, title cards, and trumpet source are also in the RAID
archive. The reusable synchronization-safe assembly toolkit is committed and
pushed to the MOMA GitHub repository.

All selected superseded Lesson 1 builds and scratch directories have disappeared
from their original paths. The Windows Recycle Bin has **not** been emptied.

## Canonical retained media

### Published master

- Archive path: `D:\media_archive\MOMA\telepathy_series\lesson_01\masters\lesson1_COMPLETE_v123_20260731_231644.mp4`
- Bytes: `1,468,579,909`
- SHA-256: `5ae4c6eae7dba87aeba1859a5c60aa052269b7fbded31749210a2e2b4e98683d`
- Video: H.264, 1280 by 720, 30 frames per second, 29,368 frames
- Duration: 981.153255 seconds
- Default audio: mixed voice and music, AAC 44.1 kHz
- Reference audio: original unbroken source audio, AAC 44.1 kHz, delayed by exactly 3.5 seconds and retained as the non-default second audio stream

### Synchronized source assembly

- Archive path: `D:\media_archive\MOMA\telepathy_series\lesson_01\source_assemblies\mixboard_assembly_scene305_20260730_142710.mp4`
- Bytes: `1,437,128,091`
- SHA-256: `5a63872d5e40441038b8e680085fed088bb0ec717e1f683521736421af91ffda`
- Video: H.264, 1280 by 720, 30 frames per second, 29,053 frames
- Duration: 970.653255 seconds
- Audio: original synchronized AAC 44.1 kHz stream

The local copies of both files were hashed again after cleanup and match these
RAID copies byte for byte.

## Rebuild package and reusable method

The RAID `rebuild_package` contains the exact full-length music bed, approved
version 10 map, trumpet source, both title-card PNG files, and lesson configuration.
The RAID `qc_records` contains the release record, failure analysis, stream
contract, and toolkit documentation.

The reusable toolkit is in the MOMA repository under
`sound_assembly/code/musicunder`. Its four Python scripts compile successfully,
its plan-only frame reconstruction produces `105 + 29053 + 210 = 29368` frames,
and its full automated quality control passes on the published master. Commit
`318a7959c28b80278fd0514ce8acbc0cd5193bbd` is present on the remote `master`
branch with no uncommitted toolkit changes.

## RAID verification

Centauri volume `D:` is the healthy 16 TB RAID volume. After archiving it has
10,229,529,403,392 bytes free. Every one of the 13 entries in the initial
`SHA256SUMS_v01.txt` manifest was rehashed on Centauri after cleanup: 13 passed,
0 failed.

## Recycle Bin audit

The reviewed cleanup manifest selected 41 top-level targets containing 764 files,
65,049,094,822 bytes (60.582 GiB). The move operation reported no errors and all
41 original paths are gone.

Recycle Bin metadata independently confirms 40 substantive top-level targets,
totaling 64,944,237,222 declared bytes. These remain recoverable until the bin is
emptied.

One 104,857,600-byte object does not have Recycle Bin metadata or a payload:
`lesson1_COMPLETE_preview_v12_20260731_135418.mp4-chunking-846533714-2-0`.
Its `.mp4-chunking-...` suffix identifies it as an incomplete Nextcloud transfer
chunk, not a valid video or unique source. Its original path is gone. This is the
only recoverability exception.

The C-drive Recycle Bin quota was temporarily increased from 26,424 MB to 90,000
MB so the retained intermediates would fit. After Max explicitly approves
emptying the Recycle Bin, restore the quota to 26,424 MB.

## Retained working locations

- The published master remains the only media file in the Lesson 1 `music_mix\out` folder.
- The synchronized source assembly remains on `G:`.
- The approved version 10 map remains beside the published master.
- The original trumpet track remains in the Suno music catalog.
- MOMA source assets and the committed reusable toolkit remain in place.

## Hold point

Do not empty the Windows Recycle Bin until Max gives a separate explicit command.

