---
Pine hard crash -- 2026-04-13 12:29 PM
---

## What happened

Pine (Dell Precision 7560) froze completely and rebooted. First time this has ever happened. Max had not restarted it for a while before the crash. Possibly leftover from earlier Python work.

## Event log findings

- Event 41 (Kernel-Power): system rebooted without clean shutdown at 12:29 PM.
- Event 6008: confirmed unexpected shutdown.
- No BSOD minidump files -- not a blue-screen crash.
- No WHEA hardware errors -- no detected CPU/RAM/PCIe faults.
- Two "Active battery count change" events at reboot.
- RAM was fine (32 GB total, 20 GB free after restart).

## Likely cause

Best guess: GPU driver hang or a leaked Python process (possibly CUDA-related) that accumulated over time without restart. No signs of hardware degradation.

## Action

None taken. Monitoring only. If it repeats, investigate GPU driver version and thermal history.

---

## Second crash -- 2026-04-13 9:27:40 PM (~9 hours later)

Pine froze again. Event 41 + 6008 confirm another unclean reboot.

### New clues

- **Disk errors (Event 51) at 8:42:20 PM**, ~45 min before freeze: 10+ paging-operation errors on `\Device\Harddisk1\DR2`.
- Harddisk1 = Micron 2300 NVMe 1024GB, **BusType = USB** (external drive in an enclosure, plugged in recently by Max).
- Harddisk0 = internal WDC SN810 512GB (C:) -- no errors, healthy.
- Network miniport fatal error at 8:42:22 PM: Wi-Fi Direct Virtual Adapter failed power transition (same pattern also at 7:36 AM and 10:45 AM today without causing crashes).
- Both drives still report Healthy; no BSOD, no WHEA errors, no minidump.

### Interpretation

The USB-attached Micron drive briefly dropped off the bus. Because another chat session was using it via a virtualization passthrough (likely WSL or Hyper-V), kernel threads waiting on I/O to that drive hung, freezing the whole system. Hyper-V Event 129 at reboot confirms virtualization is active.

Caveat: the USB+WSL story cleanly explains crash #2 but NOT crash #1 at 12:29 PM (WSL was not yet involved then). Possibilities:
1. Two unrelated crashes same day.
2. The USB drive/enclosure itself is the common factor -- even without WSL, Windows indexing or scanning a flaky USB NVMe can stall I/O.

### Action

Still monitoring. If it repeats, suspect the USB enclosure/cable. Consider powered USB hub or moving work to internal drive.
