"""
Expiries — list all expiry dates available for an underlying (expired + live).

Uses the Upstox Expired Instrument API to fetch the full list of expiry dates
for an underlying (e.g. NIFTY), useful for back-testing against expired
contracts.

Usage:
  python expired_instruments/expiries.py --token <TOKEN>
  python expired_instruments/expiries.py --token <TOKEN> --query BANKNIFTY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_underlying, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Expiry dates via Expired Instrument API")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    inst = resolve_underlying(client, args.query)
    if not inst:
        die(f"Could not resolve an underlying for '{args.query}'.")
    instrument_key = inst.get("instrument_key", "")

    print(f"\n{BOLD}Fetching expiries{RESET} for {args.query.upper()} "
          f"({instrument_key})...\n")

    api = upstox_client.ExpiredInstrumentApi(client)
    try:
        response = api.get_expiries(instrument_key)
    except Exception as e:
        die(f"API error: {e}")

    expiries = response.data or []
    if not expiries:
        die("No expiries returned.")

    print(f"  {BOLD}{'#':>3}  Expiry{RESET}")
    print("  " + "─" * 24)
    for i, exp in enumerate(sorted(str(e) for e in expiries), start=1):
        print(f"  {CYAN}{i:>3}{RESET}  {exp}")

    print(f"\n  {DIM}Total expiries: {len(expiries)}{RESET}\n")


if __name__ == "__main__":
    main()
