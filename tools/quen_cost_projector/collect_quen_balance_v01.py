"""Estimate pure Qwen (DashScope Model Studio) spend for the Quen cost tracker.

Schema 2. Two independent sources:

1. PURE QWEN (this tracker's own numbers): local Codex session logs
   (~/.codex/sessions/**/rollout-*.jsonl) whose session_meta declares
   model_provider "qwen". Every token_count event carries the per-API-call
   usage (last_token_usage); summing those over all qwen sessions is the
   billed token total (forked sessions do not replay parent usage). Tokens
   are priced at the published qwen3.8-max International rates:
   input $2.00/1M, context-cache hit input $0.20/1M (10% of input),
   output $6.00/1M (reasoning tokens are part of output). input_tokens is
   treated as inclusive of cached_input_tokens (OpenAI-compatible semantics),
   so fresh input = input_tokens - cached_input_tokens.

2. DASHSCOPE LEDGER (context only): the ds_ledger /report DashScope provider
   total. That number is 100% MoMA video generation (wan2.6-i2v-flash) and is
   shown on the page only as a separate context line, never mixed into the
   Qwen cards or chart.

All USD figures are estimates; the page labels them as such.
Both output files are written atomically (temp file + rename) so the
60-second auto-refresh can never read a half-written file.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
SESSIONS = Path.home() / ".codex" / "sessions"
HISTORY = HERE / "quen_balance.json"
JS_OUTPUT = HERE / "quen_balance.js"
SECRET_FILE = (
    r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\ds_ledger_secret_20260610.txt"
)
LEDGER_URL = "https://ledger.maxrempel.com/report"
PACIFIC = ZoneInfo("America/Los_Angeles")
MAX_SNAPSHOTS = 5000
MAX_SERIES = 1500

PRICE_INPUT_PER_M = 2.0
PRICE_CACHED_INPUT_PER_M = 0.2
PRICE_OUTPUT_PER_M = 6.0


def event_cost(usage: dict) -> tuple[float, dict]:
    inp = int(usage.get("input_tokens") or 0)
    cached = int(usage.get("cached_input_tokens") or 0)
    out = int(usage.get("output_tokens") or 0)
    cached = min(cached, inp)
    fresh = inp - cached
    usd = (
        fresh * PRICE_INPUT_PER_M
        + cached * PRICE_CACHED_INPUT_PER_M
        + out * PRICE_OUTPUT_PER_M
    ) / 1_000_000.0
    return usd, {"input": inp, "cached_input": cached, "output": out}


def scan_sessions() -> dict:
    events: list[tuple[int, float, dict]] = []
    sessions = 0
    if SESSIONS.exists():
        for path in sorted(SESSIONS.rglob("rollout-*.jsonl")):
            try:
                with path.open("r", encoding="utf-8", errors="replace") as fh:
                    first = fh.readline()
                    if '"model_provider":"qwen"' not in first:
                        continue
                    sessions += 1
                    fh.seek(0)
                    for line in fh:
                        if '"token_count"' not in line:
                            continue
                        record = json.loads(line)
                        payload = record.get("payload") or {}
                        if record.get("type") != "event_msg" or payload.get("type") != "token_count":
                            continue
                        info = payload.get("info") or {}
                        usage = info.get("last_token_usage")
                        if not usage:
                            continue
                        ts = record.get("timestamp") or payload.get("timestamp") or ""
                        try:
                            epoch = int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp())
                        except ValueError:
                            continue
                        usd, tokens = event_cost(usage)
                        events.append((epoch, usd, tokens))
            except (OSError, json.JSONDecodeError):
                continue
    events.sort(key=lambda item: item[0])
    return {"events": events, "sessions": sessions}


def build_qwen(scan: dict) -> dict:
    now = time.time()
    daily: dict[str, dict] = {}
    series: list[list] = []
    totals = {"input": 0, "cached_input": 0, "output": 0}
    lifetime = 0.0
    today_usd = 0.0
    week_usd = 0.0
    month_usd = 0.0
    today_key = datetime.now(PACIFIC).strftime("%Y-%m-%d")
    for epoch, usd, tokens in scan["events"]:
        lifetime += usd
        for key, value in tokens.items():
            totals[key] += value
        day = datetime.fromtimestamp(epoch, PACIFIC).strftime("%Y-%m-%d")
        bucket = daily.setdefault(day, {"usd": 0.0, "input": 0, "cached_input": 0, "output": 0})
        bucket["usd"] += usd
        for key, value in tokens.items():
            bucket[key] += value
        age = now - epoch
        if age <= 7 * 86400:
            week_usd += usd
        if age <= 30 * 86400:
            month_usd += usd
        if day == today_key:
            today_usd += usd
        series.append([epoch, round(lifetime, 6)])
    if len(series) > MAX_SERIES:
        step = len(series) / MAX_SERIES
        thinned = [series[int(i * step)] for i in range(MAX_SERIES)]
        if thinned[-1] != series[-1]:
            thinned.append(series[-1])
        series = thinned
    daily_rows = [
        [day, round(row["usd"], 6), row["input"], row["cached_input"], row["output"]]
        for day, row in sorted(daily.items(), reverse=True)
    ]
    return {
        "lifetime_usd": round(lifetime, 6),
        "today_usd": round(today_usd, 6),
        "last_7_days_usd": round(week_usd, 6),
        "last_30_days_usd": round(month_usd, 6),
        "tokens": totals,
        "sessions": scan["sessions"],
        "events": len(scan["events"]),
        "daily": daily_rows,
        "series": series,
    }


def fetch_ledger_context() -> dict | None:
    try:
        with open(SECRET_FILE, encoding="utf-8") as fh:
            secret = next(
                line.strip() for line in fh if line.strip() and not line.strip().startswith("#")
            )
        request = urllib.request.Request(
            LEDGER_URL,
            headers={
                "X-Ledger-Secret": secret,
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (compatible; quen-tracker/2.0)",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            report = json.loads(response.read().decode("utf-8"))
        for provider in report.get("providers", []):
            if provider.get("key") == "dashscope":
                return {
                    "lifetime": float(provider.get("lifetime", 0)),
                    "today": float(provider.get("today", 0)),
                    "last_7_days": float(provider.get("last_7_days", 0)),
                    "note": "MoMA video generation (wan2.6-i2v-flash); context only",
                }
    except Exception as exc:  # noqa: BLE001 - context is optional
        print(f"ledger context unavailable: {type(exc).__name__}: {exc}", file=sys.stderr)
    return None


def load_snapshots() -> list[dict]:
    if not HISTORY.exists():
        return []
    try:
        data = json.loads(HISTORY.read_text(encoding="utf-8"))
        return data.get("snapshots", [])
    except (json.JSONDecodeError, OSError, AttributeError):
        return []


def atomic_write(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    scan = scan_sessions()
    qwen = build_qwen(scan)

    now = int(time.time())
    snapshots = load_snapshots()
    spend = 0.0
    if snapshots:
        previous = float(snapshots[-1].get("lifetime", 0))
        if qwen["lifetime_usd"] > previous + 1e-9:
            spend = round(qwen["lifetime_usd"] - previous, 6)
    snapshots.append(
        {"t": now, "lifetime": qwen["lifetime_usd"], "spend": spend, "source": "session-logs"}
    )
    snapshots = snapshots[-MAX_SNAPSHOTS:]

    payload = {
        "schema": 2,
        "updated": now,
        "model": "qwen3.8-max",
        "pricing": {
            "input_per_m": PRICE_INPUT_PER_M,
            "cached_input_per_m": PRICE_CACHED_INPUT_PER_M,
            "output_per_m": PRICE_OUTPUT_PER_M,
            "note": "DashScope Model Studio International list prices; cache hits at 10%",
        },
        "source": "local Codex session logs (model_provider=qwen), per-call token usage",
        "qwen": qwen,
        "snapshots": snapshots,
        "dashscope_ledger": fetch_ledger_context(),
    }
    atomic_write(HISTORY, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    atomic_write(
        JS_OUTPUT,
        "window.QUEN_BALANCE=" + json.dumps(payload, separators=(",", ":")) + ";\n",
    )
    print(
        f"qwen lifetime=${qwen['lifetime_usd']:.4f} today=${qwen['today_usd']:.4f} "
        f"7d=${qwen['last_7_days_usd']:.4f} sessions={qwen['sessions']} "
        f"events={qwen['events']} points={len(snapshots)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
