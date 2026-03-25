"""
Search for equity instruments by name.

Usage:
  python instrument_search/search_equity.py --token <ACCESS_TOKEN> --query RELIANCE
  python instrument_search/search_equity.py --token <ACCESS_TOKEN> --query INFY --exchange BSE
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument


def main():
    parser = argparse.ArgumentParser(description="Search equity instruments on Upstox")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="RELIANCE", help="Stock name or symbol to search")
    parser.add_argument("--exchange", default="NSE", help="Exchange: NSE or BSE (default: NSE)")
    parser.add_argument("--records", type=int, default=10, help="Max results (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Searching equity instruments for '{args.query}' on {args.exchange}...\n")

    response = search_instrument(
        client,
        args.query,
        exchanges=args.exchange,
        segments="EQ",
        records=args.records,
    )

    instruments = response.data or []
    if not instruments:
        print("No instruments found.")
        return

    print(f"{'Instrument Key':<25} {'Trading Symbol':<20} {'Name':<30} {'ISIN':<15} {'Lot Size'}")
    print("-" * 105)

    for inst in instruments:
        print(
            f"{inst.get('instrument_key', ''):<25} "
            f"{inst.get('trading_symbol', ''):<20} "
            f"{inst.get('name', ''):<30} "
            f"{inst.get('isin', ''):<15} "
            f"{inst.get('lot_size', '')}"
        )

    meta = response.meta_data
    if meta and meta.page:
        p = meta.page
        print(f"\nPage {p.page_number} of {p.total_pages}  |  Showing {p.records} of {p.total_records} total results")
        if p.total_pages and int(str(p.total_pages)) > 1:
            print("Tip: use --records 30 or add --page to paginate further.")


if __name__ == "__main__":
    main()
