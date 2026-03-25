"""
Search for futures contracts by underlying symbol.

Lists all available expiries sorted nearest-first.

Usage:
  python instrument_search/search_futures.py --token <TOKEN>
  python instrument_search/search_futures.py --token <TOKEN> --query BANKNIFTY
  python instrument_search/search_futures.py --token <TOKEN> --query CRUDEOIL --exchange MCX
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument


def main():
    parser = argparse.ArgumentParser(description="Search futures contracts on Upstox")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--exchange", default="NSE", help="Exchange: NSE, BSE, MCX (default: NSE)")
    parser.add_argument("--records", type=int, default=10, help="Max results (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Searching futures contracts for '{args.query}' on {args.exchange}...\n")

    response = search_instrument(
        client,
        args.query,
        exchanges=args.exchange,
        segments="FO" if args.exchange != "MCX" else "COMM",
        instrument_types="FUT",
        records=args.records,
    )

    instruments = response.data or []
    if not instruments:
        print("No futures found.")
        return

    # Sort by expiry (nearest first)
    instruments.sort(key=lambda x: x.get("expiry", ""))

    print(f"{'#':<4} {'Instrument Key':<25} {'Trading Symbol':<25} {'Expiry':<14} {'Lot Size':>10} {'Tick Size':>10}")
    print("-" * 95)

    for i, inst in enumerate(instruments, 1):
        label = " <-- near month" if i == 1 else (" <-- far month" if i == 2 else "")
        print(
            f"{i:<4} "
            f"{inst.get('instrument_key', ''):<25} "
            f"{inst.get('trading_symbol', ''):<25} "
            f"{inst.get('expiry', ''):<14} "
            f"{inst.get('lot_size', ''):>10} "
            f"{inst.get('tick_size', ''):>10}"
            f"{label}"
        )

    meta = response.meta_data
    if meta and meta.page:
        p = meta.page
        print(f"\nShowing {p.records} of {p.total_records} total results")


if __name__ == "__main__":
    main()
