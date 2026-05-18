"""
Corporate Actions — dividends, splits, bonuses and other events.

Fetches the corporate action history from the Upstox Fundamentals API and
displays each event with its date, amount or ratio.

Usage:
  python fundamentals/corporate_actions.py --token <TOKEN>
  python fundamentals/corporate_actions.py --token <TOKEN> --symbol HDFCBANK
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


def main():
    parser = argparse.ArgumentParser(description="Corporate Actions via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, _ = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching corporate actions for {args.symbol.upper()} (ISIN: {isin})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_corporate_actions(isin)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    items = data if isinstance(data, list) else ([data] if data else [])

    if not items:
        die("No corporate action data found.")

    rows = []
    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        elif not isinstance(item, dict):
            item = vars(item) if hasattr(item, "__dict__") else {}

        name   = _val(item, "name")
        date   = _val(item, "expiry_date") or _val(item, "date") or _val(item, "ex_date")
        amount = _val(item, "amount")
        ratio  = _val(item, "ratio")

        # flatten event_details if present
        details = item.get("event_details") or []
        detail_str = ""
        if details:
            if isinstance(details, list):
                parts = []
                for d in details:
                    if hasattr(d, "to_dict"):
                        d = d.to_dict()
                    elif not isinstance(d, dict):
                        d = vars(d) if hasattr(d, "__dict__") else {}
                    dn = d.get("name") or ""
                    dv = d.get("value") or ""
                    if dn or dv:
                        parts.append(f"{dn}: {dv}" if dn else str(dv))
                detail_str = " | ".join(parts)
            else:
                detail_str = str(details)

        rows.append((name, date, amount, ratio, detail_str))

    # Sort by date descending (most recent first)
    rows.sort(key=lambda r: r[1], reverse=True)

    print(f"  {BOLD}{'Action':<28} {'Ex-Date':<14} {'Amount':>12} {'Ratio':>12}  Details{RESET}")
    print("  " + "─" * 90)

    for name, date, amount, ratio, details in rows:
        detail_col = details[:35] if details and details != "—" else ""
        print(f"  {CYAN}{name:<28}{RESET} {date:<14} {amount:>12} {ratio:>12}  {detail_col}")

    print(f"\n  Total: {len(rows)} corporate action(s)\n")


if __name__ == "__main__":
    main()
