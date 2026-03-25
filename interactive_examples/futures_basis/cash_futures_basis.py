"""
Cash-Futures Basis: Compare index spot (cash) price vs near-month futures.

The basis = Futures Price - Spot Price.
Positive basis = futures premium over spot (contango / cost-of-carry).
Negative basis = futures discount (backwardation).

This script searches for the NIFTY index (spot) and near-month NIFTY futures,
fetches their LTPs, and computes the basis and implied annualised carry rate.

Usage:
  python futures_basis/cash_futures_basis.py --token <TOKEN>
  python futures_basis/cash_futures_basis.py --token <TOKEN> --query BANKNIFTY
"""

import argparse
import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_futures_sorted, get_ltp


def get_index_key(client, query: str) -> dict:
    """Find the index (spot) instrument for a given query."""
    resp = search_instrument(
        client,
        query,
        exchanges="NSE",
        segments="INDEX",
        instrument_types="INDEX",
        records=5,
    )
    instruments = resp.data or []
    for inst in instruments:
        if query.upper() in inst.get("trading_symbol", "").upper():
            return inst
    return instruments[0] if instruments else None


def days_to_expiry(expiry_str: str) -> int:
    try:
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        return max((expiry - date.today()).days, 1)
    except ValueError:
        return 30  # fallback


def main():
    parser = argparse.ArgumentParser(description="Cash-Futures basis and implied carry")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY 50", help="Index name (default: NIFTY 50)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching spot and futures data for '{args.query}'...\n")

    # Get index spot
    index_inst = get_index_key(client, args.query)
    if not index_inst:
        print(f"Could not find index instrument for '{args.query}'.")
        sys.exit(1)

    # Get near-month futures
    futures = get_futures_sorted(client, args.query.replace(" ", ""), exchange="NSE")
    if not futures:
        futures = get_futures_sorted(client, "NIFTY", exchange="NSE")
    if not futures:
        print("Could not find futures contracts.")
        sys.exit(1)

    near = futures[0]
    index_key = index_inst["instrument_key"]
    futures_key = near["instrument_key"]

    ltp_data = get_ltp(client, index_key, futures_key)

    spot_ltp = ltp_data[index_key].last_price
    futures_ltp = ltp_data[futures_key].last_price

    basis = futures_ltp - spot_ltp
    basis_pct = (basis / spot_ltp) * 100
    dte = days_to_expiry(near.get("expiry", ""))
    annualised_carry = (basis_pct / dte) * 365

    print(f"{'Instrument':<35} {'LTP':>12}")
    print("-" * 50)
    print(f"{index_inst.get('trading_symbol', 'INDEX'):<35} {spot_ltp:>12.2f}  (spot)")
    print(f"{near['trading_symbol']:<35} {futures_ltp:>12.2f}  (futures)")
    print("-" * 50)

    print(f"\nBasis (Futures - Spot) : {basis:>+10.2f}  ({basis_pct:+.2f}%)")
    print(f"Days to expiry         : {dte}")
    print(f"Annualised carry       : {annualised_carry:+.2f}% p.a.")

    if basis > 0:
        print("\nFutures at premium — market expects positive carry (interest > dividends).")
    elif basis < 0:
        print("\nFutures at discount — dividend yield exceeds interest cost, or bearish sentiment.")


if __name__ == "__main__":
    main()
