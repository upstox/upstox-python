"""
Futures Roll Cost Calculator.

Rolling a futures position means closing the near-month contract and
opening the same position in the far-month contract.

Roll cost = Far LTP - Near LTP  (for a long position)
           = Near LTP - Far LTP  (for a short position)

Expresses the roll cost as:
  - Absolute points
  - Percentage of near-month price
  - Annualised rate
  - Cost in rupees per lot

Usage:
  python futures_basis/futures_roll_cost.py --token <TOKEN>
  python futures_basis/futures_roll_cost.py --token <TOKEN> --query BANKNIFTY --side short
"""

import argparse
import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, get_futures_sorted, get_ltp


def days_between(d1: str, d2: str) -> int:
    fmt = "%Y-%m-%d"
    try:
        return abs((datetime.strptime(d1, fmt) - datetime.strptime(d2, fmt)).days)
    except ValueError:
        return 30


def main():
    parser = argparse.ArgumentParser(description="Futures roll cost calculator")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--side", default="long", choices=["long", "short"], help="Position side")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching {args.query} futures for roll cost calculation...\n")
    futures = get_futures_sorted(client, args.query, exchange="NSE")

    if len(futures) < 2:
        print(f"Need at least 2 contracts, found {len(futures)}.")
        sys.exit(1)

    near = futures[0]
    far = futures[1]

    near_key = near["instrument_key"]
    far_key = far["instrument_key"]

    ltp_data = get_ltp(client, near_key, far_key)

    near_ltp = ltp_data[near_key].last_price
    far_ltp = ltp_data[far_key].last_price

    if args.side == "long":
        roll_cost = far_ltp - near_ltp
        action = "Sell near + Buy far"
    else:
        roll_cost = near_ltp - far_ltp
        action = "Buy near + Sell far"

    roll_pct = (roll_cost / near_ltp) * 100
    lot_size = near.get("lot_size", 1)
    roll_rupees = roll_cost * lot_size

    days_gap = days_between(near.get("expiry", ""), far.get("expiry", ""))
    dte_near = max((datetime.strptime(near.get("expiry", date.today().isoformat()), "%Y-%m-%d").date() - date.today()).days, 1)
    annualised = (roll_pct / days_gap) * 365 if days_gap else 0

    print(f"Position side : {args.side.upper()}")
    print(f"Roll action   : {action}\n")

    print(f"{'Contract':<30} {'LTP':>10} {'Expiry':<14}")
    print("-" * 58)
    print(f"{near['trading_symbol']:<30} {near_ltp:>10.2f} {near.get('expiry', ''):<14}  (near — close this)")
    print(f"{far['trading_symbol']:<30} {far_ltp:>10.2f} {far.get('expiry', ''):<14}  (far  — open this)")
    print("-" * 58)

    print(f"\nRoll cost (points)      : {roll_cost:>+10.2f}")
    print(f"Roll cost (%)           : {roll_pct:>+10.2f}%")
    print(f"Roll cost per lot (₹)   : {roll_rupees:>+10.2f}")
    print(f"Days between expiries   : {days_gap}")
    print(f"Annualised roll rate    : {annualised:>+.2f}% p.a.")
    print(f"Days to near expiry     : {dte_near}")

    if roll_cost > 0:
        print(f"\nRolling costs {roll_pct:.2f}% — you pay a premium to stay long past expiry.")
    else:
        print(f"\nRolling earns {abs(roll_pct):.2f}% — far month at discount (backwardation).")


if __name__ == "__main__":
    main()
