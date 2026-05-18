"""
Key Ratios — P/E, P/B, ROE, ROCE, D/E and more vs sector peers.

Fetches key financial ratios from the Upstox Fundamentals API and prints
the company value alongside the sector average for quick comparison.

Usage:
  python fundamentals/key_ratios.py --token <TOKEN>
  python fundamentals/key_ratios.py --token <TOKEN> --symbol TCS
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
RESET = "\033[0m"


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _val(obj, key):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _fmt(v):
    if v is None:
        return "—"
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="Key Ratios via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, _ = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching key ratios for {args.symbol.upper()} (ISIN: {isin})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_key_ratios(isin)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    # data is a list of KeyRatioData or plain dicts
    items = data if isinstance(data, list) else ([data] if data else [])

    rows = []
    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        if isinstance(item, dict):
            rows.append((_val(item, "name"), _val(item, "company_value"), _val(item, "sector_value")))
        else:
            rows.append((getattr(item, "name", ""), getattr(item, "company_value", None), getattr(item, "sector_value", None)))

    if not rows:
        die("No ratio data found.")

    col_w = [36, 18, 18]
    header = f"  {BOLD}{'Ratio':<{col_w[0]}} {'Company':>{col_w[1]}} {'Sector Avg':>{col_w[2]}}{RESET}"
    print(header)
    print("  " + "─" * (col_w[0] + col_w[1] + col_w[2] + 4))

    for name, company_val, sector_val in rows:
        name_str = str(name) if name else "—"
        c_str = _fmt(company_val)
        s_str = _fmt(sector_val)

        # highlight if company beats sector on common ratios
        color = ""
        try:
            cv = float(company_val) if company_val is not None else None
            sv = float(sector_val)  if sector_val  is not None else None
            if cv is not None and sv is not None and sv != 0:
                name_lower = name_str.lower()
                # lower is better for D/E, P/E, P/B in value investing context
                if any(k in name_lower for k in ("debt", "d/e", "pe", "p/e", "p/b")):
                    color = GREEN if cv <= sv else RED
                elif any(k in name_lower for k in ("roe", "roce", "profit", "margin", "growth")):
                    color = GREEN if cv >= sv else RED
        except (TypeError, ValueError):
            pass

        print(f"  {CYAN}{name_str:<{col_w[0]}}{RESET} {color}{c_str:>{col_w[1]}}{RESET} {s_str:>{col_w[2]}}")

    print()


if __name__ == "__main__":
    main()
