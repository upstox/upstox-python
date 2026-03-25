"""
Option Chain (Native API) — full CE/PE chain via the dedicated OptionsApi endpoint.

This is cleaner and more complete than the search-based approach already in the project.
Returns OI, LTP, and IV for every strike at the given expiry, with the ATM row marked.

Usage:
  python options_analytics/option_chain_native.py --token <TOKEN>
  python options_analytics/option_chain_native.py --token <TOKEN> --query BANKNIFTY --expiry 2026-04-17
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

# Underlying instrument key map
INDEX_KEYS = {
    "NIFTY":      "NSE_INDEX|Nifty 50",
    "BANKNIFTY":  "NSE_INDEX|Nifty Bank",
    "FINNIFTY":   "NSE_INDEX|Nifty Fin Service",
    "MIDCPNIFTY": "NSE_INDEX|NIFTY MID SELECT",
    "SENSEX":     "BSE_INDEX|SENSEX",
}


def get_underlying_key(client, query: str) -> str:
    upper = query.upper()
    if upper in INDEX_KEYS:
        return INDEX_KEYS[upper]
    # Try searching as equity
    resp = search_instrument(client, query, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if hits:
        return hits[0]["instrument_key"]
    print(f"Cannot resolve underlying for '{query}'.")
    sys.exit(1)


def get_nearest_expiry(client, query: str) -> str:
    """Find the nearest expiry from options search."""
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types="CE", expiry="current_month", records=1)
    hits = resp.data or []
    if hits:
        return hits[0].get("expiry", "")
    return ""


def extract(obj, *keys, default=0):
    """Safely get a nested attribute/key from SDK object or dict."""
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)
    return obj if obj is not None else default


def main():
    parser = argparse.ArgumentParser(description="Full option chain via OptionsApi")
    parser.add_argument("--token",  required=True,  help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying (default: NIFTY)")
    parser.add_argument("--expiry", default="",
                        help="Expiry date YYYY-MM-DD (default: current month nearest)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    underlying_key = get_underlying_key(client, args.query)
    expiry = args.expiry or get_nearest_expiry(client, args.query)
    if not expiry:
        print("Could not determine expiry. Use --expiry YYYY-MM-DD.")
        sys.exit(1)

    print(f"\nFetching option chain for {args.query.upper()} | expiry: {expiry}...\n")

    api  = upstox_client.OptionsApi(client)
    resp = api.get_put_call_option_chain(underlying_key, expiry)
    chain = resp.data if resp.data else []
    if not isinstance(chain, list):
        chain = [chain]

    if not chain:
        print("No option chain data returned.")
        sys.exit(1)

    # Find ATM: strike closest to underlying LTP
    # underlying LTP comes from the first chain entry's underlying_spot_price or pcr
    spot = None
    for entry in chain:
        spot = extract(entry, "underlying_spot_price") or extract(entry, "spot_price")
        if spot:
            break

    rows = []
    for entry in chain:
        strike = extract(entry, "strike_price")
        ce     = extract(entry, "call_options")
        pe     = extract(entry, "put_options")

        ce_ltp = extract(ce, "market_data", "ltp")
        ce_oi  = extract(ce, "market_data", "oi")
        ce_iv  = extract(ce, "option_greeks", "iv")
        pe_ltp = extract(pe, "market_data", "ltp")
        pe_oi  = extract(pe, "market_data", "oi")
        pe_iv  = extract(pe, "option_greeks", "iv")

        rows.append((strike, ce_oi, ce_ltp, ce_iv, pe_ltp, pe_oi, pe_iv))

    rows.sort(key=lambda r: r[0])

    # Determine ATM strike
    if spot:
        atm_strike = min(rows, key=lambda r: abs(r[0] - spot))[0]
    else:
        atm_strike = rows[len(rows) // 2][0]

    # Header
    print(f"{'':2} {'Strike':>10}  {'CE OI':>12}  {'CE LTP':>10}  {'CE IV':>7}  "
          f"{'PE LTP':>10}  {'PE OI':>12}  {'PE IV':>7}")
    print("─" * 88)

    for strike, ce_oi, ce_ltp, ce_iv, pe_ltp, pe_oi, pe_iv in rows:
        is_atm = strike == atm_strike
        marker = f"{CYAN}→{RESET}" if is_atm else "  "
        ce_col = BOLD if is_atm else ""
        pe_col = BOLD if is_atm else ""

        ce_iv_s  = f"{ce_iv*100:.1f}%"  if ce_iv  else "—"
        pe_iv_s  = f"{pe_iv*100:.1f}%"  if pe_iv  else "—"
        ce_ltp_s = f"{ce_ltp:,.2f}"     if ce_ltp else "—"
        pe_ltp_s = f"{pe_ltp:,.2f}"     if pe_ltp else "—"
        ce_oi_s  = f"{int(ce_oi):,}"    if ce_oi  else "—"
        pe_oi_s  = f"{int(pe_oi):,}"    if pe_oi  else "—"

        print(f"{marker} {ce_col}{strike:>10,.0f}  "
              f"{GREEN}{ce_oi_s:>12}{RESET}  {ce_col}{ce_ltp_s:>10}{RESET}  {ce_iv_s:>7}  "
              f"{pe_col}{pe_ltp_s:>10}{RESET}  {RED}{pe_oi_s:>12}{RESET}  {pe_iv_s:>7}")

    print("─" * 88)
    if spot:
        print(f"\n  {BOLD}Spot price: {spot:,.2f}{RESET}  |  ATM strike: {atm_strike:,.0f}  |  Expiry: {expiry}")
    total_ce_oi = sum(r[1] for r in rows if r[1])
    total_pe_oi = sum(r[5] for r in rows if r[5])
    if total_ce_oi and total_pe_oi:
        pcr = total_pe_oi / total_ce_oi
        print(f"  Total CE OI: {int(total_ce_oi):,}  |  Total PE OI: {int(total_pe_oi):,}  "
              f"|  PCR: {pcr:.2f}  ({'bullish' if pcr > 1 else 'bearish'})")
    print()


if __name__ == "__main__":
    main()
