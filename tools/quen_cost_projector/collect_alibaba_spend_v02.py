"""Collect real Alibaba Cloud Model Studio spend, split into VIDEO and QWEN.

Version 02, written 2026-08-06 by Claude Opus 5. Replaces
collect_quen_balance_v01.py, which estimated Qwen spend from local Codex
session logs and was about 2.3x too high, and which relied on MoMA's
ds_ledger for video, which under-reported by roughly half.

Both numbers now come from the same authoritative place: the Alibaba bill.

Two buckets, never mixed:

  VIDEO - wan* image-to-video / speech-to-video models plus videoretalk
          lip-sync. This is MoMA movie production.
  QWEN  - qwen* text models. This is Codex chat usage.

Anything else that appears on the bill (kimi, deepseek served by Alibaba,
embeddings) lands in OTHER and is reported but charted separately from
neither bucket.

Data sources, in order of preference:

1. Alibaba BSS OpenAPI (DescribeInstanceBill). Needs an AccessKey pair in
   ALIBABA_KEY_FILE, one line "AccessKeyId:AccessKeySecret" or two lines.
   With the key present this runs unattended every hour and reports the real
   invoice. Without it the script still works, but only from the seed.
2. The seed file, a verbatim copy of the console Cost Overview read by hand
   on 2026-08-06. It is the historical floor: live data is merged on top of
   it and a month total is never allowed to drop below the seed.

Output is written atomically so the page's auto-refresh can never read a
half-written file.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.parse
import urllib.request
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
SEED_FILE = HERE / "alibaba_bill_seed_20260806_v01.json"
HISTORY = HERE / "alibaba_spend.json"
JS_OUTPUT = HERE / "alibaba_spend.js"
ALIBABA_KEY_FILE = Path(
    r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\alibaba_billing_accesskey.txt"
)

BSS_ENDPOINT = "https://business.ap-southeast-1.aliyuncs.com/"
BSS_VERSION = "2017-12-14"
PRODUCT_CODE = "bailian"
FIRST_MONTH = "2026-04"
DAILY_LOOKBACK_DAYS = 6
MAX_SNAPSHOTS = 5000

# Alibaba bills on China Standard Time, so "today" on the bill is a Beijing
# day. The page says so; we bucket by the billing date exactly as given.
BEIJING = ZoneInfo("Asia/Shanghai")

VIDEO_HINTS = ("wan", "videoretalk", "i2v", "t2v", "s2v", "r2v", "video")
QWEN_HINTS = ("qwen",)


# --------------------------------------------------------------------------
# bucketing


def classify(model: str) -> str:
    """Return 'video', 'qwen' or 'other' for a billed model name."""
    name = (model or "").strip().lower()
    if not name:
        return "other"
    if any(h in name for h in VIDEO_HINTS):
        return "video"
    if any(name.startswith(h) for h in QWEN_HINTS):
        return "qwen"
    return "other"


# --------------------------------------------------------------------------
# BSS OpenAPI


def load_access_key() -> tuple[str, str] | None:
    if not ALIBABA_KEY_FILE.exists():
        return None
    try:
        text = ALIBABA_KEY_FILE.read_text(encoding="utf-8")
    except OSError:
        return None
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        return None
    if ":" in lines[0] and len(lines) == 1:
        key_id, _, secret = lines[0].partition(":")
        return key_id.strip(), secret.strip()
    if len(lines) >= 2:
        return lines[0], lines[1]
    return None


def _percent_encode(text: str) -> str:
    encoded = urllib.parse.quote(str(text), safe="")
    return encoded.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


def bss_call(key_id: str, secret: str, action: str, extra: dict) -> dict:
    """Signed GET against the BSS OpenAPI (RPC signature version 1.0)."""
    params = {
        "Action": action,
        "Version": BSS_VERSION,
        "Format": "JSON",
        "AccessKeyId": key_id,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": uuid.uuid4().hex,
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    params.update({k: v for k, v in extra.items() if v is not None})
    canonical = "&".join(
        _percent_encode(k) + "=" + _percent_encode(params[k]) for k in sorted(params)
    )
    string_to_sign = "GET&" + _percent_encode("/") + "&" + _percent_encode(canonical)
    signature = base64.b64encode(
        hmac.new((secret + "&").encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()
    url = BSS_ENDPOINT + "?" + canonical + "&Signature=" + _percent_encode(signature)
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def row_model_name(row: dict) -> str:
    """Find the model name in a bill row without assuming one field name."""
    for field in (
        "InstanceConfig",
        "NickName",
        "InstanceID",
        "InstanceId",
        "CommodityCode",
        "InstanceSpec",
        "ItemName",
        "BillingItem",
        "ProductDetail",
    ):
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            if classify(value) != "other":
                return value.strip()
    for field in ("InstanceConfig", "NickName", "InstanceID", "CommodityCode"):
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def row_amount(row: dict) -> float:
    for field in ("PretaxAmount", "PaymentAmount", "PretaxGrossAmount", "CashAmount"):
        value = row.get(field)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue
    return 0.0


def fetch_bill(key_id: str, secret: str, cycle: str, billing_date: str | None) -> list[dict]:
    """One month (billing_date None) or one day of instance-level bill rows."""
    rows: list[dict] = []
    token = None
    while True:
        extra = {
            "BillingCycle": cycle,
            "ProductCode": PRODUCT_CODE,
            "Granularity": "DAILY" if billing_date else "MONTHLY",
            "MaxResults": 300,
            "NextToken": token,
        }
        if billing_date:
            extra["BillingDate"] = billing_date
        payload = bss_call(key_id, secret, "DescribeInstanceBill", extra)
        data = payload.get("Data") or {}
        items = data.get("Items") or []
        if isinstance(items, dict):
            items = items.get("Item") or []
        rows.extend(items)
        token = data.get("NextToken")
        if not token:
            return rows


def months_since(first: str) -> list[str]:
    year, month = (int(p) for p in first.split("-"))
    today = datetime.now(BEIJING).date()
    out = []
    while (year, month) <= (today.year, today.month):
        out.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1
    return out


def collect_live(key_id: str, secret: str) -> tuple[dict, dict, list[str]]:
    """Return (months, daily, errors). months[cycle][bucket], daily[date][bucket]."""
    months: dict[str, dict[str, float]] = {}
    daily: dict[str, dict[str, float]] = {}
    errors: list[str] = []

    for cycle in months_since(FIRST_MONTH):
        try:
            for row in fetch_bill(key_id, secret, cycle, None):
                bucket = classify(row_model_name(row))
                months.setdefault(cycle, {}).setdefault(bucket, 0.0)
                months[cycle][bucket] += row_amount(row)
        except Exception as exc:  # noqa: BLE001 - one bad month must not kill the run
            errors.append(f"month {cycle}: {type(exc).__name__}: {exc}")

    today = datetime.now(BEIJING).date()
    for back in range(DAILY_LOOKBACK_DAYS):
        day = today - timedelta(days=back)
        stamp = day.isoformat()
        try:
            for row in fetch_bill(key_id, secret, f"{day.year:04d}-{day.month:02d}", stamp):
                bucket = classify(row_model_name(row))
                daily.setdefault(stamp, {}).setdefault(bucket, 0.0)
                daily[stamp][bucket] += row_amount(row)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"day {stamp}: {type(exc).__name__}: {exc}")

    return months, daily, errors


# --------------------------------------------------------------------------
# seed + merge


def load_seed() -> dict:
    try:
        return json.loads(SEED_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"seed unreadable: {exc}", file=sys.stderr)
        return {"months": {}, "video_daily": [], "qwen_daily": []}


def merge(seed: dict, live_months: dict, live_daily: dict) -> tuple[dict, dict]:
    """Seed is a floor. Live wins wherever it reports more."""
    months: dict[str, dict[str, float]] = {}
    for cycle, buckets in (seed.get("months") or {}).items():
        months[cycle] = {k: float(v) for k, v in buckets.items()}
    for cycle, buckets in live_months.items():
        target = months.setdefault(cycle, {})
        for bucket, amount in buckets.items():
            target[bucket] = max(target.get(bucket, 0.0), round(amount, 6))

    daily: dict[str, dict[str, float]] = {}
    for day, amount in seed.get("video_daily") or []:
        daily.setdefault(day, {})["video"] = float(amount)
    for day, amount in seed.get("qwen_daily") or []:
        daily.setdefault(day, {})["qwen"] = float(amount)
    for day, buckets in live_daily.items():
        target = daily.setdefault(day, {})
        for bucket, amount in buckets.items():
            target[bucket] = max(target.get(bucket, 0.0), round(amount, 6))
    return months, daily


def build_bucket(months: dict, daily: dict, bucket: str) -> dict:
    rows = sorted(
        ((day, round(buckets.get(bucket, 0.0), 6)) for day, buckets in daily.items()),
        key=lambda item: item[0],
    )
    rows = [row for row in rows if row[1] > 0]

    today_key = datetime.now(BEIJING).date().isoformat()
    week_cut = (datetime.now(BEIJING).date() - timedelta(days=6)).isoformat()
    today_usd = sum(usd for day, usd in rows if day == today_key)
    week_usd = sum(usd for day, usd in rows if day >= week_cut)

    # Lifetime comes from the monthly totals, which are complete even for the
    # months whose day-level rows we never pulled.
    lifetime = sum(buckets.get(bucket, 0.0) for buckets in months.values())

    series: list[list] = []
    running = 0.0
    for day, usd in rows:
        running += usd
        epoch = int(
            datetime.fromisoformat(day).replace(tzinfo=BEIJING).timestamp() + 86399
        )
        series.append([epoch, round(running, 6)])

    return {
        "lifetime_usd": round(lifetime, 6),
        "today_usd": round(today_usd, 6),
        "last_7_days_usd": round(week_usd, 6),
        "daily": [[day, usd] for day, usd in reversed(rows)],
        "series": series,
        "months": {
            cycle: round(buckets.get(bucket, 0.0), 6)
            for cycle, buckets in sorted(months.items())
            if buckets.get(bucket, 0.0) > 0
        },
    }


# --------------------------------------------------------------------------


def load_snapshots() -> list[dict]:
    if not HISTORY.exists():
        return []
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8")).get("snapshots", [])
    except (OSError, json.JSONDecodeError, AttributeError):
        return []


def atomic_write(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    seed = load_seed()
    credentials = load_access_key()
    errors: list[str] = []
    live_months: dict = {}
    live_daily: dict = {}

    if credentials:
        live_months, live_daily, errors = collect_live(*credentials)
        source = "Alibaba BSS OpenAPI (real bill)" if not errors else "Alibaba BSS OpenAPI (partial)"
    else:
        source = "seed only - no Alibaba AccessKey installed"
        errors.append(
            f"no AccessKey at {ALIBABA_KEY_FILE}; showing the console read of "
            f"{seed.get('read_on', 'unknown date')} and nothing newer"
        )

    months, daily = merge(seed, live_months, live_daily)
    video = build_bucket(months, daily, "video")
    qwen = build_bucket(months, daily, "qwen")
    other = build_bucket(months, daily, "other")

    now = int(time.time())
    snapshots = load_snapshots()
    snapshots.append(
        {
            "t": now,
            "video": video["lifetime_usd"],
            "qwen": qwen["lifetime_usd"],
            "live": bool(credentials and not errors),
        }
    )
    snapshots = snapshots[-MAX_SNAPSHOTS:]

    payload = {
        "schema": 3,
        "updated": now,
        "source": source,
        "live": bool(credentials and not errors),
        "errors": errors,
        "account": seed.get("account_id"),
        "region": seed.get("region"),
        "timezone_note": "Alibaba billing days follow China Standard Time (UTC+8), so a Pacific evening lands on the next billing day.",
        "video": video,
        "qwen": qwen,
        "other": other,
        "grand_total_usd": round(
            video["lifetime_usd"] + qwen["lifetime_usd"] + other["lifetime_usd"], 6
        ),
        "snapshots": snapshots,
    }

    atomic_write(HISTORY, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    atomic_write(
        JS_OUTPUT,
        "window.ALIBABA_SPEND=" + json.dumps(payload, separators=(",", ":")) + ";\n",
    )
    print(
        f"video=${video['lifetime_usd']:.2f} qwen=${qwen['lifetime_usd']:.2f} "
        f"other=${other['lifetime_usd']:.2f} source={source}"
    )
    for line in errors:
        print(f"  note: {line}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
