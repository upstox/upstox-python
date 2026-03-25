"""
Volatility Skew — OTM Put Premium vs OTM Call Premium.

Volatility skew measures the difference in implied volatility (or simply
option premium) between OTM puts and OTM calls at equal distance from ATM.

In equities/indices, OTM puts typically trade at higher premiums than
equidistant OTM calls (negative skew), reflecting demand for downside protection.

This script:
  - Fetches CE and PE premiums across ATM offsets -N to +N
  - Computes the skew ratio: PE_premium / CE_premium at each symmetric pair
  - Plots a simple text chart

Usage:
  python options_analytics/volatility_skew.py --token <TOKEN>
  python options_analytics/volatility_skew.py --token <TOKEN> --query BANKNIFTY --depth 5
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def fetch_one(client, query, expiry, itype, offset):
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types=itype, expiry=expiry,
                             atm_offset=offset, records=1)
    data = resp.data or []
    return data[0] if data else None


def main():
    parser = argparse.ArgumentParser(description="Options volatility skew viewer")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--depth", type=int, default=4, help="OTM depth in strikes (default: 4)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching volatility skew for {args.query} ({args.expiry}), depth={args.depth}...\n")

    rows = []
    all_keys = []
    for offset in range(1, args.depth + 1):
        ce = fetch_one(client, args.query, args.expiry, "CE", +offset)
        pe = fetch_one(client, args.query, args.expiry, "PE", -offset)
        if ce and pe:
            rows.append((offset, ce, pe))
            all_keys += [ce["instrument_key"], pe["instrument_key"]]

    # Also get ATM
    atm_ce = fetch_one(client, args.query, args.expiry, "CE", 0)
    atm_pe = fetch_one(client, args.query, args.expiry, "PE", 0)
    if atm_ce:
        all_keys.append(atm_ce["instrument_key"])
    if atm_pe:
        all_keys.append(atm_pe["instrument_key"])

    if not all_keys:
        print("No data found.")
        sys.exit(1)

    ltp_data = get_ltp(client, *all_keys)

    def price(inst):
        if not inst:
            return 0.0
        return ltp_data.get(inst["instrument_key"], type("", (), {"last_price": 0.0})()).last_price

    atm_ce_price = price(atm_ce)
    atm_pe_price = price(atm_pe)
    atm_strike = atm_ce.get("strike_price", 0) if atm_ce else 0

    print(f"ATM Strike : {atm_strike:,.0f}")
    print(f"ATM CE     : {atm_ce_price:.2f}")
    print(f"ATM PE     : {atm_pe_price:.2f}")
    print(f"ATM Skew   : PE/CE = {atm_pe_price/atm_ce_price:.3f}" if atm_ce_price else "")
    print()

    print(f"{'Offset':<8} {'CE Strike':>10} {'CE LTP':>10} {'PE Strike':>10} {'PE LTP':>10} {'PE/CE Ratio':>12} {'Skew Bar':}")
    print("-" * 85)

    for offset, ce, pe in rows:
        ce_price = price(ce)
        pe_price = price(pe)
        ratio = pe_price / ce_price if ce_price else 0
        bar_len = min(int(ratio * 10), 40)
        bar = "█" * bar_len

        print(f"{'+' + str(offset) + '/-' + str(offset):<8} "
              f"{ce.get('strike_price',0):>10.0f} {ce_price:>10.2f} "
              f"{pe.get('strike_price',0):>10.0f} {pe_price:>10.2f} "
              f"{ratio:>12.3f}  {bar}")

    print("\nInterpretation:")
    print("  PE/CE ratio > 1.0 → puts trade at premium over equidistant calls (normal negative skew)")
    print("  PE/CE ratio < 1.0 → calls premium over puts (positive/reverse skew — unusual)")
    print("  Rising ratio at deeper OTM → heavy demand for tail risk protection")


if __name__ == "__main__":
    main()
