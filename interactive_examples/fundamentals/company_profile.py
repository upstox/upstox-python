"""
Company Profile — business description, sector, and sector market cap.

Fetches company profile data from the Upstox Fundamentals API using the
instrument's ISIN resolved from the given stock symbol.

Usage:
  python fundamentals/company_profile.py --token <TOKEN>
  python fundamentals/company_profile.py --token <TOKEN> --symbol INFY
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
    """Return (isin, instrument_key, name) for the first NSE EQ match."""
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    h = hits[0]
    return h.get("isin", ""), h.get("instrument_key", ""), h.get("name", "")


def _as_dict(obj):
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj) if hasattr(obj, "__dict__") else {}


def _fmt_mcap(mcap: dict) -> str:
    if not mcap:
        return "—"
    formatted = mcap.get("formatted")
    if formatted:
        return str(formatted)
    value = mcap.get("value")
    unit  = mcap.get("unit") or ""
    if value is None:
        return "—"
    return f"{value:,.2f} {unit}".strip()


def main():
    parser = argparse.ArgumentParser(description="Company Profile via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, instrument_key, sym_name = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching company profile for {args.symbol.upper()} (ISIN: {isin})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_company_profile(isin)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    raw = _as_dict(data)

    description = raw.get("company_profile") or ""
    sector      = raw.get("sector") or "—"
    mcap_inr    = _as_dict(raw.get("sector_market_cap_inr"))
    mcap_usd    = _as_dict(raw.get("sector_market_cap_usd"))

    print(f"  {BOLD}{'Field':<22} Value{RESET}")
    print("  " + "─" * 70)
    fields = [
        ("Symbol",                args.symbol.upper()),
        ("Name",                  sym_name or "—"),
        ("ISIN",                  isin),
        ("Instrument Key",        instrument_key),
        ("Sector",                str(sector)),
        ("Sector Market Cap INR", _fmt_mcap(mcap_inr)),
        ("Sector Market Cap USD", _fmt_mcap(mcap_usd)),
    ]
    for label, value in fields:
        print(f"  {CYAN}{label:<22}{RESET} {value}")

    if description:
        print()
        print(f"  {BOLD}Business Description:{RESET}")
        wrapped = textwrap.wrap(str(description), width=92)
        for line in wrapped:
            print(f"    {line}")

    print()
    print(f"  {DIM}Note: sector market cap is the aggregate for the '{sector}' sector, "
          f"not the company's own market cap.{RESET}")
    print()


if __name__ == "__main__":
    main()
