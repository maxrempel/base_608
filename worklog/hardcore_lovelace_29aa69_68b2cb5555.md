
## [2026-06-15 15:39] b11r 6a399a4a
- DID: B11R researched the all-4-sticks-crash mystery
- STATE: Root cause = 2 DIMMs/channel overload: 4x dual-rank 16GB = 8 ranks, max electrical load on i7-9700 memory controller; each stick clean solo, crashes at 64GB. NOT a dead stick. Confirmed common DDR4 problem + M720s specs.
- NEXT: Fix options: lower RAM speed in BIOS (2666->2133) OR run 2-3 sticks. Check if Lenovo M720s BIOS exposes memory speed setting.

## [2026-06-15 16:04] b11r 6a399a4a
- DID: BIOS path checked on Sol M720s - DEAD END
- STATE: Max entered BIOS, NO memory speed/DRAM/frequency setting anywhere (Lenovo business BIOS locked, as predicted). Cannot lower RAM speed in BIOS. Root cause stands: 4 dual-rank DIMMs overload IMC, heat-triggered.
- NEXT: Two real fixes left: (1) FAN TEST - open box, fan on RAM, re-run 64GB soak that crashed; if survives heat confirmed + cheap fix keeps 64GB. (2) Run 2-3 sticks (32/48GB) = guaranteed stable, idle Sol needs little.
