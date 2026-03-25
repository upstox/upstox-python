"""
OI Skew — Put-Call Open Interest Ratio by Strike.

Compares CE OI vs PE OI across strikes to gauge market sentiment:
  - High PE OI vs CE OI at a strike → put writing (support level)
  - High CE OI vs PE OI at a strike → call writing (resistance level)
  - PCR (Put-Call OI Ratio) > 1 → more puts, slightly bullish (put writers support the market)
  - PCR < 1 → more calls, bearish signal

Usage:
  python options_analytics/oi_skew.py --token <TOKEN>
  python options_analytics/oi_skew.py --token <TOKEN> --query BANKNIFTY --strikes 8
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_full_quote


def fetch_options(client, query, expiry, itype, num_strikes):
    instruments = []
    for offset in range(-num_strikes, num_strikes + 1):
        resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                 instrument_types=itype, expiry=expiry,
                                 atm_offset=offset, records=1)
        data = resp.data or []
        if data:
            instruments.append(data[0])
    seen = set()
    unique = []
    for inst in instruments:
        k = inst.get("strike_price", 0)
        if k not in seen:
            seen.add(k)
            unique.append(inst)
    return unique


def main():
    parser = argparse.ArgumentParser(description="OI skew — put-call OI ratio by strike")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--strikes", type=int, default=7, help="Strikes each side of ATM (default: 7)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching OI skew for {args.query} ({args.expiry}), ±{args.strikes} strikes...\n")

    ce_insts = fetch_options(client, args.query, args.expiry, "CE", args.strikes)
    pe_insts = fetch_options(client, args.query, args.expiry, "PE", args.strikes)

    all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]
    quote_data = get_full_quote(client, *all_keys)

    ce_oi_map = {}
    pe_oi_map = {}
    for inst in ce_insts:
        k = inst.get("strike_price", 0)
        q = quote_data.get(inst["instrument_key"])
        ce_oi_map[k] = q.oi if q else 0
    for inst in pe_insts:
        k = inst.get("strike_price", 0)
        q = quote_data.get(inst["instrument_key"])
        pe_oi_map[k] = q.oi if q else 0

    all_strikes = sorted(set(list(ce_oi_map.keys()) + list(pe_oi_map.keys())))

    total_ce_oi = sum(ce_oi_map.values())
    total_pe_oi = sum(pe_oi_map.values())
    overall_pcr = total_pe_oi / total_ce_oi if total_ce_oi else 0

    print(f"{'Strike':>10}  {'CE OI':>12}  {'PE OI':>12}  {'PCR':>8}  {'Signal':}")
    print("-" * 65)

    max_ce_oi = max(ce_oi_map.values(), default=1)
    max_pe_oi = max(pe_oi_map.values(), default=1)

    for strike in reversed(all_strikes):
        ce_oi = ce_oi_map.get(strike, 0)
        pe_oi = pe_oi_map.get(strike, 0)
        pcr = pe_oi / ce_oi if ce_oi else 0

        signal = ""
        if ce_oi == max_ce_oi:
            signal = " <-- MAX CE OI (resistance)"
        elif pe_oi == max_pe_oi:
            signal = " <-- MAX PE OI (support)"

        print(f"{strike:>10.0f}  {ce_oi:>12,.0f}  {pe_oi:>12,.0f}  {pcr:>8.2f}{signal}")

    print("-" * 65)
    print(f"{'TOTAL':>10}  {total_ce_oi:>12,.0f}  {total_pe_oi:>12,.0f}  {overall_pcr:>8.2f}")

    print(f"\nOverall PCR : {overall_pcr:.2f}")
    if overall_pcr > 1.2:
        print("Interpretation: Heavy put writing — market likely to be supported / bullish bias.")
    elif overall_pcr < 0.8:
        print("Interpretation: Heavy call writing — market facing resistance / bearish bias.")
    else:
        print("Interpretation: Balanced OI — no strong directional bias from OI data.")

    if ce_oi_map:
        resistance = max(ce_oi_map, key=ce_oi_map.get)
        print(f"\nKey resistance (max CE OI)  : {resistance:,.0f}")
    if pe_oi_map:
        support = max(pe_oi_map, key=pe_oi_map.get)
        print(f"Key support    (max PE OI)  : {support:,.0f}")


if __name__ == "__main__":
    main()
