"""
Market Holiday — check whether a specific date is a market holiday.

Uses the Upstox Market Holidays & Timings API to fetch holiday details for a
single date (which exchanges are closed, holiday name, etc.).

Usage:
  python market_data/market_holiday.py --token <TOKEN> --date 2026-01-26
  python market_data/market_holiday.py --token <TOKEN>          # defaults to next Republic Day-ish sample
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Single-date holiday lookup via Holidays API")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--date", required=True, help="Date to check, YYYY-MM-DD")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.MarketHolidaysAndTimingsApi(client)

    print(f"\n{BOLD}Checking market holiday{RESET} for {args.date}...\n")

    try:
        response = api.get_holiday(args.date)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        print(f"  {GREEN}{args.date} is not a listed market holiday.{RESET}\n")
        return

    rows = data if isinstance(data, list) else [data]
    for r in rows:
        d = as_dict(r)
        print(f"  {CYAN}{BOLD}{d.get('date', args.date)}{RESET} — "
              f"{d.get('description') or d.get('holiday_name') or 'Holiday'}")
        day = d.get("day")
        if day:
            print(f"    Day: {day}")
        closed = d.get("closed_exchanges") or d.get("closed") or []
        open_ex = d.get("open_exchanges") or d.get("open") or []
        if closed:
            print(f"    Closed: {', '.join(str(x) for x in closed)}")
        if open_ex:
            print(f"    Open:   {', '.join(str(x) for x in open_ex)}")
        print()

    print(f"  {DIM}Holidays on {args.date}: {len(rows)}{RESET}\n")


if __name__ == "__main__":
    main()
