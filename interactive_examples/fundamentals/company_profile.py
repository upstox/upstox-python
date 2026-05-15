"""
Company Profile — sector, market cap, and business overview for an equity.

Fetches company profile data from the Upstox Fundamentals API using the
instrument's ISIN resolved from the given stock symbol.

Usage:
  python fundamentals/company_profile.py --token <TOKEN>
  python fundamentals/company_profile.py --token <TOKEN> --symbol INFY
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
    """Return (isin, instrument_key) for the first NSE EQ match."""
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _get(obj, key, default="—"):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default) or default
    return getattr(obj, key, default) or default


def fmt_crore(val):
    try:
        v = float(val)
        if v >= 1e7:
            return f"₹{v/1e7:,.2f} Cr"
        return f"₹{v:,.2f}"
    except (TypeError, ValueError):
        return str(val) if val else "—"


def main():
    parser = argparse.ArgumentParser(description="Company Profile via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, instrument_key = resolve_symbol(client, args.symbol)
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

    # data may be a model object or dict
    raw = data.to_dict() if hasattr(data, "to_dict") else (data if isinstance(data, dict) else vars(data))

    profile = raw.get("company_profile") or {}
    sector  = raw.get("sector") or {}
    mcap_inr = raw.get("sector_market_cap_inr") or {}
    mcap_usd = raw.get("sector_market_cap_usd") or {}

    if isinstance(profile, dict):
        p = profile
    else:
        p = vars(profile) if hasattr(profile, "__dict__") else {}

    if isinstance(sector, dict):
        s = sector
    else:
        s = vars(sector) if hasattr(sector, "__dict__") else {}

    print(f"  {BOLD}{'Field':<28} Value{RESET}")
    print("  " + "─" * 70)

    fields = [
        ("Company Name",    p.get("company_name") or p.get("name") or raw.get("name") or "—"),
        ("ISIN",            isin),
        ("Instrument Key",  instrument_key),
        ("Industry",        p.get("industry") or s.get("industry") or "—"),
        ("Sector",          p.get("sector") or s.get("name") or s.get("sector_name") or "—"),
        ("Sub-Sector",      p.get("sub_sector") or p.get("subsector") or "—"),
        ("Market Cap (INR)", fmt_crore(_get(mcap_inr, "market_cap") or _get(mcap_inr, "value"))),
        ("Market Cap (USD)", fmt_crore(_get(mcap_usd, "market_cap") or _get(mcap_usd, "value"))),
        ("Employees",       p.get("employees") or p.get("num_employees") or "—"),
        ("Incorporated",    p.get("incorporated") or p.get("incorporation_date") or "—"),
        ("Listing Date",    p.get("listing_date") or "—"),
        ("Website",         p.get("website") or p.get("web_url") or "—"),
    ]

    for label, value in fields:
        print(f"  {CYAN}{label:<28}{RESET} {value}")

    description = (
        p.get("description") or
        p.get("about") or
        p.get("business_description") or
        raw.get("description") or ""
    )
    if description and str(description) != "—":
        print()
        print(f"  {BOLD}About:{RESET}")
        text = str(description)
        for i in range(0, min(len(text), 600), 100):
            print(f"    {text[i:i+100]}")
        if len(text) > 600:
            print("    ...")

    print()


if __name__ == "__main__":
    main()
