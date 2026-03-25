"""
Max Pain Calculator.

Max pain is the strike price at which options buyers (as a whole) suffer the
maximum financial loss at expiry.  It's the point where the total payout to
option holders (CE + PE) is minimised.

Algorithm:
  For each candidate strike K:
    pain(K) = Σ [max(0, K - strike_i) * CE_OI_i]   ← put holders' loss
            + Σ [max(0, strike_i - K) * PE_OI_i]   ← call holders' loss
  Max pain = argmin(pain)

This script uses get_full_market_quote (which includes OI) for accuracy.

Usage:
  python options_analytics/max_pain_calculator.py --token <TOKEN>
  python options_analytics/max_pain_calculator.py --token <TOKEN> --query BANKNIFTY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_full_quote


def fetch_chain_instruments(client, query, expiry, itype, num_strikes=15):
    """Fetch option instruments across a range of ATM offsets."""
    instruments = []
    for offset in range(-num_strikes, num_strikes + 1):
        resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                 instrument_types=itype, expiry=expiry,
                                 atm_offset=offset, records=1)
        data = resp.data or []
        if data:
            instruments.append(data[0])
    # Deduplicate by strike
    seen = set()
    unique = []
    for inst in instruments:
        k = inst.get("strike_price", 0)
        if k not in seen:
            seen.add(k)
            unique.append(inst)
    return unique


def main():
    parser = argparse.ArgumentParser(description="Options max pain calculator using OI")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--strikes", type=int, default=10, help="Strikes each side of ATM (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Calculating max pain for {args.query} ({args.expiry})...\n")

    ce_insts = fetch_chain_instruments(client, args.query, args.expiry, "CE", args.strikes)
    pe_insts = fetch_chain_instruments(client, args.query, args.expiry, "PE", args.strikes)

    all_insts = ce_insts + pe_insts
    if not all_insts:
        print("No data found.")
        sys.exit(1)

    all_keys = [i["instrument_key"] for i in all_insts]
    # get_full_market_quote supports up to 500 instruments
    quote_data = get_full_quote(client, *all_keys)

    # Build OI maps by strike
    ce_oi = {}
    pe_oi = {}
    for inst in ce_insts:
        k = inst.get("strike_price", 0)
        key = inst["instrument_key"]
        q = quote_data.get(key)
        ce_oi[k] = q.oi if q else 0

    for inst in pe_insts:
        k = inst.get("strike_price", 0)
        key = inst["instrument_key"]
        q = quote_data.get(key)
        pe_oi[k] = q.oi if q else 0

    all_strikes = sorted(set(list(ce_oi.keys()) + list(pe_oi.keys())))

    # Compute pain at each strike
    pain = {}
    for candidate in all_strikes:
        total = 0
        for strike, oi in ce_oi.items():
            total += max(0, candidate - strike) * (oi or 0)
        for strike, oi in pe_oi.items():
            total += max(0, strike - candidate) * (oi or 0)
        pain[candidate] = total

    max_pain_strike = min(pain, key=pain.get)
    min_pain_val = pain[max_pain_strike]

    # Display top 10 strikes around max pain
    sorted_strikes = sorted(all_strikes, key=lambda s: abs(s - max_pain_strike))[:10]
    sorted_strikes = sorted(sorted_strikes)

    print(f"{'Strike':>10}  {'CE OI':>12}  {'PE OI':>12}  {'Pain Value':>15}  {'':}")
    print("-" * 65)
    for s in sorted_strikes:
        marker = "  <<< MAX PAIN" if s == max_pain_strike else ""
        print(f"{s:>10.0f}  {ce_oi.get(s, 0):>12,.0f}  {pe_oi.get(s, 0):>12,.0f}  "
              f"{pain.get(s, 0):>15,.0f}{marker}")

    print(f"\nMax Pain Strike : {max_pain_strike:,.0f}")
    print(f"Pain Value      : {min_pain_val:,.0f}")
    print("\nInterpretation: Underlying tends to gravitate toward max pain at expiry.")


if __name__ == "__main__":
    main()
