"""
Expired Option Contracts — list the CE/PE contracts that existed for a past expiry.

Uses the Upstox Expired Instrument API. Resolve an expiry from
`expiries.py` first, then pass it here to enumerate the strikes/contracts that
were listed for that expiry.

Usage:
  python expired_instruments/expired_option_contracts.py --token <TOKEN> --expiry 2024-12-26
  python expired_instruments/expired_option_contracts.py --token <TOKEN> --query BANKNIFTY --expiry 2024-12-24
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_underlying, as_dict, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
RED   = "\033[31m"
DIM   = "\033[2m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="Expired option contracts via Expired Instrument API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", required=True, help="Past expiry date YYYY-MM-DD")
    args = parser.parse_args()

    client = get_api_client(args.token)

    inst = resolve_underlying(client, args.query)
    if not inst:
        die(f"Could not resolve an underlying for '{args.query}'.")
    instrument_key = inst.get("instrument_key", "")

    print(f"\n{BOLD}Fetching expired option contracts{RESET} for {args.query.upper()} "
          f"expiry={args.expiry}...\n")

    api = upstox_client.ExpiredInstrumentApi(client)
    try:
        response = api.get_expired_option_contracts(instrument_key, args.expiry)
    except Exception as e:
        die(f"API error: {e}")

    contracts = response.data or []
    if not contracts:
        die("No expired option contracts returned for that expiry.")

    rows = sorted(
        (as_dict(c) for c in contracts),
        key=lambda d: (d.get("strike_price") or 0, d.get("instrument_type") or ""),
    )

    print(f"  {BOLD}{'Type':<5} {'Strike':>10}  {'Trading Symbol':<24} {'Instrument Key'}{RESET}")
    print("  " + "─" * 78)
    for d in rows:
        itype = (d.get("instrument_type") or "").upper()
        colour = GREEN if itype == "CE" else (RED if itype == "PE" else "")
        strike = d.get("strike_price")
        strike_s = f"{strike:>10,.2f}" if isinstance(strike, (int, float)) else f"{'—':>10}"
        print(f"  {colour}{itype:<5}{RESET} {strike_s}  "
              f"{str(d.get('trading_symbol') or '—'):<24} {d.get('instrument_key') or '—'}")

    print(f"\n  {DIM}Total contracts: {len(rows)}{RESET}\n")


if __name__ == "__main__":
    main()
