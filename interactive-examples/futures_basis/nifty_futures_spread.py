"""
Nifty near-month vs far-month futures calendar spread (arbitrage).

Uses instrument search to dynamically find the two nearest NIFTY futures
contracts, fetches their live LTPs, and prints the spread.

A positive spread (far > near) indicates contango (normal for index futures).
A narrowing spread as expiry approaches signals roll or arbitrage opportunity.

Usage:
  python futures_basis/nifty_futures_spread.py --token <TOKEN>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, get_futures_sorted, get_ltp


def main():
    parser = argparse.ArgumentParser(description="NIFTY near/far futures calendar spread")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Index symbol (default: NIFTY)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching {args.query} futures contracts...\n")
    futures = get_futures_sorted(client, args.query, exchange="NSE", exact_symbol=True)

    if len(futures) < 2:
        print(f"Need at least 2 futures contracts, found {len(futures)}. Try a broader query.")
        sys.exit(1)

    near = futures[0]
    far = futures[1]

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

    print(f"{'Contract':<30} {'LTP':>10} {'Close':>10} {'Volume':>10}")
    print("-" * 65)
    for key, label in [(near_key, near["trading_symbol"]), (far_key, far["trading_symbol"])]:
        q = ltp_data[key]
        print(f"{label:<30} {q.last_price:>10.2f} {q.cp:>10.2f} {q.volume:>10,}")

    print("-" * 65)
    print(f"\nCalendar Spread (far - near) : {spread:>+10.2f}  ({spread_pct:+.2f}%)")

    if spread > 0:
        print("Market is in CONTANGO — far month trades at a premium (normal for index futures).")
    elif spread < 0:
        print("Market is in BACKWARDATION — far month trades at a discount (unusual, check news).")
    else:
        print("Spread is zero — contracts are trading at parity.")

    lot_size = near.get("lot_size", 1)
    print(f"\nLot size     : {lot_size}")
    print(f"Spread / lot : ₹{spread * lot_size:,.2f}")
    print(
        "\nArbitrage signal: Buy near + Sell far if spread exceeds cost-of-carry; "
        "the spread will collapse on near-month expiry."
    )


if __name__ == "__main__":
    main()
