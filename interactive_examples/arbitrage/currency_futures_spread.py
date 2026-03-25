"""
Currency Futures Calendar Spread — USDINR.

Searches NSE currency segment for USDINR futures, fetches near and far month
prices, and computes the spread (interest rate differential proxy).

USDINR futures spread reflects the USD-INR interest rate differential:
  spread ≈ spot_rate * (r_INR - r_USD) * (T2 - T1) / 365

A wider spread than the interest differential may signal a trading opportunity.

Usage:
  python arbitrage/currency_futures_spread.py --token <TOKEN>
  python arbitrage/currency_futures_spread.py --token <TOKEN> --pair EURINR
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def main():
    parser = argparse.ArgumentParser(description="Currency futures calendar spread")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--pair", default="USDINR", help="Currency pair (default: USDINR)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching {args.pair} currency futures...\n")

    resp = search_instrument(
        client,
        args.pair,
        exchanges="NSE",
        segments="CURR",
        instrument_types="FUT",
        records=10,
    )

    instruments = resp.data or []
    if len(instruments) < 2:
        print(f"Need at least 2 contracts, found {len(instruments)}.")
        sys.exit(1)

    instruments.sort(key=lambda x: x.get("expiry", ""))

    near = instruments[0]
    far  = instruments[1]

    near_key = near["instrument_key"]
    far_key  = far["instrument_key"]

    ltp_data = get_ltp(client, near_key, far_key)

    near_ltp = ltp_data[near_key].last_price
    far_ltp  = ltp_data[far_key].last_price

    spread = far_ltp - near_ltp
    spread_pct = (spread / near_ltp * 100) if near_ltp else 0

    print(f"{'Contract':<30} {'LTP':>10} {'Close':>10} {'Volume':>10}")
    print("-" * 65)
    for key, inst in [(near_key, near), (far_key, far)]:
        q = ltp_data[key]
        label = " (near)" if key == near_key else " (far)"
        print(f"{inst['trading_symbol']:<30} {q.last_price:>10.4f} {q.cp:>10.4f} {q.volume:>10,}{label}")
    print("-" * 65)

    print(f"\nPair              : {args.pair}")
    print(f"Near expiry       : {near.get('expiry')}")
    print(f"Far expiry        : {far.get('expiry')}")
    print(f"Spread (far-near) : {spread:>+8.4f}  ({spread_pct:+.4f}%)")

    if spread > 0:
        print(f"\nContango: far month at premium — implies INR depreciation expectation.")
        print(f"Annualised depreciation: ~{spread_pct:.2f}% over the period")
    else:
        print(f"\nBackwardation: unusual for USDINR — may signal RBI intervention or carry play.")

    if len(instruments) > 2:
        print(f"\nAll available contracts:")
        all_keys = [i["instrument_key"] for i in instruments]
        all_ltp = get_ltp(client, *all_keys)
        for i, inst in enumerate(instruments, 1):
            key = inst["instrument_key"]
            ltp_val = all_ltp[key].last_price if key in all_ltp else 0
            print(f"  {i}. {inst['trading_symbol']:<25} expiry: {inst.get('expiry',''):<14} LTP: {ltp_val:.4f}")


if __name__ == "__main__":
    main()
