# Scribe handover - milestone 2 (~156K tokens)
# session: 20260804_uizzical_chatelet_53cd96_03ec0d78
# cwd: C:\claude_base\.claude\worktrees\quizzical-chatelet-53cd96
# written: 2026-08-04 15:54:14 by deepseek-v4-pro

# Handover: Gaming Desktop Replacement Search

## GOAL (in Max's own words)
"I made a fork here, and your task is to search whether something better showed up in searches. Quick delivery, same price, better parameters, better specs, and better reliability. And the graphics card, I don't know if I need the graphics card that bad. I think I do. Yeah, graphics card is negotiable. I request that you do the wide search: Walmart, Costco, Best Buy, major sellers, Amazon, even eBay, but should be new and good manufacturer with good reputation."

The context is replacing a defective CyberPowerPC gaming desktop (nicknamed "Taygeta") purchased from Walmart. The old machine has memory faults and must be returned within a tight 30?day window (deadline likely Aug 12?14, 2026). Max wants to buy a new machine that arrives before returning the old one, with zero downtime. He also needs a full backup of the old system first.

## DECISIONS + WHY
1. **Graphics card is necessary.** The workload is local AI lipsync rendering (Wan 2.2 S2V in ComfyUI). 16 GB VRAM is the practical floor; dropping the GPU would force everything onto paid cloud rendering. No 24 GB cards are available under $3,000, and the RTX 50 Super refresh is delayed to late 2026. Verdict: keep a 16 GB card.
2. **Nothing at the same price beats the old config.** Searched Walmart, Best Buy, Amazon, eBay. In the $1,830-2,100 range, you either get no?name brands with single?digit reviews or downgrades to 12 GB cards. The original specs (Ryzen 9 9900X, RTX 5060 Ti 16 GB, 32 GB DDR5, 2 TB NVMe) were genuinely good value.
3. **The only sensible upgrade is the Costco MSI Aegis ZS2** at $2,699.99 (item 1927586, sale ends Aug 9). It offers the same 12?core CPU, but an RTX 5080 16 GB (double the render throughput), same RAM/storage, 850W Gold PSU, 360 mm liquid cooling. It has a 90?day return window and 2?year warranty-far safer than Walmart's 30 days plus one year. It is in stock at the SE San Diego warehouse, solving the delivery race.
4. **Middle ground (RTX 5070 Ti systems) is dead.** Those cost $2,349-2,750 at Best Buy and Walmart, nearly as much as the 5080 system but with less GPU power and worse return terms.

## CURRENT STATE
- The old Taygeta desktop (Walmart) is still running; memory errors were identified. It is within the 30?day return window (ordered Jul 13, delivered Jul 15). The exact "return by" date is not yet pulled from the Walmart account.
- Market search completed across five major retailers + eBay. Results collated and presented in the last assistant turn.
- No new purchase has been made.
- No backup has been performed yet.
- The current recommendation is to buy the Costco MSI Aegis (pick up locally) before the Aug 9 price cut ends, then return the old PC.

## EXACT NEXT STEP
1. Max must decide whether to accept the Costco step?up ($2,700) or stick with a direct replacement (which offers no better value and still carries the 30?day return risk).
2. If yes, call Costco SE San Diego to confirm in?store price and availability for item 1927586, then buy and pick up.
3. Once the new machine is in hand and verified:
   - **Back up the old Taygeta** (the session mentions a USB disk and a prior backup plan-full system image or critical files from the Ubuntu installation, plus any genomics data and SSH keys).
   - **Wipe the old machine** (Ubuntu install, sensitive data).
   - **Return the old machine** to Walmart (with original packaging, all accessories, and the $99 Protection Plan, which is refundable within 30 days).
4. Restore backup onto the new machine.

If Max prefers not to spend $2,700, the fallback is to repurchase the same CyberPowerPC from Walmart and hope the replacement is not a lemon, but the 30?day clock restarts and the original problem (no time buffer for returns) remains.

## OPEN QUESTIONS
- Does Max want to go with the Costco option, or stay in the ~$1,850 budget? (The cost difference is ~$870.)
- Should we pull the exact "Return by" date from his Walmart account? (Requires him to indicate which of the three connected Chrome instances has his logged?in session.)
- Does he have the USB backup disk ready, and is a complete system image (e.g., Clonezilla) preferred over file?level backup? The backup method was not yet discussed.

## KEY PATHS/IDS
- Old machine: CyberPowerPC Taygeta, Walmart order, total $2,070.81, Ryzen 9 9900X, RTX 5060 Ti 16 GB, 32 GB RAM, 2 TB SSD.
- Costco option: MSI Aegis ZS2, item 1927586, URL: https://www.costco.com/msi-aegis-gaming-desktop---amd-ryzen-9-9900x---geforce-rtx-5080---windows-11-home---32gb-ram---2tb-ssd.product.4000355760.html
- SE San Diego Costco warehouse (physical pickup).
- Walmart return policy page: https://www.walmart.com/help/article/walmart-standard-return-policy/adc0dfb692954e67a4de206fb8d9e03a
- The user's Gmail has Walmart purchase and delivery confirmation emails (used to extract dates).

## GOTCHAS
- **Walmart 30?day return on PCs.** The normal 90?day policy does not apply. The deadline is likely Aug 12-14. Overlapping the new machine too tightly risks forfeiting the refund if the new one is delayed. The recommended drop?dead date to hand over the old one is Aug 10.
- **Costco sale expires Aug 9.** The price may rise after that.
- **Costco warehouse pricing may differ** from online; call ahead.
- **Backup must happen before any wipe.** The old machine contains a functional Ubuntu install, ComfyUI setup, and genomics data. Losing that without a verified full backup would be catastrophic.
- **All accessories and original packaging** must go back to Walmart (including the protection plan) for a full refund.
- **Fallback if return window missed:** CyberPowerPC warranty covers defect repair, but that would be a repair, not a refund. The goal is refund, so hitting the window is critical.

No other dead ends or ruled?out paths exist; all major retailers were checked and only Costco offered a genuine upgrade with better protection.
