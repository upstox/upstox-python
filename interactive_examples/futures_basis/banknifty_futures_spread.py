"""
BankNifty near-month vs far-month futures calendar spread.

Same logic as nifty_futures_spread.py but for BANKNIFTY.
BankNifty has weekly expiries — this script picks the two nearest contracts
(which may both be in the current month or span two months).

Usage:
  python futures_basis/banknifty_futures_spread.py --token <TOKEN>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, get_futures_sorted, get_ltp


def main():
    parser = argparse.ArgumentParser(description="BankNifty near/far futures calendar spread")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print("Fetching BANKNIFTY futures contracts...\n")
    futures = get_futures_sorted(client, "BANKNIFTY", exchange="NSE")

    if len(futures) < 2:
        print(f"Need at least 2 futures contracts, found {len(futures)}.")
        sys.exit(1)

    near = futures[0]
    far = futures[1]

    near_key = near["instrument_key"]
    far_key = far["instrument_key"]

    print(f"Near contract : {near['trading_symbol']}  (expiry: {near['expiry']})")
    print(f"Far contract  : {far['trading_symbol']}  (expiry: {far['expiry']})")
    print()

    ltp_data = get_ltp(client, near_key, far_key)

    near_ltp = ltp_data[near_key].last_price
    far_ltp = ltp_data[far_key].last_price

    spread = far_ltp - near_ltp
    spread_pct = (spread / near_ltp) * 100
    lot_size = near.get("lot_size", 1)

    print(f"{'Contract':<35} {'LTP':>10} {'Close':>10} {'Volume':>10}")
    print("-" * 70)
    for key, sym in [(near_key, near["trading_symbol"]), (far_key, far["trading_symbol"])]:
        q = ltp_data[key]
        print(f"{sym:<35} {q.last_price:>10.2f} {q.cp:>10.2f} {q.volume:>10,}")

    print("-" * 70)
    print(f"\nCalendar Spread (far - near) : {spread:>+10.2f}  ({spread_pct:+.2f}%)")
    print(f"Lot size                     : {lot_size}")
    print(f"Spread per lot               : ₹{spread * lot_size:,.2f}")

    if spread > 0:
        print("\nContango: far month at premium — normal. Monitor for roll opportunity.")
    else:
        print("\nBackwardation: far month at discount — unusual. Possible supply shock or event.")


if __name__ == "__main__":
    main()
