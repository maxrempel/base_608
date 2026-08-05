# OMEGA GRCh37 v02 — Manager Verification Note

## Opening decision

**Do not open or execute the sealed 96-row v02.1 blind panel.** Stop for manager verification. Exact reconstruction remains unvalidated, and the exposed controls do not qualify the panel for opening.

## Compact evidence table

| Control | Verified result |
|---|---|
| Corrected runtime contract commit `83c7ac1f` | Independently verified. |
| Reference `hs37d5` compressed/decompressed/FAI | Exact registered hashes match. BAM SQ order matched 86/86. |
| Derived hg19 `genomicSuperDups` BED | Exact registered hash match; 39,747 rows. |
| Clean-region definition | No GIAB Tier1 detector mask; no third clean BED. Clean region remains local low-MAPQ fraction ≤ 40%. |
| Immutable wrapper | Binds frozen `omega_junction_v02.py` SHA `e42c5a68...`; discovery scripts and thresholds unchanged. |
| Synthetic exposed controls | 100-bp exact: 1/1. Corrected 5,000-bp: unresolved. No false exact calls in synthetic set. |
| Old exposed GIAB32 | v01 candidate 22/32, accepted 7/32. v02 candidate 22/32, accepted 9/32. v02 made 2 exact-length calls: 0 correct, 2 false exact. No retained prespecified exact-junction coordinate tolerance, so exact junction was not scored. |
| Protected exposed 3-real/3-sham panel | v01 and v02 both: 1/3 locus windows, 1/3 junction classes, 0/3 exact coordinate-plus-payload, 0/3 sham windows. |
| Repeated exposed coded smoke | PAF, v02 hit table, and payload hashes identical across two independent runs. |
| Resource control | First two service attempts killed by `systemd-oomd` because `MemoryHigh` was below mapper working set. Per-locus checkpoints preserved 22 units. Scoped 13/14 GiB retry completed remaining units with zero restarts, 11.2 GiB peak, zero swap, and no storage/kernel faults. |

## Interpretation

v02 shows a modest accepted-call improvement in the old exposed GIAB32 control (7/32 → 9/32) and reproducible outputs across independent runs. The resource failure is traceable to memory bound configuration and was successfully contained by checkpointing and a scoped retry.

However, the exposed regressions remain disqualifying for opening the sealed panel:

- v02 produced 2 false exact-length calls and 0 correct exact-length calls in the old exposed GIAB32 control; length claims are prohibited.
- Synthetic corrected 5,000-bp exact reconstruction remains unresolved.
- Protected exposed 3-real/3-sham performance is unchanged and low: 0/3 exact coordinate-plus-payload and 0/3 sham windows.
- Clean-region coverage remains limited to local low-MAPQ fraction ≤ 40%, with no GIAB Tier1 detector mask or third clean BED.
- These results are exposed engineering controls only, not the sealed 96-row v02.1 blind panel.

No biological claim, correction factor, threshold change, or code repair is supported by this record.

## Immutable identities / checksum note

All registered hash checks passed for the corrected runtime contract commit `83c7ac1f`, the frozen `omega_junction_v02.py` SHA `e42c5a68...`, `hs37d5` compressed/decompressed/FAI, and the derived hg19 `genomicSuperDups` BED. Exact registered hash values should be re-confirmed against the frozen registry if any later authorization is requested. BAM SQ order matched 86/86.

## Resource incident / repair note

The first two service attempts were killed by `systemd-oomd` because `MemoryHigh` was below the mapper working set. Per-locus checkpoints preserved 22 units. The scoped 13/14 GiB retry completed the remaining units with zero restarts, 11.2 GiB peak, zero swap, and no storage/kernel faults. The incident is isolated to memory bound sizing; no discovery-script or threshold change is in this record.

## Explicit stop / next authorization required

**Stop.** Do not open or execute the sealed 96-row v02.1 blind panel until manager verification is performed and explicit authorization is given for any further action. No next step is authorized by this note.
