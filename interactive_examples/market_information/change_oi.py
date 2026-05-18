"""
Change in OI — open-interest deltas across strikes over a configurable lookback.

Fetches per-strike call/put OI change data from the Upstox Market API.

Usage:
  python market_information/change_oi.py --token <TOKEN> --expiry 2026-05-29
  python market_information/change_oi.py --token <TOKEN> --expiry 2026-05-29 --interval 5
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
RED   = "\033[31m"
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


def _fmt_delta(v):
    if v in (None, "", "—"):
        return "—"
    try:
        f = float(v)
        if f > 0:
            return f"{GREEN}{int(f):>+14,}{RESET}"
        if f < 0:
            return f"{RED}{int(f):>+14,}{RESET}"
        return f"{int(f):>+14,}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="Change in OI via Market API")
    parser.add_argument("--token",          required=True, help="Upstox access or analytics token")
    parser.add_argument("--instrument-key", default="NSE_INDEX|Nifty 50",
                        help='Underlying instrument key (default: "NSE_INDEX|Nifty 50")')
    parser.add_argument("--expiry",         required=True, help="Expiry date YYYY-MM-DD")
    parser.add_argument("--date",           dest="_date", default=date.today().isoformat(),
                        help="Data date YYYY-MM-DD (default: today)")
    parser.add_argument("--interval",       default="5",
                        help="Lookback in days (default: 5)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketApi(client)

    print(f"\nFetching Change-in-OI for {args.instrument_key} expiry={args.expiry} "
          f"date={args._date} interval={args.interval}d...\n")

    try:
        response = api.get_change_oi_data(args.instrument_key, args.expiry, args._date, args.interval)
    except Exception as e:
        die(f"API error: {e}")

    data = _as_dict(response.data)
    if not data:
        die("No data returned.")

    total_calls = data.get("total_calls")
    total_puts  = data.get("total_puts")
    spot        = data.get("spot_closing_price")
    strikes     = data.get("call_put_oi_data_list") or []

    print(f"  {CYAN}Spot Close          {RESET} {spot if spot is not None else '—'}")
    print(f"  {CYAN}Total Δ Calls OI    {RESET} {_fmt_delta(total_calls)}")
    print(f"  {CYAN}Total Δ Puts OI     {RESET} {_fmt_delta(total_puts)}")
    print()

    if not strikes:
        die("No per-strike change-in-OI data.")

    col_w = 16
    print(f"  {BOLD}{'Strike':>{col_w}} {'Δ Call OI':>{col_w}} {'Δ Put OI':>{col_w}}{RESET}")
    print("  " + "─" * ((col_w + 1) * 3))

    rows = []
    for s in strikes:
        s = _as_dict(s)
        try:
            strike = float(s.get("strike") or s.get("strike_price") or 0)
        except (TypeError, ValueError):
            strike = 0
        rows.append((strike, s.get("call_oi"), s.get("put_oi")))

    rows.sort(key=lambda r: r[0])
    for strike, call_oi, put_oi in rows:
        marker = ""
        try:
            if spot is not None and abs(float(strike) - float(spot)) < 1e-6:
                marker = f"  {DIM}← spot{RESET}"
        except (TypeError, ValueError):
            pass
        print(f"  {strike:>{col_w},.2f} {_fmt_delta(call_oi):>{col_w}} {_fmt_delta(put_oi):>{col_w}}{marker}")

    print(f"\n  {len(rows)} strikes.\n")


if __name__ == "__main__":
    main()
