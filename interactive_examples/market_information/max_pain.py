"""
Max Pain — strike level at which option writers experience least loss.

Fetches the Max Pain value for the requested underlying + expiry + date plus
intraday insights bucketed at the requested interval.

Usage:
  python market_information/max_pain.py --token <TOKEN> --expiry 2026-05-29
  python market_information/max_pain.py --token <TOKEN> --instrument-key "NSE_INDEX|Nifty Bank" --expiry 2026-05-29 --bucket-interval 30
"""

import argparse
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _as_dict(obj):
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj) if hasattr(obj, "__dict__") else {}


def _fmt_num(v, prec=2):
    if v in (None, "", "—"):
        return "—"
    try:
        return f"{float(v):,.{prec}f}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="Max Pain via Market API")
    parser.add_argument("--token",           required=True, help="Upstox access or analytics token")
    parser.add_argument("--instrument-key",  default="NSE_INDEX|Nifty 50",
                        help='Underlying instrument key (default: "NSE_INDEX|Nifty 50")')
    parser.add_argument("--expiry",          required=True, help="Expiry YYYY-MM-DD")
    parser.add_argument("--date",            dest="_date", default=date.today().isoformat(),
                        help="Data date YYYY-MM-DD (default: today)")
    parser.add_argument("--bucket-interval", default="60",
                        help="Intraday bucket size in minutes (default: 60)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketApi(client)

    print(f"\nFetching Max Pain for {args.instrument_key} expiry={args.expiry} "
          f"date={args._date} bucket={args.bucket_interval}m...\n")

    try:
        response = api.get_max_pain_data(
            args.instrument_key, args.expiry, args._date, args.bucket_interval
        )
    except Exception as e:
        die(f"API error: {e}")

    data = _as_dict(response.data)
    if not data:
        die("No data returned.")

    max_pain = data.get("max_pain")
    spot     = data.get("spot_closing_price")
    insights = data.get("insights") or []

    print(f"  {CYAN}Max Pain Strike  {RESET} {GREEN}{_fmt_num(max_pain)}{RESET}")
    print(f"  {CYAN}Spot Close       {RESET} {_fmt_num(spot)}")
    print()

    if not insights:
        print(f"  {DIM}No intraday insights returned.{RESET}\n")
        return

    col_w = 14
    print(f"  {BOLD}{'Timestamp':<24} {'Max Pain':>{col_w}} {'Spot':>{col_w}}{RESET}")
    print("  " + "─" * (24 + (col_w + 1) * 2))

    for ins in insights:
        ins = _as_dict(ins)
        ts  = ins.get("timestamp") or ins.get("time") or "—"
        mp  = ins.get("max_pain")
        sp  = ins.get("spot_price")
        print(f"  {str(ts):<24} {_fmt_num(mp):>{col_w}} {_fmt_num(sp):>{col_w}}")

    print(f"\n  {len(insights)} data points.\n")


if __name__ == "__main__":
    main()
