# Scribe handover - milestone 4 (~301K tokens)
# session: 20260804_uizzical_chatelet_53cd96_03ec0d78
# cwd: C:\claude_base\.claude\worktrees\quizzical-chatelet-53cd96
# written: 2026-08-04 17:51:22 by deepseek-v4-pro

# HANDOVER - Taygeta Replacement & Backup

---

## GOAL (in Max's words)

Max discovered memory faults in the new Taygeta computer (CyberPowerPC from Walmart) and decided to return it. He bought a replacement (Dell Tower from Costco, now called "Taygeta 2") and needs to back up the old machine fully before returning it, then restore onto the new one - or reinstall from scratch with a captured inventory if the cross-vendor migration fails. He also wants the USB rescue stick's SSH autorun code backed up and properly documented.

---

## DECISIONS + WHY

**1. Return the CyberPowerPC to Walmart, not repair it.**
- Walmart's return window for PCs is **30 days** (not 90). The machine was ordered Jul 13, delivered Jul 15. Deadline is **Aug 12**. Very tight.
- The $99 Allstate protection plan is also 30-day refundable and comes back with the machine. Worth confirming it actually lands.
- Fallback: if the window is missed, CyberPowerPC's own warranty would cover a repair/RMA (memory faults are a defect), but that's a repair, not a refund.

**2. Don't buy the same brand again.**
- CyberPowerPC has a 22% one-star rate on Trustpilot (bimodal: mostly 5-star or 1-star, almost nothing in between). Signature of a quality-control problem, not a design issue. Max landed in the bad 22%.
- The memory faults were probably not cosmic bad luck - the brand is just spotty.

**3. Downgrade the graphics card - it's not being used.**
- Max tried local video generation (Wan 2.2 S2V lipsync in ComfyUI) and it produced garbage. Possibly workflow settings, possibly the model is too large for 16GB VRAM.
- Either way, the 5060 Ti 16GB isn't delivering value. A cheaper RTX 5060 (8GB) is enough for Whisper and voice synthesis, which are the only GPU workloads actually used.
- Max explicitly ruled out an upgrade ($2,700 Costco MSI Aegis with RTX 5080) - "that's just not a question."

**4. Buy a Dell Tower from Costco - CPU slightly slower but everything else is better value.**
- **Dell Tower Desktop, item 1951491, $1,299.99** (after $500 off, promo runs to Aug 16).
- **Core Ultra 7 265F** (20 cores, 20 threads, but 12 of those are efficiency cores). Benchmarks about **10% slower** than the Ryzen 9 9900X in multithreaded genomics work. That's the real trade.
- **32GB RAM** (single stick - weak, but fixable with a second stick for ~$100).
- **1TB SSD** (half the old 2TB - also fixable with a $120 add-on drive).
- **RTX 5060 8GB** - enough for Whisper/voice synthesis.
- **90-day returns, 2-year warranty** (vs Walmart's 30 days / 1 year).
- No other machine in this price band kept the big CPU and storage without welding a $1,000+ GPU to it. The config Max wants (strong CPU, big storage, weak graphics) is a workstation config and simply isn't sold as a prebuilt.

**5. Add parts to fix the Dell's weaknesses:**
- A second 32GB DDR5 stick (~$100) - the Dell ships with one stick, halving memory bandwidth. Adding a second stick gives 64GB and full dual-channel bandwidth. The board has an empty slot.
- A 2TB NVMe drive (~$120) - solves the 1TB restore constraint and the genomics scratch-space need.
- **All in: roughly $1,520** vs the $2,070 paid for the CyberPowerPC. About $550 back, with double the RAM, more total storage, better warranty, and a tier-1 brand.
- Exact part numbers to be confirmed once the Dell is physically here (avoid guessing and returning wrong parts).

**6. Full disk image PLUS an inventory kit before returning the old machine.**
- The old box is AMD Ryzen 9 9900X. The new one is Intel Core Ultra 7 265F. That's a cross-vendor migration.
- A disk image *may* boot directly (Linux detects hardware at boot), but it's not guaranteed. Three known failure modes: processor microcode, boot image (initramfs) lacking Intel chipset drivers, and network interface renaming.
- So the plan became: **don't bet on the image booting. Instead, capture a full inventory of everything installed on Taygeta, then reinstall Ubuntu fresh on the Dell using unattended install and restore from the inventory.** The inventory is the real safety net - if it's captured before the old machine goes back, nothing is lost.

**7. Use the existing SystemRescue SSH stick (identified as a 1.9GB "General UDisk").**
- It was built April 12 during a previous session ("Sol Rescue Handover"). The clever part: it uses **SystemRescue** (Arch-based), not Ubuntu. SystemRescue has a writable data partition and a built-in autorun mechanism, so the entire SSH customization is one 638-byte script (`autorun0`) sitting on the stick. Ubuntu's live image is read-only, which is why the original Ubuntu plan failed and cost three days.
- The autorun script: kills the firewall, drops Max's SSH public key into root's account, starts the SSH server, prints the machine's IP address.
- Both halves of the key pair are intact - private key on Pine, public key on the stick, with a backup copy in Nextcloud.

**8. The McAfee and Microsoft 365 bundle items.**
- Auto-attached by Costco at $0.01 each and discounted back to zero. Can't remove them from the cart.
- The fix: **never redeem the codes.** An unredeemed license key isn't a subscription - no account, no card on file, nothing to renew. Delete the emails and they're inert.

**9. Skip the Allstate protection plan for the Dell.**
- Costco already gives 2 years of warranty free. Allstate would only add accidental damage (useless for a tower that sits on the floor) and a third year (when the machine is worth ~$500). Not worth it.

---

## CURRENT STATE

**Purchased and ordered:**
- **Costco order #1304543892**, placed Tue Aug 4, confirmed. $1,299.99 + $14.99 shipping + $101.91 tax = **$1,416.89 total**.
- Dell Tower Desktop, item 1951491: Core Ultra 7 265F, RTX 5060, 32GB, 1TB, Windows 11 Home.
- Shipping: standard (3-5 business days). Estimated arrival: **Aug 7 (earliest) to Aug 11 (latest)**.
- Confirmation email sent to max.rempel2@gmail.com.
- No specific delivery date yet - Costco doesn't commit until the shipping confirmation email.

**Calendar entries added:**
- Fri Aug 7: delivery window opens
- Tue Aug 11: delivery window closes (last day of the window; if no shipment by then, chase Costco). Also: **all-day event to return Taygeta to Walmart**.
- Mon Aug 10: "TOMORROW: return Taygeta to Walmart, prep today" - verify image and fallback kit, wipe drives, box with accessories.
- Wed Aug 12: last day to return CyberPowerPC (backstop deadline, $2,070.81 at stake)

**Identified and documented:**
- **USB rescue stick**: 1.9GB "General UDisk", SystemRescue with autorun0 SSH config dated 2026-04-12. Works by killing firewall, dropping Max's key, starting SSH, printing IP. Both key halves verified present.
- **Stick m4**: ASolid 7.5GB, full Ubuntu Server 24.04 installer. Intact.
- **Stick s3**: SanDisk Cruzer Glide 14.6GB, actually Debian Live (not Ubuntu as previously thought).
- **Three blank sticks** available for overwriting: a 3.8GB "General UDisk" and two 1.9GB "General UDisk" sticks (one is the rescue stick, the other is blank).
- Plus a Memorex 57.8GB (HP recovery drive, not ours) and a SanDisk Cruzer Blade 3.7GB (unreadable from Windows, contents unknown).
- Full stick registry written: `C:\claude_base\tools\taygeta\usb_stick_registry_20260804_v01_tomemex.md`

**Backed up to git (master, commit 34b7c2d3):**
- `tools/usb_rescue_ssh/autorun0_systemrescue_20260412_v01.sh` - the 638-byte script verbatim
- `tools/usb_rescue_ssh/README_usb_rescue_ssh_tomemex.md` - full explanation of how it works, where both key halves are, how to refresh for new hardware
- `tools/taygeta/taygeta_replacement_20260804_v01_tomemex.md` - full order record, specs, side-by-side comparison, upgrade parts, checklist
- `tools/taygeta/usb_stick_registry_20260804_v01_tomemex.md` - all seven sticks identified

**In flight - Taygeta inventory script:**
- A comprehensive inventory script was deployed and launched **detached** (via `nohup setsid`) on Taygeta at 192.168.1.142.
- It's capturing: installed packages, NVIDIA and CUDA versions, every Python and conda environment, ComfyUI location and custom nodes, cron jobs, systemd units, network config, mounts, SSH keys, and a full `/etc` archive.
- **The result needs to be pulled off Taygeta onto Pine plus a second location, and verified complete before Taygeta goes back.**

---

## EXACT NEXT STEP

**When Max returns from his break (1-4 hours):**

1. **Stick labeling session.** Max pulls USB sticks out of Taygeta one by one. Claude identifies each against the registry and updates labels. Three sticks are currently blank/unlabeled and need physical labels matched to the registry.

2. **Check the Taygeta inventory job.** It was launched detached. Needs to be checked for completion, then the output pulled to Pine and to a second location (Nextcloud or similar). Verify it's complete enough to rebuild from.

3. **Finalize the restore/rebuild plan for the Dell.** Two tracks:
   - **Track A (optimistic):** prepare the disk image with pre-emptive fixes (Intel microcode, broad initramfs, network config) so it might just boot on the Dell.
   - **Track B (pragmatic):** prepare an unattended Ubuntu Server install on stick m4 (or a fresh stick) that auto-partitions, sets up Max's user, and comes up with SSH. Then restore everything from the inventory over the network.
   - Given Max's preference ("just reinstall everything"), **Track B is primary. Track A is a nice-to-have if the image happens to boot.**

4. **When the Dell arrives:** disable Secure Boot in firmware, boot from the installer, let unattended install run, SSH in, restore from inventory.

5. **Before Aug 11, on the old Taygeta:** pull the inventory (if not already done), optionally take a disk image, wipe the drives, box it with all accessories.

6. **Aug 11:** return the CyberPowerPC to Walmart. Check that the $99 Allstate refund posts.

7. **After the Dell is running:** order the second 32GB RAM stick and 2TB NVMe drive (confirmed against the Dell's board).

---

## OPEN QUESTIONS (awaiting Max)

1. **Stick labeling.** Max said he'd pull sticks one by one so Claude can update the registry with physical labels. Still pending.

2. **Did the Taygeta inventory job finish?** Needs checking when Max is back.

3. **Which stick should be used for the unattended installer?** Three blank sticks are available. Or m4 (ASolid 7.5GB) could be repurposed - it's currently a plain Ubuntu Server 24.04 installer.

4. **Should we attempt the disk image at all, or just do inventory + fresh install?** Max seemed to prefer the fresh install route ("It should be automatic. You should be able to do that."), but the image is a nice fallback. Worth confirming.

5. **Does Max want the Dell's Windows 11 license key captured before wiping?** The machine ships with Windows 11 Home. If Ubuntu is going on it immediately, the license key might be worth saving in case of resale or dual-boot later.

6. **The old Taygeta has a 24TB external drive ("green24").** Confirmed it just plugs into the new box - nothing to restore there. But worth confirming it's physically accounted for.

---

## KEY PATHS / IDs / COMMANDS

**Order:**
- Costco order #1304543892
- Item 1951491 (Dell Tower Desktop)
- $1,416.89 total, Visa ending 6391
- max.rempel2@gmail.com, membership 111917523210

**Machines:**
- **Taygeta (old):** CyberPowerPC Gamer Supreme, Ryzen 9 9900X, RTX 5060 Ti 16GB, 32GB, 2TB. IP: 192.168.1.142. SSH key: `~/.ssh/sol_key` on Pine. User/pw: maxre / T2w3e4r5t6y= (from shared_logins_frequent.txt line 280-292). Ordered Jul 13, delivered Jul 15. $2,070.81 with Allstate plan.
- **Taygeta 2 (new):** Dell Tower Desktop, Core Ultra 7 265F, RTX 5060 8GB, 32GB (1 stick), 1TB. Arriving Aug 7-11.
- **Pine:** the current Claude host machine (Windows + WSL). SSH private key at `~/.ssh/sol_key` and `C:\Users\maxre\Nextcloud\zSyncMain\ssh\`.

**USB sticks:**
- Rescue stick: 1.9GB "General UDisk", SystemRescue, autorun0 at `/mnt/srdata/autorun/autorun0` (when mounted on Taygeta)
- m4: ASolid 7.5GB, Ubuntu Server 24.04 installer
- s3: SanDisk Cruzer Glide 14.6GB, Debian Live
- Three blank sticks: 3.8GB "General UDisk", two 1.9GB "General UDisk" (one is the rescue stick, other is blank)
- Registry: `C:\claude_base\tools\taygeta\usb_stick_registry_20260804_v01_tomemex.md`

**SSH autorun code:**
- Script: `C:\claude_base\tools\usb_rescue_ssh\autorun0_systemrescue_20260412_v01.sh`
- Docs: `C:\claude_base\tools\usb_rescue_ssh\README_usb_rescue_ssh_tomemex.md`
- Private key (Pine): `~/.ssh/sol_key` and Nextcloud backup
- Public key: on the stick, dropped into root's authorized_keys

**Taygeta replacement doc:**
- `C:\claude_base\tools\taygeta\taygeta_replacement_20260804_v01_tomemex.md`

**Inventory script:** deployed to `/tmp/taygeta_inventory_v01.sh` on Taygeta, launched with `nohup setsid`. Output expected at `/tmp/taygeta_inventory_*.tar.gz` or similar. Log at `/tmp/inv_nohup.log`.

**Walmart return:**
- 30-day window for PCs and PC components
- Deadline: Aug 12 (from purchase) or Aug 14 (from delivery) - Walmart's purchase history shows the exact "return by" date
- Original box and all accessories required
- Allstate plan refunds with the machine

---

## GOTCHAS

1. **The 30-day return window is very tight.** Standard shipping puts the Dell at Aug 7-11. The return deadline is Aug 12. The worst-case scenario is only one day of overlap. **The inventory capture is independent of the Dell's arrival** - once it's done, the old machine can be returned even if the Dell hasn't shown up yet.

2. **Don't format any USB sticks when Windows offers.** Windows can't read Linux partitions and will offer to "format" them. Cancel every time. Formatting destroys the data.

3. **Sticks can't be read from Pine.** Windows/WSL can't attach USB flash drives. They must be read on a Linux machine - Taygeta was available for this before it goes back, but after Aug 11, a different Linux box (or the new Dell, or a live USB boot) will be needed.

4. **Cross-vendor migration (AMD to Intel) is not trivial.** A disk image may not boot. Three known problems: microcode, initramfs, network interface naming. The inventory + fresh install route is safer than betting on the image.

5. **The Dell ships with one RAM stick.** Single-channel memory at half bandwidth - hurts genomics throughput. Fix requires a matching second stick.

6. **The Dell has only 1TB storage.** If Taygeta's system drive is more than 1TB full, a disk image won't restore onto the Dell anyway. Another reason to go inventory + fresh install.

7. **McAfee and Microsoft 365 bundle items.** Don't redeem the codes - they'll auto-renew in a year. Just delete the emails.

8. **The $500 Costco discount expires Aug 16.** Order was placed in time, but worth knowing in case of cancellation/reorder.

9. **The external 24TB drive ("green24") is safe.** It's external, not part of the system restore. Just plugs into the new machine.

10. **SystemRescue stick is from April 2026.** Its kernel may not recognize
