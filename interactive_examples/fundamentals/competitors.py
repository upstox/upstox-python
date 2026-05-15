"""
Competitors — peer companies in the same sector with market cap data.

Fetches the competitor list from the Upstox Fundamentals API using the
instrument_key resolved from the given stock symbol and displays a
comparison table of each peer company's sector and market capitalisation.

Usage:
  python fundamentals/competitors.py --token <TOKEN>
  python fundamentals/competitors.py --token <TOKEN> --symbol TCS
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


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _val(obj, key, default="—"):
    if obj is None:
        return default
    if isinstance(obj, dict):
        v = obj.get(key)
    else:
        v = getattr(obj, key, None)
    return str(v) if v is not None else default


def _fmt_crore(val):
    try:
        v = float(val)
        if v >= 1e7:
            return f"₹{v/1e7:>12,.2f} Cr"
        return f"₹{v:>12,.2f}"
    except (TypeError, ValueError):
        return "—"


def main():
    parser = argparse.ArgumentParser(description="Competitors via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    _, instrument_key = resolve_symbol(client, args.symbol)
    if not instrument_key:
        die(f"Could not resolve instrument key for '{args.symbol}'.")

    print(f"\nFetching competitors for {args.symbol.upper()} ({instrument_key})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_competitors(instrument_key)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    items = data if isinstance(data, list) else ([data] if data else [])

    rows = []
    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        elif not isinstance(item, dict):
            item = vars(item) if hasattr(item, "__dict__") else {}

        profile = item.get("company_profile") or {}
        sector  = item.get("sector") or {}
        mcap_inr = item.get("sector_market_cap_inr") or {}
        ikey    = _val(item, "instrument_key")

        if isinstance(profile, dict):
            p = profile
        else:
            p = vars(profile) if hasattr(profile, "__dict__") else {}

        if isinstance(sector, dict):
            s = sector
        else:
            s = vars(sector) if hasattr(sector, "__dict__") else {}

        if isinstance(mcap_inr, dict):
            m = mcap_inr
        else:
            m = vars(mcap_inr) if hasattr(mcap_inr, "__dict__") else {}

        name     = p.get("company_name") or p.get("name") or "—"
        industry = p.get("industry") or s.get("industry") or s.get("name") or "—"
        mcap     = m.get("market_cap") or m.get("value") or "—"

        rows.append((str(name), str(industry), mcap, ikey))

    if not rows:
        die("No competitor data found.")

    # Sort by market cap descending
    def _sort_mcap(row):
        try:
            return float(row[2])
        except (TypeError, ValueError):
            return -1

    rows.sort(key=_sort_mcap, reverse=True)

    print(f"  {BOLD}{'Company':<35} {'Industry':<30} {'Mkt Cap (INR)':>18}  Instrument Key{RESET}")
    print("  " + "─" * 105)

    for i, (name, industry, mcap, ikey) in enumerate(rows):
        color = GREEN if i == 0 else CYAN
        print(f"  {color}{name:<35}{RESET} {industry:<30} {_fmt_crore(mcap):>18}  {ikey}")

    print(f"\n  Total: {len(rows)} competitor(s)\n")


if __name__ == "__main__":
    main()
