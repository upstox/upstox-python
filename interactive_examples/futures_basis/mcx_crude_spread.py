"""
MCX Crude Oil near-month vs far-month futures spread.

Crude oil is a commodity futures traded on MCX. The near/far spread
reflects storage costs, supply expectations, and global oil market structure.

Contango (far > near): market expects future supply tightness or storage cost.
Backwardation (near > far): immediate demand spike or supply disruption.

Usage:
  python futures_basis/mcx_crude_spread.py --token <TOKEN>
  python futures_basis/mcx_crude_spread.py --token <TOKEN> --query NATURALGAS
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def main():
    parser = argparse.ArgumentParser(description="MCX commodity futures near/far spread")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="CRUDEOIL", help="MCX commodity symbol (default: CRUDEOIL)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching MCX {args.query} futures contracts...\n")

    response = search_instrument(
        client,
        args.query,
        exchanges="MCX",
        segments="COMM",
        instrument_types="FUT",
        records=10,
    )

    instruments = response.data or []
    if len(instruments) < 2:
        print(f"Need at least 2 futures contracts, found {len(instruments)}.")
        sys.exit(1)

    # Sort by expiry
    instruments.sort(key=lambda x: x.get("expiry", ""))

    near = instruments[0]
    far = instruments[1]

    near_key = near["instrument_key"]
    far_key = far["instrument_key"]

    print(f"Near month : {near['trading_symbol']}  (expiry: {near['expiry']})")
    print(f"Far month  : {far['trading_symbol']}  (expiry: {far['expiry']})")
    print()

    ltp_data = get_ltp(client, near_key, far_key)

    near_ltp = ltp_data[near_key].last_price
    far_ltp = ltp_data[far_key].last_price

    spread = far_ltp - near_ltp
    spread_pct = (spread / near_ltp) * 100
    lot_size = near.get("lot_size", 1)

    print(f"{'Contract':<30} {'LTP':>10} {'Close':>10}")
    print("-" * 55)
    for key, inst in [(near_key, near), (far_key, far)]:
        q = ltp_data[key]
        print(f"{inst['trading_symbol']:<30} {q.last_price:>10.2f} {q.cp:>10.2f}")
    print("-" * 55)

    print(f"\nSpread (far - near)  : {spread:>+10.2f}  ({spread_pct:+.2f}%)")
    print(f"Lot size             : {lot_size} barrels")
    print(f"Spread per lot (₹)   : {spread * lot_size:>+10.2f}")

    if len(instruments) > 2:
        print(f"\nAll available contracts for {args.query}:")
        print(f"  {'#':<4} {'Symbol':<25} {'Expiry':<14} {'LTP':>10}")
        all_keys = [i["instrument_key"] for i in instruments]
        all_ltp = get_ltp(client, *all_keys)
        for i, inst in enumerate(instruments, 1):
            key = inst["instrument_key"]
            ltp_val = all_ltp[key].last_price if key in all_ltp else 0
            print(f"  {i:<4} {inst['trading_symbol']:<25} {inst.get('expiry', ''):<14} {ltp_val:>10.2f}")

    if spread > 0:
        print("\nContango: market pricing in storage/carry costs (normal for crude).")
    else:
        print("\nBackwardation: immediate demand or supply disruption signal.")


if __name__ == "__main__":
    main()
