# Scribe handover - milestone 1 (~118K tokens)
# session: 20260804_uizzical_chatelet_53cd96_03ec0d78
# cwd: C:\claude_base\.claude\worktrees\quizzical-chatelet-53cd96
# written: 2026-08-04 15:43:51 by deepseek-v4-pro

# HANDOVER - Walmart Taygeta Computer Return

---

## GOAL (Max's own words)

Max has identified memory faults in the new Taygeta computer bought from Walmart. He wants to return it and buy a replacement. His plan: order the new one, and as soon as it arrives, return the old one - zero overlap, zero downtime. He also needs a full backup so he can reinstall painlessly. He has a USB disk for that somewhere. First priority: confirm the return is authorized.

---

## DECISIONS + WHY

1. **Return window is 30 days, not 90.** Walmart's standard policy gives 90 days for most items, but "PCs and PC Components" and "Consumer Electronics" are explicit 30-day exceptions. This was confirmed by fetching Walmart's own policy page (updated June 1, 2026). The $99 Walmart Protection Plan is also refundable within 30 days, so it comes back with the machine.

2. **Deadline is tight: roughly Aug 12-14, 2026.** The order was placed Mon Jul 13, delivered Wed Jul 15. The 30-day clock likely starts from purchase or delivery - Walmart's purchase history shows the exact "return by" date per item, which is authoritative. Either way, it's mid-August.

3. **The "return only after new one arrives" plan carries risk.** Last order took 2 days to deliver, so it *can* work, but if the replacement slips by even a week, a ~$2,000 refund is lost. Claude advised treating **Aug 10** as the drop-dead date, not the actual deadline. Do not plan to hand it over on the last day.

4. **Fallback if the return window is missed:** memory faults are a manufacturing defect, so CyberPowerPC's own warranty covers repair/RMA. But that's a repair, not a refund. The return is the preferred path.

5. **Two pre-return requirements identified:** wipe the drives (Ubuntu install, genomics data, SSH keys), and have the original box and all accessories. The backup must come first.

---

## CURRENT STATE

- **Return eligibility: CONFIRMED.** The Taygeta is returnable under the 30-day policy.
- **Exact "return by" date: NOT YET PULLED.** Claude offered to pull it from Max's Walmart account but noted three Chrome instances are connected and needs Max to specify which one.
- **Backup: NOT YET STARTED.** Max mentioned having a USB disk "somewhere." No backup has been created yet.
- **Replacement order: NOT YET PLACED.**
- **Wipe: NOT YET DONE.**

---

## EXACT NEXT STEP

Claude's last question to Max was: **"Want me to pull the exact 'Return by' date from your Walmart account? I can, but three Chromes are connected here and I'd need you to say which one."**

So the immediate next step is for Max to answer that question - which Chrome instance has his logged-in Walmart session - so Claude can navigate to the orders page and extract the authoritative return-by date.

After that, the logical sequence is:
1. Get the exact return-by date.
2. Order the replacement immediately.
3. Create a full backup before wiping.
4. Wipe the drives (Ubuntu, genomics data, SSH keys).
5. Return the old machine as soon as the new one arrives, respecting the drop-dead date of ~Aug 10.

---

## OPEN QUESTIONS (awaiting Max)

1. **Which Chrome instance** has the logged-in Walmart session? (Three are connected to Claude.)
2. **Where is the USB backup disk?** Max said "I have somewhere the key, I mean the USB disk for that."
3. **Replacement model:** Is Max buying the exact same Taygeta model, or a different one?
4. **Budget/price:** The original was $2,070.81 total. Is the replacement same price? Any concerns about price changes?

---

## KEY PATHS / IDs / NAMES

| Item | Detail |
|------|--------|
| **Computer** | "Taygeta" - sold by CyberPowerPC via Walmart |
| **Retailer** | Walmart (walmart.com) |
| **Order date** | Mon Jul 13, 2026 |
| **Delivery date** | Wed Jul 15, 2026 |
| **Order total** | $2,070.81 |
| **Add-on** | $99 Walmart Protection Plan (Allstate) |
| **Return window** | 30 days (PCs & PC Components exception) |
| **Estimated deadline** | Aug 12-14, 2026 |
| **Advised drop-dead date** | Aug 10, 2026 |
| **Walmart return policy URL** | `https://www.walmart.com/help/article/walmart-standard-return-policy/adc0dfb692954e67a4de206fb8d9e03a` |
| **Walmart corporate policy URL** | `https://corporate.walmart.com/policies#return-policy` |
| **Orders page** | `https://www.walmart.com/orders` |
| **Email evidence** | Walmart confirmation emails found in Max's Gmail (searched via MCP email tool) |

---

## GOTCHAS

1. **The 30-day trap:** Walmart's default is 90 days, and many people assume that applies universally. It does NOT for PCs. Missing this means losing ~$2,000. The corporate policy page was difficult to scrape (required multiple JavaScript injection attempts), but the help article page was successfully fetched and confirms the 30-day exception.

2. **Start-of-clock ambiguity:** The policy doesn't explicitly say whether the 30 days runs from order date or delivery date. Walmart's per-item "return by" date in the purchase history is the only authoritative source. Until that's pulled, there's a 2-day uncertainty window.

3. **No-slack plan risk:** "Return old only after new arrives" requires the replacement to ship and arrive before the return deadline. A shipping delay, backorder, or price-change hold could blow the window. The backup and wipe steps also take time and must happen before return.

4. **Three Chrome instances:** Claude has multiple browser connections active. Navigating to the orders page requires knowing which one is logged into Max's Walmart account. Guessing wrong wastes time and could trigger security flags.

5. **Original packaging required:** Walmart's policy explicitly says original packaging and all accessories must be included. Max needs to have kept the box and everything that came in it.

6. **Data at risk:** The machine has an Ubuntu install, genomics data, and SSH keys. These must be backed up AND wiped before return. No backup has been made yet. The USB disk's location is unknown.
