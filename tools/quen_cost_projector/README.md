# Alibaba spend tracker (WAN video + Qwen text)

Version 02, rewritten 2026-08-06 by Claude Opus 5.

## What this is

One page, two graphs, both fed by the **real Alibaba Cloud Model Studio bill**:

- **Top graph: WAN video generation.** MoMA movie production. Any `wan*`
  model plus `videoretalk` lip-sync.
- **Bottom graph: Qwen text.** Codex running on `qwen3.8-max` and
  `qwen3.7-plus`.

They share one Alibaba account, one API key and one invoice, but they are
different work and are **never summed together**. The shared expense summary
table carries them as two separate rows.

Page: `quen_tracker.html` (filename kept so the sibling trackers' links keep
working). Collector: `collect_alibaba_spend_v02.py`. Schedule installer:
`update_schedule_v02.py`.

## Why version 02 exists

Version 01 estimated Qwen spend by counting tokens in local Codex session
logs, and took video spend from MoMA's `ds_ledger`. Both were wrong, in
opposite directions. Checked against the console bill on 2026-08-06:

| | v01 said | Real bill |
|---|---|---|
| Qwen text | about $65 | **$28.37** |
| WAN video, lifetime | $108.75 | **$217.13** |

Three separate faults in the Qwen number: it counted sessions that started
under the `qwen` provider label but were switched mid-run to `gpt-5.6-sol`
or `deepseek-v4-flash`; it priced `qwen3.7-plus` at `qwen3.8-max` rates
(five times too high on input); and its cache discount did not match what
Alibaba actually applied. The video number was simply MoMA guessing its own
cost per clip and guessing low.

Version 02 stops estimating. Both numbers come from the invoice.

## Data sources

1. **Alibaba BSS OpenAPI** (`DescribeInstanceBill`, product `bailian`,
   endpoint `business.ap-southeast-1.aliyuncs.com`). This is the same API the
   console itself calls. Needs an AccessKey pair at
   `C:\Users\maxre\Nextcloud\zSyncMain\ssh\alibaba_billing_accesskey.txt`
   (one line `AccessKeyId:AccessKeySecret`, or two lines). **Not installed
   yet** — until it is, the page shows an amber banner and the seed only.
2. **Seed file** `alibaba_bill_seed_20260806_v01.json` — a verbatim record of
   the console Cost Overview read by hand on 2026-08-06, months 2026-04
   through 2026-08. It is a floor: live data merges on top and a total is
   never allowed to fall below it.

## Schedule

Hourly, at seven minutes past, as the task **Alibaba Spend Collector**
(hidden, `pythonw`). Max's rule of 2026-08-06: hourly if the numbers can come
through an API, every eight hours if a human has to log in each time. The BSS
OpenAPI route is an API, so hourly. Set `HOURS = 8` in
`update_schedule_v02.py` if the key is ever removed.

The old ramping 5/20/30-minute task **Quen Balance Collector** has been
deleted; it existed only because the session-log estimate changed minute to
minute.

## Timezone trap

Alibaba's billing day follows **China Standard Time (UTC+8)**. A Pacific
evening lands on the *next* billing day. This is why every dollar of the
Qwen work Max did on the evening of Pacific 2026-08-05 appears on billing day
2026-08-06, and why the page labels its "Today" card as a Beijing billing day.

## The real numbers as of 2026-08-06

| Month | Video | Qwen |
|---|---|---|
| Apr 2026 | $15.04 | - |
| May 2026 | $7.44 | - |
| Jun 2026 | $66.30 | - |
| Jul 2026 | $128.35 | - |
| Aug 2026 | - | $28.37 |
| **Total** | **$217.13** | **$28.37** |

July includes $9.23 of tax. April's video figure is mostly `videoretalk`
lip-sync ($10.85). The Qwen day splits `qwen3.8-max` $24.93 and
`qwen3.7-plus` $3.45.

## Files

| File | Role |
|---|---|
| `quen_tracker.html` | the page, two graphs |
| `collect_alibaba_spend_v02.py` | collector, writes `alibaba_spend.json` / `.js` |
| `alibaba_bill_seed_20260806_v01.json` | hand-read console history, the floor |
| `update_schedule_v02.py` | installs the hourly task |
| `../shared_expense_summary.js` | v03, carries WAN and Qwen as two rows |
| `archive/` | superseded v01 collector, page and data |

Output files (`alibaba_spend.json` / `.js`) are generated and git-ignored.
