"""
Competitors — peer companies in the same sector with market cap data.

Fetches the competitor list from the Upstox Fundamentals API using the
instrument_key resolved from the given stock symbol and displays each peer's
sector, sector market capitalisation and business description.

Usage:
  python fundamentals/competitors.py --token <TOKEN>
  python fundamentals/competitors.py --token <TOKEN> --symbol TCS
"""

import argparse
import sys
import os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _as_dict(obj):
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj) if hasattr(obj, "__dict__") else {}


def _instrument_to_label(ikey: str) -> str:
    """NSE_EQ|INE242A01010 → INE242A01010 (helps eyeball the symbol)."""
    if not ikey:
        return "—"
    return ikey.split("|", 1)[-1]


def _lookup_name(client, ikey: str):
    """Resolve a peer's trading symbol + company name from its instrument_key."""
    if not ikey or "|" not in ikey:
        return "—", "—"
    isin = ikey.split("|", 1)[-1]
    try:
        resp = search_instrument(client, isin, exchanges="NSE", segments="EQ", records=1)
        hits = resp.data or []
        if hits:
            h = hits[0]
            return (h.get("trading_symbol") or h.get("symbol") or "—",
                    h.get("name") or "—")
    except Exception:
        pass
    return "—", "—"


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

    items = data if isinstance(data, list) else [data]

    rows = []
    for item in items:
        item = _as_dict(item)
        ikey       = str(item.get("instrument_key") or "—")
        descr      = str(item.get("company_profile") or "")
        sector     = str(item.get("sector") or "—")
        mcap_inr   = _as_dict(item.get("sector_market_cap_inr"))
        mcap_usd   = _as_dict(item.get("sector_market_cap_usd"))
        mcap_value = mcap_inr.get("value")
        sym, name  = _lookup_name(client, ikey)
        rows.append({
            "symbol": sym,
            "name":   name,
            "ikey": ikey,
            "descr": descr,
            "sector": sector,
            "mcap_inr_formatted": str(mcap_inr.get("formatted") or "—"),
            "mcap_usd_formatted": str(mcap_usd.get("formatted") or "—"),
            "mcap_value": mcap_value,
        })

    if not rows:
        die("No competitor data found.")

    # Sort by sector market cap descending (when numeric)
    def _sort_mcap(r):
        try:
            return float(r["mcap_value"])
        except (TypeError, ValueError):
            return -1
    rows.sort(key=_sort_mcap, reverse=True)

    print(f"  {BOLD}{'Symbol':<14} {'Company':<34} {'Sector':<18} {'Sector Mkt Cap (INR)':>22}  {'(USD)':<10} Instrument Key{RESET}")
    print("  " + "─" * 130)
    for i, r in enumerate(rows):
        color = GREEN if i == 0 else CYAN
        name = (r["name"][:32] + "…") if len(r["name"]) > 33 else r["name"]
        print(f"  {color}{r['symbol']:<14}{RESET} {name:<34} {r['sector']:<18} {r['mcap_inr_formatted']:>22}  {r['mcap_usd_formatted']:<10} {r['ikey']}")

    print()
    for i, r in enumerate(rows, 1):
        if not r["descr"]:
            continue
        header = r["name"] if r["name"] != "—" else r["ikey"]
        print(f"  {BOLD}{i}. {header}{RESET} {DIM}({r['symbol']} · {r['sector']}){RESET}")
        wrapped = textwrap.wrap(r["descr"], width=92)
        for line in wrapped[:4]:
            print(f"     {line}")
        if len(wrapped) > 4:
            print(f"     {DIM}...{RESET}")
        print()

    print(f"  Total: {len(rows)} competitor(s)\n")


if __name__ == "__main__":
    main()
