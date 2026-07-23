"""
Expired Future Contracts — list the futures contracts that existed for a past expiry.

Uses the Upstox Expired Instrument API. Resolve an expiry from
`expiries.py` first, then pass it here.

Usage:
  python expired_instruments/expired_future_contracts.py --token <TOKEN> --expiry 2024-12-26
  python expired_instruments/expired_future_contracts.py --token <TOKEN> --query BANKNIFTY --expiry 2024-12-24
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_underlying, most_recent_past_expiry, as_dict, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Expired future contracts via Expired Instrument API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default=None,
                        help="Past expiry date YYYY-MM-DD (default: most recent past expiry)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    inst = resolve_underlying(client, args.query)
    if not inst:
        die(f"Could not resolve an underlying for '{args.query}'.")
    instrument_key = inst.get("instrument_key", "")

    expiry = args.expiry
    if not expiry:
        try:
            expiry = most_recent_past_expiry(client, instrument_key)
        except Exception as e:
            die(f"API error fetching expiries: {e}")
        if not expiry:
            die("No past expiry available to demonstrate expired contracts.")
        print(f"\n{DIM}Auto-selected most recent past expiry: {expiry}{RESET}")

    print(f"\n{BOLD}Fetching expired future contracts{RESET} for {args.query.upper()} "
          f"expiry={expiry}...\n")

    api = upstox_client.ExpiredInstrumentApi(client)
    try:
        response = api.get_expired_future_contracts(instrument_key, expiry)
    except Exception as e:
        die(f"API error: {e}")

    contracts = response.data or []
    if not contracts:
        die("No expired future contracts returned for that expiry.")

    print(f"  {BOLD}{'Trading Symbol':<24} {'Lot':>6} {'Expiry':<12} {'Instrument Key'}{RESET}")
    print("  " + "─" * 78)
    for c in contracts:
        d = as_dict(c)
        print(f"  {CYAN}{str(d.get('trading_symbol') or '—'):<24}{RESET} "
              f"{str(d.get('lot_size') or '—'):>6} "
              f"{str(d.get('expiry') or '—'):<12} {d.get('instrument_key') or '—'}")

    print(f"\n  {DIM}Total contracts: {len(contracts)}{RESET}\n")


if __name__ == "__main__":
    main()
