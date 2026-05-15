"""
Share Holdings — promoter, FII, DII and public shareholding over quarters.

Fetches shareholding pattern history from the Upstox Fundamentals API
and displays the quarterly breakdown across holder categories.

Usage:
  python fundamentals/share_holdings.py --token <TOKEN>
  python fundamentals/share_holdings.py --token <TOKEN> --symbol INFY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
RESET = "\033[0m"

CATEGORY_ORDER = ["promoter", "fii", "dii", "public", "others"]


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _sort_key(cat_name: str) -> int:
    nl = cat_name.lower()
    for i, k in enumerate(CATEGORY_ORDER):
        if k in nl:
            return i
    return len(CATEGORY_ORDER)


def _fmt(v):
    if v in (None, "", "—"):
        return "—"
    try:
        return f"{float(v):>8.2f}%"
    except (TypeError, ValueError):
        return str(v)[:9]


def main():
    parser = argparse.ArgumentParser(description="Share Holdings via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, _ = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching share holdings for {args.symbol.upper()} (ISIN: {isin})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_share_holdings(isin)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    items = data if isinstance(data, list) else ([data] if data else [])

    categories = []
    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        elif not isinstance(item, dict):
            item = vars(item) if hasattr(item, "__dict__") else {}
        cat  = str(item.get("category") or "—")
        hist = item.get("history") or []
        categories.append((cat, hist))

    if not categories:
        die("No shareholding data found.")

    # Sort by standard category order
    categories.sort(key=lambda x: _sort_key(x[0]))

    max_cols = 8
    # Use the history length of the first entry to determine number of periods
    n_periods = max(len(h) for _, h in categories) if categories else 0
    n_cols    = min(n_periods, max_cols)
    periods   = [f"Q{i+1}" for i in range(n_cols)]

    col_w   = 10
    label_w = 26

    header_periods = " ".join(f"{p:>{col_w}}" for p in periods)
    print(f"  {BOLD}{'Category':<{label_w}} {header_periods}{RESET}")
    print("  " + "─" * (label_w + (col_w + 1) * len(periods)))

    for cat, hist in categories:
        vals = (hist or [])[:n_cols]
        while len(vals) < n_cols:
            vals.append(None)
        row_vals = " ".join(f"{_fmt(v):>{col_w}}" for v in vals)
        print(f"  {CYAN}{cat:<{label_w}}{RESET} {row_vals}")

    if n_periods > max_cols:
        print(f"\n  (showing latest {max_cols} of {n_periods} quarters)")
    print()


if __name__ == "__main__":
    main()
