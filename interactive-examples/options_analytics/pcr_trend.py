"""
Put-Call Ratio (PCR) Trend — OI-based sentiment gauge via the native Option Chain API.

Fetches the full option chain for a given underlying and expiry, sums CE OI vs PE OI
across all strikes, and computes the overall PCR plus a per-strike breakdown.

  PCR > 1.2  → heavy put writing → bullish bias (support from put writers)
  PCR < 0.8  → heavy call writing → bearish bias (resistance from call writers)
  0.8–1.2    → balanced / neutral

Usage:
  python options_analytics/pcr_trend.py --token <TOKEN>
  python options_analytics/pcr_trend.py --token <TOKEN> --query BANKNIFTY --expiry 2026-04-17
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
RESET = "\033[0m"

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
    resp = search_instrument(client, query, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if hits:
        return hits[0]["instrument_key"]
    print(f"Cannot resolve underlying for '{query}'.")
    sys.exit(1)


def get_nearest_expiry(client, query: str) -> str:
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types="CE", expiry="current_month", records=1)
    hits = resp.data or []
    if hits:
        return hits[0].get("expiry", "")
    return ""


def extract(obj, *keys, default=0):
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)
    return obj if obj is not None else default


def main():
    parser = argparse.ArgumentParser(description="Put-Call Ratio from option chain OI")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying (default: NIFTY)")
    parser.add_argument("--expiry", default="", help="Expiry YYYY-MM-DD (default: current month)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    underlying_key = get_underlying_key(client, args.query)
    expiry = args.expiry or get_nearest_expiry(client, args.query)
    if not expiry:
        print("Could not determine expiry. Use --expiry YYYY-MM-DD.")
        sys.exit(1)

    print(f"\nFetching PCR for {args.query.upper()} | expiry: {expiry}...\n")

    api = upstox_client.OptionsApi(client)
    resp = api.get_put_call_option_chain(underlying_key, expiry)
    chain = resp.data if resp.data else []
    if not isinstance(chain, list):
        chain = [chain]

    if not chain:
        print("No option chain data returned.")
        sys.exit(1)

    # Collect per-strike OI
    rows = []
    for entry in chain:
        strike = extract(entry, "strike_price")
        ce_oi = extract(entry, "call_options", "market_data", "oi")
        pe_oi = extract(entry, "put_options", "market_data", "oi")
        rows.append((strike, ce_oi, pe_oi))

    rows.sort(key=lambda r: r[0])

    total_ce_oi = sum(r[1] for r in rows if r[1])
    total_pe_oi = sum(r[2] for r in rows if r[2])
    overall_pcr = total_pe_oi / total_ce_oi if total_ce_oi else 0

    # Header
    print(f"{'Strike':>10}  {'CE OI':>12}  {'PE OI':>12}  {'PCR':>8}  Signal")
    print("-" * 65)

    max_ce = max((r[1] for r in rows if r[1]), default=0)
    max_pe = max((r[2] for r in rows if r[2]), default=0)

    for strike, ce_oi, pe_oi in rows:
        pcr = pe_oi / ce_oi if ce_oi else 0
        signal = ""
        if ce_oi and ce_oi == max_ce:
            signal = " <-- MAX CE OI (resistance)"
        elif pe_oi and pe_oi == max_pe:
            signal = " <-- MAX PE OI (support)"

        ce_s = f"{int(ce_oi):,}" if ce_oi else "—"
        pe_s = f"{int(pe_oi):,}" if pe_oi else "—"
        print(f"{strike:>10,.0f}  {GREEN}{ce_s:>12}{RESET}  {RED}{pe_s:>12}{RESET}  {pcr:>8.2f}{signal}")

    print("-" * 65)
    print(f"{'TOTAL':>10}  {GREEN}{int(total_ce_oi):>12,}{RESET}  "
          f"{RED}{int(total_pe_oi):>12,}{RESET}  {BOLD}{overall_pcr:>8.2f}{RESET}")

    print(f"\n{BOLD}Overall PCR: {overall_pcr:.2f}{RESET}")
    if overall_pcr > 1.2:
        print(f"  {GREEN}Bullish bias{RESET} — heavy put writing, market likely supported.")
    elif overall_pcr < 0.8:
        print(f"  {RED}Bearish bias{RESET} — heavy call writing, market facing resistance.")
    else:
        print(f"  {CYAN}Neutral{RESET} — balanced OI, no strong directional signal.")

    if rows:
        resistance = max(rows, key=lambda r: r[1])[0]
        support = max(rows, key=lambda r: r[2])[0]
        print(f"\n  Key resistance (max CE OI): {resistance:,.0f}")
        print(f"  Key support    (max PE OI): {support:,.0f}")
    print()


if __name__ == "__main__":
    main()
