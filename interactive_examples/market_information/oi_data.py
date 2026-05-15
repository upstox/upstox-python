"""
OI Data — Open Interest across all strikes for an underlying + expiry.

Fetches per-strike call/put OI from the Upstox Market API.

Usage:
  python market_information/oi_data.py --token <TOKEN> --expiry 2026-05-29
  python market_information/oi_data.py --token <TOKEN> --instrument-key "NSE_INDEX|Nifty Bank" --expiry 2026-05-29 --date 2026-05-14
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


def _fmt_int(v):
    if v in (None, "", "—"):
        return "—"
    try:
        return f"{int(float(v)):>14,}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="OI Data via Market API")
    parser.add_argument("--token",          required=True, help="Upstox access or analytics token")
    parser.add_argument("--instrument-key", default="NSE_INDEX|Nifty 50",
                        help='Underlying instrument key (default: "NSE_INDEX|Nifty 50")')
    parser.add_argument("--expiry",         required=True, help="Expiry date YYYY-MM-DD")
    parser.add_argument("--date",           dest="_date", default=date.today().isoformat(),
                        help="Data date YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketApi(client)

    print(f"\nFetching OI data for {args.instrument_key} expiry={args.expiry} date={args._date}...\n")

    try:
        response = api.get_oi_data(args.instrument_key, args.expiry, args._date)
    except Exception as e:
        die(f"API error: {e}")

    data = _as_dict(response.data)
    if not data:
        die("No data returned.")

    total_calls = data.get("total_calls")
    total_puts  = data.get("total_puts")
    spot        = data.get("spot_closing_price")
    strikes     = data.get("call_put_oi_data_list") or []

    pcr = None
    try:
        if total_calls and float(total_calls) > 0:
            pcr = float(total_puts) / float(total_calls)
    except (TypeError, ValueError):
        pass

    print(f"  {CYAN}Spot Close      {RESET} {spot if spot is not None else '—'}")
    print(f"  {CYAN}Total Calls OI  {RESET} {_fmt_int(total_calls)}")
    print(f"  {CYAN}Total Puts OI   {RESET} {_fmt_int(total_puts)}")
    print(f"  {CYAN}PCR (Puts/Calls){RESET} {pcr:.3f}" if pcr is not None else f"  {CYAN}PCR{RESET} —")
    print()

    if not strikes:
        die("No per-strike OI data.")

    col_w = 16
    print(f"  {BOLD}{'Strike':>{col_w}} {'Call OI':>{col_w}} {'Put OI':>{col_w}}{RESET}")
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
        print(f"  {strike:>{col_w},.2f} {_fmt_int(call_oi):>{col_w}} {_fmt_int(put_oi):>{col_w}}{marker}")

    print(f"\n  {len(rows)} strikes.\n")


if __name__ == "__main__":
    main()
