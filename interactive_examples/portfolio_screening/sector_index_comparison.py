"""
Sector Index Comparison.

Fetches live LTPs for major NSE sector indices and ranks them by
daily performance (% change from previous close).

Sectors tracked: Nifty 50, Bank Nifty, Nifty IT, Nifty Pharma,
Nifty Auto, Nifty FMCG, Nifty Metal, Nifty Realty, Nifty Energy, Nifty Media.

Usage:
  python portfolio_screening/sector_index_comparison.py --token <TOKEN>
  python portfolio_screening/sector_index_comparison.py --token <TOKEN> --sectors "NIFTY 50,NIFTY BANK,NIFTY IT"
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp

DEFAULT_SECTORS = [
    "NIFTY 50",
    "NIFTY BANK",
    "NIFTY IT",
    "NIFTY PHARMA",
    "NIFTY AUTO",
    "NIFTY FMCG",
    "NIFTY METAL",
    "NIFTY REALTY",
    "NIFTY ENERGY",
    "NIFTY MEDIA",
]


def find_index(client, name):
    resp = search_instrument(client, name, exchanges="NSE", segments="INDEX", records=3)
    data = resp.data or []
    for inst in data:
        if name.upper() in inst.get("trading_symbol", "").upper():
            return inst
    return data[0] if data else None


def main():
    parser = argparse.ArgumentParser(description="Compare live NSE sector index performance")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument(
        "--sectors",
        default=",".join(DEFAULT_SECTORS),
        help="Comma-separated sector index names",
    )
    args = parser.parse_args()

    client = get_api_client(args.token)
    sector_names = [s.strip() for s in args.sectors.split(",")]

    print("Fetching sector indices...\n")

    # Resolve instrument keys
    index_map = {}
    for name in sector_names:
        inst = find_index(client, name)
        if inst:
            index_map[name] = inst
        else:
            print(f"  Warning: '{name}' not found, skipping.")

    if not index_map:
        print("No indices found.")
        sys.exit(1)

    all_keys = [inst["instrument_key"] for inst in index_map.values()]
    ltp_data = get_ltp(client, *all_keys)

    # Compute change% and sort
    results = []
    for name, inst in index_map.items():
        key = inst["instrument_key"]
        q = ltp_data.get(key)
        if not q:
            continue
        ltp = q.last_price
        prev = q.cp  # close price = previous day close
        chg = ltp - prev
        chg_pct = (chg / prev * 100) if prev else 0
        results.append((name, inst.get("trading_symbol", name), ltp, prev, chg, chg_pct))

    results.sort(key=lambda x: x[5], reverse=True)

    print(f"{'Rank':<5} {'Index':<20} {'Symbol':<20} {'LTP':>10} {'Prev':>10} {'Chg':>10} {'Chg%':>8}  {'Bar':}")
    print("-" * 95)

    for rank, (name, symbol, ltp, prev, chg, chg_pct) in enumerate(results, 1):
        bar_len = min(int(abs(chg_pct) * 3), 20)
        bar = ("▲" if chg >= 0 else "▼") * bar_len
        arrow = "▲" if chg >= 0 else "▼"
        print(
            f"{rank:<5} {name:<20} {symbol:<20} "
            f"{ltp:>10,.2f} {prev:>10,.2f} {chg:>+10.2f} {chg_pct:>+7.2f}%  {bar}"
        )

    best  = results[0]
    worst = results[-1]
    print(f"\nBest performer  : {best[0]}  ({best[5]:+.2f}%)")
    print(f"Worst performer : {worst[0]}  ({worst[5]:+.2f}%)")
    breadth_pos = sum(1 for r in results if r[5] > 0)
    print(f"Market breadth  : {breadth_pos}/{len(results)} sectors up")


if __name__ == "__main__":
    main()
