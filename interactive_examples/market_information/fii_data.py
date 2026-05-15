"""
FII Data — Foreign Institutional Investor activity across market segments.

Fetches FII buy / sell / open-interest data from the Upstox Market API for the
requested segment and interval.

Usage:
  python market_information/fii_data.py --token <TOKEN>
  python market_information/fii_data.py --token <TOKEN> --data-type "NSE_FO|INDEX_OPTIONS" --interval 1D
  python market_information/fii_data.py --token <TOKEN> --interval 1M --from 2026-01-01
"""

import argparse
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

ALLOWED_DATA_TYPES = (
    "NSE_EQ|CASH",
    "NSE_FO|INDEX_FUTURES",
    "NSE_FO|STOCK_FUTURES",
    "NSE_FO|INDEX_OPTIONS",
    "NSE_FO|STOCK_OPTIONS",
)


def _as_dict(obj):
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj) if hasattr(obj, "__dict__") else {}


def _fmt_amt(v):
    if v in (None, "", "—"):
        return "—"
    try:
        f = float(v)
        color = GREEN if f > 0 else (RED if f < 0 else "")
        return f"{color}{f:>16,.2f}{RESET}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="FII Activity Data via Market API")
    parser.add_argument("--token",     required=True, help="Upstox access or analytics token")
    parser.add_argument("--data-type", default="NSE_EQ|CASH",
                        help=f"Segment (default: NSE_EQ|CASH). Allowed: {', '.join(ALLOWED_DATA_TYPES)}")
    parser.add_argument("--interval",  default="1D", choices=("1D", "1M"),
                        help="Interval (default: 1D)")
    parser.add_argument("--from",      dest="_from", default=None,
                        help="Optional start date YYYY-MM-DD")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketApi(client)

    print(f"\nFetching FII data — data_type={args.data_type}, interval={args.interval}"
          f"{f', from={args._from}' if args._from else ''}...\n")

    try:
        if args._from:
            response = api.get_fii_data(args.data_type, args.interval, _from=args._from)
        else:
            response = api.get_fii_data(args.data_type, args.interval)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    IST = timezone(timedelta(hours=5, minutes=30))

    def _ts(ms):
        try:
            return datetime.fromtimestamp(int(ms) / 1000, tz=IST).strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            return str(ms)

    # The API returns either a list of rows OR a dict keyed by segment whose
    # values are lists of rows. Flatten both into one row stream, tagging the
    # segment when present.
    flat_rows = []
    if isinstance(data, dict):
        for seg, rows in data.items():
            if not isinstance(rows, list):
                rows = [rows]
            for r in rows:
                d = _as_dict(r)
                d["segment"] = seg
                flat_rows.append(d)
    elif isinstance(data, list):
        for r in data:
            d = _as_dict(r)
            d.setdefault("segment", args.data_type)
            flat_rows.append(d)
    else:
        d = _as_dict(data)
        d.setdefault("segment", args.data_type)
        flat_rows.append(d)

    if not flat_rows:
        die("No FII rows.")

    # Sort by time_stamp if present
    flat_rows.sort(key=lambda r: r.get("time_stamp") or 0)

    DATE_COLS = ("date", "trade_date", "_date", "time_stamp", "timestamp")
    PREFERRED_COLS = [
        "segment", "time_stamp", "date", "trade_date", "_date",
        "buy_amount", "sell_amount",
        "buy_contracts", "sell_contracts",
        "oi_contracts", "oi_amount",
        "total_long_contracts", "total_short_contracts",
        "total_call_long_contracts", "total_put_long_contracts",
        "total_call_short_contracts", "total_put_short_contracts",
    ]
    seen = set(); cols = []
    for r in flat_rows:
        for c in PREFERRED_COLS:
            if c in r and c not in seen:
                cols.append(c); seen.add(c)
    if not cols:
        cols = list(flat_rows[0].keys())

    col_w = 22
    header = " ".join(f"{c:>{col_w}}" for c in cols)
    print(f"  {BOLD}{header}{RESET}")
    print("  " + "─" * (len(cols) * (col_w + 1)))

    for r in flat_rows:
        cells = []
        for c in cols:
            v = r.get(c)
            if c == "time_stamp":
                cells.append(f"{_ts(v):>{col_w}}")
            elif c == "segment":
                cells.append(f"{CYAN}{str(v or '—'):>{col_w}}{RESET}")
            elif c in DATE_COLS:
                cells.append(f"{str(v) if v is not None else '—':>{col_w}}")
            else:
                # _fmt_amt adds ANSI color codes (~9 chars) — pad accordingly
                cells.append(f"{_fmt_amt(v):>{col_w + 9}}")
        print("  " + " ".join(cells))

    print(f"\n  Rows: {len(flat_rows)}\n")


if __name__ == "__main__":
    main()
