"""
Market Status — print live open/closed/pre-open status for NSE, BSE, and MCX.

Usage:
  python market_data/market_status.py --token <TOKEN>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client
import upstox_client

EXCHANGES = ["NSE", "BSE", "MCX", "NFO", "BFO", "CDS"]

STATUS_COLOUR = {
    "open":     "\033[32m",   # green
    "pre_open": "\033[33m",   # yellow
    "closed":   "\033[31m",   # red
}
RESET = "\033[0m"
BOLD  = "\033[1m"


def colour(status: str) -> str:
    s = (status or "").lower().replace(" ", "_")
    c = STATUS_COLOUR.get(s, "")
    return f"{c}{status}{RESET}" if c else status


def main():
    parser = argparse.ArgumentParser(description="Live market status for NSE, BSE, MCX")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.MarketHolidaysAndTimingsApi(client)

    print(f"\n{BOLD}Market Status{RESET}\n")
    print(f"{'Exchange':<12} {'Status'}")
    print("─" * 35)

    for exchange in EXCHANGES:
        try:
            resp = api.get_market_status(exchange)
            m = resp.data
            if m is None:
                print(f"{exchange:<12} {'N/A':<18}")
                continue
            status = getattr(m, "status", "") or ""
            exch   = getattr(m, "exchange", exchange) or exchange
            print(f"{exchange:<12} {colour(status)}")
        except Exception as e:
            err = str(e)
            if "400" in err or "404" in err or "No data" in err.lower():
                print(f"{exchange:<12} {'—':<18}  (not available)")
            else:
                print(f"{exchange:<12} {'ERROR':<18}  {str(e)[:50]}")

    print()


if __name__ == "__main__":
    main()
