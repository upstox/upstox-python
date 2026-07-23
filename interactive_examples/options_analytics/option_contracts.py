"""
Option Contracts — enumerate the live option contracts for an underlying.

Uses the Upstox Options API (get_option_contracts). Lists the CE/PE strikes
available for an underlying, optionally filtered to a single expiry. This is
the raw contract master — pair it with option_chain_native.py for pricing.

Usage:
  python options_analytics/option_contracts.py --token <TOKEN>
  python options_analytics/option_contracts.py --token <TOKEN> --query BANKNIFTY --expiry 2026-07-30
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_underlying, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Live option contracts via Options API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default=None, help="Optional expiry filter YYYY-MM-DD")
    args = parser.parse_args()

    client = get_api_client(args.token)

    inst = resolve_underlying(client, args.query)
    if not inst:
        die(f"Could not resolve an underlying for '{args.query}'.")
    instrument_key = inst.get("instrument_key", "")

    print(f"\n{BOLD}Fetching option contracts{RESET} for {args.query.upper()} "
          f"({instrument_key}){f', expiry={args.expiry}' if args.expiry else ''}...\n")

    api = upstox_client.OptionsApi(client)
    try:
        if args.expiry:
            response = api.get_option_contracts(instrument_key, expiry_date=args.expiry)
        else:
            response = api.get_option_contracts(instrument_key)
    except Exception as e:
        die(f"API error: {e}")

    contracts = response.data or []
    if not contracts:
        die("No option contracts returned.")

    rows = sorted(
        (as_dict(c) for c in contracts),
        key=lambda d: (str(d.get("expiry") or ""), d.get("strike_price") or 0,
                       d.get("instrument_type") or ""),
    )

    print(f"  {BOLD}{'Expiry':<12} {'Type':<5} {'Strike':>10}  {'Trading Symbol':<24} {'Instrument Key'}{RESET}")
    print("  " + "─" * 90)
    for d in rows[:60]:
        itype = (d.get("instrument_type") or "").upper()
        colour = GREEN if itype == "CE" else (RED if itype == "PE" else "")
        strike = d.get("strike_price")
        strike_s = f"{strike:>10,.2f}" if isinstance(strike, (int, float)) else f"{'—':>10}"
        print(f"  {str(d.get('expiry') or '—')[:10]:<12} {colour}{itype:<5}{RESET} {strike_s}  "
              f"{str(d.get('trading_symbol') or '—'):<24} {d.get('instrument_key') or '—'}")

    print(f"\n  {DIM}Showing {min(len(rows), 60)} of {len(rows)} contracts.{RESET}\n")


if __name__ == "__main__":
    main()
