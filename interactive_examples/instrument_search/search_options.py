"""
Search for options contracts by underlying symbol.

Demonstrates the expiry and atm_offset filters of the instrument search API.

Usage:
  python instrument_search/search_options.py --token <TOKEN> --query NIFTY
  python instrument_search/search_options.py --token <TOKEN> --query BANKNIFTY --expiry current_month --atm_offset 2
  python instrument_search/search_options.py --token <TOKEN> --query RELIANCE --expiry 2025-04-24 --type CE
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument


def main():
    parser = argparse.ArgumentParser(description="Search options contracts on Upstox")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument(
        "--expiry",
        default="current_month",
        help="Expiry: 'current_week', 'current_month', or 'yyyy-MM-dd' (default: current_month)",
    )
    parser.add_argument(
        "--atm_offset",
        type=int,
        default=0,
        help="ATM offset: 0=ATM, +1=one strike OTM call, -1=one strike OTM put (default: 0)",
    )
    parser.add_argument(
        "--type",
        dest="option_type",
        default="CE,PE",
        help="Option type: CE, PE, or CE,PE (default: CE,PE)",
    )
    parser.add_argument("--records", type=int, default=10, help="Max results (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(
        f"Searching {args.option_type} options for '{args.query}'  "
        f"expiry={args.expiry}  atm_offset={args.atm_offset:+d}\n"
    )

    response = search_instrument(
        client,
        args.query,
        exchanges="NSE",
        segments="FO",
        instrument_types=args.option_type,
        expiry=args.expiry,
        atm_offset=args.atm_offset,
        records=args.records,
    )

    instruments = response.data or []
    if not instruments:
        print("No options found. Try a different expiry or symbol.")
        return

    print(f"{'Instrument Key':<25} {'Symbol':<25} {'Type':<6} {'Strike':>10} {'Expiry':<14} {'Lot Size'}")
    print("-" * 95)

    for inst in instruments:
        print(
            f"{inst.get('instrument_key', ''):<25} "
            f"{inst.get('trading_symbol', ''):<25} "
            f"{inst.get('instrument_type', ''):<6} "
            f"{inst.get('strike_price', 0):>10.2f} "
            f"{inst.get('expiry', ''):<14} "
            f"{inst.get('lot_size', '')}"
        )

    meta = response.meta_data
    if meta and meta.page:
        p = meta.page
        print(f"\nShowing {p.records} of {p.total_records} total results")


if __name__ == "__main__":
    main()
